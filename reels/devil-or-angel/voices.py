"""Free, offline voices with Piper TTS (MIT). Downloads two voice models once."""
import json, os, subprocess, urllib.request
import numpy as np, wave

VOICE_DIR = os.path.expanduser("~/.cache/piper-voices")
BASE = "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US"
VOICES = {"H": "ryan/high/en_US-ryan-high", "W": "amy/medium/en_US-amy-medium"}
# style -> (length_scale, noise_scale)  (bigger length = slower)
STYLE = {"whisper": (1.12, 0.5), "flat": (1.0, 0.4), "annoyed": (0.95, 0.75),
         "normal": (1.0, 0.667), "serious": (1.05, 0.6), "warm": (1.05, 0.7)}

def model(who):
    os.makedirs(VOICE_DIR, exist_ok=True)
    rel = VOICES[who]; name = os.path.basename(rel)
    path = os.path.join(VOICE_DIR, name + ".onnx")
    for ext in (".onnx", ".onnx.json"):
        if not os.path.exists(path.replace(".onnx", ext)):
            print("downloading", name + ext)
            urllib.request.urlretrieve(f"{BASE}/{rel}{ext}", path.replace(".onnx", ext))
    return path

def whisperize(p):
    """Breathy, close-to-the-ear version: highpass + mixed-in shaped noise."""
    with wave.open(p) as w:
        sr = w.getframerate(); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    a = np.append(a[0], a[1:] - 0.9 * a[:-1])               # pre-emphasis = thinner, airy
    env = np.convolve(np.abs(a), np.ones(400) / 400, "same")
    noise = np.random.default_rng(1).normal(0, 1, len(a)) * env * 0.9
    out = 0.55 * a + noise
    out = out / (np.abs(out).max() + 1e-6) * 0.8
    with wave.open(p, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((out * 32767).astype(np.int16).tobytes())

if __name__ == "__main__":
    os.makedirs("audio", exist_ok=True)
    for i, (who, text, style) in enumerate(json.load(open("lines.json"))):
        ls, ns = STYLE[style]
        out = f"audio/{i:02d}.wav"
        subprocess.run(["piper", "-m", model(who), "-f", out, "--length-scale", str(ls), "--noise-scale", str(ns)],
                       input=text.encode(), check=True, capture_output=True)
        if style == "whisper": whisperize(out)
        print(out, text)
