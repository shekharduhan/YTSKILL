# One More Episode — 60-second reel, made 100% free with code

Same idea as `../devil-or-angel`, flipped: it's 1 A.M., his alarm is at 6, and **she** keeps
whispering "one more episode" in his ear. *Are you the devil? That's what the devil does — speaks
in your ear and talks you into things you'll regret.* … *Don't be a devil. Be an angel.*

Written with the `/yt-script` skill. Five hooks were scored with `skills/yt-script/hookscore.py`;
the winner (60, WORKABLE) was:

> If your partner whispers "one more episode" at 1am, you lose 6 hours of sleep. Here's why

It's shortened for the on-screen header: *She whispers "one more episode" at 1 A.M... 6 A.M. alarm. Devil or angel?*

Output: `output/one-more-episode-reel.mp4` — 1080×1920, 30 fps, exactly 60 s.

## Everything is free

Piper TTS voices (offline, open source), synthesised sound effects and music, Pillow animation,
ffmpeg. No API keys, no paid services, no stock assets.

## Build

```bash
./make.sh
```

Edit the dialogue in `lines.json` (`W` = wife, `H` = husband).
