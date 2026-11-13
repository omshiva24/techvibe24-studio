// node stills.mjs out_prefix t1,t2,...   (renders single frames from www/news for review)
import http from 'http'; import fs from 'fs'; import path from 'path';
import { createRequire } from 'module';
const { chromium } = createRequire(import.meta.url)('playwright');
const ROOT = path.resolve('www');
const TYPES = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.ttf': 'font/ttf', '.json': 'application/json', '.jpg': 'image/jpeg', '.png': 'image/png' };
const srv = http.createServer((req, res) => { const p = path.join(ROOT, decodeURIComponent(req.url.split('?')[0])); fs.readFile(p, (e, d) => { if (e) { res.writeHead(404); res.end(); return; } res.writeHead(200, { 'Content-Type': TYPES[path.extname(p)] || 'application/octet-stream' }); res.end(d); }); }).listen(0);
const browser = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
const page = await (await browser.newContext({ viewport: { width: 1080, height: 1920 } })).newPage();
const errs = []; page.on('pageerror', e => errs.push('PAGE ' + e.message)); page.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') errs.push(m.type() + ' ' + m.text()); });
await page.goto(`http://127.0.0.1:${srv.address().port}/quote/index.html`);
const n = await page.evaluate(() => window.READY); const tl = JSON.parse(fs.readFileSync('build_quote/quote_tl.json', 'utf8')); await page.evaluate(tl => init(tl), tl);
const ts = process.argv[3].split(',').map(Number); const t0 = Date.now();
for (const t of ts) { await page.evaluate(t => frame(t), t); await page.screenshot({ path: `${process.argv[2]}_${t.toFixed(2)}.jpg`, type: 'jpeg', quality: 85 }); }
console.log('scenes', n, 'ms/frame', ((Date.now() - t0) / ts.length).toFixed(0), 'errors', errs.slice(0, 8));
await browser.close(); srv.close();
