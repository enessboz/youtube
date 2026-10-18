#!/usr/bin/env python3
"""footage: ücretsiz stok videoları (Pexels, Pixabay) arar ve lisans bilgisiyle indirir.

Anahtarlar ortam değişkeninde: PEXELS_API_KEY, PIXABAY_API_KEY (ikisi de ücretsiz, biri yetebilir).

Kullanım:
  python3 footage.py search "blacksmith forging" [--n 12] [--min-duration 5]
  python3 footage.py download pexels:1234567 <hedef-klasör>      # assets/footage/
Çıktı (indirme): <klasör>/<sağlayıcı>-<id>.mp4 ve .json (kaynak URL, yazar, lisans, tarih).

Lisans (kurulumdan önce güncel metni doğrula):
  Pexels: ticari kullanım serbest, atıf zorunlu değil; videoyu değiştirmeden satmak ve kişileri/markaları
  yanıltıcı kullanmak yasak. Pixabay: ticari kullanım serbest, atıf zorunlu değil; aynen yeniden satış yasak.
  Her klip için kaynak sayfası kaydedilir; videoda tanınabilir kişi/marka varsa ayrıca değerlendir.
"""
import argparse
import datetime as dt
import json
import os
import sys
import urllib.parse
import urllib.request

UA = "yt-content-system/0.1"
LICENSE = {
    "pexels": "Pexels License (https://www.pexels.com/license/)",
    "pixabay": "Pixabay Content License (https://pixabay.com/service/license-summary/)",
}


def http_json(url, headers=None):
    req = urllib.request.Request(url, headers={"User-Agent": UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.load(r)


def pick_pexels_file(files, max_h=1080):
    """≤1080p mp4'ler arasında en yükseği."""
    ok = [f for f in files if f.get("file_type") == "video/mp4" and f.get("height") and f["height"] <= max_h]
    return max(ok, key=lambda f: f["height"], default=None)


def parse_pexels(data):
    out = []
    for v in data.get("videos", []):
        f = pick_pexels_file(v.get("video_files", []))
        if not f:
            continue
        out.append({
            "ref": f"pexels:{v['id']}", "provider": "pexels", "id": v["id"], "duration": v.get("duration", 0),
            "page": v.get("url"), "author": (v.get("user") or {}).get("name"),
            "width": f["width"], "height": f["height"], "file": f["link"], "thumb": v.get("image"),
        })
    return out


def parse_pixabay(data):
    out = []
    for v in data.get("hits", []):
        vs = v.get("videos", {})
        f = next((vs[k] for k in ("large", "medium", "small") if vs.get(k, {}).get("url") and vs[k].get("height", 0) <= 1080), None)
        if not f:
            continue
        out.append({
            "ref": f"pixabay:{v['id']}", "provider": "pixabay", "id": v["id"], "duration": v.get("duration", 0),
            "page": v.get("pageURL"), "author": v.get("user"), "width": f["width"], "height": f["height"],
            "file": f["url"], "thumb": (v.get("userImageURL") or ""),
        })
    return out


def search(query, n=12, min_duration=5):
    res = []
    key = os.environ.get("PEXELS_API_KEY")
    if key:
        q = urllib.parse.urlencode({"query": query, "per_page": n, "orientation": "landscape"})
        res += parse_pexels(http_json(f"https://api.pexels.com/videos/search?{q}", {"Authorization": key}))
    key = os.environ.get("PIXABAY_API_KEY")
    if key:
        q = urllib.parse.urlencode({"key": key, "q": query, "per_page": max(3, n), "video_type": "film"})
        res += parse_pixabay(http_json(f"https://pixabay.com/api/videos/?{q}"))
    if not res and not (os.environ.get("PEXELS_API_KEY") or os.environ.get("PIXABAY_API_KEY")):
        raise SystemExit("PEXELS_API_KEY veya PIXABAY_API_KEY tanımlı değil.")
    return [r for r in res if r["duration"] >= min_duration]


def download(ref, dest_dir):
    provider, vid = ref.split(":", 1)
    found = None
    # arama sonucunu yeniden bul: kimlik ile doğrudan sorgu
    if provider == "pexels":
        data = http_json(f"https://api.pexels.com/videos/videos/{vid}", {"Authorization": os.environ["PEXELS_API_KEY"]})
        found = parse_pexels({"videos": [data]})
    elif provider == "pixabay":
        data = http_json(f"https://pixabay.com/api/videos/?key={os.environ['PIXABAY_API_KEY']}&id={vid}")
        found = parse_pixabay(data)
    if not found:
        raise SystemExit(f"bulunamadı: {ref}")
    item = found[0]
    os.makedirs(dest_dir, exist_ok=True)
    path = os.path.join(dest_dir, f"{provider}-{vid}.mp4")
    req = urllib.request.Request(item["file"], headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as r, open(path, "wb") as f:
        f.write(r.read())
    meta = {**item, "license": LICENSE[provider], "downloaded": dt.date.today().isoformat()}
    with open(path[:-4] + ".json", "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)
    return path, meta


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search")
    s.add_argument("query")
    s.add_argument("--n", type=int, default=12)
    s.add_argument("--min-duration", type=int, default=5)
    d = sub.add_parser("download")
    d.add_argument("ref")
    d.add_argument("dest")
    a = ap.parse_args()
    if a.cmd == "search":
        for r in search(a.query, a.n, a.min_duration):
            print(f"{r['ref']:<18} {r['duration']:>3}s {r['width']}x{r['height']}  {r['author']}  {r['page']}")
    else:
        path, meta = download(a.ref, a.dest)
        print(path, meta["license"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
