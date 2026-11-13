'''Handwritten-notes renderer for the OS one-shot video.
python osv/render.py PAGE_FROM PAGE_TO OUT.mp4      (renders pages [from, to) and the page turns after them)
python osv/render.py --stills t1,t2,...  PREFIX      (single frames for review)
python osv/render.py --pages DIR                     (final state of every notes page, for the PDF)'''
import json, math, os, re, subprocess, sys, time
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); B = f'{HERE}/build'
W, H, FPS = 1920, 1080, 30
TL = json.load(open(f'{B}/tl.json')); S = json.load(open(f'{HERE}/os_script.json'))
CHAPS = S['chapters']
INK = {'blue': (22, 50, 168), 'black': (30, 30, 36), 'red': (204, 36, 40), 'green': (16, 118, 66), 'grey': (120, 120, 128)}
HLC = {'yellow': (255, 232, 64), 'pink': (255, 170, 200), 'green': (150, 240, 170)}
FF = {'body': 'Kalam-Regular.ttf', 'bold': 'Kalam-Bold.ttf', 'light': 'Kalam-Light.ttf', 'cav': 'Caveat.ttf', 'anton': 'Anton.ttf',
      'sg': 'SpaceGrotesk.ttf', 'inter': 'Inter.ttf', 'mono': 'JetBrainsMono.ttf'}
_fc = {}
def font(kind, size):
    k = (kind, size)
    if k not in _fc:
        f = ImageFont.truetype(f'{HERE}/fonts/{FF[kind]}', size)
        if kind in ('sg', 'inter', 'mono', 'cav'):
            try: f.set_variation_by_axes([700 if kind != 'inter' else 600])
            except Exception: pass
        _fc[k] = f
    return _fc[k]
def ease(k): k = min(1, max(0, k)); return 1 - (1 - k) ** 3
def eio(k): k = min(1, max(0, k)); return 4 * k * k * k if k < .5 else 1 - (-2 * k + 2) ** 3 / 2

# ---------------------------------------------------------------- paper
def make_paper():
    rng = np.random.default_rng(7)
    base = np.ones((H, W, 3), np.float32) * np.array([251, 248, 239], np.float32)
    low = np.array(Image.fromarray((rng.random((27, 48)) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC), np.float32) / 255 - .5
    base += low[..., None] * 6 + (rng.random((H, W, 1)) - .5) * 5
    im = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)); d = ImageDraw.Draw(im)
    for k in range(15): y = 232 + 54 * k; d.line([(0, y), (W, y)], fill=(176, 200, 232), width=2)
    d.line([(150, 0), (150, H)], fill=(232, 150, 150), width=2); d.line([(156, 0), (156, H)], fill=(238, 175, 175), width=1)
    # binder edge shadow on the left
    a = np.array(im, np.float32); g = np.clip(1 - np.exp(-np.arange(W) / 26), .78, 1)[None, :, None]; a *= g
    return Image.fromarray(a.astype(np.uint8))
PAPER = make_paper()
def page_base(pg):
    im = PAPER.copy(); d = ImageDraw.Draw(im)
    ch = pg['ch']; ct = CHAPS[ch - 1][1] if ch else pg['title']
    d.text((180, 1046), f'Operating System  ·  {"Ch " + str(ch) + ": " if ch else ""}{ct}', font=font('cav', 32), fill=(120, 120, 130), anchor='ls')
    d.text((1880, 1046), '@TECHVIBE24', font=font('cav', 34), fill=(22, 50, 168), anchor='rs')
    n = sum(1 for p in TL['pages'][:pg['i'] + 1] if p['kind'] == 'page')
    d.text((1650, 1046), f'p. {n}', font=font('cav', 32), fill=(120, 120, 130), anchor='rs')
    return np.array(im)

# ---------------------------------------------------------------- markup text
def parse(s):
    out, i, cur = [], 0, ''
    while i < len(s):
        if s[i] == '[' and i + 2 < len(s) and s[i + 1] in 'rgkhp' and s[i + 2] == ':':
            if cur: out.append((cur, None)); cur = ''
            j, depth = i + 3, 1
            while j < len(s) and depth:
                if s[j] == '[': depth += 1
                elif s[j] == ']': depth -= 1
                j += 1
            out.append((s[i + 3:j - 1], s[i + 1])); i = j
        else: cur += s[i]; i += 1
    if cur: out.append((cur, None))
    return out
_tc = {}
def text_layer(e):
    key = (e['s'], e['size'], e['font'], e['color'])
    if key in _tc: return _tc[key]
    f = font(e['font'], e['size']); spans = parse(e['s']); x = 0; parts = []; hls = []
    for txt, m in spans:
        col = INK[{'r': 'red', 'g': 'green', 'k': 'black'}.get(m, e['color'])]
        w = f.getlength(txt); parts.append((x, txt, col))
        if m in ('h', 'p'): hls.append((x - 4, x + w + 4, 'yellow' if m == 'h' else 'pink'))
        x += w
    wid = int(x) + 16; asc = int(e['size'] * 1.15); hgt = int(e['size'] * 1.75)
    im = Image.new('RGBA', (wid, hgt), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for px, txt, col in parts: d.text((px + 6, asc), txt, font=f, fill=col + (255,), anchor='ls')
    a = np.array(im); a[..., 3] = (a[..., 3].astype(np.float32) * .94).astype(np.uint8)   # ink is never perfectly opaque
    r = (a, asc, hls); _tc[key] = r; return r
def blend(base, layer, x, y, cut=None):
    '''alpha-blend RGBA numpy layer onto base at (x,y); cut = visible width from the left (soft edge)'''
    h, w = layer.shape[:2]; x0, y0 = max(0, x), max(0, y); x1, y1 = min(W, x + w), min(H, y + h)
    if x1 <= x0 or y1 <= y0: return
    L = layer[y0 - y:y1 - y, x0 - x:x1 - x]; a = L[..., 3:4].astype(np.float32) / 255
    if cut is not None:
        cols = np.arange(x0 - x, x1 - x, dtype=np.float32); m = np.clip((cut - cols) / 10 + 1, 0, 1)[None, :, None]; a = a * m
    reg = base[y0:y1, x0:x1].astype(np.float32); base[y0:y1, x0:x1] = (reg * (1 - a) + L[..., :3] * a).astype(np.uint8)
def highlighter(base, x0, x1, y0, y1, color, frac=1.0):
    x1 = x0 + (x1 - x0) * frac; xa, xb, ya, yb = int(max(0, x0)), int(min(W, x1)), int(max(0, y0)), int(min(H, y1))
    if xb <= xa: return
    c = np.array(HLC[color], np.float32) / 255; reg = base[ya:yb, xa:xb].astype(np.float32)
    k = .85
    base[ya:yb, xa:xb] = (reg * (1 - k + k * c)).astype(np.uint8)

# ---------------------------------------------------------------- hand-drawn strokes
def jitter(pts, seed, amp=1.1):
    out = []; n = len(pts)
    for i, (x, y) in enumerate(pts):
        u = i / max(1, n - 1)
        out.append((x + amp * math.sin(u * 7.3 + seed) + .6 * math.sin(u * 23 + seed * 2), y + amp * math.cos(u * 6.1 + seed * 1.3) + .6 * math.sin(u * 19 + seed)))
    return out
def densify(pts, step=5):
    out = [pts[0]]
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        d = math.hypot(x2 - x1, y2 - y1); n = max(1, int(d / step))
        out += [(x1 + (x2 - x1) * k / n, y1 + (y2 - y1) * k / n) for k in range(1, n + 1)]
    return out
def plen(pts): return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:]))
def cut_path(pts, frac):
    if frac >= 1: return pts, pts[-1]
    total = plen(pts) * frac; acc = 0; out = [pts[0]]
    for a, b in zip(pts, pts[1:]):
        d = math.hypot(b[0] - a[0], b[1] - a[1])
        if acc + d >= total:
            k = (total - acc) / max(d, 1e-6); p = (a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k); out.append(p); return out, p
        acc += d; out.append(b)
    return out, out[-1]
def draw_strokes(base, strokes, color, w=4):
    '''strokes: list of point lists; drawn anti-aliased by supersampling the bounding box'''
    pts = [p for s in strokes for p in s if len(s) > 1]
    if not pts: return
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]; pad = w + 4
    x0, y0, x1, y1 = int(min(xs)) - pad, int(min(ys)) - pad, int(max(xs)) + pad, int(max(ys)) + pad
    x0, y0, x1, y1 = max(0, x0), max(0, y0), min(W, x1), min(H, y1)
    if x1 <= x0 or y1 <= y0: return
    s = 2; im = Image.new('L', ((x1 - x0) * s, (y1 - y0) * s), 0); d = ImageDraw.Draw(im)
    for st in strokes:
        if len(st) > 1: d.line([((x - x0) * s, (y - y0) * s) for x, y in st], fill=235, width=w * s, joint='curve')
        for x, y in (st[0], st[-1]): d.ellipse([(x - x0) * s - w, (y - y0) * s - w, (x - x0) * s + w, (y - y0) * s + w], fill=235)
    a = np.array(im.resize((x1 - x0, y1 - y0), Image.BOX), np.float32)[..., None] / 255
    reg = base[y0:y1, x0:x1].astype(np.float32); base[y0:y1, x0:x1] = (reg * (1 - a) + np.array(INK[color], np.float32) * a).astype(np.uint8)

_geo = {}
def geometry(e, seed):
    '''list of strokes (point lists) for a shape element, in drawing order'''
    key = id(e)
    if key in _geo: return _geo[key]
    t = e['t']; st = []
    if t == 'rect':
        x, y, w, h = e['x'], e['y'], e['w'], e['h']; o = 3
        st = [jitter(densify([(x - o, y), (x + w + o, y + 1)]), seed), jitter(densify([(x + w, y - o), (x + w - 1, y + h + o)]), seed + 1),
              jitter(densify([(x + w + o, y + h), (x - o, y + h - 1)]), seed + 2), jitter(densify([(x, y + h + o), (x + 1, y - o)]), seed + 3)]
    elif t == 'ellipse':
        cx, cy, rx, ry = e['x'] + e['w'] / 2, e['y'] + e['h'] / 2, e['w'] / 2, e['h'] / 2; a0 = -2.2
        n = int(max(40, (rx + ry) * 1.2))
        st = [jitter([(cx + rx * (1 + .012 * math.sin(k * .3)) * math.cos(a0 + 6.6 * k / n), cy + ry * math.sin(a0 + 6.6 * k / n)) for k in range(n + 1)], seed, .8)]
    elif t == 'arrow':
        (x1, y1), (x2, y2) = e['p1'], e['p2']; c = e.get('curve', 0)
        if c:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2; L_ = math.hypot(x2 - x1, y2 - y1) or 1; nx, ny = -(y2 - y1) / L_, (x2 - x1) / L_
            cx, cy = mx + nx * c, my + ny * c; n = 40
            line = [((1 - u) ** 2 * x1 + 2 * (1 - u) * u * cx + u * u * x2, (1 - u) ** 2 * y1 + 2 * (1 - u) * u * cy + u * u * y2) for u in [k / n for k in range(n + 1)]]
        else: line = densify([(x1, y1), (x2, y2)])
        line = jitter(line, seed, .7); st = [line]
        def head(pa, pb):
            ang = math.atan2(pb[1] - pa[1], pb[0] - pa[0]); L2 = 18
            return [[(pb[0] - L2 * math.cos(ang - .45), pb[1] - L2 * math.sin(ang - .45)), pb], [pb, (pb[0] - L2 * math.cos(ang + .45), pb[1] - L2 * math.sin(ang + .45))]]
        if e.get('head', True): st += head(line[-4], line[-1])
        if e.get('both'): st += head(line[3], line[0])
    elif t == 'line': st = [jitter(densify([tuple(p) for p in e['pts']]), seed, .6)]
    _geo[key] = st; return st

def label_els(e):
    '''text sub-elements for labels of shapes'''
    out = []
    lab = e.get('label')
    if not lab: return out
    f = font('body', e.get('size', 30)); lines = lab.split('\n')
    if e['t'] in ('rect', 'ellipse'):
        cx, cy = e['x'] + e['w'] / 2, e['y'] + e['h'] / 2; lh = e.get('size', 30) * 1.15
        for k, ln in enumerate(lines):
            y = cy + (k - (len(lines) - 1) / 2) * lh + e.get('size', 30) * .36
            out.append(dict(t='text', x=int(cx - f.getlength(ln) / 2 - 6), y=int(y), s=ln, size=e.get('size', 30), font='body', color=e.get('lc', 'black')))
    elif e['t'] == 'arrow':
        (x1, y1), (x2, y2) = e['p1'], e['p2']; mx, my = (x1 + x2) / 2 + e.get('lx', 0), (y1 + y2) / 2 + e.get('ly', -14)
        if e.get('curve'):
            L_ = math.hypot(x2 - x1, y2 - y1) or 1; mx += -(y2 - y1) / L_ * e['curve'] * .5; my += (x2 - x1) / L_ * e['curve'] * .5
        out.append(dict(t='text', x=int(mx - f.getlength(lab) / 2 - 6), y=int(my), s=lab, size=e.get('size', 28), font='body', color='green'))
    return out

def table_parts(e):
    x0, y0, cw, rh, rows = e['x'], e['y'], e['cw'], e['rh'], e['rows']; nr, nc = len(rows), len(cw)
    xs = [x0 + sum(cw[:k]) for k in range(nc + 1)]; ys = [y0 + rh * k for k in range(nr + 1)]
    grid = [densify([(xs[0], y), (xs[-1], y)]) for y in ys] + [densify([(x, ys[0]), (x, ys[-1])]) for x in xs]
    cells = []
    order = [(r, c) for c in range(nc) for r in range(nr)] if e.get('order') == 'col' else [(r, c) for r in range(nr) for c in range(nc)]
    for r, c in order:
        s = rows[r][c] if c < len(rows[r]) else ''
        if not s: continue
        col = e['colors'].get(f'{r},{c}', 'black' if (e.get('hdr') and r == 0) else e['color'])
        fnt = 'bold' if (e.get('hdr') and r == 0) else 'body'
        f = font(fnt, e['size']); cx = (xs[c] + xs[c + 1]) / 2; cy = (ys[r] + ys[r + 1]) / 2
        cells.append(dict(t='text', x=int(cx - f.getlength(s) / 2 - 6), y=int(cy + e['size'] * .36), s=s, size=e['size'], font=fnt, color=col))
    return grid, cells

def gantt_parts(e):
    x0, y0, u, h = e['x'], e['y'], e['u'], e['h']; parts = []; f = font('body', e['size'])
    for k, (n, s, t) in enumerate(e['segs']):
        xa, xb = x0 + s * u, x0 + t * u
        parts.append(('stroke', [densify([(xa, y0), (xb, y0)]), densify([(xb, y0), (xb, y0 + h)]), densify([(xb, y0 + h), (xa, y0 + h)])] + ([densify([(xa, y0 + h), (xa, y0)])] if k == 0 else [])))
        parts.append(('text', dict(t='text', x=int((xa + xb) / 2 - f.getlength(n) / 2 - 6), y=int(y0 + h / 2 + e['size'] * .36), s=n, size=e['size'], font='body', color=e['color'])))
        if k == 0: parts.append(('text', dict(t='text', x=int(xa - 12), y=int(y0 + h + 36), s=str(s), size=26, font='body', color='black')))
        parts.append(('text', dict(t='text', x=int(xb - 12 if t < 10 else xb - 18), y=int(y0 + h + 36), s=str(t), size=26, font='body', color='black')))
    return parts

# ---------------------------------------------------------------- element painting (progress 0..1); returns pen position
def paint(base, e, prog, seed):
    t = e['t']
    if t == 'text':
        a, asc, hls = text_layer(e); x, y = e['x'] - 6, e['y'] - asc; w = a.shape[1]
        tw_ = prog * (1.25 if hls else 1)
        cutw = min(1, tw_) * (w - 10) + 4
        if hls and tw_ > 1:
            k = min(1, (tw_ - 1) / .25)
            for xa, xb, c in hls: highlighter(base, x + 6 + xa, x + 6 + xb, e['y'] - e['size'] * .78, e['y'] + e['size'] * .2, c, k)
        blend(base, a, x, y, None if prog >= 1 else cutw)
        if e.get('title') and prog > .5:
            k = min(1, (prog - .5) / .5); x1 = e['x'] + (w - 20) * k
            draw_strokes(base, [jitter(densify([(e['x'], e['y'] + 16), (x1, e['y'] + 18)]), seed, 1.6)], 'red', 4)
        if prog >= 1 or (hls and tw_ >= 1): return None
        return (x + cutw, e['y'] - e['size'] * .25 + math.sin(prog * 60) * e['size'] * .12)
    if t in ('rect', 'ellipse', 'arrow', 'line'):
        strokes = geometry(e, seed); labs = label_els(e); L_ = [plen(s) for s in strokes]; tot = sum(L_) or 1
        tl_ = sum(len(l['s']) for l in labs) / 34 * 1500 if labs else 0; fill = e.get('fill')
        sw = tot / (tot + tl_ + (300 if fill else 0)); fw = (300 if fill else 0) / (tot + tl_ + (300 if fill else 0))
        ps = min(1, prog / sw) if sw > 0 else 1; acc = 0; drawn = []; pen = None
        if fill and prog > sw:
            k = min(1, (prog - sw) / fw) if fw else 1
            highlighter(base, e['x'] + 3, e['x'] + e['w'] - 3, e['y'] + 3, e['y'] + e['h'] - 3, fill, k)
        for s, l in zip(strokes, L_):
            need = ps * tot - acc
            if need <= 0: break
            if need >= l: drawn.append(s)
            else: part, pen = cut_path(s, need / l); drawn.append(part); break
            acc += l
        draw_strokes(base, drawn, e['color'], e.get('w', 4) if t == 'line' else 3)
        if labs and prog > sw + fw:
            k = (prog - sw - fw) / max(1e-6, 1 - sw - fw); n = len(labs)
            for i, l in enumerate(labs):
                pp = min(1, max(0, k * n - i))
                if pp > 0:
                    r = paint(base, l, pp, seed + i)
                    if r: pen = r
        if prog >= 1: return None
        return pen if pen else (strokes[-1][-1] if strokes and strokes[-1] else None)
    if t == 'table':
        grid, cells = table_parts(e); gl = sum(plen(g) for g in grid); ct = sum(len(c['s']) / 42 + .03 for c in cells)
        gw = (gl / 3600) / (gl / 3600 + ct); pen = None
        if prog < gw:
            k = prog / gw; need = k * gl; drawn = []
            for g in grid:
                l = plen(g)
                if need >= l: drawn.append(g); need -= l
                else: part, pen = cut_path(g, need / l); drawn.append(part); break
            draw_strokes(base, [jitter(g, 3, .5) for g in drawn], e['color'], 3); return pen
        draw_strokes(base, [jitter(g, 3, .5) for g in grid], e['color'], 3)
        k = (prog - gw) / (1 - gw); tot = ct; acc = 0
        for c in cells:
            d = (len(c['s']) / 42 + .03) / tot
            pp = min(1, max(0, (k - acc) / d)); acc += d
            if pp <= 0: break
            r = paint(base, c, pp, 1)
            if r: pen = r
        return None if prog >= 1 else pen
    if t == 'gantt':
        parts = gantt_parts(e); wts = [(plen([p for s in v for p in s]) / 1800 + .02) if k == 'stroke' else (.1 + len(v['s']) / 40) for k, v in parts]
        tot = sum(wts); acc = 0; pen = None
        for (k, v), wt in zip(parts, wts):
            pp = min(1, max(0, (prog * tot - acc) / wt)); acc += wt
            if pp <= 0: break
            if k == 'stroke':
                L_ = [plen(s) for s in v]; tl_ = sum(L_); need = pp * tl_; drawn = []
                for s, l in zip(v, L_):
                    if need >= l: drawn.append(s); need -= l
                    else: part, pen = cut_path(s, need / l); drawn.append(part); break
                draw_strokes(base, [jitter(s, 5, .5) for s in drawn], e['color'], 3)
            else:
                r = paint(base, v, pp, 2)
                if r: pen = r
        return None if prog >= 1 else pen
    if t == 'stamp':
        k = ease(prog); sc = 1.5 - .5 * k; f = font('bold', e['size'])
        tw_ = int(f.getlength(e['text'])) + 40; th = int(e['size'] * 1.6)
        im = Image.new('RGBA', (tw_ + 20, th + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        col = INK[e['color']]
        d.rounded_rectangle([10, 10, tw_ + 10, th + 10], radius=12, outline=col + (230,), width=4)
        d.text((tw_ / 2 + 10, th / 2 + 10 + e['size'] * .05), e['text'], font=f, fill=col + (235,), anchor='mm')
        im = im.rotate(e.get('rot', -8), expand=True, resample=Image.BICUBIC)
        im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.BICUBIC)
        a = np.array(im); a[..., 3] = (a[..., 3] * min(1, prog * 3) * .9).astype(np.uint8)
        blend(base, a, int(e['x'] - im.width / 2 + tw_ / 2), int(e['y'] - im.height / 2)); return None
    if t == 'hl':
        highlighter(base, e['x'], e['x'] + e['w'], e['y'], e['y'] + e['h'], e['color'], ease(prog)); return (e['x'] + e['w'] * ease(prog), e['y'] + e['h'] / 2) if prog < 1 else None
    return None

# ---------------------------------------------------------------- pen sprite
def make_pen():
    s = 4; im = Image.new('RGBA', (110 * s, 520 * s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    cx = 55 * s
    d.polygon([(cx, 0), (cx - 9 * s, 34 * s), (cx + 9 * s, 34 * s)], fill=(190, 192, 200, 255))          # metal tip
    d.polygon([(cx, 0), (cx - 3 * s, 10 * s), (cx + 3 * s, 10 * s)], fill=(30, 40, 90, 255))
    d.rounded_rectangle([cx - 13 * s, 32 * s, cx + 13 * s, 120 * s], radius=6 * s, fill=(28, 30, 38, 255))   # grip
    for k in range(6): d.line([(cx - 13 * s, (44 + 12 * k) * s), (cx + 13 * s, (44 + 12 * k) * s)], fill=(55, 58, 70, 255), width=2 * s)
    d.rounded_rectangle([cx - 15 * s, 118 * s, cx + 15 * s, 500 * s], radius=12 * s, fill=(26, 70, 190, 255))  # barrel
    d.rounded_rectangle([cx - 8 * s, 126 * s, cx - 2 * s, 480 * s], radius=3 * s, fill=(110, 150, 240, 150))  # shine
    d.rounded_rectangle([cx + 10 * s, 380 * s, cx + 18 * s, 495 * s], radius=3 * s, fill=(200, 205, 215, 255))  # clip
    im = im.resize((110, 520), Image.LANCZOS).rotate(-38, expand=True, resample=Image.BICUBIC)
    a = np.array(im); ys, xs = np.where(a[..., 3] > 0)
    # tip = lowest-left point after rotation
    i = np.argmax(ys - xs * .0); tip = (xs[i], ys[i])
    sh = Image.fromarray(a).split()[3].filter(ImageFilter.GaussianBlur(9)); sha = np.zeros_like(a); sha[..., 3] = (np.array(sh) * .32).astype(np.uint8)
    return a, sha, tip
PEN, PEN_SH, PEN_TIP = make_pen()
def draw_pen(img, pos, alpha=1.0):
    if pos is None or alpha <= 0: return
    x, y = int(pos[0]), int(pos[1])
    sh = PEN_SH.copy(); sh[..., 3] = (sh[..., 3] * alpha).astype(np.uint8); blend(img, sh, x - PEN_TIP[0] + 26, y - PEN_TIP[1] + 30)
    p = PEN.copy(); p[..., 3] = (p[..., 3] * alpha).astype(np.uint8); blend(img, p, x - PEN_TIP[0], y - PEN_TIP[1])

# ---------------------------------------------------------------- full-screen cards
def card_bg():
    a = np.zeros((H, W, 3), np.float32); yy, xx = np.mgrid[0:H, 0:W]
    a[:] = np.array([12, 16, 26], np.float32)
    g = np.exp(-(((xx - 1350) / 900) ** 2 + ((yy - 300) / 650) ** 2)); a += g[..., None] * np.array([20, 60, 110], np.float32)
    g2 = np.exp(-(((xx - 300) / 700) ** 2 + ((yy - 950) / 500) ** 2)); a += g2[..., None] * np.array([60, 30, 100], np.float32)
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)); d = ImageDraw.Draw(im)
    for x in range(0, W, 60): d.line([(x, 0), (x, H)], fill=(255, 255, 255, 8))
    a = np.array(im, np.float32)
    for x in range(0, W, 60): a[:, x] = a[:, x] * .94 + 255 * .06 * .3
    for y in range(0, H, 60): a[y, :] = a[y, :] * .94 + 255 * .06 * .3
    return a.astype(np.uint8)
CARD = card_bg()
def star(d, cx, cy, r, fill):
    pts = [(cx + (r if k % 2 == 0 else r * .45) * math.cos(-math.pi / 2 + k * math.pi / 5), cy + (r if k % 2 == 0 else r * .45) * math.sin(-math.pi / 2 + k * math.pi / 5)) for k in range(10)]
    d.polygon(pts, fill=fill)
_chf = {}
def chapter_frame(pg, lt):
    if lt > 1.8 and pg['i'] in _chf: return _chf[pg['i']]
    r = _chapter_frame(pg, lt)
    if lt > 1.8: _chf[pg['i']] = r
    return r
def _chapter_frame(pg, lt):
    im = Image.fromarray(CARD.copy()).convert('RGBA'); ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    k1, k2, k3 = ease(lt / .5), ease((lt - .25) / .5), ease((lt - .5) / .6)
    a = lambda k: int(255 * k)
    d.text((160 - 60 * (1 - k1), 300), f'CHAPTER {pg["num"]:02d}', font=font('mono', 40), fill=(46, 230, 255, a(k1)), anchor='ls')
    d.text((160 - 80 * (1 - k2), 450), pg['title'].upper(), font=font('anton', 130), fill=(244, 247, 251, a(k2)), anchor='ls')
    d.rounded_rectangle([160, 490, 160 + int(520 * k2), 498], radius=4, fill=(46, 230, 255, a(k2)))
    for i, s in enumerate(pg['subs']):
        kk = ease((lt - .6 - i * .12) / .4)
        d.text((190 + 40 * (1 - kk), 590 + i * 62), f'›  {s}', font=font('inter', 40), fill=(205, 216, 230, a(kk)), anchor='ls')
    kk = ease((lt - 1.0) / .5)
    d.text((1180, 590), 'EXAM WEIGHTAGE', font=font('mono', 30), fill=(46, 230, 255, a(kk)), anchor='ls')
    for i in range(5): star(d, 1205 + i * 70, 650, 26, (255, 214, 10, a(kk)) if i < pg['stars'] else (255, 255, 255, a(kk) // 5))
    for i in range(10):   # chapter progress
        x = 160 + i * 160; on = i < pg['num']
        d.rounded_rectangle([x, 960, x + 140, 968], radius=4, fill=(46, 230, 255, 230) if on else (255, 255, 255, 50))
    d.text((1760, 1000), '@TECHVIBE24', font=font('sg', 34), fill=(255, 255, 255, 200), anchor='rs')
    im = Image.alpha_composite(im, ov); return np.array(im.convert('RGB'))
_cov = {}
def cover_parts(outro):
    if outro in _cov: return _cov[outro]
    a = np.zeros((H, W, 3), np.float32); yy, xx = np.mgrid[0:H, 0:W]
    a[:] = np.array([18, 30, 70], np.float32); a += (np.exp(-(((xx - 960) / 1000) ** 2 + ((yy - 500) / 600) ** 2))[..., None] * np.array([30, 50, 90]))
    rng = np.random.default_rng(3); a += (rng.random((H, W, 1)) - .5) * 10
    bg = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert('RGBA'); d = ImageDraw.Draw(bg)
    d.rectangle([0, 0, 70, H], fill=(10, 16, 40, 255))
    lab = Image.new('RGBA', (1180, 640), (0, 0, 0, 0)); ld = ImageDraw.Draw(lab)
    ld.rounded_rectangle([0, 0, 1179, 639], radius=36, fill=(251, 248, 239, 255))
    for i in range(6): ld.line([(40, 250 + 62 * i), (1140, 250 + 62 * i)], fill=(176, 200, 232, 255), width=2)
    if not outro:
        ld.text((590, 150), 'OPERATING SYSTEM', font=font('bold', 112), fill=INK['black'] + (255,), anchor='ms')
        ld.text((590, 236), 'Complete notes  ·  one shot', font=font('body', 54), fill=INK['blue'] + (255,), anchor='ms')
        ld.text((590, 360), 'B.Tech CSE  ·  All universities  +  GATE', font=font('body', 48), fill=INK['red'] + (255,), anchor='ms')
        ld.text((590, 470), 'Simple explanation + handwritten notes', font=font('body', 44), fill=INK['green'] + (255,), anchor='ms')
        ld.text((590, 590), 'Name: ____________     @TECHVIBE24', font=font('cav', 50), fill=INK['blue'] + (255,), anchor='ms')
    else:
        ld.text((590, 170), 'All the best!', font=font('bold', 120), fill=INK['black'] + (255,), anchor='ms')
        ld.text((590, 300), 'Share with friends who have the exam', font=font('body', 50), fill=INK['blue'] + (255,), anchor='ms')
        ld.text((590, 420), 'Comment: which subject next?', font=font('body', 50), fill=INK['red'] + (255,), anchor='ms')
        ld.text((590, 560), 'Subscribe  @TECHVIBE24', font=font('bold', 64), fill=INK['blue'] + (255,), anchor='ms')
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(sh); x0, y0 = (W - 1180) // 2 + 30, (H - 640) // 2 + 10
    sd.rounded_rectangle([x0 + 14, y0 + 20, x0 + 1180 + 14, y0 + 640 + 20], radius=36, fill=(0, 0, 0, 120)); sh = sh.filter(ImageFilter.GaussianBlur(16))
    bg = Image.alpha_composite(bg, sh)
    st = Image.new('RGBA', (360, 140), (0, 0, 0, 0)); sdd = ImageDraw.Draw(st); col = (220, 40, 50, 230)
    sdd.rounded_rectangle([6, 6, 354, 134], radius=16, outline=col, width=7); sdd.text((180, 72), 'ONE SHOT', font=font('bold', 64), fill=col, anchor='mm')
    st = st.rotate(12, expand=True, resample=Image.BICUBIC)
    _cov[outro] = (bg, lab, st); return _cov[outro]
_covf = {}
def cover_frame(pg, lt, outro=False):
    if lt > 1.4 and outro in _covf: return _covf[outro]
    bg, lab, st = cover_parts(outro); im = bg.copy()
    k = ease(lt / .8); sc = 1.04 - .04 * k
    l2 = lab if sc == 1 else lab.resize((int(1180 * sc), int(640 * sc)), Image.BICUBIC)
    im.alpha_composite(l2, ((W - l2.width) // 2 + 30, (H - l2.height) // 2 + 10))
    if not outro and lt > .9:
        kk = ease((lt - .9) / .3); s2 = 1.6 - .6 * kk; s3 = st.resize((int(st.width * s2), int(st.height * s2)), Image.BICUBIC)
        a = np.array(s3); a[..., 3] = (a[..., 3] * min(1, (lt - .9) * 4)).astype(np.uint8); s3 = Image.fromarray(a)
        im.alpha_composite(s3, (1450 - s3.width // 2, 230 - s3.height // 2))
    r = np.array(im.convert('RGB'))
    if lt > 1.4: _covf[outro] = r
    return r

# ---------------------------------------------------------------- page state machine
class PageState:
    def __init__(self, pg):
        self.pg = pg; self.base = page_base(pg); self.done = 0
        self.els = [(e, (pg['i'] * 131 + k) % 997) for b in pg['beats'] for k, e in enumerate(b['els'])]
    def frame(self, t):
        while self.done < len(self.els) and t >= self.els[self.done][0]['w1']:
            e, sd = self.els[self.done]; paint(self.base, e, 1.0, sd); self.done += 1
        img = self.base.copy(); pen = None
        if self.done < len(self.els):
            e, sd = self.els[self.done]
            if t >= e['w0']: pen = paint(img, e, (t - e['w0']) / max(1e-3, e['w1'] - e['w0']), sd)
        return img, pen
    def final(self):
        for e, sd in self.els[self.done:]: paint(self.base, e, 1.0, sd)
        self.done = len(self.els); return self.base
def pen_logic(state, t, pen):
    '''pen visible while writing, glides between elements, fades when idle'''
    els = state.els
    if pen is not None: state.last_pen = pen; state.last_t = t; return pen, 1.0
    nxt = next((e for e, _ in els if e['w0'] > t), None); lp = getattr(state, 'last_pen', None); lt = getattr(state, 'last_t', -9)
    if nxt and nxt['w0'] - t < .3 and lp is not None and nxt['t'] not in ('stamp',):
        k = eio(1 - (nxt['w0'] - t) / .3); tgt = (nxt.get('x', nxt.get('p1', [0, 0])[0] if nxt['t'] == 'arrow' else 0), nxt.get('y', 0))
        if nxt['t'] == 'arrow': tgt = tuple(nxt['p1'])
        elif nxt['t'] == 'line': tgt = tuple(nxt['pts'][0])
        elif nxt['t'] == 'table': tgt = (nxt['x'], nxt['y'])
        elif nxt['t'] == 'gantt': tgt = (nxt['x'], nxt['y'])
        return (lp[0] + (tgt[0] - lp[0]) * k, lp[1] + (tgt[1] - lp[1]) * k - 30 * math.sin(k * math.pi)), 1.0
    if lp is not None and t - lt < .7: return (lp[0] + 30 * ease((t - lt) / .7), lp[1] + 40 * ease((t - lt) / .7)), 1 - ease((t - lt - .3) / .4)
    return None, 0

def compose_turn(old, new, k):
    '''new page slides in from the right over the old one'''
    k = eio(k); off = int(W * (1 - k)); img = old.copy()
    if off < W:
        img[:, :W - off] = (img[:, :W - off].astype(np.float32) * (1 - .25 * k)).astype(np.uint8) if off > 0 else img[:, :W - off]
        img[:, off:] = new[:, :W - off]
        sw = 40; xs = np.arange(sw)
        if off > sw:
            shade = (1 - .45 * (1 - xs / sw) ** 2)[None, :, None]; img[:, off - sw:off] = (img[:, off - sw:off].astype(np.float32) * shade).astype(np.uint8)
    return img

def render_range(p0, p1, out, stills=None):
    pages = TL['pages']; T = TL['T']
    t_start = pages[p0]['t0']; t_end = pages[p1]['t0'] if p1 < len(pages) else T
    ff = None
    if out:
        ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                               '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p', '-r', str(FPS), out], stdin=subprocess.PIPE)
    states = {}; finals = {}
    def state(i):
        if i not in states: states[i] = PageState(pages[i])
        return states[i]
    def page_img(i, t):
        pg = pages[i]
        if pg['kind'] == 'chapter': return chapter_frame(pg, t - pg['t0']), None, 0
        if pg['kind'] in ('cover', 'outro'): return cover_frame(pg, t - pg['t0'], pg['kind'] == 'outro'), None, 0
        st = state(i); img, pen = st.frame(t); pp, pa = pen_logic(st, t, pen); return img, pp, pa
    def final_img(i):
        if i in finals: return finals[i]
        pg = pages[i]
        if pg['kind'] == 'chapter': r = chapter_frame(pg, 99)
        elif pg['kind'] in ('cover', 'outro'): r = cover_frame(pg, 99, pg['kind'] == 'outro')
        else: r = state(i).final().copy()
        finals[i] = r; return r
    def blank_img(i):
        pg = pages[i]
        if pg['kind'] == 'chapter': return chapter_frame(pg, 0)
        if pg['kind'] in ('cover', 'outro'): return cover_frame(pg, 0, pg['kind'] == 'outro')
        return page_base(pg)
    times = stills if stills else [f / FPS for f in range(int(round(t_start * FPS)), int(round(t_end * FPS)))]
    t0 = time.time(); prev_key = None; prev_bytes = None
    for n, t in enumerate(times):
        i = max(k for k, p in enumerate(pages) if p['t0'] <= t + 1e-6)
        pg = pages[i]
        if t >= pg['t1'] and i + 1 < len(pages):     # page turn
            img = compose_turn(final_img(i), blank_img(i + 1), (t - pg['t1']) / TL['TURN'])
        elif t >= pg['t1']:
            img = final_img(i)
            e = TL['T'] - t
            if e < 1.2: img = (img.astype(np.float32) * max(0, e / 1.2)).astype(np.uint8)
        else:
            img, pp, pa = page_img(i, t)
            if pp is not None: img = img.copy(); draw_pen(img, pp, pa)
        if stills:
            Image.fromarray(img).save(f'{out_prefix}_{t:07.2f}.jpg', quality=90)
        else:
            ff.stdin.write(img.tobytes())
        if not stills and n % 900 == 0: print(f'{out} {n}/{len(times)} {time.time() - t0:.0f}s', flush=True)
        for k in list(states):
            if k < i - 1: del states[k]
    if ff: ff.stdin.close(); ff.wait()
    print('done', out, len(times), 'frames', f'{time.time() - t0:.0f}s', flush=True)

if __name__ == '__main__':
    if sys.argv[1] == '--stills':
        ts = [float(x) for x in sys.argv[2].split(',')]; out_prefix = sys.argv[3]; render_range(0, len(TL['pages']), None, stills=ts)
    elif sys.argv[1] == '--pages':
        d = sys.argv[2]; os.makedirs(d, exist_ok=True)
        for pg in TL['pages']:
            if pg['kind'] == 'page': Image.fromarray(PageState(pg).final()).save(f'{d}/page_{pg["i"]:03d}.png')
            elif pg['kind'] == 'cover': Image.fromarray(cover_frame(pg, 99)).save(f'{d}/page_{pg["i"]:03d}.png')
        print('pages saved')
    else:
        render_range(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3])
