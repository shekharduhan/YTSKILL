"""Render Hindi scripts to narration with ElevenLabs.

    python3 eleven_render.py 1            # episode 1
    python3 eleven_render.py 2 3 4
    python3 eleven_render.py all

Needs network access to api.elevenlabs.io and an API key. The key is either injected by the
environment's network proxy, or read from ELEVENLABS_API_KEY.

How it renders: each script line is split at [विराम]; every chunk is one request (with the
neighbouring text sent as context so the delivery stays even); chunks are joined with silences:
  [विराम]  1.6 s   end of line 0.45 s   new scene 1.0 s
"…" stays in the text, so the voice takes its own short breath there.
Output: audio/epNN.mp3, levelled to -16 LUFS. Chunks are cached in audio/cache/, so re-running
after an edit only pays for the lines that changed.
"""
import glob, hashlib, json, os, re, subprocess, sys, tempfile, urllib.request

VOICE_ID = "tp9ZAQ5ti5xjrtabLbxF"   # Vijay - Narrative Mythology (ElevenLabs voice library)
MODEL = "eleven_v4"
SETTINGS = {"stability": 0.5, "similarity_boost": 0.8, "style": 0.35, "speed": 0.9}
FULL, LINE, SCENE = 1.6, 0.45, 1.0

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "audio", "cache")
KEY = os.environ.get("ELEVENLABS_API_KEY", "proxy-injected")


def plan(md):
    body = md.split("\n---\n", 1)[1]
    body = re.split(r"(?m)^## (जाँच लें|कॉपी ब्लॉक)", body)[0]
    items = []
    for line in body.splitlines():
        if line.startswith("## "):
            items.append(("pause", SCENE)); continue
        if "[स्क्रीन" in line or line.startswith(">") or not line.strip():
            continue
        line = line.replace("**", "").strip()
        parts = [p.strip() for p in line.split("[विराम]")]
        for i, p in enumerate(parts):
            if p.strip(" …"):
                items.append(("text", p))
            if i < len(parts) - 1:
                items.append(("pause", FULL))
        items.append(("pause", LINE))
    return items


def tts(text, prev, nxt):
    key = hashlib.sha1(json.dumps([VOICE_ID, MODEL, SETTINGS, text, prev, nxt]).encode()).hexdigest()
    path = os.path.join(CACHE, key + ".mp3")
    if os.path.exists(path):
        return path
    body = {"text": text, "model_id": MODEL, "language_code": "hi", "voice_settings": SETTINGS}
    if prev: body["previous_text"] = prev
    if nxt: body["next_text"] = nxt
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}?output_format=mp3_44100_128",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "xi-api-key": KEY})
    with urllib.request.urlopen(req, timeout=180) as r:
        data = r.read()
    open(path, "wb").write(data)
    return path


def render(md_path, out_mp3):
    items = plan(open(md_path, encoding="utf-8").read())
    texts = [v for k, v in items if k == "text"]
    with tempfile.TemporaryDirectory() as tmp:
        silences = {}
        def silence(sec):
            if sec not in silences:
                p = os.path.join(tmp, f"sil{int(sec*1000)}.wav")
                subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i",
                                "anullsrc=r=44100:cl=mono", "-t", str(sec), p], check=True)
                silences[sec] = p
            return silences[sec]
        parts, ti = [], 0
        for kind, val in items:
            if kind == "pause":
                parts.append(silence(val))
            else:
                prev = texts[ti - 1] if ti > 0 else None
                nxt = texts[ti + 1] if ti + 1 < len(texts) else None
                mp3 = tts(val, prev, nxt)
                wav = os.path.join(tmp, f"t{ti}.wav")
                subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", mp3, "-ac", "1", "-ar", "44100", wav], check=True)
                parts.append(wav); ti += 1
        lst = os.path.join(tmp, "list.txt")
        open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
                        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "44100", "-b:a", "160k", out_mp3], check=True)


def main(args):
    os.makedirs(CACHE, exist_ok=True)
    files = sorted(glob.glob(os.path.join(HERE, "ep*-hindi.md")))
    if args != ["all"]:
        want = {int(a) for a in args}
        files = [f for f in files if int(os.path.basename(f)[2:4]) in want]
    for f in files:
        n = os.path.basename(f)[2:4]
        out = os.path.join(HERE, "audio", f"ep{n}.mp3")
        render(f, out)
        print("wrote", out)


if __name__ == "__main__":
    main(sys.argv[1:] or ["1"])
