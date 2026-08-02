# İçerik Geçmişi

Bu klasör ideavoll'un Instagram'da paylaştığı (ya da paylaşılmak üzere üretilen)
tüm içeriklerin kaydını tutar — hem organik post/story/reel hem reklam
kreatifleri. Amaç: aynı hook/tema/caption'ı tekrar etmemek ve hesabın
kimliğini (ton, görsel dil, tekrar eden temalar) zaman içinde tutarlı tutmak.

## Dosya

`instagram_log.jsonl` — her satır tek bir içerik kaydı (JSON object).
Yeni içerik eklerken dosyanın sonuna yeni bir satır ekle, mevcut satırları
değiştirme.

## Şema

| Alan | Açıklama |
|---|---|
| `id` | Benzersiz kısa kimlik, format: `YYYY-MM-DD-NN` (o gün için sıra no) |
| `date` | Üretim/planlama tarihi (ISO 8601, `YYYY-MM-DD`) |
| `type` | `post` \| `story` \| `reel` \| `carousel` |
| `source` | `organic` (organik) \| `ad` (reklam kreatifi) |
| `theme` | Kısa etiket — ör. `keşif`, `mizah`, `ürün-carousel`, `topluluk` |
| `hook_used` | Varsa kullanılan hook/kurgu kalıbı (ör. Higgsfield "Interview" hook'u, ya da serbest metin) |
| `caption` | Tam caption metni |
| `hashtags` | Kullanılan hashtag'ler (varsa) |
| `cta` | Varsa call-to-action metni |
| `visual_style` | Kısa not: renk paleti, format, ton, sahne kurgusu |
| `media_ref` | Görsel/video dosya yolu (repo içi) ya da yayınlandıysa Instagram post URL'si |
| `status` | `taslak` (henüz paylaşılmadı) \| `yayında` (canlı) \| `arşiv` |
| `notes` | Serbest not (opsiyonel) |

## Kullanım

**Yeni içerik üretmeden önce:** bu dosyayı grep'le/oku, aynı hook/tema/caption
tekrar kullanılmış mı kontrol et.

**İçerik üretildikten/onaylandıktan sonra:** yeni bir satır ekle. Instagram'a
gerçekten yüklendiğinde `status`'u `yayında` yap ve varsa `media_ref`'i
gerçek post linkiyle güncelle.

Yayınlama artık elle yapılmıyor: `scripts/flows/` altındaki script'ler
Instagram ve Facebook'a doğrudan gönderiyor (bkz. proje CLAUDE.md,
"Yayınlama"). Bu dosya yine de elle güncellenir — script'ler log'a kayıt
düşmez, yayından sonra kaydı sen eklersin.
