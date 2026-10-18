# YouTube içerik sistemi — çalışma kuralları

Bu repo iki kanalın (Almanca `gestern-gabs-das`, İtalyanca `quando-eravamo-noi`) araştırma, üretim ve ölçümünü yönetir. Ana plan: `PLAN.md` (§7 kanal planı). Mimari: `docs/ARCHITECTURE.md`.

## Rol dağılımı
Ana oturum **üst ajan (producer)** olarak çalışır; işi tek başına yapmaz, `.claude/agents/` altındaki alt ajanlara devreder (Agent aracı, `subagent_type`). Alt ajanlar birbirini çağıramaz; her şey üst ajandan geçer. Akış ve kapılar: `.claude/skills/produce-video/SKILL.md`. Model seçimi ve yükseltme kuralları: `docs/AGENTS.md`.

## Model yönlendirme (özet)
- Varsayılan model ajan dosyasındaki `model:` değeridir. Üst ajan görev zorluğuna göre Agent aracının `model` parametresiyle **yükseltir veya düşürür**.
- Yaratıcı/risk yüksek iş (araştırma, senaryo, ilk video, çelişkili fact-check) → `opus`. Hızlı/yapısal iş (paketleme, sahne planı, redaksiyon) → `sonnet`. Mekanik iş (klasör, manifest, kontrol listesi) → `haiku`.
- Yükseltme sinyalleri: fact-checker "ÜST AJANA YÜKSELT", compliance KALDI/EMİN DEĞİLİM, kanalın ilk 3 videosu, kalite çıtası altında kalan çıktı.

## Değişmez kurallar
- **Yayın ve ödeme insan onayıyla.** Hiçbir ajan video yayınlamaz, API anahtarı oluşturmaz, para harcayan işi (ses/görsel üretimi) kullanıcı onayı olmadan çalıştırmaz.
- Sağlık/finans iddiası yok; yanıltıcı başlık/kapak yok; gerçekçi sentetik görsel Studio'da beyan edilir. AI kullanımını gizlemeye yönelik hiçbir iş yapılmaz (özgünlük ve kalite ≠ gizleme).
- Her olgu kaynaklı; kaynaksız bilgi senaryoya girmez. İçerik ülkeye özgü araştırılır, çeviri değildir.
- Her kanalın dosyaları kendi klasöründe (`channels/<kanal>/`); kanallar arası içerik kopyalanmaz.
- API anahtarları ortam değişkeninde (`YOUTUBE_API_KEY`, `ELEVENLABS_API_KEY`), repoya yazılmaz.
- Başka GitHub reposu klonlamak için önce kullanıcıdan onay al (oturum yalnızca bu repoya bağlı).

## Komutlar
- Yeni video klasörü: `python3 scripts/new_video.py <kanal> <slug>`
- Niş/rakip ölçümü: `pipeline/niche_scout/` (`scout.py`, `competitors.py`, `handles.py`; kota için dosya başlığına bak)
- Testler: `python3 -m unittest discover -s pipeline/niche_scout/tests`
