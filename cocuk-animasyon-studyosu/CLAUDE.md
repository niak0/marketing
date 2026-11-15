# CLAUDE.md — Çocuk Animasyon Stüdyosu

Bu klasör çocuklar için kısa animasyon hikâyeleri üretme stüdyosu. Her hikâye
`projeler/<hikaye-adi>/` altında kendi klasöründe yaşar. Makine: Mac mini M4
(Apple Silicon); komutları buna göre yaz (Homebrew, `python3`, `/opt/homebrew`).

## Üretim yöntemi: animasyonu kod çiziyor

Karakterler, sahneler, yazılar ve müzik **kodla** üretiliyor; yapay zekâ görsel
modeline çizdirilmiyor. Sebep: Türkçe karakterler ve karakter tutarlılığı her
karede birebir aynı kalsın, render ücretsiz ve tekrarlanabilir olsun.

Zincir:
1. `projeler/<x>/index.html`: tek bir SVG sahnesi (1280×720 viewBox) + JS.
   Sayfa `window.render(t)` (t = saniye) ve `window.DUR` (toplam süre) sunar.
   `render(t)` **deterministik** olmalı: aynı t, aynı kare. Animasyonda
   `Date`/`Math.random` kullanma; rastgelelik gerekirse t'den türet.
2. `projeler/<x>/music.py`: numpy ile melodi üretir → WAV (`python3 music.py out.wav <süre>`).
3. `tools/render.js`: Playwright/Chromium sayfayı `?record` ile açar, 30 fps
   kare kare ekran görüntüsü alır, müziği üretir, ffmpeg ile 1920×1080 MP4 yapar.

| İş | Komut |
|---|---|
| Tarayıcıda izle/düzenle | `open projeler/<x>/index.html` |
| Kontrol kareleri (12 adet) | `npm run test-kare -- projeler/<x>` → `projeler/<x>/kontrol/` |
| Final MP4 | `npm run render -- projeler/<x>` → `projeler/<x>/<x>.mp4` |

Yeni hikâyeye başlarken: `projeler/zeyno-ile-fistik/` klasörünü kopyala, bu
dosyadaki "Karakter çizim kalıbı"nı kullan. Ayrıntılar
`projeler/zeyno-ile-fistik/NASIL-YAPILDI.md`.

## Karakter çizim kalıbı

- Her karakter `<g id="xWrap"><g id="x">…</g></g>`. Origin = **ayakların ortası (0,0)**,
  sağa bakar. Yön/ölçek/konum Wrap'e verilir: `translate(x y) rotate(r) scale(dir*s s)`.
- Hareketli parçalar (bacak, boyun, hortum, kulak, kuyruk) ayrı `id`'li gruplar;
  JS `rotate(açı pivotX pivotY)` ile döndürür. Yürüme = bacaklarda `sin(walk)`,
  çaprazlar zıt faz + gövdede `|cos|` zıplaması.
- Konuşma balonu, alt yazı, sahne geçişi (siyah fade) ortak yardımcılar.
- Sahneler `SCENES` dizisindeki zaman sınırlarıyla bölünür; her sahne kendi
  `lt` (yerel zaman) değeriyle `seg()/win()` easing yardımcılarını kullanır.

## Kurallar

- Hedef kitle küçük çocuklar: yumuşak renkler, şiddet/korku yok, kısa ve
  okunaklı Türkçe cümleler, büyük font.
- Bitirdiğini söylemeden önce `test-kare` ile kareleri **gözle kontrol et**
  (karakter iç içe geçmesi, havada kalma, balonların kesilmesi).
- MP4/WAV büyük binary: git'e girmez (`.gitignore`).
- Format (yatay 16:9 / dikey 9:16 Reels), süre veya seslendirme belli değilse
  üretime başlamadan sor.
