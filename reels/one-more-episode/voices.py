"""Free, offline voices with Kokoro TTS (Apache-2.0, 82M params). Downloads the model once (~350 MB).

Whispered lines blend the speaker's voice with Kokoro's soft/whisper voice (af_nicole) so it stays
the same character, just quieter and breathier - no fake noise filters.
"""
import json, os, urllib.request
import numpy as np, soundfile as sf
from kokoro_onnx import Kokoro

CACHE = os.path.expanduser("~/.cache/kokoro")
URL = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/"
FILES = ["kokoro-v1.0.onnx", "voices-v1.0.bin"]
VOICE = {"H": "am_michael", "W": "af_heart"}
WHISPER_VOICE = "af_nicole"
PACE = 1.08  # overall delivery speed for this reel (fits 60 s)
# style -> speed
SPEED = {"whisper": 0.95, "flat": 1.0, "annoyed": 1.08, "normal": 1.0, "serious": 0.97, "warm": 0.97}

def load():
    os.makedirs(CACHE, exist_ok=True)
    for f in FILES:
        p = os.path.join(CACHE, f)
        if not os.path.exists(p):
            print("downloading", f); urllib.request.urlretrieve(URL + f, p)
    return Kokoro(*(os.path.join(CACHE, f) for f in FILES))

def style(k, who, s):
    base = k.get_voice_style(VOICE[who])
    if s == "whisper":
        mix = 0.55 if who == "W" else 0.35   # husband keeps more of his own timbre
        return base * (1 - mix) + k.get_voice_style(WHISPER_VOICE) * mix
    return base

if __name__ == "__main__":
    os.makedirs("audio", exist_ok=True)
    k = load()
    for i, (who, text, s) in enumerate(json.load(open("lines.json"))):
        a, sr = k.create(text, voice=style(k, who, s), speed=SPEED[s] * PACE, lang="en-us")
        if s == "whisper": a = a * 0.75
        # trim leading/trailing silence so the timeline stays tight
        nz = np.where(np.abs(a) > 0.01)[0]
        if len(nz): a = a[max(0, nz[0] - 800): nz[-1] + 1600]
        sf.write(f"audio/{i:02d}.wav", a, sr)
        print(f"audio/{i:02d}.wav", text)
