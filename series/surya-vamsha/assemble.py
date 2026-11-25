"""Assemble an episode video: images + ElevenLabs narration -> 1080p MP4, in sync with the voice.

    python3 assemble.py 1
    python3 assemble.py --check 1     # only check the timing plan, don't render

Needs: audio/epNN.mp3 and audio/epNN.timing.json (eleven_render.py), images/epNN/NN.png
(gen_images.py), and epNN-image-prompts.md, whose last column ("starts at") holds the narration
words at which each picture appears.

Each picture starts at the moment its words are spoken (looked up in the timing file; inside a
long paragraph the moment is estimated from the character position), shifted earlier by one
crossfade so the new picture is fully visible as the words begin. Pictures get a slow Ken Burns
zoom (alternating in/out) and a 0.6 s crossfade. Black letterbox bars are cropped first.
Output: video/epNN.mp4 (H.264 + AAC, 1920x1080, 25 fps).
"""
import glob, json, os, re, subprocess, sys, tempfile
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
W, H, FPS, XF = 1920, 1080, 25, 0.6
MIN_SHOT = 2.5


def dur(path):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", path]).strip())


def anchors(ep):
    """{image number: narration phrase} from the prompts table's last column."""
    out = {}
    for line in open(os.path.join(HERE, f"ep{ep:02d}-image-prompts.md"), encoding="utf-8"):
        m = re.match(r"\|\s*(\d+)\s*\|", line)
        if m:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            out[int(m.group(1))] = cells[-1]
    return out


def squash(s):
    return re.sub(r"[\s…,।\"'“”‘’!?\-—]+", "", s)


def shot_plan(ep):
    timing = json.load(open(os.path.join(HERE, "audio", f"ep{ep:02d}.timing.json"), encoding="utf-8"))
    pieces = [it for it in timing["items"] if it["kind"] == "text"]
    total = dur(os.path.join(HERE, "audio", f"ep{ep:02d}.mp3"))
    starts, problems = [], []
    for n, phrase in sorted(anchors(ep).items()):
        key, hits = squash(phrase), []
        for it in pieces:
            body = squash(it["text"])
            pos = body.find(key)
            if pos >= 0:
                frac = pos / max(1, len(body))
                hits.append(it["start"] + frac * (it["end"] - it["start"]))
        if not hits:
            problems.append(f"image {n}: words not found in narration: {phrase}"); continue
        if len(hits) > 1:
            problems.append(f"image {n}: words occur {len(hits)} times, using the first: {phrase}")
        starts.append((max(0.0, hits[0] - XF), n))
    starts.sort()
    if starts:
        starts[0] = (0.0, starts[0][1])
    shots = []
    for i, (t, n) in enumerate(starts):
        end = starts[i + 1][0] if i + 1 < len(starts) else total
        shots.append([n, t, end - t])
        if end - t < MIN_SHOT:
            problems.append(f"image {n}: on screen only {end - t:.1f}s")
    return shots, total, problems


def autocrop(src, dst):
    im = Image.open(src).convert("RGB")
    a = np.asarray(im).mean(axis=2)
    rows = np.where(a.mean(axis=1) > 18)[0]; cols = np.where(a.mean(axis=0) > 18)[0]
    im = im.crop((cols[0], rows[0], cols[-1] + 1, rows[-1] + 1))
    w, h = im.size; target = W / H
    if w / h > target:
        nw = int(h * target); im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else:
        nh = int(w / target); im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    im.resize((W * 2, H * 2), Image.LANCZOS).save(dst, quality=92)


def main(ep, check_only=False):
    shots, total, problems = shot_plan(ep)
    for p in problems:
        print("  !", p)
    for n, t, d in shots:
        print(f"  {int(t // 60)}:{t % 60:04.1f}  image {n:2d}  {d:4.1f}s")
    if check_only:
        return
    audio = os.path.join(HERE, "audio", f"ep{ep:02d}.mp3")
    out_dir = os.path.join(HERE, "video"); os.makedirs(out_dir, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        clips = []
        for i, (n, t, d) in enumerate(shots):
            src = os.path.join(HERE, "images", f"ep{ep:02d}", f"{n:02d}.png")
            big = os.path.join(tmp, f"{n:02d}.jpg"); autocrop(src, big)
            # frame counts from the absolute timeline, so rounding never accumulates into drift
            f0, f1 = round(t * FPS), round((t + d) * FPS)
            frames = f1 - f0 + (round(XF * FPS) if i < len(shots) - 1 else 0)
            step = min(0.0009, 0.15 / max(frames, 1))           # gentle zoom, never more than 15 %
            z = f"min(1+{step:.6f}*on,1.15)" if i % 2 == 0 else f"max(1.15-{step:.6f}*on,1)"
            clip = os.path.join(tmp, f"c{i:02d}.mp4")
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i", big, "-vf",
                            f"zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s={W}x{H}:fps={FPS},format=yuv420p",
                            "-frames:v", str(frames), "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", clip], check=True)
            clips.append(clip)
        inputs, filt, last = [], [], "[0:v]"
        for c in clips:
            inputs += ["-i", c]
        for i in range(1, len(clips)):
            offset = round(shots[i][1] * FPS) / FPS          # picture i is fully in at its start time + XF
            filt.append(f"{last}[{i}:v]xfade=transition=fade:duration={XF}:offset={offset:.3f}[v{i}]")
            last = f"[v{i}]"
        silent = os.path.join(tmp, "silent.mp4")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(filt),
                        "-map", last, "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", silent], check=True)
        out = os.path.join(out_dir, f"ep{ep:02d}.mp4")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", silent, "-i", audio, "-map", "0:v", "-map", "1:a",
                        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], check=True)
    print("wrote", out, f"{total:.1f}s narration, {len(shots)} shots, video {dur(out):.1f}s")


if __name__ == "__main__":
    args = sys.argv[1:]
    main(int([a for a in args if a != "--check"][0]), check_only="--check" in args)
