#!/bin/zsh
export PATH=/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
D=/Users/artemis/.openclaw/workspace/projects/record-sconces/renders-final
while [[ ! -f $D/logs/post.done ]]; do sleep 20; done
$D/src/batch.sh "living bar studio"
python3 $D/src/build_index.py >> $D/logs/post.log 2>&1
touch $D/logs/rerun.done
