# Kanal açılış paketi — Gestern gab's das (@GesternGabsDas)

Bu dosyadaki metinleri YouTube Studio'ya kopyala-yapıştır. Genel kriterler ve adımlar: `docs/CHANNEL_SETUP.md`. Görseller: `art/` (ayrıntılar aşağıda). Metinler hedef dilde yazıldı (Almanca); yayından önce anadili konuşan birine okutmak iyi olur.

## 1) Görseller (`art/`)
| Dosya | Boyut | Nereye yüklenir |
|---|---|---|
| `avatar-800.png` | 800×800 | Studio → Özelleştirme → Marka → Profil resmi (YouTube 98×98 gösterir; daire kırpar) |
| `banner-2560x1440.png` | 2560×1440 (güvenli alan 1544×423 ortada) | Marka → Banner resmi |
| `watermark-300.png` | 300×300, şeffaf | Marka → Video filigranı (öneri: tüm video boyunca) |

Palet: kağıt, petrol, kiremit kırmızısı, hardal. Avatar: 'G' + kesme işareti (kırmızı damga). Yeniden üretmek için: `python3 scripts/make_channel_art.py`.

## 2) Kanal adı ve kullanıcı adı
- Ad: **Gestern gab's das**
- Handle: **@GesternGabsDas** (API'de boş göründü; Studio'da doğrula)

## 3) Açıklama (Hakkında) — kopyala (Almanca)
```
Gestern gab's das – Geschichten aus dem Alltag von damals.

Hier geht es um Läden, Berufe, Namen und Dinge, die früher jeder kannte und die heute fast verschwunden sind: der Tante-Emma-Laden an der Ecke, der Milchmann, der Versandhauskatalog, der Nachname, der etwas über deine Vorfahren verrät.

Wir recherchieren in Archiven und verlässlichen Quellen, erzählen ruhig und ohne Hektik und nennen die Quellen unter jedem Video. Bilder stammen aus Archiven (mit Quellenangabe) oder sind Illustrationen; am Computer erzeugte Bilder kennzeichnen wir.

Für alle, die sich gern erinnern – und für alle, die wissen wollen, wie es früher wirklich war.

Neue Videos erscheinen regelmäßig. Wenn dir ein Thema fehlt, schreib es in die Kommentare.

Kontakt: [E-Mail-Adresse]
```
`[E-posta]` yerine kanal için ayrı bir iş e-postası yaz (Studio → Hakkında → "İş talepleri için e-posta").
Önizlemede ilk ~125 karakter görünür; kısa tanıtım:
> Läden, Berufe, Namen und Alltag von damals – ruhig erzählt, mit Quellen. Neue Videos regelmäßig.

Kanal tanıtımının Türkçe karşılığı: Dükkânlar, meslekler, soyadları ve eskiden herkesin bildiği, bugün neredeyse kaybolmuş şeyler. Arşivlerde ve güvenilir kaynaklarda araştırma, sakin anlatım, her videonun altında kaynaklar. Görseller kaynak belirtilmiş arşivlerden veya illüstrasyon; bilgisayarla üretilenler işaretlenir.

## 4) Anahtar kelimeler (Studio → Ayarlar → Kanal → Temel bilgiler)
`früher, damals, Nostalgie, Alltag, Geschichte, 60er, 70er, 80er, DDR, BRD, Nachnamen, Berufe, Läden, Erinnerungen, Kindheit, Dokumentation`

## 5) Ülke/Bölge ve kitle
- **Ülke/Bölge:** gerçek ikamet ülken (Almanya/İtalya seçme; açıklama `docs/CHANNEL_SETUP.md`'de).
- **Kitle (Gelişmiş ayarlar):** "Hayır, bu kanal çocuklara özel değil".

## 6) Yükleme varsayılanları (Studio → Ayarlar → Yükleme varsayılanları)
- Kategori: Education (Bildung)
- Video dili: Deutsch
- Başlık/açıklama dili: Deutsch
- Görünürlük: **Özel** (yayına kendin alırsın)
- Etiketler: `früher, damals, Nostalgie, Alltag, Geschichte, 60er Jahre, 70er Jahre, Erinnerungen`
- Gerçekçi sentetik içerik beyanı: her videoda sor (`shared/checklists/compliance.md`).
- Yorumlar: "Uygunsuz olabilecek yorumları incelemeye tut".
- Açıklama şablonu:
```
{Kanca: 1-2 Sätze, was dich im Video erwartet}

Kapitel:
0:00 {Einleitung}
{Zeitstempel aus script.md}

Quellen:
- {Quelle 1 – URL}
- {Quelle 2 – URL}

Bildnachweise:
- {Bild – Urheber/Archiv – Lizenz}

Gefällt dir, was du siehst? Abonniere den Kanal und lass ein Like da – das hilft uns, dass mehr Menschen diese Geschichten finden.
Was fehlt auf der Liste? Schreib es in die Kommentare.

#früher #damals #nostalgie
```

## 7) Oynatma listeleri (içerik yayınlandıkça doldurulur)
1. Nachnamen und Herkunft
2. Läden und Marken von damals
3. Berufe, die es nicht mehr gibt
4. Kindheit und Alltag
5. Essen und Gaststätten

## 8) Sabitlenmiş yorum şablonu
> Quellen und Bildnachweise stehen in der Beschreibung. Was fehlt auf der Liste? Schreib es hier in die Kommentare – wir sammeln die Themen für die nächsten Videos.

## 9) İlk gün kontrol listesi
- [ ] Marka hesabıyla kanal oluşturuldu, ad ve handle girildi
- [ ] Avatar, banner, filigran yüklendi
- [ ] Hakkında, anahtar kelimeler, iş e-postası girildi
- [ ] Ülke/Bölge ve kitle ayarı yapıldı
- [ ] Yükleme varsayılanları girildi
- [ ] Telefon doğrulaması yapıldı (özel kapak ve 15 dk üstü video için)
- [ ] 2 adımlı doğrulama açık
- [ ] AdSense bağlama (YPP şartı sağlanınca): `docs/CHANNEL_SETUP.md`
