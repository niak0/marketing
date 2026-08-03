# Flow Registry

Bu klasördeki script'ler, elle sürülmüş ve stabilleşmiş akışların donmuş
halidir. Yeni bir akışa başlamadan önce burayı kontrol et — zaten yazılmış
olabilir.

## refresh-meta-tokens
- **Dosya:** `scripts/flows/refresh-meta-tokens.sh`
- **Yapar:** Graph API Explorer'dan alınan kısa ömürlü user token'ı uzun
  ömürlüye (60 gün) çevirir, ondan Page access token'ı türetir, sayfaya bağlı
  IG Business hesap ID'sini doğrular ve `.env`'i günceller. Diğer tüm publish
  script'leri bu token'lara bağlı — 401/"could not be decrypted" hatası
  alındığında ilk çalıştırılacak akış budur.
- **Ön koşul:** `.env` içinde `META_APP_ID`, `META_APP_SECRET`, `META_PAGE_ID`
  tanımlı olmalı. Elle alınan kısa ömürlü token şu izinlere sahip olmalı:
  `instagram_basic`, `instagram_content_publish`, `pages_manage_posts`,
  `pages_read_engagement`, `pages_show_list`.
- **Bırakır:** `.env` üzerine yazar, öncesinde `.env.bak` yedeği alır (ikisi de
  gitignore kapsamında). Meta tarafında kalıcı bir şey değiştirmez; eski
  token'ları geçersiz kılmaz.
- **Çalıştır:** `./scripts/flows/refresh-meta-tokens.sh "<short_lived_token>"`
- **Süre:** ~3-5s

## publish-instagram-post
- **Dosya:** `scripts/flows/publish-instagram-post.sh`
- **Yapar:** Public bir görsel URL'ini Instagram Business hesabına (ideavoll)
  organik foto post olarak yayınlar. İki adımlı Graph API akışı (container
  oluştur → FINISHED bekle → publish) tek komuta indirgenmiş.
- **Ön koşul:** `.env` içinde `META_ACCESS_TOKEN` (scope: `instagram_basic`,
  `instagram_content_publish`) ve `META_IG_BUSINESS_ACCOUNT_ID` tanımlı olmalı.
  Görsel URL'i herkese açık ve Meta'nın erişebileceği bir adres olmalı (yerel
  dosya yolu çalışmaz).
- **Bırakır:** `--dry-run` olmadan çalıştırılırsa Instagram'da **gerçek,
  canlı bir post** — kalıcı, script bunu geri almaz. `--dry-run` ile sadece
  işlenmiş ama yayınlanmamış bir container bırakır (görünür değil, temizlik
  gerekmez).
- **Çalıştır:**
  `./scripts/flows/publish-instagram-post.sh "<image_url>" "<caption>" [--dry-run]`
- **Süre:** ~5-10s (container işlenme süresine bağlı)

## publish-facebook-post
- **Dosya:** `scripts/flows/publish-facebook-post.sh`
- **Yapar:** Public bir görsel URL'ini Facebook Page'e (Ideavoll) foto post
  olarak paylaşır. Tek Graph API çağrısı (`/{page-id}/photos`).
- **Ön koşul:** `.env` içinde `META_PAGE_ACCESS_TOKEN` (scope: `pages_manage_posts`,
  `pages_read_engagement`) ve `META_PAGE_ID` tanımlı olmalı.
- **Bırakır:** `--dry-run` olmadan çalıştırılırsa Facebook'ta **gerçek,
  canlı bir post**. `--dry-run` ile `published=false` olarak taslak bırakır
  (herkese açık görünmez, temizlik gerekmez).
- **Çalıştır:**
  `./scripts/flows/publish-facebook-post.sh "<image_url>" "<caption>" [--dry-run]`
- **Süre:** ~2-3s

## publish-instagram-carousel
- **Dosya:** `scripts/flows/publish-instagram-carousel.sh`
- **Yapar:** 2-10 public görsel URL'ini tek bir Instagram carousel postu
  olarak yayınlar. Üç aşamalı Graph API akışı: her slayt için
  `is_carousel_item=true` container → `media_type=CAROUSEL` üst container
  (children listesi + caption) → FINISHED bekle → publish.
- **Ön koşul:** `.env` içinde `META_ACCESS_TOKEN` ve
  `META_IG_BUSINESS_ACCOUNT_ID`. Görseller JPEG olmalı (PNG güvenilir
  çalışmıyor) ve Instagram oran aralığında (4:5 – 1.91:1).
- **Bırakır:** `--dry-run` olmadan çalıştırılırsa Instagram'da **gerçek,
  canlı bir carousel postu**. `--dry-run` ile slayt container'ları ve
  yayınlanmamış carousel container'ı bırakır (görünmez, temizlik gerekmez).
- **Çalıştır:**
  `./scripts/flows/publish-instagram-carousel.sh "<caption>" "<url1>" "<url2>" ... [--dry-run]`
- **Süre:** ~10-20s (slayt sayısına bağlı)

## publish-instagram-story
- **Dosya:** `scripts/flows/publish-instagram-story.sh`
- **Yapar:** Public bir görsel/video URL'ini Instagram Business hesabına Story
  olarak yayınlar (`media_type=STORIES`).
- **Ön koşul:** `.env` içinde `META_ACCESS_TOKEN` ve `META_IG_BUSINESS_ACCOUNT_ID`
  tanımlı olmalı (aynı token, `publish-instagram-post` ile paylaşılıyor).
- **Bırakır:** `--dry-run` olmadan çalıştırılırsa Instagram'da **gerçek, canlı
  bir Story** — 24 saat sonra kendiliğinden kaybolur, script müdahale etmez.
  `--dry-run` ile sadece işlenmiş ama yayınlanmamış container bırakır.
- **Çalıştır:**
  `./scripts/flows/publish-instagram-story.sh "<media_url>" <IMAGE|VIDEO> [--dry-run]`
- **Süre:** ~5-10s (foto), video için daha uzun olabilir

## publish-instagram-reel
- **Dosya:** `scripts/flows/publish-instagram-reel.sh`
- **Yapar:** Public bir video URL'ini Instagram Business hesabına Reel olarak
  yayınlar (`media_type=REELS`). Reels sekmesinde görünmesi için video 9:16
  oranında ve 5-90sn olmalı — script bunu doğrulamaz, dışındaki videolar
  normal video post olarak yayınlanır.
- **Ön koşul:** `.env` içinde `META_ACCESS_TOKEN` ve `META_IG_BUSINESS_ACCOUNT_ID`
  tanımlı olmalı.
- **Bırakır:** `--dry-run` olmadan çalıştırılırsa Instagram'da **gerçek, canlı
  bir Reel** — kalıcı. `--dry-run` ile işlenmiş ama yayınlanmamış container
  bırakır.
- **Çalıştır:**
  `./scripts/flows/publish-instagram-reel.sh "<video_url>" "<caption>" [--dry-run]`
- **Süre:** video işlenmesine bağlı, birkaç dakikaya kadar sürebilir

## update-facebook-profile-picture
- **Dosya:** `scripts/flows/update-facebook-profile-picture.sh`
- **Yapar:** Facebook Page profil resmini `<image_url>` ile değiştirir
  (`POST /{page-id}/picture`).
- **Ön koşul:** `.env` içinde `META_PAGE_ACCESS_TOKEN` ve `META_PAGE_ID`
  tanımlı olmalı.
- **Bırakır:** **`--dry-run` YOK** — her çalıştırma Page'in profil resmini
  gerçek ve anında değiştirir, herkese açık şekilde görünür değişir. Dikkatli
  kullan, çalıştırmadan önce doğru URL olduğundan emin ol.
- **Çalıştır:** `./scripts/flows/update-facebook-profile-picture.sh "<image_url>"`
- **Süre:** ~2s

## update-facebook-cover-photo
- **Dosya:** `scripts/flows/update-facebook-cover-photo.sh`
- **Yapar:** Facebook Page kapak görselini `<image_url>` ile değiştirir. İki
  adım: foto Page albümüne yükle (`published=false`, feed'e düşmez) → o foto
  ID'sini `cover` olarak set et.
- **Ön koşul:** `.env` içinde `META_PAGE_ACCESS_TOKEN` ve `META_PAGE_ID`
  tanımlı olmalı.
- **Bırakır:** **`--dry-run` YOK** — çalıştırma Page'in kapak görselini
  gerçek ve anında değiştirir. Ayrıca Page albümüne yayınlanmamış bir foto
  (adım 1) bırakır — bu foto herkese açık görünmez, temizlik gerekmez.
- **Çalıştır:** `./scripts/flows/update-facebook-cover-photo.sh "<image_url>" [offset_y]`
- **Süre:** ~3-4s

## publish-facebook-reel
- **Dosya:** `scripts/flows/publish-facebook-reel.sh`
- **Yapar:** Public bir video URL'ini Facebook Page'e Reel olarak yayınlar.
  Video API resumable upload akışı: upload session başlat → `file_url` ile
  yükle → `uploading_phase=complete` bekle → `upload_phase=finish` ile
  yayınla. Video specs: 9:16, 540x960-1080x1920px, 3-90sn, 24-60fps.
- **Ön koşul:** `.env` içinde `META_PAGE_ACCESS_TOKEN` (scope:
  `pages_manage_posts`) ve `META_PAGE_ID` tanımlı olmalı.
- **Bırakır:** `--dry-run` olmadan çalıştırılırsa Facebook'ta **gerçek, canlı
  bir Reel**. `--dry-run` ile video yüklenmiş ama `finish` çağrılmamış bir
  video ID bırakır (yayınlanmamış, herkese açık görünmez — Meta tarafında
  bir süre sonra kendiliğinden expire olur, script temizlik yapmaz).
- **Not:** `processing_phase` alanı `upload_phase=finish` çağrılmadan
  `not_started` kalıyor — asıl bekleme kapısı `uploading_phase.status`.
- **Çalıştır:**
  `./scripts/flows/publish-facebook-reel.sh "<video_url>" "<description>" [--dry-run]`
- **Süre:** ~1-3dk (video boyutuna bağlı)
