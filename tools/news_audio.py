'''Music bed + sound design + final mix for the news Short (all synthesized here, no samples).
python tools/news_audio.py build/  ->  build/news_mix.wav (48 kHz stereo, before loudness normalisation)'''
import json, sys, wave
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve, sawtooth
B = sys.argv[1]; SR = 48000
tl = json.load(open(f'{B}/news_tl.json')); T = tl['T']; N = int((T + .5) * SR)
rng = np.random.default_rng(24)
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], btype='band', fs=SR, output='sos'), x)
def lp(x, f, o=2): return sosfilt(butter(o, f, btype='low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, btype='high', fs=SR, output='sos'), x)
def add(buf, x, t0, g=1.0):
    i0 = int(t0 * SR)
    if i0 >= len(buf): return
    if i0 < 0: x = x[-i0:]; i0 = 0
    n = min(len(x), len(buf) - i0); buf[i0:i0 + n] += g * x[:n]
def mtof(m): return 440 * 2 ** ((m - 69) / 12)
BPM = 120; BEAT = 60 / BPM; BAR = 4 * BEAT
END = T - 1.2                                   # groove stops here, last hit rings out
nbeats = int(END / BEAT)
L = np.zeros(N); Rr = np.zeros(N); WET = np.zeros(N)
# ---- drums ----
tt = np.arange(int(.45 * SR)) / SR
kick = np.sin(2 * np.pi * np.cumsum(48 + 120 * np.exp(-tt * 32)) / SR) * np.exp(-tt * 7.5)
kick += .4 * hp(rng.standard_normal(len(tt)), 2500) * np.exp(-tt * 400); kick = np.tanh(kick * 1.6) * .9
ts = np.arange(int(.3 * SR)) / SR
snare = bp(rng.standard_normal(len(ts)), 900, 6000) * np.exp(-ts * 16) * .8 + .35 * np.sin(2 * np.pi * 190 * ts) * np.exp(-ts * 28)
th = np.arange(int(.08 * SR)) / SR
hat = hp(rng.standard_normal(len(th)), 7500, 4) * np.exp(-th * 70)
oh = np.arange(int(.35 * SR)) / SR
ohat = hp(rng.standard_normal(len(oh)), 6500, 4) * np.exp(-oh * 9)
for b in range(nbeats):
    t0 = b * BEAT
    add(L, kick, t0, .55); add(Rr, kick, t0, .55)
    if b % 4 in (1, 3): add(L, snare, t0, .2); add(Rr, snare, t0, .2); add(WET, snare, t0, .12)
    for k in range(4):
        v = (.11 if k == 2 else .05) * (1 + .15 * np.sin(b * 1.7 + k))
        add(L, hat, t0 + k * BEAT / 4, v * .8); add(Rr, hat, t0 + k * BEAT / 4, v * 1.1)
    if b % 2 == 1 and b > 8: add(L, ohat, t0 + BEAT / 2, .035); add(Rr, ohat, t0 + BEAT / 2, .045)
# ---- harmony: Am F C G, one chord per bar pair ----
CH = [(45, [57, 60, 64]), (41, [53, 57, 60]), (48, [55, 60, 64]), (43, [55, 59, 62])]
tN = np.arange(N) / SR
pump = np.ones(N)
for b in range(nbeats): i0 = int(b * BEAT * SR); n = min(int(BEAT * SR), N - i0); pump[i0:i0 + n] = 1 - .55 * np.exp(-np.arange(n) / SR / .11)
bass = np.zeros(N); padL = np.zeros(N); padR = np.zeros(N); arp = np.zeros(N)
nch = int(END / (2 * BAR)) + 1
for k in range(nch):
    root, notes = CH[k % 4]; t0 = k * 2 * BAR; t1 = min(END, t0 + 2 * BAR); i0, i1 = int(t0 * SR), int(t1 * SR)
    if i1 <= i0: break
    seg = tN[i0:i1] - t0
    # bass: 8th-note pulses
    f = mtof(root - 12); env = np.exp(-((seg % (BEAT / 2)) / .16))
    bass[i0:i1] += (np.sin(2 * np.pi * f * seg) + .35 * np.sin(2 * np.pi * 2 * f * seg)) * env
    # pad: detuned saws, slow attack
    a = np.clip(seg / .5, 0, 1) * np.clip((t1 - t0 - seg) / .3, 0, 1)
    for m in notes:
        for dt, side in ((-.08, 0), (.08, 1), (0, 2)):
            w = sawtooth(2 * np.pi * mtof(m + dt) * seg + rng.random() * 6) * a
            if side == 0: padL[i0:i1] += w
            elif side == 1: padR[i0:i1] += w
            else: padL[i0:i1] += .5 * w; padR[i0:i1] += .5 * w
    # arp: 16ths over chord tones
    seq = [notes[0] + 12, notes[1] + 12, notes[2] + 12, notes[1] + 24, notes[2] + 12, notes[0] + 24, notes[1] + 12, notes[2] + 24]
    step = BEAT / 4; ns = int((t1 - t0) / step)
    tn = np.arange(int(step * SR * 1.6)) / SR
    for j in range(ns):
        f = mtof(seq[j % 8]); pl = (sawtooth(2 * np.pi * f * tn, .5) * .6 + np.sin(2 * np.pi * f * tn)) * np.exp(-tn * 22)
        add(arp, pl, t0 + j * step, .9 if j % 4 == 0 else .6)
bass = np.tanh(lp(bass, 220) * 1.4) * pump
padL = lp(padL, 1400) * (.55 + .45 * pump); padR = lp(padR, 1400) * (.55 + .45 * pump)
arp = lp(arp, 3200)
dly = int(BEAT * .75 * SR)
arpL = arp.copy(); arpR = np.zeros(N); arpR[dly:] += .55 * arp[:-dly]; arpL[2 * dly:] += .3 * arp[:-2 * dly]
L += .32 * bass + .055 * padL + .05 * arpL; Rr += .32 * bass + .055 * padR + .05 * arpR
WET += .03 * (padL + padR) + .04 * (arpL + arpR)
# ---- sound design ----
def whoosh(d=.55, f0=300, f1=7000):
    n = int(d * SR); x = rng.standard_normal(n); out = np.zeros(n); blk = 480; zi = None
    for i in range(0, n, blk):
        k = i / n; fc = f0 * (f1 / f0) ** k
        sos = butter(2, [fc * .7, min(fc * 1.4, SR / 2 - 100)], btype='band', fs=SR, output='sos')
        if zi is None: zi = np.zeros((sos.shape[0], 2))
        out[i:i + blk], zi = sosfilt(sos, x[i:i + blk], zi=zi)
    e = np.linspace(0, 1, n) ** 2.2; e[-int(.06 * SR):] *= np.linspace(1, 0, int(.06 * SR)); return out * e
def impact(d=1.6):
    t = np.arange(int(d * SR)) / SR
    sub = np.sin(2 * np.pi * np.cumsum(32 + 70 * np.exp(-t * 6)) / SR) * np.exp(-t * 2.6)
    crack = lp(rng.standard_normal(len(t)), 3000) * np.exp(-t * 18)
    return np.tanh(1.5 * sub) * .9 + .45 * crack
def blip(f=1500, d=.09):
    t = np.arange(int(d * SR)) / SR; return (np.sin(2 * np.pi * f * t) + .4 * np.sin(2 * np.pi * f * 1.5 * t)) * np.exp(-t * 45)
def rise(d=.7):
    t = np.arange(int(d * SR)) / SR; return np.sin(2 * np.pi * np.cumsum(500 + 1400 * (t / d) ** 2) / SR) * (t / d) * np.exp(-((t - d) / .05) ** 2 * (t > d - .05))
SFX = np.zeros(N)
imp = impact(); add(SFX, imp, 0, .7); add(WET, imp, 0, .25)
end_imp = impact(2.4); add(SFX, end_imp, END, .55); add(WET, end_imp, END, .35)
for s in tl['segs'][1:]:
    w = whoosh(); add(SFX, w, s['t0'] - len(w) / SR + .06, .32); add(WET, w, s['t0'] - .4, .08)
    add(SFX, impact(.9), s['t0'], .28)
def cue(seg, word, nth=0):
    k = 0
    for x in seg['words']:
        if ''.join(ch for ch in x[0].lower() if ch.isalnum() or ch in '.$').startswith(word):
            if k == nth: return x[1]
            k += 1
    return None
CUES = {'hook': ["here's"], 's1': ['nothing', 'colette'], 's2': ['nasdaq', 'next'], 's3': ['texas', 'arizona'],
        's4': ['openai', 'google', 'meta', 'anthropic', 'spacex', 'freeze'], 's5': ['google', 'december'], 'cta': ['follow']}
RISES = {'s2': '1.2', 's3': '74', 's5': '395'}
for s in tl['segs']:
    for w in CUES.get(s['id'], []):
        t0 = cue(s, w.replace("'", "") if w != "here's" else "heres")
        if t0: add(SFX, blip(1700 if w != 'freeze' else 900), t0, .06); add(WET, blip(), t0, .03)
    if s['id'] in RISES:
        t0 = cue(s, RISES[s['id']])
        if t0: r = rise(.8); add(SFX, r, t0 - .5 - .3, .05)
    if s['id'] == 's1':
        t0 = cue(s, 'jensen')
        if t0: add(SFX, blip(1300), s['t0'] + .5, .08)
# ---- reverb on the wet bus ----
ir_t = np.arange(int(1.6 * SR)) / SR
irL = lp(rng.standard_normal(len(ir_t)), 6000) * np.exp(-ir_t / .32); irR = lp(rng.standard_normal(len(ir_t)), 6000) * np.exp(-ir_t / .32)
irL /= np.sqrt((irL ** 2).sum()); irR /= np.sqrt((irR ** 2).sum())
revL = fftconvolve(WET, irL)[:N]; revR = fftconvolve(WET, irR)[:N]
# ---- duck music under the voice ----
voice = np.load(f'{B}/voice.npy'); voice = np.pad(voice, (0, max(0, N - len(voice))))[:N]
hop = 240; n = N // hop; e = np.sqrt((voice[:n * hop].reshape(n, hop) ** 2).mean(1)); act = (e > .012).astype(float)
g = np.zeros(n); y = 0
for i in range(n): y = y + (act[i] - y) * (.25 if act[i] > y else .012); g[i] = y
duck = np.repeat(1 - .55 * g, hop); duck = np.pad(duck, (0, N - len(duck)), constant_values=1)
fade_out = np.clip((T - .15 - tN) / 1.0, 0, 1)
music_gain = .24 * duck * fade_out
outL = (L + revL * .5) * music_gain + (SFX + revL * .5) * fade_out * .9 + voice * .95
outR = (Rr + revR * .5) * music_gain + (SFX + revR * .5) * fade_out * .9 + voice * .95
mx = max(np.abs(outL).max(), np.abs(outR).max()); outL /= mx / .89; outR /= mx / .89
st = (np.stack([outL, outR], 1)[:int(T * SR)] * 32767).astype(np.int16)
with wave.open(f'{B}/news_mix.wav', 'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())
print('mix', T, 's peak-normalised; voice rms', float(np.sqrt((voice ** 2).mean())), 'music rms', float(np.sqrt(((L * music_gain) ** 2).mean())))
# QA: how far the music sits under the voice while someone is speaking
vm = np.repeat(act, hop); vm = np.pad(vm, (0, N - len(vm)))[:N] > 0
mus = ((L + revL * .5) * music_gain)[vm]; sfx = ((SFX + revL * .5) * fade_out * .9)[vm]; vv = (voice * .95)[vm]
db = lambda x: 20 * np.log10(np.sqrt((hp(x, 120) ** 2).mean()) + 1e-9)   # rough loudness: ignore sub-bass
print('while speaking: voice %.1f dB, music %.1f dB (%.1f dB under), sfx %.1f dB' % (db(vv), db(mus), db(vv) - db(mus), db(sfx)))
