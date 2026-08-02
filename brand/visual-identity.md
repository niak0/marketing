# ideavoll — Pazarlama Görsel Kimliği

Bu dosya **pazarlama içeriğinin** görsel dilini tanımlar. Uygulamanın kendi
tema tanımı için `design-system.md`'ye bak — o dosya koddan türetilmiştir ve
ürünün içini anlatır; bu dosya ürünün dışarıya nasıl göründüğünü anlatır.

Karar tarihi: 2026-08-03.

## Nereden geldi

Üç kaynak vardı ve üçü birbirini tutmuyordu:

1. **2026-05-14 arşiv serisi** — logo + dev başlık + 3 madde + CTA + telefon
   mockup. Tanınır ama şablon; ayrıca mockup'lardaki arayüz AI ile
   uydurulmuştu ve açık temalıydı, yani olmayan bir ürünü gösteriyordu.
2. **2026-07 lifestyle serisi** — metinsiz, logosuz sinematik fotoğraflar.
   Güzel ama markasız: feed'e düşen biri "bu ne uygulaması?" sorusunu
   cevaplayamıyordu.
3. **Uygulama teması** — sadece dark tema, `#5A78FF` primary.

Altı sanat yönü denendi (3 saf + 3 karışım), ikisi seçildi. Amaç: arşivin
tanınırlığını korumak, ama kalıbı kopyalamak yerine ideavoll'a özgü bir imza
kurmak.

## İmza

Bu dört öğe **her kartta** bulunur ve markayı taşır. Hangi düzen kullanılırsa
kullanılsın feed tutarlı görünmesini bunlar sağlar.

| Öğe | Neden bu |
|---|---|
| **Konum halkaları** | Logo bir harita pini. Halkalar "yakınında" fikrinin görselleşmesi — dekorasyon değil, ürünün vaadi |
| **`ne zaman · nerede · kim var`** | Ürünün kendi verisi. Her kartta tekrar eden veri üçlüsü, kartı poster olmaktan çıkarıp "gerçek bir etkinlik" yapar |
| **Gerçek uygulama ekranı** | Telefon mockup'ına daima gerçek ekran görüntüsü konur, asla uydurma UI değil |
| **Logo + wordmark** | Sol üstte, `id`+turuncu `e`+`avoll` |

## Renk

Marka renkleri **logodan örneklendi** (`brand/logo.png`, alpha kompozit
sonrası piksel değerleri):

| Ad | Hex | Kullanım |
|---|---|---|
| Marka mavi | `#0370FB` | Başlık vurgusu, CTA, halkalar, pin |
| Marka turuncu | `#FD7201` | Tek kelimelik aksan, veri vurgusu, wordmark'taki `e` |
| Gece zemini | `#060E1C` | Koyu kartların arka planı |
| Kart yüzeyi | `#101B30` | Bilet/davetiye objesi |
| Yumuşak metin | `#93A1B8` | Alt metinler |

Uygulama primary'si `#5A78FF` ile logo mavisi `#0370FB` farklıdır — bu kasıtlı
değil, tarihsel. Pazarlama görsellerinde **logo mavisi** esastır; `#5A78FF`
zaten gömülü ekran görüntülerinde görünür.

## Tipografi

Pazarlama içeriği uygulamanın sistem fontunu (SF Pro) kullanmaz — nötr kalıyor
ve markaya kişilik katmıyordu.

| Rol | Font | Not |
|---|---|---|
| Başlık | **Bricolage Grotesque** 800 | Sıkı, enerjik, karakterli. `letter-spacing: -0.045em` |
| Gövde | **Inter** 400/600 | Okunabilirlik |
| Veri | **JetBrains Mono** 700 | Bilet satırları, sayaç, damga |
| Afiş alternatifi | **Archivo** 900 | Sadece çok geniş/ağır başlık gerektiğinde |

Dördü de Türkçe glifleri (ğ, ı, İ, ş, ç, ö, ü) tam destekliyor — doğrulandı.
Fontlar `templates/brand-card/fonts/` altında gömülüdür.

**ALL CAPS kullanma.** Türkçe'de uzun kelimelerde okunabilirliği düşürür ve
`I`/`İ` ayrımı riski taşır. Sadece kısa etiketlerde (üst damga, veri başlığı)
serbest.

## İki kart çizgisi

**Afiş** (`card_afis.html`) — fotoğraf tam kaplar, dev başlık üstüne biner,
cam veri şeridi. Küçük ekranda en güçlü duran. Kullanım: reklam kreatifi,
dikkat çekmesi gereken organik post.

**Davetiye** (`card_davetiye.html`) — gece zemini, yayılan halkalar, bilet
objesi. Ürünü ve etkinliği aynı karede anlatır. Kullanım: özellik/anlatım
postları, yeni kullanıcıya "bu ne?" sorusunu cevaplayan içerik.

İkisi de aynı imzayı taşıdığı için feed'de karışık kullanılabilir.

## İçerik ritmi

- **Haftada 2-3 lifestyle fotoğraf** — metinsiz, duygusal, relatable
- **Ayda 2-3 marka kartı** — yukarıdaki iki çizgiden

Sebep: sadece lifestyle marka bırakmıyor, sadece kart feed'i reklam panosuna
çeviriyor.

## Üretim

Görseller **AI ile değil, HTML/CSS + Chrome** ile üretilir. Gerekçe ve
kullanım: `templates/brand-card/README.md`.

AI'ın rolü, kartların içine giren **lifestyle fotoğrafları** üretmekle sınırlı
(Higgsfield/Gemini). Metin, logo ve arayüz asla AI'a çizdirilmez.
