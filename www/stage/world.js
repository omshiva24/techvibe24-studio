// Scenery, props and effects for the story. All motion comes from the time argument.
const W = 1080, H = 1920, GROUND = 1120;
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const ease = (x) => { x = clamp(x); return x * x * (3 - 2 * x); };
const easeOut = (x) => 1 - Math.pow(1 - clamp(x), 3);
const lerp = (a, b, t) => a + (b - a) * t;
function rng(seed) { return () => { seed |= 0; seed = seed + 0x6D2B79F5 | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
function mkCanvas(w, h) { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; }
const CACHE = {};
function cached(key, w, h, draw) { if (!CACHE[key]) { const cv = mkCanvas(w, h); draw(cv.getContext('2d')); CACHE[key] = cv; } return CACHE[key]; }
function glowSprite(r, stops) { const c = mkCanvas(r * 2, r * 2), x = c.getContext('2d'); const g = x.createRadialGradient(r, r, 0, r, r, r); stops.forEach(([o, col]) => g.addColorStop(o, col)); x.fillStyle = g; x.fillRect(0, 0, r * 2, r * 2); return c; }
const G_GOLD = glowSprite(256, [[0, 'rgba(255,245,200,1)'], [0.2, 'rgba(255,205,100,.75)'], [0.55, 'rgba(255,140,30,.22)'], [1, 'rgba(255,100,0,0)']]);
const G_WHITE = glowSprite(128, [[0, 'rgba(255,255,245,1)'], [0.3, 'rgba(255,240,200,.55)'], [1, 'rgba(255,220,150,0)']]);
const G_EMBER = glowSprite(32, [[0, 'rgba(255,240,180,1)'], [0.35, 'rgba(255,150,30,.7)'], [1, 'rgba(255,80,0,0)']]);
const G_GREEN = glowSprite(32, [[0, 'rgba(240,255,210,1)'], [0.35, 'rgba(120,255,140,.75)'], [1, 'rgba(40,200,80,0)']]);
const G_BLUE = glowSprite(128, [[0, 'rgba(235,245,255,1)'], [0.3, 'rgba(150,200,255,.55)'], [1, 'rgba(80,120,255,0)']]);
const G_CLOUD = glowSprite(128, [[0, 'rgba(255,250,245,.95)'], [0.5, 'rgba(255,240,230,.55)'], [1, 'rgba(255,235,220,0)']]);
const G_DARK = glowSprite(128, [[0, 'rgba(20,0,30,.9)'], [0.5, 'rgba(30,0,40,.5)'], [1, 'rgba(30,0,40,0)']]);
function glow(c, spr, x, y, r, a = 1) { c.save(); c.globalAlpha = a; c.globalCompositeOperation = 'lighter'; c.drawImage(spr, x - r, y - r, r * 2, r * 2); c.restore(); }

// ---------- skies ----------
const SKY = {
  dawn:    ['#1c1040', '#6b2d6b', '#e8590c', '#ffc078'],
  day:     ['#1971c2', '#4dabf7', '#a5d8ff', '#fff3bf'],
  sunset:  ['#2b0a3d', '#a61e4d', '#f76707', '#ffd43b'],
  night:   ['#02030f', '#0b1640', '#1c2f6b', '#3b4a8a'],
  divine:  ['#3d0c02', '#a83a0a', '#ff922b', '#fff3bf'],
  storm:   ['#0b0b14', '#1f1f33', '#3a3a55', '#5c5c7a'],
  lanka:   ['#1a0000', '#5c0a00', '#c92a2a', '#ff8c1a'],
  cosmic:  ['#05010f', '#1e0b3d', '#4a1a7a', '#a64dff'],
  temple:  ['#2a0a00', '#7a1f00', '#e8590c', '#ffd8a8'],
  heaven:  ['#fff4e6', '#ffd8a8', '#ffc078', '#fff9db'],
};
function sky(c, name, mix = null, m = 0) {
  const a = SKY[name], b = mix ? SKY[mix] : null;
  const col = (i) => b ? mixHex(a[i], b[i], m) : a[i];
  const g = c.createLinearGradient(0, 0, 0, H * 0.72);
  g.addColorStop(0, col(0)); g.addColorStop(0.35, col(1)); g.addColorStop(0.75, col(2)); g.addColorStop(1, col(3));
  c.fillStyle = g; c.fillRect(0, 0, W, H);
}
function mixHex(a, b, t) { const p = (h) => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16)); const A = p(a), B = p(b); return `rgb(${A.map((v, i) => Math.round(lerp(v, B[i], t))).join(',')})`; }

const STARS = (() => { const r = rng(5); return Array.from({ length: 260 }, () => [r() * W, r() * H * 0.62, r() * 2 + 0.5, r() * 6.28, 0.5 + r() * 2]); })();
function stars(c, t, a = 1) { c.save(); c.fillStyle = '#fff8e6'; STARS.forEach(([x, y, r, ph, sp]) => { c.globalAlpha = a * (0.35 + 0.65 * (0.5 + 0.5 * Math.sin(t * sp + ph))); c.fillRect(x, y, r, r); }); c.restore(); }
function sun(c, x, y, r, t, a = 1, col = ['#fffbe6', '#ffd43b', '#ff922b', '#f76707']) {
  glow(c, G_GOLD, x, y, r * 3.2, 0.9 * a);
  c.save(); c.globalAlpha = a; c.globalCompositeOperation = 'lighter'; c.translate(x, y); c.rotate(t * 0.05);
  for (let i = 0; i < 24; i++) { c.rotate(Math.PI / 12); const L = r * (1.7 + 0.25 * Math.sin(t * 2 + i * 1.7)); const g = c.createLinearGradient(0, r, 0, L); g.addColorStop(0, 'rgba(255,210,100,.45)'); g.addColorStop(1, 'rgba(255,150,0,0)'); c.fillStyle = g; c.beginPath(); c.moveTo(-r * 0.12, r * 0.95); c.lineTo(0, L); c.lineTo(r * 0.12, r * 0.95); c.fill(); }
  c.restore();
  c.save(); c.globalAlpha = a; const g = c.createRadialGradient(x - r * 0.3, y - r * 0.3, r * 0.05, x, y, r);
  g.addColorStop(0, col[0]); g.addColorStop(0.45, col[1]); g.addColorStop(0.85, col[2]); g.addColorStop(1, col[3]); c.fillStyle = g; c.beginPath(); c.arc(x, y, r, 0, 7); c.fill(); c.restore();
}
function moon(c, x, y, r, a = 1) {
  glow(c, G_WHITE, x, y, r * 3, 0.55 * a);
  c.save(); c.globalAlpha = a; const g = c.createRadialGradient(x - r * 0.3, y - r * 0.3, 1, x, y, r); g.addColorStop(0, '#ffffff'); g.addColorStop(0.7, '#fff3d6'); g.addColorStop(1, '#e6c98f');
  c.fillStyle = g; c.beginPath(); c.arc(x, y, r, 0, 7); c.fill(); c.restore();
}
function clouds(c, t, y, a = 0.6, speed = 8, seed = 1, n = 7, tint = null) {
  const r = rng(seed); c.save(); c.globalAlpha = a;
  for (let i = 0; i < n; i++) {
    const w = 260 + r() * 260, x0 = r() * (W + 600) - 300, yy = y + (r() - 0.5) * 120;
    const x = ((x0 + t * speed * (0.6 + r())) % (W + 700)) - 350;
    for (let k = 0; k < 5; k++) { const rr = w * (0.25 + r() * 0.2); c.drawImage(G_CLOUD, x + (k - 2) * w * 0.18 - rr, yy - rr * 0.55 + (r() - 0.5) * 30, rr * 2, rr * 1.1); }
  }
  if (tint) { c.globalCompositeOperation = 'source-atop'; }
  c.restore();
}
function hills(c, key, base, layers, t = 0, shift = 0) {
  // layers: [[color, height, roughness, seed]]
  layers.forEach(([col, h, rough, seed], i) => {
    const img = cached(`hill_${key}_${i}`, W + 400, 700, (x) => {
      const r = rng(seed); x.fillStyle = col; x.beginPath(); x.moveTo(0, 700);
      let y = 700 - h * (0.5 + r() * 0.5);
      for (let px = 0; px <= W + 400; px += 40) { y += (r() - 0.5) * rough; y = Math.max(700 - h * 1.1, Math.min(700 - h * 0.35, y)); x.lineTo(px, y); }
      x.lineTo(W + 400, 700); x.closePath(); x.fill();
    });
    c.drawImage(img, -200 + shift * (i + 1) * 0.5, base - 700 + 4);
  });
}
function ground(c, y, top, bottom) { const g = c.createLinearGradient(0, y, 0, H); g.addColorStop(0, top); g.addColorStop(1, bottom); c.fillStyle = g; c.fillRect(0, y, W, H - y); }
function ocean(c, t, hz, moonX = null) {
  for (let k = 0; k < 7; k++) {
    const y0 = hz + k * 48, amp = 8 + k * 5, f = 0.012 - k * 0.001, sp = 0.8 + k * 0.3;
    c.beginPath(); c.moveTo(0, H);
    for (let x = 0; x <= W; x += 12) c.lineTo(x, y0 + Math.sin(x * f + t * sp + k) * amp + Math.sin(x * f * 2.3 - t * sp * 1.3) * amp * 0.35);
    c.lineTo(W, H); c.closePath();
    const g = c.createLinearGradient(0, y0 - 20, 0, H); g.addColorStop(0, ['#3e8fb5', '#2d7aa0', '#226287', '#1a4d6d', '#123a54', '#0b2a3e', '#082033'][k]); g.addColorStop(1, '#041320');
    c.fillStyle = g; c.fill(); c.strokeStyle = `rgba(255,230,170,${0.32 - k * 0.04})`; c.lineWidth = 2; c.stroke();
  }
  if (moonX !== null) { c.save(); c.globalCompositeOperation = 'lighter'; for (let i = 0; i < 24; i++) { const y = hz + 14 + i * 14, w = 90 - i * 2 + 30 * Math.sin(t * 2 + i); c.fillStyle = `rgba(255,230,170,${0.25 - i * 0.009})`; c.fillRect(moonX - w / 2 + Math.sin(t * 1.7 + i * 0.8) * 14, y, w, 3); } c.restore(); }
}
function river(c, t, y) {
  const g = c.createLinearGradient(0, y, 0, y + 160); g.addColorStop(0, '#ffb35c'); g.addColorStop(1, '#7a3b10');
  c.fillStyle = g; c.beginPath(); c.moveTo(0, y + 30); c.quadraticCurveTo(W / 2, y - 20, W, y + 20); c.lineTo(W, y + 160); c.lineTo(0, y + 160); c.fill();
  c.save(); c.globalCompositeOperation = 'lighter'; for (let i = 0; i < 18; i++) { const yy = y + 30 + i * 7, w = 140 + 60 * Math.sin(t + i); c.fillStyle = 'rgba(255,230,160,.18)'; c.fillRect(W / 2 - w / 2 + Math.sin(t * 1.5 + i) * 40, yy, w, 2); } c.restore();
}
// ---------- buildings & nature ----------
function tree(c, x, y, s, t, seed = 3, fruit = 0, leaf = '#1d3b12', leaf2 = '#2b5a1a') {
  c.save(); c.translate(x, y); c.scale(s, s);
  c.fillStyle = '#2a1405'; c.strokeStyle = '#140800'; c.lineWidth = 3;
  c.beginPath(); c.moveTo(-26, 0); c.bezierCurveTo(-18, -120, -30, -200, -10, -280); c.lineTo(14, -280); c.bezierCurveTo(26, -200, 16, -120, 30, 0); c.closePath(); c.fill(); c.stroke();
  c.lineWidth = 14; c.lineCap = 'round'; c.strokeStyle = '#2a1405';
  [[-10, -220, -150, -300], [10, -240, 160, -330], [0, -270, -40, -390], [8, -180, 140, -200]].forEach(([a, b, x2, y2]) => { c.beginPath(); c.moveTo(a, b); c.quadraticCurveTo((a + x2) / 2, y2 + 40, x2, y2); c.stroke(); });
  const r = rng(seed);
  const blobs = Array.from({ length: 26 }, () => [(r() - 0.5) * 420, -300 - r() * 200 + Math.abs(r() - 0.5) * 80, 50 + r() * 50, r()]);
  blobs.forEach(([bx, by, br, k]) => { const sw = Math.sin(t * 1.2 + bx * 0.02) * 4; c.fillStyle = k > 0.5 ? leaf : leaf2; c.beginPath(); c.arc(bx + sw, by, br, 0, 7); c.fill(); });
  if (fruit > 0) blobs.forEach(([bx, by, br, k], i) => { if (i % 2) return; c.save(); c.globalAlpha = fruit; glow(c, G_GOLD, bx + 10, by + br * 0.4, 26, 0.8); c.fillStyle = '#ffd43b'; c.beginPath(); c.arc(bx + 10, by + br * 0.4, 9, 0, 7); c.fill(); c.restore(); });
  c.restore();
}
function palace(c, x, y, s, col = '#2a0a00', glowA = 0.6, t = 0) {
  c.save(); c.translate(x, y); c.scale(s, s); c.fillStyle = col;
  c.fillRect(-300, -160, 600, 160);
  [[-300, 120], [-150, 150], [0, 210], [150, 150], [300, 120]].forEach(([px, h]) => {
    c.fillRect(px - 50, -160 - h * 0.6, 100, h * 0.6);
    c.beginPath(); c.moveTo(px - 60, -160 - h * 0.6); c.quadraticCurveTo(px, -160 - h * 1.35, px + 60, -160 - h * 0.6); c.fill();
    c.fillRect(px - 2, -160 - h * 1.35 - 26, 4, 30);
  });
  c.fillStyle = `rgba(255,190,80,${glowA})`;
  for (let i = -5; i <= 5; i++) { if (i === 0) continue; c.beginPath(); c.moveTo(i * 50 - 10, -40); c.lineTo(i * 50 - 10, -80); c.quadraticCurveTo(i * 50, -100, i * 50 + 10, -80); c.lineTo(i * 50 + 10, -40); c.fill(); }
  // big doorway
  c.fillStyle = `rgba(255,200,90,${glowA + 0.2})`; c.beginPath(); c.moveTo(-40, 0); c.lineTo(-40, -90); c.quadraticCurveTo(0, -150, 40, -90); c.lineTo(40, 0); c.fill();
  c.restore();
}
function temple(c, x, y, s, t, col = '#2a0a00') {
  c.save(); c.translate(x, y); c.scale(s, s); c.fillStyle = col;
  c.fillRect(-160, -90, 320, 90); c.fillRect(-120, -130, 240, 40);
  c.beginPath(); c.moveTo(-100, -130); c.bezierCurveTo(-90, -260, -40, -380, 0, -420); c.bezierCurveTo(40, -380, 90, -260, 100, -130); c.fill();
  for (let i = 1; i < 6; i++) { c.strokeStyle = 'rgba(255,170,60,.25)'; c.lineWidth = 2; c.beginPath(); c.moveTo(-100 + i * 6, -130 - i * 45); c.lineTo(100 - i * 6, -130 - i * 45); c.stroke(); }
  c.beginPath(); c.arc(0, -425, 14, 0, 7); c.fill(); c.fillRect(-2, -500, 4, 80);
  // saffron flag
  const N = 14; c.fillStyle = '#ff7a00'; c.beginPath(); c.moveTo(2, -500);
  for (let i = 0; i <= N; i++) { const u = i / N; c.lineTo(2 + u * 110, -500 + u * 26 + Math.sin(u * 5 - t * 5) * 8 * u); }
  for (let i = N; i >= 0; i--) { const u = i / N; c.lineTo(2 + u * 110, -440 - u * 26 + Math.sin(u * 5 - t * 5) * 8 * u); }
  c.fill();
  c.fillStyle = 'rgba(255,200,90,.85)'; c.beginPath(); c.moveTo(-30, 0); c.lineTo(-30, -60); c.quadraticCurveTo(0, -100, 30, -60); c.lineTo(30, 0); c.fill();
  c.restore();
}
function lankaCity(c, t, base, burning = 0) {
  const r = rng(51); const B = []; let x = 40; while (x < 1040) { const w = 50 + r() * 80, h = 120 + r() * 240; B.push([x, w, h, r() < 0.45 ? 'dome' : r() < 0.6 ? 'spire' : 'flat', r()]); x += w * 0.85; }
  c.save(); c.globalCompositeOperation = 'lighter';
  if (burning > 0) for (let i = 0; i < 40; i++) { const fx = 40 + i * 25, h = (200 + 160 * (0.5 + 0.5 * Math.sin(t * 3 + i * 1.7))) * burning; flame(c, fx, base - 120, 40, h, t + i, 0.7); }
  c.restore();
  c.fillStyle = '#1a0300';
  c.beginPath(); c.moveTo(0, H); c.lineTo(0, base + 40); c.quadraticCurveTo(W / 2, base - 70, W, base + 40); c.lineTo(W, H); c.fill();
  B.forEach(([bx, w, h, kind, k], i) => {
    const y = base + 20 - Math.sin(bx / W * Math.PI) * 70; c.fillStyle = '#2b0800';
    c.fillRect(bx, y - h, w, h);
    if (kind === 'dome') { c.beginPath(); c.arc(bx + w / 2, y - h, w / 2, Math.PI, 0); c.fill(); c.fillRect(bx + w / 2 - 2, y - h - w / 2 - 26, 4, 26); }
    if (kind === 'spire') { c.beginPath(); c.moveTo(bx, y - h); c.lineTo(bx + w / 2, y - h - w * 1.3); c.lineTo(bx + w, y - h); c.fill(); }
    c.fillStyle = '#ffcf40'; c.globalAlpha = 0.35; c.fillRect(bx, y - h, w, 4); c.globalAlpha = 1;   // gold edge (Lanka is golden)
    for (let rr = 0; rr < Math.floor(h / 50); rr++) { const fl = 0.5 + 0.5 * Math.sin(t * 8 + i * 3 + rr); c.fillStyle = `rgba(255,${150 + 70 * fl},50,${0.45 + 0.4 * fl})`; c.fillRect(bx + w / 2 - 6, y - h + 22 + rr * 50, 12, 18); }
  });
  if (burning > 0) { c.save(); c.globalCompositeOperation = 'lighter'; for (let i = 0; i < 26; i++) { const fx = 60 + i * 38; flame(c, fx, base - 30 - Math.sin(fx / W * Math.PI) * 70, 34, (140 + 120 * (0.5 + 0.5 * Math.sin(t * 4 + i))) * burning, t * 1.3 + i, 0.6); } c.restore(); }
}
function flame(c, x, y, w, h, t, a = 0.7) {
  const sway = Math.sin(t * 2.4) * w * 0.4;
  const g = c.createLinearGradient(0, y, 0, y - h); g.addColorStop(0, `rgba(255,235,140,${a})`); g.addColorStop(0.35, `rgba(255,140,20,${a * 0.8})`); g.addColorStop(1, 'rgba(200,30,0,0)');
  c.fillStyle = g; c.beginPath(); c.moveTo(x - w, y); c.quadraticCurveTo(x - w * 0.8 + sway * 0.3, y - h * 0.5, x + sway, y - h); c.quadraticCurveTo(x + w * 0.8 + sway * 0.3, y - h * 0.5, x + w, y); c.fill();
}
function kailash(c, t) {
  c.save(); c.fillStyle = '#c5d3e8';
  c.beginPath(); c.moveTo(80, GROUND); c.lineTo(380, 520); c.lineTo(460, 470); c.lineTo(540, 360); c.lineTo(620, 470); c.lineTo(720, 520); c.lineTo(1000, GROUND); c.fill();
  c.fillStyle = '#ffffff'; c.beginPath(); c.moveTo(380, 520); c.lineTo(460, 470); c.lineTo(540, 360); c.lineTo(620, 470); c.lineTo(720, 520); c.lineTo(640, 560); c.lineTo(560, 520); c.lineTo(480, 580); c.lineTo(420, 540); c.fill();
  c.fillStyle = 'rgba(80,100,140,.35)'; c.beginPath(); c.moveTo(540, 360); c.lineTo(620, 470); c.lineTo(1000, GROUND); c.lineTo(600, GROUND); c.fill();
  c.restore();
}
function mountainProp(c, x, y, s, t, herbs = 1) {
  c.save(); c.translate(x, y); c.scale(s, s);
  const g = c.createLinearGradient(0, -150, 0, 60); g.addColorStop(0, '#9fb070'); g.addColorStop(0.5, '#3f5a22'); g.addColorStop(1, '#1a2608');
  c.fillStyle = g; c.strokeStyle = '#142006'; c.lineWidth = 3;
  c.beginPath(); c.moveTo(-160, 40); c.lineTo(-110, -40); c.lineTo(-70, -20); c.lineTo(-20, -130); c.lineTo(20, -90); c.lineTo(60, -150); c.lineTo(110, -50); c.lineTo(160, 40); c.quadraticCurveTo(0, 110, -160, 40); c.closePath(); c.fill(); c.stroke();
  c.fillStyle = '#fff'; c.beginPath(); c.moveTo(60, -150); c.lineTo(80, -110); c.lineTo(62, -116); c.lineTo(46, -104); c.lineTo(40, -120); c.fill();
  const r = rng(77); for (let i = 0; i < 26; i++) { const hx = (r() - 0.5) * 260, hy = -r() * 110 + 20; glow(c, G_GREEN, hx, hy, 12 + 6 * Math.sin(t * 4 + i), herbs * (0.6 + 0.4 * Math.sin(t * 3 + i))); }
  c.restore();
}
function boulder(c, x, y, s) {
  c.save(); c.translate(x, y); c.scale(s, s);
  const g = c.createRadialGradient(-40, -60, 10, 0, 0, 160); g.addColorStop(0, '#8d7b6b'); g.addColorStop(1, '#3a2c22');
  c.fillStyle = g; c.strokeStyle = '#1e140c'; c.lineWidth = 4;
  c.beginPath(); c.moveTo(-150, 20); c.bezierCurveTo(-170, -90, -60, -150, 20, -140); c.bezierCurveTo(120, -130, 170, -60, 150, 20); c.bezierCurveTo(100, 60, -100, 60, -150, 20); c.fill(); c.stroke();
  c.restore();
}
function diya(c, x, y, s, t) {
  c.save(); c.translate(x, y); c.scale(s, s);
  c.fillStyle = '#b35c00'; c.strokeStyle = '#4a1d00'; c.lineWidth = 2; c.beginPath(); c.moveTo(-26, 0); c.quadraticCurveTo(0, 24, 26, 0); c.quadraticCurveTo(10, -6, 30, -10); c.lineTo(-26, -6); c.closePath(); c.fill(); c.stroke();
  glow(c, G_GOLD, 22, -26, 70, 0.7 + 0.1 * Math.sin(t * 9));
  flame(c, 22, -8, 6, 30 + 4 * Math.sin(t * 11), t * 3, 1);
  c.restore();
}
function ring(c, x, y, r, t) { glow(c, G_GOLD, x, y, r * 4, 0.8); c.save(); c.strokeStyle = '#ffd43b'; c.lineWidth = r * 0.35; c.beginPath(); c.arc(x, y, r, 0, 7); c.stroke(); c.fillStyle = '#a5f3fc'; c.beginPath(); c.arc(x, y - r, r * 0.35, 0, 7); c.fill(); c.restore(); }
function chains(c, x, y, s, broken, t) {
  c.save(); c.translate(x, y); c.scale(s, s); c.strokeStyle = '#868e96'; c.lineWidth = 6;
  for (let side of [-1, 1]) for (let i = 0; i < 6; i++) {
    const off = broken * (40 + i * 30) * side, fall = broken * broken * i * 40;
    c.save(); c.translate(side * (40 + i * 26) + off, -120 + i * 10 + fall); c.rotate(side * 0.4 + broken * i * 0.5 * side); c.beginPath(); c.ellipse(0, 0, 16, 9, 0, 0, 7); c.stroke(); c.restore();
  }
  c.restore();
}
function mala(c, x, y, r, t, n = 54) {
  c.save(); c.translate(x, y); c.rotate(t * 0.6);
  for (let i = 0; i < n; i++) { const a = i / n * Math.PI * 2; c.fillStyle = i % 9 ? '#c2410c' : '#ffd43b'; c.beginPath(); c.arc(Math.cos(a) * r, Math.sin(a) * r, i % 9 ? 9 : 12, 0, 7); c.fill(); }
  c.restore();
}
function glyph(c, txt, x, y, size, a = 1, col = '#ffd43b') { c.save(); c.globalAlpha = a; c.font = `${size}px Yatra`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.shadowColor = 'rgba(255,170,40,.9)'; c.shadowBlur = size * 0.25; c.fillStyle = col; c.fillText(txt, x, y); c.restore(); }
// ---------- effects ----------
function rays(c, x, y, t, a = 0.5, n = 18, col = '255,215,140') {
  c.save(); c.globalCompositeOperation = 'lighter'; c.translate(x, y); c.rotate(t * 0.04);
  const g = c.createRadialGradient(0, 0, 0, 0, 0, 1400); g.addColorStop(0, `rgba(${col},${0.35 * a})`); g.addColorStop(0.4, `rgba(${col},${0.12 * a})`); g.addColorStop(1, `rgba(${col},0)`);
  c.fillStyle = g; for (let i = 0; i < n; i++) { const an = i / n * Math.PI * 2, w = 0.06 + (i % 3) * 0.025; c.beginPath(); c.moveTo(0, 0); c.arc(0, 0, 1400, an - w, an + w); c.fill(); }
  c.restore();
}
const PET = (() => { const r = rng(31); return Array.from({ length: 70 }, () => [r() * W, r() * 2200, 70 + r() * 90, r() * 6.28, 0.6 + r() * 0.8, r() < 0.5 ? 0 : 1]); })();
function petals(c, t, amount = 1) {
  const n = Math.round(PET.length * amount);
  for (let i = 0; i < n; i++) { const [x0, off, sp, ph, sz, kind] = PET[i]; const y = ((t * sp + off) % (H + 220)) - 110, x = x0 + Math.sin(t * 0.9 + ph) * 46;
    c.save(); c.translate(x, y); c.rotate(t * 1.3 * sz + ph); c.scale(1, 0.45 + 0.45 * Math.abs(Math.sin(t * 2 + ph)));
    c.fillStyle = kind ? '#ffb300' : '#ff6a00'; c.globalAlpha = 0.9; c.beginPath(); c.ellipse(0, 0, 15 * sz, 9 * sz, 0, 0, 7); c.fill(); c.restore(); }
}
const EMB = (() => { const r = rng(21); return Array.from({ length: 90 }, () => [r() * W, r() * 2000, 35 + r() * 90, 3 + r() * 9, r() * 6.28]); })();
function embers(c, t, a = 1) { c.save(); c.globalCompositeOperation = 'lighter'; EMB.forEach(([x0, off, sp, s, ph]) => { const y = H + 60 - ((t * sp + off) % (H + 160)); const x = x0 + Math.sin(t * 0.7 + ph) * 30; c.globalAlpha = a * (0.35 + 0.35 * Math.sin(t * 5 + ph)); c.drawImage(G_EMBER, x - s, y - s, s * 2, s * 2); }); c.restore(); }
function sparkles(c, x, y, t, n = 30, spread = 200, spr = G_EMBER, a = 1) {
  const r = rng(Math.floor(x + y)); c.save(); c.globalCompositeOperation = 'lighter';
  for (let i = 0; i < n; i++) { const ph = r() * 6.28, sp = 0.3 + r() * 0.7, p = (t * sp + r()) % 1; const ang = r() * 6.28, d = spread * (0.2 + p * r());
    c.globalAlpha = a * Math.sin(p * Math.PI); const s = 10 + r() * 16; c.drawImage(spr, x + Math.cos(ang) * d - s / 2, y + Math.sin(ang) * d - p * 120 - s / 2, s, s); }
  c.restore();
}
function windStreaks(c, t, a = 1, y0 = 200, y1 = 1100) {
  c.save(); c.globalCompositeOperation = 'lighter';
  for (let i = 0; i < 18; i++) { const y = y0 + (y1 - y0) * ((i * 0.618) % 1), p = (t * (0.6 + (i % 4) * 0.25) + i * 0.37) % 1;
    const g = c.createLinearGradient(0, 0, 300, 0); g.addColorStop(0, 'rgba(255,245,220,0)'); g.addColorStop(1, `rgba(255,245,220,${0.25 * a * Math.sin(p * Math.PI)})`);
    c.save(); c.translate(lerp(-400, W + 100, p), y + Math.sin(t + i) * 20); c.fillStyle = g; c.fillRect(0, 0, 300, 3); c.restore(); }
  c.restore();
}
function shockwave(c, x, y, p, col = '255,220,140') { if (p <= 0 || p >= 1) return; c.save(); c.strokeStyle = `rgba(${col},${0.7 * (1 - p)})`; c.lineWidth = 14 * (1 - p) + 2; c.beginPath(); c.ellipse(x, y, 60 + p * 700, (60 + p * 700) * 0.55, 0, 0, 7); c.stroke(); c.restore(); }
function lightning(c, t, seed, x0, y0, x1, y1, a = 1) {
  const r = rng(seed); c.save(); c.globalCompositeOperation = 'lighter';
  c.beginPath(); c.moveTo(x0, y0); const n = 10; for (let i = 1; i <= n; i++) { const u = i / n; c.lineTo(lerp(x0, x1, u) + (i < n ? (r() - 0.5) * 80 : 0), lerp(y0, y1, u)); }
  c.strokeStyle = `rgba(220,235,255,${a})`; c.lineWidth = 5; c.stroke(); c.strokeStyle = `rgba(120,160,255,${0.35 * a})`; c.lineWidth = 20; c.stroke(); c.restore();
}
function orbs(c, x, y, n, t, R, cols, a = 1) { for (let i = 0; i < n; i++) { const an = t * 0.8 + i / n * Math.PI * 2; const px = x + Math.cos(an) * R, py = y + Math.sin(an) * R * 0.45; glow(c, G_GOLD, px, py, 46, a * 0.8); c.save(); c.globalAlpha = a; c.fillStyle = cols[i % cols.length]; c.beginPath(); c.arc(px, py, 13, 0, 7); c.fill(); c.restore(); } }
function wisps(c, t, x, y, n, flee = 0) {
  const r = rng(9); c.save();
  for (let i = 0; i < n; i++) { const ang = r() * 6.28, d = 260 + r() * 200 + flee * 700, ph = r() * 6.28;
    const px = x + Math.cos(ang + t * 0.3) * d, py = y + Math.sin(ang + t * 0.3) * d * 0.5 - 100;
    c.globalAlpha = (1 - flee) * 0.8; c.drawImage(G_DARK, px - 70, py - 90 + Math.sin(t * 3 + ph) * 12, 140, 180);
    c.fillStyle = `rgba(160,255,200,${(1 - flee) * 0.8})`; c.beginPath(); c.arc(px - 14, py - 70 + Math.sin(t * 3 + ph) * 12, 5, 0, 7); c.arc(px + 14, py - 70 + Math.sin(t * 3 + ph) * 12, 5, 0, 7); c.fill(); }
  c.restore();
}
function vignette(c, a = 0.55) { const g = c.createRadialGradient(W / 2, H * 0.4, H * 0.25, W / 2, H * 0.45, H * 0.8); g.addColorStop(0, 'rgba(0,0,0,0)'); g.addColorStop(1, `rgba(0,0,0,${a})`); c.fillStyle = g; c.fillRect(0, 0, W, H); }
function stage(c) { // puppet-theatre touch: soft screen texture + warm lamp at top
  glow(c, G_GOLD, W / 2, -200, 900, 0.15);
}
