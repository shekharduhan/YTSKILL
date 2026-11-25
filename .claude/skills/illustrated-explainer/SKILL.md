---
name: illustrated-explainer
description: Make a narrated illustrated-explainer video (AI still images + Ken Burns motion + one TTS narrator + captions), in English, Hindi or both. Use when the user asks for "the entire history of X in N minutes", "an illustrated history/explainer video", "a cartoon history video like the square-head channels", "make this topic into a YouTube explainer", a Hindi/Hinglish history video, or a cheap alternative to AI video generators for long narrated videos. Covers research, script formula, shot list, image prompts, voice, captions and ffmpeg assembly to 16:9 or 9:16.
---

# Illustrated explainer video

The format: one calm narrator tells a whole story (history of a country, an empire, an
idea) in 8-15 minutes over a new flat-cartoon still image every 3-5 s. The stills are
AI-generated, get slow pan/zoom ("Ken Burns") motion and short crossfades, and carry
occasional `NAME — YEAR` titles. No video generator is needed, which is why it is cheap:
about 170-250 images and one voice track per 14-minute video.

Read these when you reach the step that needs them:
- `references/script-formula.md` - structure, word budget, rhetorical patterns, Hindi rules
- `references/style-bible.md` - the MASTER STYLE BLOCK, shot-type mix, shot prompts, palette, character cards
- `references/production-stack.md` - image/voice/music options, Hindi voices, costs, hardware

Scripts (in `scripts/`, run with `python`; need ffmpeg + ffprobe on PATH):
| script | what it does |
|---|---|
| `make_voice.py` | script text -> `voice.mp3` + `voice.timings.json` (per-line start/end) + `voice.srt`. Backends: `edge` (free, default), `elevenlabs` (paid), `dryrun` (silent test track, offline) |
| `shotlist.py` | timings -> `shots.json` skeleton, ~5 s per shot, cuts on sentence boundaries, plus a prompt worksheet; `--like` retimes one language's shot list to the other language's voice |
| `placeholders.py` | stand-in images for every shot (needs Pillow) to test the edit before buying images |
| `assemble.py` | `shots.json` + voice [+ music, + srt] -> finished MP4, 1920x1080 or `--vertical` 1080x1920 |

## What Claude can and cannot do here

- **Can:** research, write and fact-check the script in English and Hindi, plan shots, write every
  image prompt, run TTS, build captions, and assemble the final MP4 with ffmpeg.
- **Cannot:** draw raster images itself. Pictures must come from an image tool: an image-generation
  MCP/connector in this session, an API key the user provides (e.g. Gemini via Google AI Studio,
  OpenAI images), a local FLUX/SDXL setup, or images the user generates by hand from the
  prompts and drops into `images/`. Say this plainly before step 5, and never pass off placeholders as final art.
- Cannot hear reference videos. If the user points at an example video, work from its
  transcript/thumbnails and say that voice judgments are guesses.

## Pipeline

Work in a project folder, e.g. `videos/<slug>/` with `script_en.txt`, `script_hi.txt`, `images/`, `out/`.

### 1. Topic and brief (ask only what is missing)
Topic, length in minutes (default 12), language(s) (`en`, `hi`, or both), aspect (16:9, plus
optional 9:16 Shorts cut-downs), voice preference, and which image tool they have. Default to
what they already have; do not push a paid service.

### 2. Research
Gather 8-12 eras/beats, each with dates, 2-3 concrete objects or images, one surprising fact,
one common myth to correct, and one point scholars debate. Use web search if available and
keep a short source list in `notes.md`. Hedge disputed facts ("historians debate…",
"estimates range from…"), especially caste, religion, Partition, borders and death tolls.

### 3. Script (follow `references/script-formula.md`)
- Budget: English minutes x 155 words; Hindi minutes x 130 words.
- Cold open (deep-time or physical event + present-day wonder fact + "this shaped everything"),
  a thesis question by second ~35, one era per section, a callback ending that answers the
  question, a three-option comment question, and a next-video line.
- Write the script file as **one sentence per line**, `## Section` lines for chapters, a blank
  line for an act-break pause. Hindi TTS scripts in Devanagari (TTS reads Latin Hinglish badly);
  English loanwords are fine in Devanagari or as-is.
- For both languages: write the English master first, then **adapt** (not translate) to Hindi.
  Keep names, numbers and title cards identical so one image set serves both voice tracks.
- Show the user the script for approval before spending on voice or images.

### 4. Voice + timings
```bash
python scripts/make_voice.py script_hi.txt -o out/voice_hi            # edge-tts, hi-IN-MadhurNeural
python scripts/make_voice.py script_en.txt -o out/voice_en            # edge-tts, en-US-GuyNeural
python scripts/make_voice.py script_hi.txt -o out/voice_hi --backend elevenlabs --voice <voice_id>
python scripts/make_voice.py --list-voices --lang hi
python scripts/make_voice.py script_hi.txt -o out/voice_hi --backend dryrun     # silent, offline test track
```
- Default: free `edge-tts` (`pip install edge-tts`). Hindi: `hi-IN-MadhurNeural` (m), `hi-IN-SwaraNeural` (f);
  English: `en-US-GuyNeural`, `en-US-AndrewNeural`, `en-IN-PrabhatNeural`. `--rate=-5%` for a calmer read
  (write it with `=`; the script also accepts `--rate -5%`).
- edge-tts needs the host `speech.platform.bing.com`. In sandboxed/cloud sessions it is often
  blocked (DNS/403); then use `--backend elevenlabs` if a key is available
  (`ELEVENLABS_API_KEY`; in a cloud session whose proxy injects the ElevenLabs key, set the variable to any
  placeholder such as `x` and the proxy supplies the real one), or run the step on the user's own PC.
  ElevenLabs bills per character: list voices with `--list-voices --backend elevenlabs` and pick one
  tagged for Hindi/Indian accent for Hindi; Claude cannot judge how a voice sounds.
- `--backend dryrun` writes a SILENT track with word-count-estimated timings (~155 wpm EN, ~130 wpm HI).
  Use it only to test shot lists and the edit without network or cost; never deliver it.
- Listen-check is the user's job: Claude cannot hear the result. Ask them to listen to the first 30 s.

### 5. Shot list
```bash
python scripts/shotlist.py out/voice_hi.timings.json -o shots.json --prompts prompts.md
```
Then fill each shot's `prompt` (and `title` where an era/name/date starts) following
`references/style-bible.md`: MASTER STYLE BLOCK + one shot description, about this mix:
dialogue two-shots 30%, wide/establishing 27%, close-ups 11%, single medium 10%, object inserts 9%,
maps 6%, dark spotlight 4%, text/infographic 2%. Picture what the narrator is saying right then,
literally. Use `motion` to vary zoom_in / zoom_out / pan_left / pan_right; `static` for maps with text.
`shots.json` stores the audio path relative to itself, so `assemble.py` finds it even without `--audio`.

**Bilingual (one image set, two voices):** make the Hindi script with the same number of spoken lines
in the same order as the English one (adapt line by line, same `## ` sections). Build and illustrate
the shot list for one language, then retime it to the other voice:
```bash
python scripts/shotlist.py out/voice_en.timings.json -o shots_en.json --like shots.json --chapters chapters_en.txt
```
Each shot keeps its image, prompt, motion and title, with new start/end. Auto section titles switch
to the new language; for hand-written titles add `"title_en"` / `"title_hi"` fields and pass
`--title-key title_en` to `assemble.py` (shots without that field fall back to `title`). If the line
counts differ, `--like` stops with an error: fix the script rather than stretching one timing
(`assemble.py` only holds/trims the LAST shot, so reusing one language's timings for the other drifts).

### 6. Images
- Tell the user the options (production-stack.md) and use what they have. Generate **without text**
  in the image; `assemble.py` adds the titles (Devanagari included) from the `title` field.
- Keep character cards fixed (style-bible.md section "Character consistency"). Save as
  `images/shot_001.png …` at 16:9, 1920x1080 or larger (PNG/JPG/WebP; smaller images work but look soft,
  and `assemble.py` warns). A still whose shape is far from the frame (e.g. portrait in 16:9) is shown
  whole on a blurred fill instead of being cropped; `--crop-all` forces cropping. A short `.mp4`
  (image-to-video) can replace any still for hero shots; it is looped/trimmed to the shot length.
- Before paying for images, do a dry run: `python scripts/placeholders.py --shots shots.json`.

### 7. Assemble
```bash
python scripts/assemble.py shots.json --audio out/voice_hi.mp3 --srt out/voice_hi.srt \
       --music music/bed.mp3 -o out/video_hi.mp4
python scripts/assemble.py shots.json --audio out/voice_hi.mp3 --srt out/voice_hi.srt \
       --vertical -o out/short_hi.mp4                     # 1080x1920, blurred fill (--vfill crop)
```
Useful flags: `--subs burn|soft|none`, `--fade 0.4`, `--zoom 0.12`, `--music-db -18`,
`--fontsdir fonts/ --title-font "Mukta ExtraBold"`, `--title-key title_en`, `--workdir out/work` (keeps a
clip cache, so re-running after replacing one image re-renders only that shot), `--no-fit` (do not hold/trim
the last shot to the audio). Timing is always driven by the narration: if the shot list ends early the
last shot is held; if it runs long, shots that start after the voice ends are dropped (both are logged).
A missing `--music`/`--srt` file is an error, so leave the flag out when there is no music.
For Shorts, cut a 45-60 s script section and make a separate `shots.json` for it.

Hindi text needs a font with Devanagari: check `fc-list :lang=hi family`. `assemble.py` picks the first
installed of Noto Sans Devanagari, Mukta, Hind, Nirmala UI, Lohit Devanagari, FreeSans/FreeSerif, and
warns if none exists; for a better look put Mukta/Hind `.ttf` files in `fonts/` and pass `--fontsdir fonts`.

### 8. QA checklist (do all before handing over)
- [ ] `ffprobe` the MP4: video + audio streams, duration = narration ±0.5 s, 1920x1080 (or 1080x1920), 30 fps.
- [ ] Extract 3+ frames (`ffmpeg -ss T -i out.mp4 -frames:v 1 f.png`) and look at them: mid-shot motion, a crossfade, a title, a caption; Devanagari has no dotted circles.
- [ ] Every shot image exists and matches what is said at that moment; no garbled text drawn by the image model.
- [ ] Same character looks the same across shots (hair, headwear, colours).
- [ ] Facts: dates checked, disputed points hedged, no copied script lines from any other channel.
- [ ] Loudness ≈ -14 LUFS (`ffmpeg -i out.mp4 -af ebur128 -f null -`); music never fights the voice.
- [ ] Music licence noted (YouTube Audio Library / Pixabay / attribution text in description).
- [ ] Deliver: MP4(s), SRT(s) for upload in both languages, chapter timestamps (`shotlist.py --chapters chapters.txt`; YouTube needs 3+ chapters starting at 0:00, each ≥10 s), title/description draft.
- [ ] Nothing in the delivery is a placeholder image or a `dryrun` silent track.

## Originality rules
Make original work in this general format. Do not copy another channel's name, logo, mascot,
intro, script lines or exact character designs; describe the style generically (as the master
block does) and give your channel its own palette tweak or recurring host character.
