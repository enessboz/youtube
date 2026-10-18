# Ajan yapısı ve model yönlendirme

**Üst ajan (producer):** ana Claude Code oturumu. İşi planlar, alt ajanlara devreder (Agent aracı), çıktıları kontrol eder, kapılarda kullanıcıya durur. Akış: `.claude/skills/produce-video/SKILL.md`.
**Alt ajanlar:** `.claude/agents/*.md`. Her birinin tek bir işi, kendi araç listesi ve varsayılan modeli var. Alt ajanlar birbirini çağırmaz; koordinasyon üst ajandadır.

| Ajan | İş | Varsayılan | Yükselt (→ opus) | Düşür (→ haiku) |
|---|---|---|---|---|
| `research-analyst` | kaynaklı araştırma | opus | zaten en üst | — (araştırma kalitesi kritik) |
| `script-writer` | senaryo | opus | zaten en üst | kısa düzeltme turu için sonnet |
| `fact-checker` | doğrulama | sonnet | ≥3 yanlış/doğrulanamayan, ilk 3 video | — |
| `native-editor` | dil redaksiyonu | sonnet | ton/dil sorunu sürerse | — |
| `packager` | başlık/kapak/açıklama | sonnet | kanalın ilk 3 videosu, düşük CTR sonrası tur | etiket ve açıklama biçimlendirme |
| `visual-director` | sahne planı | sonnet | ilk 3 video, yeni stil kararı | tekrar eden sahne şablonu |
| `compliance-reviewer` | uyum kapısı | haiku | KALDI/EMİN DEĞİLİM → sonnet, sonra opus | — |
| `analytics-analyst` | haftalık rapor | sonnet | kill/ölçekle kararı sınırdaysa | veri çekme/biçimlendirme |
| `ops-clerk` | klasör/manifest | haiku | — | — |

## Model yönlendirme kuralları (üst ajan uygular)
1. **Varsayılan, dosyadaki `model:` değeridir.** Agent aracında `model` parametresiyle iş başına geçersiz kılınabilir; gerekçe `video-log.md`'ye yazılır.
2. **Yükselt:** çıktı kalite çıtasının altında; ajan "ÜST AJANA YÜKSELT" dedi; iddialar çelişiyor; kanalın ilk 3 videosu (tonu ve çıtayı bu belirler); yüksek maliyetli bir karar (kapak seçimi, kill/ölçekle).
3. **Düşür:** iş mekanik veya biçimsel (dosya adlandırma, manifest, açıklamayı şablona yerleştirme, kontrol listesi işaretleme).
4. **Opus'u yalnızca değer yarattığı yerde kullan:** araştırma ve senaryo. Diğerlerinde önce sonnet/haiku dene, kalite yetmezse yükselt.
5. Model adları: Opus 5.5, Sonnet 5.5, Haiku 5.5 (Agent aracında `opus`/`sonnet`/`haiku`). Güncel model listesi ve fiyatlar kullanıldığında doğrulanır.

## Kapılar (insan onayı olmadan geçilmez)
Konu ve kaynaklar → anadil düzeltmeni işaretli satırlar → başlık/kapak seçimi → görsel stil → ses (maliyet) → yayın.

## Genişletme
Yeni rol gerekirse `.claude/agents/<rol>.md` ekle, bu tabloyu ve `produce-video` akışını güncelle. Aynı anda birden fazla videoyu paralel üretmek için üst ajan bağımsız ajanları aynı anda çağırabilir (ör. iki kanalın araştırması). Büyük toplu işler için Workflow aracı yalnızca kullanıcı açıkça isterse kullanılır.
