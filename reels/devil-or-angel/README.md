# Devil or Angel? — 60-second reel, made 100% free with code

A husband keeps whispering in his wife's ear ("one more slice of cake…"). She asks:
*are you the devil? That's what the devil does — speaks in your ear and manipulates you.
Which side are you on, good or bad?* … *Don't be a devil. Be an angel.*

Output: `output/devil-or-angel-reel.mp4` — 1080×1920, 30 fps, exactly 60 s.

## Everything is free

| part | how |
| --- | --- |
| voices | [Piper TTS](https://github.com/rhasspy/piper) — offline, open source (Ryan + Amy voices) |
| whisper effect | numpy breath-noise filter in `voices.py` |
| sound effects | synthesised in `sfx.py` (organ sting, harp chime) |
| music | synthesised pizzicato loop in `music.py` |
| animation | drawn frame by frame with Pillow in `render.py` |
| assembly | ffmpeg (`mix.py`) |

No API keys, no paid services, no stock assets.

## Build

```bash
./make.sh
```

Needs Python 3 and ffmpeg. First run downloads the two Piper voice models (~180 MB) to `~/.cache/piper-voices`.

## Change it

- Edit the dialogue in `lines.json` (`H` = husband, `W` = wife, third field = delivery style).
- Expressions / horns / halo timing are keyed by line number in `render.py` (`WHISPER`, `H_EXPR`, `W_EXPR`).
