#!/bin/zsh
export PATH=/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:/opt/homebrew/bin
B=/Applications/Blender.app/Contents/MacOS/Blender
D=/Users/artemis/.openclaw/workspace/projects/record-sconces/render
MODE=$1; shift
$B -b -P $D/sconce_v2.py -- $MODE "$@" > $D/v2_${MODE}_$(date +%H%M%S).log 2>&1
