#!/usr/bin/env python3
"""handles: @handle listesi için competitors.py ile aynı metrikleri çıkarır (kanal başına ~3 birim).

Kullanım: python3 handles.py @MemoriaRetroOficial @RecetasDeAntes --out out
"""
import argparse
import datetime as dt
import os
import sys

import competitors
import scout


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("handles", nargs="+")
    ap.add_argument("--out", default="out")
    args = ap.parse_args()
    key = os.environ.get("YOUTUBE_API_KEY")
    if not key:
        print("YOUTUBE_API_KEY tanımlı değil.", file=sys.stderr)
        return 2
    scout.COST["playlistItems"] = 1
    client = scout.Client(key, os.path.join(args.out, "cache"))
    now = dt.datetime.now(dt.timezone.utc)
    for h in args.handles:
        res = client.get("channels", {"part": "snippet,statistics,contentDetails", "forHandle": h})
        items = res.get("items", [])
        if not items:
            print(f"{h}: bulunamadı")
            continue
        m = competitors.measure(client, items[0], now)
        print(h, m)
    print(f"kota: {client.spent}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
