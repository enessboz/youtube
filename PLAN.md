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

## 7. Kanal planı v2 (veriye dayalı — nişe tarama sonuçlarından)

Kaynak: `pipeline/niche_scout` taraması, elle toplanan ekran görüntüleri (DE/FR/IT/ES) ve `handles.py` ile ölçülen 9 rakip kanal.
Güvenilirlik notu: Ölçülen kanallar **hayatta kalan, hit almış** kanallar; hiç tutmayıp kapananlar örneklemde yok. Rakamlar iyimser, eşikler **başlangıç varsayımıdır**, 20 video sonrası kendi verimizle güncellenir.

### 7.0 Veri özeti (karar dayanağı)
| Bulgu | Kaynak |
|---|---|
| Format kanıtlanmış: "N tane (kaybolan şey), 20-35 dk liste" her dilde kopyalanıyor | DE/FR/IT/ES taramaları |
| 100K+ video oranı ≈ %5 (≈ 20 videoda 1), medyan çoğu kanalda 1,4K-8K | `handles.py` (n≥50 video olan kanallar) |
| En güçlü kanal: Vergessene Deutsche Küche — 4 ayda 59 video, medyan 25K, %28'i ≥50K | `handles.py` |
| Yemek en kalabalık; **soyadları, kaybolan dükkân/markalar** yemek dışı hit'lerin kaynağı (DE 384K, IT 393K/278K, ES 92K) | `handles.py` |
| **Meslekler ve günlük yaşam**: DE'de yerel arz ince (en iyi 1-2K, biri 65K tarih odaklı); IT'de dublajlı Amerikan içerik boşluğu dolduruyor | ekran görüntüleri |
| Hit'li kanallar da durabiliyor (Deutschland Früher: 554K/395K/251K hit, 10K abone, 164 gündür video yok) | `handles.py` |
| Hit abone getirmiyor (Fogones del Recuerdo: 69K izlenme → 677 abone) | API |
| İspanyolca tavanı en yüksek (1-2,6M) ama en kalabalık ve sağlık iddialı içerik çok | ekran görüntüleri |

### 7.1 Karar özeti (Faz 0)
1. **İki kanal:** Almanca ve İtalyanca. İspanyolca ertelendi (3. slot rezerve), Fransızca tarih rafa kalktı, Portekizce test edilemedi.
2. **Ortak konu hattı, ayrı sunum:** konu iskeleti ortak, içerik **ülkeye özgü araştırma** (çeviri değil). Her kanalın kendi sesi, renk paleti, bölüm yapısı ve kapak dili var (§6 toplu-üretim riski).
3. **Avatar yok.** Anlatıcı sesi + dönem görselleri; marka kimliği için kanal başına **çizim sunucu karakteri** (fotogerçekçi değil). Avatar, kazanan kanalda sonra A/B ile denenir. Gerçekçi AI görseller YouTube'un sentetik içerik beyanıyla işaretlenir.
4. **Katıl / ürün hattı 10K aboneden sonra değerlendirilir.** Rakiplerde görülen gelir yolu e-kitap/tarif paketi (açıklamadaki bağlantı); satış verisi elimizde yok.
5. **Abone/beğeni çağrısı zorunlu** (7.6).
6. **Araçlar:** önce ince betikler + kütüphaneler; başka repo klonu gerekirse tek tek onayla (oturum yalnızca `enessboz/youtube`'a bağlı).

### 7.2 Kanal konseptleri

#### Kanal A — Almanca
- **Konsept:** Almanya'nın (Doğu + Batı) 50'li-80'li yıllar günlük yaşamı: **soyadları, kaybolan dükkânlar ve markalar, meslekler, çocukluk eşyaları**. Yemek toplamın en çok %15'i.
- **Kitle:** 55+ Almanca konuşan; nostalji, "bizim zamanımızda" duygusu. Almanca kitle abone olmaya isteksiz (transkript) → çağrı gerekçeli olmalı.
- **Format karması (şablon tekrarını kırmak için):** %60 liste (15-25 madde), %25 tek konu derin anlatı, %15 karşılaştırma (Doğu/Batı, kuzey/güney). Süre 20-30 dk.
- **Ton:** sakin, sıcak, yavaş anlatım; kısa cümle; dönem müziği hafif.
- **Rakip konumu:** "Vergessene…", "Früher…" kalıbından kaçın; başlıklar özgün.

#### Kanal B — İtalyanca
- **Konsept:** İtalya'nın 50'li-70'li yıllar günlük yaşamı: **cognomi, bottega (dükkân), mestieri scomparsi, çocukluk/oyuncak**, TV ve aile ritüelleri. Yemek en çok %15-20.
- **Boşluk:** İtalyanca aramalarda "mestieri scomparsi", "giocattoli anni 60-70" sonuçlarını dublajlı Amerikan kanallar dolduruyor; yerel içerik yok veya çok küçük. **Varsayım (kanıtlanmadı):** gerçekten İtalya'ya özgü içerik bu boşlukta daha iyi tutar.
- **Format karması:** Kanal A ile aynı oranlar, ama farklı bölüm yapısı ve farklı ses.
- **Dikkat:** Tavan Almanya'dan düşük olabilir (yerel hit'ler 100-393K, medyanlar 1-4K).

#### Ortak üretim kuralları (her video için)
- **Özgün katkı kontrol listesi (video çıkmadan):** ≥2 bağımsız kaynak; ≥1 yerel ayrıntı (şehir/bölge/isim) hiçbir rakipten kopyalanmamış; tarih, marka ve isim doğrulaması (LLM hatası riski yüksek); başlık ve kapak rakiplerden birebir değil.
- **Dil kontrolü:** Anadili konuşan bir kişi senaryoyu okur (freelance düzeltmen). Bütçe kalemi.
- **Sağlık iddiası yok:** "Doktorlar yasakladı", "güçlendirir" kalıpları yasak.
- **Sentetik içerik:** gerçekçi AI görseller beyan edilir.

### 7.3 Ses
- **Birincil:** ElevenLabs. Her kanal için **Voice Design** ile kütüphanede olmayan ayrı bir ses.
- **Seçim yöntemi:** Her dil için 3 aday ses, aynı 60 sn'lik metin, anadili konuşan (mümkünse 55+) bir kişiye kör dinletme. Hız yavaş, ton sıcak.
- **Yedek:** Azure veya Google Cloud TTS nöral sesler (maliyet ve ticari koşulları kullanmadan önce doğrula).
- **Kural:** yaygın hazır kütüphane seslerini kullanma; kimsenin sesini izinsiz klonlama (§6).

### 7.4 İlk 20 video — konu listeleri
Etiketler: **[kanıt]** rakipte hit aldı, **[boşluk]** yerel arz ince, **[deneme]** benim hipotezim, **[kalabalık]** rakip çok. Başlıklar çalışma başlığıdır, yayında özgünleştirilir. Marka/isim iddiaları yayından önce doğrulanır.

**Kanal A — Almanca**
| # | Çalışma başlığı | Tür | Etiket |
|---|---|---|---|
| 1 | Nachnamen, die einen Beruf verraten: Müller, Schmidt, Wagner & Co. | liste | kanıt |
| 2 | Nachnamen im Norden und im Süden: Woher dein Name kommt | karşılaştırma | kanıt |
| 3 | Nachnamen, die bald aussterben | liste | deneme |
| 4 | Der Tante-Emma-Laden: Was es dort gab und warum er verschwand | derin | kanıt |
| 5 | Versandhaus-Kataloge: Quelle, Neckermann & Otto | derin | deneme |
| 6 | Elektromarken der 60er-80er: Grundig, Saba, Nordmende & Co. | liste | kanıt |
| 7 | Kaufhäuser, die jede Stadt kannte | liste | deneme |
| 8 | Berufe, die es nicht mehr gibt: Milchmann, Kohlenträger, Telefonistin | liste | boşluk |
| 9 | Frauenberufe der 50er | liste | boşluk |
| 10 | Aussterbende Handwerke: Stellmacher, Böttcher & Co. | liste | boşluk |
| 11 | Ein Tag auf der Zeche: Alltag im Ruhrgebiet | derin | deneme |
| 12 | Spielzeug der 60er: Ost und West im Vergleich | karşılaştırma | kanıt |
| 13 | Alltag in der DDR: Dinge, die jeder hatte | liste | kanıt/kalabalık |
| 14 | Das Wohnzimmer der 70er: Schrankwand, Kachelofen, Röhrenfernseher | liste | deneme |
| 15 | Schulalltag in den 60ern | liste | boşluk |
| 16 | Der Sonntag in den 70ern | derin | deneme |
| 17 | Gaststätten-Klassiker der 70er | liste | kanıt/kalabalık |
| 18 | Die Bäckerei von früher: Brote und Gebäck, die verschwanden | liste | deneme |
| 19 | Kindheit auf der Straße: Spiele ohne Handy | liste | deneme |
| 20 | Dorfleben in den 60ern | derin | deneme |

**Kanal B — İtalyanca** (çeviri değil, İtalya'ya özgü araştırma)
| # | Çalışma başlığı | Tür | Etiket |
|---|---|---|---|
| 1 | Cognomi che raccontano un mestiere: Ferrari, Fabbri, Sarto… | liste | kanıt |
| 2 | Cognomi del Nord e del Sud: da dove vengono | karşılaştırma | kanıt |
| 3 | Cognomi che stanno scomparendo | liste | deneme |
| 4 | La bottega sotto casa: negozi di quartiere che non ci sono più | derin | boşluk |
| 5 | Marchi italiani spariti: elettrodomestici, auto, giocattoli | liste | deneme |
| 6 | I grandi magazzini d'una volta | derin | deneme |
| 7 | Il cinema di quartiere | derin | deneme |
| 8 | Carosello: la pubblicità che univa gli italiani | derin | deneme |
| 9 | Mestieri scomparsi in Italia: arrotino, lattaio, ombrellaio, spazzacamino | liste | boşluk |
| 10 | Mestieri delle donne negli anni '50 | liste | boşluk |
| 11 | I mestieri ambulanti | liste | boşluk |
| 12 | La vita del mezzadro: una giornata in campagna | derin | deneme |
| 13 | Giocattoli italiani anni '60-'70 | liste | boşluk |
| 14 | Giochi da cortile | liste | deneme |
| 15 | La vita nel cortile e sul ballatoio | derin | deneme |
| 16 | La domenica degli italiani negli anni '60 | derin | deneme |
| 17 | La televisione in bianco e nero: volti e programmi | liste | deneme |
| 18 | L'estate al mare negli anni '60 | derin | deneme |
| 19 | Piatti poveri della cucina contadina | liste | kanıt |
| 20 | Osterie e trattorie di una volta | liste | deneme |

**Yayın temposu:** İlk 4 hafta kanal başına 3 video/hafta (12 video), ardından tempo kararı (7.5). Hazır tampon: en az 3 video. 20 video ≈ 7. hafta.

### 7.5 Kill / ölçekle kuralları (başlangıç eşikleri)
Bu bölüm §4'teki "7 günde karar" kuralının yerine geçer, çünkü haftada 3 videoda 7 gün = 3 veri noktası (çok az) ve ilk 5 günlük veri gecikmeli. **Değerlendirme: her videoyu 14. günde ölç.** Eşikler ölçülmüş benchmark'lardan (hayatta kalan kanallar) kaba çıkarıldı; 20 video sonra kendi verimizle yeniden kalibre edilir.

| Kontrol noktası | Ölçüt | Karar |
|---|---|---|
| **Video 10** (≈5. hafta) | medyan <300 izlenme **veya** CTR <%2 | KES değil; **paketleme turu**: başlık/kapak revizyonu, 1 kez |
| | aksi halde | devam |
| **Video 20** (≈7-8. hafta) | medyan <1K **ve** en iyi video <10K **ve** abone <300 | **KES** |
| | medyan 1-3K **veya** en iyi video 10-50K | **İZLE**, +10 video |
| | medyan ≥5K **veya** en iyi ≥100K **veya** abone ≥1.000 | **ÖLÇEKLE** (tempo/format) |
| **Video 40** | 1.000 abone / 4.000 saat eşiğine uzak ve medyan <3K | **KES** veya konsept değiştir |

Referans: ölçtüğümüz en iyi kanal 4 ayda medyan 25K'ya çıktı; Fogones (9 video, 677 abone, bırakılmış) "İZLE" bandında kalırdı. Şunlar **sabit durdurma** sebepleridir: politika ihlali/uyarısı veya gelir kısıtı → **iki kanalda da yüklemeyi dondur**, şablonu denetle; bütçe tavanı aşımı.
Her hafta doldurulacak tablo: video, 14. gün izlenme, CTR, ort. izlenme süresi, 1.000 izlenmede abone, dönüşüm notu.
İki kanalla "model işe yarıyor" demek için örnek az (n=2); §4'teki %40 portföy eşiği burada anlamsız, kanıt olarak kullanma.

### 7.6 Abone ve beğeni çağrısı (kurgu şablonu)
- **1. çağrı:** girişten sonra (30-60. sn), tek cümle, gerekçeli ("her hafta ... anlatıyorum").
- **2. çağrı:** videonun ortasında, en güçlü maddeden hemen sonra, kısa.
- **3. çağrı:** sonda, "sıradaki video" ile birlikte son ekran.
- Büyük, net animasyonlu buton (yaşlı izleyici), tekrar spam gibi olmasın.
- Metrik: **1.000 izlenmede abone**; çağrı metni ve yerleşimi buna göre A/B edilir.
- Yasak: abone karşılığı vaat, yanıltıcı çağrı.

### 7.7 Kanal adları
**Kriterler:** rakip kalıplarından farklı ("Vergessene…", "Früher", "Ricordi…" değil), hatırlanır, 2-3 kelime, ses ve kimlikle uyumlu, handle boş.
Handle kontrolü (`forHandle`, 1 birim): boş görünenler uygun, ancak **kanalı açarken YouTube Studio'da tekrar doğrulanmalı** ve benzer isimli kanallar elle aranmalı.

| Dil | Aday (handle durumu) |
|---|---|
| DE | **Gestern gab's das** (@GesternGabsDas boş) ← öneri; Unser Damals (boş); Zeitfenster Alltag (boş); Damals im Land (boş); Das war mal Deutschland (boş). Dolu: Alltag von gestern, Spuren des Alltags |
| IT | **Quando Eravamo Noi** (@QuandoEraviamoNoi boş) ← öneri; Bottega del Ricordo (boş; dükkân/meslek konseptine çok uygun); Quando Ero Bambino (boş); Ieri in Bottega (boş); Via del Ricordo (boş). Dolu: Il Tempo di Ieri, L'Italia di Ieri |

Karar kullanıcıda; marka tescili/benzer isim araştırması kullanıcı tarafında yapılacak.

### 7.8 Sonraki işler
1. Ses seçimi (7.3): 3 aday × 2 dil, kör dinleme.
2. Kanal adlarını kesinleştir, kanalları aç (§6 hesap yapısı: tek marka çatısı, gerçek kimlik).
3. İlk video uçtan uca (Faz 2): Kanal A video #1 (soyadları).
4. Anadili düzeltmen bul (bütçe kalemi).
5. 3. kanal slotu için İspanyolca'ya (İspanya'ya özgü, sağlık iddiasız) ikinci tur.

---

## 8. Açık sorular (cevaba göre planı netleştiririm)
1. **Hedef**: Ana gelir mi, yan gelir/hobi mi? Aylık hedef?
2. **Kimlik**: Yüz/ses kullanmaya hazır mısın (yüzlü kanal, kendi ses klonu)?
3. **Dil/niş**: Hangi dil(ler) ve hangi nişlerle başlayalım (finans, tarih, e-bakım…)? Hangi dilleri yazıp kontrol edebiliyorsun?
4. **Bütçe**: Araç + GPU için aylık ne kadar? (Transkriptteki kişi ~400-800$/ay harcıyor.)
5. **Teknik**: Python mu, Node mu? Claude Code kullanacak mısın (kurgu/otomasyonu onunla mı kurarız)? GPU'n var mı, yoksa kiralama mı?
6. **Kapsam**: Önce hangi modülü kuralım — `analyzer` (rakip → format kılavuzu) en hızlı değer katar; öneririm onunla başlayalım.
