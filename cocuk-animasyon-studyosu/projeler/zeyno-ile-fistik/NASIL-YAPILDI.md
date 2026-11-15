# Zeyno ile Fıstık: Parkta Bir Gün — Nasıl Yapıldı

Komşu zürafa (Zeyno) ile fil yavrusu (Fıstık) parka gidip oynuyor.
34 sn, 16:9, 1080p, müzikli. İlk istek: "komşu olan zürafa ve fil yavrusu
parka gidip oyun oynar, bunu animasyonlaştırabilir misin?"

## Sahneler (`SCENES = [0, 6, 11, 17, 23, 29, 34]`)

| # | Süre | Ne oluyor |
|---|---|---|
| 1 | 0–6 | Başlık kartı → iki ev; ikisi kapıdan çıkıp buluşur, "Günaydın" balonları, duman tüter |
| 2 | 6–11 | Yol: karakterler yerinde yürür, ağaçlar sola kayar (sonsuz döngü), kelebek, PARK tabelası |
| 3 | 11–17 | Salıncak: sarkaç açısı `28°·sin`, fil oturağa bağlı; zürafa boynuyla iter |
| 4 | 17–23 | Kaydırak: merdiven tırmanışı → iki Bezier eğrisi boyunca kayış (açı eğimden) → kum bulutu |
| 5 | 23–29 | Top: kafa ↔ hortum arasında parabol; hortum topa yaklaşınca kalkar; su püskürtme → gökkuşağı |
| 6 | 29–34 | Gün batımı gökyüzü, vedalaşma, kalpler, eve dönüş, pencere ışıkları, "SON" |

## Teknik notlar

- Tek SVG; tüm sahne grupları aynı anda DOM'da, `render(t)` her karede hangisinin
  görüneceğini `display/opacity` ile seçer. Karakterler sahneler arası paylaşılır.
- Zürafa: gövde elips + benekler, 4 bacak (`g-leg-*`, pivot üst uç), boyun grubu
  `g-neck` (pivot 62,-160) içinde baş `g-head`. Boyun dönmesi = selam/itme/kafa vuruşu.
- Fil: gövde elips, baş `e-head`, kulak `e-ear`, hortum `e-trunk` (pivot 88,-94).
  Hortum `-130°`'ye kadar kalkar; daha fazlası ters döner (sınır `Math.min`).
- Kaydırak yolu: `bez()` kübik Bezier; açı = sonraki noktaya `atan2`, sola baktığı
  için `-180°` düzeltmesi.
- Su damlaları: hortum ucundan sabit hız + yerçekimi (`520·u²`), faz kaydırmalı döngü.
- Müzik: `music.py` — bell sesi melodi (harmoniklerle sinüs) + bas/akor, sonda 2.5 sn fade.
- Font: Bricolage Grotesque (`bricolage.woff2`, yerel; Türkçe karakter destekli).

## İlk turda düzeltilen hatalar (kontrol karelerinden)

- Salıncak A-çerçevesi siyah dolu çıkıyordu → path grubuna `fill="none"`.
- Hortum su püskürtürken -270°'ye dönüp aşağı bakıyordu → açı sınırlandı,
  su çıkış noktası hortum ucunun gerçek konumuna taşındı.
- Su damlaları gökyüzünde görünmüyordu → koyu mavi + beyaz kontur.

## Fikirler (sonraki sürüm)

- Dikey 9:16 versiyon (viewBox 720×1280, sahneler yeniden kadraj).
- Seslendirme (TTS) + damla/kayma/top ses efektleri.
- Karakter isimleri/hikâye çocukla birlikte seçilebilir.
