#!/bin/zsh
# Detached batch: every scene x every aspect, skips finished PNGs. CYCLES, OIDN.
export PATH=/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
D=/Users/artemis/.openclaw/workspace/projects/record-sconces/renders-final
B=/Applications/Blender.app/Contents/MacOS/Blender
SCENES=(${=1:-hero_chrome hero_brass hero_black set single7 macro living bar studio bedroom swap1 swap2 swap3 flatlay})
rm -f $D/logs/batch.done
for s in $SCENES; do for a in wide square tall; do
  out=$D/png/${s}_${a}.png
  [[ -f $out ]] && continue
  echo "START $s $a $(date +%T)" >> $D/logs/batch.log
  $B -b -P $D/src/final.py -- $s $a --samples ${SAMPLES:-448} > $D/logs/r_${s}_${a}.log 2>&1
  echo "END   $s $a $(date +%T) $( [[ -f $out ]] && echo ok || echo FAIL)" >> $D/logs/batch.log
done; done
touch $D/logs/batch.done
