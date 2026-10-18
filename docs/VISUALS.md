# Görsel strateji: rakiplerden farklı, kaliteli, dürüst

**Hedef:** rakiplerin ortak "AI nine + sarı-siyah kapak + sepya" görünümünden kökten farklı, tutarlı ve kaliteli bir görsel dil. Bu fark kaliteden ve sanat yönünden gelir; yapay zeka kullanımını **gizlemekten** gelmez. Gerçekçi sentetik içerik YouTube'da beyan edilir ve sahte "tarihî fotoğraf" üretilmez. Hem politika hem izleyici güveni için, hem de uzun vadede daha iyi bir markadır.

## Kaynak hiyerarşisi (yukarıdan aşağı)
0. **Gerçek hareketli görüntü (ana omurga):** stok video (Pexels/Pixabay, ticari kullanım serbest; `pipeline/footage/footage.py`) ve lisansı doğrulanmış arşiv filmi. Video **hareketli planlardan** oluşur (3-6 sn'lik çekimler), fotoğraf/gravür yalnızca vurgu, belge ve karşılaştırma için; tüm videoyu fotoğraf slayt gösterisine çevirmeyiz. Stok görüntüde yer/ülke iddiası yapma (klipin nerede çekildiği bilinmiyor). Tüm klipler kanalın renk düzeltmesi, film greni ve vinyetiyle aynı görünüme oturtulur (`pipeline/render/src/scenes/Clip.tsx`).
1. **Gerçek arşiv** fotoğraf/film (lisansı doğrulanmış; atıf zorunluysa açıklamada). Ülkeye özgü kaynaklar `channels/<kanal>/brand/visual-style.md`'de.
2. **Belge ve efemera taramaları:** katalog sayfası, etiket, pul, bilet, gazete başlığı (telif durumu her öğe için kontrol edilir).
3. **Grafik:** harita, zaman çizelgesi, sayaç, tipografi, fiyat etiketi animasyonları.
4. **Kanalın sabit illüstrasyon stili:** Almanca kanalda serigrafi/yarım ton, İtalyanca kanalda suluboya ve kâğıt kolaj. Fotogerçekçi değil, tanınabilir bir sanat yönü.
5. **Fotogerçekçi üretim:** yalnızca başka yol yoksa, hedef ≤%25 üretim payı içinde, beyanlı; gerçek bir olayı/kişiyi gösteriyormuş gibi sunulmaz.

## "AI sosu" göstergeleri ve kaçınma
| Gösterge | Önlem |
|---|---|
| Plastik cilt, aynı yüz tipi, bozuk eller | Yüz yerine nesne, belge, mekân, siluet; insan gerekiyorsa illüstrasyon |
| Hep aynı sepya/altın ışık | Kanalın paleti (visual-style.md); aynı filtreyi art arda uygulama |
| Bozuk veya uydurma yazı | Yazıları görselde üretme; Remotion'da gerçek tipografiyle ekle |
| Her sahne aynı hareket (yavaş zoom) | Hareket sözlüğünü çeşitlendir: parallax, harita çizimi, sayaç, kesme |
| Her video aynı kapak şablonu | Kanal kapak sistemi + A/B; sarı-siyah genel şablon yasak |
| Söylenenle uyuşmayan görsel | `scenes.json`'da her sahne `text_anchor` ile cümleye bağlı |

## Hareket (video) üretimi
Image-to-video modelleri sadece kısa vurgu planlarında (ör. dumanlı mutfak, yağmur). Ana hareket 2.5D katman parallax'ı ve Remotion animasyonlarıdır: daha ucuz, tutarlı ve "yapay video" tuhaflıklarından uzak.

## Yapma
- Gerçek bir olayı/kişiyi tasvir eden sahte arşiv fotoğrafı üretip "tarihî" diye sunmak.
- Lisansı doğrulanmamış arşiv/katalog/reklam görselleri.
- İki kanal arasında palet, sunucu karakteri veya şablon paylaşmak.
- AI içerik beyanını atlamak.

## Kalite çıtası (ilk 3 video)
İlk 3 videoda görsel plan opus ile hazırlanır, kullanıcı stil ve kaynakları onaylar; çıta oradan belirlenir.
