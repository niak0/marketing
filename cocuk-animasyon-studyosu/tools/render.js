#!/usr/bin/env node
// Bir projeyi MP4'e çevirir: HTML sahnesini kare kare çeker, müziği üretir, ffmpeg ile birleştirir.
// Kullanım: node tools/render.js projeler/<proje> [--fps 30] [--test]
//   --test : sadece birkaç kontrol karesi çeker (projeler/<proje>/kontrol/*.png)
const { chromium } = require('playwright');
const { execFileSync } = require('child_process');
const fs = require('fs'), path = require('path'), os = require('os');

const args = process.argv.slice(2);
const dir = path.resolve(args.find(a => !a.startsWith('--')) || '');
if (!fs.existsSync(path.join(dir, 'index.html'))) { console.error('Kullanım: node tools/render.js projeler/<proje>'); process.exit(1); }
const fps = +(args[args.indexOf('--fps') + 1] || 30) || 30;
const test = args.includes('--test');
const name = path.basename(dir);

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 1.5 });
  page.on('pageerror', e => console.error('Sayfa hatası:', e.message));
  await page.goto('file://' + path.join(dir, 'index.html') + '?record');
  await page.evaluate(() => document.fonts.ready);
  const DUR = await page.evaluate(() => window.DUR);

  if (test) {
    const out = path.join(dir, 'kontrol'); fs.mkdirSync(out, { recursive: true });
    const times = Array.from({ length: 12 }, (_, i) => +(((i + 0.5) / 12) * DUR).toFixed(2));
    for (const t of times) { await page.evaluate(t => render(t), t); await page.screenshot({ path: path.join(out, `t_${t}.png`) }); }
    await browser.close(); console.log('Kontrol kareleri:', out); return;
  }

  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'anim-'));
  const N = Math.round(DUR * fps);
  for (let i = 0; i < N; i++) {
    await page.evaluate(t => render(t), i / fps);
    await page.screenshot({ path: path.join(tmp, `f_${String(i).padStart(5, '0')}.png`) });
    if (i % fps === 0) process.stdout.write(`\r${i}/${N} kare`);
  }
  await browser.close();
  console.log(`\r${N}/${N} kare`);

  const wav = path.join(tmp, 'music.wav');
  const hasMusic = fs.existsSync(path.join(dir, 'music.py'));
  if (hasMusic) execFileSync('python3', [path.join(dir, 'music.py'), wav, String(DUR)], { stdio: 'inherit' });
  const mp4 = path.join(dir, `${name}.mp4`);
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-framerate', String(fps), '-i', path.join(tmp, 'f_%05d.png'),
    ...(hasMusic ? ['-i', wav, '-c:a', 'aac', '-b:a', '160k', '-shortest'] : []),
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-vf', 'scale=1920:1080', mp4], { stdio: 'inherit' });
  fs.rmSync(tmp, { recursive: true, force: true });
  console.log('Hazır:', mp4);
})();
