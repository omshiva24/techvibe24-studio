// Frame composer: story shot (with cross-fades) + lyrics overlay. Everything is a pure function of t.
const cv = document.getElementById('bg'), g = cv.getContext('2d');
const $ = id => document.getElementById(id);
const OFF1 = mkCanvas(W, H), OFF2 = mkCanvas(W, H), o1 = OFF1.getContext('2d'), o2 = OFF2.getContext('2d');
let TL = null, SEGS = [], curV = -2, wordEls = [];
const DEVD = '०१२३४५६७८९', dev = n => String(n).split('').map(d => DEVD[+d]).join('');
const XF = 0.9;  // cross-dissolve seconds

async function init(tl) {
  await window.SCENE_READY;
  TL = tl;
  const segs = [{ t0: 0, shot: 'intro' }];
  TL.sections.forEach((s, i) => segs.push({ t0: s.t0, shot: i === 0 ? 'intro' : i === 1 ? 'section' : 'pavanFly' }));
  TL.verses.forEach(v => {
    const shots = STORY[v.id] || ['blessBig'];
    v.lines.forEach(([a], i) => segs.push({ t0: i === 0 ? v.t0 : a - 0.3, shot: shots[Math.min(i, shots.length - 1)] }));
  });
  segs.push({ t0: TL.outro[0], shot: 'outro' });
  segs.sort((a, b) => a.t0 - b.t0);
  // merge consecutive identical shots so the motion continues instead of restarting
  SEGS = segs.filter((s, i) => i === 0 || s.shot !== segs[i - 1].shot || s.t0 - segs[i - 1].t0 < 0.01);
  SEGS.forEach((s, i) => s.t1 = i + 1 < SEGS.length ? SEGS[i + 1].t0 : TL.T);
  await Promise.all(['100px Yatra', '40px Tiro', 'italic 40px TiroI', '700 40px Brico', '800 40px Brico'].map(f => document.fonts.load(f, 'राम हनुमान Abc')));
  await document.fonts.ready;
  return SEGS.length;
}
function segAt(t) { let k = 0; for (let i = 0; i < SEGS.length; i++) if (SEGS[i].t0 <= t) k = i; return k; }
function drawShot(ctx, seg, t) {
  ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over'; ctx.shadowBlur = 0;
  const d = seg.t1 - seg.t0, p = clamp((t - seg.t0) / d);
  SH[seg.shot](ctx, p, t, d);
}
function buildVerse(i) {
  const box = $('verse'); box.innerHTML = ''; wordEls = [];
  if (i < 0) return;
  const v = TL.verses[i];
  box.className = v.kind === 'doha' ? 'doha' : v.big ? 'big' : '';
  v.rows.forEach((row, r) => {
    const d = document.createElement('div'); d.className = 'row';
    row.forEach(([w, a, b]) => { const s = document.createElement('span'); s.className = 'w'; s.textContent = w; d.appendChild(s); wordEls.push([s, a, b]); });
    let p = v.kind === 'doha' ? (r % 2 === 0 ? ',' : (r === 1 ? '।' : '॥')) : v.kind === 'chaupai' ? (r === 0 ? '।' : '॥') : '॥';
    const s = document.createElement('span'); s.className = 'danda'; s.textContent = p; d.appendChild(s);
    box.appendChild(d);
  });
  box.querySelectorAll('.row').forEach(r => { const k = 990 / r.scrollWidth; if (k < 1) r.style.fontSize = `${parseFloat(getComputedStyle(r).fontSize) * k}px`; });
  $('en').textContent = v.en || '';
  $('pillt').textContent = v.label;
  const n = v.kind === 'chaupai' ? +v.id.slice(1) : null;
  $('cnt').textContent = n ? `${dev(n)} / ${dev(40)}` : v.kind === 'doha' ? 'दोहा' : 'जय श्री राम';
}
function frame(t) {
  const I = TL.intro, O = TL.outro;
  // ---- story ----
  const k = segAt(t), seg = SEGS[k], fadeIn = clamp((t - seg.t0) / XF);
  drawShot(o1, seg, t);
  g.setTransform(1, 0, 0, 1, 0, 0); g.globalAlpha = 1; g.drawImage(OFF1, 0, 0);
  if (fadeIn < 1 && k > 0) { drawShot(o2, SEGS[k - 1], t); g.globalAlpha = 1 - ease(fadeIn); g.drawImage(OFF2, 0, 0); g.globalAlpha = 1; }
  // panel shade so the lyrics always read well
  const band = g.createLinearGradient(0, 1060, 0, 1920);
  band.addColorStop(0, 'rgba(18,2,2,0)'); band.addColorStop(0.16, 'rgba(18,2,2,.72)'); band.addColorStop(0.4, 'rgba(14,1,1,.86)'); band.addColorStop(1, 'rgba(8,1,1,.92)');
  g.fillStyle = band; g.fillRect(0, 1060, W, 860);
  const top = g.createLinearGradient(0, 0, 0, 200); top.addColorStop(0, 'rgba(10,1,1,.55)'); top.addColorStop(1, 'rgba(10,1,1,0)'); g.fillStyle = top; g.fillRect(0, 0, W, 200);
  // ---- lyrics ----
  let vi = -1; TL.verses.forEach((v, i) => { if (t >= v.t0 && t < v.t1) vi = i; });
  if (vi !== curV) { buildVerse(vi); curV = vi; }
  const v = vi >= 0 ? TL.verses[vi] : null, inOutro = t >= O[0];
  const uiA = t < I[1] ? ease((t - (I[1] - 0.6)) / 0.6) : inOutro ? 1 - ease((t - O[0]) / 0.5) : 1;
  ['pill', 'orn', 'en', 'bar', 'cnt', 'title'].forEach(id => $(id).style.opacity = uiA);
  if (v) {
    const a = ease((t - v.t0) / 0.35) * (1 - ease((t - (v.t1 - 0.32)) / 0.32));
    const box = $('verse'); box.style.opacity = a; box.style.transform = `translateY(${(1 - a) * 22}px)`;
    wordEls.forEach(([el, a0, a1]) => {
      if (t >= a1) { if (el.className !== 'w past') { el.className = 'w past'; el.style.transform = ''; el.style.removeProperty('--p'); } }
      else if (t >= a0 - 0.04) { el.className = 'w now'; const q = clamp((t - a0) / Math.max(0.05, a1 - a0)); el.style.setProperty('--p', `${Math.round(q * 100)}%`); el.style.transform = `scale(${1 + 0.07 * Math.sin(Math.min(1, q * 1.4) * Math.PI)})`; }
      else if (el.className !== 'w') { el.className = 'w'; el.style.transform = ''; }
    });
    const ea = ease((t - v.lines[0][0] - 0.25) / 0.5) * (1 - ease((t - (v.t1 - 0.32)) / 0.32));
    $('en').style.opacity = Math.min(uiA, ea); $('pill').style.opacity = Math.min(uiA, a);
  } else { $('verse').style.opacity = 0; $('en').style.opacity = 0; $('pill').style.opacity = 0; }
  const V0 = TL.verses[0].t0, V1 = TL.verses[TL.verses.length - 1].t1, pr = clamp((t - V0) / (V1 - V0));
  $('bar').querySelector('i').style.width = `${pr * 100}%`; $('bar').querySelector('b').style.left = `${pr * 100}%`;
  let sa = 0, sl = '';
  TL.sections.forEach(s => { if (t >= s.t0 - 0.05 && t < s.t1) { sl = s.label; sa = ease((t - s.t0) / 0.4) * (1 - ease((t - (s.t1 - 0.35)) / 0.35)); } });
  const sec = $('sec'); sec.textContent = sl; sec.style.opacity = sa; sec.style.transform = `scale(${0.86 + 0.14 * sa})`;
  const it = $('intro'); it.style.opacity = t < I[1] + 0.1 ? 1 - ease((t - (I[1] - 1.1)) / 0.8) : 0;
  const kids = it.children; [1.0, 1.6, 2.6, 3.2].forEach((d, i) => { const a = ease((t - d) / 0.7); kids[i].style.opacity = a; kids[i].style.transform = `translateY(${(1 - a) * 30}px) scale(${i === 1 ? 0.9 + 0.1 * a : 1})`; });
  const ot = $('outro'); ot.style.opacity = inOutro ? ease((t - O[0] - 0.2) / 0.7) : 0;
  const ok = ot.children; [0.2, 1.4, 1.9, 2.3].forEach((d, i) => { const a = ease((t - O[0] - d) / 0.6); ok[i].style.opacity = a; ok[i].style.transform = `translateY(${(1 - a) * 30}px) scale(${i === 1 ? 0.8 + 0.2 * a + 0.03 * Math.sin((t - O[0]) * 5) * a : 1})`; });
  $('fade').style.opacity = Math.max(1 - ease(t / 1.0), ease((t - (TL.T - 0.9)) / 0.9));
}
window.init = init; window.frame = frame;
