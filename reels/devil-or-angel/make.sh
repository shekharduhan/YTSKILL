#!/usr/bin/env bash
# Build the 60s "Devil or Angel" reel. 100% free: Piper TTS + Python + ffmpeg. No API keys.
set -euo pipefail
cd "$(dirname "$0")"
pip install -q kokoro-onnx soundfile numpy pillow
python3 voices.py     # dialogue  -> audio/00.wav .. 15.wav
python3 sfx.py        # sting + chime
python3 music.py      # background loop
python3 render.py     # 1080x1920 @30fps animation -> video_only.mp4 (+ timeline.json)
python3 mix.py ../../output/devil-or-angel-reel.mp4
