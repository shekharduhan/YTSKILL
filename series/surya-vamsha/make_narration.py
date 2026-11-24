"""Turn each Hindi script into narration-only files for a voice artist or a TTS service.

    python3 make_narration.py

Writes, for every epNN-*-hindi.md:
  narration/epNN.txt   spoken words only, pauses as blank lines (for a human narrator)
  narration/epNN.ssml  SSML for neural TTS: slow, low, confident delivery, pauses as breaks

The SSML voice defaults to Azure's male Hindi neural voice hi-IN-MadhurNeural. Change VOICE,
RATE and PITCH below to suit the service you use. This is a generic stock voice, not an imitation
of any real person.
"""
import glob, os, re
from xml.sax.saxutils import escape

VOICE = "hi-IN-MadhurNeural"
RATE = "-12%"      # slower than default: measured, weighty
PITCH = "-6%"      # a little lower: deeper, more authoritative
SHORT_PAUSE = "450ms"   # for …
FULL_PAUSE = "2000ms"   # for [विराम]
SECTION_PAUSE = "1200ms"

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "narration")
os.makedirs(OUT, exist_ok=True)


def spoken_lines(md):
    body = md.split("\n---\n", 1)[1]
    body = re.split(r"(?m)^## (जाँच लें|कॉपी ब्लॉक)", body)[0]
    sections, cur = [], []
    for line in body.splitlines():
        if line.startswith("## "):
            if cur:
                sections.append(cur)
            cur = []
            continue
        if "[स्क्रीन" in line or line.startswith(">"):
            continue
        line = line.strip()
        if not line:
            continue
        line = line.replace("**", "")
        cur.append(line)
    if cur:
        sections.append(cur)
    return sections


def to_txt(sections):
    out = []
    for sec in sections:
        for line in sec:
            out.append(line.replace("[विराम]", "\n").strip())
        out.append("")
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip() + "\n"


def to_ssml(sections):
    parts = []
    for sec in sections:
        for line in sec:
            t = escape(line)
            t = t.replace("[विराम]", f'<break time="{FULL_PAUSE}"/>')
            t = t.replace("…", f'<break time="{SHORT_PAUSE}"/>')
            parts.append(t)
        parts.append(f'<break time="{SECTION_PAUSE}"/>')
    inner = "\n".join(parts)
    return (
        '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="hi-IN">\n'
        f'<voice name="{VOICE}"><prosody rate="{RATE}" pitch="{PITCH}">\n'
        f"{inner}\n"
        "</prosody></voice>\n</speak>\n"
    )


for f in sorted(glob.glob(os.path.join(HERE, "ep*-hindi.md"))):
    n = re.match(r"ep(\d+)", os.path.basename(f)).group(1)
    secs = spoken_lines(open(f, encoding="utf-8").read())
    open(os.path.join(OUT, f"ep{n}.txt"), "w", encoding="utf-8").write(to_txt(secs))
    open(os.path.join(OUT, f"ep{n}.ssml"), "w", encoding="utf-8").write(to_ssml(secs))
print("wrote", len(glob.glob(os.path.join(OUT, "*.txt"))), "narration files to", OUT)
