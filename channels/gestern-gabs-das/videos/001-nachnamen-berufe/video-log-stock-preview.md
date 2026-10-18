# Video log — Nachnamen, die einen Beruf verraten: Müller, Schmidt, Wagner & Co.

| Tarih | Adım | Ajan | Model | Sonuç |
|---|---|---|---|---|
| 2026-10-18 Europe/Istanbul | Repo ve anahtar kontrolü | producer | Codex/GPT-6, oturumun atanmış modeli | İstenen dal indirildi; Pexels anahtarı yalnızca ortamda kullanıldı, değeri loglanmadı. |
| 2026-10-18 Europe/Istanbul | Senaryo | script-writer | Geçerli Codex modeli | 3.462 konuşma kelimelik 13 meslekli taslak ve ilk dört meslek için ayrı preview JSON üretildi. |
| 2026-10-18 Europe/Istanbul | Bağımsız olgu/dil kontrolü | factcheck-editor | Geçerli Codex modeli | Gösterilmeyen arşiv fotoğraflarına göndermeler, özel anıt ve dil sorunları düzeltildi. İnsan anadil incelemesi yapılmadı. |
| 2026-10-18 Europe/Istanbul | Stok görüntü planı | visual-director | Geçerli Codex modeli | Pexels arama/indirme; gerçek karelerden temas sayfaları; uygunsuz sanayi/tarım/logo/bayrak klipleri elendi. |
| 2026-10-18 Europe/Istanbul | Altyazı ve kurgu | producer | Codex + deterministik Python/Remotion | 63 hareketli plan, 17 stok kaynak, 3 gravür PiP; en fazla iki satır altyazı. Sahne kaynakları scenes.stock-plan.json içinde. |
| 2026-10-18 Europe/Istanbul | Render hata giderme | producer | Kod araçları | Remotion Windows ffprobe/compositor 3221225477 ile çöktü. Statik FFmpeg/ffprobe eklendi; Html5Video kısa test geçti, tam kesitte yavaş. Aynı planı yerel FFmpeg ile 1080p30/CRF26 işleme yolu eklendi. |
| 2026-10-18 Europe/Istanbul | Teknik doğrulama | producer | FFmpeg/ffprobe + Python/TypeScript | Altyazı kelime koruma ve iki satır testi, kabul edilmiş klip/süre testi, TypeScript kontrolü geçti. Video tamamen çözümlendi; ses akışı yok. |
| 2026-10-18 Europe/Istanbul | Uyum | compliance-reviewer | Geçerli Codex modeli | Özel editoryal önizleme için kontrol; insan anadil, açık kaynak ayrıntıları ve yayın paketi nedeniyle yayın kapısı kapalı. |

## Model uyarlaması

Repodaki opus/sonnet/haiku rol isimleri bu Codex oturumunda seçilebilir model kimlikleri değildir. Roller ayrı alt ajanlara devredildi; erişilmeyen Claude modelleri çalıştırılmış gibi raporlanmadı. Ücretli medya API'si, ses üretimi veya yayın yapılmadı.

## Kapsam

İlk kesit sessizdir ve yaklaşık 4:36 sürer; tüm 25 dakikalık video render edilmedi. Tam senaryonun sonraki dokuz mesleği henüz olgu/dil kontrolünden geçmedi. Kullanıcı önce bu kurgu yönünü değerlendirecek. Son ses için Qwen entegrasyonu bu kesite dahil değildir.

## Bilinen kalite sınırları

- Hareketli kaynaklar güncel meslek temsilleridir; tarihî Alman yer/olay görüntüsü olarak sunulmaz.
- Özellikle değirmen bölümünde kaynak havuzu dar ve bazı kesitler tekrar ediyor. Tam bölüm öncesi daha çeşitli çekimler gerekir.
- Altyazı süreleri yaklaşık 140 kelime/dakika okuma hızından hesaplandı; ses eklendiğinde gerçek sesle hizalanacak.
- FFmpeg yolunda 0,10 saniyelik dip kesmeler var; Remotion yay animasyonları bu çıkışta yok.
- CRF26 ile ayrıntılı hareketli 1080p görüntüyü 10 MB'a sığdırmak mümkün olmadı; yüksek kalite kopyanın yanında yaklaşık 10 MB/720p izleme kopyası hazırlanıyor.

## Eşzamanlı dal güncellemesiyle birleştirme

Üretim sırasında origin dalına b7cb21c geldi. O güncellemenin ana script.md, factcheck.md, native-edit-notes.md, compliance.md, shotlist ve Remotion bileşenleri korundu. Bu oturumun tam senaryo taslağı script-stock-draft.md, önizleme kontrolleri *-stock-preview.md ve sahneleri scenes.stock-preview.json / scenes.stock-plan.json adlarında saklandı. Gerçek teslim dosyası yerel FFmpeg ile üretilen stock-preview varyantıdır. Bu ayrım diğer çalışmanın üstüne yazılmasını önler.
