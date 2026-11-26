#!/bin/bash
# Build each episode as soon as its narration and all its pictures exist. Safe to restart.
cd "$(dirname "$0")"
LOG=reports/build_loop.log; mkdir -p reports
for n in $(seq ${1:-3} ${2:-20}); do
  e=$(printf %02d $n)
  [ -f reports/ep$e.txt ] && continue
  want=$(python3 -c "import gen_images as g;print(len(g.prompts($n)))")
  until [ -f audio/ep$e.timing.json ] && [ -f audio/ep$e.mp3 ] && [ "$(ls images/ep$e/*.png 2>/dev/null | wc -l)" -ge "$want" ] \
        && [ -f images/ep$e/.reviewed ]; do sleep 30; done
  echo "$(date +%H:%M) building E$e" >> $LOG
  python3 -u produce.py build $n >> $LOG 2>&1
  git add -A images/ep$e audio reports brand/out/thumbnails captions >/dev/null 2>&1
  git commit -qm "Episode $n built and checked

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01YRsRDuewzUsAzkoCiXPerC" >/dev/null 2>&1
  git push -q >/dev/null 2>&1
  echo "$(date +%H:%M) done E$e" >> $LOG
done
