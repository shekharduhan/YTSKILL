"""Generate an episode's images with Google's cheapest image model (gemini-2.5-flash-image).

    python3 gen_images.py 1            # all prompts in ep01-image-prompts.md
    python3 gen_images.py 1 7 12       # only images 7 and 12 (to redo a bad one)

Skips images that already exist, so a re-run never pays twice. Output: images/epNN/NN.png
The key is injected by the environment's network proxy (Authorization: Bearer).
"""
import base64, json, os, re, sys, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
STYLE = ("Polished digital painting in a premium animated Indian mythology film style, smooth cel-shaded colour "
         "with clean outlines, highly detailed, saturated warm golden-hour and firelight, amber, saffron and deep "
         "red against a dusk purple-blue sky, cinematic rim lighting, dignified faces, sacred and majestic, not cartoonish, "
         "not comic, no text, no watermark. ")
MODEL = "gemini-2.5-flash-image"

def prompts(ep):
    rows = {}
    for line in open(os.path.join(HERE, f"ep{ep:02d}-image-prompts.md"), encoding="utf-8"):
        m = re.match(r"\|\s*(\d+)\s*\|\s*([^|]+)\|\s*([^|]+)\|", line)
        if m: rows[int(m.group(1))] = m.group(3).strip()
    return rows

def gen(text, out):
    body = {"model": MODEL, "prompt": STYLE + text + ". Wide 16:9 landscape composition.", "n": 1,
            "size": "1536x864", "response_format": "b64_json"}
    req = urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/openai/images/generations",
        data=json.dumps(body).encode(), headers={"Content-Type": "application/json", "Authorization": "Bearer proxy-injected"})
    with urllib.request.urlopen(req, timeout=300) as r:
        open(out, "wb").write(base64.b64decode(json.load(r)["data"][0]["b64_json"]))

if __name__ == "__main__":
    ep = int(sys.argv[1]); only = {int(x) for x in sys.argv[2:]}
    d = os.path.join(HERE, "images", f"ep{ep:02d}"); os.makedirs(d, exist_ok=True)
    from concurrent.futures import ThreadPoolExecutor
    def one(item):
        n, text = item
        out = os.path.join(d, f"{n:02d}.png")
        if os.path.exists(out) and not only: return
        tmp = out + ".new"
        import time
        for attempt in range(8):          # empty replies and rate limits: retry (refused requests cost nothing)
            try:
                gen(text, tmp); os.replace(tmp, out)   # the old picture is replaced only on success
                print("ok", n, flush=True); return
            except Exception as e:
                err = e
                if "402" in str(e): break               # out of credit: retrying won't help
                if "429" in str(e): time.sleep(30 * (attempt + 1))   # per-minute limit: wait it out
        print("fail", n, err, flush=True)
    todo = [(n, t) for n, t in sorted(prompts(ep).items()) if not only or n in only]
    with ThreadPoolExecutor(2) as ex: list(ex.map(one, todo))
