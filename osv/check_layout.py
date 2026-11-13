'''Find text that runs off the page or into diagrams.'''
import json, re
from PIL import ImageFont
S = json.load(open('os_script.json'))
F = {'body': ImageFont.truetype('fonts/Kalam-Regular.ttf', 40), 'bold': ImageFont.truetype('fonts/Kalam-Bold.ttf', 40)}
def plain(s):
    out, i = '', 0
    while i < len(s):
        if s[i] == '[' and i + 2 < len(s) and s[i + 1] in 'rgkhp' and s[i + 2] == ':': i += 3; continue
        out += s[i]; i += 1
    return out.replace(']]', ']') if False else out
def tb(e):
    f = ImageFont.truetype('fonts/Kalam-Regular.ttf' if e['font'] == 'body' else 'fonts/Kalam-Bold.ttf', e['size'])
    s = re.sub(r'\[([rgkhp]):', '', e['s']); s = s.replace(']', '') if '[' not in s else s   # approximate
    w = f.getlength(s); return (e['x'], e['y'] - e['size'] * .8, e['x'] + w, e['y'] + e['size'] * .25)
def sb(e):
    t = e['t']
    if t in ('rect', 'ellipse'): return (e['x'], e['y'], e['x'] + e['w'], e['y'] + e['h'])
    if t == 'table': return (e['x'], e['y'], e['x'] + sum(e['cw']), e['y'] + e['rh'] * len(e['rows']))
    if t == 'gantt': return (e['x'], e['y'], e['x'] + max(s[2] for s in e['segs']) * e['u'], e['y'] + e['h'] + 40)
    return None
def ov(a, b): return min(a[2], b[2]) - max(a[0], b[0]) > 4 and min(a[3], b[3]) - max(a[1], b[1]) > 4
for p in S['pages']:
    if p['kind'] != 'page': continue
    els = [e for b in p['beats'] for e in b['els']]
    texts = [(e, tb(e)) for e in els if e['t'] == 'text']; shapes = [(e, sb(e)) for e in els if sb(e)]
    for e, b in texts:
        if b[2] > 1885 or b[3] > 1015: print(f"OUT  {p['title'][:30]:30} {e['s'][:50]!r} right={b[2]:.0f} bottom={b[3]:.0f}")
        for e2, b2 in shapes:
            if ov(b, b2) and not (b2[0] <= b[0] and b[2] <= b2[2] and b2[1] <= b[1] and b[3] <= b2[3]):
                print(f"HIT  {p['title'][:30]:30} {e['s'][:50]!r} x {e2['t']}")
    for i, (e, b) in enumerate(texts):
        for e2, b2 in texts[i + 1:]:
            if ov(b, b2): print(f"TXT  {p['title'][:30]:30} {e['s'][:35]!r} / {e2['s'][:35]!r}")
