#!/usr/bin/env python3
"""video_maker: sahne listesinden (anlatım + Pexels arama sorgusu) mp4 üretir.

Hat: her sahne için TTS (gTTS) -> Pexels'ten stok klip -> ffmpeg ile ses süresine
kırp/döngüle, 16:9'a kırp -> birleştir -> altyazı (drawtext) -> out/<slug>.mp4

Kullanım:
  export PEXELS_API_KEY=...
  python3 make_video.py script_example.json --out out
  python3 make_video.py script_example.json --out out --no-subs --width 1280 --height 720

Script formatı: {"title", "lang", "scenes": [{"narration", "query"}]}
Pexels klipleri ve ses dosyaları out/cache altında saklanır; tekrar çalıştırmak ağ harcamaz.
Pexels lisansı ticari kullanıma izin verir; atıf zorunlu değil ama credits.txt yazılır.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import textwrap
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (video_maker)"  # Pexels varsayılan Python UA'yı 403 ile reddeder
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"komut başarısız: {' '.join(cmd[:4])}...\n{r.stderr[-800:]}")
    return r.stdout


def duration(path):
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                      "-of", "default=nw=1:nk=1", path]))


def tts(text, lang, cache):
    path = os.path.join(cache, hashlib.sha1(f"{lang}|{text}".encode()).hexdigest() + ".mp3")
    if not os.path.exists(path):
        from gtts import gTTS
        gTTS(text, lang=lang).save(path)
    return path


def pexels_clip(query, key, cache, min_s, used):
    """En uygun yatay HD klibi bul, indir. Aynı klibi iki sahnede kullanma."""
    qfile = os.path.join(cache, "q_" + hashlib.sha1(query.encode()).hexdigest() + ".json")
    if os.path.exists(qfile):
        data = json.load(open(qfile))
    else:
        url = "https://api.pexels.com/videos/search?" + urllib.parse.urlencode(
            {"query": query, "orientation": "landscape", "size": "medium", "per_page": 15})
        req = urllib.request.Request(url, headers={"Authorization": key, "User-Agent": UA})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.load(r)
        json.dump(data, open(qfile, "w"))
    vids = [v for v in data.get("videos", []) if v["id"] not in used]
    # önce yeterince uzun olanlar
    vids.sort(key=lambda v: (v["duration"] < min_s, -v["duration"]))
    for v in vids:
        files = [f for f in v["video_files"] if f.get("file_type") == "video/mp4"
                 and f.get("width") and 1280 <= f["width"] <= 1920]
        if not files:
            continue
        f = min(files, key=lambda f: abs(f["width"] - 1920))
        path = os.path.join(cache, f"pexels_{v['id']}.mp4")
        if not os.path.exists(path):
            req = urllib.request.Request(f["link"], headers={"Authorization": key, "User-Agent": UA})
            with urllib.request.urlopen(req, timeout=120) as r, open(path, "wb") as out:
                out.write(r.read())
        used.add(v["id"])
        return path, {"id": v["id"], "url": v["url"], "user": v["user"]["name"]}
    sys.exit(f"Pexels'te klip bulunamadı: {query!r}")


def esc(s):
    return s.replace("\\", "\\\\").replace(":", "\\:").replace("'", "’").replace("%", "\\%")


def render_scene(clip, audio, text, idx, w, h, subs, tmp):
    dur = duration(audio) + 0.35  # cümleler arası kısa nefes
    vf = (f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},"
          f"fps=30,format=yuv420p")
    if subs:
        lines = textwrap.wrap(text, 48)[:3]
        tf = os.path.join(tmp, f"sub{idx}.txt")
        open(tf, "w", encoding="utf-8").write("\n".join(lines))
        vf += (f",drawtext=fontfile={FONT}:textfile={tf}:fontsize={h // 22}:fontcolor=white:"
               f"borderw=3:bordercolor=black:line_spacing=8:x=(w-text_w)/2:y=h-text_h-{h // 14}")
    out = os.path.join(tmp, f"scene{idx:02d}.mp4")
    run(["ffmpeg", "-y", "-v", "error", "-stream_loop", "-1", "-i", clip, "-i", audio,
         "-t", f"{dur:.2f}", "-vf", vf, "-af", "apad", "-map", "0:v", "-map", "1:a",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "22", "-c:a", "aac", "-b:a", "160k",
         "-ar", "44100", "-ac", "2", out])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("--out", default="out")
    ap.add_argument("--width", type=int, default=1920)
    ap.add_argument("--height", type=int, default=1080)
    ap.add_argument("--no-subs", action="store_true")
    a = ap.parse_args()

    key = os.environ.get("PEXELS_API_KEY") or sys.exit("PEXELS_API_KEY tanımlı değil")
    spec = json.load(open(a.script, encoding="utf-8"))
    slug = re.sub(r"[^a-z0-9]+", "-", spec["title"].lower().replace("ı", "i")).strip("-") or "video"
    cache = os.path.join(a.out, "cache")
    tmp = os.path.join(a.out, "tmp_" + slug)
    os.makedirs(cache, exist_ok=True)
    os.makedirs(tmp, exist_ok=True)

    used, credits, scenes = set(), [], []
    for i, sc in enumerate(spec["scenes"]):
        audio = tts(sc["narration"], spec.get("lang", "tr"), cache)
        clip, meta = pexels_clip(sc["query"], key, cache, duration(audio) + 0.35, used)
        credits.append(f"sahne {i + 1}: {meta['url']} ({meta['user']})")
        scenes.append(render_scene(clip, audio, sc["narration"], i, a.width, a.height,
                                   not a.no_subs, tmp))
        print(f"sahne {i + 1}/{len(spec['scenes'])} tamam", file=sys.stderr)

    lst = os.path.join(tmp, "list.txt")
    open(lst, "w").write("".join(f"file '{os.path.abspath(s)}'\n" for s in scenes))
    final = os.path.join(a.out, slug + ".mp4")
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst,
         "-c", "copy", "-movflags", "+faststart", final])
    open(os.path.join(a.out, slug + ".credits.txt"), "w").write(
        spec["title"] + "\nVideo klipleri: Pexels (pexels.com)\n" + "\n".join(credits) + "\n")
    print(f"{final}  ({duration(final):.1f} sn)")


if __name__ == "__main__":
    main()
