'''Rebuild timeline.json (verse/line/word timings for the karaoke lyrics) from the approved final audio mix.
python tools/timeline.py mix.wav chalisa/chalisa.json build/timeline.json'''
import json, sys, wave
import numpy as np
from scipy.signal import butter, sosfilt
MIX, CH, OUT = sys.argv[1:4]
DEV = '०१२३४५६७८९'
def dev(n): return ''.join(DEV[int(c)] for c in str(n))
# verse windows (t0, t1) of the approved mix, seconds
VT = {'d1': (9.6, 21.3), 'd2': (21.3, 32.7), 'c1': (34.4, 41.8), 'c2': (41.8, 48.7), 'c3': (48.7, 55.6), 'c4': (55.6, 62.6), 'c5': (62.6, 69.0),
      'c6': (69.0, 75.7), 'c7': (75.7, 82.0), 'c8': (82.0, 91.4), 'c9': (91.4, 101.7), 'c10': (101.7, 111.4), 'c11': (111.4, 120.8),
      'c12': (120.8, 129.6), 'c13': (129.6, 138.5), 'c14': (138.5, 147.5), 'c15': (147.5, 156.0), 'c16': (156.0, 165.0), 'c17': (165.0, 175.5),
      'c18': (175.5, 186.1), 'c19': (186.1, 197.0), 'c20': (197.0, 207.8), 'c21': (207.8, 218.2), 'c22': (218.2, 228.0), 'c23': (228.0, 237.8),
      'c24': (237.8, 247.3), 'c25': (247.3, 257.1), 'c26': (257.1, 270.0), 'c27': (270.0, 281.9), 'c28': (281.9, 293.6), 'c29': (293.6, 304.7),
      'c30': (304.7, 315.4), 'c31': (315.4, 326.6), 'c32': (326.6, 337.2), 'c33': (337.2, 348.0), 'c34': (348.0, 358.3), 'c35': (358.3, 369.9),
      'c36': (369.9, 381.6), 'c37': (381.6, 392.7), 'c38': (392.7, 404.9), 'c39': (404.9, 416.7), 'c40': (416.7, 427.1), 'd3': (428.7, 445.7),
      'jai1': (445.7, 449.6), 'jai2': (449.6, 453.46)}
LEAD = {'jai1': 0.4, 'jai2': 0.2}; TAIL = {'d1': 1.2, 'd2': 1.2, 'd3': 1.4, 'jai1': 0.4, 'jai2': 0.9}
T = 460.96
w = wave.open(MIX); sr = w.getframerate(); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
if w.getnchannels() == 2: a = a.reshape(-1, 2).mean(1)
a = sosfilt(butter(4, [300, 3400], btype='band', fs=sr, output='sos'), a)
hop = sr // 100; n = len(a) // hop; E = np.sqrt((a[:n * hop].reshape(n, hop) ** 2).mean(1))
def quiet_runs(e, thr, lo, hi, minlen):
    runs, st = [], None
    for i in range(lo, hi):
        if e[i] < thr:
            if st is None: st = i
        else:
            if st is not None and i - st >= minlen: runs.append((st, i))
            st = None
    return runs
def split_at(e, s0, s1, frac, thr):
    lo, hi = int(s0 + (s1 - s0) * 0.2), int(s0 + (s1 - s0) * 0.85)
    runs = quiet_runs(e, thr, lo, hi, 6); target = s0 + (s1 - s0) * frac
    if not runs: return target, target
    a0, b0 = min(runs, key=lambda r: abs((r[0] + r[1]) / 2 - target) - 0.4 * (r[1] - r[0]))
    if abs((a0 + b0) / 2 - target) > (s1 - s0) * 0.22: return target, target
    return a0, b0
def words_of(line): return line.replace('।', ' ').replace('॥', ' ').replace(',', ' , ').replace('-', ' ').split()
def spread(ws, s0, s1):
    wt = [max(1.0, len(x)) for x in ws]; tot = sum(wt); out, t = [], s0
    for x, k in zip(ws, wt):
        d = (s1 - s0) * k / tot; out.append([x, round(t, 3), round(t + d, 3)]); t += d
    return out
def layout(vid, lines):
    t0, t1 = VT[vid]; at = t0 + LEAD.get(vid, 0.5); end = t1 - TAIL.get(vid, 0.8)
    lo, hi = int((at - 0.35) * 100), min(n, int((end + 0.35) * 100))
    seg = E[lo:hi]; p10, p90 = np.percentile(seg, 10), np.percentile(seg, 90)
    thr_on = p10 + 0.3 * (p90 - p10); thr_q = p10 + 0.18 * (p90 - p10)
    on = np.where(seg > thr_on)[0]
    s0, s1 = (lo + on[0], lo + on[-1] + 1) if len(on) else (int(at * 100), int(end * 100))
    toks = [words_of(l) for l in lines]; rows, spans = [], []
    if len(lines) == 2:
        c1 = sum(len(x) for x in toks[0] if x != ','); c2 = sum(len(x) for x in toks[1] if x != ',')
        g0, g1 = split_at(E, s0, s1, c1 / (c1 + c2), thr_q); spans = [(s0, g0), (g1, s1)]
    else: spans = [(s0, s1)]
    for (l0, l1), ws in zip(spans, toks):
        if ',' in ws:
            i = ws.index(','); L, Rr = ws[:i], ws[i + 1:]
            cl = sum(len(x) for x in L); cr = sum(len(x) for x in Rr)
            m0, m1 = split_at(E, l0, l1, cl / (cl + cr), thr_q)
            rows.append(spread(L, l0 / 100, m0 / 100)); rows.append(spread(Rr, m1 / 100, l1 / 100))
        else: rows.append(spread(ws, l0 / 100, l1 / 100))
    return rows, [[round(x / 100, 3), round(y / 100, 3)] for x, y in spans]
V = json.load(open(CH))
tl = {'verses': [], 'sections': [{'label': '॥ दोहा ॥', 't0': 8.0, 't1': 9.6}, {'label': '॥ चौपाई ॥', 't0': 32.7, 't1': 34.4}, {'label': '॥ दोहा ॥', 't0': 427.1, 't1': 428.7}],
      'events': [], 'intro': [0, 8.0], 'outro': [453.46, T], 'T': T}
allv = V + [{'id': 'jai1', 'kind': 'jai', 'lines': ['बोलो सियावर रामचंद्र की जय।']}, {'id': 'jai2', 'kind': 'jai', 'lines': ['पवनसुत हनुमान की जय।']}]
for v in allv:
    vid = v['id']; rows, lines = layout(vid, v['lines'])
    if vid in ('d1', 'd2'): label = 'दोहा ' + dev(int(vid[1:]))
    elif vid == 'd3': label = 'दोहा'
    elif vid.startswith('jai'): label = 'जयकारा'
    else: label = 'चौपाई ' + dev(int(vid[1:]))
    tl['verses'].append({'id': vid, 'kind': v.get('kind', 'jai'), 'label': label, 'theme': v.get('theme', ''), 'rows': rows, 'lines': lines,
                         'en': v.get('en', ''), 't0': VT[vid][0], 't1': VT[vid][1], 'big': vid.startswith('jai')})
json.dump(tl, open(OUT, 'w'), ensure_ascii=False)
print('verses', len(tl['verses']), 'T', T, 'sample', tl['verses'][2]['lines'], tl['verses'][2]['rows'][0][:2])
