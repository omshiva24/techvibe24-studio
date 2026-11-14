'''Nostalgic score + sound design + mix for the Children's Day Short (synthesized).   python tools/kids_audio.py build_kids/'''
import json, sys, wave
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve, sawtooth
B = sys.argv[1]; SR = 48000
tl = json.load(open(f'{B}/quote_tl.json')); T = tl['T']; N = int((T + .3) * SR); seg = {s['id']: s for s in tl['segs']}
rng = np.random.default_rng(14); tN = np.arange(N) / SR
def lp(x, f, o=2): return sosfilt(butter(o, f, btype='low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, btype='high', fs=SR, output='sos'), x)
def add(buf, x, t0, g=1.0):
    i0 = int(t0 * SR)
    if i0 < 0: x = x[-i0:]; i0 = 0
    n = min(len(x), len(buf) - i0)
    if n > 0: buf[i0:i0 + n] += g * x[:n]
def mtof(m): return 440 * 2 ** ((m - 69) / 12)
L = np.zeros(N); Rr = np.zeros(N); WET = np.zeros(N)
t2, t3, t5, t7, tc = .55, seg['m2']['vo0'], 1e9, seg['m7']['vo0'], tl['card0']    # no lonely intro, no percussion: soft and emotional
BEAT = .85; CL = 4 * BEAT
CH = [(48, [60, 64, 67]), (43, [59, 62, 67]), (45, [60, 64, 69]), (41, [60, 65, 69])]     # C  G  Am  F
def piano(f, d=2.6, bright=1.0):
    t = np.arange(int(d * SR)) / SR
    x = sum(a * np.sin(2 * np.pi * f * h * t) * np.exp(-t * (1.1 + h * .8)) for h, a in ((1, 1), (2, .4 * bright), (3, .18 * bright), (4, .08 * bright)))
    return x * np.minimum(1, t / .005)
def musicbox(f, d=2.0):
    t = np.arange(int(d * SR)) / SR
    return (np.sin(2 * np.pi * f * t) * np.exp(-t * 2.2) + .25 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 6) + .12 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t * 9)) * np.minimum(1, t / .002)
def pad(f, d):
    t = np.arange(int(d * SR)) / SR; a = np.minimum(1, t / .8) * np.minimum(1, (d - t) / .7)
    return lp(sum(sawtooth(2 * np.pi * f * (1 + dt) * t + rng.random() * 6) for dt in (-.003, 0, .0035)) / 3, 1600) * a
# --- k1: lonely low piano + clock ticks (deadlines)
for i, m in enumerate([57, 60, 64, 60, 57, 60, 64, 62]):
    tt = .5 + i * .6
    if tt > t2 - .4: break
    p = piano(mtof(m), 2.4, .6); add(L, p, tt, .09); add(Rr, p, tt, .08); add(WET, p, tt, .06)
tick = hp(rng.standard_normal(int(.03 * SR)), 2500) * np.exp(-np.arange(int(.03 * SR)) / SR * 300)
tt = .4
pass
# --- from k2: warm progression, piano arpeggios + music-box melody
MEL = [72, 76, 79, 76, 74, 71, 74, 79, 76, 72, 69, 72, 77, 76, 74, 72]
t = t2 - .35; k = 0
while t < T - 1.0:
    root, notes = CH[k % 4]; warm = 1.0 if t > t3 else .6
    for j in range(8):
        n_ = notes[j % 3] + (12 if j >= 4 else 0); tt = t + j * BEAT / 2
        if tt < T - 1.2: p = piano(mtof(n_), 1.8, warm); add(L, p, tt, .045); add(Rr, p, tt + .006, .05); add(WET, p, tt, .03)
    b = piano(mtof(root - 12), 3.2, .5); add(L, b, t, .1); add(Rr, b, t, .1)
    if t > t3 - .5:
        d = min(CL + .8, T - t)
        for n_ in notes: x = pad(mtof(n_), d); add(L, x, t, .035); add(Rr, x, t + .01, .035); add(WET, x, t, .03)
    for j in range(4):
        tt = t + j * BEAT; m = MEL[(k * 4 + j) % len(MEL)]
        if tt < T - 1.2: mb = musicbox(mtof(m + 12)); add(L, mb, tt, .045); add(Rr, mb, tt, .04); add(WET, mb, tt, .06)
    t += CL; k += 1
# --- light percussion from k5 (street cricket) to the card
def kick():
    t = np.arange(int(.35 * SR)) / SR; return np.sin(2 * np.pi * np.cumsum(50 + 80 * np.exp(-t * 25)) / SR) * np.exp(-t * 9)
def clap():
    t = np.arange(int(.2 * SR)) / SR; return sosfilt(butter(2, [900, 3500], btype='band', fs=SR, output='sos'), rng.standard_normal(len(t))) * np.exp(-t * 22)
def shaker():
    t = np.arange(int(.08 * SR)) / SR; return hp(rng.standard_normal(len(t)), 6000) * np.sin(np.pi * t / .08) ** 2
t = t5 - .2
while t < tc + 1.0:
    for j in range(4):
        tt = t + j * BEAT
        if j in (0, 2): add(L, kick(), tt, .12); add(Rr, kick(), tt, .12)
        if j in (1, 3): add(L, clap(), tt, .05); add(Rr, clap(), tt, .06); add(WET, clap(), tt, .03)
        add(L, shaker(), tt + BEAT / 2, .025); add(Rr, shaker(), tt + BEAT / 2, .03)
    t += CL
# --- rain ambience under the paper-boat scene
rain = hp(rng.standard_normal(N), 1500) * .5 + lp(rng.standard_normal(N), 700) * .5
renv = np.clip((tN - (seg['m5']['t0'] - .3)) / .6, 0, 1) * np.clip((seg['m6']['t0'] + .4 - tN) / .6, 0, 1)
L += rain * renv * .035; Rr += np.roll(rain, 1201) * renv * .035
# --- final card: swell + chimes
sw_t = np.arange(int(1.6 * SR)) / SR; swell = hp(rng.standard_normal(len(sw_t)), 3000) * (sw_t / 1.6) ** 3
add(L, swell, tc - 1.5, .06); add(Rr, swell, tc - 1.5, .06)
for i, m in enumerate([84, 88, 91, 96]):
    mb = musicbox(mtof(m), 2.5); add(L, mb, tc + .1 + i * .12, .06); add(Rr, mb, tc + .16 + i * .12, .06); add(WET, mb, tc + .1 + i * .12, .08)
for n_ in (48, 55, 60, 64, 67):
    d = T - tc; p = pad(mtof(n_), d); add(L, p, tc, .05); add(Rr, p, tc, .05); add(WET, p, tc, .04)
# --- reverb, ducking, mix
ir_t = np.arange(int(2.2 * SR)) / SR
irs = [lp(rng.standard_normal(len(ir_t)), 6000) * np.exp(-ir_t / .55) for _ in range(2)]; irs = [ir / np.sqrt((ir ** 2).sum()) for ir in irs]
L += fftconvolve(WET, irs[0])[:N] * .7; Rr += fftconvolve(WET, irs[1])[:N] * .7
voice = np.load(f'{B}/voice.npy'); voice = np.pad(voice, (0, max(0, N - len(voice))))[:N]
hop = 240; n = N // hop; e = np.sqrt((voice[:n * hop].reshape(n, hop) ** 2).mean(1)); act = (e > .01).astype(float); g = np.zeros(n); y = 0
for i in range(n): y += (act[i] - y) * (.3 if act[i] > y else .015); g[i] = y
duck = np.pad(np.repeat(1 - .35 * g, hop), (0, N - n * hop), constant_values=1)
fade = np.clip((T - tN) / 1.6, 0, 1) * np.clip(tN / .4, 0, 1)
vox = voice + .12 * fftconvolve(voice, irs[0][:int(.6 * SR)] * .5)[:N]
MG = 0.68
outL = (L * duck * fade) * MG + vox; outR = (Rr * duck * fade) * MG + vox
st = np.stack([outL, outR], 1); st /= np.abs(st).max() / .9
with wave.open(f'{B}/quote_mix.wav', 'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st[:int(T * SR)] * 32767).astype(np.int16).tobytes())
vm = np.repeat(act, hop)[:N]; vm = np.pad(vm, (0, N - len(vm))) > 0
db = lambda x: 20 * np.log10(np.sqrt((hp(x, 120) ** 2).mean()) + 1e-9)
print('while speaking: voice %.1f dB, music %.1f dB' % (db(vox[vm]), db((L * duck * fade * MG)[vm])))
