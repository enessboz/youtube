# Kanal kurulumu: hesap, ülke ve kriterler

Kaynaklar: YouTube Yardım (Partner Programı uygunluğu, kanal ayarları, kanal oluşturma, marka görselleri; erişim 2026-10). Ülkeye ve politikaya göre değişen şeyler işaretlendi: kurmadan önce Studio'da kendi hesabında doğrula.

## Yeni üyelik (Google hesabı) açmak gerekir mi?
**Hayır, zorunlu değil.** Yardım sayfasına göre ikinci bir kanalı **Marka Hesabı (Brand Account)** olarak oluşturursun: Ayarlar → Hesap → "Kanal ekle veya yönet" → "Yeni kanal oluştur". Bu sana Google hesabından farklı bir kanal adı verir ve birden çok yönetici/sahip eklemene izin verir. Sayfa ayrı Google hesabı gerektiğini söylemiyor.
- **Her marka hesabında en fazla bir kanal** olur: iki kanal için iki marka hesabı aç.
- **Önerim:** tek, **gerçek kimliğinle** bir Google hesabı (istersen bu iş için ayrı bir hesap, ama yine senin gerçek kimliğin). Sahte kimlik, başkasının adıyla hesap veya "bağlantıyı gizleme" tavsiyelerini uygulamıyoruz (PLAN.md §6): kanallar kapanırsa risk zaten AdSense'te toplanır; çözüm kanal sayısını az tutmak ve geliri çeşitlendirmek.
- **Önce:** hesapta **2 adımlı doğrulama** açık olmalı (Partner Programı şartı).

## Ülke/Bölge ayarı
Studio → Ayarlar → Kanal → Temel bilgiler → **Ülke/Bölge**. Yardım sayfası: *"Eligibility for the YouTube Partner Program is based on the country/region setting you choose here."*
- **Gerçek ikamet ülkeni seç.** Almanya/İtalya seçme: hedef kitle ülke ayarıyla değil, **dil ve içerikle** belirlenir; yanlış ülke seçmek Partner Programı uygunluğunu ve ödeme/vergi sürecini (AdSense adresi, vergi bilgisi) bozabilir.
- Partner Programı **ülkeye bağlı**: hesabının ülkesinde mevcut olup olmadığını YouTube'un güncel "YPP uygun ülkeler" listesinden kontrol et (bu oturumda listeyi okuyamadım, Türkiye'nin dahil olduğunu doğrulamadım).
- Ücret ve vergi: AdSense ödeme profili adın/adresin gerçek olmalı (banka adıyla eşleşmeli), vergi bilgisi istenirse doldurulmalı (ayrıntı için AdSense/YouTube'un vergi sayfalarına bak; ben doğrulamadım).

## Önemli kriterler (kontrol listesi)
**Hesap ve güvenlik**
- [ ] 2 adımlı doğrulama açık
- [ ] Telefon doğrulaması (özel kapak resmi ve 15 dakikadan uzun video gibi özellikler için istenir; Studio'da doğrula)
- [ ] Kanal başına marka hesabı, gerçek kimlik, iş e-postası
- [ ] Hesap kurtarma bilgileri güncel; yönetici/sahip yalnızca senin kontrolünde

**Kanal ayarları**
- [ ] Ülke/Bölge = gerçek ikamet ülken
- [ ] Kitle: "çocuklara özel değil" (Gelişmiş ayarlar → Kitle). Seçilmezse kısıtlamalar olur
- [ ] Yükleme varsayılanları: dil, kategori, özel görünürlük (`channels/<kanal>/launch/README.md`)
- [ ] Marka görselleri: profil (PNG/JPG, ≤15 MB, 98 px gösterilir), banner (2560×1440 önerilen, min 2048×1152, güvenli alan 1235×338 min boyutta, ≤6 MB), filigran (≥150×150, kare, <1 MB)

**Partner Programı (para kazanma)**
- Standart eşik: **1.000 abone + 4.000 geçerli genel izlenme saati (son 12 ay)** veya 1.000 abone + 10 milyon geçerli Shorts izlenmesi (son 90 gün). Aktif Community Guidelines ihlali (strike) olmamalı.
- **Erken erişim katmanı** (üyelik, Super Chat gibi hayran finansmanı için): 500 abone + son 90 günde 3 genel yükleme + 3.000 izlenme saati (12 ay) veya 3 milyon Shorts izlenmesi (90 gün). Başlangıçta sınırlı ülkelerde açıldı (ABD, İngiltere, Kanada, Tayvan, Güney Kore) ve zamanla genişleyeceği söylendi: **kendi ülkende geçerli mi Studio'da bak.** Bizim planda Katıl zaten 10K aboneden sonra.
- **AdSense:** Partner Programı'na kabul için bir aktif AdSense for YouTube hesabı kanala bağlanır (Studio'dan kurulur).
- Bir kanalda 6 ay veya daha uzun süre hiç video/gönderi olmazsa YouTube parayı kapatabilir. Kanalları sürekli beslemek gerek.
- Toplu/özgün olmayan içerik politikaları kanalı bütün olarak değerlendirir: `shared/checklists/originality.md`.

**Sonraki aşama (kod): YouTube API**
- Google Cloud'da proje, **YouTube Data API v3** ve **YouTube Analytics API** etkin; OAuth istemcisi (masaüstü uygulaması). Anahtarı (`YOUTUBE_API_KEY`) zaten kullanıyoruz; yükleme ve analitik için ayrıca OAuth gerekir.
- OAuth uygulaması "Testing" durumundayken yenileme belirteçleri kısa sürede (yaklaşık 7 gün) dolabilir: üretime almak veya yenilemeyi planlamak gerekebilir (doğrula).
- Yükleme ilk testte **özel** yapılır; `status.publishAt` zamanlaması test edilir (`docs/TOOLS.md`).

## Kurulum sırası (öneri)
1. Google hesabı: 2 adımlı doğrulama, kurtarma bilgileri, iş e-postası.
2. Kanal A (Marka Hesabı) → `channels/gestern-gabs-das/launch/README.md` adımları.
3. Kanal B (ayrı Marka Hesabı) → `channels/quando-eravamo-noi/launch/README.md` adımları.
4. Telefon doğrulaması, kitle ayarı, yükleme varsayılanları.
5. Boş kanallarda içerik yok iken **hiçbir şey yayınlama**; ilk video hazır olunca özel yükle, kontrol et, yayına al.
6. AdSense bağlama: eşik sağlandığında.
