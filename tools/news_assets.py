'''Assets for the TechVibe24 news Short (runs on GitHub Actions, which has open internet):
voiceover per segment with word timings (edge-tts), photoreal backdrops (AI Horde), depth maps, review sheets.
python tools/news_assets.py news/script.json OUTDIR'''
import asyncio, json, os, sys, time, urllib.request, urllib.error
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.dirname(__file__))
import importlib
_pm = importlib.import_module(os.environ.get('PROMPTS', 'news_prompts')); P, full = _pm.P, _pm.full
SCRIPT, OUT = sys.argv[1], sys.argv[2]
for d in ('vo', 'scenes', 'depth', 'sheets'): os.makedirs(f'{OUT}/{d}', exist_ok=True)
def log(*a): print(time.strftime('%H:%M:%S'), *a, flush=True)

# ---------------- voiceover ----------------
async def tts_one(text, voice, rate, mp3, pitch='+0Hz'):
    import edge_tts
    try: com = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch, boundary='WordBoundary')
    except TypeError: com = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    words, sents = [], []
    with open(mp3, 'wb') as f:
        async for ch in com.stream():
            if ch['type'] == 'audio': f.write(ch['data'])
            elif ch['type'] == 'WordBoundary': words.append([ch['text'], round(ch['offset'] / 1e7, 3), round((ch['offset'] + ch['duration']) / 1e7, 3)])
            elif ch['type'] == 'SentenceBoundary': sents.append([ch['text'], round(ch['offset'] / 1e7, 3), round((ch['offset'] + ch['duration']) / 1e7, 3)])
    return words, sents
def voiceover():
    S = json.load(open(SCRIPT)); meta = {}
    for voice in S['voices']:
        vd = f'{OUT}/vo/{voice}'; os.makedirs(vd, exist_ok=True); ok = True; meta[voice] = {}
        for seg in S['segments']:
            for k in range(4):
                try:
                    w, s = asyncio.run(tts_one(seg['vo'], voice, S.get('rate', '+0%'), f'{vd}/{seg["id"]}.mp3', S.get('pitch', '+0Hz')))
                    meta[voice][seg['id']] = {'words': w, 'sentences': s}; break
                except Exception as e:
                    log('tts retry', voice, seg['id'], repr(e)[:120]); time.sleep(4 + 4 * k)
            else: ok = False
        log('voice', voice, 'ok' if ok else 'FAILED', 'words', sum(len(v['words']) for v in meta[voice].values()))
        if not ok: meta.pop(voice, None)
    json.dump(meta, open(f'{OUT}/vo/words.json', 'w'), indent=1)

# ---------------- backdrops (AI Horde, anonymous) ----------------
API = 'https://aihorde.net/api/v2'
H = {'apikey': '0000000000', 'Content-Type': 'application/json', 'Client-Agent': 'techvibe24-studio:1.0:anon', 'User-Agent': 'curl/8.5.0'}
MODELS = {'A': 'Juggernaut XL', 'B': 'Juggernaut XL', 'C': 'AlbedoBase XL (SDXL)'}
USE_PP = [True]
def req(method, path, body=None):
    r = urllib.request.Request(API + path, data=json.dumps(body).encode() if body is not None else None, headers=H, method=method)
    return json.load(urllib.request.urlopen(r, timeout=60))
def submit(sid, v, k=0):
    seed = str(abs(hash((sid, v, k, 'news'))) % 99991 + 11)
    params = {'sampler_name': 'k_dpmpp_2m', 'karras': True, 'cfg_scale': 5.5, 'width': 768, 'height': 1344, 'steps': 32, 'n': 1, 'seed': seed}
    if USE_PP[0]: params['post_processing'] = ['RealESRGAN_x2plus']
    body = {'prompt': full(sid), 'params': params, 'models': [MODELS[v]], 'nsfw': False, 'censor_nsfw': True, 'r2': True}
    return req('POST', '/generate/async', body)['id']
def generate(ids, variants, budget_min=50):
    todo = [(s, v) for s in ids for v in variants if not os.path.exists(f'{OUT}/scenes/{s}_{v}.jpg')]
    live, tries, t_end = {}, {}, time.time() + budget_min * 60
    while (todo or live) and time.time() < t_end:
        while todo and len(live) < 20:
            s, v = todo[0]
            try:
                live[(s, v)] = submit(s, v, tries.get((s, v), 0)); todo.pop(0); log('submitted', s, v, 'pp' if USE_PP[0] else '')
            except urllib.error.HTTPError as e:
                body = e.read()[:300].decode('utf8', 'replace'); log('submit wait', s, v, e.code, body[:160])
                if USE_PP[0] and ('kudos' in body.lower() or 'upfront' in body.lower() or 'post' in body.lower()): USE_PP[0] = False; continue
                break
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
                    im = Image.open(f'/tmp/{s}_{v}.webp').convert('RGB')
                    if im.width > 1080: im = im.resize((1080, round(1080 * im.height / im.width)), Image.LANCZOS)
                    im.save(f'{OUT}/scenes/{s}_{v}.jpg', quality=94)
                    log('done', s, v, im.size, g.get('worker_name'))
                elif c.get('faulted') or not c.get('is_possible', True):
                    del live[key]; raise ValueError('faulted')
            except Exception as e:
                gone = isinstance(e, ValueError) or (isinstance(e, urllib.error.HTTPError) and e.code == 404)
                if gone:
                    live.pop(key, None); tries[key] = tries.get(key, 0) + 1
                    if tries[key] < 4: todo.append(key)
                    log('retry', s, v, repr(e)[:80])
            time.sleep(0.6)
    log('generation finished; missing:', todo + list(live))
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
        Image.fromarray((d * 255).astype(np.uint8)).resize((W, Hh), Image.BICUBIC).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(4)).save(out)
    log('depth done')
def sheets(ids, variants):
    tw, th, per = 216, 378, 4
    for n in range(0, len(ids), per):
        chunk = ids[n:n + per]
        sheet = Image.new('RGB', (len(variants) * tw, len(chunk) * (th + 26)), (10, 14, 22)); d = ImageDraw.Draw(sheet)
        for i, s in enumerate(chunk):
            for j, v in enumerate(variants):
                x, y = j * tw, i * (th + 26); p = f'{OUT}/scenes/{s}_{v}.jpg'
                if os.path.exists(p): sheet.paste(Image.open(p).convert('RGB').resize((tw, th)), (x, y + 26))
                d.text((x + 6, y + 6), f'{s} {v}', fill=(120, 230, 255))
        sheet.save(f'{OUT}/sheets/news_sheet_{n // per + 1:02d}.jpg', quality=85)
    log('sheets done')
if __name__ == '__main__':
    what = sys.argv[3] if len(sys.argv) > 3 else 'all'
    if what in ('all', 'vo'): voiceover()
    if what in ('all', 'img'):
        ids = list(P); generate(ids, 'ABC'); depth_maps(); sheets(ids, 'ABC')
