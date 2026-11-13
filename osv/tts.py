'''Voiceover for every beat of the OS video (runs on GitHub Actions). python osv/tts.py osv/os_script.json OUT VOICE...'''
import asyncio, json, os, sys, time
import edge_tts
S = json.load(open(sys.argv[1])); OUT = sys.argv[2]; VOICES = sys.argv[3:]
beats = [(pi, bi, b['say']) for pi, p in enumerate(S['pages']) for bi, b in enumerate(p['beats'])]
async def one(voice, pi, bi, text, sem):
    path = f'{OUT}/{voice}/b{pi:03d}_{bi:02d}.mp3'
    if os.path.exists(path) and os.path.getsize(path) > 1000: return True
    async with sem:
        for k in range(5):
            try:
                await edge_tts.Communicate(text, voice, rate='+0%').save(path)
                if os.path.getsize(path) > 1000: return True
            except Exception as e:
                print('retry', voice, pi, bi, repr(e)[:100], flush=True)
            await asyncio.sleep(3 + 3 * k)
    return False
async def main():
    for v in VOICES:
        os.makedirs(f'{OUT}/{v}', exist_ok=True); sem = asyncio.Semaphore(4); t = time.time()
        ok = await asyncio.gather(*[one(v, pi, bi, s, sem) for pi, bi, s in beats])
        print(v, sum(ok), '/', len(ok), 'ok in', round(time.time() - t), 's', flush=True)
asyncio.run(main())
