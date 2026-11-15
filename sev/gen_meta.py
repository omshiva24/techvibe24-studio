'''YouTube chapters + English subtitles (SRT) from the final timeline.   python osv/gen_meta.py OUT_DIR'''
import json, os, re, sys, textwrap
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
tl = json.load(open(f'{HERE}/build/tl.json'))
def ts(t): return '%d:%02d:%02d' % (t // 3600, t % 3600 // 60, t % 60) if t >= 3600 else '%d:%02d' % (t // 60, t % 60)
chap = ['0:00 Introduction & contents']
for pg in tl['pages']:
    if pg['kind'] == 'chapter': chap.append(f"{ts(int(pg['t0']))} Ch {pg['num']}: {pg['title']}")
    NUM = {'ER Diagram to Tables': 'ER diagram to tables', 'Number of Super Keys': 'Counting super keys', 'Division Operator': 'Division operator',
           'SELECT, GROUP BY & HAVING': 'SQL GROUP BY & HAVING', 'Attribute Closure': 'Attribute closure', 'Finding Candidate Keys': 'Finding candidate keys',
           'Finding the Normal Form': 'Finding the normal form', 'Conflict Serializability': 'Conflict serializability', 'Log-Based Recovery & Checkpoints': 'Recovery with checkpoints',
           'Index Numerical: Block Accesses': 'Index block accesses', 'B+ Tree Insertion': 'B+ tree order & insertion'}
    if pg['kind'] == 'page' and pg['title'] in NUM:      # YouTube rejects < and > in descriptions, so no '->' here
        chap.append(f"{ts(int(pg['t0']))}   • {NUM[pg['title']]} (numerical)")
open(f'{OUT}/chapters.txt', 'w').write('\n'.join(chap) + '\n')
def srt_t(t): ms = int(round(t * 1000)); return '%02d:%02d:%02d,%03d' % (ms // 3600000, ms % 3600000 // 60000, ms % 60000 // 1000, ms % 1000)
subs = []
for pg in tl['pages']:
    for b in pg['beats']:
        sents = [s.strip() for s in re.split(r'(?<=[.!?])\s+', b['say']) if s.strip()]
        tot = sum(len(s) for s in sents); t = b['t0']
        for s in sents:
            d = b['d'] * len(s) / tot
            chunks = textwrap.wrap(s, 84) or [s]; per = d / len(chunks)
            for c in chunks:
                subs.append((t, t + per, '\n'.join(textwrap.wrap(c, 42)))); t += per
with open(f'{OUT}/SE_OneShot_English.srt', 'w') as f:
    for i, (a, b, s) in enumerate(subs, 1): f.write(f'{i}\n{srt_t(a)} --> {srt_t(b)}\n{s}\n\n')
print('\n'.join(chap)); print('subtitles', len(subs))
