// "Insults create leaders" cinematic Short: photoreal scenes with depth parallax + kinetic typography.
// frame(t) is a pure function of time.
const W = 1080, H = 1920;
const cv = document.getElementById('c'), c = cv.getContext('2d');
const GOLD = '#ffc94d', WHITE = '#f6f3ee';
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const eOut = k => 1 - Math.pow(1 - clamp(k), 3), eIO = k => { k = clamp(k); return k < .5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2; };
const eBack = k => { k = clamp(k); const s = 1.6; return 1 + (s + 1) * Math.pow(k - 1, 3) + s * Math.pow(k - 1, 2); };
const R = (i, k) => { const x = Math.sin(i * 127.1 + k * 311.7) * 43758.5453; return x - Math.floor(x); };
function mk(w, h) { const k = document.createElement('canvas'); k.width = w; k.height = h; return k; }

// ---------------- WebGL scene with depth parallax + cinematic grade ----------------
const glc = mk(W, H), gl = glc.getContext('webgl', { antialias: false, preserveDrawingBuffer: true });
const VS = 'attribute vec2 p;varying vec2 v;void main(){v=vec2(p.x*.5+.5,.5-p.y*.5);gl_Position=vec4(p,0.,1.);}';
const FS = `precision highp float;varying vec2 v;uniform sampler2D img,dep;uniform vec2 pan,par,px;uniform float zoom,asp,tm,temp,dim,bright;
vec3 tap(vec2 q){return texture2D(img,clamp(q,.002,.998)).rgb;}
void main(){vec2 uv=(v-.5)/zoom+.5+pan;uv.x=(uv.x-.5)*asp+.5;
float d=texture2D(dep,uv).r;vec2 o=par*(d-.5);d=texture2D(dep,uv-o).r;o=par*(d-.5);d=texture2D(dep,uv-o).r;o=par*(d-.5);
vec2 q=uv-o;vec2 ca=(v-.5)*.004;vec3 c=vec3(tap(q+ca).r,tap(q).g,tap(q-ca).b);
vec3 b=(tap(q+vec2(px.x,0.))+tap(q-vec2(px.x,0.))+tap(q+vec2(0.,px.y))+tap(q-vec2(0.,px.y)))*.25;c=clamp(c+(c-b)*.6,0.,1.);
float L=dot(c,vec3(.299,.587,.114));
vec3 cold=mix(c,vec3(L)*vec3(.75,.92,1.15),.45);vec3 warm=mix(c,c*vec3(1.18,1.0,.78),.55);
c=temp<0.?mix(c,cold,-temp):mix(c,warm,temp);
c=mix(c,c*vec3(.82,1.0,1.12),(1.-smoothstep(.03,.45,L))*.4);
c=(c-.5)*1.16+.5;c*=bright;
vec2 r=v-vec2(.5,.47);float vg=smoothstep(.25,.95,length(r*vec2(1.,.62)*1.55));c*=1.-.62*vg;
float n=fract(sin(dot(v*vec2(1234.5,987.6)+tm,vec2(12.9898,78.233)))*43758.5453);c+=(n-.5)*.055;c*=1.-dim;
gl_FragColor=vec4(clamp(c,0.,1.),1.);}`;
let U = {};
(function () {
  const sh = (t, s) => { const o = gl.createShader(t); gl.shaderSource(o, s); gl.compileShader(o); if (!gl.getShaderParameter(o, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(o)); return o; };
  const P = gl.createProgram(); gl.attachShader(P, sh(gl.VERTEX_SHADER, VS)); gl.attachShader(P, sh(gl.FRAGMENT_SHADER, FS)); gl.linkProgram(P); gl.useProgram(P);
  const b = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, b); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
  const l = gl.getAttribLocation(P, 'p'); gl.enableVertexAttribArray(l); gl.vertexAttribPointer(l, 2, gl.FLOAT, false, 0, 0);
  ['img', 'dep', 'pan', 'par', 'px', 'zoom', 'asp', 'tm', 'temp', 'dim', 'bright'].forEach(n => U[n] = gl.getUniformLocation(P, n));
  gl.uniform1i(U.img, 0); gl.uniform1i(U.dep, 1); gl.viewport(0, 0, W, H);
})();
function tex(src) {
  const t = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, t); gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, src);
  [gl.TEXTURE_WRAP_S, gl.TEXTURE_WRAP_T].forEach(k => gl.texParameteri(gl.TEXTURE_2D, k, gl.CLAMP_TO_EDGE));
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR); return t;
}
const img = s => new Promise(r => { const i = new Image(); i.onload = () => r(i); i.onerror = () => r(null); i.src = s; });
const SCN = {};
// per scene: camera move, colour temperature (-1 cold .. +1 golden), particles
const LOOK = {
  rain: { cam: 'push', temp: -.9, fx: 'rain' }, crowd: { cam: 'drift', temp: -.7, fx: 'dust' }, fist: { cam: 'pushFast', temp: -.3, fx: 'dust' },
  study: { cam: 'slide', temp: .15, fx: 'dust' }, stairs: { cam: 'rise', temp: .55, fx: 'dust' }, peak: { cam: 'pull', temp: .85, fx: 'embers' },
  stage: { cam: 'push', temp: .9, fx: 'confetti' }, walk: { cam: 'push', temp: .8, fx: 'embers' },
};
const CAMS = {
  push: e => ({ zoom: 1.04 + .1 * e, pan: [0, -.008 * e], par: [.012 * (2 * e - 1), -.004] }),
  pushFast: e => ({ zoom: 1.06 + .18 * e, pan: [0, 0], par: [.008 * (2 * e - 1), .004] }),
  pull: e => ({ zoom: 1.18 - .12 * e, pan: [0, .012 * (1 - e)], par: [-.014 * (2 * e - 1), .004] }),
  drift: e => ({ zoom: 1.12, pan: [.03 - .06 * e, 0], par: [.016 * (2 * e - 1), 0] }),
  slide: e => ({ zoom: 1.1, pan: [-.025 + .05 * e, -.004], par: [-.012 * (2 * e - 1), 0] }),
  rise: e => ({ zoom: 1.1, pan: [0, .03 - .05 * e], par: [0, -.012 * (2 * e - 1)] }),
};
async function loadScenes(ids) {
  await Promise.all(ids.map(async id => {
    const [im, dp] = await Promise.all([img(`scn/img/${id}.jpg`), img(`scn/depth/${id}.png`)]);
    if (!im) return; let d = dp; if (!d) { d = mk(4, 4); const x = d.getContext('2d'); x.fillStyle = '#808080'; x.fillRect(0, 0, 4, 4); }
    SCN[id] = { t: tex(im), d: tex(d), asp: (W / H) / (im.width / im.height), w: im.width, h: im.height };
  }));
}
function drawScene(id, p, t, o = {}) {
  const s = SCN[id]; if (!s) return;
  const L = LOOK[id] || { cam: 'push', temp: 0 }; const cam = CAMS[L.cam](eIO(p));
  const shake = o.shake || 0;
  gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, s.t); gl.activeTexture(gl.TEXTURE1); gl.bindTexture(gl.TEXTURE_2D, s.d);
  gl.uniform2f(U.pan, cam.pan[0] + shake * (R(t * 60 | 0, 1) - .5) * .012, cam.pan[1] + shake * (R(t * 60 | 0, 2) - .5) * .012);
  gl.uniform2f(U.par, cam.par[0], cam.par[1]); gl.uniform2f(U.px, 1 / s.w, 1 / s.h);
  gl.uniform1f(U.zoom, cam.zoom * (1 + shake * .02)); gl.uniform1f(U.asp, Math.min(1, s.asp)); gl.uniform1f(U.tm, Math.floor(t * 24) * .37 % 97);
  gl.uniform1f(U.temp, L.temp); gl.uniform1f(U.dim, o.dim || 0); gl.uniform1f(U.bright, o.bright || 1);
  gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
  c.save(); c.globalAlpha = o.alpha ?? 1; c.drawImage(glc, 0, 0, W, H); c.restore();
}

// ---------------- sprites ----------------
function glow(col) { const k = mk(128, 128), x = k.getContext('2d'), g = x.createRadialGradient(64, 64, 0, 64, 64, 64); g.addColorStop(0, `rgba(${col},1)`); g.addColorStop(.35, `rgba(${col},.35)`); g.addColorStop(1, `rgba(${col},0)`); x.fillStyle = g; x.fillRect(0, 0, 128, 128); return k; }
const G_W = glow('255,255,255'), G_G = glow('255,190,90'), G_B = glow('140,190,255');

// ---------------- timeline ----------------
let TL = null, PAGES = [];
const KEY = /^(insult|insults|gift|precious|fuel|leaders|leader|watch|me|thank|you\.?)$/i;
const norm = s => s.toLowerCase().replace(/[^a-z']/g, '');
function buildPages() {
  PAGES = [];
  for (const s of TL.segs) {
    if (s.id === 'q6') continue;           // shown as the big title instead
    let cur = []; const flush = () => { if (cur.length) PAGES.push({ seg: s.id, words: cur }); cur = []; };
    s.words.forEach((w, i) => {
      const prev = s.words[i - 1], gap = prev ? w[1] - prev[2] : 0, chars = cur.reduce((a, x) => a + x[0].length + 1, 0) + w[0].length;
      if (cur.length && (cur.length >= 3 || chars > 14 || gap > .22)) flush();
      cur.push(w);
    });
    flush();
  }
  PAGES.forEach(p => p.t0 = p.words[0][1] - .05);
  PAGES.forEach((p, i) => { const nx = PAGES[i + 1], end = p.words[p.words.length - 1][2] + .45; p.t1 = nx && nx.seg === p.seg ? Math.min(nx.t0, end + .5) : end; });
}
function init(tl) { TL = tl; buildPages(); return TL.segs.length; }
window.init = init;
window.READY = (async () => {
  for (const [n, u, w] of [['Anton', 'fonts/Anton.ttf', '400'], ['Cinzel', '../fonts/Cinzel.ttf', '400 900'], ['Inter', 'fonts/Inter.ttf', '100 900'], ['SG', 'fonts/SpaceGrotesk.ttf', '300 700']]) {
    try { const f = new FontFace(n, `url(${u})`, { weight: w }); await f.load(); document.fonts.add(f); } catch (e) { console.warn('font', n); }
  }
  await loadScenes(Object.keys(LOOK)); return Object.keys(SCN).length;
})();

// ---------------- layers ----------------
const XF = .7;
function sceneList() { const out = []; for (const s of TL.segs) for (const sc of s.scenes) out.push(sc); return out; }
function background(t) {
  const L = sceneList(); let i = L.findIndex(x => t >= x[1] && t < x[2]); if (i < 0) i = t < L[0][1] ? 0 : L.length - 1;
  const sc = L[i], p = clamp((t - sc[1]) / (sc[2] - sc[1]));
  const imp = impact(t);
  drawScene(sc[0], p, t, { shake: imp, bright: 1 + imp * .25 });
  if (i > 0 && t - sc[1] < XF) { const pr = L[i - 1]; drawScene(pr[0], 1, t, { alpha: 1 - eIO((t - sc[1]) / XF) }); }
  return sc[0];
}
function impact(t) {   // short punch at the big moments
  let v = 0;
  for (const id of ['q3', 'q6']) { const s = TL.segs.find(x => x.id === id); if (!s) continue; const d = t - s.vo0 + .08; if (d > 0 && d < .6) v = Math.max(v, Math.exp(-d * 7)); }
  return v;
}
function particles(t, kind) {
  c.save(); c.globalCompositeOperation = 'lighter';
  if (kind === 'rain') {
    c.strokeStyle = 'rgba(200,220,255,.22)'; c.lineWidth = 2;
    for (let i = 0; i < 160; i++) { const sp = 1600 + R(i, 1) * 900, x = R(i, 2) * W - 80, y = ((R(i, 3) * H * 1.2 + t * sp) % (H * 1.2)) - 100, l = 40 + R(i, 4) * 60; c.globalAlpha = .4 + R(i, 5) * .5; c.beginPath(); c.moveTo(x, y); c.lineTo(x + l * .12, y + l); c.stroke(); }
  } else {
    const n = kind === 'confetti' ? 70 : 50, spr = kind === 'dust' ? G_W : G_G;
    for (let i = 0; i < n; i++) {
      const up = kind === 'embers' ? -1 : kind === 'confetti' ? 1 : -.3, sp = 20 + R(i, 1) * 50;
      const y = ((R(i, 2) * H + up * t * sp) % H + H) % H, x = R(i, 3) * W + Math.sin(t * .6 + i) * 40, r = (kind === 'dust' ? 2 : 3) + R(i, 4) * 6;
      c.globalAlpha = (kind === 'dust' ? .25 : .55) * (.5 + .5 * Math.sin(t * 2 + i));
      if (kind === 'confetti') { c.save(); c.translate(x, y); c.rotate(t * 3 + i); c.fillStyle = i % 2 ? '#ffd27a' : '#fff1c9'; c.fillRect(-6, -3, 12, 6); c.restore(); }
      else c.drawImage(spr, x - r * 3, y - r * 3, r * 6, r * 6);
    }
  }
  c.restore();
}
function grade(t, scene) {
  let g = c.createLinearGradient(0, 0, 0, 420); g.addColorStop(0, 'rgba(0,0,0,.55)'); g.addColorStop(1, 'rgba(0,0,0,0)'); c.fillStyle = g; c.fillRect(0, 0, W, 420);
  g = c.createLinearGradient(0, 950, 0, H); g.addColorStop(0, 'rgba(0,0,0,0)'); g.addColorStop(.5, 'rgba(0,0,0,.45)'); g.addColorStop(1, 'rgba(0,0,0,.75)'); c.fillStyle = g; c.fillRect(0, 950, W, H - 950);
  const warm = (LOOK[scene] || {}).temp > 0;
  c.save(); c.globalCompositeOperation = 'screen'; c.globalAlpha = warm ? .22 : .1;
  const lx = W * (.3 + .5 * Math.sin(t * .17)), ly = 260 + 120 * Math.sin(t * .23); c.drawImage(warm ? G_G : G_B, lx - 700, ly - 700, 1400, 1400); c.restore();
}
function txt(s, x, y, font, col, o = {}) {
  c.save(); c.font = font; c.fillStyle = col; c.textAlign = o.align || 'center'; c.textBaseline = o.base || 'middle'; c.letterSpacing = o.ls || '0px';
  if (o.glow) { c.shadowColor = o.glow; c.shadowBlur = o.blur || 30; }
  if (o.stroke) { c.lineJoin = 'round'; c.strokeStyle = o.stroke; c.lineWidth = o.sw || 10; c.strokeText(s, x, y); }
  c.fillText(s, x, y); c.restore();
}
function tw(s, font, ls = '0px') { c.save(); c.font = font; c.letterSpacing = ls; const w = c.measureText(s).width; c.restore(); return w; }
function captions(t) {
  const p = PAGES.find(q => t >= q.t0 && t < q.t1); if (!p) return;
  const words = p.words.map(w => w[0].toUpperCase().replace(/[.,]+$/, ''));
  let size = 132; const font = n => `400 ${n}px Anton`, ls = '2px', gap = 30;
  let ws = words.map(w => tw(w, font(size), ls)), total = ws.reduce((a, b) => a + b, 0) + gap * (ws.length - 1);
  while (total > 920 && size > 80) { size -= 6; ws = words.map(w => tw(w, font(size), ls)); total = ws.reduce((a, b) => a + b, 0) + gap * (ws.length - 1); }
  const a = clamp((p.t1 - t) / .15); let x = W / 2 - total / 2; const cy = 1240;
  words.forEach((w, i) => {
    const w0 = p.words[i][1]; if (t < w0 - .04) { x += ws[i] + gap; return; }
    const k = clamp((t - w0 + .04) / .22), key = KEY.test(norm(p.words[i][0]));
    c.save(); c.globalAlpha = a * clamp(k * 2.5);
    c.translate(x + ws[i] / 2, cy + (1 - eOut(k)) * 26); const sc = 1 + (1 - eBack(k)) * .25; c.scale(sc, sc);
    c.filter = k < .6 ? `blur(${(1 - k / .6) * 8}px)` : 'none';
    txt(w, 0, 0, font(size), key ? GOLD : WHITE, { glow: key ? 'rgba(255,170,40,.75)' : 'rgba(0,0,0,.85)', blur: key ? 40 : 24, ls });
    c.restore(); x += ws[i] + gap;
  });
}
function bigTitle(t) {   // "INSULTS / CREATE / LEADERS"
  const s = TL.segs.find(x => x.id === 'q6'); if (!s) return;
  const t0 = s.vo0 - .1, t1 = s.t1; if (t < t0 || t > t1) return;
  const out = clamp((t1 - t) / .4);
  const lines = [['INSULTS', 0], ['CREATE', 1], ['LEADERS', 2]];
  lines.forEach(([w, k]) => {
    const wt = s.words[k] ? s.words[k][1] - .06 : t0 + k * .3; if (t < wt) return;
    const e = clamp((t - wt) / .3);
    c.save(); c.globalAlpha = out * clamp(e * 3); const y = 760 + k * 240; c.translate(W / 2, y); const sc = 1.35 - .35 * eOut(e); c.scale(sc, sc);
    txt(w, 0, 0, `400 ${k === 2 ? 250 : 200}px Anton`, k === 2 ? GOLD : WHITE, { glow: k === 2 ? 'rgba(255,170,40,.9)' : 'rgba(0,0,0,.8)', blur: k === 2 ? 60 : 30, ls: '6px' });
    c.restore();
  });
}
function quoteCard(t) {
  const T = TL.T, t0 = TL.card0; if (t < t0) return;
  const k = eIO((t - t0) / .9);
  c.save(); c.fillStyle = `rgba(4,3,2,${.72 * k})`; c.fillRect(0, 0, W, H); c.restore();
  const l = ['THE MOST PRECIOUS', 'GIFT IS INSULTS.'], l2 = ['INSULTS', 'CREATE LEADERS.'];
  const a1 = eOut((t - t0 - .2) / .8), a2 = eOut((t - t0 - .9) / .8), a3 = eOut((t - t0 - 1.6) / .6);
  c.save(); c.globalAlpha = a1; txt(l[0], W / 2, 700 - 20 * (1 - a1), '700 64px Cinzel', WHITE, { glow: 'rgba(0,0,0,.9)', blur: 20, ls: '3px' }); txt(l[1], W / 2, 790 - 20 * (1 - a1), '700 64px Cinzel', WHITE, { glow: 'rgba(0,0,0,.9)', blur: 20, ls: '3px' }); c.restore();
  c.save(); c.globalAlpha = a2; txt(l2[0], W / 2, 930 - 20 * (1 - a2), '900 92px Cinzel', GOLD, { glow: 'rgba(255,170,40,.8)', blur: 40, ls: '4px' }); txt(l2[1], W / 2, 1040 - 20 * (1 - a2), '900 92px Cinzel', GOLD, { glow: 'rgba(255,170,40,.8)', blur: 40, ls: '4px' }); c.restore();
  c.save(); c.globalAlpha = a3; c.fillStyle = GOLD; c.fillRect(W / 2 - 120 * a3, 1130, 240 * a3, 3);
  txt('— @TECHVIBE24', W / 2, 1200, '600 40px SG', WHITE, { ls: '4px' }); c.restore();
  const e = T - t; if (e < .6) { c.save(); c.globalAlpha = 1 - e / .6; c.fillStyle = '#000'; c.fillRect(0, 0, W, H); c.restore(); }
}
function watermark(t) {
  c.save(); c.globalAlpha = .7 * clamp(t / .8) * (t > TL.card0 ? clamp(1 - (t - TL.card0) / .5) : 1);
  txt('@TECHVIBE24', W / 2, 150, '700 34px SG', WHITE, { glow: 'rgba(0,0,0,.8)', blur: 14, ls: '5px' }); c.restore();
}
const GRAIN = [0, 1, 2].map(k => { const g = mk(270, 480), x = g.getContext('2d'), d = x.createImageData(270, 480); for (let i = 0; i < d.data.length; i += 4) { const v = 128 + (R(i + k * 7, 3) - .5) * 160; d.data[i] = d.data[i + 1] = d.data[i + 2] = v; d.data[i + 3] = 255; } x.putImageData(d, 0, 0); return g; });
function finish(t) {
  c.save(); c.globalCompositeOperation = 'overlay'; c.globalAlpha = .07; c.drawImage(GRAIN[Math.floor(t * 24) % 3], 0, 0, W, H); c.restore();
  const imp = impact(t); if (imp > 0) { c.save(); c.globalCompositeOperation = 'screen'; c.globalAlpha = imp * .55; c.fillStyle = '#fff4e0'; c.fillRect(0, 0, W, H); c.restore(); }
  if (t < .6) { c.save(); c.globalAlpha = 1 - t / .6; c.fillStyle = '#000'; c.fillRect(0, 0, W, H); c.restore(); }
}
function frame(t) {
  c.setTransform(1, 0, 0, 1, 0, 0); c.globalAlpha = 1; c.globalCompositeOperation = 'source-over'; c.fillStyle = '#000'; c.fillRect(0, 0, W, H);
  const scene = background(t); particles(t, (LOOK[scene] || {}).fx || 'dust'); grade(t, scene);
  bigTitle(t); captions(t); watermark(t); quoteCard(t); finish(t);
}
window.frame = frame;
