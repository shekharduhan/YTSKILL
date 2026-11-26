"""Render Hindi scripts to narration with ElevenLabs, check every recording, and time it exactly.

    python3 eleven_render.py 1            # episode 1
    python3 eleven_render.py 2 3 4
    python3 eleven_render.py all
    python3 eleven_render.py --no-qa 1    # skip the speech check (not recommended)

Needs network access to api.elevenlabs.io and an API key (injected by the environment's network
proxy, or read from ELEVENLABS_API_KEY).

How it renders
- The script is read paragraph by paragraph. A paragraph is all the consecutive spoken lines
  between blank lines, joined, so a sentence wrapped over two lines in the file is ONE recording.
  (Recording half-sentences made the voice stop abruptly and sometimes read neighbouring text.)
- Each paragraph is split only at [विराम]. Each piece is one request, with the neighbouring
  text sent as context so the delivery stays even.
- Every recording is transcribed offline (qa_audio.py, Whisper) and compared with the script. A
  recording with extra words (repeats, context read aloud), missing words or a cut-off ending is
  recorded once more without context and with a new seed (at most one retry), and the better take is kept.
  The approved recording of each line is remembered in audio/takes.json (line -> file), so a
  re-run never pays twice, and editing one line does not re-record its neighbours.
- Silence the voice adds at the start and end of a recording is trimmed, long silences inside a
  recording are shortened, and the script's pauses are added exactly:
      [विराम] 1.0 s    between paragraphs 0.5 s    new scene 0.8 s    (stacked pauses max 1.2 s)
- Output: audio/epNN.mp3 (levelled to -16 LUFS) and audio/epNN.timing.json, the exact start and
  end of every spoken piece. assemble.py and the subtitles use the timing file, so pictures and
  captions stay in sync with the voice.
"""
import glob, hashlib, json, os, re, subprocess, sys, tempfile, urllib.request
import numpy as np

VOICE_ID = "tp9ZAQ5ti5xjrtabLbxF"   # Vijay - Narrative Mythology (ElevenLabs voice library)
MODEL = "eleven_v4"
SETTINGS = {"stability": 0.5, "similarity_boost": 0.8, "style": 0.35, "speed": 0.9}
FULL, LINE, SCENE, MAX_PAUSE = 1.0, 0.5, 0.8, 1.2
SR = 44100

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "audio", "cache")
TAKES = os.path.join(HERE, "audio", "takes.json")
KEY = os.environ.get("ELEVENLABS_API_KEY", "proxy-injected")
DEVANAGARI = re.compile(r"[ऀ-ॿ]")


def plan(md):
    """[("text", str) | ("pause", sec) | ("scene", heading)] in speaking order."""
    body = md.split("\n---\n", 1)[1]
    body = re.split(r"(?m)^## (जाँच लें|कॉपी ब्लॉक)|^---\s*$", body)[0]
    items, para = [], []

    def flush():
        if not para:
            return
        text = " ".join(para).replace("**", "")
        text = re.sub(r"\s+", " ", text).strip()
        parts = [p.strip() for p in text.split("[विराम]")]
        for i, p in enumerate(parts):
            if DEVANAGARI.search(p) and p.strip(" …"):
                items.append(("text", p))
            if i < len(parts) - 1:
                items.append(("pause", FULL))
        items.append(("pause", LINE))
        para.clear()

    for line in body.splitlines():
        s = line.strip()
        if s.startswith("## "):
            flush(); items.append(("scene", s[3:])); items.append(("pause", SCENE)); continue
        if not s or "[स्क्रीन" in s or s.startswith(">"):
            flush(); continue
        para.append(s)
    flush()
    # merge stacked pauses so there is never long dead air
    out = []
    for kind, val in items:
        if kind == "pause":
            # a pause just before a scene heading merges with the scene's pause
            j = len(out) - 1
            while j >= 0 and out[j][0] == "scene":
                j -= 1
            if j >= 0 and out[j][0] == "pause":
                out[j] = ("pause", min(MAX_PAUSE, out[j][1] + val)); continue
        out.append((kind, val))
    while out and out[0][0] == "pause":
        out.pop(0)
    return out


def texts_of(items):
    return [v for k, v in items if k == "text"]


def chunk_path(text, prev, nxt, take=0):
    if take:   # retakes: no context (context is what gets read aloud by mistake), fixed seed
        key = hashlib.sha1(json.dumps([VOICE_ID, MODEL, SETTINGS, text, "take", take]).encode()).hexdigest()
    else:
        key = hashlib.sha1(json.dumps([VOICE_ID, MODEL, SETTINGS, text, prev, nxt]).encode()).hexdigest()
    return os.path.join(CACHE, key + ".mp3")


def tts(text, prev, nxt, take=0):
    path = chunk_path(text, prev, nxt, take)
    if os.path.exists(path):
        return path
    body = {"text": text, "model_id": MODEL, "language_code": "hi", "voice_settings": SETTINGS}
    if take:
        body["seed"] = 1000 + take
    else:
        if prev: body["previous_text"] = prev
        if nxt: body["next_text"] = nxt
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}?output_format=mp3_44100_128",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "xi-api-key": KEY})
    with urllib.request.urlopen(req, timeout=180) as r:
        data = r.read()
    os.makedirs(CACHE, exist_ok=True)
    open(path, "wb").write(data)
    return path


def decode(path):
    out = subprocess.check_output(["ffmpeg", "-loglevel", "error", "-i", path, "-ac", "1", "-ar", str(SR),
                                   "-f", "f32le", "-"])
    return np.frombuffer(out, np.float32).copy()


def tidy(a, lead=0.04, tail=0.12, max_gap=0.8, gap_to=0.55):
    """Trim edge silence, shorten long inner silences, fade the edges so nothing clicks."""
    n = int(SR * 0.01)
    fr = a[: len(a) // n * n].reshape(-1, n)
    db = 20 * np.log10(np.sqrt((fr ** 2).mean(axis=1)) + 1e-9)
    loud = db > db.max() - 42
    idx = np.where(loud)[0]
    if not len(idx):
        return a
    keep, run_start = [], None
    for j in range(idx[0], idx[-1] + 1):
        if loud[j]:
            if run_start is not None:
                gap = j - run_start
                limit = int(gap_to * 100) if gap > max_gap * 100 else gap
                keep.extend(range(run_start, run_start + limit))
                run_start = None
            keep.append(j)
        elif run_start is None:
            run_start = j
    body = np.concatenate([fr[k] for k in keep])
    pre = a[max(0, idx[0] * n - int(lead * SR)): idx[0] * n]
    post = a[(idx[-1] + 1) * n: (idx[-1] + 1) * n + int(tail * SR)]
    out = np.concatenate([pre, body, post])
    f = int(SR * 0.012)
    out[:f] *= np.linspace(0, 1, f); out[-f * 3:] *= np.linspace(1, 0, f * 3)
    return out


def load_takes():
    return json.load(open(TAKES, encoding="utf-8")) if os.path.exists(TAKES) else {}


def choose(text, prev, nxt, takes, qa=True):
    """Return the path of a good recording of `text`, re-recording if the speech check fails."""
    if text in takes:
        v = takes[text]
        if isinstance(v, str):                      # the approved recording's file, whatever its context
            path = os.path.join(CACHE, v)
            if os.path.exists(path):
                return path
        else:
            return tts(text, prev, nxt, v)
    if not qa:
        return tts(text, prev, nxt)
    import qa_audio
    best = None
    for take in range(0, 2):          # first recording + at most one retry of a broken take
        p = tts(text, prev, nxt, take)
        r = qa_audio.score(p, text)
        print(f"   take {take}: ratio {r['ratio']} sim {r['sim']} {', '.join(r['flags']) or 'ok'}", flush=True)
        if best is None or r["badness"] < best[1]["badness"]:
            best = (take, r)
        if not r["flags"]:
            break
    path = tts(text, prev, nxt, best[0])
    takes[text] = os.path.basename(path)
    json.dump(takes, open(TAKES, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if best[1]["flags"]:
        print(f"   !! kept best take {best[0]} but it still has: {', '.join(best[1]['flags'])}", flush=True)
    return path


def render(md_path, out_mp3, qa=True):
    items = plan(open(md_path, encoding="utf-8").read())
    texts = texts_of(items)
    takes = load_takes()
    pieces, timing, t, ti = [], [], 0.0, 0
    for kind, val in items:
        if kind == "scene":
            timing.append({"kind": "scene", "text": val, "start": round(t, 3)}); continue
        if kind == "pause":
            pieces.append(np.zeros(int(SR * val), np.float32)); t += int(SR * val) / SR; continue
        prev = texts[ti - 1] if ti > 0 else None
        nxt = texts[ti + 1] if ti + 1 < len(texts) else None
        print(f"[{ti + 1}/{len(texts)}] {val[:50]}", flush=True)
        a = tidy(decode(choose(val, prev, nxt, takes, qa)))
        timing.append({"kind": "text", "i": ti, "text": val, "start": round(t, 3), "end": round(t + len(a) / SR, 3)})
        pieces.append(a); t += len(a) / SR; ti += 1
    audio = np.concatenate(pieces)
    with tempfile.TemporaryDirectory() as tmp:
        raw = os.path.join(tmp, "raw.f32")
        audio.astype(np.float32).tofile(raw)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", raw,
                        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", str(SR), "-b:a", "160k", out_mp3], check=True)
    json.dump({"duration": round(t, 3), "items": timing},
              open(out_mp3.replace(".mp3", ".timing.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return t


def main(args):
    qa = "--no-qa" not in args
    args = [a for a in args if a != "--no-qa"]
    files = sorted(glob.glob(os.path.join(HERE, "ep*-hindi.md")))
    if args != ["all"]:
        want = {int(a) for a in args}
        files = [f for f in files if int(os.path.basename(f)[2:4]) in want]
    for f in files:
        n = os.path.basename(f)[2:4]
        out = os.path.join(HERE, "audio", f"ep{n}.mp3")
        t = render(f, out, qa)
        print("wrote", out, f"{t:.1f}s")


if __name__ == "__main__":
    main(sys.argv[1:] or ["1"])
