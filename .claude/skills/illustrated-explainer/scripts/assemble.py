#!/usr/bin/env python3
"""assemble.py - build the finished video from still images + narration (stdlib + ffmpeg only).

  shots.json + voice.mp3 [+ music] [+ captions.srt]  ->  1920x1080 (or 1080x1920) 30 fps MP4

What it does
  * Ken Burns motion on every still (zoompan on a 2x upscaled copy, so it does not jitter)
  * short crossfades between shots (per-shot "transition": "cut" for a hard cut)
  * keeps picture and voice in sync: shot times come from start/end (or duration_s) and the
    last shot is stretched or trimmed so the video ends exactly with the audio
  * optional music bed: lowered to --music-db (default -18 dB) and ducked under the voice
    with sidechaincompress, faded in/out
  * on-screen titles ("AKBAR - 1556") drawn by libass, so Devanagari is shaped correctly
  * captions burned in (--subs burn) or added as a soft subtitle track (--subs soft)
  * --vertical: 1080x1920 for Shorts/Reels, blurred-fill background (default) or centre crop

shots.json (a list, or {"shots": [...]}; paths are relative to the shots.json folder)
  [{"image": "images/shot_001.png",       # PNG/JPG/WebP still, or a short .mp4/.mov hero clip
    "start": 0.0, "end": 5.1,              # or "duration_s": 5.1
    "motion": "zoom_in",                   # zoom_in | zoom_out | pan_left | pan_right |
                                           # pan_up | pan_down | static
    "title": "MAURYA EMPIRE - 321 BCE",    # optional top title (added as text, not in the image)
    "caption": "...",                      # optional per-shot bottom text, used only when no --srt
    "transition": "fade"}]                 # optional: fade (default) | cut  (into the NEXT shot)

Examples
  python assemble.py shots.json --audio voice.mp3 -o video.mp4
  python assemble.py shots.json --audio voice.mp3 --music bed.mp3 --srt voice.srt --subs burn -o video.mp4
  python assemble.py shots.json --audio voice.mp3 --vertical --vfill blur --srt voice.srt -o short.mp4
  python assemble.py shots.json --audio voice.mp3 --srt voice.srt --subs soft --sub-lang hin -o video.mp4

Requires ffmpeg/ffprobe (tested with ffmpeg 6.1) built with libx264 and libass.
"""
import argparse
import concurrent.futures as cf
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

VIDEO_EXT = (".mp4", ".mov", ".webm", ".mkv", ".m4v")
MOTIONS = ("zoom_in", "zoom_out", "pan_left", "pan_right", "pan_up", "pan_down", "static")
DEVANAGARI = re.compile(r"[ऀ-ॿ]")
VERBOSE = False


def die(msg):
    sys.exit("assemble: " + msg)


def log(msg):
    print("assemble: " + msg, file=sys.stderr)


def run(cmd, cwd=None):
    if VERBOSE:
        log("$ " + " ".join(cmd))
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
    if r.returncode != 0:
        die("ffmpeg failed:\n  %s\n%s" % (" ".join(cmd), r.stderr[-3000:]))
    return r


def probe_duration(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                        "default=nw=1:nk=1", path], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        die("could not read duration of %s" % path)


# ------------------------------------------------------------------ timing
def load_shots(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    shots = data["shots"] if isinstance(data, dict) else data
    if not shots:
        die("no shots in " + path)
    base = os.path.dirname(os.path.abspath(path))
    for n, s in enumerate(shots):
        if "image" not in s:
            die("shot %d has no image" % (n + 1))
        s["_path"] = s["image"] if os.path.isabs(s["image"]) else os.path.join(base, s["image"])
        if not os.path.exists(s["_path"]):
            die("shot %d: image not found: %s" % (n + 1, s["_path"]))
        m = s.get("motion", "zoom_in")
        if m == "auto":
            m = ("zoom_in", "pan_right", "zoom_out", "pan_left")[n % 4]
        if m not in MOTIONS:
            die("shot %d: unknown motion %r (use one of %s)" % (n + 1, m, ", ".join(MOTIONS)))
        s["_motion"] = m
        s["_size"] = probe_size(s["_path"])
        if s["_size"][0] < 960 or s["_size"][1] < 540:
            log("note: shot %d image is only %dx%d; it will look soft (use 1920x1080 or larger)"
                % (n + 1, s["_size"][0], s["_size"][1]))
    return shots, (data.get("audio") if isinstance(data, dict) else None), base


def shot_durations(shots):
    """Contiguous durations. start/end wins (gaps go to the earlier shot); else duration_s."""
    if all("start" in s for s in shots):
        starts = [float(s["start"]) for s in shots]
        starts[0] = 0.0
        d = [starts[k + 1] - starts[k] for k in range(len(shots) - 1)]
        last = shots[-1]
        d.append(float(last["end"]) - starts[-1] if "end" in last else float(last.get("duration_s", 5)))
    else:
        d = [float(s.get("duration_s", 5)) for s in shots]
    for k, x in enumerate(d):
        if x <= 0:
            die("shot %d has a non-positive duration (%.3f s); check start/end" % (k + 1, x))
    return d


def fit_to(d, total):
    """Stretch/trim the tail so sum(d) == total."""
    s = sum(d)
    if abs(s - total) < 1e-3:
        return d
    d = list(d)
    if s < total:
        log("shots end at %.2f s, audio at %.2f s: holding the last shot %.2f s longer" % (s, total, total - s))
        d[-1] += total - s
        return d
    log("shots run %.2f s past the audio: trimming the tail" % (s - total))
    n0 = len(d)
    while len(d) > 1 and sum(d) - d[-1] >= total - 0.5:
        d.pop()
    d[-1] = total - sum(d[:-1])
    if len(d) < n0:
        log("dropped shot(s) %d-%d: they start after the narration ends" % (len(d) + 1, n0))
    return d


# ------------------------------------------------------------------ per-shot clips
def motion_expr(m, n, zoom):
    N = max(n - 1, 1)
    p = "(on/%d)" % N
    cx, cy = "(iw-iw/zoom)/2", "(ih-ih/zoom)/2"
    Z = 1 + zoom
    if m == "zoom_in":
        return "1+%g*%s" % (zoom, p), cx, cy
    if m == "zoom_out":
        return "1+%g*(1-%s)" % (zoom, p), cx, cy
    if m == "pan_right":
        return "%g" % Z, "(iw-iw/zoom)*%s" % p, cy
    if m == "pan_left":
        return "%g" % Z, "(iw-iw/zoom)*(1-%s)" % p, cy
    if m == "pan_down":
        return "%g" % Z, cx, "(ih-ih/zoom)*%s" % p
    if m == "pan_up":
        return "%g" % Z, cx, "(ih-ih/zoom)*(1-%s)" % p
    return "1", "0", "0"  # static


def probe_size(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=width,height", "-of", "csv=p=0:s=x", path], capture_output=True, text=True)
    try:
        w, h = r.stdout.strip().splitlines()[0].split("x")[:2]
        return int(w), int(h)
    except (ValueError, IndexError):
        die("could not read the picture size of %s (not an image/video ffmpeg can open?)" % path)


def fit_still(src, w, h, work):
    """Image far from the target aspect (e.g. a portrait still in a 16:9 video): put the whole
    picture on a blurred copy of itself instead of cropping most of it away."""
    st = os.stat(src)
    tag = hashlib.sha1(json.dumps([src, st.st_mtime, st.st_size, w, h]).encode()).hexdigest()[:10]
    out = os.path.join(work, "fit_%s.png" % tag)
    if not os.path.exists(out):
        fc = ("[0:v]split=2[a][b];[a]scale=%d:%d:force_original_aspect_ratio=increase,crop=%d:%d,boxblur=20:2,"
              "eq=brightness=-0.08:saturation=0.85[bg];[b]scale=%d:%d:force_original_aspect_ratio=decrease[fg];"
              "[bg][fg]overlay=(W-w)/2:(H-h)/2" % (w, h, w, h, w, h))
        run(["ffmpeg", "-v", "error", "-y", "-i", src, "-filter_complex", fc, "-frames:v", "1", out])
    return out


def kb_chain(label_in, label_out, m, n, w, h, zoom, fps, up):
    z, x, y = motion_expr(m, n, zoom)
    W, H = w * up, h * up
    return ("[%s]scale=%d:%d:force_original_aspect_ratio=increase:flags=lanczos,crop=%d:%d,setsar=1,"
            "zoompan=z='%s':x='%s':y='%s':d=%d:s=%dx%d:fps=%d[%s]"
            % (label_in, W, H, W, H, z, x, y, n, w, h, fps, label_out))


def video_chain(label_in, label_out, n, w, h, fps):
    return ("[%s]scale=%d:%d:force_original_aspect_ratio=increase,crop=%d:%d,setsar=1,fps=%d,"
            "trim=end_frame=%d,setpts=PTS-STARTPTS[%s]" % (label_in, w, h, w, h, fps, n, label_out))


def render_clip(job):
    s, n, out, cfg = job["shot"], job["frames"], job["out"], job["cfg"]
    if os.path.exists(out) and os.path.getsize(out) > 0:
        return out
    is_vid = s["_path"].lower().endswith(VIDEO_EXT)
    W, H, fps = cfg["W"], cfg["H"], cfg["fps"]
    src = s["_path"]
    if not is_vid and cfg["fit"]:
        # frame the picture is cropped into: the 16:9 band for vertical blur-fill, else the output
        tw, th = (W, int(round(W * 9 / 16 / 2)) * 2) if (cfg["vertical"] and cfg["vfill"] == "blur") else (W, H)
        iw, ih = s["_size"]
        if max(iw / ih, tw / th) / min(iw / ih, tw / th) > 1.25:
            src = fit_still(src, tw, th, cfg["work"])
    inp = (["-stream_loop", "-1"] if is_vid else []) + ["-i", src]
    if cfg["vertical"] and cfg["vfill"] == "blur":
        fw, fh = W, int(round(W * 9 / 16 / 2)) * 2  # 1080x608 foreground band
        fg = (video_chain("f0", "fg", n, fw, fh, fps) if is_vid else
              kb_chain("f0", "fg", s["_motion"], n, fw, fh, cfg["zoom"], fps, cfg["up"]))
        bg_src = "[b0]scale=%d:%d:force_original_aspect_ratio=increase,crop=%d:%d,boxblur=12:2," \
                 "eq=brightness=-0.10:saturation=0.85,scale=%d:%d,setsar=1" % (W // 6, H // 6, W // 6, H // 6, W, H)
        if is_vid:
            bg = bg_src + ",fps=%d,trim=end_frame=%d,setpts=PTS-STARTPTS[bg]" % (fps, n)
        else:
            bg = bg_src + ",loop=loop=%d:size=1,fps=%d,trim=end_frame=%d,setpts=PTS-STARTPTS[bg]" % (n, fps, n)
        fc = "[0:v]split=2[f0][b0];%s;%s;[bg][fg]overlay=(W-w)/2:(H-h)/2,format=yuv420p[v]" % (fg, bg)
    else:
        fc = (video_chain("0:v", "k", n, W, H, fps) if is_vid else
              kb_chain("0:v", "k", s["_motion"], n, W, H, cfg["zoom"], fps, cfg["up"]))
        fc += ";[k]format=yuv420p[v]"
    tmp = out + ".part.mp4"
    run(["ffmpeg", "-v", "error", "-y"] + inp + ["-filter_complex", fc, "-map", "[v]", "-an",
         "-frames:v", str(n), "-r", str(fps), "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
         "-pix_fmt", "yuv420p", tmp])
    os.replace(tmp, out)
    return out


# ------------------------------------------------------------------ joining
def join_filter(n_inputs, nominal, ext, fps, first_index=0):
    """xfade chain. Clip k is nominal[k]+ext[k] frames long; ext[k] is the overlap into clip k+1.
    Returns (filter, out_label). Output length = sum(nominal) + ext[-1] frames."""
    parts = []
    for k in range(n_inputs):
        parts.append("[%d:v]settb=AVTB,setpts=PTS-STARTPTS,fps=%d,format=yuv420p[c%d]" % (first_index + k, fps, k))
    if n_inputs == 1:
        return ";".join(parts), "c0"
    if all(e == 0 for e in ext[:-1]):
        parts.append("".join("[c%d]" % k for k in range(n_inputs)) + "concat=n=%d:v=1:a=0[j]" % n_inputs)
        return ";".join(parts), "j"
    acc, offset = "c0", 0
    for k in range(1, n_inputs):
        offset += nominal[k - 1]
        dur = max(ext[k - 1], 1)
        lab = "x%d" % k
        parts.append("[%s][c%d]xfade=transition=fade:duration=%.6f:offset=%.6f[%s]"
                     % (acc, k, dur / fps, offset / fps, lab))
        acc = lab
    return ";".join(parts), acc


def join_chunk(files, nominal, ext, fps, out):
    fc, lab = join_filter(len(files), nominal, ext, fps)
    cmd = ["ffmpeg", "-v", "error", "-y"]
    for f in files:
        cmd += ["-i", f]
    total = sum(nominal) + ext[-1]
    cmd += ["-filter_complex", fc, "-map", "[%s]" % lab, "-frames:v", str(total), "-r", str(fps),
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", out]
    run(cmd)


# ------------------------------------------------------------------ subtitles / titles (ASS)
def parse_srt(path):
    with open(path, encoding="utf-8-sig") as f:
        blocks = re.split(r"\n\s*\n", f.read().replace("\r", "").strip())
    out = []
    for b in blocks:
        lines = b.split("\n")
        for i, ln in enumerate(lines):
            m = re.match(r"(\d+):(\d+):(\d+)[,.](\d+)\s*-->\s*(\d+):(\d+):(\d+)[,.](\d+)", ln)
            if m:
                g = [int(x) for x in m.groups()]
                a = g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000
                e = g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000
                out.append((a, e, "\n".join(lines[i + 1:]).strip()))
                break
    return out


def ass_time(t):
    t = max(0.0, t)
    cs = int(round(t * 100))
    h, cs = divmod(cs, 360000)
    m, cs = divmod(cs, 6000)
    s, cs = divmod(cs, 100)
    return "%d:%02d:%02d.%02d" % (h, m, s, cs)


def ass_text(t):
    t = re.sub(r"<[^>]+>", "", t).replace("\\", "\\\\").replace("{", "(").replace("}", ")")
    return t.replace("\n", "\\N")


def write_ass(path, cfg, titles, captions, font, title_font):
    W, H = cfg["W"], cfg["H"]
    if cfg["vertical"]:
        t_size, c_size = int(W * 0.075), int(W * 0.058)
        band = int(round(W * 9 / 16))
        if cfg["vfill"] == "blur":
            t_margin = max(40, (H - band) // 2 - int(t_size * 2.4))
            c_margin = max(60, (H - band) // 2 - int(c_size * 3.2))
        else:
            t_margin, c_margin = int(H * 0.12), int(H * 0.2)
    else:
        t_size, c_size = int(H * 0.068), int(H * 0.05)
        t_margin, c_margin = int(H * 0.06), int(H * 0.065)
    # letter-spacing breaks Devanagari shaping in libass (dotted circles), so only space Latin titles
    spacing = 0 if any(DEVANAGARI.search(t[2]) for t in titles) else 2
    head = """[Script Info]
ScriptType: v4.00+
PlayResX: %d
PlayResY: %d
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Title,%s,%d,&H00E3F8FC,&H00E3F8FC,&H00090C0A,&H80000000,-1,0,0,0,100,100,%d,0,1,%d,2,8,60,60,%d,1
Style: Cap,%s,%d,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,%d,1,2,80,80,%d,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""" % (W, H, title_font, t_size, spacing, max(3, t_size // 12), t_margin, font, c_size, max(3, c_size // 12), c_margin)
    ev = []
    for a, e, txt in titles:
        ev.append("Dialogue: 1,%s,%s,Title,,0,0,0,,{\\fad(250,250)}%s" % (ass_time(a), ass_time(e), ass_text(txt)))
    for a, e, txt in captions:
        ev.append("Dialogue: 0,%s,%s,Cap,,0,0,0,,%s" % (ass_time(a), ass_time(e), ass_text(txt)))
    with open(path, "w", encoding="utf-8") as f:
        f.write(head + "\n".join(ev) + "\n")


HINDI_FONTS = ("Noto Sans Devanagari", "Mukta", "Hind", "Poppins", "Nirmala UI", "Lohit Devanagari",
               "Kohinoor Devanagari", "FreeSans", "FreeSerif")


def pick_hindi_font(fontsdir):
    """An installed family that has Devanagari glyphs (fontconfig), else the first default."""
    fams = set()
    if shutil.which("fc-list"):
        r = subprocess.run(["fc-list", ":lang=hi", "family"], capture_output=True, text=True)
        for ln in r.stdout.splitlines():
            fams.update(x.strip() for x in ln.split(","))
    for f in HINDI_FONTS:
        if f in fams:
            return f
    if shutil.which("fc-list") and not fontsdir:
        log("WARNING: no Devanagari font found (fc-list :lang=hi is empty). Hindi text will show as boxes. "
            "Install Noto Sans Devanagari / Mukta, or pass --fontsdir fonts/ --font \"<family>\"")
    return HINDI_FONTS[0]


# ------------------------------------------------------------------ main
def main():
    global VERBOSE
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("shots", help="shots.json")
    ap.add_argument("--audio", help="narration audio (default: the 'audio' field of shots.json)")
    ap.add_argument("-o", "--out", default="video.mp4", help="output MP4 (default video.mp4)")
    ap.add_argument("--music", help="optional music bed (looped to length)")
    ap.add_argument("--music-db", type=float, default=-18.0, help="music gain in dB before ducking (default -18)")
    ap.add_argument("--no-duck", action="store_true", help="do not duck music under the voice")
    ap.add_argument("--srt", help="captions .srt (e.g. from make_voice.py)")
    ap.add_argument("--subs", choices=["burn", "soft", "none"], default="burn",
                    help="burn captions into the picture, add a soft track, or none (default burn when --srt given)")
    ap.add_argument("--sub-lang", default=None, help="ISO 639-2 language tag for soft subs, e.g. hin or eng (default: detect)")
    ap.add_argument("--no-titles", action="store_true", help="ignore the 'title' fields")
    ap.add_argument("--title-key", default="title", help="shots.json field used for titles (default title; e.g. title_hi)")
    ap.add_argument("--font", help="caption font family (default for Hindi: the first installed of Noto Sans "
                                   "Devanagari, Mukta, Hind, Nirmala UI, ..., FreeSans; else Arial)")
    ap.add_argument("--title-font", help="title font family (default: same as --font)")
    ap.add_argument("--fontsdir", help="folder of extra .ttf/.otf fonts for titles/captions (e.g. Mukta, Oswald)")
    ap.add_argument("--vertical", action="store_true", help="1080x1920 output for Shorts/Reels")
    ap.add_argument("--vfill", choices=["blur", "crop"], default="blur", help="vertical: blurred fill (default) or centre crop")
    ap.add_argument("--size", help="output size WxH (default 1920x1080, or 1080x1920 with --vertical)")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--fade", type=float, default=0.4, help="crossfade seconds between shots (0 = hard cuts; default 0.4)")
    ap.add_argument("--zoom", type=float, default=0.12, help="Ken Burns zoom amount (default 0.12 = 12%%)")
    ap.add_argument("--upscale", type=int, default=2, help="upscale factor before zoompan to avoid jitter (default 2)")
    ap.add_argument("--no-fit", action="store_true", help="do not stretch/trim shots to the audio length")
    ap.add_argument("--crop-all", action="store_true", help="always centre-crop stills to the frame (default: a still whose "
                                                          "aspect differs by >25%%, e.g. portrait in 16:9, is shown whole on a blurred fill)")
    ap.add_argument("--no-loudnorm", action="store_true", help="skip loudness normalisation (default: -14 LUFS)")
    ap.add_argument("--crf", type=int, default=20, help="final x264 CRF (default 20)")
    ap.add_argument("--preset", default="medium", help="final x264 preset (default medium)")
    ap.add_argument("--chunk", type=int, default=20, help="shots joined per intermediate chunk (default 20)")
    ap.add_argument("--jobs", type=int, default=max(1, (os.cpu_count() or 2) // 2), help="parallel clip renders")
    ap.add_argument("--workdir", help="folder for intermediate clips (default <out>_work; reused as a cache)")
    ap.add_argument("--keep", action="store_true", help="keep the work folder")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()
    VERBOSE = args.verbose

    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            die(tool + " not found on PATH")
    shots, audio_field, base = load_shots(args.shots)
    audio = args.audio or (os.path.join(base, audio_field) if audio_field else None)
    if not audio or not os.path.exists(audio):
        die("narration audio not found (pass --audio)")
    for flag, p in (("--music", args.music), ("--srt", args.srt), ("--fontsdir", args.fontsdir)):
        if p and not os.path.exists(p):
            die("%s file/folder not found: %s (leave the flag out to skip it)" % (flag, p))
    if args.size:
        try:
            W, H = [int(x) for x in args.size.lower().split("x")]
        except ValueError:
            die("--size must look like 1920x1080")
        if W % 2 or H % 2:
            die("--size needs even width and height for H.264 (e.g. 1280x720)")
    else:
        W, H = (1080, 1920) if args.vertical else (1920, 1080)
    cfg = {"W": W, "H": H, "fps": args.fps, "zoom": args.zoom, "up": max(1, args.upscale),
           "vertical": args.vertical, "vfill": args.vfill}
    fps = args.fps

    a_dur = probe_duration(audio)
    d = shot_durations(shots)
    if not args.no_fit:
        d = fit_to(d, a_dur)
        shots = shots[:len(d)]
    total = sum(d)

    # frame-exact timeline (cumulative rounding, no drift)
    cum, frames, t = [0], [], 0.0
    for x in d:
        t += x
        cum.append(int(round(t * fps)))
    frames = [cum[k + 1] - cum[k] for k in range(len(d))]
    fade_f = int(round(args.fade * fps))
    ext = []
    for k, s in enumerate(shots):
        if k == len(shots) - 1:
            ext.append(0)
        elif fade_f == 0:
            ext.append(0)
        elif s.get("transition") == "cut":
            ext.append(1)
        else:
            ext.append(min(fade_f, frames[k + 1] // 2, frames[k] // 2))
    if any(f < 2 for f in frames):
        die("a shot is shorter than 2 frames; check the timings")

    out = os.path.abspath(args.out)
    work = os.path.abspath(args.workdir or os.path.splitext(out)[0] + "_work")
    os.makedirs(work, exist_ok=True)
    cfg["work"], cfg["fit"] = work, not args.crop_all
    log("%d shots, %.2f s, %dx%d@%d, fade %.2f s, audio %.2f s" % (len(shots), total, W, H, fps, args.fade, a_dur))

    # 1. clips (cached by content)
    jobs = []
    for k, s in enumerate(shots):
        st = os.stat(s["_path"])
        key = json.dumps([s["_path"], st.st_mtime, st.st_size, s["_motion"], frames[k] + ext[k],
                          W, H, fps, args.zoom, cfg["up"], args.vertical, args.vfill, cfg["fit"]])
        h = hashlib.sha1(key.encode()).hexdigest()[:10]
        jobs.append({"shot": s, "frames": frames[k] + ext[k], "cfg": cfg,
                     "out": os.path.join(work, "clip_%03d_%s.mp4" % (k + 1, h))})
    with cf.ThreadPoolExecutor(max_workers=args.jobs) as ex:
        clips = []
        for k, c in enumerate(ex.map(render_clip, jobs)):
            clips.append(c)
            if (k + 1) % 10 == 0 or k + 1 == len(jobs):
                log("rendered %d/%d clips" % (k + 1, len(jobs)))

    # 2. chunks (keeps any single ffmpeg graph small)
    units, u_nom, u_ext = clips, frames, ext
    if len(clips) > args.chunk:
        units, u_nom, u_ext = [], [], []
        for c0 in range(0, len(clips), args.chunk):
            c1 = min(len(clips), c0 + args.chunk)
            cpath = os.path.join(work, "chunk_%03d_%s.mp4" % (c0 // args.chunk,
                                 hashlib.sha1("".join(clips[c0:c1]).encode()).hexdigest()[:10]))
            if not os.path.exists(cpath):
                join_chunk(clips[c0:c1], frames[c0:c1], ext[c0:c1], fps, cpath)
            units.append(cpath)
            u_nom.append(sum(frames[c0:c1]))
            u_ext.append(ext[c1 - 1])
        log("joined %d chunks" % len(units))

    # 3. final pass: join + titles/captions + audio
    vfc, vlab = join_filter(len(units), u_nom, u_ext, fps)
    titles, captions = [], []
    if not args.no_titles:
        for k, s in enumerate(shots):
            txt = (s.get(args.title_key) or "").strip()
            if txt:
                a = cum[k] / fps + 0.25
                titles.append((a, max(a + 0.8, cum[k + 1] / fps - 0.15), txt))
    soft_srt = None
    all_text = " ".join(t[2] for t in titles)
    if args.srt and args.subs != "none":
        cues = parse_srt(args.srt)
        all_text += " ".join(c[2] for c in cues)
        if args.subs == "burn":
            captions = cues
        else:
            soft_srt = os.path.abspath(args.srt)
    elif not args.srt and args.subs != "none":
        for k, s in enumerate(shots):
            if (s.get("caption") or "").strip():
                captions.append((cum[k] / fps, cum[k + 1] / fps, s["caption"].strip()))
                all_text += " " + s["caption"]
    is_hi = bool(DEVANAGARI.search(all_text))
    font = args.font or (pick_hindi_font(args.fontsdir) if is_hi else "Arial")
    title_font = args.title_font or font
    if titles or captions:
        write_ass(os.path.join(work, "overlay.ass"), cfg, titles, captions, font, title_font)
        opt = ":fontsdir=%s" % os.path.relpath(os.path.abspath(args.fontsdir), work).replace(":", "\\:") if args.fontsdir else ""
        vfc += ";[%s]ass=overlay.ass%s[vout]" % (vlab, opt)
        vlab = "vout"

    cmd = ["ffmpeg", "-v", "error", "-y"]
    for u in units:
        cmd += ["-i", u]
    ai = len(units)
    cmd += ["-i", os.path.abspath(audio)]
    afmt = "aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo"
    afc = "[%d:a]%s,apad,atrim=0:%.3f[voice]" % (ai, afmt, total)
    nxt = ai + 1
    if args.music:
        cmd += ["-stream_loop", "-1", "-i", os.path.abspath(args.music)]
        fo = max(0.0, total - 3)
        afc += (";[%d:a]%s,atrim=0:%.3f,volume=%gdB,afade=t=in:d=1.5,afade=t=out:st=%.3f:d=3[mus]"
                % (nxt, afmt, total, args.music_db, fo))
        nxt += 1
        if args.no_duck:
            afc += ";[voice][mus]amix=inputs=2:duration=first:normalize=0[mix]"
        else:
            afc += (";[voice]asplit=2[v1][v2];[mus][v2]sidechaincompress=threshold=0.05:ratio=4:attack=20:"
                    "release=350:makeup=1[duck];[v1][duck]amix=inputs=2:duration=first:normalize=0[mix]")
        alab = "mix"
    else:
        alab = "voice"
    if not args.no_loudnorm:
        afc += ";[%s]loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[aout]" % alab
        alab = "aout"
    if soft_srt:
        cmd += ["-i", soft_srt]
    cmd += ["-filter_complex", vfc + ";" + afc, "-map", "[%s]" % vlab, "-map", "[%s]" % alab]
    if soft_srt:
        lang = args.sub_lang or ("hin" if is_hi else "eng")
        cmd += ["-map", "%d:s" % nxt, "-c:s", "mov_text", "-metadata:s:s:0", "language=" + lang]
    cmd += ["-t", "%.3f" % total, "-r", str(fps), "-c:v", "libx264", "-preset", args.preset, "-crf", str(args.crf),
            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out]
    log("final encode -> %s" % out)
    run(cmd, cwd=work)
    if not args.keep and not args.workdir:
        shutil.rmtree(work, ignore_errors=True)
    log("done: %s (%.2f s)" % (out, probe_duration(out)))
    print(out)


if __name__ == "__main__":
    main()
