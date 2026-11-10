#!/bin/zsh
# Runs after batch.sh: install cutaways, video passes + loop, triptych, index.
export PATH=/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
D=/Users/artemis/.openclaw/workspace/projects/record-sconces/renders-final
B=/Applications/Blender.app/Contents/MacOS/Blender
L=$D/logs/post.log
while [[ ! -f $D/logs/batch.done ]]; do sleep 20; done
for a in wide square tall; do
  [[ -f $D/png/install_$a.png ]] && continue
  echo "START install $a $(date +%T)" >> $L
  $B -b -P $D/src/install_v3.py -- cutaway --aspect $a --samples 448 > $D/logs/r_install_$a.log 2>&1
  echo "END   install $a $(date +%T) $( [[ -f $D/png/install_$a.png ]] && echo ok || echo FAIL)" >> $L
done
mkdir -p $D/video
for p in ambient halo; do
  [[ -f $D/video/pass_$p.exr ]] && continue
  echo "START pass $p $(date +%T)" >> $L
  $B -b -P $D/src/final.py -- darkroom tall --samples 768 --pass $p --exr --out $D/video/pass_$p.exr > $D/logs/r_pass_$p.log 2>&1
  echo "END   pass $p $(date +%T) $( [[ -f $D/video/pass_$p.exr ]] && echo ok || echo FAIL)" >> $L
done
echo "START video $(date +%T)" >> $L
$B -b -P $D/src/video_comp.py > $D/logs/video.log 2>&1
echo "END   video $(date +%T) $( [[ -f $D/video/halo_fade_loop_1080x1920.mp4 ]] && echo ok || echo FAIL)" >> $L
python3 - <<'PY' >> $L 2>&1
from PIL import Image, ImageDraw, ImageFont
D="/Users/artemis/.openclaw/workspace/projects/record-sconces/renders-final/png/"
ims=[Image.open(D+f"swap{i}_square.png").convert("RGB").resize((1200,1200)) for i in (1,2,3)]
G=Image.new("RGB",(3*1200+4*40,1200+160),(22,19,15)); d=ImageDraw.Draw(G)
f=ImageFont.truetype("/System/Library/Fonts/Supplemental/Futura.ttc",54,index=1)
for i,(im,t) in enumerate(zip(ims,["1  Unscrew the dome","2  Lift the record off","3  Drop on the next one"])):
    G.paste(im,(40+i*1240,40)); d.text((40+i*1240,1265),t,font=f,fill=(239,231,218))
G.save(D+"swap_triptych.png"); print("triptych ok")
PY
python3 $D/src/build_index.py >> $L 2>&1
touch $D/logs/post.done
