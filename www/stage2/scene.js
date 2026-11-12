// Painted scenes brought to life: depth-based 2.5D camera moves (WebGL) + light/particle effects + film grade.
// Every frame is a pure function of t, so parallel renders stay seamless.
const GLW = window.GLW || 864, GLH = window.GLH || 1536;
const SCN = {};           // id -> {img, dep, tex, dtex, aspFix}
const glc = mkCanvas(GLW, GLH);
const gl = glc.getContext('webgl', { preserveDrawingBuffer: !!window.GLPRESERVE, antialias: false, premultipliedAlpha: false });
const VS = 'attribute vec2 p;varying vec2 v;void main(){v=vec2(p.x*.5+.5,.5-p.y*.5);gl_Position=vec4(p,0.,1.);}';
const FS = `precision highp float;varying vec2 v;uniform sampler2D img,dep;uniform vec2 pan,par,px;uniform float zoom,focus,asp,sharp,tm,warm;
void main(){vec2 uv=(v-.5)/zoom+.5+pan;uv.x=(uv.x-.5)*asp+.5;
float d=texture2D(dep,uv).r;vec2 o=par*(d-focus);d=texture2D(dep,uv-o).r;o=par*(d-focus);d=texture2D(dep,uv-o).r;o=par*(d-focus);
vec2 q=clamp(uv-o,.002,.998);vec2 ca=(v-.5)*.0035;vec3 c=vec3(texture2D(img,clamp(q+ca,.002,.998)).r,texture2D(img,q).g,texture2D(img,clamp(q-ca,.002,.998)).b);
vec3 b=(texture2D(img,q+vec2(px.x,0.)).rgb+texture2D(img,q-vec2(px.x,0.)).rgb+texture2D(img,q+vec2(0.,px.y)).rgb+texture2D(img,q-vec2(0.,px.y)).rgb)*.25;
c=clamp(c+(c-b)*sharp,0.,1.);vec3 sl=mix(2.*c*vec3(1.,.604,.235)+c*c*(1.-2.*vec3(1.,.604,.235)),c,1.-warm);c=sl;float L=dot(c,vec3(.299,.587,.114));c=mix(c,c*vec3(.86,1.,1.1),(1.-smoothstep(.05,.5,L))*.35);c=mix(c,c*vec3(1.08,1.,.88),smoothstep(.45,.95,L)*.3);c=(c-.5)*1.07+.5;vec2 r=v-vec2(.5,.4);float vg=smoothstep(.28,.85,length(r*vec2(1.05,.62)*1.55));c*=1.-.62*vg;float n=fract(sin(dot(v*vec2(1234.5,987.6)+tm,vec2(12.9898,78.233)))*43758.5453);c+=(n-.5)*.045;gl_FragColor=vec4(c,1.);}`;
let PRG = null, U = {};
function glInit() {
  const sh = (type, src) => { const s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s); if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s)); return s; };
  PRG = gl.createProgram(); gl.attachShader(PRG, sh(gl.VERTEX_SHADER, VS)); gl.attachShader(PRG, sh(gl.FRAGMENT_SHADER, FS)); gl.linkProgram(PRG); gl.useProgram(PRG);
  const b = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, b); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
  const loc = gl.getAttribLocation(PRG, 'p'); gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
  ['img', 'dep', 'pan', 'par', 'px', 'zoom', 'focus', 'asp', 'sharp', 'tm', 'warm'].forEach(n => U[n] = gl.getUniformLocation(PRG, n));
  gl.uniform1i(U.img, 0); gl.uniform1i(U.dep, 1); gl.viewport(0, 0, GLW, GLH);
}
function mkTex(src) {
  const t = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, t);
  gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, src);
  [gl.TEXTURE_WRAP_S, gl.TEXTURE_WRAP_T].forEach(k => gl.texParameteri(gl.TEXTURE_2D, k, gl.CLAMP_TO_EDGE));
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
  return t;
}
const loadImg = src => new Promise(r => { const i = new Image(); i.onload = () => r(i); i.onerror = () => r(null); i.src = src; });
async function loadScenes(ids) {
  glInit();
  await Promise.all(ids.map(async id => {
    const [im, dp] = await Promise.all([loadImg(`../scn/img/${id}.jpg`), loadImg(`../scn/depth/${id}.png`)]);
    if (!im) return;
    let dsrc = dp;
    if (!dp) { dsrc = mkCanvas(4, 4); const x = dsrc.getContext('2d'); x.fillStyle = '#808080'; x.fillRect(0, 0, 4, 4); }
    SCN[id] = { tex: mkTex(im), dtex: mkTex(dsrc), asp: (GLW / GLH) / (im.width / im.height), w: im.width, h: im.height };
  }));
  return Object.keys(SCN).length;
}
function glDraw(id, cam) {
  const s = SCN[id] || SCN.c1 || SCN[Object.keys(SCN)[0]];
  gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, s.tex);
  gl.activeTexture(gl.TEXTURE1); gl.bindTexture(gl.TEXTURE_2D, s.dtex);
  gl.uniform2f(U.pan, cam.pan[0], cam.pan[1]); gl.uniform2f(U.par, cam.par[0], cam.par[1]);
  gl.uniform2f(U.px, 1 / s.w, 1 / s.h); gl.uniform1f(U.zoom, cam.zoom); gl.uniform1f(U.focus, cam.focus ?? 0.45);
  gl.uniform1f(U.asp, Math.min(1, s.asp)); gl.uniform1f(U.sharp, 0.55); gl.uniform1f(U.tm, (cam.t || 0) % 97); gl.uniform1f(U.warm, 0.14);
  gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
}
// ---------- camera moves (e = eased progress 0..1) ----------
const CAMS = {
  push: e => ({ zoom: 1.07 + 0.14 * e, pan: [0, -0.018 * e], par: [0.018 * (2 * e - 1), -0.006] }),
  pull: e => ({ zoom: 1.24 - 0.15 * e, pan: [0, 0.016 * (1 - e)], par: [-0.016 * (2 * e - 1), 0.005] }),
  rise: e => ({ zoom: 1.13, pan: [0, 0.042 - 0.075 * e], par: [0.008 * Math.sin(e * 3), -0.014 * (2 * e - 1)] }),
  sink: e => ({ zoom: 1.13, pan: [0, -0.035 + 0.065 * e], par: [-0.008 * Math.sin(e * 3), 0.012 * (2 * e - 1)] }),
  slideL: e => ({ zoom: 1.14, pan: [0.04 - 0.08 * e, -0.008], par: [0.02 * (2 * e - 1), 0] }),
  slideR: e => ({ zoom: 1.14, pan: [-0.04 + 0.08 * e, -0.008], par: [-0.02 * (2 * e - 1), 0] }),
  orbit: e => ({ zoom: 1.1 + 0.05 * Math.sin(e * Math.PI), pan: [0, -0.01], par: [0.024 * Math.sin((e - 0.5) * Math.PI), 0.008 * Math.cos(e * Math.PI)] }),
  drift: e => ({ zoom: 1.08 + 0.07 * e, pan: [0.012 * (1 - 2 * e), -0.01 * e], par: [0.013 * (2 * e - 1), -0.004] }),
};
// ---------- effects ----------
const R = (i, k) => { const x = Math.sin(i * 127.1 + k * 311.7) * 43758.5453; return x - Math.floor(x); };
function fxDust(c, t, n = 48, col = [255, 214, 140]) {
  c.save(); c.globalCompositeOperation = 'lighter';
  for (let i = 0; i < n; i++) {
    const sp = 6 + R(i, 1) * 18, x = (R(i, 2) * W + Math.sin(t * 0.3 + i) * 40 + t * (R(i, 3) - 0.5) * 20) % W, y = ((R(i, 4) * H * 1.1 - t * sp) % (H * 1.1) + H * 1.1) % (H * 1.1) - 40;
    const a = 0.25 + 0.55 * (0.5 + 0.5 * Math.sin(t * (1 + R(i, 5) * 2) + i * 3)), r = 1.2 + R(i, 6) * 3.2;
    c.globalAlpha = a * (y < 1150 ? 1 : 0.5);
    c.drawImage(G_WHITE, (x + W) % W - r * 3, y - r * 3, r * 6, r * 6);
  }
  c.restore();
}
function fxEmbers(c, t, n = 80) {
  c.save(); c.globalCompositeOperation = 'lighter';
  for (let i = 0; i < n; i++) {
    const sp = 60 + R(i, 1) * 160, life = (H + 300) / sp, ph = ((t + R(i, 2) * life) % life) / life;
    const y = H + 100 - ph * (H + 300), x = R(i, 3) * W + Math.sin(t * 1.3 + i) * 30 + ph * (R(i, 4) - 0.5) * 220;
    const r = 3 + R(i, 5) * 7, a = Math.sin(ph * Math.PI) * (0.55 + 0.45 * Math.sin(t * 9 + i * 5));
    c.globalAlpha = Math.max(0, a); c.drawImage(G_EMBER, x - r * 2, y - r * 2, r * 4, r * 4);
  }
  c.restore();
}
function fxPetals(c, t, n = 26) {
  const cols = ['#ff8f1f', '#ffb52e', '#e8402a', '#ffd34d'];
  c.save();
  for (let i = 0; i < n; i++) {
    const sp = 55 + R(i, 1) * 60, life = (H + 200) / sp, ph = ((t + R(i, 2) * life) % life) / life;
    const y = -100 + ph * (H + 200), x = R(i, 3) * W + Math.sin(t * 0.9 + i * 2) * 70;
    c.setTransform(1, 0, 0, 1, x, y); c.rotate(t * (0.8 + R(i, 4)) + i); c.scale(1, 0.45 + 0.35 * Math.sin(t * 2 + i));
    c.globalAlpha = 0.85 * Math.min(1, Math.sin(ph * Math.PI) * 3); c.fillStyle = cols[i % 4];
    c.beginPath(); c.ellipse(0, 0, 13 + R(i, 5) * 8, 7, 0, 0, Math.PI * 2); c.fill();
  }
  c.setTransform(1, 0, 0, 1, 0, 0); c.restore();
}
function fxRays(c, t, x = W / 2, y = 120, a = 0.22, col = '255,214,140') {
  c.save(); c.globalCompositeOperation = 'lighter'; c.translate(x, y);
  for (let i = 0; i < 16; i++) {
    const ang = Math.PI / 2 + (i - 7.5) * 0.11 + Math.sin(t * 0.15 + i) * 0.03, len = 2300, wdt = 0.025 + R(i, 1) * 0.04;
    const g = c.createLinearGradient(0, 0, Math.cos(ang) * len, Math.sin(ang) * len);
    const k = a * (0.4 + 0.6 * (0.5 + 0.5 * Math.sin(t * 0.6 + i * 1.7)));
    g.addColorStop(0, `rgba(${col},${k})`); g.addColorStop(1, `rgba(${col},0)`);
    c.fillStyle = g; c.beginPath(); c.moveTo(0, 0); c.lineTo(Math.cos(ang - wdt) * len, Math.sin(ang - wdt) * len); c.lineTo(Math.cos(ang + wdt) * len, Math.sin(ang + wdt) * len); c.fill();
  }
  c.restore();
}
function fxGlow(c, t, x, y, r = 520, a = 0.35, spr = G_GOLD) { glow(c, spr, x, y, r * (1 + 0.05 * Math.sin(t * 1.6)), a * (0.8 + 0.2 * Math.sin(t * 1.1))); }
const MIST = cached('mist', W * 2, 360, x => { for (let i = 0; i < 16; i++) { const r = 150 + R(i, 1) * 140, cx = R(i, 2) * W * 2, cy = 180 + (R(i, 4) - 0.5) * 200; x.globalAlpha = 0.5 + 0.5 * R(i, 5); x.drawImage(G_CLOUD, cx - r * 1.6, cy - r * 0.5, r * 3.2, r); x.drawImage(G_CLOUD, cx - r * 1.6 - W * 2, cy - r * 0.5, r * 3.2, r); x.drawImage(G_CLOUD, cx - r * 1.6 + W * 2, cy - r * 0.5, r * 3.2, r); } });
function fxMist(c, t, a = 0.18, y0 = 1000, speed = 18) {
  c.save();
  for (let j = 0; j < 2; j++) { const off = ((t * speed * (j ? 0.6 : 1) + j * 700) % (W * 2)); c.globalAlpha = a * (j ? 0.8 : 1); const yy = y0 + j * 330; c.drawImage(MIST, -off, yy, W * 2, 360 * 1.5); c.drawImage(MIST, W * 2 - off, yy, W * 2, 360 * 1.5); }
  c.restore();
}
function fxWind(c, t, n = 34, dx = -1, dy = 0.35) {
  c.save(); c.globalCompositeOperation = 'lighter'; c.lineCap = 'round';
  for (let i = 0; i < n; i++) {
    const sp = 900 + R(i, 1) * 900, L = 120 + R(i, 2) * 260, per = (W + 800) / sp, ph = ((t + R(i, 3) * per) % per) / per;
    const x = dx < 0 ? W + 400 - ph * (W + 800) : -400 + ph * (W + 800), y = R(i, 4) * 1300 + (x - W / 2) * dy * -dx;
    c.strokeStyle = `rgba(255,240,220,${0.10 + 0.16 * R(i, 5)})`; c.lineWidth = 1.5 + R(i, 6) * 2.5;
    c.beginPath(); c.moveTo(x, y); c.lineTo(x - dx * L, y - dy * L * -dx); c.stroke();
  }
  c.restore();
}
function fxStars(c, t, n = 90) {
  c.save(); c.globalCompositeOperation = 'lighter';
  for (let i = 0; i < n; i++) { const x = R(i, 1) * W, y = R(i, 2) * 820, r = 0.8 + R(i, 3) * 2.2; c.globalAlpha = 0.3 + 0.6 * (0.5 + 0.5 * Math.sin(t * (1.5 + R(i, 4) * 3) + i)); c.drawImage(G_WHITE, x - r * 3, y - r * 3, r * 6, r * 6); }
  c.restore();
}
function boltPath(c, x0, y0, x1, y1, seed, w) {
  let x = x0, y = y0; const n = 14; c.beginPath(); c.moveTo(x, y);
  for (let k = 1; k <= n; k++) { const f = k / n; x = lerp(x0, x1, f) + (R(seed, k) - 0.5) * 120 * (1 - f * 0.4); y = lerp(y0, y1, f); c.lineTo(x, y); }
  c.lineWidth = w; c.stroke();
}
function fxLightning(c, t, period = 3.1) {
  const k = Math.floor(t / period), ph = t - k * period;
  if (ph > 0.42) return 0;
  const fl = ph < 0.08 ? 1 : ph < 0.16 ? 0.35 : ph < 0.24 ? 0.85 : Math.max(0, 1 - (ph - 0.24) / 0.18) * 0.5;
  c.save(); c.globalCompositeOperation = 'lighter';
  const x0 = 150 + R(k, 7) * 780; c.strokeStyle = `rgba(210,225,255,${fl})`; c.shadowColor = 'rgba(160,190,255,1)'; c.shadowBlur = 30;
  boltPath(c, x0, -20, x0 + (R(k, 8) - 0.5) * 300, 500 + R(k, 9) * 400, k, 5);
  c.shadowBlur = 0; c.globalAlpha = fl * 0.28; c.fillStyle = '#cfdcff'; c.fillRect(0, 0, W, H);
  c.restore(); return fl;
}
function fxShock(c, t, x, y, period = 2.6) {
  c.save(); c.globalCompositeOperation = 'lighter';
  for (let j = 0; j < 2; j++) { const ph = ((t + j * period / 2) % period) / period, r = 60 + ph * 900; c.strokeStyle = `rgba(255,210,120,${0.5 * (1 - ph)})`; c.lineWidth = 14 * (1 - ph) + 2; c.beginPath(); c.ellipse(x, y, r, r * 0.55, 0, 0, Math.PI * 2); c.stroke(); }
  c.restore();
}
function fxFire(c, t, a = 0.22) {
  const f = 0.75 + 0.25 * Math.sin(t * 7.3) * Math.sin(t * 3.1 + 1);
  c.save(); c.globalCompositeOperation = 'lighter'; const g = c.createLinearGradient(0, H, 0, 500);
  g.addColorStop(0, `rgba(255,110,20,${a * f})`); g.addColorStop(1, 'rgba(255,60,0,0)'); c.fillStyle = g; c.fillRect(0, 500, W, H - 500); c.restore();
}
function fxRain(c, t, n = 160) {
  c.save(); c.strokeStyle = 'rgba(200,215,235,.28)'; c.lineWidth = 2;
  c.beginPath();
  for (let i = 0; i < n; i++) { const sp = 1800 + R(i, 1) * 700, per = (H + 200) / sp, ph = ((t + R(i, 2) * per) % per) / per, x = R(i, 3) * (W + 300) - ph * 260, y = -100 + ph * (H + 200); c.moveTo(x, y); c.lineTo(x - 18, y + 60); }
  c.stroke(); c.restore();
}
function fxLamps(c, t, pts) { pts.forEach(([x, y, r], i) => glow(c, G_GOLD, x, y, r * (1 + 0.08 * Math.sin(t * 9 + i * 2) * Math.sin(t * 4.3 + i)), 0.55)); }
// grain + vignette + warm grade
const GRAIN = [0, 1, 2].map(k => { const cv = mkCanvas(360, 640), x = cv.getContext('2d'), d = x.createImageData(360, 640); for (let i = 0; i < d.data.length; i += 4) { const v = 128 + (R(i + k * 7, 3) - 0.5) * 160; d.data[i] = d.data[i + 1] = d.data[i + 2] = v; d.data[i + 3] = 255; } x.putImageData(d, 0, 0); return cv; });
function grade(c, t, warm = 0.12) {
  c.save();
  c.globalCompositeOperation = 'soft-light'; c.globalAlpha = warm; c.fillStyle = '#ff9a3c'; c.fillRect(0, 0, W, H);
  c.globalCompositeOperation = 'source-over'; c.globalAlpha = 1;
  const v = c.createRadialGradient(W / 2, H * 0.36, H * 0.25, W / 2, H * 0.45, H * 0.78);
  v.addColorStop(0, 'rgba(0,0,0,0)'); v.addColorStop(1, 'rgba(6,1,0,.62)'); c.fillStyle = v; c.fillRect(0, 0, W, H);
  c.globalCompositeOperation = 'overlay'; c.globalAlpha = 0.07; c.drawImage(GRAIN[Math.floor(t * 24) % 3], 0, 0, W, H);
  c.restore();
}
// ---------- scene table ----------
const CYCLE = ['push', 'orbit', 'rise', 'pull', 'slideL', 'drift', 'slideR', 'sink'];
const FXBY = {
  intro: ['rays', 'mist', 'dust'], d1: ['lamps', 'dust', 'mist'], d2: ['wind', 'mist', 'dust'], c1: ['rays', 'glow', 'dust'], c2: ['rays', 'dust', 'wind'],
  c3: ['lightning', 'dust', 'shake'], c4: ['glow', 'dust'], c5: ['rays', 'wind', 'dust'], c6: ['rays', 'petals', 'dust'], c7: ['dust', 'rays'],
  c8: ['glow', 'petals', 'dust'], c9: ['stars', 'glowSoft', 'dust'], c10: ['embers', 'fire', 'shake'], c11: ['stars', 'wind', 'mistFast', 'glowGreen'],
  c12: ['rays', 'petals', 'dust'], c13: ['rays', 'glow', 'petals'], c14: ['rays', 'stars', 'dust'], c15: ['rays', 'stars', 'dust'], c16: ['rays', 'dust'],
  c17: ['glow', 'dust', 'petals'], c18: ['raysBig', 'glowSun', 'dust'], c19: ['wind', 'mistFast', 'dust'], c20: ['rays', 'dust'], c21: ['lamps2', 'dust', 'glowSoft'],
  c22: ['rain', 'lightning', 'glow'], c23: ['shock', 'dust', 'shake', 'lightningSoft'], c24: ['mist', 'glow', 'dust'], c25: ['lamps', 'glow', 'dust'],
  c26: ['glow', 'mist', 'dust'], c27: ['rays', 'dust'], c28: ['lamps2', 'embersSoft', 'dust'], c29: ['raysBig', 'stars', 'dust'], c30: ['embers', 'glow', 'shake'],
  c31: ['glow', 'dust', 'petals'], c32: ['glow', 'dust'], c33: ['rays', 'dust', 'petals'], c34: ['raysBig', 'mist', 'dust'], c35: ['lamps', 'petals', 'dust'],
  c36: ['lightningSoft', 'embers', 'glow'], c37: ['rays', 'dust', 'petals'], c38: ['rays', 'dust'], c39: ['stars', 'glow', 'dust'], c40: ['rays', 'glow', 'petals'],
  d3: ['rays', 'glow', 'petals', 'dust'], jai1: ['rays', 'petals', 'dust'],
};
const CAMBY = { intro: 'pull', c1: 'pull', c11: 'slideL', c18: 'rise', c19: 'slideR', c23: 'push', c10: 'orbit', d3: 'pull', jai1: 'push', c4: 'push', c34: 'rise' };
function sceneFx(c, id, t, p, d) {
  const fx = FXBY[id] || ['dust'], FX0 = 420;
  for (const f of fx) {
    if (f === 'dust') fxDust(c, t);
    else if (f === 'embers') fxEmbers(c, t);
    else if (f === 'embersSoft') { c.save(); c.globalAlpha = 0.6; fxEmbers(c, t, 40); c.restore(); }
    else if (f === 'petals') fxPetals(c, t);
    else if (f === 'rays') fxRays(c, t, W / 2, 60, 0.16);
    else if (f === 'raysBig') fxRays(c, t, W / 2, 330, 0.3);
    else if (f === 'glow') fxGlow(c, t, W / 2, FX0 + 180, 560, 0.3);
    else if (f === 'glowSoft') fxGlow(c, t, W / 2, FX0 + 220, 420, 0.18);
    else if (f === 'glowSun') fxGlow(c, t, W / 2, 330, 700, 0.42);
    else if (f === 'glowGreen') fxGlow(c, t, W * 0.62, FX0, 260, 0.45, G_GREEN);
    else if (f === 'mist') fxMist(c, t);
    else if (f === 'mistFast') fxMist(c, t, 0.16, 700, 260);
    else if (f === 'wind') fxWind(c, t);
    else if (f === 'stars') fxStars(c, t);
    else if (f === 'lightning') fxLightning(c, t);
    else if (f === 'lightningSoft') { c.save(); c.globalAlpha = 0.55; fxLightning(c, t + 1.3, 4.3); c.restore(); }
    else if (f === 'shock') fxShock(c, t, W / 2, FX0 + 40);
    else if (f === 'fire') fxFire(c, t);
    else if (f === 'rain') fxRain(c, t);
    else if (f === 'lamps') fxLamps(c, t, [[230, 1020, 120], [860, 1060, 100]]);
    else if (f === 'lamps2') fxLamps(c, t, [[120, 1100, 90], [960, 1100, 90], [300, 1180, 70], [780, 1180, 70]]);
  }
}
function drawScene(c, id, idx, p, t, d, camName) {
  const fx = FXBY[id] || [], e = ease(p);
  const cam = CAMS[camName || CAMBY[id] || CYCLE[idx % CYCLE.length]](e);
  if (fx.includes('shake')) { cam.pan = [cam.pan[0] + 0.0025 * Math.sin(t * 23) * Math.sin(t * 5.1), cam.pan[1] + 0.002 * Math.sin(t * 19 + 1)]; }
  cam.pan = [cam.pan[0] + 0.0016 * Math.sin(t * 0.71) + 0.0007 * Math.sin(t * 1.9), cam.pan[1] + 0.0012 * Math.sin(t * 0.53 + 1)];
  cam.t = Math.floor(t * 24) * 0.37; glDraw(id, cam);
  c.setTransform(1, 0, 0, 1, 0, 0); c.globalAlpha = 1; c.globalCompositeOperation = 'source-over';
  c.imageSmoothingEnabled = true; c.imageSmoothingQuality = 'high';
  c.drawImage(glc, 0, 0, W, H);
  sceneFx(c, id, t, p, d);
}
// ---------- hook into the existing timeline composer ----------
const SH = {}, STORY = {};
const ORDER = ['intro', 'd1', 'd2', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10', 'c11', 'c12', 'c13', 'c14', 'c15', 'c16', 'c17', 'c18', 'c19', 'c20',
  'c21', 'c22', 'c23', 'c24', 'c25', 'c26', 'c27', 'c28', 'c29', 'c30', 'c31', 'c32', 'c33', 'c34', 'c35', 'c36', 'c37', 'c38', 'c39', 'c40', 'd3', 'jai1'];
ORDER.forEach((id, i) => { SH[id] = (c, p, t, d) => drawScene(c, SCN[id] ? id : 'c1', i, p, t, d); STORY[id] = [id]; });
STORY.jai2 = ['jai2']; SH.jai2 = (c, p, t, d) => drawScene(c, SCN.c23 ? 'c23' : 'c1', 25, p, t, d, 'push');
SH.section = (c, p, t, d) => drawScene(c, SCN.c1 ? 'c1' : 'intro', 3, p, t, d, 'drift');
SH.pavanFly = (c, p, t, d) => drawScene(c, SCN.d3 ? 'd3' : 'intro', 43, p, t, d, 'drift');
SH.outro = (c, p, t, d) => drawScene(c, SCN.d3 ? 'd3' : 'intro', 43, p, t, d, 'pull');
SH.blessBig = SH.c1;
window.SCENE_READY = loadScenes(ORDER);
