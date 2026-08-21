# Reel — Yeni Şehir

**Başlık (iç referans):** Yeni Şehir
**Tür:** reel (AI video, start/end-frame tekniği) — `posts/2026-08-11-reel-yalniz-degilsin/`
ile aynı teknik pipeline
**Kaynak:** ad (reklam adayı)
**Tema:** basit-etkinlik / yalnız-gitmeme (yeni şehre taşınma senaryosu)

**Karakter:** `seed-images/avatars/av-03-zeynep.jpg` (Higgsfield'a yüklendi,
tüm karelerde kimlik referansı olarak kullanıldı)

**Hikaye:**
- Sahne 1 (ev/pencere): Yarı boşaltılmış kutularla dolu, sade bir dairede
  Zeynep pencere kenarında, elinde telefon, dışarı bakıyor — hafif hüzünlü.
  Bitiş karesi: aynı oda/kıyafet, şimdi telefon ekranına bakıyor, hafif
  merak/ilgi ifadesi.
- Sahne 2 (mahalle buluşması): Sıcak öğleden sonra ışığında sokak kafesinde
  Zeynep ve 3 kişi, markasız kahve bardaklarıyla sohbet/gülüşme. Bitiş
  karesi: yakın kadraj, Zeynep gülerek bir arkadaşına bakıyor.

**Teknik akış:**
1. Higgsfield `nano_banana_pro` (9:16, 2k) ile 4 anahtar kare — her sahne
   için start/end çifti, avatar + önceki kare referans alınarak kompozisyon/
   kıyafet/ışık sabit tutuldu (`frame1_yeni_sehir.png`, `frame1b_ilgi.png`,
   `frame2_bulusma.png`, `frame3_yakin.png`).
2. Higgsfield `kling3_0` (mode pro, 5sn, 9:16, sound off, start-image +
   end-image) ile Sahne 1 ve Sahne 2'den iki ayrı ~5sn video klip
   (`klip1_yenisehir.mp4`, `klip2_yenisehir.mp4`).
3. klip1: 1080x1920/24fps'e normalize edildi, üzerine
   `render_overlay.py` ile üretilen iki ayrı şeffaf hook metni
   (`overlay_hook1.png` / `overlay_hook2.png`) fade in/out ile bindirildi
   (0–1.65sn ve 2.0–3.95sn) → `klip1_with_text.mp4`.
4. CTA kartı: `templates/brand-card/cards/reel_yenisehir_cta.json` +
   `render_reel_overlay.py` (`--duration-ms 5500`) ile 132 kare (24fps,
   şeffaf zemin) → `cta_frames/`.
5. klip2: normalize edildi, `tpad=stop_mode=clone` ile 6.5sn'ye uzatıldı
   (`klip2_extended.mp4`), CTA kare dizisi `-itsoffset 1` ile (1sn
   gecikmeli) üzerine bindirildi → `klip2_with_cta.mp4`.
6. `concat` filtresiyle klip1_with_text + klip2_with_cta birleştirildi
   → `silent_full.mp4` (11.54sn).
7. `posts/2026-07-30-etkinlik-olusturma-reklam/music_raw.wav` loop'landı,
   son 1.5sn'de `afade=out` ile kısıldı → `reel_final.mp4`.

**Hook metinleri:** "Yeni şehir, tek başına." → "Burada da birileri var."
**CTA:** "Burada yalnız değilsin." / Mahalle Kahve Buluşması, Bugün 18:00,
Kadıköy, 5 kişi / Etkinlik Oluştur

**Dosyalar:**
- `frame1_yeni_sehir.png`, `frame1b_ilgi.png` — Sahne 1 start/end kareleri
- `frame2_bulusma.png`, `frame3_yakin.png` — Sahne 2 start/end kareleri
- `klip1_yenisehir.mp4`, `klip2_yenisehir.mp4` — ham AI video klipler
- `overlay_hook1.png`, `overlay_hook2.png` — hook metin katmanları
- `cta_frames/` — CTA animasyon kare dizisi (132 kare)
- `klip1_with_text.mp4`, `klip2_extended.mp4`, `klip2_with_cta.mp4` —
  ara işlenmiş klipler
- `silent_full.mp4` — sessiz birleşik video
- `reel_final.mp4` — final, müzikli, 1080x1920, 24fps, 11.54sn
- `caption.txt`

**Uyum notları:** Alkol yok, marka/logo/tanınabilir ürün etiketi yok
(kahve bardakları markasız, telefon ekranı boş/okunaksız), karakterler
yetişkin görünümlü ve gündelik/uygun kıyafetli. Metin ve CTA kartı tamamen
kod (`render_overlay.py` / `render_reel_overlay.py`) ile üretildi, AI'a
çizdirilmedi.

**Revizyon (2026-08-19):** Müşteri geri bildirimiyle hook metni konumu
`overlay_text.html`'de göz seviyesine (üst-orta, `padding-top: 560px`)
taşındı — önceki konum ekranın alt-orta kesimindeydi. Bu artık şablonun
varsayılan konumu; sonraki reellerde otomatik uygulanacak. Eski sürüm
`reel_final_old_position.mp4` olarak saklandı.

**Yayın notu (2026-08-21):** Yayınlandı — Instagram Reel
(https://www.instagram.com/reel/DcSyYA0lV1t/) ve Facebook Page Reel
(https://www.facebook.com/reel/1055109527382657). Diğer 4 reel
(cuma-plansiz, tek-basina-kosu, ogle-arasi, sergi-tereddut) hâlâ inceleme
bekliyor. Bu reel'in temasıyla eşleşen bir feed postu + story
(`kart_feed.png` / `kart_story.png`, `templates/brand-card/cards/afis_yenisehir_post.json`,
`frame3_yakin.png` fotoğrafı reel'den yeniden kullanıldı) hazırlanıp
kullanıcıya inceleme için gönderildi — henüz yayınlanmadı.
