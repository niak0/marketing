# CLAUDE.md — ideavoll Marketing İçerik Üretimi

Bu klasör **ideavoll** mobil uygulamasının reklam/pazarlama içeriklerini
üretmek için ayrılmıştır. Uygulamanın kendi kod deposundan (`../lovable`)
kasıtlı olarak bağımsızdır — burada üretilen görsel/video dosyaları o
projenin git geçmişine karışmaz.

## Proje Neyle İlgili (içerik ürettiğimiz uygulama)

**ideavoll** — sosyal akış + etkinlik/bilet platformu (Flutter, iOS/Android).
Kod: `/Volumes/Okantosh/projects/ideavoll/lovable`

- **Domain:** ideavoll.com (app.ideavoll.com deeplink/auth subdomain'i)
- **Bundle ID:** `com.vlkndmr.ideavoll`
- Uygulama tek başına ne bir "sosyal medya app'i" ne de "sadece bilet app'i" —
  ikisinin karışımı:
  - **Sosyal akış (home):** post + story karışık feed, takip sistemi, DM
  - **Etkinlik keşfi:** kategori/harita bazlı etkinlik arama (explore/search)
  - **Etkinlik oluşturma & bilet satışı:** organizatörler etkinlik açar,
    kullanıcılar bilet satın alır (İşBankası İşPOS entegrasyonu)
  - **Organizatör tarafı:** business hesabına geçiş, KYC/onay süreci, cüzdan/
    hakediş takibi (wallet), fatura görüntüleme
- **Marka rengi (uygulama temasından):** primary `#5A78FF` (indigo/mavi tonu),
  koyu tema arka plan `#171717` / `#212121`. Gradient aksan: `#374FC7` →
  `#23BA99`. Üretilen görsellerde bu paleti referans al, ama bire bir şart
  değil — pazarlama içeriği daha canlı/dikkat çekici olabilir.

> Öncelikli persona netleşti: **bireysel kullanıcı / etkinlik katılımcısı**.
> Organizatör/kurumsal taraf (business hesabı, KYC, wallet vb.) şu an için
> içerik kapsamı **dışında** — bir sonraki aşamada ele alınacak. Marka tonu
> (samimi/eğlenceli mi, ciddi mi) hâlâ net değil — bir kampanya başlamadan
> önce bunu netleştir, tahmin etme.
>
> **İlk faz içerik odağı (müşteri yönü, Volkan Demir, 2026-07-30):** Büyük
> konser/etkinlik değil, **basit/günlük bireysel etkinlikler** vurgulanacak —
> sabah koşusu, ebru, seramik boyama gibi kolayca oluşturulabilecek/katılınacak
> etkinlikler. Mesaj odağı: "oluştur ve katıl" basitliği. Reklam/organik
> içerik konsept seçerken bu örneklere yakın, gösterişli olmayan senaryolar
> tercih et.

Marka renk/tipografi/logo referansı için bkz. `brand/design-system.md`
(kod kaynağından — `../lovable/lib/core/theme/` — çıkarıldı) ve
`brand/logo.png`.

## Bu Klasörün Amacı

- Higgsfield CLI (+ eklenecek MCP) ile reklam görseli/videosu üretmek
- Üretilen içerik **Meta Ads** (Facebook/Instagram) üzerinden yayınlanacak
- Bu klasör bağımsız bir çalışma alanı: kendi `.gitignore`'u, kendi git
  geçmişi (varsa) burada tutulur, `../lovable` reposuna dokunmaz

## Araçlar

- **Higgsfield CLI** (`higgsfield` / `higgs`) — global npm paketi, zaten
  kurulu ve login olundu (`higgsfield auth login`)
- **Higgsfield skills** (bkz. `../lovable/.agents/skills/` — oradan buraya
  taşınabilir ya da burada ayrıca `npx skills add higgsfield-ai/skills` ile
  kurulabilir):
  - `higgsfield-generate` — görsel/video/3D/audio üretimi (genel)
  - `higgsfield-product-photoshoot` — ürün/marka görseli, hero/banner,
    Meta ads creative
  - `higgsfield-marketplace-cards` — marketplace ürün kartı formatı
    (muhtemelen bu proje için gerekli değil)
  - `higgsfield-video-explainer` — anlatıcı/açıklayıcı video
  - `higgsfield-soul-id` — yüz/kimlik tutarlılığı (influencer/avatar videosu
    gerekirse)
  - `higgsfield-websites` — bu klasörde muhtemelen kullanılmayacak
- **MCP:** kullanıcı ayrıca kuracak (Meta Ads API / Higgsfield MCP olabilir) —
  kurulunca burada bir "İlgili Araçlar" notu olarak güncelle.

## İçerik Üretim Sistemi (2026-08-03)

Görsel içerik artık **kodla** üretiliyor. Yeni içerik üretmeden önce
`templates/brand-card/README.md` ve `brand/visual-identity.md` oku.

**Neden kod:** AI üretiminde Türkçe karakterler ve logo bozuluyordu (bkz.
`content-history/instagram_log.jsonl`, kayıt `2026-07-22-01`). HTML/CSS →
Chrome ekran görüntüsü ile metin, logo ve marka renkleri her seferinde
birebir aynı çıkıyor; üretim maliyeti de sıfır.

| İhtiyaç | Komut (`templates/brand-card/` içinden) |
|---|---|
| Tek kart | `python3 render.py cards/<x>.json -t card_afis.html -o <çıktı>` |
| Üç oran birden | aynı komut + `-f all` (feed 4:5, story 9:16, kare 1:1) |
| Carousel | `python3 render_carousel.py cards/<x>.json -o <çıktı>` |
| Animasyonlu Reel | `python3 render_reel.py cards/<x>.json -o <x>.mp4 --music <wav>` |

İki kart çizgisi var: `card_afis.html` (dikkat çekici / reklam) ve
`card_davetiye.html` (ürün anlatımı). İkisi de aynı marka imzasını taşır.

**AI'ın rolü** kartların içine giren lifestyle fotoğrafları üretmekle
sınırlı. Metin, logo ve arayüz asla AI'a çizdirilmez. Telefon mockup'ına
daima **gerçek** uygulama ekran görüntüsü konur.

## Yayınlama

Instagram/Facebook yayını **elle değil**, `scripts/flows/` altındaki
script'lerle yapılıyor (post, story, reel, Facebook post/reel, kapak/profil
görseli). Kullanım ve ön koşullar: `scripts/flows/README.md`.

- Medya public bir URL'de olmalı — Meta yerel dosya kabul etmez. Yöntem:
  dosyayı bu repoya commit + push et, `raw.githubusercontent.com` URL'ini
  kullan (`.gitignore` görselleri dışladığı için `git add -f` gerekir).
- Token'lar öldüğünde (`code 190`, "could not be decrypted") ilk çalıştırılacak
  akış: `scripts/flows/refresh-meta-tokens.sh`.
- Her yayından sonra `content-history/instagram_log.jsonl`'a kayıt düş.

## Çalışma Kuralları

- Bu klasördeki iş **ideavoll uygulama koduyla ilgili değil** —
  `../lovable/CLAUDE.md`'deki Flutter/Riverpod/İşBankası kuralları burada
  geçerli değil.
- Üretilen ham/ara görsel-video dosyaları (büyük binary) commit edilmeden
  önce `.gitignore`'a eklenmeli.
- Bir kampanya/set üretilirken hedef (hangi platform: Reels/Story/Feed,
  hangi format/oran, hangi CTA) net değilse üretime başlamadan önce sor.
