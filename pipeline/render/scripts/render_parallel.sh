#!/bin/bash
# Kareleri N parçaya bölüp paralel render eder, ffmpeg ile birleştirir. Biten parçalar atlanır (devam edilebilir).
# Kullanım: scripts/render_parallel.sh <kanal> <video> <çıktı.mp4> [parça=3] (RENDER_PARALLEL=2 eşzamanlı)
# Not: bellek için RENDER_CONCURRENCY (varsayılan 2) x parça sayısı sınırlı tutulmalı (SIGKILL = bellek).
CH=$1; VID=$2; OUT=$3; N=${4:-3}
export RENDER_CONCURRENCY=${RENDER_CONCURRENCY:-2}
HERE=$(cd "$(dirname "$0")" && pwd)
SC=$HERE/../../../channels/$CH/videos/$VID/scenes.render.json
TOTAL=$(python3 -c "import json;d=json.load(open('$SC'));f=d.get('fps',30);print(sum(max(1,round(s['duration_s']*f)) for s in d['scenes']))")
STEP=$(( (TOTAL + N - 1) / N ))
TMP=$HERE/../../../.cache/rp-$VID-$TOTAL
mkdir -p "$TMP"
PAR=${RENDER_PARALLEL:-2}
run_part() {
  i=$1; a=$((i*STEP)); b=$(( (i+1)*STEP-1 )); [ $b -ge $TOTAL ] && b=$((TOTAL-1))
  [ $a -gt $b ] && return 0
  [ -s "$TMP/part$i.ok" ] && return 0
  node "$HERE/render.mjs" "$CH" "$VID" --frames $a-$b --out "$TMP/part$i.mp4" > "$TMP/log$i.txt" 2>&1 && echo ok > "$TMP/part$i.ok"
}
export -f run_part; export HERE CH VID STEP TOTAL TMP
seq 0 $((N-1)) | xargs -P $PAR -I{} bash -c 'run_part {}'
for i in $(seq 0 $((N-1))); do
  [ -s "$TMP/part$i.ok" ] || { echo "HATA: parça $i bitmedi (bkz. $TMP/log$i.txt)"; exit 1; }
done
for i in $(seq 0 $((N-1))); do echo "file '$TMP/part$i.mp4'"; done > "$TMP/list.txt"
ffmpeg -v error -y -f concat -safe 0 -i "$TMP/list.txt" -c copy "$OUT" && echo "tamam: $OUT ($TOTAL kare)"
