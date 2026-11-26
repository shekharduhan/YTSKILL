"""Check a picture plan against its script before any picture is drawn (free, no audio needed).

    python3 check_plan.py 21 22 23

For each epNN-image-prompts.md:
  - every "starts at" phrase occurs exactly once in the narration (as assemble.py will search it)
  - picture 1 starts at the very first narration words
  - pictures are in narration order, and none stays on screen much longer than ~20 s
    (estimated from characters: the voice speaks about 8 squashed characters a second, pauses included)
  - every prompt ends with the no-text guard and is 30-160 words
  - the Thumbnail line exists and points at a real picture
Exit code 1 if anything is wrong.
"""
import glob, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import eleven_render as er
from assemble import squash

CPS = 8.0   # squashed characters per second of narration, measured on E14-16 (pauses included)


def check(ep):
    md = open(glob.glob(os.path.join(HERE, f"ep{ep:02d}-*-hindi.md"))[0], encoding="utf-8").read()
    pieces = [squash(t) for k, t in er.plan(md) if k == "text"]
    full = "".join(pieces)
    plan = open(os.path.join(HERE, f"ep{ep:02d}-image-prompts.md"), encoding="utf-8").read()
    rows = []
    for line in plan.splitlines():
        m = re.match(r"\|\s*(\d+)\s*\|", line)
        if m:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            rows.append((int(m.group(1)), cells[-2], cells[-1]))
    bad = []
    pos = []
    for n, prompt, anchor in rows:
        key = squash(anchor)
        hits = sum(p.count(key) for p in pieces) if key else 0
        if hits != 1:
            bad.append(f"picture {n}: start words found {hits} times: {anchor}")
            continue
        pos.append((full.find(key), n))
        words = len(prompt.split())
        if not prompt.rstrip(". ").endswith("no text, no letters, no writing, no signature"):
            bad.append(f"picture {n}: prompt must end with 'no text, no letters, no writing, no signature'")
        if not 30 <= words <= 160:
            bad.append(f"picture {n}: prompt has {words} words (30-160)")
    if [n for n, _, _ in rows] != list(range(1, len(rows) + 1)):
        bad.append("pictures are not numbered 1..N in order")
    if pos and pos[0][0] != 0:
        bad.append("picture 1 does not start at the first narration words")
    if [n for _, n in sorted(pos)] != [n for _, n in pos]:
        bad.append("pictures are not in narration order")
    ends = sorted(pos) + [(len(full), None)]
    for (a, n), (b, _) in zip(ends, ends[1:]):
        secs = (b - a) / CPS
        if secs > 24:
            bad.append(f"picture {n}: on screen about {secs:.0f}s (add a picture or move a start)")
        if secs < 2.0:
            bad.append(f"picture {n}: on screen only about {secs:.1f}s")
    m = re.search(r"\*\*Thumbnail:\*\*\s*picture\s*(\d+),\s*words\s*(left|top|bottom)", plan)
    if not m or not 1 <= int(m.group(1)) <= len(rows):
        bad.append("missing or wrong '**Thumbnail:** picture K, words left|top|bottom' line")
    print(f"E{ep:02d}: {len(rows)} pictures, about {len(full) / CPS / 60:.1f} min, "
          f"{'OK' if not bad else str(len(bad)) + ' problems'}")
    for b in bad:
        print("  !", b)
    return not bad


if __name__ == "__main__":
    ok = all([check(int(e)) for e in sys.argv[1:]])
    sys.exit(0 if ok else 1)
