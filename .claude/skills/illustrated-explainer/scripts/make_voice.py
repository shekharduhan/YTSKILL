#!/usr/bin/env python3
"""make_voice.py - turn a narration script into one voice track plus timings.

Each script line is synthesised on its own, then the lines are joined with short
pauses. Because every line is measured separately, the per-line start/end times
are exact, so you get:

  <out>.mp3            the full narration
  <out>.timings.json   {"duration": s, "lines": [{"i", "text", "start", "end", "section"}]}
  <out>.srt            captions, split into short readable chunks

Backends
  edge        (default, free) Microsoft Edge neural voices through the `edge-tts`
              package (pip install edge-tts). Needs speech.platform.bing.com.
  elevenlabs  ElevenLabs REST API (paid, best Hindi). Key from $ELEVENLABS_API_KEY
              or --api-key. Uses only the Python standard library.
  dryrun      no voice at all: a SILENT track whose line lengths are estimated from
              word count (~155 wpm English, ~130 wpm Hindi). Only for testing the
              shot list / edit offline; replace it with a real voice before release.

Script format (UTF-8 text file)
  * one sentence per line works best (use --split to split paragraphs into sentences)
  * a blank line = longer pause (paragraph / act break)
  * a line starting with "## " starts a new section (not spoken; stored in timings)
  * a line starting with "#" (but not "## ") is a comment and is skipped

Examples
  python make_voice.py script_hi.txt -o out/voice_hi                 # Hindi, auto voice
  python make_voice.py script_en.txt -o out/voice_en --voice en-US-GuyNeural --rate=-5%
  python make_voice.py script_hi.txt -o out/voice_hi --backend dryrun     # silent test track
  python make_voice.py script_hi.txt -o out/voice_hi --backend elevenlabs \
         --voice <voice_id> --model eleven_multilingual_v2
  python make_voice.py --list-voices --lang hi
  python make_voice.py --list-voices --backend elevenlabs

Requires ffmpeg and ffprobe on PATH.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
import wave

DEFAULT_VOICES = {"hi": "hi-IN-MadhurNeural", "en": "en-US-GuyNeural"}
EDGE_SUGGESTED = {
    "hi": ["hi-IN-MadhurNeural (male)", "hi-IN-SwaraNeural (female)"],
    "en": ["en-US-GuyNeural (male)", "en-US-AndrewNeural (male)", "en-GB-RyanNeural (male)",
           "en-IN-PrabhatNeural (male, Indian English)", "en-IN-NeerjaNeural (female, Indian English)"],
}
SR = 44100
DEVANAGARI = re.compile(r"[ऀ-ॿ]")


def die(msg):
    sys.exit("make_voice: " + msg)


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        die("command failed: %s\n%s" % (" ".join(cmd[:6]), (r.stderr or r.stdout)[-2000:]))
    return r


# ---------------------------------------------------------------- script parsing
def split_sentences(text):
    # split after . ! ? or the Hindi danda, keeping the mark; avoid splitting "B.R." style initials
    parts = re.split(r"(?<=[.!?।॥])\s+(?=[^\s])", text.strip())
    out = []
    for p in parts:
        if out and re.search(r"\b[A-Z]\.$", out[-1]):
            out[-1] += " " + p
        else:
            out.append(p)
    return [p.strip() for p in out if p.strip()]


def parse_script(path, split):
    with open(path, encoding="utf-8") as f:
        raw = f.read().splitlines()
    items, section, pending_pause = [], "", False
    for line in raw:
        s = line.strip()
        if not s:
            pending_pause = True
            continue
        if s.startswith("## "):
            section = s[3:].strip()
            pending_pause = True
            continue
        if s.startswith("#"):
            continue
        for sent in (split_sentences(s) if split else [s]):
            items.append({"text": sent, "section": section, "pause_before": pending_pause})
            pending_pause = False
    if not items:
        die("no spoken lines found in " + path)
    return items


# ---------------------------------------------------------------- backends
def edge_bin(args):
    if args.edge_bin:
        return args.edge_bin
    here = shutil.which("edge-tts")
    if here:
        return here
    cand = os.path.join(os.path.dirname(sys.executable), "edge-tts")
    if os.path.exists(cand):
        return cand
    die("edge-tts not found. Install it:  pip install edge-tts   (or pass --edge-bin)")


def edge_synth(args, text, out_mp3):
    cmd = [edge_bin(args), "--voice", args.voice, "--text", text, "--write-media", out_mp3]
    if args.rate:
        cmd += ["--rate=" + args.rate]
    if args.pitch:
        cmd += ["--pitch=" + args.pitch]
    if args.proxy:
        cmd += ["--proxy", args.proxy]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0 or not os.path.exists(out_mp3) or os.path.getsize(out_mp3) == 0:
        tail = (r.stderr or "")[-600:]
        die("edge-tts failed for line %r.\n%s\nIf this is a network/proxy error, the host "
            "speech.platform.bing.com is blocked here: run on your own PC, pass --proxy, "
            "or use --backend elevenlabs." % (text[:60], tail))


def el_key(args):
    key = args.api_key or os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        die("ElevenLabs needs a key: set ELEVENLABS_API_KEY or pass --api-key")
    return key


def el_request(args, url, body=None):
    req = urllib.request.Request(url, data=None if body is None else json.dumps(body).encode(),
                                 headers={"xi-api-key": el_key(args), "Content-Type": "application/json",
                                          "Accept": "application/json"},
                                 method="GET" if body is None else "POST")
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            return r.read()
    except urllib.error.HTTPError as e:
        die("ElevenLabs HTTP %s: %s" % (e.code, e.read()[:500].decode("utf-8", "replace")))


def el_synth(args, text, out_mp3, prev_text, next_text):
    body = {"text": text, "model_id": args.model}
    if prev_text:
        body["previous_text"] = prev_text
    if next_text:
        body["next_text"] = next_text
    vs = {"stability": args.stability, "similarity_boost": 0.75}
    if args.speed:
        vs["speed"] = args.speed
    body["voice_settings"] = vs
    url = "https://api.elevenlabs.io/v1/text-to-speech/%s?output_format=mp3_44100_128" % args.voice
    data = el_request(args, url, body)
    with open(out_mp3, "wb") as f:
        f.write(data)


def dry_synth(args, text, out_wav, lang):
    words = len(text.split())
    secs = max(0.6, words * 60.0 / (130.0 if lang == "hi" else 155.0))
    with wave.open(out_wav, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(b"\x00\x00" * int(secs * SR))


def list_voices(args):
    if args.backend == "elevenlabs":
        d = json.loads(el_request(args, "https://api.elevenlabs.io/v1/voices"))
        for v in d.get("voices", []):
            lab = v.get("labels") or {}
            print("%-22s %-45s %s %s" % (v["voice_id"], v["name"][:45], lab.get("accent", ""), lab.get("gender", "")))
        print("\nTip: models with Hindi include eleven_multilingual_v2, eleven_v3, eleven_flash_v2_5, eleven_turbo_v2_5")
        return
    cmd = [edge_bin(args), "--list-voices"] + (["--proxy", args.proxy] if args.proxy else [])
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("Could not reach the edge-tts voice list (network). Known good voices:")
        for lang, vs in EDGE_SUGGESTED.items():
            if not args.lang or args.lang == lang:
                for v in vs:
                    print("  ", v)
        return
    for line in r.stdout.splitlines():
        if not args.lang or line.startswith(args.lang + "-") or line.startswith("Name"):
            print(line)


# ---------------------------------------------------------------- audio helpers
def to_pcm(src, dst):
    run(["ffmpeg", "-v", "error", "-y", "-i", src, "-ac", "1", "-ar", str(SR), "-sample_fmt", "s16", dst])
    with wave.open(dst, "rb") as w:
        return w.readframes(w.getnframes())


def trim_silence(pcm, thresh=300):
    """Trim leading/trailing near-silence (16-bit mono) so pauses are controlled by --gap."""
    n = len(pcm) // 2
    import array
    a = array.array("h", pcm[: n * 2])
    s, e = 0, n
    while s < e and abs(a[s]) < thresh:
        s += 1
    while e > s and abs(a[e - 1]) < thresh:
        e -= 1
    s = max(0, s - int(0.03 * SR))
    e = min(n, e + int(0.06 * SR))
    return a[s:e].tobytes()


def fmt_srt(t):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return "%02d:%02d:%02d,%03d" % (h, m, s, ms)


def chunk_line(text, start, end, max_chars):
    words = text.split()
    chunks, cur = [], []
    for w in words:
        if cur and len(" ".join(cur + [w])) > max_chars:
            chunks.append(" ".join(cur))
            cur = [w]
        else:
            cur.append(w)
    if cur:
        chunks.append(" ".join(cur))
    total = sum(len(c) for c in chunks) or 1
    out, t = [], start
    for c in chunks:
        d = (end - start) * len(c) / total
        out.append((t, t + d, c))
        t += d
    return out


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("script", nargs="?", help="UTF-8 script text file")
    ap.add_argument("-o", "--out", default="voice", help="output prefix (default: voice) -> voice.mp3/.timings.json/.srt")
    ap.add_argument("--backend", choices=["edge", "elevenlabs", "dryrun"], default="edge",
                    help="edge (free, default), elevenlabs (paid) or dryrun (silent test track, offline)")
    ap.add_argument("--voice", help="edge voice name or ElevenLabs voice_id (default: auto by language for edge)")
    ap.add_argument("--lang", choices=["hi", "en"], help="language hint for auto voice / voice listing (default: detect)")
    ap.add_argument("--split", action="store_true", help="split each line into sentences (. ! ? and the Hindi danda)")
    ap.add_argument("--gap", type=float, default=0.25, help="pause between lines in seconds (default 0.25)")
    ap.add_argument("--para-gap", type=float, default=0.6, help="pause at blank lines / sections (default 0.6)")
    ap.add_argument("--lead", type=float, default=0.3, help="silence before the first line (default 0.3)")
    ap.add_argument("--tail", type=float, default=0.8, help="silence after the last line (default 0.8)")
    ap.add_argument("--max-chars", type=int, default=42, help="max characters per caption chunk (default 42)")
    ap.add_argument("--rate", help="edge: speaking rate, e.g. --rate=-5%% or --rate=+10%%")
    ap.add_argument("--pitch", help="edge: pitch, e.g. --pitch=-2Hz")
    ap.add_argument("--proxy", help="edge: HTTP proxy URL for edge-tts")
    ap.add_argument("--edge-bin", help="path to the edge-tts executable")
    ap.add_argument("--model", default="eleven_multilingual_v2", help="elevenlabs model id (default eleven_multilingual_v2)")
    ap.add_argument("--speed", type=float, help="elevenlabs: speed 0.7-1.2")
    ap.add_argument("--stability", type=float, default=0.5, help="elevenlabs: stability 0-1 (default 0.5)")
    ap.add_argument("--api-key", help="elevenlabs key (else $ELEVENLABS_API_KEY)")
    ap.add_argument("--no-trim", action="store_true", help="do not trim silence around each line")
    ap.add_argument("--list-voices", action="store_true", help="list voices for the chosen backend and exit")
    ap.add_argument("--keep", action="store_true", help="keep per-line audio in <out>_lines/")
    # "--rate -5%" would be read by argparse as a new option; glue such values on
    argv = sys.argv[1:]
    for k in range(len(argv) - 1):
        if argv[k] in ("--rate", "--pitch") and argv[k + 1].startswith("-"):
            argv[k:k + 2] = [argv[k] + "=" + argv[k + 1], ""]
    args = ap.parse_args([a for a in argv if a != ""])

    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            die(tool + " not found on PATH")
    if args.list_voices:
        list_voices(args)
        return
    if not args.script:
        ap.error("script file is required (or use --list-voices)")

    items = parse_script(args.script, args.split)
    lang = args.lang or ("hi" if any(DEVANAGARI.search(i["text"]) for i in items) else "en")
    if args.backend == "dryrun":
        args.voice = "none (silent dry run)"
    if not args.voice:
        if args.backend == "elevenlabs":
            die("--voice <voice_id> is required for elevenlabs (see --list-voices --backend elevenlabs)")
        args.voice = DEFAULT_VOICES[lang]
    print("make_voice: %d lines, lang=%s, backend=%s, voice=%s" % (len(items), lang, args.backend, args.voice), file=sys.stderr)

    out_dir = os.path.dirname(os.path.abspath(args.out))
    os.makedirs(out_dir, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="voice_", dir=out_dir)
    pcm_all = bytearray(b"\x00\x00" * int(args.lead * SR))
    lines = []
    try:
        for n, it in enumerate(items):
            mp3 = os.path.join(tmp, "line_%04d.mp3" % n)
            if args.backend == "dryrun":
                mp3 = mp3[:-4] + "_dry.wav"
                dry_synth(args, it["text"], mp3, lang)
            elif args.backend == "edge":
                edge_synth(args, it["text"], mp3)
            else:
                prev_t = items[n - 1]["text"] if n else None
                next_t = items[n + 1]["text"] if n + 1 < len(items) else None
                el_synth(args, it["text"], mp3, prev_t, next_t)
            pcm = to_pcm(mp3, os.path.join(tmp, "line_%04d.wav" % n))
            if not args.no_trim and args.backend != "dryrun":
                pcm = trim_silence(pcm)
            if n:
                gap = args.para_gap if it["pause_before"] else args.gap
                pcm_all += b"\x00\x00" * int(gap * SR)
            start = len(pcm_all) / 2 / SR
            pcm_all += pcm
            end = len(pcm_all) / 2 / SR
            lines.append({"i": n, "text": it["text"], "section": it["section"],
                          "start": round(start, 3), "end": round(end, 3)})
            print("  [%3d] %6.2f-%6.2f  %s" % (n, start, end, it["text"][:70]), file=sys.stderr)
        pcm_all += b"\x00\x00" * int(args.tail * SR)
        wav = os.path.join(tmp, "all.wav")
        with wave.open(wav, "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes(bytes(pcm_all))
        mp3_out = args.out + ".mp3"
        run(["ffmpeg", "-v", "error", "-y", "-i", wav, "-c:a", "libmp3lame", "-b:a", "192k", mp3_out])
        duration = len(pcm_all) / 2 / SR
        meta = {"audio": os.path.basename(mp3_out), "duration": round(duration, 3), "lang": lang,
                "backend": args.backend, "voice": args.voice, "lines": lines}
        with open(args.out + ".timings.json", "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=1)
        srt, k = [], 1
        for ln in lines:
            for a, b, c in chunk_line(ln["text"], ln["start"], ln["end"], args.max_chars):
                srt.append("%d\n%s --> %s\n%s\n" % (k, fmt_srt(a), fmt_srt(b), c))
                k += 1
        with open(args.out + ".srt", "w", encoding="utf-8") as f:
            f.write("\n".join(srt))
        if args.keep:
            keep = args.out + "_lines"
            os.makedirs(keep, exist_ok=True)
            for fn in os.listdir(tmp):
                if fn.endswith(".mp3"):
                    shutil.copy(os.path.join(tmp, fn), keep)
        print("make_voice: wrote %s (%.2f s), %s.timings.json, %s.srt" % (mp3_out, duration, args.out, args.out))
        if args.backend == "dryrun":
            print("make_voice: NOTE dryrun = silent track with estimated timings; make the real voice before release")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
