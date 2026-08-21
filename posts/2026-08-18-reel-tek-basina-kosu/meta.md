# Tek Başına Koşu — Reel

**Başlık (iç referans):** Tek Başına Koşu
**Tür:** reel (Instagram + Facebook)
**Kaynak:** ad
**Tema:** basit-etkinlik-olusturma / yalniz-gitmeme
**Format:** 9:16, 1080x1920, 24fps, 11.54sn, sesli (müzik).

**Hikaye:** Bir kadın sabah erkenden kapı önünde tek başına koşu
ayakkabısını bağlıyor, isteksiz — telefonuna bakınca yüzünde hafif bir
gülümseme beliriyor (ideavoll'da bir sabah koşusu etkinliği görmüş gibi).
Sahne değişiyor: sahilde İstanbul silüeti önünde 4 kişilik bir grupla
(kendisi dahil) koşuyor, koşunun sonunda kutlama/high-five anı.

**Karakter:** `seed-images/avatars/av-05-selin.jpg` (ilk kullanım bu
serinin karakteri olarak; av-18-sude yalniz-degilsin reelinde, av-05-selin
avatar setinde ayrıca duruyordu).

**Üretim tekniği (yalniz-degilsin ve reel-yoga reelleriyle aynı hibrit
teknik):**
1. Avatar Higgsfield'a yüklendi (`upload create`), tüm karelerde
   `image_references` olarak kullanıldı.
2. `nano_banana_pro` (9:16, 2k) ile 4 anahtar kare üretildi:
   - `frame1_kapida.png` — sahne 1 başlangıç (ayakkabı bağlama)
   - `frame1b_telefon.png` — sahne 1 bitiş (telefon + gülümseme)
   - `frame2_sahil_v2.png` — sahne 2 başlangıç (grup koşusu, sahil)
   - `frame3_kutlama.png` — sahne 2 bitiş (kutlama/high-five)
   İlk `frame2_sahil.png` denemesinde bir runner'ın şortunda Nike logosu
   çıktı (aynı "no logos" ihlali yalniz-degilsin'deki Coca-Cola sahnesiyle
   aynı kategoride) — prompt'a daha sert "completely plain/unbranded,
   no swoosh" kısıtı eklenip yeniden üretildi (`_v2`), onaylandı.
3. `kling3_0` (mode pro, duration 5, aspect-ratio 9:16, sound off,
   start_image/end_image) ile iki 5.04sn video klibe dönüştürüldü
   (`klip1_raw.mp4`, `klip2_raw.mp4`).
4. Klipler 1080x1920/24fps/yuv420p'ye normalize edildi (`klip1_norm.mp4`,
   `klip2_norm.mp4`).
5. Klip1 üzerine `overlay_text.html`/`render_overlay.py` ile iki ayrı
   şeffaf metin katmanı (fade in/out) bindirildi: "Yine tek mi
   koşuyorsun?" (0-1.65sn) → kaybolup "Beraber daha kolay." (2.0-3.95sn)
   geliyor → `klip1_with_text.mp4`.
6. Klip2, `tpad` ile 6.5sn'ye uzatıldı (`klip2_extended.mp4`) — CTA
   animasyonunun 1sn gecikmeyle başlayıp 5.5sn sürmesi için (1+5.5=6.5).
7. `reel_overlay.html`/`render_reel_overlay.py` ile kart tanımından
   (`templates/brand-card/cards/reel_kosu_cta.json`) şeffaf CTA kare
   dizisi üretildi (132 kare, 24fps, 5.5sn) ve klip2'nin üstüne 1sn
   gecikmeyle composite edildi → `klip2_with_cta.mp4`.
8. İki klip concat edildi → `silent_full.mp4` (11.54sn).
9. Müzik (`posts/2026-07-30-etkinlik-olusturma-reklam/music_raw.wav`,
   aynı kaynak diğer reellerle) loop'lanıp trim + son 1.5sn fade-out
   ile eklendi → `reel_final.mp4`.

**CTA kartı:** "Beraber koşmak daha kolay." / Sabah Koşusu / Yarın 07:00
/ Sahil / 4 kişi / Etkinlik Oluştur.

**Dosyalar:**
- `reel_final.mp4` — yayına hazır final (1080x1920, 11.54sn, müzikli)
- `frame1_kapida.png`, `frame1b_telefon.png`, `frame2_sahil_v2.png`,
  `frame3_kutlama.png` — anahtar kareler
- `klip1_raw.mp4`, `klip2_raw.mp4` — Higgsfield ham video çıktıları
- `overlay_hook1.png`, `overlay_hook2.png` — hook metin katmanları
- `cta_frames/` — CTA animasyon kare dizisi
- `caption.txt` — post açıklaması + hashtag

**Revizyon (2026-08-19):** Hook metni göz seviyesine taşındı (bkz.
`posts/2026-08-18-reel-yeni-sehir/meta.md` revizyon notu). Eski sürüm
`reel_final_old_position.mp4` olarak saklandı.

**Yayın notu (2026-08-21):** Yayınlandı — Instagram Reel
(https://www.instagram.com/reel/DcUPbkkiZgF/, ID 18105112499180585) ve
Facebook Page Reel (https://www.facebook.com/reel/1801334871040564, ID
1801334871040564). Aynı turda Yeni Şehir reel kampanyasının feed postu +
story'si de yayınlandı (bkz. `posts/2026-08-18-reel-yeni-sehir/meta.md`) —
bu reel bilinçli olarak farklı bir tema (sabah koşusu) taşıyor. Diğer 3 reel
(cuma-plansiz, ogle-arasi, sergi-tereddut) hâlâ inceleme bekliyor.
