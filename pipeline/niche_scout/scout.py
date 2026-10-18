#!/usr/bin/env python3
"""niche_scout: niş x ülke adaylarını YouTube Data API ile puanlar.

Fikir: "talep var, rekabet az" işaretlerini ara.
  - small_hits : küçük kanalların (<=20k abone) >=50k izlenen uzun videoları
  - young_hits : son 1 yılda açılmış kanalların >=20k izlenen videoları
  - median_views: sonuçların medyan izlenmesi (talep)
  - big_share  : sonuçların kaç kesri dev kanallardan (>=1M abone) (rekabet)

Kota: search.list = 100 birim, videos/channels.list = 1 birim. Günlük 10.000 birim.
Ham yanıtlar disk önbelleğine yazılır; aynı sorgu ikinci kez kota harcamaz.

Kullanım:
  export YOUTUBE_API_KEY=...
  python3 scout.py --candidates candidates_es.json --out out --dry-run
  python3 scout.py --candidates candidates_es.json --out out
"""
import argparse
import csv
import datetime as dt
import hashlib
import json
import os
import re
import statistics
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "https://www.googleapis.com/youtube/v3"
COST = {"search": 100, "videos": 1, "channels": 1}
MIN_DURATION_S = 180  # Shorts ve çok kısa videoları ele


class QuotaError(RuntimeError):
    pass


class Client:
    def __init__(self, key, cache_dir):
        self.key = key
        self.cache_dir = cache_dir
        self.spent = 0
        os.makedirs(cache_dir, exist_ok=True)

    def get(self, path, params):
        ident = json.dumps([path, sorted(params.items())])
        cache_file = os.path.join(self.cache_dir, hashlib.sha1(ident.encode()).hexdigest() + ".json")
        if os.path.exists(cache_file):
            with open(cache_file, encoding="utf-8") as f:
                return json.load(f)
        url = f"{API}/{path}?" + urllib.parse.urlencode({**params, "key": self.key})
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                data = json.load(r)
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "replace")
            if e.code == 403 and "quota" in body.lower():
                raise QuotaError("Günlük YouTube API kotası doldu; yarın devam edin (önbellek korunur).")
            raise RuntimeError(f"YouTube API hatası {e.code}: {body[:300]}")
        self.spent += COST[path]
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(data, f)
        return data


def parse_duration(iso):
    m = re.fullmatch(r"P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso or "")
    if not m:
        return 0
    d, h, mi, s = (int(x or 0) for x in m.groups())
    return d * 86400 + h * 3600 + mi * 60 + s


def parse_ts(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))


def chunks(seq, n):
    for i in range(0, len(seq), n):
        yield seq[i:i + n]


def collect(client, queries, region, lang, days):
    """Bir niş x ülke için video satırları döndürür."""
    after = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%SZ")
    video_ids = []
    for q in queries:
        res = client.get("search", {
            "part": "snippet", "q": q, "type": "video", "order": "viewCount",
            "regionCode": region, "relevanceLanguage": lang, "publishedAfter": after,
            "videoDuration": "long", "maxResults": 25,
        })
        video_ids += [i["id"]["videoId"] for i in res.get("items", [])]
    video_ids = list(dict.fromkeys(video_ids))

    videos = []
    for ids in chunks(video_ids, 50):
        res = client.get("videos", {"part": "snippet,statistics,contentDetails", "id": ",".join(ids)})
        videos += res.get("items", [])

    channel_ids = list(dict.fromkeys(v["snippet"]["channelId"] for v in videos))
    channels = {}
    for ids in chunks(channel_ids, 50):
        res = client.get("channels", {"part": "snippet,statistics", "id": ",".join(ids)})
        for c in res.get("items", []):
            channels[c["id"]] = c

    rows = []
    for v in videos:
        dur = parse_duration(v["contentDetails"].get("duration"))
        if dur < MIN_DURATION_S:
            continue
        ch = channels.get(v["snippet"]["channelId"])
        if not ch:
            continue
        cs = ch["statistics"]
        rows.append({
            "video_id": v["id"],
            "title": v["snippet"]["title"],
            "channel_id": ch["id"],
            "channel_title": ch["snippet"]["title"],
            "views": int(v["statistics"].get("viewCount", 0)),
            "subs": None if cs.get("hiddenSubscriberCount") else int(cs.get("subscriberCount", 0)),
            "channel_created": ch["snippet"]["publishedAt"],
            "duration_s": dur,
        })
    return rows


def score(rows, now=None):
    """Satırlardan metrik + 0-100 puan üretir (sezgisel, ağırlıklar elle seçildi)."""
    now = now or dt.datetime.now(dt.timezone.utc)
    if not rows:
        return {"n_videos": 0, "n_channels": 0, "median_views": 0, "small_hits": 0,
                "young_hits": 0, "big_share": 1.0, "score": 0.0}
    small_hits = sum(1 for r in rows if r["subs"] is not None and r["subs"] <= 20_000 and r["views"] >= 50_000)
    young_hits = sum(
        1 for r in rows
        if (now - parse_ts(r["channel_created"])).days <= 365 and r["views"] >= 20_000
    )
    known = [r for r in rows if r["subs"] is not None]
    big_share = (sum(1 for r in known if r["subs"] >= 1_000_000) / len(known)) if known else 1.0
    median_views = statistics.median(r["views"] for r in rows)
    s = 100 * (
        0.35 * min(small_hits / 5, 1)
        + 0.25 * min(young_hits / 3, 1)
        + 0.20 * min(median_views / 200_000, 1)
        + 0.20 * (1 - big_share)
    )
    return {
        "n_videos": len(rows),
        "n_channels": len({r["channel_id"] for r in rows}),
        "median_views": int(median_views),
        "small_hits": small_hits,
        "young_hits": young_hits,
        "big_share": round(big_share, 2),
        "score": round(s, 1),
    }


def load_jobs(path, default_lang, default_regions, only_lang=None):
    """İki biçimi destekler: düz liste (tek dil) veya {markets, niches} (çok dilli)."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    jobs = []
    if isinstance(data, list):
        for c in data:
            for region in default_regions:
                jobs.append({"niche": c["niche"], "queries": c["queries"], "lang": default_lang, "region": region})
    else:
        for n in data["niches"]:
            for lang, queries in n["queries"].items():
                if only_lang and lang not in only_lang:
                    continue
                for region in data["markets"].get(lang, []):
                    jobs.append({"niche": n["niche"], "queries": queries, "lang": lang, "region": region})
    return jobs


def estimate_quota(jobs):
    return sum(len(j["queries"]) * 100 + 4 for j in jobs)


def write_report(results, out_dir):
    results.sort(key=lambda r: r["score"], reverse=True)
    fields = ["niche", "lang", "region", "score", "n_videos", "n_channels", "median_views",
              "small_hits", "young_hits", "big_share"]
    with open(os.path.join(out_dir, "results.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(results)
    lines = ["# Niş taraması sonuçları\n",
             "Puan sezgiseldir; son karar için örnek videoları elle incele. "
             "Genel API izleyici yaşını vermez; 55+ uyumu konu seçiminden ve örnek videoların "
             "içeriğinden/yorumlarından elle doğrulanmalıdır.\n"]
    for title, key in (("Niş ortalaması", "niche"), ("Pazar ortalaması", "market")):
        groups = {}
        for r in results:
            k = r[key] if key == "niche" else f"{r['lang']}-{r['region']}"
            groups.setdefault(k, []).append(r["score"])
        lines.append(f"## {title}")
        for k, v in sorted(groups.items(), key=lambda kv: -statistics.mean(kv[1])):
            lines.append(f"- {k}: {statistics.mean(v):.1f} ({len(v)} ölçüm)")
        lines.append("")
    for r in results[:15]:
        lines.append(f"## {r['niche']} — {r['lang']}-{r['region']} (puan {r['score']})")
        lines.append(f"- medyan izlenme {r['median_views']:,}, küçük kanal vuruşu {r['small_hits']}, "
                     f"genç kanal vuruşu {r['young_hits']}, dev kanal payı {r['big_share']}")
        for t in r["top"]:
            lines.append(f"  - [{t['title']}](https://youtu.be/{t['video_id']}) — "
                         f"{t['channel_title']} ({t['subs'] if t['subs'] is not None else '?'} abone, {t['views']:,} izlenme)")
        lines.append("")
    with open(os.path.join(out_dir, "report.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--candidates", required=True)
    ap.add_argument("--out", default="out")
    ap.add_argument("--regions", default="MX,ES", help="Düz liste biçiminde kullanılacak ülkeler")
    ap.add_argument("--lang", default="es", help="Düz liste biçiminde dil")
    ap.add_argument("--only-lang", default="", help="Çok dilli dosyada sadece bu diller (virgüllü)")
    ap.add_argument("--days", type=int, default=365, help="Son kaç gün içinde yüklenen videolar")
    ap.add_argument("--quota-budget", type=int, default=9000, help="Bu çalıştırmada harcanacak azami kota")
    ap.add_argument("--dry-run", action="store_true", help="Sadece kota tahmini yazdır")
    args = ap.parse_args()

    only = [x.strip() for x in args.only_lang.split(",") if x.strip()] or None
    jobs = load_jobs(args.candidates, args.lang, [r.strip() for r in args.regions.split(",")], only)
    est = estimate_quota(jobs)
    print(f"{len(jobs)} iş (niş x pazar); tahmini kota ≈ {est} birim (günlük limit 10.000; önbellekteki işler kota harcamaz)")
    if args.dry_run:
        return 0

    key = os.environ.get("YOUTUBE_API_KEY")
    if not key:
        print("YOUTUBE_API_KEY tanımlı değil.", file=sys.stderr)
        return 2
    os.makedirs(args.out, exist_ok=True)
    client = Client(key, os.path.join(args.out, "cache"))
    results, skipped = [], 0
    try:
        for j in jobs:
            need = len(j["queries"]) * 100 + 4
            if client.spent + need > args.quota_budget:
                skipped += 1
                continue
            rows = collect(client, j["queries"], j["region"], j["lang"], args.days)
            m = score(rows)
            top = sorted(rows, key=lambda r: r["views"], reverse=True)[:3]
            results.append({"niche": j["niche"], "lang": j["lang"], "region": j["region"], "top": top, **m})
            print(f"{j['niche'][:34]:<34} {j['lang']}-{j['region']}  puan {m['score']:>5}  (kota: {client.spent})")
    except QuotaError as e:
        print(str(e), file=sys.stderr)
    write_report(results, args.out)
    if skipped:
        print(f"{skipped} iş bütçe nedeniyle atlandı; aynı komutu yarın tekrar çalıştır (önbellek devam ettirir).")
    print(f"Rapor: {os.path.join(args.out, 'report.md')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
