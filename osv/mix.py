'''Audio for the OS video: voice + soft study music + pen-writing, page-turn and stamp sounds.
Processed in 20-second chunks so a 35-minute mix fits in memory.   python osv/mix.py  ->  osv/build/mix.wav'''
import json, os, wave
import numpy as np
from scipy.signal import butter, sosfilt
HERE = os.path.dirname(os.path.abspath(__file__)); B = f'{HERE}/build'; SR = 48000
tl = json.load(open(f'{B}/tl.json')); T = tl['T']; N = int(T * SR)
voice = np.load(f'{B}/voice.npy', mmap_mode='r')
rng = np.random.default_rng(11)
def sos(kind, f, o=2): return butter(o, f, btype=kind, fs=SR, output='sos')
S_SCR, S_LOWSCR, S_LP_MUS, S_LP_CR = sos('band', [1800, 7000]), sos('band', [400, 1200], 1), sos('low', 3500), sos('low', 6000)
def swish(d=.55):
    n = int(d * SR); x = rng.standard_normal(n).astype(np.float32); out = np.zeros(n, np.float32); blk = 480; zi = None
    for i in range(0, n, blk):
        k = i / n; fc = 700 * (5000 / 700) ** k; s_ = butter(2, [fc * .6, min(fc * 1.6, SR / 2 - 100)], btype='band', fs=SR, output='sos')
        if zi is None: zi = np.zeros((s_.shape[0], 2))
        out[i:i + blk], zi = sosfilt(s_, x[i:i + blk], zi=zi)
    return out * (np.sin(np.pi * np.linspace(0, 1, n)) ** 1.5).astype(np.float32)
def thump(f=70, d=.35):
    t = np.arange(int(d * SR)) / SR; return (np.sin(2 * np.pi * f * t) * np.exp(-t * 14) + .3 * sosfilt(sos('low', 1500), rng.standard_normal(len(t))) * np.exp(-t * 40)).astype(np.float32)
def ep(f, d=2.6):
    t = np.arange(int(d * SR)) / SR; a = np.minimum(1, t / .012)
    return (a * (np.sin(2 * np.pi * f * t) * np.exp(-t * 1.6) + .35 * np.sin(4 * np.pi * f * t) * np.exp(-t * 3.5) + .08 * np.sin(6 * np.pi * f * t) * np.exp(-t * 6)) * (1 + .15 * np.sin(2 * np.pi * 4.5 * t))).astype(np.float32)
# ---- event lists (time, gain, sound, bus)
SW, SW8, TH90, TH55, TH110, TH50 = swish(), swish(.8), thump(90, .2), thump(55, .9), thump(110, .25), thump(50, 1.2)
events = [(0, .5, TH50, 'fx')]
pages = tl['pages']
for i, pg in enumerate(pages):
    if i + 1 < len(pages): events += [(pg['t1'] + .05, .35, SW, 'fx'), (pg['t1'] + .45, .15, TH90, 'fx')]
    if pg['kind'] == 'chapter': events += [(pg['t0'], .3, SW8, 'fx'), (pg['t0'] + .3, .5, TH55, 'fx')]
    for b in pg['beats']:
        for e in b['els']:
            if e['t'] == 'stamp': events.append((e['w0'] + .08, .45, TH110, 'fx'))
BPM = 72; BEAT = 60 / BPM; BAR = 4 * BEAT
CH = [[48, 52, 55, 59], [45, 48, 52, 55], [50, 53, 57, 60], [43, 47, 50, 53]]
EPC = {}
t = 0.0; k = 0
while t < T:
    notes = CH[k % 4]
    for hit, g in ((0, 1), (2.5 * BEAT, .6), (4 * BEAT, .8), (6.5 * BEAT, .5)):
        for j, m in enumerate(notes):
            if m not in EPC: EPC[m] = ep(440 * 2 ** ((m + 12 - 69) / 12))
            events.append((t + hit + j * .012, .16 * g, EPC[m], 'mus'))
    tb = np.arange(int(2 * BAR * SR)) / SR; bass = 440 * 2 ** ((notes[0] - 12 - 69) / 12)
    key = ('b', notes[0])
    if key not in EPC: EPC[key] = (np.sin(2 * np.pi * bass * tb) * np.minimum(1, tb / .05) * np.exp(-tb * .5)).astype(np.float32)
    events.append((t, .22, EPC[key], 'mus')); t += 2 * BAR; k += 1
writes = [(e['w0'], e['w1'], e['t']) for pg in pages for b in pg['beats'] for e in b['els'] if e['t'] not in ('stamp', 'hl')]
# ---- ducking + music level (coarse, whole length)
hop = 480; n = len(voice) // hop
e = np.sqrt((np.asarray(voice[:n * hop]).reshape(n, hop).astype(np.float32) ** 2).mean(1)); act = (e > .01).astype(np.float32)
g = np.zeros(n, np.float32); y = 0.0
for i in range(n): y += (act[i] - y) * (.2 if act[i] > y else .01); g[i] = y
lvl = np.full(n, .55, np.float32)
for pg in pages:
    if pg['kind'] in ('cover', 'chapter', 'outro'): lvl[int(pg['t0'] * 100):int(pg['t1'] * 100)] = 1.0
lvl = np.convolve(lvl, np.ones(100) / 100, mode='same').astype(np.float32)
mgain_c = (1 - .5 * g) * lvl
# ---- render in chunks
CH_S = 20 * SR; zs = {'scr': None, 'low': None, 'mus': None, 'cr': None}
wf = wave.open(f'{B}/mix.wav', 'wb'); wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(SR)
peak = 0; vstat = []; mstat = []
def filt(name, s_, x):
    if zs[name] is None: zs[name] = np.zeros((s_.shape[0], 2))
    y, zs[name] = sosfilt(s_, x, zi=zs[name]); return y.astype(np.float32)
for c0 in range(0, N, CH_S):
    c1 = min(N, c0 + CH_S); L = c1 - c0; ta, tb_ = c0 / SR, c1 / SR
    v = np.zeros(L, np.float32); vv = np.asarray(voice[c0:min(c1, len(voice))], np.float32); v[:len(vv)] = vv
    env = np.zeros(L, np.float32)
    for w0, w1, kind in writes:
        if w1 <= ta or w0 >= tb_: continue
        i0, i1 = max(c0, int(w0 * SR)), min(c1, int(w1 * SR)); kk = (np.arange(i0, i1) / SR - w0).astype(np.float32); dur = w1 - w0
        rate = 9 if kind in ('text', 'table', 'gantt') else 4; ph = (w0 * 13.7) % 6
        st = (np.sin(2 * np.pi * rate * kk + ph) * .5 + .5) ** 3 * (.6 + .4 * np.sin(2 * np.pi * 2.3 * kk + ph * 2))
        fd = np.minimum(1, np.minimum(kk / .05, (dur - kk) / .05)); env[i0 - c0:i1 - c0] = np.maximum(env[i0 - c0:i1 - c0], st * fd * (1 if rate == 9 else .6))
    noise = rng.standard_normal(L).astype(np.float32)
    pen = (filt('scr', S_SCR, noise) * .6 + filt('low', S_LOWSCR, rng.standard_normal(L).astype(np.float32)) * .25) * env
    fx = np.zeros(L, np.float32); mus = np.zeros(L, np.float32)
    for t0, gg, snd, bus in events:
        i0 = int(t0 * SR); i1 = i0 + len(snd)
        if i1 <= c0 or i0 >= c1: continue
        a, b_ = max(i0, c0), min(i1, c1); (fx if bus == 'fx' else mus)[a - c0:b_ - c0] += gg * snd[a - i0:b_ - i0]
    mus = filt('mus', S_LP_MUS, mus)
    cr = np.zeros(L, np.float32); m = rng.random(L) < 6 / SR; cr[m] = rng.standard_normal(m.sum()) * .4; mus += filt('cr', S_LP_CR, cr) * .5
    gi = np.interp(np.arange(c0, c1) / SR * 100, np.arange(n), mgain_c).astype(np.float32)
    tt = np.arange(c0, c1, dtype=np.float32) / SR; fade = np.clip((T - tt) / 2.5, 0, 1) * np.clip(tt / 1.0, 0, 1)
    music = mus * gi * fade * .30
    out = v + pen * .035 + fx * .55 + music
    st = np.stack([out + music * .1, out - music * .1], 1); st = np.tanh(st * 1.05) / 1.05
    peak = max(peak, float(np.abs(st).max())); wf.writeframes((np.clip(st, -1, 1) * 32767).astype(np.int16).tobytes())
    speak = np.repeat(act[c0 // hop:c1 // hop + 1], hop)[:L]; speak = np.pad(speak, (0, L - len(speak))) > 0
    if speak.any(): vstat.append(float((v[speak] ** 2).mean())); mstat.append(float((music[speak] ** 2).mean()))
wf.close()
print('mix written; peak %.2f; music %.1f dB under voice while speaking' % (peak, 10 * np.log10(np.mean(vstat) / max(1e-12, np.mean(mstat)))))
