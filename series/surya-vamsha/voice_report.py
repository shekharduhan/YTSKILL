"""Deeper voice check of a finished narration, on top of qa_audio.py.

    python3 voice_report.py 1 2

Uses audio/epNN.mp3, its timing file and audio/qa/epNN.json (from qa_audio.py). Reports:
  - repeats across pieces: the end of one piece's transcript heard again at the start of the next
  - loudness jumps: a piece more than 4 dB louder or quieter than the episode's median
  - speed jumps: a piece spoken much faster or slower (characters per second) than the median
  - clipping: samples at full scale
  - dead air: any silence longer than 1.8 s anywhere in the file
"""
import json, os, re, subprocess, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from qa_audio import load, norm, SR


def words(s):
    return norm(s).split()


def report(ep):
    base = os.path.join(HERE, "audio", f"ep{ep:02d}")
    timing = [x for x in json.load(open(base + ".timing.json", encoding="utf-8"))["items"] if x["kind"] == "text"]
    qa = {r["i"]: r for r in json.load(open(os.path.join(HERE, "audio", "qa", f"ep{ep:02d}.json")))["rows"]}
    a = load(base + ".mp3")
    problems = []

    def at(t):
        return f"{int(t // 60)}:{t % 60:04.1f}"

    # repeats across boundaries: last 3 spoken words of a piece == first 3 of the next (but not in the script)
    for x, y in zip(timing, timing[1:]):
        sx, sy = words(qa[x["i"]]["said"]), words(qa[y["i"]]["said"])
        wy = words(y["text"])
        for k in (4, 3):
            if len(sx) >= k and len(sy) >= k and sx[-k:] == sy[:k] and wy[:k] != words(x["text"])[-k:]:
                problems.append(f"{at(y['start'])} repeat across pieces: {' '.join(sy[:k])}"); break

    # loudness and speed per piece
    lufs, rate = [], []
    for x in timing:
        seg = a[int(x["start"] * SR): int(x["end"] * SR)]
        rms = 20 * np.log10(np.sqrt((seg ** 2).mean()) + 1e-9)
        lufs.append(rms)
        rate.append(len(norm(x["text"]).replace(" ", "")) / max(0.1, x["end"] - x["start"]))
    ml, mr = np.median(lufs), np.median(rate)
    for x, l, r in zip(timing, lufs, rate):
        if abs(l - ml) > 4:
            problems.append(f"{at(x['start'])} loudness {l - ml:+.1f} dB vs the rest: {x['text'][:40]}")
        if r > mr * 1.35 or r < mr * 0.65:
            problems.append(f"{at(x['start'])} speed {r / mr:.2f}x the usual: {x['text'][:40]}")

    # clipping
    clipped = int((np.abs(a) > 0.999).sum())
    if clipped > 10:
        problems.append(f"{clipped} clipped samples")

    # dead air anywhere (10 ms frames below -50 dBFS)
    n = int(SR * 0.01)
    fr = a[: len(a) // n * n].reshape(-1, n)
    quiet = 20 * np.log10(np.sqrt((fr ** 2).mean(axis=1)) + 1e-9) < -50
    run, longest, where = 0, 0, 0
    for i, q in enumerate(quiet):
        run = run + 1 if q else 0
        if run > longest:
            longest, where = run, i - run + 1
    if longest * 0.01 > 1.8:
        problems.append(f"{at(where * 0.01)} silence of {longest * 0.01:.1f}s")

    flagged = sum(1 for r in qa.values() if r["flags"])
    print(f"E{ep:02d} voice: {len(timing)} pieces, {flagged} failed the script check, "
          f"longest silence {longest * 0.01:.1f}s, loudness spread {min(lufs) - ml:+.1f}/{max(lufs) - ml:+.1f} dB, "
          f"speed spread {min(rate) / mr:.2f}-{max(rate) / mr:.2f}x, clipped samples {clipped}")
    for p in problems:
        print("  !", p)
    if not problems:
        print("  no problems found")
    return not problems and not flagged


if __name__ == "__main__":
    ok = all([report(int(e)) for e in sys.argv[1:]])
    sys.exit(0 if ok else 1)
