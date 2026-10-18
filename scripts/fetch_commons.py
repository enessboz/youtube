#!/usr/bin/env python3
"""fetch_commons: Wikimedia Commons dosyasını indirir ve lisansını API'den okur.

Kullanım: python3 scripts/fetch_commons.py "<Dosya adı>" <hedef.jpg> [--width 960]
Lisans PD/CC değilse indirmez. Çıktı: lisans, yazar ve atıf bilgisi (JSON, hedef.json olarak da kaydedilir).
"""
import argparse
import json
import sys
import urllib.parse
import urllib.request

WIDTH = 960  # Commons'un izin verdiği standart küçük resim boyutlarından (960, 1280, 1920)
UA = "yt-content-system/0.1 (research tool; contact: repo owner)"
API = "https://commons.wikimedia.org/w/api.php"
OK_PREFIX = ("public domain", "cc0", "pd", "cc by", "cc-by")


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def info(title):
    q = urllib.parse.urlencode({
        "action": "query", "format": "json", "prop": "imageinfo", "titles": "File:" + title,
        "iiprop": "extmetadata|url", "iiurlwidth": WIDTH, "iiextmetadatafilter": "LicenseShortName|Artist|Credit|AttributionRequired|UsageTerms",
    })
    data = json.loads(get(f"{API}?{q}"))
    page = next(iter(data["query"]["pages"].values()))
    ii = page["imageinfo"][0]
    md = {k: v["value"] for k, v in ii["extmetadata"].items()}
    return ii.get("thumburl") or ii["url"], md


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("title")
    ap.add_argument("dest")
    ap.add_argument("--width", type=int, default=960, help="960, 1280 veya 1920 (Commons standart boyutları)")
    a = ap.parse_args()
    global WIDTH
    WIDTH = a.width
    url, md = info(a.title)
    lic = md.get("LicenseShortName", "").lower()
    out = {"file": a.title, "license": md.get("LicenseShortName"), "artist": md.get("Artist"), "credit": md.get("Credit"),
           "attribution_required": md.get("AttributionRequired"), "source": "https://commons.wikimedia.org/wiki/File:" + urllib.parse.quote(a.title.replace(" ", "_"))}
    if not lic.startswith(OK_PREFIX):
        print(json.dumps(out, ensure_ascii=False, indent=1))
        print("lisans uygun değil veya okunamadı: indirilmedi", file=sys.stderr)
        return 2
    blob = get(url)
    with open(a.dest, "wb") as f:
        f.write(blob)
    with open(a.dest + ".json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
