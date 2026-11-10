#!/bin/zsh
# Render every SVG in brand/logo and brand/packaging to PNG with headless Chrome,
# via an HTML wrapper so the SVG scales to the window (Chrome otherwise renders it at
# intrinsic pt size and crops). Logos at 2 px/pt, packaging at 40 px/in (big sheets)
# or 150 px/in (cards and stickers).
CH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
B="$(cd "$(dirname "$0")/.." && pwd)"
TMP="${TMPDIR:-/tmp}/sconce-preview-$$"
mkdir -p "$B/preview" "$TMP"
for f in "$B"/logo/*.svg "$B"/packaging/*.svg; do
  n=$(basename "$f" .svg)
  dims=$(python3 - "$f" <<'PY'
import re,sys
t=open(sys.argv[1]).read(2000)
w=re.search(r'width="([\d.]+)(pt|in)"',t); h=re.search(r'height="([\d.]+)(pt|in)"',t)
wv,u=float(w.group(1)),w.group(2); hv=float(h.group(1))
if u=='pt': s=2.0
else: s=40.0 if max(wv,hv)>12 else 150.0
print(int(wv*s), int(hv*s))
PY
)
  PW=${dims%% *}
  PH=${dims##* }
  cat > "$TMP/$n.html" <<EOF
<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;padding:0;background:transparent}img{display:block;width:${PW}px;height:${PH}px}</style></head><body><img src="file://$f"></body></html>
EOF
  "$CH" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 --screenshot="$B/preview/$n.png" --window-size=${PW},${PH} --default-background-color=00000000 "file://$TMP/$n.html" >/dev/null 2>&1
done
rm -rf "$TMP"
ls "$B/preview" | wc -l
