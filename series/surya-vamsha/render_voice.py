"""Render a Hindi script to narration audio with a free offline voice (Piper).

    python3 render_voice.py --model path/to/hi_IN-pratham-medium.onnx 1      # episode 1
    python3 render_voice.py --model ... 1 2 3                               # several
    python3 render_voice.py --model ... all

Reads epNN-*-hindi.md, keeps only the spoken lines, and honours the script's pauses:
  …          short breath (0.35 s)
  [विराम]    full pause   (1.8 s)
  new line   0.55 s, new scene 1.1 s
Then deepens and steadies the voice with ffmpeg (pitch down at the same
speed by default -3 semitones, chest warmth, compression, a light room echo; **bold** words are said slower) and levels it to -16 LUFS.
Output: audio/epNN.mp3

The Piper voice hi_IN-pratham-medium is a generic stock voice. Its dataset licence is
CC BY-NC-SA 4.0 (non-commercial): fine for drafts and a non-monetised channel; for a monetised
channel use a commercially licensed voice or a human narrator.
"""
import argparse, glob, os, re, subprocess, tempfile, wave
from piper import PiperVoice, SynthesisConfig

HERE = os.path.dirname(os.path.abspath(__file__))
SHORT, FULL, LINE, SCENE = 0.35, 1.8, 0.55, 1.1


def segments(md):
    body = md.split("\n---\n", 1)[1]
    body = re.split(r"(?m)^## (जाँच लें|कॉपी ब्लॉक)", body)[0]
    out = []  # ("text", str) or ("pause", seconds)
    for line in body.splitlines():
        if line.startswith("## "):
            out.append(("pause", SCENE)); continue
        if "[स्क्रीन" in line or line.startswith(">") or not line.strip():
            continue
        parts = re.split(r"(\[विराम\]|…|\*\*[^*]+\*\*)", line.strip())
        for p in parts:
            if p == "[विराम]": out.append(("pause", FULL))
            elif p == "…": out.append(("pause", SHORT))
            elif p.startswith("**"):
                out.append(("pause", 0.12)); out.append(("bold", p.strip("*").strip(" ,"))); out.append(("pause", 0.12))
            elif p.strip(" ,"): out.append(("text", p.strip(" ,")))
        out.append(("pause", LINE))
    return out


def render(voice, cfg, md_path, out_mp3, pitch=-3.0, reverb=True, max_items=None, bold_cfg=None):
    rate = voice.config.sample_rate
    frames = bytearray()
    segs = segments(open(md_path, encoding="utf-8").read())
    if max_items: segs = segs[:max_items]
    for kind, val in segs:
        if kind == "pause":
            frames += b"\x00\x00" * int(rate * val)
        else:
            c = bold_cfg if (kind == "bold" and bold_cfg) else cfg
            for chunk in voice.synthesize(val, syn_config=c):
                frames += chunk.audio_int16_bytes
    with tempfile.TemporaryDirectory() as tmp:
        raw = os.path.join(tmp, "raw.wav")
        with wave.open(raw, "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate); w.writeframes(bytes(frames))
        f = 2 ** (pitch / 12)
        chain = (f"asetrate={int(rate*f)},aresample={rate},atempo={1/f:.4f},"
                 "highpass=f=60,equalizer=f=110:t=q:w=1:g=5,equalizer=f=250:t=q:w=1:g=2,"
                 "equalizer=f=3200:t=q:w=1.5:g=2,"
                 "acompressor=threshold=-22dB:ratio=3:attack=10:release=250:makeup=2")
        if reverb:
            chain += ",aecho=0.85:0.6:45|90:0.18|0.10"
        chain += ",loudnorm=I=-16:TP=-1.5:LRA=9"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-af", chain,
                        "-ar", "44100", "-b:a", "160k", out_mp3], check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--speed", type=float, default=1.18, help="Piper length_scale; higher = slower")
    ap.add_argument("--pitch", type=float, default=-3.0, help="semitones, negative = deeper")
    ap.add_argument("--no-reverb", action="store_true")
    ap.add_argument("--emphasis", type=float, default=1.2, help="extra slowness on **bold** words")
    ap.add_argument("--first", type=int, default=None, help="render only the first N segments (preview)")
    ap.add_argument("--suffix", default="")
    ap.add_argument("episodes", nargs="+")
    a = ap.parse_args()
    voice = PiperVoice.load(a.model)
    cfg = SynthesisConfig(length_scale=a.speed, noise_scale=0.55, noise_w_scale=0.6)
    bold = SynthesisConfig(length_scale=a.speed * a.emphasis, noise_scale=0.5, noise_w_scale=0.5, volume=1.15)
    files = sorted(glob.glob(os.path.join(HERE, "ep*-hindi.md")))
    if a.episodes != ["all"]:
        want = {int(e) for e in a.episodes}
        files = [f for f in files if int(os.path.basename(f)[2:4]) in want]
    os.makedirs(os.path.join(HERE, "audio"), exist_ok=True)
    for f in files:
        n = os.path.basename(f)[2:4]
        out = os.path.join(HERE, "audio", f"ep{n}{a.suffix}.mp3")
        render(voice, cfg, f, out, pitch=a.pitch, reverb=not a.no_reverb, max_items=a.first, bold_cfg=bold)
        print("wrote", out)


if __name__ == "__main__":
    main()
