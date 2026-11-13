// node tools/render.mjs START END OUT.mp4   (renders www/stage2 with build_quote/quote_tl.json; needs playwright + ffmpeg)
import http from 'http'; import fs from 'fs'; import path from 'path'; import { spawn } from 'child_process';
import { createRequire } from 'module';
const { chromium } = createRequire(import.meta.url)('playwright');
const ROOT = path.resolve('www'), FPS = 30;
const TYPES = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.ttf': 'font/ttf', '.json': 'application/json', '.jpg': 'image/jpeg', '.png': 'image/png' };
const srv = http.createServer((req, res) => {
  const p = path.join(ROOT, decodeURIComponent(req.url.split('?')[0]));
  fs.readFile(p, (e, d) => { if (e) { res.writeHead(404); res.end(); return; } res.writeHead(200, { 'Content-Type': TYPES[path.extname(p)] || 'application/octet-stream' }); res.end(d); });
}).listen(0);
const port = srv.address().port;
const browser = await chromium.launch({ args: ['--force-color-profile=srgb', '--disable-lcd-text', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
const page = await (await browser.newContext({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 })).newPage();
const errs = [];
page.on('pageerror', e => errs.push('PAGE ' + e.message));
page.on('console', m => { if (m.type() === 'error') errs.push('CONSOLE ' + m.text()); });
await page.goto(`http://127.0.0.1:${port}/quote/index.html`);
const tl = JSON.parse(fs.readFileSync('build_quote/quote_tl.json', 'utf8'));
const nscn = await page.evaluate(() => window.READY); const nseg = await page.evaluate(tl => init(tl), tl);
console.log('segments', nseg, 'scenes loaded', nscn);
const start = +process.argv[2], end = Math.min(+process.argv[3], tl.T), out = process.argv[4];
const f0 = Math.round(start * FPS), f1 = Math.round(end * FPS);
const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
  '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17', '-pix_fmt', 'yuv420p', '-r', String(FPS), out], { stdio: ['pipe', 'inherit', 'inherit'] });
const t0 = Date.now();
for (let f = f0; f < f1; f++) {
  await page.evaluate(t => frame(t), f / FPS);
  const buf = await page.screenshot({ type: 'jpeg', quality: 92 });
  if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
  if ((f - f0) % 300 === 0) console.log(`${out} ${f - f0}/${f1 - f0} ${((Date.now() - t0) / 1000).toFixed(0)}s`);
}
ff.stdin.end(); await new Promise(r => ff.on('close', r));
console.log('done', out, ((Date.now() - t0) / 1000).toFixed(0) + 's', 'errors', errs.length, errs.slice(0, 3).join(' | '));
await browser.close(); srv.close();
