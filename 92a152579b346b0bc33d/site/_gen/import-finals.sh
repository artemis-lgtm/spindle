#!/bin/bash
# Re-crops and compresses the final renders (renders-final/png) into site/img.
# Safe to re-run as more finals land. Never writes outside site/. Requires sips + cwebp.
set -e
S="$(cd "$(dirname "$0")/.." && pwd)"
F="$S/../renders-final/png"
T="${TMPDIR:-/private/tmp}/spindle-import-$$"; mkdir -p "$T"
conv() { # src, outbase, widths...
  local src=$1 base=$2; shift 2
  for w in "$@"; do
    sips --resampleWidth $w "$src" --out "$T/$base-$w.png" >/dev/null
    cwebp -quiet -q 80 "$T/$base-$w.png" -o "$S/img/$base-$w.webp"
    sips -s format jpeg -s formatOptions 82 "$T/$base-$w.png" --out "$S/img/$base-$w.jpg" >/dev/null
  done
}
for f in chrome brass black; do
  # wide hero (1920x1080): crop to 1200x1080 with the sconce at ~70% so desktop copy sits left of it
  if [ -f "$F/hero_${f}_wide.png" ]; then
    sips -c 1080 1200 --cropOffset 0 230 "$F/hero_${f}_wide.png" --out "$T/w_$f.png" >/dev/null
    conv "$T/w_$f.png" "hero-$f" 1200 800; echo "hero-$f updated from finals"
  fi
  # square (1600x1600) -> product / mobile hero
  if [ -f "$F/hero_${f}_square.png" ]; then
    conv "$F/hero_${f}_square.png" "sq-$f" 1080 640; echo "sq-$f updated from finals"
  fi
done
# macro -> cap tiles, swap triptych -> swap frames, others as plain 16:9
[ -f "$F/macro_square.png" ] && conv "$F/macro_square.png" "macro" 1080 640 && echo "macro added"
for n in swap1 swap2 swap3 flatlay living bar bedroom studio set install; do
  [ -f "$F/${n}_wide.png" ] && conv "$F/${n}_wide.png" "$n" 1600 900 && echo "$n added"
  [ -f "$F/${n}_square.png" ] && conv "$F/${n}_square.png" "$n-sq" 1080 640 && echo "$n-sq added"
done
# OG image 1200x630 from the chrome wide final
if [ -f "$F/hero_chrome_wide.png" ]; then
  sips -c 630 1200 --cropOffset 225 360 "$F/hero_chrome_wide.png" --out "$T/og.png" >/dev/null
  sips -s format jpeg -s formatOptions 85 "$T/og.png" --out "$S/img/og.jpg" >/dev/null; echo "og updated"
fi
rm -rf "$T"
