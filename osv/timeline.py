'''Timeline for the OS video: when every page, beat and note element happens.
python osv/timeline.py VOICE_DIR  ->  osv/build/tl.json + osv/build/voice.npy'''
import json, os, subprocess, sys
import numpy as np
from PIL import ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); VD = sys.argv[1]; B = f'{HERE}/build'; os.makedirs(B, exist_ok=True)
S = json.load(open(f'{HERE}/os_script.json')); SR = 48000
FONT = {'body': f'{HERE}/fonts/Kalam-Regular.ttf', 'bold': f'{HERE}/fonts/Kalam-Bold.ttf'}
_fc = {}
def font(kind, size):
    k = (kind, size)
    if k not in _fc: _fc[k] = ImageFont.truetype(FONT[kind], size)
    return _fc[k]
def decode(path):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    hop = 480; n = len(x) // hop; e = np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1)); on = np.where(e > max(e.max() * .03, 1e-3))[0]
    if len(on): x = x[max(0, on[0] * hop - 1200): min(len(x), (on[-1] + 1) * hop + 2400)]
    return x
import re
def plain(s): return re.sub(r'\[([rgkhp]):', '', s).replace(']', '') if '[' in s else s
def write_time(e):
    t = e['t']
    if t == 'text': return max(.35, len(plain(e['s'])) / 30)
    if t in ('rect', 'ellipse'):
        per = 2 * (e['w'] + e['h']) if t == 'rect' else 3.3 * (e['w'] + e['h']) / 2
        return per / 1500 + (len(e['label'] or '') / 34 if e.get('label') else 0) + (.25 if e.get('fill') else 0)
    if t == 'arrow':
        (x1, y1), (x2, y2) = e['p1'], e['p2']; return max(.25, ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** .5 / 1400) + .12 + (len(e['label'] or '') / 34 if e.get('label') else 0)
    if t == 'line':
        p = e['pts']; return max(.25, sum(((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** .5 for a, b in zip(p, p[1:])) / 1300)
    if t == 'table':
        rows = e['rows']; W = sum(e['cw']); Hh = e['rh'] * len(rows)
        grid = (W * (len(rows) + 1) + Hh * (len(e['cw']) + 1)) / 3600
        cells = sum(len(c) for r in rows for c in r) / 42 + .03 * sum(1 for r in rows for c in r if c)
        return grid + cells
    if t == 'gantt': return sum(((s[2] - s[1]) * e['u'] * 2 + e['h'] * 2) / 1800 + .25 for s in e['segs']) + .3
    if t == 'stamp': return .35
    if t == 'hl': return .35
    return .5
tl = {'pages': [], 'T': 0}; t = 0.0; voice = []
GAP, TURN, CARD_PAD = .5, .75, 1.0
for pi, p in enumerate(S['pages']):
    pg = {'i': pi, 'kind': p['kind'], 'title': p['title'], 'ch': p['ch'], 't0': round(t, 3), 'beats': []}
    for k in ('num', 'subs', 'stars'):
        if k in p: pg[k] = p[k]
    if p['kind'] == 'page':   # page title is written first
        title = dict(t='text', x=180, y=150, s=p['title'], size=56, font='bold', color='black', title=True)
        p['beats'][0]['els'].insert(0, title)
    cur = t + (.35 if p['kind'] == 'page' else .6)
    for bi, b in enumerate(p['beats']):
        x = decode(f'{VD}/b{pi:03d}_{bi:02d}.mp3'); d = len(x) / SR
        nat = sum(write_time(e) + .12 for e in b['els'])
        blen = max(d + GAP, nat * .8 + .3)
        speed = max(1.0, nat / max(.1, blen - .3))
        els, et = [], cur + .1
        for e in b['els']:
            wt = write_time(e) / speed; e2 = dict(e); e2['w0'] = round(et, 3); e2['w1'] = round(et + wt, 3); els.append(e2); et += wt + .12 / speed
        pg['beats'].append({'t0': round(cur, 3), 'd': round(d, 3), 'say': b['say'], 'els': els})
        voice.append((cur, x)); cur += blen
    if p['kind'] == 'chapter': cur += CARD_PAD
    if p['kind'] in ('cover', 'outro'): cur += .8
    pg['t1'] = round(cur, 3); tl['pages'].append(pg); t = cur + (TURN if pi + 1 < len(S['pages']) else 0)
tl['T'] = round(t + 1.5, 3); tl['TURN'] = TURN
json.dump(tl, open(f'{B}/tl.json', 'w'), indent=1, ensure_ascii=False)
y = np.zeros(int((tl['T'] + 1) * SR), np.float32)
for t0, x in voice: i0 = int(t0 * SR); y[i0:i0 + len(x)] += x
np.save(f'{B}/voice.npy', y)
chap = [(pg['t0'], pg['num'], pg['title']) for pg in tl['pages'] if pg['kind'] == 'chapter']
print('T', tl['T'], 'min', round(tl['T'] / 60, 2), 'pages', len(tl['pages']))
for c in chap: print('%d:%02d  Ch %d %s' % (c[0] // 60, c[0] % 60, c[1], c[2]))
