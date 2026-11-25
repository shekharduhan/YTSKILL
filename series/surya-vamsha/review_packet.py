"""Make a review packet for an episode: frames from the finished video with the words spoken there.

    python3 review_packet.py 1 OUTDIR

Writes OUTDIR/epNN/shotNN-start.jpg and -middle.jpg for every picture (taken from video/epNN.mp4),
and OUTDIR/epNN/shots.json listing, per shot: time, picture number, its prompt, and the narration
spoken while it is on screen. Reviewers use it to check picture-vs-words, continuity and drawing
mistakes without having to play the video.
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import assemble, gen_images


def main(ep, outdir):
    d = os.path.join(outdir, f"ep{ep:02d}"); os.makedirs(d, exist_ok=True)
    shots, total, _ = assemble.shot_plan(ep)
    prompts = gen_images.prompts(ep)
    pieces = [x for x in json.load(open(os.path.join(HERE, "audio", f"ep{ep:02d}.timing.json"), encoding="utf-8"))["items"]
              if x["kind"] == "text"]
    video = os.path.join(HERE, "video", f"ep{ep:02d}.mp4")
    rows = []
    for k, (n, t, dur) in enumerate(shots):
        spoken = [p["text"] for p in pieces if p["end"] > t + assemble.XF and p["start"] < t + dur]
        files = {}
        for label, at in (("start", t + assemble.XF + 0.3), ("middle", t + dur / 2)):
            f = os.path.join(d, f"shot{k + 1:02d}-{label}.jpg")
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{at:.2f}", "-i", video, "-frames:v", "1",
                            "-vf", "scale=960:-1", "-q:v", "3", f], check=True)
            files[label] = f
        rows.append({"shot": k + 1, "picture": n, "on_screen": f"{int(t // 60)}:{t % 60:04.1f}",
                     "seconds": round(dur, 1), "prompt": prompts[n], "narration_while_on_screen": spoken,
                     "frames": files})
    json.dump(rows, open(os.path.join(d, "shots.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("wrote", d, len(rows), "shots")


if __name__ == "__main__":
    main(int(sys.argv[1]), sys.argv[2])
