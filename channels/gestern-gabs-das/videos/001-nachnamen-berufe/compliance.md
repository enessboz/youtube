# Uyum — Nachnamen, die einen Beruf verraten: Müller, Schmidt, Wagner & Co.

Kontrol tarihi: 2026-10-18
Kapsam: İLK KESİT — Kanca, Einleitung, "1. Müller" (sessiz, altyazılı, stok klip + gravür). Girdiler: script.md (Kanca 13–24, Einleitung 26–47, Müller 51–81), shotlist.json, scenes.render.json (s001–s051), assets/SOURCES.md, assets/footage/*.json (kesitte kullanılan 19 klip), assets/mueller.jpg, research.md (lisans tablosu), factcheck.md, native-edit-notes.md, packaging.md.
Kapsam dışı (bu çalıştırmada kontrol edilmedi, tam video için açık): originality.md, şablon tekrarı (son 5 video), made-for-kids ayarı, kesit dışı bölümler (2–13, Kapanış).
Not: Klip kareleri ve gravür dosyası bu oturumda görsel olarak incelenemedi; görsel içerik kontrolleri (AI, kişi tanınabilirliği) metin/metadata kanıtına dayanır.

## Sonuç

**YAYINLANMAZ — ÜST AJANA YÜKSELT**

- KALDI: 3 madde (4c CC BY-SA kalıntısı ekranda; 6 Ebern/1860/1903 yer-yıl iddiasının stok klipe bağlanması; 7 altyazıda üretim notu sızıntısı)
- EMİN DEĞİLİM: 6 madde (2 final kapak; 3 AI-üretim kontrolü; 8a Dräger alıntısı; 8b "Mainz" atfı; 8d stok klipte kişi tanınabilirliği; 12 fact-check son turda yeniden çalıştırılmadı). Ayrıca 11 (originality), 13 (made-for-kids) kapsam dışı.
- GEÇTİ: 1, 4a, 4b, 5, 8c, 8e, 9, 10

---

## Madde madde kontrol

### 1. Sağlık / tıbbi / finans iddiası ve "doktorlar/devlet gizledi" kalıbı
- Durum: **GEÇTİ**
- Kanıt: scenes.render.json s001–s051 ve script.md 13–81'de sağlık, tıbbi veya finans iddiası yok. Müller bölümündeki Mühlengesetz 1957 ve "Prämie" tarihsel anlatım (factcheck satır 74: BVerfG 1 BvL 5/64 ile doğrulandı); tavsiye veya gizleme kalıbı yok.

### 2. Başlık ve kapak içeriği yansıtıyor (yanıltıcı vaat yok)
- Durum: **EMİN DEĞİLİM** (kesit başlık kartı GEÇTİ; yayın kapağı henüz yok)
- Kanıt: Başlık kartı scenes.render.json s006 "13 Namen – 13 Berufe / Müller, Schmidt, Wagner & Co." — script.md'deki 13 başlıkla uyumlu (Müller, Schmidt, Schneider/Schröder, Fischer, Weber, Wagner, Becker, Böttcher, Schäfer, Zimmermann, Meyer, Schulz, Richter). packaging.md yalnızca başlık iskeleti; kapak konsepti ve başlık metni boş. Final başlık/kapak yayın öncesi ayrıca kontrol edilmeli.

### 3. Gerçekçi sentetik görsel/ses varsa Studio'da "altered or synthetic content" beyanı
- Durum: **EMİN DEĞİLİM**
- Kanıt: Kesitte planlanan üretim görseli yok: tarihî görseller gemeinfrei Holzschnitt (mueller.jpg), kanal illüstrasyonu (shotlist "missing" listesi, ücretli üretim yapılmadı). Ses dosyası yok (audio/ yalnızca .gitkeep). Ancak 19 Pexels klibinin AI-üretimi olmadığı teyit edilemedi: footage json'larında AI/sentetik alanı yok ve kare incelemesi yapılamadı. AI-üretimi çıkarsa Studio'da beyan gerekir.
- Kullanılan 19 klip: 29853437, 5538183, 35794910, 11272050, 13617608, 6980366, 30117908, 7546434, 35378802, 5846389, 6765471, 7666907, 7235862, 34038695, 34760833, 6728035, 39353425, 34214782, 8190714.

### 4. Görsel/müzik lisans ve atıfları açıklamada
- 4a. Pexels klipleri — **GEÇTİ**
  - Kanıt: 19 kullanılan klibin her biri için assets/footage/*.json içinde `"license": "Pexels License (https://www.pexels.com/license/)"` ve sayfa/yazar kaydı; assets/SOURCES.md tablosunda sayfa, yazar, lisans satırları mevcut. Atıf zorunlu değil; yazar adları açıklamada verilmeli.
- 4b. Gravür (assets/mueller.jpg, Ständebuch 1568 "Molitor. Der Müller.") — **GEÇTİ**
  - Kanıt: SOURCES.md satır 5 (Deutsche Fotothek df_tg_0002113, Public domain); research.md bildirim tablosu satır 314 "Public domain (geprüft)" (Commons API kaydı). Bu oturumda Commons yeniden sorgulanmadı. Ekranda kaynak yazısı var: scenes.render.json s024–s051 pip "Ständebuch 1568 · Deutsche Fotothek".
- 4c. CC BY-SA görseller — **KALDI**
  - Kanıt (ekrana giden metin): scenes.render.json s050 caption `). Fotothek "Klotzmühle, Franz Müller beim Schärfen der Steine" (Günter Rapp,` ve s051 caption `CC BY-SA 3.0 DE). Ebern için fotoğraf yok…` — CC BY-SA ifadesi ekranda. Bu fotoğraf (Klotzmühle, CC BY-SA 3.0 DE) bu videoda kullanılmayacak (kural ve ÜST AJAN NOTU).
  - Kanıt (script): script.md satır 24 (Kanca SAHNE) Buschmühle "Fotothek df rp-c 0200059 … CC BY-SA 3.0 DE" ve satır 81 (Müller SAHNE) Klotzmühle CC BY-SA referansları hâlâ metinde. native-edit-notes.md satır 6–7 bunları "geçersiz" işaretliyor ama silinmemiş.
  - shotlist.json: CC BY-SA görsel referansı yok (olumlu).

### 5. Gerçek olay/kişiyi gösteren üretilmiş sahte arşiv görseli
- Durum: **GEÇTİ**
- Kanıt: Kesitte üretilmiş fotogerçekçi arşiv görseli yok. Tarihî görseller yalnızca PD gravür; stok klipler atmosfer olarak kullanılıyor (VISUALS.md kaynak hiyerarşisi 0).

### 6. Yanıltıcı görsel: stok klip belirli yer/yıl/kişi gibi sunuluyor mu (altyazıdaki yer/yıl iddiası)
- Durum: **KALDI**
- Kanıt: Ebern/Unterfranken/1860/1903/Achtzigerjahre altyazıları stok kliplerle eşleştirilmiş:
  - s045 "Ein Beispiel aus Unterfranken: die Stadtmühle in Ebern." — üzerinde pexels-6980366 (büyüteçle mektup okuyan kişi)
  - s046 "1860 baute dort der Stadtmüller Johann Aumüller an." — üzerinde pexels-30117908 (eski belge çeviren eller)
  - s047 "Ja, er hieß wirklich Aumüller. 1903 ersetzten zwei Turbinen das alte Holzrad." — üzerinde pexels-35794910 (kapalı mekânda değirmen işçisi)
  - s048 "Anfang der Achtzigerjahre stand die Mühle still." — üzerinde pexels-39353425 (su çarkı, hareketli)
- Plan ile çelişki: shotlist.json "missing" maddesi "Ebern su çarkı → türbin kanal illüstrasyonu; stok klip Ebern gibi etiketlenmemeli"; script.md satır 81 "Ebern için fotoğraf yok: kanal illüstrasyonu". Render bu planı uygulamamış; stok klip Ebern'in tarihine bağlanmış. VISUALS.md: "Stok görüntüde yer/ülke iddiası yapma."
- Diğer kesit sahneleri (Kanca, Einleitung, Müller'in genel kısmı) yer/yıl etiketi taşımıyor; GEÇTİ.

### 7. Altyazıda üretim notu / iç not sızıntısı
- Durum: **KALDI**
- Kanıt: scenes.render.json s023 caption `PM 26.04.2016 [Q2]. Stok klip atmosferi: eski el aletleri bir tezgâhta (çekiç, makas, ağ, rende). Rakam/sıralama grafiği YOK.]` — script SAHNE notu ekranda; s050 ve s051 (madde 4c) da aynı sızıntı. Hem izleyiciyi yanıltır hem iç kurgu notlarını yayına taşır.

### 8. Tanınabilir kişi / marka riski
- 8a. Yaşayan kişi alıntısı (Dr. Kathrin Dräger, Uni Freiburg) — **EMİN DEĞİLİM**
  - Kanıt: scenes.render.json s022 caption ve script.md satır 47 (SAHNE alıntı kartı) "Die 14 häufigsten Familiennamen … allesamt Familiennamen aus Berufsbezeichnungen." – Dräger, PM 26.04.2016 [Q2]. factcheck.md satır 29: alıntı yalnızca arama özetinde doğrulandı; PM/PDF açılmadı. Yaşayan, adıyla anılan kişinin alıntısı birincil kaynakta doğrulanmalı. Alıntıda "[sind]" ile değişiklik var.
- 8b. "Namenforscher aus Mainz und Freiburg sagen" (script.md satır 29; s008 caption) — **EMİN DEĞİLİM**
  - Kanıt: factcheck satır 29 yalnızca Freiburg PM'yi destekliyor; "Mainz" atfının kaynağı yok.
- 8c. Tarihî kişiler (Johann Aumüller 1860; Stadtmüller) — yaşayan değil; **GEÇTİ** (tek kaynak: factcheck satır 47, [TEK KAYNAK] infranken).
- 8d. Stok klipte görünen gerçek insanların tanınabilirliği ve model release durumu — **EMİN DEĞİLİM**
  - Kanıt: kareler bu oturumda incelenemedi; Pexels json'larında kişi/model bilgisi yok. Kesit metninde stok kliplerdeki kişiler adlandırılmıyor (scenes.render notu: 7546434 ve 11272050 gerçek kişi/yer gibi adlandırılmaz). Görüntüdeki kişiler yine de kare kare kontrol edilmeli.
- 8e. Marka/logo — **GEÇTİ** (kesit metninde marka adı yok).

### 9. Kimseyi karalama, nefret, yaşayan kişilere doğrulanmamış iddia
- Durum: **GEÇTİ** (kesitte karalama yok; yaşayan kişi iddiası yalnızca 8a/8b'de, orada EMİN DEĞİLİM olarak işaretli)

### 10. Kimsenin sesi izinsiz klonlanmadı
- Durum: **GEÇTİ** (ses üretimi yapılmadı; audio/ boş)

### 11. Özgünlük (originality.md)
- Durum: **EMİN DEĞİLİM** — bu çalıştırmada kapsam dışı; tam video için açık.

### 12. Fact-check: YANLIŞ ve DOĞRULANAMADI satırı kalmadı
- Durum: **EMİN DEĞİLİM**
- Kanıt: factcheck.md "ÜST AJANA YÜKSELT" (12 satır: YANLIŞ 4, DOĞRULANAMADI 8) ile bitti. Kesitle ilgili durum:
  - factcheck satır 34 "dreizehn dieser Namen" YANLIŞ — script satır 34'te düzeltilmiş ("dreizehn Berufs- und Amtsnamen"). Kapandı.
  - factcheck satır 61 ("ausnahmsweise einig") ve 63 ("starke Stellung") DOĞRULANAMADI — script'ten çıkarılmış, ama shotlist.json anchor'larında hâlâ duruyor (stale anchor). Ekranda yok.
  - factcheck satır 40 KISMEN "frühen neunzehnten Jahrhundert" önerisi uygulanmamış: scenes.render.json s034 ve script satır 63 hâlâ "Erst im frühen neunzehnten Jahrhundert…". Kaynakta kesin yasa tarihi yok.
  - Dräger/Mainz atfı: madde 8a–8b.
- factcheck yeniden çalıştırılmamış; yazar düzeltmelerinden sonra yeniden doğrulama gerekir.

### 13. Çocuklara yönelik içerik / made-for-kids
- Durum: **EMİN DEĞİLİM** — bu çalıştırmada kapsam dışı.

---

## Özet bulgular (ÜST AJAN İÇİN, düzeltme yapılmadı)

1. scenes.render.json s023, s050, s051 caption'larından üretim notu ve CC BY-SA ifadeleri çıkarılmalı.
2. script.md satır 24 (Kanca SAHNE, Buschmühle CC BY-SA) ve satır 81 (Müller SAHNE, Klotzmühle CC BY-SA) metinden silinmeli; native-edit-notes.md "geçersiz" notu yerine fiilî temizlik yapılmalı.
3. s045–s048: Ebern/1860/1903/1980er altyazılarının altındaki stok klipler kaldırılmalı; script ve shotlist "missing" maddesinin öngördüğü kanal illüstrasyonu (su çarkı → türbin) veya yer/yıl sözü taşımayan görsel kullanılmalı.
4. Dr. Kathrin Dräger alıntısı PM 26.04.2016 birincil kaynaktan doğrulanmalı; "Namenforscher aus Mainz und Freiburg" atfı yalnızca doğrulanan kurumla sınırlandırılmalı.
5. s034 "frühen neunzehnten Jahrhundert" factcheck önerisine göre değiştirilmeli.
6. shotlist.json anchor'ları script ile senkronlanmalı (stale: "ausnahmsweise einig", "starke Stellung").
7. Stok kliplerin AI-üretim ve kişi tanınabilirliği kare kare insan incelemesinden geçmeli; AI-üretim çıkarsa Studio beyanı eklenmeli.
8. Düzeltmelerden sonra kesit yeniden render edilmeli; compliance ve factcheck yeniden çalıştırılmalı.

## Son karar

**YAYINLANMAZ — ÜST AJANA YÜKSELT.** KALDI: 4c, 6, 7. EMİN DEĞİLİM: 2, 3, 8a, 8b, 8d, 12 (kapsam dışı: 11, 13).
