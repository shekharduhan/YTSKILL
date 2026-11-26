#!/bin/bash
# Build episodes in the given order; a lock file stops two loops building the same episode.
cd "$(dirname "$0")"
LOG=reports/build_loop.log; mkdir -p reports
for n in "$@"; do
  e=$(printf %02d $n)
  [ -f reports/ep$e.txt ] && continue
  mkdir reports/ep$e.lock 2>/dev/null || continue
  echo "$(date +%H:%M) building E$e" >> $LOG
  python3 -u produce.py build $n >> $LOG 2>&1
  echo "$(date +%H:%M) done E$e" >> $LOG
  rmdir reports/ep$e.lock
done
