"""Check a finished video: is the right picture on screen when its words are spoken?

    python3 verify_video.py 2

For every picture in the shot plan (assemble.py), grabs the video frame 0.3 s after the picture's
narration words begin and halfway through its shot, and compares each frame with all of the
episode's pictures. Reports any moment where a different picture matches better, plus the video
and audio lengths (they must agree to within 0.1 s).
"""
import os, subprocess, sys, tempfile
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import assemble


def thumb(im):
    g = np.asarray(im.convert("L").resize((64, 36), Image.BILINEAR), np.float32)
    g -= g.mean()
    return g / (np.linalg.norm(g) + 1e-6)


def main(ep):
    shots, total, _ = assemble.shot_plan(ep)
    video = os.path.join(HERE, "video", f"ep{ep:02d}.mp4")
    refs = {}
    for n, _, _ in shots:
        tmp = os.path.join(tempfile.gettempdir(), f"vv{os.getpid()}.jpg")
        assemble.autocrop(os.path.join(HERE, "images", f"ep{ep:02d}", f"{n:02d}.png"), tmp)
        refs[n] = thumb(Image.open(tmp))
    bad = 0
    with tempfile.TemporaryDirectory() as d:
        for n, t, dur in shots:
            for label, at in (("start", t + assemble.XF + 0.3), ("middle", t + dur / 2)):
                f = os.path.join(d, "f.jpg")
                subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{at:.2f}", "-i", video, "-frames:v", "1", f],
                               check=True)
                fr = thumb(Image.open(f))
                scores = {k: float((fr * v).sum()) for k, v in refs.items()}
                best = max(scores, key=scores.get)
                if best != n:
                    bad += 1
                    print(f"  ! {int(at // 60)}:{at % 60:04.1f} ({label} of image {n}): looks like image {best} "
                          f"({scores[best]:.2f} vs {scores[n]:.2f})")
    v, a = assemble.dur(video), assemble.dur(os.path.join(HERE, "audio", f"ep{ep:02d}.mp3"))
    print(f"E{ep:02d}: {len(shots)} pictures, {bad} mismatches; video {v:.2f}s, narration {a:.2f}s")
    return bad == 0 and abs(v - a) < 0.1


if __name__ == "__main__":
    ok = all(main(int(e)) for e in sys.argv[1:])
    sys.exit(0 if ok else 1)
