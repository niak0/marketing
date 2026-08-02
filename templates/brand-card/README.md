# Marka Kartı Sistemi

ideavoll'un görsel içeriklerini (post, story, carousel, reel) tarayıcıda
üreten şablon sistemi. Görsel **AI ile değil, Chrome ile** çizilir: Türkçe
karakterler, logo ve marka renkleri her seferinde birebir aynı çıkar. AI
üretiminde bunlar bozuluyordu — bkz. `content-history/instagram_log.jsonl`,
kayıt `2026-07-22-01`.

## Görsel dil

2026-08-03'te iki çizgi seçildi. İkisi de aynı imzayı taşır, bu yüzden
feed karışık kullanıldığında bile tutarlı görünür:

| Öğe | Nereden geliyor |
|---|---|
| Konum halkaları | Logodaki harita pini — "yakınında" fikrinin görselleşmesi |
| `ne zaman · nerede · kim var` | Ürünün kendi verisi; her kartta tekrar eder |
| Mavi `#0370FB`, turuncu `#FD7201` | Doğrudan logodan örneklendi |
| Bricolage Grotesque | Başlıklar. Gövde: Inter, veri: JetBrains Mono |

**`card_afis.html`** — fotoğraf tam kaplar, dev başlık üstüne biner.
Dikkat çekici; reklam kreatifi ve öne çıkan organik post için.

**`card_davetiye.html`** — gece zemini, bilet/davetiye objesi. Ürünü ve
etkinliği birlikte anlatır; özellik/anlatım postları için.

## Kullanım

```bash
cd templates/brand-card

# Tek kart, tek format
python3 render.py cards/<kart>.json -t card_afis.html \
    -o ../../posts/<klasör>/<ad>.png

# Üç oranın hepsi (feed 4:5, story 9:16, kare 1:1)
python3 render.py cards/<kart>.json -t card_afis.html -f all \
    -o ../../posts/<klasör>/<ad>.png

# Carousel (slayt slayt PNG)
python3 render_carousel.py cards/<carousel>.json \
    -o ../../posts/<klasör>/slayt.png

# Animasyonlu Reel (9:16 mp4, 6 sn)
python3 render_reel.py cards/<reel>.json \
    -o ../../posts/<klasör>/reel.mp4 --music <yol.wav>
```

Fontlar `fonts/` altında gömülü gelir. Yeniden indirmek gerekirse:
`python3 fetch_fonts.py`

## Kart JSON alanları

| Alan | Açıklama |
|---|---|
| `headline` | Başlık. `<br>` satır kırar, `<em>` vurgu rengi verir |
| `lede` | Alt metin. `<b>` beyaz/koyu, `<i>` turuncu |
| `kicker` | Üstteki küçük etiket ("5 dakika yürüme mesafende") |
| `event_name` | Bilet objesindeki etkinlik adı |
| `meta_time` / `meta_place` / `meta_people` | İmza veri üçlüsü |
| `cta` | Buton metni (baştaki `+` otomatik) |
| `photo` | Lifestyle fotoğraf (proje köküne göre yol) |
| `device_screenshot` | Telefon içindeki **gerçek** uygulama ekranı |

Carousel'de bunlar `slides` listesindeki her slayta yazılır; slaytın
`role` alanı düzeni seçer: `hook`, `step`, `cta`. Reel'de başlık üç ayrı
alana bölünür: `line1`, `line2`, `line3` (satırlar sırayla animasyonla
girer).

## Kurallar

- **Telefonun içine daima gerçek ekran görüntüsü koy.** 2026-05-14 arşiv
  serisindeki mockup'lar AI ile uydurulmuştu ve açık temalıydı; gerçek
  uygulama sadece dark tema (`#171717`) kullanıyor.
- **İçerik odağı:** basit/günlük bireysel etkinlikler (sabah koşusu, ebru,
  seramik). Kurumsal/organizatör tarafı şu an kapsam dışı — proje
  `CLAUDE.md`'ye bak.
- **Story formatında** üst ve alt ~200px Instagram arayüzüne ayrılmıştır,
  şablon bunu zaten boş bırakır; oraya içerik taşırma.

## Reel nasıl çalışıyor

Chrome tek kare ekran görüntüsü alır, animasyonu "oynatamaz". Çözüm:
`reel.html` içindeki her animasyonun gecikmesi `calc(<başlangıç> -
var(--t))` ve tüm animasyonlar duraklatılmış. `render_reel.py` her kare
için `--t` değerini değiştirip Chrome'u çağırır, böylece kare tam o ana
sabitlenir; kareler ffmpeg ile mp4'e çevrilir.

CSS'in sonundaki `animation-play-state/fill-mode: !important` kuralı bu
mekanizmanın şartıdır — `animation` kısayolu bu iki alt özelliği
sıfırladığı için kural en sonda ve `!important` olmak zorunda. Kaldırma.

144 kare ~2 dakikada üretilir (4 paralel Chrome).

## Gereksinimler

Chrome (`/Applications/Google Chrome.app`), Python `Pillow`, `ffmpeg`.
Hepsi kurulu.
