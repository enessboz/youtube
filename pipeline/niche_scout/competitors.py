#!/usr/bin/env python3
"""competitors: hedef kanal başına rakip kanalları bulur ve son yüklemelerinden ölçer.

Akış (hedef başına): alt konu sorguları -> search.list -> kanallar -> her kanalın
yükleme listesi (playlistItems, 1 birim) -> videos.list -> kanal metrikleri.

Metrikler: abone, kanal yaşı, son 90 günde haftalık yükleme, uzun videoların medyan
ve en iyi izlenmesi, medyan izlenme / abone oranı (>1 ise abone tabanının ötesine ulaşıyor).

Kota: her sorgu 100 birim, kanal başına ~2 birim. Önbellek scout.py ile aynı (out/cache).

Kullanım:
  python3 competitors.py --targets targets_3channels.json --out out
"""
import argparse
import csv
import datetime as dt
import json
import os
import statistics
import sys

import scout

scout.COST["playlistItems"] = 1
MAX_SUBS = 500_000  # çok büyük kanallar taklit edilebilir rakip değil
UPLOADS = 40


def find_channels(client, queries, region, lang, days):
    after = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=days)).strftime("%Y-%m-%dT00:00:00Z")
    hits = {}
    for q in queries:
        res = client.get("search", {
            "part": "snippet", "q": q, "type": "video", "order": "viewCount",
            "regionCode": region, "relevanceLanguage": lang, "publishedAfter": after,
            "videoDuration": "long", "maxResults": 25,
        })
        for i in res.get("items", []):
            hits.setdefault(i["snippet"]["channelId"], set()).add(q)
    ids = list(hits)
    channels = []
    for part in scout.chunks(ids, 50):
        res = client.get("channels", {"part": "snippet,statistics,contentDetails", "id": ",".join(part)})
        channels += res.get("items", [])
    return channels, hits


def measure(client, ch, now):
    uploads = ch["contentDetails"]["relatedPlaylists"]["uploads"]
    pl = client.get("playlistItems", {"part": "contentDetails", "playlistId": uploads, "maxResults": UPLOADS})
    ids = [i["contentDetails"]["videoId"] for i in pl.get("items", [])]
    if not ids:
        return None
    vids = client.get("videos", {"part": "snippet,statistics,contentDetails", "id": ",".join(ids)}).get("items", [])
    longs = []
    for v in vids:
        d = scout.parse_duration(v["contentDetails"].get("duration"))
        if d >= scout.MIN_DURATION_S:
            longs.append({"id": v["id"], "title": v["snippet"]["title"], "dur": d,
                          "views": int(v["statistics"].get("viewCount", 0)),
                          "ts": scout.parse_ts(v["snippet"]["publishedAt"])})
    if len(longs) < 3:
        return None
    recent = [v for v in longs if (now - v["ts"]).days <= 90]
    cs = ch["statistics"]
    subs = None if cs.get("hiddenSubscriberCount") else int(cs.get("subscriberCount", 0))
    med = statistics.median(v["views"] for v in longs)
    best = max(longs, key=lambda v: v["views"])
    return {
        "channel_id": ch["id"], "channel": ch["snippet"]["title"], "subs": subs,
        "age_days": (now - scout.parse_ts(ch["snippet"]["publishedAt"])).days,
        "per_week_90d": round(len(recent) / (90 / 7), 1),
        "median_views": int(med), "best_views": best["views"], "best_title": best["title"], "best_id": best["id"],
        "median_dur_min": round(statistics.median(v["dur"] for v in longs) / 60),
        "views_per_sub": round(med / subs, 2) if subs else None,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--targets", required=True)
    ap.add_argument("--out", default="out")
    ap.add_argument("--days", type=int, default=365)
    ap.add_argument("--top", type=int, default=12, help="Hedef başına raporlanacak kanal")
    ap.add_argument("--quota-budget", type=int, default=9000)
    args = ap.parse_args()

    key = os.environ.get("YOUTUBE_API_KEY")
    if not key:
        print("YOUTUBE_API_KEY tanımlı değil.", file=sys.stderr)
        return 2
    with open(args.targets, encoding="utf-8") as f:
        targets = json.load(f)["targets"]
    os.makedirs(args.out, exist_ok=True)
    client = scout.Client(key, os.path.join(args.out, "cache"))
    now = dt.datetime.now(dt.timezone.utc)
    allrows, lines = [], ["# Rakip kanallar\n",
                          "Sıralama: medyan izlenme (son uzun videolar). views/sub > 1 = abone tabanından büyük erişim. "
                          f"Aboneliği {MAX_SUBS:,} üstü kanallar hariç.\n"]
    try:
        for t in targets:
            if client.spent + len(t["queries"]) * 100 > args.quota_budget:
                print(f"{t['slug']}: bütçe yetmedi, atlandı")
                continue
            channels, hits = find_channels(client, t["queries"], t["region"], t["lang"], args.days)
            rows = []
            for ch in channels:
                subs = None if ch["statistics"].get("hiddenSubscriberCount") else int(ch["statistics"].get("subscriberCount", 0))
                if subs is not None and subs > MAX_SUBS:
                    continue
                m = measure(client, ch, now)
                if m:
                    m.update(slug=t["slug"], hit_queries=len(hits[ch["id"]]))
                    rows.append(m)
            rows.sort(key=lambda r: r["median_views"], reverse=True)
            allrows += rows
            print(f"{t['slug']}: {len(channels)} kanal bulundu, {len(rows)} ölçüldü (kota: {client.spent})")
            lines.append(f"## {t['slug']} — {t['niche']} ({t['lang']}-{t['region']})\n")
            lines.append("| Kanal | Abone | Yaş (ay) | Video/hafta | Medyan izlenme | views/sub | Süre dk | En iyi video |")
            lines.append("|---|---|---|---|---|---|---|---|")
            for r in rows[:args.top]:
                lines.append(f"| [{r['channel']}](https://youtube.com/channel/{r['channel_id']}) | "
                             f"{r['subs'] if r['subs'] is not None else '?'} | {r['age_days'] // 30} | {r['per_week_90d']} | "
                             f"{r['median_views']:,} | {r['views_per_sub']} | {r['median_dur_min']} | "
                             f"[{r['best_views']:,}](https://youtu.be/{r['best_id']}) {r['best_title'][:50]} |")
            lines.append("")
    except scout.QuotaError as e:
        print(str(e), file=sys.stderr)
    with open(os.path.join(args.out, "competitors.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    if allrows:
        with open(os.path.join(args.out, "competitors.csv"), "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(allrows[0]), extrasaction="ignore")
            w.writeheader()
            w.writerows(allrows)
    print(f"Rapor: {os.path.join(args.out, 'competitors.md')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
