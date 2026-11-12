'''Make candidate paintings for every scene on AI Horde (free, anonymous), depth maps, and review sheets.
python tools/scenes.py [ids,comma] [variants]   e.g.  python tools/scenes.py "" AB'''
import json, os, sys, time, urllib.request, urllib.error
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.dirname(__file__))
from prompts import P, full
API = 'https://aihorde.net/api/v2'
H = {'apikey': '0000000000', 'Content-Type': 'application/json', 'Client-Agent': 'techvibe24-studio:1.0:anon', 'User-Agent': 'curl/8.5.0'}
MODELS = {'A': 'AlbedoBase XL (SDXL)', 'B': 'Juggernaut XL', 'C': 'AlbedoBase XL (SDXL)', 'D': 'Juggernaut XL'}
OUT = 'out'; os.makedirs(f'{OUT}/scenes', exist_ok=True); os.makedirs(f'{OUT}/depth', exist_ok=True); os.makedirs(f'{OUT}/sheets', exist_ok=True)
def log(*a): print(time.strftime('%H:%M:%S'), *a, flush=True)
def req(method, path, body=None):
    r = urllib.request.Request(API + path, data=json.dumps(body).encode() if body is not None else None, headers=H, method=method)
    return json.load(urllib.request.urlopen(r, timeout=60))
def submit(sid, v, k=0):
    seed = str(abs(hash((sid, v, k))) % 99991 + 7)
    body = {'prompt': full(sid), 'params': {'sampler_name': 'k_dpmpp_2m', 'karras': True, 'cfg_scale': 6, 'width': 768, 'height': 1344, 'steps': 30, 'n': 1, 'seed': seed},
            'models': [MODELS[v]], 'nsfw': False, 'censor_nsfw': True, 'r2': True}
    return req('POST', '/generate/async', body)['id']
def generate(ids, variants, budget_min=75):
    todo = [(s, v) for s in ids for v in variants if not os.path.exists(f'{OUT}/scenes/{s}_{v}.jpg')]
    live, tries, t_end = {}, {}, time.time() + budget_min * 60
    while (todo or live) and time.time() < t_end:
        while todo and len(live) < 24:
            s, v = todo[0]
            try:
                live[(s, v)] = submit(s, v, tries.get((s, v), 0)); todo.pop(0); log('submitted', s, v)
            except urllib.error.HTTPError as e:
                log('submit wait', s, v, e.code, e.read()[:120]); break
            time.sleep(1.1)
        time.sleep(15)
        for key, jid in list(live.items()):
            s, v = key
            try:
                c = req('GET', '/generate/check/' + jid)
                if c.get('done'):
                    g = req('GET', '/generate/status/' + jid)['generations'][0]
                    del live[key]
                    if g.get('censored'): raise ValueError('censored')
                    urllib.request.urlretrieve(g['img'], f'/tmp/{s}_{v}.webp')
                    Image.open(f'/tmp/{s}_{v}.webp').convert('RGB').save(f'{OUT}/scenes/{s}_{v}.jpg', quality=95)
                    log('done', s, v, g.get('worker_name'))
                elif c.get('faulted') or not c.get('is_possible', True):
                    del live[key]; raise ValueError('faulted')
            except Exception as e:
                gone = isinstance(e, ValueError) or (isinstance(e, urllib.error.HTTPError) and e.code == 404)
                if gone:
                    live.pop(key, None); tries[key] = tries.get(key, 0) + 1
                    if tries[key] < 4: todo.append(key)
                    log('retry', s, v, repr(e)[:80])
            time.sleep(0.6)
    log('generation finished; missing:', [k for k in todo] + list(live))
def depth_maps():
    import onnxruntime as ort
    mp = '/tmp/depth.onnx'
    if not os.path.exists(mp):
        urllib.request.urlretrieve('https://huggingface.co/onnx-community/depth-anything-v2-small/resolve/main/onnx/model.onnx', mp)
    sess = ort.InferenceSession(mp, providers=['CPUExecutionProvider']); iname = sess.get_inputs()[0].name
    M = np.array([0.485, 0.456, 0.406], np.float32); S = np.array([0.229, 0.224, 0.225], np.float32)
    for f in sorted(os.listdir(f'{OUT}/scenes')):
        out = f'{OUT}/depth/' + f.replace('.jpg', '.png')
        if os.path.exists(out): continue
        im = Image.open(f'{OUT}/scenes/' + f).convert('RGB'); W, Hh = im.size
        w, h = 518, int(round(518 * Hh / W / 14)) * 14
        x = (np.asarray(im.resize((w, h), Image.BICUBIC), np.float32) / 255 - M) / S
        d = sess.run(None, {iname: x.transpose(2, 0, 1)[None]})[0][0]
        d = np.clip((d - np.percentile(d, 1)) / (np.percentile(d, 99.5) - np.percentile(d, 1) + 1e-6), 0, 1)
        dm = Image.fromarray((d * 255).astype(np.uint8)).resize((W, Hh), Image.BICUBIC).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(4))
        dm.save(out)
    log('depth done')
def sheets(ids, variants):
    tw, th = 216, 378; per = 8; cols = len(variants) * 2
    for n in range(0, len(ids), per):
        chunk = ids[n:n + per]; rows = (len(chunk) + 1) // 2
        sheet = Image.new('RGB', (cols * tw, rows * (th + 26)), (20, 12, 8)); d = ImageDraw.Draw(sheet)
        for i, s in enumerate(chunk):
            for j, v in enumerate(variants):
                x, y = ((i % 2) * len(variants) + j) * tw, (i // 2) * (th + 26)
                p = f'{OUT}/scenes/{s}_{v}.jpg'
                if os.path.exists(p): sheet.paste(Image.open(p).convert('RGB').resize((tw, th)), (x, y + 26))
                d.text((x + 6, y + 6), f'{s} {v}', fill=(255, 220, 120))
        sheet.save(f'{OUT}/sheets/sheet_{n // per + 1:02d}.jpg', quality=82)
    log('sheets done')
if __name__ == '__main__':
    ids = [i for i in (sys.argv[1].split(',') if len(sys.argv) > 1 and sys.argv[1] else list(P))]
    variants = sys.argv[2] if len(sys.argv) > 2 else 'AB'
    generate(ids, variants)
    depth_maps()
    sheets(ids, variants)
