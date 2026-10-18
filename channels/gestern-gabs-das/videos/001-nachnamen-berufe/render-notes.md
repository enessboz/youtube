# Sessiz stok-video önizlemesini yeniden üretme

Repo kökünden, Python + Pillow ve Node/npm ile:

```sh
cd pipeline/render
npm ci
cd ../..
python scripts/make_channel_art.py
python scripts/collect_preview_footage.py
python scripts/build_stock_preview.py
python scripts/render_stock_preview.py
python -m unittest discover -s tests -p 'test_stock_preview.py' -v
```

Toplayıcı `PEXELS_API_KEY` ortam değişkenini kullanır; gerekirse `.env` veya `PEXELS_ENV_FILE` dosyası yerelde okunur. Anahtar Git'e veya loglara eklenmez. Pexels MP4 ve inceleme JPG'leri Git dışında tutulur; JSON kaynak/lisans dosyaları sürümlenir. Kayıtlı arama sonuçları ve mevcut indirmeler tekrar kullanılır. Seçilmiş kaynak kredileri `assets/SOURCES-stock-preview.md` içindedir.

`build_stock_preview.py`, yalnızca `footage-review.json` içinde gerçek kareleri incelenmiş kabul edilmiş pencereleri kullanır. `script-preview.json` kelimeleri kaybolmadan iki satırlık altyazılara ayrılır. Her kesim yaklaşık 3–5 saniye, tüm video 3–5 dakika aralığında doğrulanır. Bu ses hizalaması değildir.

## İki render yolu

- Dalın mevcut Remotion yolu `shotlist.json` / `scenes.render.json` dosyalarıyla ayrı çalışır. Üretim sırasında gelen b7cb21c güncellemesinin Remotion bileşenleri korundu. Codex denemesinde Windows compositor çöktü; Html5Video kısa testi geçti ama bu deneme değişiklikleri ortak renderer üzerine taşınmadı. Teslim edilen stock-preview varyantı aşağıdaki yerel FFmpeg yoluyla yeniden üretilir.
- Yerel FFmpeg: `python scripts/render_stock_preview.py --workers 3`. Aynı sahne planı, gerçek video kaynakları, sıcak renk düzeltme, iki satırlık altyazı, isim etiketi ve kısa gravür PiP kullanır. Çapraz geçiş yerine çok kısa dip kesmeler üretir. Çıktı `render/preview-stock-1080p.mp4`, 1920×1080/30fps/H.264/CRF26/sessizdir.

Yerel FFmpeg sistem PATH'inden, `FFMPEG_BINARY` veya `--ffmpeg` ile, ya da render paketinin `ffmpeg-static` bağımlılığından bulunur. `render/render-report.json` gerçek çıktı raporudur. Ara parçalar ve video dosyaları Git'e eklenmez.

Yaklaşık 10 MB izleme kopyası, yüksek kaliteli dosyadan 720p iki geçişli 292 kbps H.264 olarak hazırlanır. Bu kopya sıkıştırma nedeniyle ayrıntı kaybeder; asıl görüntü değerlendirmesi 1080p dosyadan yapılmalıdır.

## Yayın durumu

Bu dosya yayınlanacak tam bölüm değildir. İnsan anadil incelemesi, açık kaynak ayrıntıları, son ses, tam metin doğrulaması ve yayın paketi beklenir. İlk dört isimden sonraki senaryo bu üretimde render edilmedi.
