"""Mix dialogue + sfx + music onto the timeline the renderer wrote, then mux with the video."""
import json, subprocess, sys
OUT = sys.argv[1] if len(sys.argv) > 1 else "devil-or-angel-reel.mp4"
tl = json.load(open("timeline.json")); st = {x["i"]: x["start"] for x in tl if "i" in x}
inputs, filt, labels = [], [], []
def add(path, t, vol):
    k = len(labels); ms = int(max(0, t) * 1000)
    inputs.extend(["-i", path])
    filt.append(f"[{k}:a]aresample=44100,aformat=channel_layouts=stereo,adelay={ms}|{ms},volume={vol}[v{k}]")
    labels.append(f"[v{k}]")
for i in range(len(st)): add(f"audio/{i:02d}.wav", st[i], 1.4)
add("audio/sting.wav", st[5] - 0.05, 0.5); add("audio/sting.wav", st[15] - 0.05, 0.55); add("audio/chime.wav", st[12] - 0.2, 0.4)
add("audio/music.wav", 0, 0.12)
filt.append("".join(labels) + f"amix=inputs={len(labels)}:normalize=0,atrim=0:60,afade=t=out:st=58:d=2,alimiter=limit=0.95[out]")
subprocess.run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(filt), "-map", "[out]", "-c:a", "aac", "-b:a", "192k", "mix.m4a"], check=True)
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", "video_only.mp4", "-i", "mix.m4a", "-map", "0:v", "-map", "1:a", "-c", "copy",
                "-shortest", "-movflags", "+faststart", OUT], check=True)
print("wrote", OUT)
