#!/usr/bin/env python3
"""new_video: bir kanal için numaralı video klasörünü şablondan açar.

Kullanım:
  python3 scripts/new_video.py <kanal> <slug> [--title ...] [--kind liste|derin|karsilastirma] [--tag kanit|bosluk|deneme|kalabalik]

Klasör: channels/<kanal>/videos/NNN-<slug>/ (NNN, mevcut en büyük numara + 1).
channel.yaml içindeki `target_minutes:` değeri brief ve senaryoya yazılır.
"""
import argparse
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUBDIRS = ("assets", "audio", "render")
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def flat_value(path, key, default=None):
    """Düz `anahtar: değer` satırından değeri okur (yaml bağımlılığı yok)."""
    if not os.path.exists(path):
        return default
    with open(path, encoding="utf-8") as f:
        for line in f:
            m = re.match(rf"^{re.escape(key)}:\s*(.+?)\s*(#.*)?$", line)
            if m:
                return m.group(1).strip().strip("\"'")
    return default


def next_number(videos_dir):
    nums = [int(m.group(1)) for d in os.listdir(videos_dir) if (m := re.match(r"^(\d{3})-", d))] \
        if os.path.isdir(videos_dir) else []
    return max(nums, default=0) + 1


def create(channel, slug, title=None, kind="liste", tag="deneme", root=ROOT):
    if not SLUG.match(slug):
        raise ValueError("slug küçük harf, rakam ve tireden oluşmalı")
    channel_dir = os.path.join(root, "channels", channel)
    if not os.path.isdir(channel_dir) or channel.startswith("_"):
        raise FileNotFoundError(f"kanal yok: {channel}")
    videos_dir = os.path.join(channel_dir, "videos")
    os.makedirs(videos_dir, exist_ok=True)
    vid = f"{next_number(videos_dir):03d}-{slug}"
    dest = os.path.join(videos_dir, vid)
    os.makedirs(dest)
    subs = {
        "title": title or slug.replace("-", " "),
        "channel": channel,
        "id": vid,
        "kind": kind,
        "tag": tag,
        "target_minutes": flat_value(os.path.join(channel_dir, "channel.yaml"), "target_minutes", "25"),
    }
    tpl = os.path.join(root, "shared", "templates", "video")
    for name in os.listdir(tpl):
        with open(os.path.join(tpl, name), encoding="utf-8") as f:
            text = f.read()
        for k, v in subs.items():
            text = text.replace("{{" + k + "}}", str(v))
        with open(os.path.join(dest, name), "w", encoding="utf-8") as f:
            f.write(text)
    for d in SUBDIRS:
        os.makedirs(os.path.join(dest, d))
        open(os.path.join(dest, d, ".gitkeep"), "w").close()
    return dest


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("channel")
    ap.add_argument("slug")
    ap.add_argument("--title")
    ap.add_argument("--kind", default="liste", choices=["liste", "derin", "karsilastirma"])
    ap.add_argument("--tag", default="deneme", choices=["kanit", "bosluk", "deneme", "kalabalik"])
    a = ap.parse_args()
    try:
        print(create(a.channel, a.slug, a.title, a.kind, a.tag))
    except (ValueError, FileNotFoundError) as e:
        print(f"hata: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
