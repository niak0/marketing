# ideavoll — Marka & Tasarım Referansı

Kaynak: `../../lovable/lib/core/theme/` (app_colors.dart, app_theme.dart,
app_typography.dart) + `../../lovable/assets/logo.png`. Bu dosya, kod
tarafındaki tema tanımının pazarlama görseli üretiminde referans alınabilecek
özetidir — kod tarafı değişirse burası da güncellenmeli.

## Logo

`brand/logo.png` — 1092×1092, PNG/RGBA, şeffaf arka plan. Görsel üretiminde
`--image` referansı olarak veya kompozisyona overlay olarak kullanılabilir.

## Renk Paleti

### Primary
| Ad | Hex |
|---|---|
| primary | `#5A78FF` |
| primaryLight | `#708AFF` |
| primaryMuted | `#899FFF` |

### Arka Plan / Yüzey (dark tema — uygulama sadece dark tema kullanıyor)
| Ad | Hex |
|---|---|
| background | `#171717` |
| surface | `#212121` |
| surfaceDim | `#1D1D1D` |
| surfaceVariant | `#2C2D30` |

### Gri Skala
| Ad | Hex |
|---|---|
| gray100 | `#E8EAED` |
| gray200 | `#D5D7DB` |
| gray300 | `#BABDC2` |
| gray500 | `#7E8085` |
| gray600 | `#606266` |
| gray700 | `#404145` |
| gray800 | `#2C2D30` |

### Metin
| Ad | Hex |
|---|---|
| textPrimary | `#FFFFFF` |
| textSecondary | `#D5D7DB` |
| textTertiary | `#7E8085` |

### Durum
| Ad | Hex |
|---|---|
| error | `#EF5350` |
| warning | `#FFB74D` |
| success | `#4CAF50` |

### Gradientler
- **storyGradient** (hikaye border'ı — ana marka gradienti):
  `#374FC7 → #23BA99` (bottomLeft → topRight, indigo-teal)
- **boostGradient** (öne çıkan/boost'lu içerik rozeti — altın/amber,
  storyGradient'ten kasıtlı ayrıştırılmış): `#FFD54F → #FF8F00`

Pazarlama görsellerinde ana vurgu için **storyGradient** kullan; boostGradient
sadece "öne çıkan/premium" hissi gereken özel durumlar için (örn. "trend
etkinlik" vurgusu).

## Tipografi

Font ailesi: **SF Pro** (iOS sistem fontu — Android'de sistem fallback'ine
düşer, marka özel bir font yüklemiyor; `pubspec.yaml`'da custom font tanımı
yorum satırında/pasif).

| Stil | Boyut | Weight | Kullanım |
|---|---|---|---|
| headlineLarge | 32 | 600 | büyük başlıklar |
| headlineMedium | 24 | 400 | karşılama/orta başlık |
| titleMedium | 18 | 600 | sayfa başlığı |
| titleSmall | 18 | 500 | alt başlık |
| bodyLarge | 16 | 400 | paragraf |
| bodyMedium | 14 | 400 | paragraf (orta) |
| button | 16 | 600 | buton metni |

Satır yüksekliği genelde 1.5×. Görsel üretiminde başlık tipografisini taklit
ederken: kalın (semibold/600), yuvarlak hatlı, bol boşluklu (letter-spacing
hafif negatif -0.03 büyük başlıklarda).

## Buton / UI Dili (kompozisyonda tutarlılık için)

- Köşe yarıçapı: 12px (butonlar, kartlar)
- Primary buton: dolu `#5A78FF` zemin, beyaz metin
- Outline buton: şeffaf zemin, `surfaceVariant` renginde border
- Genel his: koyu tema, yüksek kontrast beyaz metin, yumuşak köşeler, düz
  (elevation'sız/gölgesiz) yüzeyler

## Higgsfield Brand Kit ile senkron alternatifi

Bu dosya kod kaynağından elle çıkarıldı. Higgsfield'ın kendi `brand-kits
fetch --url ideavoll.com` özelliği de var (bkz.
`.agents/skills/higgsfield-generate/references/marketing-brand-kits.md`) ve
üretimde `--brand-kit-id` olarak bağlanabiliyor — ama web sitesi uygulamanın
koyu temasını birebir yansıtmayabilir. Üretimde ikisi çelişirse **bu dosya
(kod kaynaklı) esas alınmalı**, brand kit tamamlayıcı/ikincil kaynak.
