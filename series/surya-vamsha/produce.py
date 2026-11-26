"""Make finished episodes end to end, once, with every check.

    python3 produce.py audio 3 4 5       # record narration (each line checked; at most one retry of a broken take)
    python3 produce.py images 3 4 5      # draw each picture ONCE (never redraws an existing picture)
    python3 produce.py build 3 4 5       # video + thumbnail + subtitles + all checks + report

Writes reports/epNN.txt with the check results. Nothing here pays twice: recordings are cached per
line, pictures are skipped if they exist.
"""
import glob, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def run(cmd):
    p = subprocess.run(cmd, cwd=HERE, capture_output=True, text=True)
    out = "\n".join(l for l in (p.stdout + p.stderr).splitlines() if "warn" not in l.lower())
    return p.returncode, out


def thumb_settings(ep):
    """'**Thumbnail:** picture 7, words left' line in the prompt table (default: picture 1, bottom)."""
    s = open(os.path.join(HERE, f"ep{ep:02d}-image-prompts.md"), encoding="utf-8").read()
    m = re.search(r"\*\*Thumbnail:\*\*\s*picture\s*(\d+)(?:,\s*words\s*(left|top|bottom))?", s)
    return (int(m.group(1)), m.group(2) or "bottom") if m else (1, "bottom")


def audio(eps):
    import eleven_render as er
    for ep in eps:
        md = glob.glob(os.path.join(HERE, f"ep{ep:02d}-*-hindi.md"))[0]
        t = er.render(md, os.path.join(HERE, "audio", f"ep{ep:02d}.mp3"))
        print(f"E{ep:02d} narration {t:.1f}s", flush=True)


def images(eps):
    for ep in eps:
        code, out = run(["python3", "gen_images.py", str(ep)])
        n = len(glob.glob(os.path.join(HERE, "images", f"ep{ep:02d}", "*.png")))
        fails = [l for l in out.splitlines() if l.startswith("fail")]
        print(f"E{ep:02d} pictures on disk: {n}; failed now: {len(fails)} {fails[:3]}", flush=True)


def build(eps):
    os.makedirs(os.path.join(HERE, "reports"), exist_ok=True)
    for ep in eps:
        rep = [f"E{ep:02d} production report"]
        code, out = run(["python3", "assemble.py", "--check", str(ep)])
        rep.append("timing plan problems:\n" + ("\n".join(l for l in out.splitlines() if "!" in l) or "  none"))
        if any("not found" in l for l in out.splitlines()):
            rep.append("STOPPED: a picture's start words are missing from the narration")
            print("\n".join(rep)); continue
        code, out = run(["python3", "assemble.py", str(ep)])
        rep.append(out.splitlines()[-1] if out else "assemble: no output")
        n, pos = thumb_settings(ep)
        code, out = run(["python3", "brand_assets.py", "thumb", str(ep), f"images/ep{ep:02d}/{n:02d}.png", "0.5", pos])
        rep.append(out.strip())
        for tool in ("qa_audio.py", "voice_report.py", "verify_video.py", "sync_check.py"):
            code, out = run(["python3", tool, str(ep)])
            rep.append(f"--- {tool}\n{out.strip()}")
        open(os.path.join(HERE, "reports", f"ep{ep:02d}.txt"), "w", encoding="utf-8").write("\n".join(rep) + "\n")
        print("\n".join(rep), flush=True)


if __name__ == "__main__":
    step, eps = sys.argv[1], [int(a) for a in sys.argv[2:]]
    {"audio": audio, "images": images, "build": build}[step](eps)
