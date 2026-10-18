# YouTube İçerik Sistemi — Plan (taslak v1)

Kaynak: Ertan Dönmez ile yapılan ~1 saat 44 dk'lık röportaj transkripti.
Amaç: Transkriptteki taktikleri, tekrarlanabilir ve ölçülebilir bir "içerik fabrikası" sistemine çevirmek.

---

## 1. Transkriptten çıkan taktikler

### A. Strateji / iş modeli
| # | Taktik | Not |
|---|--------|-----|
| 1 | **Portföy yaklaşımı**: çok kanal dene, azı tutar. Kendi başarı oranı ~%20-30, "baraj" %40. | Tek kanala bahis yok. |
| 2 | **Hızlı kill kararı**: kanal en fazla ~1 hafta; önerilmiyor / Browse'a düşmüyorsa kenara. | İstatistikler ~5 gün geriden gelir. |
| 3 | **Yüksek RPM nişleri**: finans/ekonomi, tarih/belgesel. Hedef kitle **65+** (zamanı ve parası var, uzun video izler). | Sağlık içeriği bilinçli olarak dışarıda (risk). |
| 4 | **Dil arbitrajı**: İngilizce rekabetli → **Almanca, İspanyolca**; Rusça (Kazakistan, vb.) ucuz ama yüksek izlenme. Türkçe RPM düşük. | Almanca kitle abone olmaya isteksiz, İspanyolca etkileşimli. |
| 5 | **Evergreen > güncel**: model haberi videosu 2 günde ölür, "proje/rehber" videosu yıllarca izlenir. | |
| 6 | **Yüz/insan unsuru**: yüzlü kanallar daha kalıcı, kapanma riski düşük. Tam avatar değil, "AI + insan" hibrit. | |
| 7 | **Pasif gelir kolları**: ElevenLabs ses marketplace'i (kendi klonlanmış sesin), sponsorluk, ürün incelemesi. | |
| 8 | **Ses stratejisi**: yaygın hazır AI seslerden kaçın; kendi sesin (Türkçe oku → İngilizce/Almanca dublaj) veya nadir seçilen ses. | "Aynı ses + aynı kapak + aynı şablon" = toplu inceleme riski. |
| 9 | **Hesap riski**: tek AdSense'e bağlı kanalların hepsi birlikte düşebilir. | Aşağıda §6'ya bak. |

### B. Üretim hattı (pipeline) taktikleri
1. **Rakip analizi**: nişte popüler kanalın ~20 videosunun başlık, kapak, açıklama, transkript → LLM'e ver → anlatıcı tonu, hitap, CTA yerleşimi çıkar.
2. **Yerelleştirme**: Başka dile "çeviri" değil, **kültürel uyarlama** (jargon, para birimi, ekonomi bağlamı).
3. **Deep research** ile bölüm iskeleti; yazım için daha hafif model.
4. **Kapak**: LLM'den 5 alternatif → görsel model → ajanlarla (farklı LLM'ler) puanlama → insan seçer → renk paleti revizesi. İnsan hâlâ kritik (LLM kolay manipüle olur, "yalakalık" yapar).
5. **Karakter tutarlılığı**: karakter sayfası (character sheet) + her prompt sonuna karakter etiketi (`@ref1`, `@ref2`). Kelime ↔ görsel eşleşmesi (söylenen şey ekranda görünmeli).
6. **Ses**: kendi sesinle kayıt → ElevenLabs dublaj. Metinler ana dilde "konuşma tonunda" olmalı (dikte ile yaz → LLM'e "bu benim tonum" diye ver).
7. **Video**: Seedance (hareket), Kling, Higgsfield, Magnific; yerelde LTX 2.3; upscale için Topaz. Kısa sahneler (5-10 sn).
8. **Kurgu/render**: HyperFrames (HeyGen, HTML tabanlı) / Remotion + Claude Code → zaman çizelgesi → otomatik render. Sahne başı not ekle → sistem düzeltir.
9. **Altyazı**: yer yer, otomatik; kötü durduğu yerde kapat.
10. **Kuyruk/otomasyon**: şablon + API, GPU sunucu (RTX 4090 saatlik kiralama), 20 paralel render, 30 dk video ≈ 45 dk.
11. **Yükleme & zamanlama**: kapak, başlık, açıklama, yükleme, en uygun saatte otomatik zamanlama.
12. **Skill/komut mimarisi**: mekanik işler (dosya adlandırma, birleştirme, render) → **script**; yaratıcı işler (hikaye, başlık) → **LLM**. İş parçalara bölünür ("montaj hattı"), skill'ler kısa, "anayasa" değil "yönlendirici kaynak". Çıktıdan öğrenip skill güncellenir.
13. **Yedekleme**: çalışma dizini + sohbet logları günlük zip → Drive; sunucu ↔ yerel senkron.
14. **Maliyet çerçevesi**: kendi söylediği ~400-800$/ay araç + sunucu; maliyet "yeni modelleri denemek" için bütçeli.

---

## 2. Hedef sistem mimarisi

```
[1 Keşif]  →  [2 Analiz]  →  [3 Senaryo]  →  [4 Paketleme]  →  [5 Üretim]  →  [6 Yayın]  →  [7 Ölçüm]
 niş/rakip     transkript    araştırma +     başlık +         görsel/video     yükle +        analytics →
 /dil seçimi   ton/format    yerel uyarlama  kapak (A/B/C)    ses + render     zamanla        kill / scale
```

Her aşama: **kısa skill + deterministik script + insan onay kapısı**. Tam otomasyon değil; "yarı otomatik, insan tek tıkla onaylar".

### Modüller
| Modül | Girdi → Çıktı | Teknoloji önerisi |
|-------|---------------|-------------------|
| `discovery` | niş/dil → rakip kanal listesi + 20 video metadatası | YouTube Data API v3 |
| `analyzer` | transkript+başlık+kapak → "format kılavuzu" (ton, yapı, CTA, süre) | yt-dlp (transkript) + LLM |
| `localizer` | kılavuz + hedef dil → o dile uyarlanmış anlatım profili | LLM + dil/ton profili dosyası |
| `scriptwriter` | konu + profil → bölümlü senaryo | LLM (araştırma ayrı, yazım ayrı) |
| `packager` | senaryo → 5 başlık + 5 kapak → puanlama → seçim | görsel model + çoklu LLM puanlama + insan |
| `assets` | senaryo → sahne listesi → görsel/video klipleri (karakter etiketli) | görsel/video API'leri |
| `voice` | senaryo → ses (kendi ses klonu / nadir ses) | ElevenLabs |
| `renderer` | sahneler+ses+altyazı → mp4 | HyperFrames / Remotion + GPU worker |
| `publisher` | mp4+meta → YouTube (zamanlı) | YouTube Data API (OAuth) |
| `analytics` | kanal metrikleri → günlük rapor + kill/scale önerisi | YouTube Analytics API |
| `backup` | çalışma dizini → günlük zip | cron + Drive |

### Repo yapısı (öneri)
```
youtube/
  PLAN.md
  channels/<kanal-slug>/{config.yaml, tone.md, characters/, videos/}
  pipeline/{discovery,analyzer,localizer,scriptwriter,packager,assets,voice,renderer,publisher,analytics}/
  skills/            # kısa, tek işlik skill dosyaları
  scripts/           # deterministik işler (adlandırma, birleştirme, render kuyruğu)
  templates/         # video şablonları
  docs/
```

---

## 3. Aşamalar

**Faz 0 — Kararlar (1-2 gün):** niş, dil, ilk 3-5 kanal konsepti, bütçe, hesap/AdSense yapısı (§6).

**Faz 1 — Keşif + analiz (1 hafta):** `discovery` + `analyzer`. Çıktı: seçilen niş için "format kılavuzu" + yerelleştirilmiş ton profili.

**Faz 2 — Tek video uçtan uca, manuel-yarı otomatik (1-2 hafta):** senaryo → kapak → görsel → ses → render. Hedef: 1 video, kalite çıtası belirlenir.

**Faz 3 — Otomasyon (2-3 hafta):** render kuyruğu, GPU worker, `publisher` + zamanlama, `backup`.

**Faz 4 — Portföy testi (4+ hafta):** 5-10 konsept paralel, her biri için §4 kuralları, `analytics` günlük rapor.

**Faz 5 — Ölçekleme:** tutan konseptleri çoğalt (yeni dil/alt niş), tutmayanları kes; "yüz/insan" unsurunu ekle.

---

## 4. Karar kuralları (transkriptten)

- Kanal değerlendirme penceresi: **7 gün** (monetization istatistikleri 5 gün gecikmeli).
- "Öneriliyor mu?" → Browse/Suggested/ana sayfa gösterimi var mı? Yoksa kes. Tutuyorsa +1 hafta şans.
- Portföy başarı eşiği: denenen konseptlerin **≥%40'ı** tutuyorsa model sürdürülebilir.
- Kapak: LLM puanı tek başına karar değil; **insan son söz**.
- Yeni model her gün çıkar → **2-3 konsepte odaklan**, hepsine atlama.

## 5. Başarı metrikleri
İzlenme/saat, ilk 48 sa CTR, ortalama izlenme süresi, abone/izlenme, RPM (dil bazlı), video başı maliyet, video başı üretim süresi, konsept başı "tuttu/tutmadı" oranı.

---

## 6. Uyum / risk — bu planda **bilerek dışarıda bırakılanlar**

Transkriptte geçen ama planlamayacağım taktikler:
- **Hesap bağlantısını gizleme / ban atlatma** (ayrı telefon, kurtarma e-postası, "her kanalı ayrı temiz yap"). YouTube'un çoklu hesap/ban evasion politikasına aykırı; ayrıca tek AdSense'in kapanması hepsini götürür. Bunun yerine: **tek marka çatısı, gerçek kimlik, az sayıda kanal**, gelir riskini çeşitlendirme (sponsorluk, ürün, e-posta listesi).
- **Başkasının sesini izinsiz klonlamak** (örn. "arkadaşımın sesi"). Sadece kendi sesin veya yazılı izinli ses.
- **Rakip içeriğini kopyala-uyarla**: Rakipten *yapı/format öğrenmek* tamam; senaryoyu/kapağı birebir yeniden üretmek değil. Her video **özgün araştırma + özgün katkı** taşımalı.
- **Toplu, şablon-tekrarı içerik** (YouTube'un "inauthentic/mass-produced content" politikası monetization'ı kapatabilir). Her videoda insan katkısı, çeşitlilik ve gerçek bir bakış açısı olmalı.
- **Sentetik/gerçekçi içerik açıklaması**: YouTube'un "altered or synthetic content" etiketi gerektiği yerde işaretlenecek.
- **Sağlık/finans tavsiyesi**: yetkinlik yoksa genel bilgi + feragat; yanlış bilgi riski.

Not: Bu politikalar zamanla değişir; yayından önce güncel YouTube/AdSense kuralları kontrol edilmeli.

---

## 7. Açık sorular (cevaba göre planı netleştiririm)
1. **Hedef**: Ana gelir mi, yan gelir/hobi mi? Aylık hedef?
2. **Kimlik**: Yüz/ses kullanmaya hazır mısın (yüzlü kanal, kendi ses klonu)?
3. **Dil/niş**: Hangi dil(ler) ve hangi nişlerle başlayalım (finans, tarih, e-bakım…)? Hangi dilleri yazıp kontrol edebiliyorsun?
4. **Bütçe**: Araç + GPU için aylık ne kadar? (Transkriptteki kişi ~400-800$/ay harcıyor.)
5. **Teknik**: Python mu, Node mu? Claude Code kullanacak mısın (kurgu/otomasyonu onunla mı kurarız)? GPU'n var mı, yoksa kiralama mı?
6. **Kapsam**: Önce hangi modülü kuralım — `analyzer` (rakip → format kılavuzu) en hızlı değer katar; öneririm onunla başlayalım.
