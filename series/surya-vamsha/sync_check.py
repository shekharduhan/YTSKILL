"""Audio-video sync check on the FINISHED video file.

    python3 sync_check.py 1 2

1. The MP4's audio and video streams must both start at 0 and end within 0.1 s of each other.
2. For every narration piece, the audio is read out of the MP4 at the piece's planned start and
   transcribed (offline Whisper). The first words heard must be that piece's first words. If the
   audio had drifted or been offset, the words heard would belong to a neighbouring piece.
3. For every picture, the frame at its words is checked by verify_video.py (run it too); together
   these show each picture is on screen exactly while its words are spoken.
"""
import difflib, json, os, subprocess, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from qa_audio import model, norm, SR


def probe(path):
    out = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries",
                                   "stream=codec_type,start_time,duration", "-of", "json", path])
    return {s["codec_type"]: (float(s.get("start_time", 0)), float(s["duration"])) for s in json.loads(out)["streams"]}


def clip(path, start, length):
    out = subprocess.check_output(["ffmpeg", "-loglevel", "error", "-ss", f"{start:.3f}", "-t", f"{length:.3f}",
                                   "-i", path, "-vn", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"])
    return np.frombuffer(out, np.float32)


def check(ep):
    video = os.path.join(HERE, "video", f"ep{ep:02d}.mp4")
    st = probe(video)
    (vs, vd), (as_, ad) = st["video"], st["audio"]
    ok = abs(vs) < 0.05 and abs(as_) < 0.05 and abs(vd - ad) < 0.1
    print(f"E{ep:02d} streams: video starts {vs:.3f}s lasts {vd:.2f}s | audio starts {as_:.3f}s lasts {ad:.2f}s"
          f" -> {'OK' if ok else 'MISMATCH'}")
    pieces = [x for x in json.load(open(os.path.join(HERE, "audio", f"ep{ep:02d}.timing.json"), encoding="utf-8"))["items"]
              if x["kind"] == "text"]
    bad = 0
    for x in pieces:
        a = clip(video, x["start"], min(2.5, x["end"] - x["start"]))
        segs, _ = model().transcribe(a, language="hi", beam_size=3, condition_on_previous_text=False)
        heard = norm(" ".join(s.text for s in segs))
        want = norm(x["text"])[: max(8, len(heard))]
        sim = difflib.SequenceMatcher(None, heard[: len(want)], want).ratio()
        if sim < 0.6:
            bad += 1
            print(f"  ! {int(x['start'] // 60)}:{x['start'] % 60:04.1f} expected: {x['text'][:45]}\n"
                  f"    {'':12s}heard:    {heard[:45]}  (match {sim:.2f})")
    print(f"E{ep:02d}: {len(pieces)} pieces checked in the video file, {bad} out of sync")
    return ok and bad == 0


if __name__ == "__main__":
    ok = all([check(int(e)) for e in sys.argv[1:]])
    sys.exit(0 if ok else 1)
