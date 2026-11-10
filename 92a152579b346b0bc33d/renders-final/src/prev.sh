#!/bin/zsh
# usage: prev.sh scene aspect [extra args]  -> preview/scene_aspect.png
export PATH=/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
D=/Users/artemis/.openclaw/workspace/projects/record-sconces/renders-final
S=$1; A=$2; shift 2
/Applications/Blender.app/Contents/MacOS/Blender -b -P $D/src/final.py -- $S $A --preview "$@" > $D/logs/prev_${S}_${A}.log 2>&1
grep -E "Error|Traceback|WROTE" -A3 $D/logs/prev_${S}_${A}.log | head -20
