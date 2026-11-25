#!/usr/bin/env python3
"""shotlist.py - turn narration timings into a shots.json skeleton (about one image per 5 s).

Input is the <out>.timings.json written by make_voice.py:
  {"duration": 41.2, "lines": [{"i":0, "text":"...", "start":0.3, "end":4.1, "section":"..."}]}

Rules
  * cuts land on sentence (line) boundaries whenever possible
  * short neighbouring lines are merged until a shot reaches --min seconds
  * a line longer than --max seconds is cut into several shots (word-proportional split)
  * shots are contiguous: shot k ends where shot k+1 starts; the first starts at 0 and the
    last ends at the audio duration, so assemble.py stays in sync with the voice
  * the first shot of each "## section" gets shot_type "wide_establishing" and a title stub
  * motion cycles zoom_in, pan_right, zoom_out, pan_left (edit freely)

Output (shots.json) - fill in "prompt" (and "title" where wanted), generate the images to the
"image" paths, then run assemble.py:
  {"audio": "voice.mp3", "duration": 41.2, "shots": [
     {"id": 1, "image": "images/shot_001.png", "start": 0.0, "end": 5.1, "duration_s": 5.1,
      "motion": "zoom_in", "shot_type": "wide_establishing", "section": "...",
      "narration": "...", "title": "", "prompt": ""}]}

Second language (same images, new timings)
  If the other-language script has the SAME number of spoken lines in the same order
  (one sentence per line, adapted line by line), --like retimes an existing shot list to the
  new voice: every shot keeps its image, prompt, motion and title but gets new start/end.
  Auto title stubs (the section name) are replaced by the new language's section name;
  hand-written titles are kept (or put per-language titles in "title_hi"/"title_en" and use
  assemble.py --title-key title_hi).

Examples
  python shotlist.py out/voice_hi.timings.json -o out/shots.json
  python shotlist.py out/voice_en.timings.json -o shots_en.json --like shots_hi.json
  python shotlist.py out/voice_hi.timings.json -o out/shots.json --target 4 --prompts out/prompts.md \\
         --chapters out/chapters.txt
"""
import argparse
import json
import os
import sys

MOTIONS = ["zoom_in", "pan_right", "zoom_out", "pan_left"]
# rough shot-type rhythm inside a section (wide -> dialogue -> close-up/insert -> ...)
SHOT_CYCLE = ["two_shot_dialogue", "close_up_reaction", "two_shot_dialogue", "object_insert",
              "single_medium", "wide_establishing", "two_shot_dialogue", "map"]


def split_long(line, max_len, target):
    """Split one long line into pieces of roughly `target` seconds, word-proportional."""
    dur = line["end"] - line["start"]
    n = max(2, round(dur / target))
    words = line["text"].split()
    n = min(n, max(1, len(words)))
    if n <= 1:
        return [dict(line)]
    total_chars = sum(len(w) + 1 for w in words)
    pieces, cur, acc = [], [], 0
    goal = total_chars / n
    for w in words:
        cur.append(w)
        acc += len(w) + 1
        if acc >= goal * (len(pieces) + 1) and len(pieces) < n - 1:
            pieces.append(" ".join(cur))
            cur = []
    if cur:
        pieces.append(" ".join(cur))
    out, t, frac = [], line["start"], 0.0
    for p in pieces:
        part = (len(p) + 1) / total_chars
        out.append({"text": p, "start": t, "end": t + dur * part, "section": line.get("section", ""),
                    "i": line["i"], "f0": round(frac, 4), "f1": round(min(1.0, frac + part), 4)})
        t += dur * part
        frac += part
    out[-1]["end"] = line["end"]
    out[-1]["f1"] = 1.0
    return out


def line_time(lines, i, f):
    ln = lines[i]
    return ln["start"] + f * (ln["end"] - ln["start"])


def retime_like(args, tm, lines, duration):
    with open(args.like, encoding="utf-8") as f:
        ref = json.load(f)
    rshots = ref["shots"] if isinstance(ref, dict) else ref
    if any("src" not in s for s in rshots):
        sys.exit("shotlist: %s has no 'src' line references (make it with this version of shotlist.py)" % args.like)
    n_ref = ref.get("n_lines") if isinstance(ref, dict) else None
    if n_ref is not None and n_ref != len(lines):
        sys.exit("shotlist: %s was built from %d spoken lines but %s has %d. --like needs the two scripts "
                 "to have the same number of lines in the same order (adapt line by line, keep '## ' "
                 "sections aligned)." % (args.like, n_ref, args.timings, len(lines)))
    spans = []
    for s in rshots:
        (i0, f0), (i1, f1) = s["src"]
        if i1 >= len(lines):
            sys.exit("shotlist: shot %s refers to line %d but the new timings have only %d lines" % (s.get("id"), i1 + 1, len(lines)))
        spans.append((line_time(lines, i0, f0), line_time(lines, i1, f1)))
    bounds = [0.0] + [round((spans[k][1] + spans[k + 1][0]) / 2, 3) for k in range(len(spans) - 1)] + [round(duration, 3)]
    shots = []
    for n, s in enumerate(rshots):
        t = dict(s)
        (i0, _), (i1, _) = s["src"]
        t["start"], t["end"] = bounds[n], bounds[n + 1]
        t["duration_s"] = round(bounds[n + 1] - bounds[n], 3)
        new_sec = lines[i0].get("section", "")
        if s.get("title") and s.get("section") and s["title"] == s["section"].upper() and new_sec:
            t["title"] = new_sec.upper()
        t["section"] = new_sec
        t["narration"] = " ".join(lines[i]["text"] for i in range(i0, i1 + 1))
        shots.append(t)
    return shots


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("timings", help="timings JSON from make_voice.py")
    ap.add_argument("-o", "--out", default="shots.json", help="output shots.json (default shots.json)")
    ap.add_argument("--target", type=float, default=5.0, help="target seconds per shot (default 5)")
    ap.add_argument("--min", dest="min_len", type=float, default=3.0, help="merge lines until a shot is at least this long (default 3)")
    ap.add_argument("--max", dest="max_len", type=float, default=7.0, help="split lines longer than this (default 7)")
    ap.add_argument("--image-dir", default="images", help="image folder written into each shot (default images)")
    ap.add_argument("--ext", default="png", help="image extension (default png)")
    ap.add_argument("--prompts", help="also write a Markdown prompt worksheet to this path")
    ap.add_argument("--chapters", help="also write YouTube chapter timestamps (from '## ' sections) to this path")
    ap.add_argument("--like", help="reuse this shots.json (other language, same line count): keep its images/prompts, retime to these timings")
    args = ap.parse_args()

    with open(args.timings, encoding="utf-8") as f:
        tm = json.load(f)
    lines = tm["lines"]
    for k, ln in enumerate(lines):
        ln.setdefault("i", k)
    duration = float(tm.get("duration") or lines[-1]["end"])
    # audio path relative to the shots.json folder, so assemble.py finds it without --audio
    audio = tm.get("audio", "")
    if audio and not os.path.isabs(audio):
        audio_abs = os.path.join(os.path.dirname(os.path.abspath(args.timings)), audio)
        audio = os.path.relpath(audio_abs, os.path.dirname(os.path.abspath(args.out)))

    if args.like:
        shots = retime_like(args, tm, lines, duration)
        write_outputs(args, tm, lines, duration, audio, shots)
        return

    # 1. split very long lines
    units = []
    for ln in lines:
        if ln["end"] - ln["start"] > args.max_len:
            units.extend(split_long(ln, args.max_len, args.target))
        else:
            units.append({"text": ln["text"], "start": ln["start"], "end": ln["end"], "section": ln.get("section", ""),
                          "i": ln["i"], "f0": 0.0, "f1": 1.0})

    # 2. greedy merge to ~target, never across a section change, never above max
    groups, cur = [], []
    for u in units:
        if cur:
            span = u["end"] - cur[0]["start"]
            cur_span = cur[-1]["end"] - cur[0]["start"]
            new_section = u["section"] != cur[0]["section"]
            if new_section or cur_span >= args.target or (cur_span >= args.min_len and span > args.max_len):
                groups.append(cur)
                cur = []
        cur.append(u)
    if cur:
        groups.append(cur)
    # fold a too-short last group into the previous one when it fits
    if len(groups) > 1 and groups[-1][-1]["end"] - groups[-1][0]["start"] < args.min_len * 0.6 \
            and groups[-1][0]["section"] == groups[-2][0]["section"]:
        groups[-2].extend(groups.pop())

    # 3. contiguous boundaries: cut halfway through the pause between groups
    bounds = [0.0]
    for a, b in zip(groups, groups[1:]):
        bounds.append(round((a[-1]["end"] + b[0]["start"]) / 2, 3))
    bounds.append(round(duration, 3))

    shots, last_section, k_in_section = [], None, 0
    for n, g in enumerate(groups):
        sec = g[0]["section"]
        if sec != last_section:
            k_in_section, last_section = 0, sec
        stype = "wide_establishing" if k_in_section == 0 else SHOT_CYCLE[(k_in_section - 1) % len(SHOT_CYCLE)]
        k_in_section += 1
        start, end = bounds[n], bounds[n + 1]
        shots.append({
            "id": n + 1,
            "image": "%s/shot_%03d.%s" % (args.image_dir, n + 1, args.ext),
            "start": start, "end": end, "duration_s": round(end - start, 3),
            "motion": MOTIONS[n % len(MOTIONS)],
            "shot_type": stype,
            "section": sec,
            "narration": " ".join(u["text"] for u in g),
            "title": ("%s" % sec.upper()) if (stype == "wide_establishing" and sec) else "",
            "prompt": "",
            "src": [[g[0]["i"], g[0]["f0"]], [g[-1]["i"], g[-1]["f1"]]],
        })
    write_outputs(args, tm, lines, duration, audio, shots)


def write_outputs(args, tm, lines, duration, audio, shots):
    out = {"audio": audio, "duration": duration, "lang": tm.get("lang", ""), "n_lines": len(lines), "shots": shots}
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    lens = [s["duration_s"] for s in shots]
    print("shotlist: %d shots over %.1f s (avg %.2f s, min %.2f, max %.2f) -> %s"
          % (len(shots), duration, sum(lens) / len(lens), min(lens), max(lens), args.out))

    if args.chapters:
        seen, rows = set(), []
        for s in shots:
            if s["section"] and s["section"] not in seen:
                seen.add(s["section"])
                t = 0 if not rows else int(s["start"])
                rows.append("%d:%02d %s" % (t // 60, t % 60, s["section"]))
        with open(args.chapters, "w", encoding="utf-8") as f:
            f.write("\n".join(rows) + "\n")
        print("shotlist: %d chapters -> %s" % (len(rows), args.chapters))
        if len(rows) < 3:
            print("shotlist: note - YouTube shows chapters only with 3+ entries (each 10 s or longer)")

    if args.prompts:
        with open(args.prompts, "w", encoding="utf-8") as f:
            f.write("# Image prompt worksheet\n\nPrepend the MASTER STYLE BLOCK (references/style-bible.md) to every prompt.\n"
                    "Generate every image WITHOUT text; titles are added by assemble.py.\n\n")
            for s in shots:
                f.write("## Shot %03d  [%s]  %.1f-%.1f s  motion=%s\n" % (s["id"], s["shot_type"], s["start"], s["end"], s["motion"]))
                f.write("Narration: %s\n\nPrompt: \n\n" % s["narration"])
        print("shotlist: prompt worksheet -> %s" % args.prompts)


if __name__ == "__main__":
    main()
