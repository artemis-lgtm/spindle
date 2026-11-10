#!/bin/bash
export PATH=/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
cd /Users/artemis/.openclaw/workspace/projects/record-sconces/render
B=/Applications/Blender.app/Contents/MacOS/Blender
rm -f render_all.done
for job in "hero --cap chrome" "hero --cap brass" "hero --cap black" "exploded --cap chrome"; do
  set -- $job
  echo "START $job $(date)" >> render_all.log
  $B -b -P sconce.py -- $1 --cap $3 --res 1920x1080 --samples 1024 >> render_all.log 2>&1
  echo "END $job $(date)" >> render_all.log
done
touch render_all.done
