#!/bin/bash
# Single builder: wait until no build is running, then build 18..46 one at a time (never in parallel: parallel builds run out of memory).
cd "$(dirname "$0")"
while pgrep -f "produce.py build" >/dev/null; do sleep 30; done
rmdir reports/ep*.lock 2>/dev/null
exec ./build_queue.sh 18 46
