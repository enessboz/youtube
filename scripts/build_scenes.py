#!/usr/bin/env python3
"""build_scenes: script.md + shotlist.json -> scenes.render.json (sessiz, altyazılı kesit).

Anlatıcı sesi yokken tempo kontrolü için her cümle öbeği ekranda altyazı olur; süre kelime sayısından
(~140 kelime/dk) hesaplanır ve her öbeğe shotlist'teki sıradaki klip atanır.

Kullanım:
  python3 scripts/build_scenes.py <kanal> <video> [--sections kanca,einleitung,1,2] [--wpm 140]
Girdi : channels/<kanal>/videos/<video>/script.md, shotlist.json, assets/footage/*.json
Çıktı : scenes.render.json (+ build-report.txt)
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def parse_sections(text):
    """script.md -> {anahtar: anlatım metni}. Anahtar: kanca | einleitung | kapanis | 1..13"""
    out = {}
    for block in re.split(r"\n(?=## )", text)[1:]:
        head, _, body = block.partition("\n")
        h = head.lower()
        m = re.match(r"##\s*(\d+)\.", head)
        key = m.group(1) if m else "kanca" if "kanca" in h else "einleitung" if "einleitung" in h else "kapanis" if "kapan" in h else None
        if not key:
            continue
        lines = []
        for ln in body.splitlines():
            ln = ln.strip()
            if ln.startswith("[SAHNE"):
                continue
            ln = re.sub(r"\s*\[(KONTROL|SAHNE)\b.*$", "", ln).strip()
            if not ln or ln == "---" or re.fullmatch(r"\[CTA-\d\]", ln):
                continue
            lines.append(ln)
        out[key] = lines
    return out


def units(lines):
    """Satırlar -> cümle birimleri (satır sonu noktalamasız ise sonrakiyle birleşir)."""
    res, cur = [], ""
    for ln in lines:
        cur = (cur + " " + ln).strip()
        if re.search(r"[.!?…:“”\"]$", cur):
            res.extend(s for s in re.split(r"(?<=[.!?])\s+(?=[A-ZÄÖÜ„])", cur) if s)
            cur = ""
    if cur:
        res.append(cur)
    return res


def words(s):
    return len(s.split())


def chunk(sentences, lo=7, hi=18):
    """Cümleleri altyazı öbeklerine böl/birleştir (hedef ~7-18 kelime)."""
    parts = []
    for s in sentences:
        if words(s) > 20:
            segs = re.split(r"(?<=,)\s+|(?<=;)\s+", s)
            buf = ""
            for g in segs:
                if buf and words(buf + " " + g) > hi:
                    parts.append(buf)
                    buf = g
                else:
                    buf = (buf + " " + g).strip()
            if buf:
                parts.append(buf)
        else:
            parts.append(s)
    out = []
    for p in parts:
        if out and (words(out[-1]) < lo) and words(out[-1]) + words(p) <= hi + 4:
            out[-1] += " " + p
        else:
            out.append(p)
    if len(out) > 1 and words(out[-1]) < 4:
        out[-2] += " " + out.pop()
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("channel")
    ap.add_argument("video")
    ap.add_argument("--sections", default="kanca,einleitung,1")
    ap.add_argument("--wpm", type=float, default=140)
    a = ap.parse_args()
    vdir = ROOT / "channels" / a.channel / "videos" / a.video
    secs = parse_sections((vdir / "script.md").read_text(encoding="utf-8"))
    plan = json.loads((vdir / "shotlist.json").read_text(encoding="utf-8"))
    xf = plan.get("crossfade_s", 0.5)
    cursor = {}  # klip -> sonraki trim
    meta = {}
    scenes, report = [], []
    n = 0

    def clip_len(c):
        if c not in meta:
            meta[c] = float(json.loads((vdir / "assets" / "footage" / f"{c}.json").read_text())["duration"])
        return meta[c]

    for key in a.sections.split(","):
        sec = plan["sections"].get(key, {})
        shots = sec.get("shots", [])
        if not shots:
            sys.exit(f"shotlist'te çekim yok: {key}")
        caps = chunk(units(secs[key]))
        last_clip = None
        sec_dur = 0.0
        cards = sec.get("cards", [])
        i = -1
        pending = None  # birleştirilen kart sahnesi
        for cap in caps:
            i += 1
            card = next((c for c in cards if re.search(c["match"], cap)), None)
            if card:
                d = round(max(2.8, words(cap) * 60 / a.wpm + 0.4), 2)
                if pending is not None and pending["_m"] == card["match"]:
                    pending["duration_s"] = round(pending["duration_s"] + d, 2)
                    pending["captions"].append({"text": cap, "duration_s": d})
                else:
                    n += 1
                    pending = {"id": f"s{n:03d}", "type": "title", "duration_s": d, **card["scene"],
                               "captions": [{"text": cap, "duration_s": d}], "_m": card["match"]}
                    scenes.append(pending)
                sec_dur += d
                continue
            if pending is not None:
                pending.pop("_m", None)
                pending = None
            dur = max(2.8, words(cap) * 60 / a.wpm + 0.4)
            dur = round(dur, 2)
            sh = shots[i % len(shots)]
            if sh["clip"] == last_clip and len(shots) > 1:
                sh = shots[(i + 1) % len(shots)]
            c = sh["clip"]
            L = clip_len(c)
            need = dur + xf + 0.2
            start = cursor.get(c, sh.get("trim_s", 0.0))
            if start + need > L:
                start = 0.0 if need <= L else 0.0
            rate = 1.0
            if need > L:
                rate = max(0.5, round(L / need, 2))
            cursor[c] = start + need * rate + 0.5
            n += 1
            sc = {
                "id": f"s{n:03d}",
                "type": "clip",
                "duration_s": dur,
                "src": f"assets/footage/{c}.mp4",
                "trim_start_s": round(start, 2),
                "playback_rate": rate,
                "grade": "warm",
                "motion": sh.get("motion", "still"),
                "caption": cap,
                "text_anchor": cap,
            }
            if i == 0 and sec.get("label"):
                sc["label"] = sec["label"]
            pip = sec.get("pip")
            if pip and i + 1 == pip.get("at_scene", 2):
                sc["pip"] = {k: pip[k] for k in ("src", "caption", "side") if k in pip}
            scenes.append(sc)
            last_clip = c
            sec_dur += dur
        report.append(f"{key}: {len(caps)} sahne, {sec_dur:.0f} sn")
        if key == "kanca" and plan.get("title_after_kanca"):
            t = plan["title_after_kanca"]
            n += 1
            scenes.append({"id": f"s{n:03d}", "type": "title", "duration_s": 3.5, **t})
    for sc in scenes:
        sc.pop('_m', None)
    total = sum(s["duration_s"] for s in scenes)
    report.append(f"toplam: {total:.0f} sn ({total/60:.1f} dk), {len(scenes)} sahne")
    out = {"fps": 30, "crossfade_s": xf, "note": "build_scenes.py çıktısı (sessiz, altyazılı kesit); süreler ~%d kelime/dk" % a.wpm, "scenes": scenes}
    (vdir / "scenes.render.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    (vdir / "build-report.txt").write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(report))


if __name__ == "__main__":
    main()
