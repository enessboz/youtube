# Kanal açılış paketi — Quando Eravamo Noi (@QuandoEravamoNoi)

Bu dosyadaki metinleri YouTube Studio'ya kopyala-yapıştır. Genel kriterler ve adımlar: `docs/CHANNEL_SETUP.md`. Görseller: `art/` (ayrıntılar aşağıda). Metinler hedef dilde yazıldı (İtalyanca); yayından önce anadili konuşan birine okutmak iyi olur.

## 1) Görseller (`art/`)
| Dosya | Boyut | Nereye yüklenir |
|---|---|---|
| `avatar-800.png` | 800×800 | Studio → Özelleştirme → Marka → Profil resmi (YouTube 98×98 gösterir; daire kırpar) |
| `banner-2560x1440.png` | 2560×1440 (güvenli alan 1544×423 ortada) | Marka → Banner resmi |
| `watermark-300.png` | 300×300, şeffaf | Marka → Video filigranı (öneri: tüm video boyunca) |

Palet: krem, mürekkep mavisi, terracotta, zeytin. Avatar: 'Q' + küçük zeytin. Yeniden üretmek için: `python3 scripts/make_channel_art.py`.

## 2) Kanal adı ve kullanıcı adı
- Ad: **Quando Eravamo Noi**
- Handle: **@QuandoEravamoNoi** (API'de boş göründü; Studio'da doğrula)

## 3) Açıklama (Hakkında) — kopyala (İtalyanca)
```
Quando Eravamo Noi – storie di vita quotidiana di una volta.

Parliamo di botteghe, mestieri, cognomi e di cose che un tempo conoscevano tutti e che oggi sono quasi scomparse: la bottega sotto casa, l'arrotino, il lattaio, il cognome che racconta da dove veniamo.

Facciamo ricerche in archivi e fonti affidabili, raccontiamo con calma e citiamo le fonti sotto ogni video. Le immagini provengono da archivi (con indicazione della fonte) o sono illustrazioni; le immagini generate al computer vengono segnalate.

Per chi ama ricordare, e per chi vuole scoprire com'era davvero una volta.

Nuovi video con regolarità. Se manca un argomento, scrivilo nei commenti.

Contatti: [indirizzo e-mail]
```
`[E-posta]` yerine kanal için ayrı bir iş e-postası yaz (Studio → Hakkında → "İş talepleri için e-posta").
Önizlemede ilk ~125 karakter görünür; kısa tanıtım:
> Botteghe, mestieri, cognomi e vita di una volta – raccontati con calma, con le fonti. Nuovi video con regolarità.

Kanal tanıtımının Türkçe karşılığı: Dükkânlar, meslekler, soyadları ve eskiden herkesin bildiği, bugün neredeyse kaybolmuş şeyler. Arşivlerde ve güvenilir kaynaklarda araştırma, sakin anlatım, her videonun altında kaynaklar. Görseller kaynak belirtilmiş arşivlerden veya illüstrasyon; bilgisayarla üretilenler işaretlenir.

## 4) Anahtar kelimeler (Studio → Ayarlar → Kanal → Temel bilgiler)
`nostalgia, una volta, anni 60, anni 70, anni 80, ricordi, mestieri scomparsi, cognomi, botteghe, infanzia, vita quotidiana, storia`

## 5) Ülke/Bölge ve kitle
- **Ülke/Bölge:** gerçek ikamet ülken (Almanya/İtalya seçme; açıklama `docs/CHANNEL_SETUP.md`'de).
- **Kitle (Gelişmiş ayarlar):** "Hayır, bu kanal çocuklara özel değil".

## 6) Yükleme varsayılanları (Studio → Ayarlar → Yükleme varsayılanları)
- Kategori: Education (Istruzione)
- Video dili: Italiano
- Başlık/açıklama dili: Italiano
- Görünürlük: **Özel** (yayına kendin alırsın)
- Etiketler: `una volta, nostalgia, ricordi, anni 60, anni 70, mestieri scomparsi, cognomi, botteghe`
- Gerçekçi sentetik içerik beyanı: her videoda sor (`shared/checklists/compliance.md`).
- Yorumlar: "Uygunsuz olabilecek yorumları incelemeye tut".
- Açıklama şablonu:
```
{Gancio: 1-2 frasi su cosa troverai nel video}

Capitoli:
0:00 {Introduzione}
{Timestamp da script.md}

Fonti:
- {Fonte 1 – URL}
- {Fonte 2 – URL}

Crediti delle immagini:
- {Immagine – autore/archivio – licenza}

Ti piace quello che vedi? Iscriviti al canale e lascia un mi piace: ci aiuta a far conoscere queste storie.
Cosa manca nell'elenco? Scrivilo nei commenti.

#unavolta #nostalgia #ricordi
```

## 7) Oynatma listeleri (içerik yayınlandıkça doldurulur)
1. Cognomi e origini
2. Botteghe e marchi di una volta
3. Mestieri scomparsi
4. Infanzia e vita quotidiana
5. Cucina e osterie

## 8) Sabitlenmiş yorum şablonu
> Fonti e crediti delle immagini sono nella descrizione. Cosa manca nell'elenco? Scrivilo qui nei commenti: raccogliamo gli argomenti per i prossimi video.

## 9) İlk gün kontrol listesi
- [ ] Marka hesabıyla kanal oluşturuldu, ad ve handle girildi
- [ ] Avatar, banner, filigran yüklendi
- [ ] Hakkında, anahtar kelimeler, iş e-postası girildi
- [ ] Ülke/Bölge ve kitle ayarı yapıldı
- [ ] Yükleme varsayılanları girildi
- [ ] Telefon doğrulaması yapıldı (özel kapak ve 15 dk üstü video için)
- [ ] 2 adımlı doğrulama açık
- [ ] AdSense bağlama (YPP şartı sağlanınca): `docs/CHANNEL_SETUP.md`
