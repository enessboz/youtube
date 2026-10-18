#!/bin/bash
# Render için klipleri hafif seek'e uygun biçime çevirir (1080p, 30 fps, sık anahtar kare).
# Kullanım: scripts/prep_footage.sh <kanal> <video>
V=channels/$1/videos/$2/assets
mkdir -p $V/footage-r
for f in $V/footage/*.mp4; do
  b=$(basename $f); [ -s $V/footage-r/$b ] && continue
  ffmpeg -v error -y -i $f -an -vf "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30" \
    -c:v libx264 -preset veryfast -crf 19 -g 8 -keyint_min 8 -pix_fmt yuv420p $V/footage-r/$b &
  while [ $(jobs -r | wc -l) -ge 3 ]; do sleep 1; done
done; wait
