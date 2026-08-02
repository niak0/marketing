# Marka Kartı Şablonu

2026-05-14 arşiv serisinin görsel dilini (logo + dev başlık + 3 madde +
CTA + telefon mockup) yeniden üreten, parametreli 4:5 Instagram kartı.

Görsel **AI ile değil, tarayıcıda** çizilir. Sebebi: AI üretiminde Türkçe
karakterler ve logo bozuluyordu (bkz. `content-history/instagram_log.jsonl`,
kayıt `2026-07-22-01`). Burada metin, logo ve marka renkleri her seferinde
birebir aynı çıkar.

## Kullanım

```bash
cd templates/brand-card
python3 render.py cards/<kart>.json -o ../../posts/<klasör>/<ad>.png
```

Çıktı: 1080×1350 PNG (2x render edilip downsample edildiği için metin
keskin).

## Yeni kart eklemek

`cards/` altına bir JSON kopyalayıp içeriği değiştir:

| Alan | Açıklama |
|---|---|
| `theme` | `light` (açık gri zemin) veya `dark` (lacivert zemin) |
| `headline` | Dev başlık. `<br>` ile satır kır, `<em>` ile mavi vurgu |
| `lede` | Alt başlık. `<b>` mavi, `<i>` turuncu vurgu |
| `features` | 3 madde: `icon`, `tint`, `title`, `body` |
| `cta` | Buton metni (başındaki `+` otomatik) |
| `tag` | Sağ alt köşedeki hashtag |
| `photo` | Sağ üstteki lifestyle fotoğraf (proje köküne göre yol) |
| `device_screenshot` | Telefon içindeki **gerçek** uygulama ekran görüntüsü |

`icon`: `plus`, `pin`, `users`, `compass`, `calendar`, `heart`, `bolt`
`tint`: `blue`, `orange`, `violet`

## Kurallar

- **Telefonun içine gerçek ekran görüntüsü koy.** Arşiv serisindeki
  mockup'lar AI ile uydurulmuştu ve açık temalıydı; gerçek uygulama sadece
  dark tema (`#171717`) kullanıyor. Uydurma UI koymak ürünü yanlış tanıtır.
- **İçerik odağı:** basit/günlük bireysel etkinlikler (sabah koşusu, ebru,
  seramik). Kurumsal/organizatör tarafı şu an kapsam dışı — bkz. proje
  `CLAUDE.md`.
- Marka renkleri logodan çıkarıldı: mavi `#0370FB`, turuncu `#FD7201`.
  Uygulama içi primary (`#5A78FF`) ekran görüntülerinde zaten görünüyor.

## Gereksinimler

Chrome (`/Applications/Google Chrome.app`) ve Python `Pillow`. İkisi de
kurulu.
