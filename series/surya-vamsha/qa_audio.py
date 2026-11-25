"""Check narration against its script, offline (no credits).

    python3 qa_audio.py 1 2         # check finished audio/epNN.mp3; writes audio/qa/epNN.json

eleven_render.py also calls score() on every new recording and re-records the ones that fail.
For each piece it measures:
  - what was actually said (Whisper large-v3-turbo, run locally) vs. the script text:
      ratio  = spoken length / script length   (> 1.2 means extra words: repeats or context read aloud)
      sim    = how closely the words match (0..1)
  - silence at the start and end of the chunk, and the longest silence inside it
  - whether the audio is still loud in its last 40 ms (a word cut off mid-sound)
Needs `pip install faster-whisper`.
The first run downloads the model from Hugging Face (set HF_HUB_DISABLE_XET=1 if the Xet host is blocked).
"""
import difflib, glob, json, os, re, subprocess, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import eleven_render as er

SR = 16000
_model = None


def model():
    global _model
    if _model is None:
        os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
        from faster_whisper import WhisperModel
        _model = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8", cpu_threads=os.cpu_count())
    return _model


def load(path):
    out = subprocess.check_output(["ffmpeg", "-loglevel", "error", "-i", path, "-ac", "1", "-ar", str(SR),
                                   "-f", "f32le", "-"])
    return np.frombuffer(out, np.float32)


def norm(s):
    """Compare spellings loosely: drop punctuation, nuqta, chandrabindu/anusvara and matra variants Whisper mixes up."""
    s = re.sub(r"[^ऀ-ॿ ]", " ", s)
    s = s.replace("़", "").replace("ँ", "ं").replace("ं", "").replace("्", "")
    s = s.replace("ॉ", "ो").replace("ई", "इ").replace("ी", "ि").replace("ू", "ु").replace("ऊ", "उ")
    return re.sub(r"\s+", " ", s).strip()


def silences(a, thr_db=-40, win=0.02):
    """Leading silence, trailing silence, longest inner silence (s); loudness of the last 40 ms vs peak (dB)."""
    n = int(SR * win)
    frames = a[: len(a) // n * n].reshape(-1, n)
    db = 20 * np.log10(np.sqrt((frames ** 2).mean(axis=1)) + 1e-9)
    peak = db.max()
    loud = db > peak + thr_db
    idx = np.where(loud)[0]
    if not len(idx):
        return 0, 0, 0, -99
    lead, trail = idx[0] * win, (len(db) - 1 - idx[-1]) * win
    inner, run = 0, 0
    for v in loud[idx[0]: idx[-1] + 1]:
        run = 0 if v else run + 1
        inner = max(inner, run)
    tail = 20 * np.log10(np.sqrt((a[-int(SR * 0.04):] ** 2).mean()) + 1e-9) - peak
    return round(lead, 2), round(trail, 2), round(inner * win, 2), round(float(tail), 1)


def score(path_or_audio, text):
    """Transcribe one recording and compare it with the script text."""
    a = load(path_or_audio) if isinstance(path_or_audio, str) else path_or_audio
    segs, _ = model().transcribe(a, language="hi", beam_size=3, condition_on_previous_text=False, vad_filter=False)
    said = " ".join(s.text.strip() for s in segs)
    n_said, n_want = norm(said), norm(text)
    ratio = len(n_said) / max(1, len(n_want))
    sim = difflib.SequenceMatcher(None, n_said, n_want).ratio()
    lead, trail, inner, tail = silences(a)
    flags = []
    if ratio > 1.2: flags.append("extra words")
    if ratio < 0.8: flags.append("missing words")
    if sim < 0.72: flags.append("does not match")
    if tail > -25: flags.append("cut off at end")
    if inner > 1.5: flags.append(f"silence {inner}s inside")
    badness = abs(1 - ratio) * 2 + (1 - sim) + (0.5 if tail > -25 else 0)
    return dict(said=said, ratio=round(ratio, 2), sim=round(sim, 2), dur=round(len(a) / SR, 2), lead=lead,
                trail=trail, inner=inner, tail=tail, flags=flags, badness=round(badness, 3))


def check(ep):
    """Re-check the FINISHED episode audio: cut it at the timing file's marks and compare each piece."""
    base = os.path.join(HERE, "audio", f"ep{ep:02d}")
    timing = json.load(open(base + ".timing.json", encoding="utf-8"))
    a = load(base + ".mp3")
    rows, gaps, last_end = [], [], 0.0
    for it in timing["items"]:
        if it["kind"] != "text":
            continue
        gaps.append(round(it["start"] - last_end, 2)); last_end = it["end"]
        piece = a[int(it["start"] * SR): int(it["end"] * SR)]
        r = score(piece, it["text"])
        r.update(i=it["i"], text=it["text"], start=it["start"])
        rows.append(r)
        if r["flags"]:
            m, sec = divmod(it["start"], 60)
            print(f"E{ep:02d} {int(m)}:{sec:04.1f} {', '.join(r['flags']):28s} want: {it['text'][:60]}\n"
                  f"{'':40s}said: {r['said'][:90]}", flush=True)
    os.makedirs(os.path.join(HERE, "audio", "qa"), exist_ok=True)
    json.dump({"rows": rows, "max_gap": max(gaps)}, open(os.path.join(HERE, "audio", "qa", f"ep{ep:02d}.json"), "w"),
              ensure_ascii=False, indent=1)
    bad = sum(1 for r in rows if r["flags"])
    print(f"E{ep:02d}: {bad} of {len(rows)} pieces flagged; longest pause between pieces {max(gaps)} s", flush=True)
    return rows


if __name__ == "__main__":
    for e in sys.argv[1:]:
        check(int(e))
