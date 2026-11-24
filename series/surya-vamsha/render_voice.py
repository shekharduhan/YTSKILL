"""Render a Hindi script to narration audio with a free offline voice (Piper).

    python3 render_voice.py --model path/to/hi_IN-pratham-medium.onnx 1      # episode 1
    python3 render_voice.py --model ... 1 2 3                               # several
    python3 render_voice.py --model ... all

Reads epNN-*-hindi.md, keeps only the spoken lines, and honours the script's pauses:
  …          short breath (0.35 s)
  [विराम]    full pause   (1.8 s)
  new line   0.55 s, new scene 1.1 s
Then deepens and steadies the voice with ffmpeg (pitch down about 2 semitones at the same
speed, a little low-end warmth, gentle compression) and levels it to -16 LUFS.
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
        line = line.replace("**", "").strip()
        parts = re.split(r"(\[विराम\]|…)", line)
        for p in parts:
            if p == "[विराम]": out.append(("pause", FULL))
            elif p == "…": out.append(("pause", SHORT))
            elif p.strip(" ,"): out.append(("text", p.strip(" ,")))
        out.append(("pause", LINE))
    return out


def render(voice, cfg, md_path, out_mp3):
    rate = voice.config.sample_rate
    frames = bytearray()
    for kind, val in segments(open(md_path, encoding="utf-8").read()):
        if kind == "pause":
            frames += b"\x00\x00" * int(rate * val)
        else:
            for chunk in voice.synthesize(val, syn_config=cfg):
                frames += chunk.audio_int16_bytes
    with tempfile.TemporaryDirectory() as tmp:
        raw = os.path.join(tmp, "raw.wav")
        with wave.open(raw, "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate); w.writeframes(bytes(frames))
        f = 0.89  # about -2 semitones
        chain = (f"asetrate={int(rate*f)},aresample={rate},atempo={1/f:.4f},"
                 "equalizer=f=120:t=q:w=1:g=3,equalizer=f=3500:t=q:w=1.5:g=1.5,"
                 "acompressor=threshold=-20dB:ratio=2.5:attack=15:release=200,"
                 "loudnorm=I=-16:TP=-1.5:LRA=11")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-af", chain,
                        "-ar", "44100", "-b:a", "160k", out_mp3], check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--speed", type=float, default=1.18, help="Piper length_scale; higher = slower")
    ap.add_argument("episodes", nargs="+")
    a = ap.parse_args()
    voice = PiperVoice.load(a.model)
    cfg = SynthesisConfig(length_scale=a.speed, noise_scale=0.6, noise_w_scale=0.7)
    files = sorted(glob.glob(os.path.join(HERE, "ep*-hindi.md")))
    if a.episodes != ["all"]:
        want = {int(e) for e in a.episodes}
        files = [f for f in files if int(os.path.basename(f)[2:4]) in want]
    os.makedirs(os.path.join(HERE, "audio"), exist_ok=True)
    for f in files:
        n = os.path.basename(f)[2:4]
        out = os.path.join(HERE, "audio", f"ep{n}.mp3")
        render(voice, cfg, f, out)
        print("wrote", out)


if __name__ == "__main__":
    main()
