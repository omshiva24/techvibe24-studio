// TechVibe24 news Short: photoreal backdrops with depth parallax (WebGL) + broadcast-style motion graphics (2D canvas).
// frame(t) is a pure function of time, so any frame can be rendered in any order.
const W = 1080, H = 1920;
const cv = document.getElementById('c'), c = cv.getContext('2d');
const C = { bg: '#04070d', cyan: '#2ee6ff', vio: '#7b5cff', red: '#ff2e4d', yel: '#ffd60a', white: '#f4f7fb', mute: '#b9c6d6', panel: 'rgba(8,13,22,0.74)' };
const F = { big: "'Anton', 'Brico', sans-serif", ui: "'Space Grotesk', 'Brico', sans-serif", body: "'Inter', 'Brico', sans-serif", mono: "'JetBrains Mono', monospace" };
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x)), lerp = (a, b, k) => a + (b - a) * k;
const eOut = k => 1 - Math.pow(1 - clamp(k), 3), eIO = k => { k = clamp(k); return k < .5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2; };
const eBack = k => { k = clamp(k); const s = 1.7; return 1 + (s + 1) * Math.pow(k - 1, 3) + s * Math.pow(k - 1, 2); };
const R = (i, k) => { const x = Math.sin(i * 127.1 + k * 311.7) * 43758.5453; return x - Math.floor(x); };
function mk(w, h) { const k = document.createElement('canvas'); k.width = w; k.height = h; return k; }

// ---------------- WebGL backdrop ----------------
const glc = mk(W, H), gl = glc.getContext('webgl', { antialias: false, premultipliedAlpha: false, preserveDrawingBuffer: true });
const VS = 'attribute vec2 p;varying vec2 v;void main(){v=vec2(p.x*.5+.5,.5-p.y*.5);gl_Position=vec4(p,0.,1.);}';
const FS = `precision highp float;varying vec2 v;uniform sampler2D img,dep;uniform vec2 pan,par,px;uniform float zoom,focus,asp,tm,blur,dim;
vec3 tap(vec2 q){return texture2D(img,clamp(q,.002,.998)).rgb;}
void main(){vec2 uv=(v-.5)/zoom+.5+pan;uv.x=(uv.x-.5)*asp+.5;
float d=texture2D(dep,uv).r;vec2 o=par*(d-focus);d=texture2D(dep,uv-o).r;o=par*(d-focus);d=texture2D(dep,uv-o).r;o=par*(d-focus);
vec2 q=uv-o;vec2 ca=(v-.5)*(.0028+blur*.03);vec3 c;
if(blur>.001){c=vec3(0.);for(int i=0;i<12;i++){float f=(float(i)/11.-.5)*blur*.11;vec2 s=q+vec2(f,f*.08);c+=vec3(tap(s+ca).r,tap(s).g,tap(s-ca).b);}c/=12.;}
else{c=vec3(tap(q+ca).r,tap(q).g,tap(q-ca).b);vec3 b=(tap(q+vec2(px.x,0.))+tap(q-vec2(px.x,0.))+tap(q+vec2(0.,px.y))+tap(q-vec2(0.,px.y)))*.25;c=clamp(c+(c-b)*.65,0.,1.);}
float L=dot(c,vec3(.299,.587,.114));c=mix(vec3(L),c,.9);
c=mix(c,c*vec3(.76,1.0,1.2),(1.-smoothstep(.04,.5,L))*.5);c=mix(c,c*vec3(1.05,1.0,.95),smoothstep(.55,.95,L)*.25);c=(c-.5)*1.1+.5;
vec2 r=v-vec2(.5,.45);float vg=smoothstep(.3,.95,length(r*vec2(1.,.6)*1.5));c*=1.-.5*vg;
float n=fract(sin(dot(v*vec2(1234.5,987.6)+tm,vec2(12.9898,78.233)))*43758.5453);c+=(n-.5)*.04;c*=1.-dim;
gl_FragColor=vec4(clamp(c,0.,1.),1.);}`;
let U = {};
function glInit() {
  const sh = (t, s) => { const o = gl.createShader(t); gl.shaderSource(o, s); gl.compileShader(o); if (!gl.getShaderParameter(o, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(o)); return o; };
  const P = gl.createProgram(); gl.attachShader(P, sh(gl.VERTEX_SHADER, VS)); gl.attachShader(P, sh(gl.FRAGMENT_SHADER, FS)); gl.linkProgram(P); gl.useProgram(P);
  const b = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, b); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
  const l = gl.getAttribLocation(P, 'p'); gl.enableVertexAttribArray(l); gl.vertexAttribPointer(l, 2, gl.FLOAT, false, 0, 0);
  ['img', 'dep', 'pan', 'par', 'px', 'zoom', 'focus', 'asp', 'tm', 'blur', 'dim'].forEach(n => U[n] = gl.getUniformLocation(P, n));
  gl.uniform1i(U.img, 0); gl.uniform1i(U.dep, 1); gl.viewport(0, 0, W, H);
}
function tex(src) {
  const t = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, t); gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, src);
  [gl.TEXTURE_WRAP_S, gl.TEXTURE_WRAP_T].forEach(k => gl.texParameteri(gl.TEXTURE_2D, k, gl.CLAMP_TO_EDGE));
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR); return t;
}
const img = s => new Promise(r => { const i = new Image(); i.onload = () => r(i); i.onerror = () => r(null); i.src = s; });
const SCN = {};
async function loadScenes(ids) {
  glInit();
  await Promise.all(ids.map(async id => {
    const [im, dp] = await Promise.all([img(`scn/img/${id}.jpg`), img(`scn/depth/${id}.png`)]);
    if (!im) return; let d = dp; if (!d) { d = mk(4, 4); const x = d.getContext('2d'); x.fillStyle = '#808080'; x.fillRect(0, 0, 4, 4); }
    SCN[id] = { t: tex(im), d: tex(d), asp: (W / H) / (im.width / im.height), w: im.width, h: im.height };
  }));
}
const CAMS = {
  push: e => ({ zoom: 1.05 + .11 * e, pan: [0, -.012 * e], par: [.014 * (2 * e - 1), -.004] }),
  pull: e => ({ zoom: 1.2 - .12 * e, pan: [0, .01 * (1 - e)], par: [-.012 * (2 * e - 1), .004] }),
  slideL: e => ({ zoom: 1.13, pan: [.035 - .07 * e, -.006], par: [.016 * (2 * e - 1), 0] }),
  slideR: e => ({ zoom: 1.13, pan: [-.035 + .07 * e, -.006], par: [-.016 * (2 * e - 1), 0] }),
  rise: e => ({ zoom: 1.12, pan: [0, .035 - .06 * e], par: [.006 * Math.sin(e * 3), -.012 * (2 * e - 1)] }),
  orbit: e => ({ zoom: 1.08 + .05 * Math.sin(e * Math.PI), pan: [0, -.008], par: [.02 * Math.sin((e - .5) * Math.PI), .006 * Math.cos(e * Math.PI)] }),
  rush: e => ({ zoom: 1.04 + .3 * e * e, pan: [0, 0], par: [.01 * Math.sin(e * 4), .006 * Math.cos(e * 3)] }),
};
const CAMBY = { hook: 'pull', nv2: 'push', nv1: 'slideL', ipo: 'rise', spx: 'slideR', law: 'push', gls: 'orbit', cta: 'rush' };
function drawBg(id, p, t, x = {}) {
  const s = SCN[id] || SCN[Object.keys(SCN)[0]]; if (!s) { c.fillStyle = C.bg; c.fillRect(0, 0, W, H); return; }
  const cam = CAMS[CAMBY[id] || 'push'](eIO(p));
  const z = cam.zoom * (x.zoomMul || 1), pan = [cam.pan[0] + (x.panX || 0) + .0015 * Math.sin(t * .7), cam.pan[1] + .001 * Math.sin(t * .53 + 1)];
  gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, s.t); gl.activeTexture(gl.TEXTURE1); gl.bindTexture(gl.TEXTURE_2D, s.d);
  gl.uniform2f(U.pan, pan[0], pan[1]); gl.uniform2f(U.par, cam.par[0], cam.par[1]); gl.uniform2f(U.px, 1 / s.w, 1 / s.h);
  gl.uniform1f(U.zoom, z); gl.uniform1f(U.focus, .5); gl.uniform1f(U.asp, Math.min(1, s.asp)); gl.uniform1f(U.tm, Math.floor(t * 24) * .37 % 97);
  gl.uniform1f(U.blur, x.blur || 0); gl.uniform1f(U.dim, x.dim || 0);
  gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
  c.save(); c.globalAlpha = x.alpha ?? 1; c.drawImage(glc, 0, 0, W, H); c.restore();
}

// ---------------- sprites ----------------
function glowSprite(col) { const k = mk(128, 128), x = k.getContext('2d'), g = x.createRadialGradient(64, 64, 0, 64, 64, 64); g.addColorStop(0, `rgba(${col},1)`); g.addColorStop(.35, `rgba(${col},.35)`); g.addColorStop(1, `rgba(${col},0)`); x.fillStyle = g; x.fillRect(0, 0, 128, 128); return k; }
const G_CY = glowSprite('46,230,255'), G_WH = glowSprite('255,255,255'), G_VI = glowSprite('123,92,255');
const GRAIN = [0, 1, 2].map(k => { const g = mk(270, 480), x = g.getContext('2d'), d = x.createImageData(270, 480); for (let i = 0; i < d.data.length; i += 4) { const v = 128 + (R(i + k * 7, 3) - .5) * 150; d.data[i] = d.data[i + 1] = d.data[i + 2] = v; d.data[i + 3] = 255; } x.putImageData(d, 0, 0); return g; });
const BUF = mk(W, H), bx = BUF.getContext('2d');

// ---------------- drawing helpers ----------------
function rr(x, y, w, h, r) { c.beginPath(); c.roundRect(x, y, w, h, r); }
function txt(s, x, y, font, col, o = {}) {
  c.save(); c.font = font; c.fillStyle = col; c.textAlign = o.align || 'left'; c.textBaseline = o.base || 'alphabetic'; c.letterSpacing = o.ls || '0px';
  if (o.glow) { c.shadowColor = o.glow; c.shadowBlur = o.blur || 30; }
  if (o.stroke) { c.lineJoin = 'round'; c.strokeStyle = o.stroke; c.lineWidth = o.sw || 10; c.strokeText(s, x, y); }
  c.fillText(s, x, y); c.restore();
}
function tw(s, font, ls = '0px') { c.save(); c.font = font; c.letterSpacing = ls; const w = c.measureText(s).width; c.restore(); return w; }
function pop(t, t0, d = .28) { return t < t0 ? 0 : eBack((t - t0) / d); }
function fade(t, t0, d = .2) { return clamp((t - t0) / d); }
function chip(s, x, y, t, t0, style = 'cyan', o = {}) {
  if (t < t0) return 0;
  const k = pop(t, t0), a = fade(t, t0, .12) * (o.alpha ?? 1), font = `700 ${o.size || 30}px ${F.mono}`, ls = '1px';
  const icon = o.icon ? 46 : 0, w = tw(s, font, ls) + 48 + icon, h = (o.size || 30) + 34;
  const col = { cyan: C.cyan, red: C.red, yel: C.yel, white: C.white, vio: C.vio }[style];
  const cx = o.align === 'center' ? x - w / 2 : x;
  c.save(); c.globalAlpha = a; c.translate(cx + w / 2, y + h / 2); c.scale(.6 + .4 * k, .6 + .4 * k); c.translate(-w / 2, -h / 2);
  c.shadowColor = 'rgba(0,0,0,.5)'; c.shadowBlur = 24; c.shadowOffsetY = 8;
  rr(0, 0, w, h, h / 2); c.fillStyle = o.solid ? col : 'rgba(6,10,18,.82)'; c.fill(); c.shadowColor = 'transparent';
  c.lineWidth = 2.5; c.strokeStyle = col; c.globalAlpha = a * (o.solid ? 1 : .85); c.stroke(); c.globalAlpha = a;
  if (o.icon) drawIcon(o.icon, 24 + 18, h / 2, 17, o.solid ? '#05070c' : col);
  txt(s, 24 + icon, h / 2 + 1, font, o.solid ? '#05070c' : C.white, { base: 'middle', ls });
  c.restore(); return w;
}
function drawIcon(kind, x, y, r, col) {
  c.save(); c.translate(x, y); c.fillStyle = col; c.strokeStyle = col; c.lineWidth = 3.5; c.lineJoin = 'round'; c.lineCap = 'round';
  if (kind === 'warn') { c.beginPath(); c.moveTo(0, -r); c.lineTo(r * 1.1, r * .85); c.lineTo(-r * 1.1, r * .85); c.closePath(); c.stroke(); c.fillRect(-1.75, -r * .35, 3.5, r * .65); c.beginPath(); c.arc(0, r * .55, 2.4, 0, 7); c.fill(); }
  else if (kind === 'pin') { c.beginPath(); c.arc(0, -r * .25, r * .62, Math.PI * .85, Math.PI * 2.15); c.lineTo(0, r); c.closePath(); c.stroke(); c.beginPath(); c.arc(0, -r * .25, r * .22, 0, 7); c.fill(); }
  else if (kind === 'up') { c.beginPath(); c.moveTo(-r * .8, r * .5); c.lineTo(-r * .2, -r * .1); c.lineTo(r * .15, r * .25); c.lineTo(r * .85, -r * .55); c.stroke(); c.beginPath(); c.moveTo(r * .35, -r * .6); c.lineTo(r * .9, -r * .6); c.lineTo(r * .9, -r * .05); c.stroke(); }
  else if (kind === 'law') { c.save(); c.rotate(-.6); c.fillRect(-r * .55, -r * .75, r * 1.1, r * .55); c.fillRect(-r * .14, -r * .2, r * .28, r * 1.1); c.restore(); c.fillRect(-r * .95, r * .62, r * 1.3, r * .3); }
  else if (kind === 'cal') { rr(-r * .9, -r * .7, r * 1.8, r * 1.6, 4); c.stroke(); c.fillRect(-r * .9, -r * .7, r * 1.8, r * .45); }
  else if (kind === 'bell') { c.beginPath(); c.moveTo(-r * .8, r * .5); c.quadraticCurveTo(-r * .7, -r * .9, 0, -r * .9); c.quadraticCurveTo(r * .7, -r * .9, r * .8, r * .5); c.closePath(); c.fill(); c.beginPath(); c.arc(0, r * .72, r * .22, 0, 7); c.fill(); }
  else if (kind === 'play') { c.beginPath(); c.moveTo(-r * .45, -r * .6); c.lineTo(r * .7, 0); c.lineTo(-r * .45, r * .6); c.closePath(); c.fill(); }
  c.restore();
}
function panel(x, y, w, h, a = 1, accent = C.cyan) {
  c.save(); c.globalAlpha = a; c.shadowColor = 'rgba(0,0,0,.55)'; c.shadowBlur = 40; c.shadowOffsetY = 14;
  rr(x, y, w, h, 28); c.fillStyle = C.panel; c.fill(); c.shadowColor = 'transparent';
  const g = c.createLinearGradient(x, y, x + w, y + h); g.addColorStop(0, 'rgba(46,230,255,.55)'); g.addColorStop(.5, 'rgba(46,230,255,.08)'); g.addColorStop(1, 'rgba(123,92,255,.45)');
  c.lineWidth = 2; c.strokeStyle = g; c.stroke();
  rr(x + 18, y + 26, 7, h - 52, 4); c.fillStyle = accent; c.fill(); c.restore();
}

// ---------------- timeline ----------------
let TL = null, PAGES = [];
const norm = s => s.toLowerCase().replace(/[^a-z0-9.$]/g, '');
function cue(seg, word, nth = 0) {
  const w = norm(word); let k = 0;
  for (const x of seg.words) { if (norm(x[0]).startsWith(w)) { if (k === nth) return x[1]; k++; } }
  for (const x of seg.words) if (norm(x[0]).includes(w)) return x[1];
  console.warn('cue missing', seg.id, word); return seg.t0 + 1;
}
function buildPages() {
  PAGES = [];
  for (const s of TL.segs) {
    let cur = [];
    const flush = () => { if (cur.length) PAGES.push({ seg: s.id, words: cur }); cur = []; };
    s.words.forEach((w, i) => {
      const prev = s.words[i - 1], gap = prev ? w[1] - prev[2] : 0;
      const chars = cur.reduce((a, x) => a + x[0].length + 1, 0) + w[0].length;
      if (cur.length && (cur.length >= 3 || chars > 15 || gap > .16)) flush();
      cur.push(w);
    });
    flush();
  }
  PAGES.forEach(p => { p.t0 = p.words[0][1] - .04; });
  PAGES.forEach((p, i) => { const nx = PAGES[i + 1]; const end = p.words[p.words.length - 1][2] + .35; p.t1 = nx && nx.seg === p.seg ? Math.min(nx.t0, end + .6) : end; });
}
const SEGINFO = {
  hook: { kick: 'BREAKING', l1: "NVIDIA'S CEO", l2: 'RESIGNS', c2: C.red, sub: '+ a trillion-dollar AI IPO is coming' },
  s1: { kick: '01 · NVIDIA', l1: 'NVIDIA BOSS', l2: 'STEPS DOWN', sub: 'Resigns days after admitting an affair', src: 'SOURCES: NVIDIA SEC FILING · NYT VIA FORTUNE' },
  s2: { kick: '02 · ANTHROPIC', l1: 'CLAUDE MAKER', l2: 'GOES PUBLIC', sub: 'Nasdaq listing planned for next week', src: 'SOURCES: RENAISSANCE CAPITAL · WSJ' },
  s3: { kick: '03 · SPACEX', l1: 'SPACEX GOES', l2: 'ALL-IN ON AI', sub: 'Two giant AI supercomputer campuses', src: 'SOURCES: QUARTZ · ANADOLU AGENCY' },
  s4: { kick: '04 · AI LAWSUIT', l1: 'AI GIANTS', l2: 'SUED TO PAUSE', sub: 'Nonprofits want next-gen AI frozen', src: 'SOURCE: AL JAZEERA' },
  s5: { kick: '05 · WEARABLES', l1: 'GEMINI SMART', l2: 'GLASSES', sub: 'Google × Samsung · pre-orders open', src: 'SOURCES: THE NEXT WEB · ANDROID HEADLINES' },
  cta: { kick: 'YOUR TURN', l1: 'WHICH ONE', l2: 'SHOCKED YOU?', c2: C.yel, sub: 'Comment the number below' },
};
function init(tl) { TL = tl; buildPages(); return TL.segs.length; }
window.init = init;
window.READY = (async () => {
  const fonts = [['Anton', 'fonts/Anton.ttf', '400'], ['Space Grotesk', 'fonts/SpaceGrotesk.ttf', '300 700'], ['Inter', 'fonts/Inter.ttf', '100 900'], ['JetBrains Mono', 'fonts/JetBrainsMono.ttf', '100 800'], ['Brico', '../fonts/Bricolage.ttf', '200 800']];
  await Promise.all(fonts.map(async ([n, u, w]) => { try { const f = new FontFace(n, `url(${u})`, { weight: w }); await f.load(); document.fonts.add(f); } catch (e) { console.warn('font', n, e.message); } }));
  await loadScenes(['hook', 'nv1', 'nv2', 'ipo', 'spx', 'law', 'gls', 'cta']);
  return Object.keys(SCN).length;
})();

// ---------------- layers ----------------
const TR = .24;   // half-length of the whip transition between segments
function background(t) {
  const segs = TL.segs; let i = segs.findIndex(s => t >= s.t0 && t < s.t1); if (i < 0) i = segs.length - 1;
  const s = segs[i];
  const scAt = (seg, tt) => seg.scenes.find(x => tt >= x[1] && tt < x[2]) || seg.scenes[seg.scenes.length - 1];
  const prog = (sc, tt) => clamp((tt - sc[1]) / (sc[2] - sc[1]));
  let opt = {};
  const nb = segs[i + 1] ? s.t1 : null;
  if (i > 0 && t - s.t0 < TR) { const k = 1 - (t - s.t0) / TR; opt = { blur: k * k, zoomMul: 1 + .22 * k * k, panX: -.07 * k * k }; }
  if (nb !== null && nb - t < TR) { const k = 1 - (nb - t) / TR; opt = { blur: k * k, zoomMul: 1 + .25 * k * k, panX: .08 * k * k }; }
  const sc = scAt(s, t); drawBg(sc[0], prog(sc, t), t, opt);
  // soft cross-cut between two scenes inside one segment
  const j = s.scenes.indexOf(sc);
  if (j > 0 && t - sc[1] < .45) { const prev = s.scenes[j - 1]; drawBg(prev[0], 1, t, { alpha: 1 - eIO((t - sc[1]) / .45), zoomMul: 1 + .06 * (t - sc[1]) / .45 }); }
  return { i, s };
}
function grade(t) {
  let g = c.createLinearGradient(0, 0, 0, 760); g.addColorStop(0, 'rgba(2,5,10,.9)'); g.addColorStop(.55, 'rgba(2,5,10,.55)'); g.addColorStop(1, 'rgba(2,5,10,0)');
  c.fillStyle = g; c.fillRect(0, 0, W, 760);
  g = c.createLinearGradient(0, 1050, 0, H); g.addColorStop(0, 'rgba(2,5,10,0)'); g.addColorStop(.35, 'rgba(2,5,10,.6)'); g.addColorStop(1, 'rgba(2,5,10,.92)');
  c.fillStyle = g; c.fillRect(0, 1050, W, H - 1050);
  // light leak drifting across
  c.save(); c.globalCompositeOperation = 'screen'; const lx = W * (.5 + .6 * Math.sin(t * .23)), ly = 300 + 200 * Math.sin(t * .31);
  c.globalAlpha = .16; c.drawImage(G_VI, lx - 700, ly - 700, 1400, 1400); c.globalAlpha = .1; c.drawImage(G_CY, W - lx - 500, 1300 - ly * .3, 1000, 1000); c.restore();
  // floating particles
  c.save(); c.globalCompositeOperation = 'lighter';
  for (let i = 0; i < 46; i++) {
    const sp = 10 + R(i, 1) * 26, y = ((R(i, 2) * H * 1.1 - t * sp) % (H * 1.1) + H * 1.1) % (H * 1.1) - 60, x = (R(i, 3) * W + Math.sin(t * .4 + i) * 30);
    const r = 2 + R(i, 4) * 6, a = (.18 + .4 * (.5 + .5 * Math.sin(t * (1 + R(i, 5) * 2) + i))) * (R(i, 6) < .3 ? 1 : .5);
    c.globalAlpha = a; c.drawImage(i % 3 ? G_CY : G_WH, x - r * 3, y - r * 3, r * 6, r * 6);
  }
  c.restore();
  // fine scanlines
  c.save(); c.globalAlpha = .035; c.fillStyle = '#000'; for (let y = (t * 40) % 6; y < H; y += 6) c.fillRect(0, y, W, 2); c.restore();
}
function topBar(t, s) {
  const st = TL.segs.filter(x => x.n), n = s.n || (s.id === 'cta' ? 6 : 0);
  // story progress
  const x0 = 60, ww = (960 - 4 * 12) / 5;
  st.forEach((q, k) => {
    const x = x0 + k * (ww + 12); rr(x, 76, ww, 7, 4); c.fillStyle = 'rgba(255,255,255,.22)'; c.fill();
    const f = n > q.n ? 1 : n === q.n ? clamp((t - q.t0) / (q.t1 - q.t0)) : 0;
    if (f > 0) { rr(x, 76, ww * f, 7, 4); const g = c.createLinearGradient(x, 0, x + ww, 0); g.addColorStop(0, C.white); g.addColorStop(1, C.cyan); c.fillStyle = g; c.fill(); }
  });
  // channel badge
  const gx = 60, gy = 112; rr(gx, gy, 62, 62, 16); const g = c.createLinearGradient(gx, gy, gx + 62, gy + 62); g.addColorStop(0, C.cyan); g.addColorStop(1, C.vio); c.fillStyle = g; c.fill();
  drawIcon('play', gx + 33, gy + 31, 20, '#fff');
  txt('@TECHVIBE24', gx + 82, gy + 30, `700 34px ${F.ui}`, C.white, { base: 'middle', ls: '1px' });
  txt('TECH NEWS IN 60 SECONDS', gx + 82, gy + 60, `600 19px ${F.mono}`, C.cyan, { base: 'middle', ls: '2px' });
  // live dot + date
  const a = .55 + .45 * Math.sin(t * 6); c.save(); c.globalAlpha = a; c.fillStyle = C.red; c.beginPath(); c.arc(1020 - tw(TL.date, `600 24px ${F.mono}`, '1px') - 22, gy + 31, 8, 0, 7); c.fill(); c.restore();
  txt(TL.date, 1020, gy + 32, `600 24px ${F.mono}`, C.mute, { align: 'right', base: 'middle', ls: '1px' });
}
function headline(t, s) {
  const I = SEGINFO[s.id]; const t0 = s.id === 'hook' ? -1 : s.t0 + .12, lt = t - t0;
  let out = 1; if (s.t1 - t < .3 && s.id !== 'cta') out = clamp((s.t1 - t) / .3);
  c.save(); c.globalAlpha = out;
  // kicker
  if (I.kick === 'BREAKING') chip('BREAKING', 60, 214, t, t0, 'red', { solid: true, size: 28 });
  else chip(I.kick, 60, 214, t, t0, 'cyan', { size: 28 });
  // headline lines with mask reveal
  const font = `400 138px ${F.big}`, Ls = [[I.l1, C.white, 412], [I.l2, I.c2 || C.cyan, 552]];
  Ls.forEach(([s2, col, y], k) => {
    const kk = s.id === 'hook' ? 1 : eOut((lt - .08 - k * .09) / .42); if (kk <= 0) return;
    c.save(); c.beginPath(); c.rect(40, y - 140, 1000, 160); c.clip();
    const yy = y + (1 - kk) * 150; const sc = s.id === 'hook' ? 1 + .14 * (1 - eOut((t + .02) / .22)) : 1;
    c.translate(60, yy); c.scale(sc, sc);
    txt(s2, 0, 0, font, col, { glow: col === C.white ? 'rgba(0,0,0,.6)' : col, blur: col === C.white ? 24 : 18 });
    c.restore();
  });
  const ks = s.id === 'hook' ? fade(t, .1, .3) : fade(lt, .35, .3);
  if (ks > 0) { c.save(); c.globalAlpha = out * ks; txt(I.sub, 62, 622, `500 40px ${F.body}`, C.white, { glow: 'rgba(0,0,0,.8)', blur: 18 }); c.restore(); }
  if (I.src) { const ka = fade(lt, .6, .4) * .8; if (ka > 0) { c.save(); c.globalAlpha = out * ka; txt(I.src, 62, 672, `500 20px ${F.mono}`, C.mute, { ls: '1.5px' }); c.restore(); } }
  c.restore();
}
function nameCard(t, t0, y, name, role, out = 1) {
  if (t < t0) return; const k = eOut((t - t0) / .45), a = fade(t, t0, .25) * out; if (a <= 0) return;
  c.save(); c.globalAlpha = a; c.translate((1 - k) * -120, 0);
  panel(60, y, 820, 150, 1); txt(name, 110, y + 76, `400 66px ${F.big}`, C.white, { ls: '1px' }); txt(role, 112, y + 122, `500 31px ${F.body}`, C.mute);
  c.restore();
}
function countUp(t, t0, dur, to, fmt) { const k = eOut((t - t0) / dur); return fmt(to * k, k); }
function bigNumber(t, t0, str, label, y, opt = {}) {
  if (t < t0 - .1) return; const a = fade(t, t0 - .1, .2) * (opt.alpha ?? 1), k = eBack((t - t0 + .1) / .4);
  c.save(); c.globalAlpha = a; txt(label, 62, y - 220, `700 28px ${F.mono}`, C.cyan, { ls: '3px' });
  c.translate(60, y); c.scale(.85 + .15 * k, .85 + .15 * k);
  txt(str, 0, 0, `400 ${opt.size || 250}px ${F.big}`, C.white, { glow: 'rgba(46,230,255,.75)', blur: 50 });
  c.restore();
}
function story(t, s) {
  const lt = t - s.t0; let out = 1; if (s.t1 - t < .3 && s.id !== 'cta') out = clamp((s.t1 - t) / .3);
  c.save(); c.globalAlpha = out;
  if (s.id === 'hook') {
    const t1 = cue(s, "here's"); if (t > t1 - .1) {
      const k = eBack((t - t1 + .1) / .45), a = fade(t, t1 - .1, .2); c.save(); c.globalAlpha = a; const cx = 300, cy = 900;
      c.translate(cx, cy); c.scale(k, k); c.lineWidth = 14; c.strokeStyle = 'rgba(255,255,255,.18)'; c.beginPath(); c.arc(0, 0, 150, 0, 7); c.stroke();
      const sw = eIO((t - t1) / 1.6); c.strokeStyle = C.cyan; c.shadowColor = C.cyan; c.shadowBlur = 30; c.lineCap = 'round'; c.beginPath(); c.arc(0, 0, 150, -Math.PI / 2, -Math.PI / 2 + Math.PI * 2 * sw); c.stroke(); c.shadowBlur = 0;
      txt('60', 0, 22, `400 150px ${F.big}`, C.white, { align: 'center', base: 'middle' }); txt('SECONDS', 0, 110, `700 24px ${F.mono}`, C.cyan, { align: 'center', ls: '4px' });
      c.restore();
      chip('5 STORIES', 500, 830, t, t1 + .15, 'white', { size: 30 }); chip('NO FLUFF', 500, 920, t, t1 + .3, 'cyan', { size: 30 });
    }
  } else if (s.id === 's1') {
    const tN = cue(s, 'nothing'), tC = cue(s, 'colette'), o1 = t < tC - .2 ? 1 : clamp(1 - (t - tC + .2) / .3);
    nameCard(t, s.t0 + .5, 720, 'JENSEN HUANG', 'Resigned as CEO · effective immediately');
    if (o1 > 0) { chip('CLAIMS UNPROVEN', 60, 905, t, tN - .05, 'yel', { icon: 'warn', alpha: o1 }); chip('NVIDIA: NO SIGN SECRETS LEAKED', 60, 995, t, tN + .9, 'white', { alpha: o1, size: 27 }); }
    nameCard(t, tC - .1, 905, 'COLETTE KRESS', 'CFO · now interim CEO');
  } else if (s.id === 's2') {
    const tV = cue(s, '1.2'), tA = cue(s, 'nasdaq'), tN = cue(s, 'next');
    bigNumber(t, tV - .5, countUp(t, tV - .5, .9, 1.2, v => '$' + v.toFixed(1) + 'T'), 'TARGET VALUE', 1010);
    chip('NASDAQ: ANT', 60, 1060, t, tA, 'cyan', { icon: 'up' }); chip('DEBUT: NEXT WEEK', 470, 1060, t, tN, 'white', { icon: 'cal' });
  } else if (s.id === 's3') {
    const tV = cue(s, '74'), tT = cue(s, 'texas'), tZ = cue(s, 'arizona');
    bigNumber(t, tV - .45, countUp(t, tV - .45, .8, 74, v => '$' + Math.round(v) + 'B+'), 'AI SUPERCOMPUTER SPEND', 1010);
    chip('TEXAS', 60, 1060, t, tT, 'cyan', { icon: 'pin' }); chip('ARIZONA', 300, 1060, t, tZ, 'cyan', { icon: 'pin' });
  } else if (s.id === 's4') {
    c.save(); const a = fade(lt, .5, .3); c.globalAlpha = a; txt('DEFENDANTS', 62, 735, `700 28px ${F.mono}`, C.cyan, { ls: '3px' }); c.restore();
    const names = [['openai', 'OPENAI'], ['google', 'GOOGLE'], ['meta', 'META'], ['anthropic', 'ANTHROPIC'], ['spacex', 'SPACEX']];
    const pos = [[60, 765], [330, 765], [600, 765], [60, 855], [370, 855]];
    names.forEach(([w, n], k) => chip(n, pos[k][0], pos[k][1], t, cue(s, w) - .05, 'white', { size: 32 }));
    chip('ASK: FREEZE NEXT-GEN AI', 60, 965, t, cue(s, 'freeze') - .05, 'red', { icon: 'law', solid: true });
    chip('4 NONPROFITS · SAN FRANCISCO', 60, 1060, t, cue(s, 'suing'), 'cyan', { size: 26 });
  } else if (s.id === 's5') {
    const tV = cue(s, '395'), tD = cue(s, 'december'), tG = cue(s, 'google');
    bigNumber(t, tV - .45, countUp(t, tV - .45, .8, 395, v => '$' + Math.round(v)), 'PRE-ORDER FROM', 1010);
    chip('GOOGLE × SAMSUNG', 60, 1060, t, tG, 'white'); chip('SHIPS DEC 10', 480, 1060, t, tD, 'cyan', { icon: 'cal' });
  } else if (s.id === 'cta') {
    const rows = ['NVIDIA CEO OUT', '$1.2T AI IPO', '$74B AI BUILD', 'AI PAUSE LAWSUIT', '$395 AI GLASSES'];
    rows.forEach((r, k) => {
      const t0 = s.t0 + .4 + k * .12; if (t < t0) return; const kk = eOut((t - t0) / .4), a = fade(t, t0, .2);
      c.save(); c.globalAlpha = a; c.translate((1 - kk) * -80, 0); const y = 700 + k * 74;
      rr(60, y, 600, 62, 16); c.fillStyle = 'rgba(8,13,22,.78)'; c.fill(); c.lineWidth = 2; c.strokeStyle = 'rgba(46,230,255,.35)'; c.stroke();
      txt(String(k + 1), 92, y + 33, `400 44px ${F.big}`, C.yel, { base: 'middle', align: 'center' }); txt(r, 130, y + 33, `700 30px ${F.ui}`, C.white, { base: 'middle', ls: '1px' });
      c.restore();
    });
    const tf = cue(s, 'follow');
    if (t > tf - .15) {
      const k = eBack((t - tf + .15) / .4), pulse = 1 + .035 * Math.sin((t - tf) * 7), a = fade(t, tf - .15, .2);
      c.save(); c.globalAlpha = a; c.translate(380, 1125); c.scale(k * pulse, k * pulse);
      c.shadowColor = 'rgba(255,46,77,.7)'; c.shadowBlur = 40; rr(-320, -52, 640, 104, 52); c.fillStyle = C.red; c.fill(); c.shadowBlur = 0;
      drawIcon('bell', -250, 0, 22, '#fff'); txt('FOLLOW @TECHVIBE24', 30, 4, `700 40px ${F.ui}`, '#fff', { align: 'center', base: 'middle', ls: '1px' });
      c.restore();
    }
  }
  c.restore();
}
function captions(t) {
  const p = PAGES.find(q => t >= q.t0 && t < q.t1); if (!p) return;
  const font = n => `400 ${n}px ${F.big}`, ls = '1px';
  const words = p.words.map(w => w[0].toUpperCase());
  let size = 112, gap = 26; const widths = () => words.map(w => tw(w, font(size), ls)); let ws = widths(), total = ws.reduce((a, b) => a + b, 0) + gap * (ws.length - 1);
  while (total > 900 && size > 70) { size -= 6; ws = widths(); total = ws.reduce((a, b) => a + b, 0) + gap * (ws.length - 1); }
  const k = eBack((t - p.t0) / .16), a = clamp((t - p.t0) / .06) * clamp((p.t1 - t) / .06);
  const cx = 490, cy = 1300; let x = cx - total / 2;
  c.save(); c.globalAlpha = a; c.translate(cx, cy); c.scale(.8 + .2 * k, .8 + .2 * k); c.translate(-cx, -cy);
  words.forEach((w, i) => {
    const [_, w0, w1] = p.words[i]; const on = t >= w0 - .03; const act = on && (t < w1 + .05 || i === words.length - 1 && t < p.t1);
    const col = act ? C.yel : on ? C.white : 'rgba(244,247,251,.55)';
    c.save(); const bump = act ? 1 + .06 * eBack(clamp((t - w0 + .03) / .12)) : 1; c.translate(x + ws[i] / 2, cy); c.scale(bump, bump);
    c.shadowColor = 'rgba(0,0,0,.7)'; c.shadowBlur = 26; c.shadowOffsetY = 6;
    txt(w, 0, 0, font(size), col, { align: 'center', base: 'middle', stroke: 'rgba(2,4,8,.92)', sw: 14, ls });
    c.restore(); x += ws[i] + gap;
  });
  c.restore();
}
function transitionFx(t) {
  for (const s of TL.segs.slice(1)) {
    const d = t - s.t0; if (Math.abs(d) > .16) continue;
    const fl = Math.max(0, 1 - Math.abs(d) / .1);
    // glitch slices
    bx.clearRect(0, 0, W, H); bx.drawImage(cv, 0, 0);
    for (let k = 0; k < 7; k++) { const y = R(k, Math.floor(t * 30)) * H, h = 20 + R(k + 9, Math.floor(t * 30)) * 90, off = (R(k + 3, Math.floor(t * 30)) - .5) * 120 * (1 - Math.abs(d) / .16); c.drawImage(BUF, 0, y, W, h, off, y, W, h); }
    c.save(); c.globalCompositeOperation = 'screen'; c.globalAlpha = fl * .32; c.fillStyle = '#dff9ff'; c.fillRect(0, 0, W, H); c.restore();
  }
}
function aiTag(t) { c.save(); c.globalAlpha = .55; txt('IMAGES: AI ILLUSTRATIONS', 62, 1452, `500 18px ${F.mono}`, C.mute, { ls: '2px' }); c.restore(); }
function vignetteGrain(t) {
  if (t < .14) { c.save(); c.globalCompositeOperation = 'screen'; c.globalAlpha = (1 - t / .14) * .7; c.fillStyle = '#fff'; c.fillRect(0, 0, W, H); c.restore(); }
  c.save(); c.globalCompositeOperation = 'overlay'; c.globalAlpha = .06; c.drawImage(GRAIN[Math.floor(t * 24) % 3], 0, 0, W, H); c.restore();
  // fade out at the very end
  const e = TL.T - t; if (e < .6) { c.save(); c.globalAlpha = 1 - e / .6; c.fillStyle = '#000'; c.fillRect(0, 0, W, H); c.restore(); }
}
function frame(t) {
  c.setTransform(1, 0, 0, 1, 0, 0); c.globalAlpha = 1; c.globalCompositeOperation = 'source-over'; c.fillStyle = C.bg; c.fillRect(0, 0, W, H);
  const { s } = background(t);
  grade(t); topBar(t, s); headline(t, s); story(t, s); captions(t); aiTag(t); transitionFx(t); vignetteGrain(t);
}
window.frame = frame;
