# Bütçe (haftalık)

Senaryo: iki kanal × 3 video/hafta = **6 video/hafta**, 25 dk/video. Doğrulanmış ve varsayım kısımları ayrı yazıldı; fiyatlar değişir, ödeme yapmadan önce resmi sayfadan doğrula.

## Ses (ElevenLabs) — doğrulanmış kısım
Kaynak: elevenlabs.io/pricing/api (erişim: 2026-10). Çok dilli v2/v3 ve Flash modeli karakter bazlı.

| Plan | Aylık | Dahil karakter (v2/v3) | Dahil karakter (Flash) |
|---|---|---|---|
| Starter | $6 | 75.000 | 150.000 |
| Creator | $22 | 275.000 | 550.000 |
| Pro | $99 | 1.238.000 | 2.475.000 |
| Scale | $299 | 3.738.000 | 7.475.000 |

Kullanım başına oran sayfada: v2/v3 **$0,08 / 1.000 karakter**, Flash **$0,04 / 1.000 karakter**. Sayfa ticari kullanım haklarını, Voice Design'ın hangi plana dahil olduğunu ve aşım fiyatını açıkça belirtmiyor: **abonelik almadan önce doğrula**. Üçüncü taraf kaynaklarda rakamlar çelişiyor; resmi sayfa esas alındı.

**Hesap:**
- 25 dk ≈ 3.500 kelime ≈ 22.000-25.000 karakter (Almanca ~24,5K, İtalyanca ~21,7K).
- Yeniden üretim ve ses testleri için %30 pay: ≈ 31.000 karakter/video.
- 6 video/hafta ≈ 187.000 karakter/hafta ≈ 810.000 karakter/ay.

| Seçenek | Aylık | Haftalık ≈ | Not |
|---|---|---|---|
| Creator (275K) | $22 | $5 | Yetmez: ayda ~9 video. Ses seçimi ve ilk 2-3 video için uygun. |
| **Pro (1,238M)** | **$99** | **$23** | 6 video/hafta için yeterli, kalan pay yeniden üretime. **Önerilen.** |
| **API, kullandığın kadar öde (v2/v3)** | **≈ $65** | **$15** | Doğrulandı (elevenlabs.io/pricing/api): $0,08 / 1K karakter, taahhüt yok, USD faturalanır. Pro ile aynı oran ($80/1M), ama sabit ücret yok. |
| API, kullandığın kadar öde (Flash/Turbo) | ≈ $32 | $7,5 | Doğrulandı: $0,04 / 1K karakter; daha az doğal |
| Flash ile Pro | $99 | — | Karakter payı iki katı ama daha az doğal; 55+ kitlede dinleyerek karşılaştır |

**Öneri (güncel):** abonelik yerine **API'de kullandığın kadar öde**. Pro'nun etkin oranı da $80/1M karakter olduğu için, 1,238M karakterin altında kullanıyorsak ($99'ı doldurmuyorsak) PAYG her zaman eşit veya ucuz. Bir video ≈ $2-2,5, 60 sn'lik ses testi ≈ $0,08. Doğrulanması gerekenler: minimum harcama/ön ödeme, PAYG'de ticari kullanım hakkı ve Voice Design erişimi. Bunlardan biri kapalıysa Starter ($1 ilk ay) ile başla.

## Ses alternatifleri (ucuz seçenekler) — aylık ≈ 810K karakter için
Doğrulanmış = resmi sayfada gördüm; doğrulanmadı = hafızamdan veya üçüncü taraf kaynaktan.

| Sağlayıcı | Oran | Aylık ≈ | Durum | Not |
|---|---|---|---|---|
| ElevenLabs Pro | $99 sabit (1,238M karakter) | $99 | doğrulandı | Voice Design ile **kanala özel, benzersiz ses**; en pahalı |
| ElevenLabs Flash (kullanım) | $0,04 / 1K | ≈ $32 | doğrulandı | Yarı fiyat, daha az doğal; plan fiyatı değil kullanım oranı |
| OpenAI `tts-1` | $15 / 1M karakter | ≈ $12 | doğrulandı (resmi sayfa) | Ucuz; **paylaşılan hazır sesler** (benzersiz değil) |
| OpenAI `tts-1-hd` | $30 / 1M karakter | ≈ $24 | doğrulandı | Aynı sesler, daha kaliteli |
| OpenAI `gpt-4o-mini-tts` | ses çıktısı $12 / 1M token (dakika karşılığı sayfada yok) | ≈ ? | kısmen | Tonu/aksanı talimatla yönlendirilebilir; token→dakika dönüşümünü test et |
| Azure Neural TTS | aylık 0,5M karakter ücretsiz; ücretli oran bu oturumda okunamadı | ≈ $5-15 | doğrulanmadı | Almanca/İtalyanca nöral sesler çok; sesler yaygın |
| Google Cloud TTS | Standard ≈ $4, Neural2 ≈ $16, Chirp 3 HD ≈ $30 / 1M | ≈ $3-24 | doğrulanmadı | Sayfa okunamadı; de-DE/it-IT desteğini doğrula |
| Cartesia | kredi bazlı (Startup $49, 1,25M kredi) | ≈ $49 | kısmen | Kredi→karakter dönüşümü belirsiz |

**Dengesi:** Ucuz seçeneklerde (OpenAI, Azure, Google) sesler çoğunlukla başkalarının da kullandığı hazır sesler; planın "yaygın hazır sesten kaçın" kuralıyla çelişir (toplu üretim işareti). ElevenLabs'in farkı Voice Design ile benzersiz ses. Bunun izleyici tutmasına etkisini **bilmiyoruz**.

**Karar yöntemi (maliyeti < $5):** Aynı 60 sn'lik Almanca ve İtalyanca örneği 4 motorla üret (ElevenLabs Creator ayı, OpenAI `tts-1-hd` ve `gpt-4o-mini-tts`, Azure veya Google), anadili konuşan (mümkünse 55+) birine kör dinlet. Ucuz seçenek yeterliyse onu seç. ElevenLabs'te maliyeti düşüren yollar: Flash, retake payını azaltmak, ilk ay Creator.

**Perspektif:** 2 kanal × 20 video test fazı ≈ 40 video ≈ 1,24M karakter ≈ **tek Pro ayı ($99)**. Yani ElevenLabs'in tüm test fazı maliyeti yaklaşık $100-130; kill edersek kayıp bu.

## Diğer kalemler — varsayım (henüz sağlayıcı seçilmedi)
| Kalem | Haftalık tahmin | Dayanak |
|---|---|---|
| Görsel üretimi | $10-20 | 25 dk ≈ 165 sahne; hedef ≤%25 üretim ≈ 40 görsel/video × 6 ≈ 240 görsel/hafta × $0,04-0,08 (**varsayım**; sağlayıcı ve fiyat seçilince güncelle) |
| Arşiv/stok görsel | $0 | Lisanslı/atıflı kamu malı ve CC kaynaklar (`docs/VISUALS.md`) |
| Müzik | $0 | YouTube Ses Kitaplığı veya lisanslı kütüphane; telifli müzik yok |
| Kurgu/render | $0 | Remotion + ffmpeg; Remotion lisans koşulunu doğrula |
| Anadil düzeltmeni | **bilinmiyor** | Freelance teklif al; video başına maliyet kalemi (kalite için zorunlu) |
| Claude kullanımı | **bilinmiyor** | Oturum planına dahil mi API token mı belirlenmeli; ilk 3 videoda ölç |
| YouTube Data/Analytics API | $0 | Ücretsiz; kota 10.000 birim/gün |

**Toplam (bilinenler):** ses ≈ $23 + görsel ≈ $10-20 ≈ **$33-43/hafta (≈ $140-190/ay)**, düzeltmen ve Claude maliyeti hariç. Transkriptteki kişinin ~400-800$/ay harcaması bunun üstünde; biz görsel üretimi azalttığımız için daha düşük başlıyoruz.

## Bütçe tavanı (karar bekliyor)
Kill kuralıyla birlikte **kanal başına test bütçesi** belirlenmeli (öneri: ilk 20 video için toplam harcama tavanı). Tavan aşılırsa üretim durur ve kullanıcıya sorulur.
