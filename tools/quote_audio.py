'''Epic score + sound design + mix for the quote Short (synthesized).   python tools/quote_audio.py build_quote/'''
import json, sys, wave
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve, sawtooth
B = sys.argv[1]; SR = 48000
tl = json.load(open(f'{B}/quote_tl.json')); T = tl['T']; N = int((T + .3) * SR); seg = {s['id']: s for s in tl['segs']}
rng = np.random.default_rng(9); tN = np.arange(N) / SR
def lp(x, f, o=2): return sosfilt(butter(o, f, btype='low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, btype='high', fs=SR, output='sos'), x)
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], btype='band', fs=SR, output='sos'), x)
def add(buf, x, t0, g=1.0):
    i0 = int(t0 * SR)
    if i0 < 0: x = x[-i0:]; i0 = 0
    n = min(len(x), len(buf) - i0)
    if n > 0: buf[i0:i0 + n] += g * x[:n]
def mtof(m): return 440 * 2 ** ((m - 69) / 12)
def env_ad(n, a, d): t = np.arange(n) / SR; return np.minimum(1, t / max(a, 1e-3)) * np.exp(-t / d)
t3, t6, t5 = seg['q3']['vo0'], seg['q6']['vo0'], seg['q5']['vo0']; card0 = tl['card0']
L = np.zeros(N); Rr = np.zeros(N); WET = np.zeros(N)
# --- harmony: D minor -> Bb -> F -> C (i - VI - III - VII), slow
CH = [(38, [50, 53, 57, 62]), (34, [50, 53, 58, 62]), (41, [48, 53, 57, 60]), (36, [48, 52, 55, 60])]
def pad_note(f, d, bright):
    t = np.arange(int(d * SR)) / SR; a = np.minimum(1, t / .9) * np.minimum(1, (d - t) / .8)
    x = sum(sawtooth(2 * np.pi * f * (1 + det) * t + rng.random() * 6) for det in (-.004, 0, .0045)) / 3
    return lp(x, 500 + 2200 * bright) * a
CLEN = 4.0
k = 0; t = 0.0
while t < T:
    root, notes = CH[k % 4]; bright = .15 if t < t3 else (.4 if t < t6 else .8); d = min(CLEN + 1, T - t + .5)
    vol = .05 if t < t3 else (.08 if t < t6 else .11)
    for j, m in enumerate(notes):
        x = pad_note(mtof(m), d, bright); add(L if j % 2 else Rr, x, t, vol); add(Rr if j % 2 else L, x, t, vol * .6); add(WET, x, t, vol * .5)
    tb = np.arange(int(d * SR)) / SR; sub = np.sin(2 * np.pi * mtof(root - 12) * tb) * np.minimum(1, tb / .3) * np.minimum(1, (d - tb) / .5)
    add(L, sub, t, .16 if t >= t3 else .1); add(Rr, sub, t, .16 if t >= t3 else .1)
    t += CLEN; k += 1
# --- piano motif (soft, starts the piece and returns at the end)
def piano(f, d=2.5):
    t = np.arange(int(d * SR)) / SR
    x = sum(a * np.sin(2 * np.pi * f * h * t) * np.exp(-t * (1.2 + h * .9)) for h, a in ((1, 1), (2, .45), (3, .22), (4, .1)))
    return x * np.minimum(1, t / .004)
MOT = [62, 65, 69, 67, 65, 62, 64, 60]
for i, m in enumerate(MOT * 3):
    tt = .8 + i * .75
    if tt > t3 - .2: break
    p = piano(mtof(m + 12)); add(L, p, tt, .07); add(Rr, p, tt, .06); add(WET, p, tt, .08)
for i, m in enumerate([62, 65, 69, 74, 72, 69]):
    tt = card0 + .3 + i * .6; p = piano(mtof(m + 12), 3); add(L, p, tt, .08); add(Rr, p, tt, .07); add(WET, p, tt, .1)
# --- string ostinato (8ths) from q2 to the end, stronger after the first impact
BEAT = .5
t = seg['q2']['vo0'] - .3
while t < card0:
    root, notes = CH[int(t // CLEN) % 4]; f = mtof(notes[0] - 12)
    n = int(.42 * SR); tt = np.arange(n) / SR; x = lp(sawtooth(2 * np.pi * f * tt) + .5 * sawtooth(2 * np.pi * 2 * f * tt), 1400) * env_ad(n, .01, .16)
    g = .035 if t < t3 else (.06 if t < t6 else .075); add(L, x, t, g); add(Rr, x, t + .012, g); t += BEAT / 2
# --- drums: heartbeat before q3, taiko after
def boom(f=48, d=1.6, click=.5):
    t = np.arange(int(d * SR)) / SR; x = np.sin(2 * np.pi * np.cumsum(f + 90 * np.exp(-t * 18)) / SR) * np.exp(-t * 3.2)
    return np.tanh(1.8 * x) + click * lp(rng.standard_normal(len(t)), 2500) * np.exp(-t * 30)
def taiko(): return boom(70, .7, .35) * .8
t = seg['q2']['vo0']
while t < t3 - .3:
    add(L, boom(52, .5, .05), t, .22); add(Rr, boom(52, .5, .05), t, .22); add(L, boom(52, .4, .05), t + .28, .14); add(Rr, boom(52, .4, .05), t + .28, .14); t += 1.0
t = t3
while t < card0 - .2:
    for off, g in ((0, .3), (.75, .18), (1.0, .26), (1.5, .16)):
        if t + off < card0 - .2: add(L, taiko(), t + off, g); add(Rr, taiko(), t + off, g); add(WET, taiko(), t + off, g * .4)
    t += 2.0
# --- impacts and risers
def riser(d=1.6):
    n = int(d * SR); t = np.arange(n) / SR; x = rng.standard_normal(n); out = np.zeros(n); blk = 480; zi = None
    for i in range(0, n, blk):
        fc = 300 * (8000 / 300) ** (i / n); s_ = butter(2, [fc * .7, min(fc * 1.4, SR / 2 - 100)], btype='band', fs=SR, output='sos')
        if zi is None: zi = np.zeros((s_.shape[0], 2))
        out[i:i + blk], zi = sosfilt(s_, x[i:i + blk], zi=zi)
    return out * (t / d) ** 2.5
for tt, g in ((t3, .9), (t6, 1.1)):
    r = riser(1.8); add(L, r, tt - 1.8, .25 * g); add(Rr, r, tt - 1.8, .25 * g)
    b = boom(38, 3.0, .8); add(L, b, tt - .02, .55 * g); add(Rr, b, tt - .02, .55 * g); add(WET, b, tt, .4 * g)
add(L, boom(40, 3.5, .6), card0, .4); add(Rr, boom(40, 3.5, .6), card0, .4); add(WET, boom(40, 3.5, .6), card0, .35)
# --- rain ambience during the first scene
rain = hp(rng.standard_normal(N), 1200) * .5 + lp(rng.standard_normal(N), 600) * .6
renv = np.clip((seg['q2']['t0'] + .5 - tN) / 1.2, 0, 1) * np.clip(tN / 1.0, 0, 1)
L += rain * renv * .05; Rr += np.roll(rain, 997) * renv * .05
# whooshes on scene changes
for s in tl['segs']:
    for sc in s['scenes'][(1 if s is tl['segs'][0] else 0):]:
        if sc[1] > 0.5: r = riser(.6)[::-1] * 0 + riser(.6); add(L, r, sc[1] - .45, .12); add(Rr, r, sc[1] - .45, .12)
# --- reverb
ir_t = np.arange(int(2.6 * SR)) / SR
irs = [lp(rng.standard_normal(len(ir_t)), 5000) * np.exp(-ir_t / .7) for _ in range(2)]; irs = [ir / np.sqrt((ir ** 2).sum()) for ir in irs]
L += fftconvolve(WET, irs[0])[:N] * .6; Rr += fftconvolve(WET, irs[1])[:N] * .6
# --- duck under the voice, fade, mix
voice = np.load(f'{B}/voice.npy'); voice = np.pad(voice, (0, max(0, N - len(voice))))[:N]
hop = 240; n = N // hop; e = np.sqrt((voice[:n * hop].reshape(n, hop) ** 2).mean(1)); act = (e > .01).astype(float); g = np.zeros(n); y = 0
for i in range(n): y += (act[i] - y) * (.3 if act[i] > y else .015); g[i] = y
duck = np.pad(np.repeat(1 - .4 * g, hop), (0, N - n * hop), constant_values=1)
fade = np.clip((T - tN) / 1.4, 0, 1) * np.clip(tN / .6, 0, 1)
vox = voice + .18 * fftconvolve(voice, irs[0][:int(.9 * SR)] * .5)[:N]          # a little room on the narrator
outL = (L * duck * fade) * .62 + vox; outR = (Rr * duck * fade) * .62 + vox
st = np.stack([outL, outR], 1); st /= np.abs(st).max() / .9
with wave.open(f'{B}/quote_mix.wav', 'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st[:int(T * SR)] * 32767).astype(np.int16).tobytes())
vm = np.repeat(act, hop)[:N]; vm = np.pad(vm, (0, N - len(vm))) > 0
db = lambda x: 20 * np.log10(np.sqrt((hp(x, 120) ** 2).mean()) + 1e-9)
print('while speaking: voice %.1f dB, music %.1f dB' % (db(vox[vm]), db((L * duck * fade * .62)[vm])))
