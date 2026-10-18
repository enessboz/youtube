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
| Kullanım başına (v2/v3) | ≈ $65 | $15 | 810K × $0,08/1K; hesapta kullanım başına seçeneğin kullanılabilirliğini doğrula |
| Flash ile Pro | $99 | — | Karakter payı iki katı ama daha az doğal; 55+ kitlede dinleyerek karşılaştır |

**Öneri:** ilk ay Creator (ses seçimi + 2-3 test videosu), kanallar 6 video/hafta temposuna gelince Pro.

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
