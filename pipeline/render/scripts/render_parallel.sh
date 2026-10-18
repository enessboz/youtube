#!/bin/bash
# Kareleri N parçaya bölüp paralel render eder, ffmpeg ile birleştirir.
# Kullanım: scripts/render_parallel.sh <kanal> <video> <çıktı.mp4> [parça=4]
set -e
CH=$1; VID=$2; OUT=$3; N=${4:-4}
HERE=$(cd "$(dirname "$0")" && pwd)
SC=$HERE/../../../channels/$CH/videos/$VID/scenes.render.json
TOTAL=$(python3 -c "import json,sys;d=json.load(open('$SC'));f=d.get('fps',30);print(sum(max(1,round(s['duration_s']*f)) for s in d['scenes']))")
STEP=$(( (TOTAL + N - 1) / N ))
TMP=$(mktemp -d)
for i in $(seq 0 $((N-1))); do
  a=$((i*STEP)); b=$(( (i+1)*STEP-1 )); [ $b -ge $TOTAL ] && b=$((TOTAL-1))
  [ $a -gt $b ] && continue
  node "$HERE/render.mjs" "$CH" "$VID" --frames $a-$b --out "$TMP/part$i.mp4" > "$TMP/log$i.txt" 2>&1 &
done
wait
for f in "$TMP"/part*.mp4; do echo "file '$f'"; done | sort > "$TMP/list.txt"
ffmpeg -v error -y -f concat -safe 0 -i "$TMP/list.txt" -c copy "$OUT"
echo "tamam: $OUT ($TOTAL kare)"
