"""Assemble an episode video: images + ElevenLabs narration -> 1080p MP4.

    python3 assemble.py 1

Needs: audio/epNN.mp3 (eleven_render.py, with its chunk cache), images/epNN/NN.png
(gen_images.py), and epNN-image-prompts.md whose "scene" column says which script section
each image belongs to (see SECTION_OF below).

Each image is shown for an equal share of its section's narration time, with a slow
Ken Burns zoom (alternating in/out) and a 0.6 s crossfade. Black letterbox bars in generated
images are cropped first. Output: video/epNN.mp4 (H.264 + AAC, 1920x1080, 25 fps).
"""
import glob, json, os, re, subprocess, sys, tempfile
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import eleven_render as er

HERE = os.path.dirname(os.path.abspath(__file__))
W, H, FPS, XF = 1920, 1080, 25, 0.6


def dur(path):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", path]).strip())


def section_times(md_path):
    """Start/end seconds of each '## ' section, from the cached narration chunks."""
    items = er.plan(open(md_path, encoding="utf-8").read())
    texts = [v for k, v in items if k == "text"]
    t, ti, bounds = 0.0, 0, [0.0]
    for kind, val in items:
        if kind == "pause":
            if val == er.SCENE:
                bounds.append(t)
            t += val
        else:
            prev = texts[ti - 1] if ti > 0 else None
            nxt = texts[ti + 1] if ti + 1 < len(texts) else None
            t += dur(er.tts(val, prev, nxt)); ti += 1
    bounds.append(t)
    # bounds[0]=0 then one per heading; the first heading is at t=0, so drop the duplicate
    starts = [b for i, b in enumerate(bounds[:-1]) if not (i == 1 and b == 0.0)]
    return list(zip(starts, starts[1:] + [t])), t


def section_of_images(ep, n_sections):
    """Map each image to a section index using the prompts file's scene column, in order."""
    rows = []
    for line in open(os.path.join(HERE, f"ep{ep:02d}-image-prompts.md"), encoding="utf-8"):
        m = re.match(r"\|\s*(\d+)\s*\|\s*([^|]+)\|", line)
        if m:
            rows.append((int(m.group(1)), m.group(2).strip()))
    labels, sec, out = [], -1, {}
    for n, lab in rows:
        if lab not in labels:
            labels.append(lab); sec += 1
        out[n] = sec
    return out, labels


def autocrop(src, dst):
    im = Image.open(src).convert("RGB")
    a = np.asarray(im).mean(axis=2)
    rows = np.where(a.mean(axis=1) > 18)[0]; cols = np.where(a.mean(axis=0) > 18)[0]
    im = im.crop((cols[0], rows[0], cols[-1] + 1, rows[-1] + 1))
    w, h = im.size; target = W / H
    if w / h > target:
        nw = int(h * target); im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else:
        nh = int(w / target); im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    im.resize((W * 2, H * 2), Image.LANCZOS).save(dst, quality=92)


def main(ep, mapping=None):
    md = glob.glob(os.path.join(HERE, f"ep{ep:02d}-*-hindi.md"))[0]
    audio = os.path.join(HERE, "audio", f"ep{ep:02d}.mp3")
    sections, total = section_times(md)
    img_sec, labels = section_of_images(ep, len(sections))
    if mapping:
        img_sec = {n: mapping[labels[s]] for n, s in img_sec.items()}
    per_sec = {}
    for n, s in sorted(img_sec.items()):
        per_sec.setdefault(s, []).append(n)
    # assign durations
    shots = []
    for s, (a, b) in enumerate(sections):
        imgs = per_sec.get(s, [])
        if not imgs:
            if shots: shots[-1][1] += b - a          # extend previous image over an image-less section
            continue
        for n in imgs:
            shots.append([n, (b - a) / len(imgs)])
    out_dir = os.path.join(HERE, "video"); os.makedirs(out_dir, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        clips = []
        for i, (n, d) in enumerate(shots):
            src = os.path.join(HERE, "images", f"ep{ep:02d}", f"{n:02d}.png")
            big = os.path.join(tmp, f"{n:02d}.jpg"); autocrop(src, big)
            length = d + (XF if i < len(shots) - 1 else 0)
            frames = int(round(length * FPS))
            z = "min(1+0.0009*on,1.15)" if i % 2 == 0 else "max(1.15-0.0009*on,1)"
            clip = os.path.join(tmp, f"c{i:02d}.mp4")
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i", big, "-vf",
                            f"zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s={W}x{H}:fps={FPS},format=yuv420p",
                            "-frames:v", str(frames), "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", clip], check=True)
            clips.append((clip, length))
        # chain crossfades
        inputs, filt, last, offset = [], [], "[0:v]", 0.0
        for i, (c, L) in enumerate(clips):
            inputs += ["-i", c]
        for i in range(1, len(clips)):
            offset += clips[i - 1][1] - XF
            filt.append(f"{last}[{i}:v]xfade=transition=fade:duration={XF}:offset={offset:.3f}[v{i}]")
            last = f"[v{i}]"
        silent = os.path.join(tmp, "silent.mp4")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(filt),
                        "-map", last, "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", silent], check=True)
        out = os.path.join(out_dir, f"ep{ep:02d}.mp4")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", silent, "-i", audio, "-map", "0:v", "-map", "1:a",
                        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], check=True)
    print("wrote", out, f"{total:.1f}s narration, {len(shots)} shots")


if __name__ == "__main__":
    main(int(sys.argv[1]))
