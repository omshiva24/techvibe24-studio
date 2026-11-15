'''Voiceover for every beat of the DBMS video (runs on GitHub Actions).   python dbv/tts.py dbv/db_script.json OUT VOICE...
A beat is re-generated only when its text changed (texts.json keeps the text of every saved file).
SHARD="k/n" makes this runner do every n-th beat starting at k; it then writes texts_k.json, and the merge job joins them.'''
import asyncio, json, os, sys, time
import edge_tts
S = json.load(open(sys.argv[1])); OUT = sys.argv[2]; VOICES = sys.argv[3:]
beats = [(pi, bi, b['say']) for pi, p in enumerate(S['pages']) for bi, b in enumerate(p['beats'])]
SH = os.environ.get('SHARD')
if SH:
    k_, n_ = map(int, SH.split('/')); beats = beats[k_::n_]
DEADLINE = time.time() + float(os.environ.get('TTS_MINUTES', '45')) * 60    # stop early so whatever is done still gets published
async def one(voice, pi, bi, text, sem):
    path = f'{OUT}/{voice}/b{pi:03d}_{bi:02d}.mp3'
    if os.path.exists(path) and os.path.getsize(path) > 1000: return True
    async with sem:
        for k in range(8):
            if time.time() > DEADLINE: return False
            try:
                await asyncio.wait_for(edge_tts.Communicate(text, voice, rate='+0%').save(path), 120)
                if os.path.getsize(path) > 1000: return True
            except Exception as e:
                print('retry', voice, pi, bi, repr(e)[:100], flush=True)
            await asyncio.sleep(3 + 3 * k)
    return False
async def main():
    for v in VOICES:
        os.makedirs(f'{OUT}/{v}', exist_ok=True); sem = asyncio.Semaphore(2); t = time.time()
        tj = f'{OUT}/{v}/texts.json'; old = json.load(open(tj)) if os.path.exists(tj) else {}
        for pi, bi, s in beats:
            k = f'b{pi:03d}_{bi:02d}'; path = f'{OUT}/{v}/{k}.mp3'
            if os.path.exists(path) and old.get(k) != s: os.remove(path)
        ok = await asyncio.gather(*[one(v, pi, bi, s, sem) for pi, bi, s in beats])
        done = {f'b{pi:03d}_{bi:02d}': s for (pi, bi, s), o in zip(beats, ok) if o}
        out = f'{OUT}/{v}/texts_{SH.split("/")[0]}.json' if SH else tj
        json.dump(done, open(out, 'w'), indent=0, ensure_ascii=False)
        for (pi, bi, s), o in zip(beats, ok):
            p_ = f'{OUT}/{v}/b{pi:03d}_{bi:02d}.mp3'
            if not o and os.path.exists(p_): os.remove(p_)
        print(v, sum(ok), '/', len(ok), 'ok in', round(time.time() - t), 's', flush=True)
asyncio.run(main())
