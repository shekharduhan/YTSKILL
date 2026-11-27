#!/bin/bash
# Build every episode in the range as soon as its narration, all its pictures and the picture review are done.
cd "$(dirname "$0")"
LOG=reports/build_loop.log
while true; do
  left=0
  for n in $(seq $1 $2); do
    e=$(printf %02d $n)
    [ -f reports/ep$e.txt ] && continue
    left=1
    want=$(grep -c "^| [0-9]" ep$e-image-prompts.md 2>/dev/null)
    have=$(ls images/ep$e/*.png 2>/dev/null | wc -l)
    [ -f audio/ep$e.mp3 ] && [ -f audio/ep$e.timing.json ] && [ -f images/ep$e/.reviewed ] && [ "$have" -ge "$want" ] || continue
    mkdir reports/ep$e.lock 2>/dev/null || continue
    echo "$(date +%H:%M) building E$e" >> $LOG
    python3 -u produce.py build $n >> $LOG 2>&1
    echo "$(date +%H:%M) done E$e" >> $LOG
    rmdir reports/ep$e.lock
  done
  [ $left = 0 ] && exit 0
  sleep 120
done
