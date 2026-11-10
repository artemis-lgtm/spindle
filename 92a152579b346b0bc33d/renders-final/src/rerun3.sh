#!/bin/zsh
export PATH=/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
D=/Users/artemis/.openclaw/workspace/projects/record-sconces/renders-final
B=/Applications/Blender.app/Contents/MacOS/Blender
while [[ ! -f $D/logs/rerun2.done ]]; do sleep 20; done
for a in wide square tall; do
  mv $D/png/install_$a.png $D/png/_superseded/ 2>/dev/null
  echo "START install $a $(date +%T)" >> $D/logs/post.log
  $B -b -P $D/src/install_v3.py -- cutaway --aspect $a --samples 448 > $D/logs/r_install_$a.log 2>&1
  echo "END   install $a $(date +%T)" >> $D/logs/post.log
done
python3 $D/src/build_index.py >> $D/logs/post.log 2>&1
touch $D/logs/rerun3.done
