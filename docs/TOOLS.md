# Araçlar, kütüphaneler ve repolar

**Karar:** başka repo klonlamıyoruz; resmi/yaygın kütüphaneleri paket olarak kuruyoruz ve ince betikler yazıyoruz. Lisansları ve güncel sürümleri kurulumdan önce doğrula (aşağıdaki lisans notları hafızamdan, doğrulanmadı).

| İş | Seçim | Kurulum | Not |
|---|---|---|---|
| YouTube yükleme, zamanlama, metadata | `googleapis/google-api-python-client` + `google-auth-oauthlib` | `pip` | `videos.insert` + `status.publishAt`; küçük bir `pipeline/publisher` betiği yazacağız. Üçüncü taraf `youtube-skill` benzeri hazır depoları kullanmıyoruz (küçük, denetlenmemiş). |
| Analytics | YouTube Analytics API (aynı istemci) | `pip` | 14. gün metrikleri için |
| Transkript (rakip analizi) | `yt-dlp`, `youtube-transcript-api` | `pip` | Rakipten format öğrenmek için; içerik kopyalamak için değil |
| Altyazı hizalama (gerekirse) | `faster-whisper` | `pip` (büyük, ihtiyaç olursa) | Senaryo zaten elimizde; çoğu durumda SRT'yi senaryo ve ses süresinden üretiriz |
| Ses | ElevenLabs Python SDK | `pip install elevenlabs` | `ELEVENLABS_API_KEY`; `docs/BUDGET.md` |
| Kurgu/render | **Remotion** (React) + **ffmpeg** | `npm` + sistem ffmpeg | Kodla yeniden üretilebilir kurgu; Remotion'ın ticari lisans koşulunu doğrula |
| Elle son kontrol / ilk şablon | **DaVinci Resolve** (ücretsiz sürüm) | kullanıcının bilgisayarı | İlk videonun ritmini elle kur, sonra Remotion şablonuna çevir |

## YouTube API gerçekleri (doğrulanacaklar)
- Google'ın `videos.insert` sayfası: çağrı başına **1 birim, Video Uploads kovasında günde 100 çağrı**; "doğrulanmamış projelerden yüklenenler özel kipe kilitlenmez" yazıyor. Birçok üçüncü taraf blog bunun tersini (1.600 birim, özel kipe kilit) anlatıyor. **Resmî sayfa esas alınır, ilk testi özel video olarak yapıp doğrularız.**
- Zamanlama: `status.publishAt` + `privacyStatus` ilişkisi sayfada net değil; test videosuyla dene.
- Thumbnail ayrı çağrı (`thumbnails.set`) ve telefon doğrulaması isteyebilir.
- Kapsam: `youtube.upload` yükleme için yeter; metadata/thumbnail için `youtube` kapsamı gerekebilir.

## Bu ortamda hazır olanlar
ffmpeg 6.1, Node 22, Python 3.13, Chromium (Remotion için). Çıktı render'ı için GPU gerekmiyor; görsel üretimi API ile yapılacak.

## Ek uygulama ihtiyacı?
- **Zorunlu değil:** Remotion + ffmpeg ile kurgu otomatik. Kullanıcının makinesinde tek gereken: tarayıcı, YouTube Studio ve (ilk video için) DaVinci Resolve.
- **Önerilir:** Resolve ile ilk videoyu elle kurup "kalite çıtası" belirlemek (PLAN.md Faz 2); sonra şablonu koda dökmek.
- CapCut vb. hazır editörler boru hattında kullanılmaz (otomasyona uymuyor, şablon tekrarı riski).
- Müzik: YouTube Ses Kitaplığı veya lisanslı kütüphane.

## Kurulum öncesi güvenlik
Üçüncü taraf kodu çalıştırmadan önce oku; API anahtarlarına dokunan her kod için özellikle. Anahtarlar ortam değişkeninde, repoya yazılmaz.
