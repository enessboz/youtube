# Mimari ve klasör düzeni

```
youtube/
  PLAN.md                    ana plan (§7 kanal planı v2)
  CLAUDE.md                  üst ajan kuralları (her oturumda yüklenir)
  .claude/
    agents/                  alt ajanlar (rol başına bir dosya, varsayılan model)
    skills/produce-video/    üst ajanın video üretim akışı ve kapıları
  channels/
    _template/               yeni kanal şablonu
    gestern-gabs-das/        Almanca kanal (her şey bu klasörde)
      channel.yaml             kimlik, kadans, ses, kill eşikleri
      brand/                   identity, tone, voice, visual-style, thumbnail-style, cta
      topics/backlog.md        20 konu ve durumları
      videos/NNN-slug/         brief, research, script, factcheck, packaging,
                               scenes.json, compliance, video-log, metrics, publish,
                               assets/ audio/ render/
      analytics/weekly/        haftalık raporlar
      research/                kanal geneli notlar (rakipler, kaynak havuzları)
    quando-eravamo-noi/      İtalyanca kanal (aynı yapı)
  shared/
    checklists/              compliance.md, originality.md (iki kanal ortak)
    templates/video/         yeni videonun şablon dosyaları
  scripts/new_video.py       numaralı video klasörü açar (test: tests/)
  pipeline/
    niche_scout/             niş ve rakip ölçümü (YouTube Data API)
    voice/ render/ publisher/  (kurulacak) ElevenLabs, Remotion/ffmpeg, YouTube yükleme
  docs/                      ARCHITECTURE, AGENTS, BUDGET, TOOLS, VISUALS
```

## Veri akışı
`backlog.md` → `brief.md` → `research.md` → `script.md` → `factcheck.md` → (redaksiyon) → `packaging.md` → `scenes.json` → `compliance.md` → ses → render → özel yükleme → yayın → `metrics.json` → haftalık rapor → kill/ölçekle.

Her aşama bir dosya üretir; bir sonraki ajan yalnızca o dosyayı okur. Bu sayede oturum kapansa da iş kaldığı yerden devam eder ve her kararın izi dosyada kalır (`video-log.md`).

## Ayrım ilkeleri
- **Kanal başına izolasyon:** her kanalın markası, sesi, stili, konu listesi ve videoları kendi klasöründe. Kanallar arası kopyalama yok.
- **Ortak olan** yalnızca kontrol listeleri, şablonlar ve boru hattı kodu.
- **İnsan kapıları:** konu/kaynak onayı, başlık-kapak seçimi, görsel stil onayı, anadil düzeltmeni, ses dinleme, maliyetli üretim, yayın.
- **Gizli bilgi:** API anahtarları ortam değişkeninde; repoya yazılmaz.
