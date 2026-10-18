#!/usr/bin/env python3
"""handles: kanalları derin ölçer (son ~150 yükleme; kanal başına ~8 birim).

Girdi biçimleri (karışık verilebilir):
  @handle         -> channels.list forHandle (1 birim)
  id:UCxxxx       -> channels.list id (1 birim)
  "Kanal adı"     -> search.list type=channel (100 birim) -- son çare

Kullanım: python3 handles.py @ornek id:UCxxxx "Kanal Adı" --out out
Çıktı: out/handles.md (tablo) ve ekrana özet.
"""
import argparse
import datetime as dt
import os
import statistics
import sys

import scout

scout.COST["playlistItems"] = 1
MAX_UPLOADS = 150


def resolve(client, arg):
    part = "snippet,statistics,contentDetails"
    if arg.startswith("@"):
        items = client.get("channels", {"part": part, "forHandle": arg}).get("items", [])
    elif arg.startswith("id:"):
        items = client.get("channels", {"part": part, "id": arg[3:]}).get("items", [])
    else:
        res = client.get("search", {"part": "snippet", "q": arg, "type": "channel", "maxResults": 3})
        if not res.get("items"):
            return None
        cid = res["items"][0]["snippet"]["channelId"]
        items = client.get("channels", {"part": part, "id": cid}).get("items", [])
    return items[0] if items else None


def uploads(client, playlist):
    ids, token = [], None
    while len(ids) < MAX_UPLOADS:
        params = {"part": "contentDetails", "playlistId": playlist, "maxResults": 50}
        if token:
            params["pageToken"] = token
        res = client.get("playlistItems", params)
        ids += [i["contentDetails"]["videoId"] for i in res.get("items", [])]
        token = res.get("nextPageToken")
        if not token:
            break
    return ids[:MAX_UPLOADS]


def measure(client, ch, now):
    ids = uploads(client, ch["contentDetails"]["relatedPlaylists"]["uploads"])
    vids = []
    for part in scout.chunks(ids, 50):
        vids += client.get("videos", {"part": "snippet,statistics,contentDetails", "id": ",".join(part)}).get("items", [])
    longs = []
    for v in vids:
        d = scout.parse_duration(v["contentDetails"].get("duration"))
        if d >= scout.MIN_DURATION_S:
            longs.append({"id": v["id"], "title": v["snippet"]["title"], "dur": d,
                          "views": int(v["statistics"].get("viewCount", 0)),
                          "ts": scout.parse_ts(v["snippet"]["publishedAt"])})
    if not longs:
        return None
    longs.sort(key=lambda v: v["ts"], reverse=True)
    cs = ch["statistics"]
    recent = [v for v in longs if (now - v["ts"]).days <= 90]
    # Çok yeni videolar henüz izlenme biriktirmedi; medyanı 14 günden eski videolardan al.
    mature = [v for v in longs if (now - v["ts"]).days >= 14] or longs
    views = [v["views"] for v in mature]
    return {
        "channel": ch["snippet"]["title"], "id": ch["id"],
        "subs": None if cs.get("hiddenSubscriberCount") else int(cs.get("subscriberCount", 0)),
        "age_mo": (now - scout.parse_ts(ch["snippet"]["publishedAt"])).days // 30,
        "n_long": len(longs), "per_week_90d": round(len(recent) / (90 / 7), 1),
        "days_since_last": (now - longs[0]["ts"]).days,
        "median": int(statistics.median(views)),
        "hit50": round(sum(1 for x in views if x >= 50_000) / len(views), 2),
        "hit100": round(sum(1 for x in views if x >= 100_000) / len(views), 2),
        "best": sorted(mature, key=lambda v: v["views"], reverse=True)[:3],
        "dur_min": round(statistics.median(v["dur"] for v in longs) / 60),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("channels", nargs="+")
    ap.add_argument("--out", default="out")
    args = ap.parse_args()
    key = os.environ.get("YOUTUBE_API_KEY")
    if not key:
        print("YOUTUBE_API_KEY tanımlı değil.", file=sys.stderr)
        return 2
    client = scout.Client(key, os.path.join(args.out, "cache"))
    now = dt.datetime.now(dt.timezone.utc)
    lines = ["| Kanal | Abone | Yaş (ay) | Video/hf (90g) | Son yüklemeden gün | Medyan | ≥50K | ≥100K | n | Süre dk | En iyi 3 |",
             "|---|---|---|---|---|---|---|---|---|---|---|"]
    for a in args.channels:
        try:
            ch = resolve(client, a)
            m = measure(client, ch, now) if ch else None
        except (scout.QuotaError, RuntimeError) as e:
            print(f"{a}: {e}")
            continue
        if not m:
            print(f"{a}: bulunamadı / uzun video yok")
            continue
        best = "; ".join(f"{v['views']:,} {v['title'][:40]}" for v in m["best"])
        lines.append(f"| [{m['channel']}](https://youtube.com/channel/{m['id']}) | {m['subs']} | {m['age_mo']} | "
                     f"{m['per_week_90d']} | {m['days_since_last']} | {m['median']:,} | {m['hit50']:.0%} | {m['hit100']:.0%} | "
                     f"{m['n_long']} | {m['dur_min']} | {best} |")
        print(lines[-1])
    os.makedirs(args.out, exist_ok=True)
    with open(os.path.join(args.out, "handles.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"kota: {client.spent}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
