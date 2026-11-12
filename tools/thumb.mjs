// node tools/thumb.mjs OUT.jpg   (www/thumb/frame.jpg must exist)
import http from 'http'; import fs from 'fs'; import path from 'path';
import { chromium } from 'playwright';
const ROOT = path.resolve('www');
const srv = http.createServer((q, s) => { const p = path.join(ROOT, decodeURIComponent(q.url.split('?')[0])); fs.readFile(p, (e, d) => { if (e) { s.writeHead(404); s.end(); return; } s.end(d); }); }).listen(0);
const b = await chromium.launch(); const pg = await (await b.newContext({ viewport: { width: 1280, height: 720 } })).newPage();
await pg.goto(`http://127.0.0.1:${srv.address().port}/thumb/thumb.html`); await pg.evaluate(() => document.fonts.ready); await pg.waitForTimeout(500);
await pg.screenshot({ path: process.argv[2], type: 'jpeg', quality: 92 });
await b.close(); srv.close();
