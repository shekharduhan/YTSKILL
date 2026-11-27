#!/bin/bash
# Restartable production: narration (cached per line, never paid twice) and pictures (existing ones skipped).
cd "$(dirname "$0")"
python3 -u produce.py audio $(seq 22 84) >> reports/audio_run.log 2>&1 &
python3 -u produce.py images $(seq 26 46) >> reports/images_run.log 2>&1 &
wait
