'''Timeline + voice track for the quote Short.   python tools/quote_timeline.py ASSETS_DIR VOICE build_quote/'''
import json, os, subprocess, sys
import numpy as np
A, VOICE, OUT = sys.argv[1], sys.argv[2], sys.argv[3]; os.makedirs(OUT, exist_ok=True); SR = 48000
S = json.load(open('quote/script.json')); W = json.load(open(f'{A}/vo/words.json'))[VOICE]
def decode(mp3):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', mp3, '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768
def env(x, hop=480): n = len(x) // hop; return np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1) + 1e-12)
GAP = {'q2': .6, 'q3': .9, 'q4': .55, 'q5': .55, 'q6': .75, 'q7': .7}
t, segs, voice = 1.0, [], []
for i, seg in enumerate(S['segments']):
    x = decode(f'{A}/vo/{VOICE}/{seg["id"]}.mp3'); e = env(x); on = np.where(e > max(e.max() * .04, 1e-3))[0]
    a0, a1 = (on[0] * .01, (on[-1] + 1) * .01) if len(on) else (0, len(x) / SR); shift = max(0, a0 - .03)
    x = x[int(shift * SR): int(min(len(x) / SR, a1 + .1) * SR)]
    if i: t += GAP.get(seg['id'], .55)
    vo0 = t; dur = len(x) / SR
    words = []
    for w, a, b in W[seg['id']]['words']:
        parts = w.split()
        if len(parts) > 1:
            wt = np.array([len(p) + 1.5 for p in parts]); cum = np.concatenate([[0], np.cumsum(wt)]) / wt.sum()
            words += [[p, round(vo0 + a + (b - a) * cum[j] - shift, 3), round(vo0 + a + (b - a) * cum[j + 1] - shift, 3)] for j, p in enumerate(parts)]
        else: words.append([w, round(vo0 + a - shift, 3), round(vo0 + b - shift, 3)])
    voice.append((vo0, x)); segs.append({'id': seg['id'], 'vo0': round(vo0, 3), 'vo1': round(vo0 + dur, 3), 'words': words, 'sc': seg['scenes']}); t = vo0 + dur
card0 = round(t + .6, 3); T = round(card0 + 4.4, 3)
for i, s in enumerate(segs): s['t0'] = 0.0 if i == 0 else round(segs[i - 1]['vo1'] + (s['vo0'] - segs[i - 1]['vo1']) * .45, 3)
for i, s in enumerate(segs): s['t1'] = segs[i + 1]['t0'] if i + 1 < len(segs) else T
for s in segs:
    sc = s.pop('sc')
    if len(sc) == 1: s['scenes'] = [[sc[0], s['t0'], s['t1']]]
    else:
        w = next((w for w in s['words'] if w[0].strip('.,').lower() == 'every'), None); m = round(w[1] - .25, 3) if w else round((s['t0'] + s['t1']) / 2, 3)
        s['scenes'] = [[sc[0], s['t0'], m], [sc[1], m, s['t1']]]
json.dump({'T': T, 'card0': card0, 'voice': VOICE, 'segs': segs}, open(f'{OUT}/quote_tl.json', 'w'), indent=1)
y = np.zeros(int((T + .5) * SR), np.float32)
for t0, x in voice: i0 = int(t0 * SR); y[i0:i0 + len(x)] += x
np.save(f'{OUT}/voice.npy', y)
print('T', T, 'card0', card0, [(s['id'], s['t0'], s['vo0'], s['vo1']) for s in segs])
