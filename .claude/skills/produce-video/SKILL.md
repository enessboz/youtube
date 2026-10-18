---
name: produce-video
description: Bir kanal için tek videoyu konu seçiminden yayın paketine kadar alt ajanlarla üretir. Kullanıcı "yeni video", "sıradaki konu" veya belirli bir backlog konusu için video istediğinde kullan.
---

# Video üretim akışı (üst ajan için)

Sen üst ajansın: işi alt ajanlara devret, çıktıları kontrol et, kapılarda kullanıcıya dur. Tek ajan her şeyi yapmaz.

Girdi: kanal slug'ı (`gestern-gabs-das` | `quando-eravamo-noi`) ve backlog konusu (yoksa `channels/<kanal>/topics/backlog.md`'den ilk "aday" konuyu öner).

| # | Adım | Ajan (varsayılan model) | Kapı |
|---|---|---|---|
| 0 | Video klasörü + brief | `ops-clerk` (haiku) | — |
| 1 | Araştırma → `research.md` | `research-analyst` (opus) | **Kullanıcı:** kaynaklar ve açı uygun mu? |
| 2 | Senaryo → `script.md` | `script-writer` (opus) | — |
| 3 | Doğrulama → `factcheck.md` | `fact-checker` (sonnet) | ≥3 yanlış/doğrulanamayan → opus ile tekrar |
| 4 | Dil redaksiyonu → `native-edit-notes.md` | `native-editor` (sonnet) | **İnsan anadil düzeltmeni** işaretli satırlara bakar |
| 5 | Paketleme → `packaging.md` | `packager` (sonnet) | **Kullanıcı** başlık ve kapağı seçer |
| 6 | Görsel plan → `scenes.json` | `visual-director` (sonnet; ilk 3 videoda opus) | **Kullanıcı** stil ve kaynakları onaylar |
| 7 | Uyum kontrolü → `compliance.md` | `compliance-reviewer` (haiku) | KALDI/EMİN DEĞİLİM → sonnet/opus ikinci görüş |
| 8 | Seslendirme (ElevenLabs) | betik (`pipeline/voice`, kurulunca) | **Kullanıcı onayı** (maliyet) ve dinleme |
| 9 | Render ve yükleme taslağı (özel) | betik (`pipeline/render`, `pipeline/publisher`, kurulunca) | **Kullanıcı** yayına alır |
| 10 | 14. gün değerlendirmesi | `analytics-analyst` (sonnet) | Kill/ölçekle kararı kullanıcıda |

Kurallar:
- Her adımın çıktısı video klasörüne yazılır; sonraki ajan yalnızca dosyadan okur (sohbet belleğine güvenme).
- Model yükseltme/düşürme: `docs/AGENTS.md`. Agent aracında `model` parametresiyle geçersiz kıl; gerekçeyi `video-log.md`'ye yaz.
- Bir ajan "ÜST AJANA YÜKSELT" derse: daha güçlü modelle tekrar çalıştır veya kullanıcıya sor; sessizce geçme.
- Adım 8 ve sonrası boru hattı kodu kurulana kadar atlanır; kullanıcıya hangi adımda olduğunu söyle.
- Her adım sonunda `video-log.md`'ye tek satır: adım, ajan, model, tarih, sonuç.
