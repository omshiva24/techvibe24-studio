'''Build the news Short timeline (segment times, word timings, scene cuts) and the voice track.
python tools/news_timeline.py ASSETS_DIR VOICE build/'''
import json, os, subprocess, sys
import numpy as np
A, VOICE, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
TEMPO = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
os.makedirs(OUT, exist_ok=True)
SR = 48000
S = json.load(open('news/script.json')); W = json.load(open(f'{A}/vo/words.json'))[VOICE]
def decode(mp3):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', mp3, '-af', f'atempo={TEMPO}', '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768
def env(x, hop=480):
    n = len(x) // hop; return np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1) + 1e-12)
GAP = {'hook': 0.30, 'cta': 0.30}
DEF_GAP = 0.38      # silence before each segment's voice (transition lives here)
START, TAILHOLD = 0.12, 1.7
t, segs, voice = START, [], []
for i, seg in enumerate(S['segments']):
    x = decode(f'{A}/vo/{VOICE}/{seg["id"]}.mp3')
    e = env(x); thr = max(e.max() * 0.04, 1e-3); on = np.where(e > thr)[0]
    a0, a1 = (on[0] * 0.01, (on[-1] + 1) * 0.01) if len(on) else (0, len(x) / SR)
    x = x[int(max(0, a0 - 0.03) * SR): int(min(len(x) / SR, a1 + 0.08) * SR)]      # trim edge silence
    shift = max(0, a0 - 0.03)
    if i: t += GAP.get(seg['id'], DEF_GAP)
    vo0 = t; dur = len(x) / SR
    words = []
    for w, a, b in W[seg['id']]['words']:
        a, b = a / TEMPO, b / TEMPO; parts = w.split()
        if len(parts) > 1:   # tokens like "1.2 trillion dollars": spread the time over the parts by length
            wt = np.array([len(pt) + 1.5 for pt in parts]); cum = np.concatenate([[0], np.cumsum(wt)]) / wt.sum()
            for j, pt in enumerate(parts): words.append([pt, round(vo0 + a + (b - a) * cum[j] - shift, 3), round(vo0 + a + (b - a) * cum[j + 1] - shift, 3)])
        else: words.append([w, round(vo0 + a - shift, 3), round(vo0 + b - shift, 3)])
    if not words:   # no boundaries from this voice: spread words over the voiced span by length
        toks = seg['vo'].split(); wt = np.array([max(2, len(k)) for k in toks], float); cum = np.concatenate([[0], np.cumsum(wt)]) / wt.sum()
        words = [[k, round(vo0 + dur * cum[j], 3), round(vo0 + dur * cum[j + 1], 3)] for j, k in enumerate(toks)]
    voice.append((vo0, x)); segs.append({'id': seg['id'], 'n': seg.get('n'), 'vo0': round(vo0, 3), 'vo1': round(vo0 + dur, 3), 'words': words})
    t = vo0 + dur
T = round(t + TAILHOLD, 3)
# segment visual windows: each segment owns the time from its transition (mid-gap) to the next one
for i, s in enumerate(segs):
    s['t0'] = 0.0 if i == 0 else round((segs[i - 1]['vo1'] + s['vo0']) / 2, 3)
for i, s in enumerate(segs):
    s['t1'] = segs[i + 1]['t0'] if i + 1 < len(segs) else T
# scene cuts inside a segment
CUT = {'s1': 'Nothing'}
for s, seg in zip(segs, S['segments']):
    sc = seg['scenes']
    if len(sc) == 1: s['scenes'] = [[sc[0], s['t0'], s['t1']]]
    else:
        w = next((w for w in s['words'] if w[0].strip('.,').lower() == CUT[s['id']].lower()), None)
        m = round(w[1] - 0.15, 3) if w else round((s['t0'] + s['t1']) / 2, 3)
        s['scenes'] = [[sc[0], s['t0'], m], [sc[1], m, s['t1']]]
tl = {'T': T, 'date': S['date'], 'voice': VOICE, 'segs': segs}
json.dump(tl, open(f'{OUT}/news_tl.json', 'w'), indent=1)
# voice track
y = np.zeros(int((T + 0.5) * SR), np.float32)
for t0, x in voice: i0 = int(t0 * SR); y[i0:i0 + len(x)] += x
np.save(f'{OUT}/voice.npy', y)
print('T', T, [(s['id'], s['t0'], s['vo0'], s['vo1'], len(s['words'])) for s in segs])
