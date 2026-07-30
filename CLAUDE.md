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

## Çalışma Kuralları

- Bu klasördeki iş **ideavoll uygulama koduyla ilgili değil** —
  `../lovable/CLAUDE.md`'deki Flutter/Riverpod/İşBankası kuralları burada
  geçerli değil.
- Üretilen ham/ara görsel-video dosyaları (büyük binary) commit edilmeden
  önce `.gitignore`'a eklenmeli.
- Bir kampanya/set üretilirken hedef (hangi platform: Reels/Story/Feed,
  hangi format/oran, hangi CTA) net değilse üretime başlamadan önce sor.
