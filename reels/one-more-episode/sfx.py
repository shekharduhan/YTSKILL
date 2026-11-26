"""Synthesised sound effects (no samples, no API): evil organ sting + angelic harp chime."""
import numpy as np, wave
SR = 44100
def save(name, a):
    a = a / (np.abs(a).max() + 1e-6) * 0.9
    with wave.open(f"audio/{name}.wav", "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((a * 32767).astype(np.int16).tobytes())
N = lambda m: 440 * 2 ** ((m - 69) / 12)
def organ(f, t):
    return sum(np.sin(2 * np.pi * f * h * t) / h for h in (0.5, 1, 2, 3, 4))
# sting: three hits then a held diminished chord, with a low rumble
t = np.arange(int(SR * 2.4)) / SR
sting = np.zeros_like(t)
for k, start in enumerate((0.0, 0.18, 0.36)):
    m = (t >= start)
    tt = t[m] - start
    chord = [50, 53, 56, 59] if k < 2 else [38, 50, 53, 56, 59, 62]
    env = np.exp(-tt * (6 if k < 2 else 1.1))
    sting[m] += env * sum(organ(N(c), tt) for c in chord) / len(chord)
sting += 0.4 * np.sin(2 * np.pi * 41 * t) * np.exp(-t * 1.5)
save("sting", sting)
# chime: harp glissando up a major scale + shimmering pad
t = np.arange(int(SR * 3.0)) / SR
chime = np.zeros_like(t)
for k, m in enumerate([72, 74, 76, 79, 81, 84, 86, 88, 91, 93]):
    s = k * 0.07; mm = t >= s; tt = t[mm] - s
    chime[mm] += np.exp(-tt * 2.5) * (np.sin(2 * np.pi * N(m) * tt) + 0.3 * np.sin(4 * np.pi * N(m) * tt))
pad = sum(np.sin(2 * np.pi * N(m) * t * (1 + 0.002 * np.sin(5 * t))) for m in (60, 64, 67, 72))
chime += 0.35 * pad * np.minimum(t / 0.6, 1) * np.exp(-t * 0.8)
save("chime", chime)
print("audio/sting.wav audio/chime.wav")
