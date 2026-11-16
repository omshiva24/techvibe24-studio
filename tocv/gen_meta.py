'''YouTube chapters + English subtitles (SRT) from the final timeline.   python tocv/gen_meta.py OUT_DIR'''
import json, os, re, sys, textwrap
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
tl = json.load(open(f'{HERE}/build/tl.json'))
def ts(t): return '%d:%02d:%02d' % (t // 3600, t % 3600 // 60, t % 60) if t >= 3600 else '%d:%02d' % (t // 60, t % 60)
chap = ['0:00 Introduction & contents']
for pg in tl['pages']:
    if pg['kind'] == 'chapter': chap.append(f"{ts(int(pg['t0']))} Ch {pg['num']}: {pg['title']}")
    NUM = {'DFA Design: Strings Ending with "ab"': 'DFA design (numerical)', 'DFA for Binary Numbers Divisible by 3': 'DFA divisible by 3',
           "DFA for Even a's and Even b's": "DFA even a's and b's", 'NFA to DFA: Subset Construction': 'NFA to DFA (numerical)',
           'DFA Minimization: Partition Method': 'DFA minimization (numerical)', "FA to RE: Arden's Theorem": "Arden's theorem (numerical)",
           'Pumping Lemma for Regular Languages': 'Pumping lemma', 'Ambiguous Grammar': 'Ambiguity', 'Simplifying a CFG': 'Simplifying a CFG',
           'Chomsky & Greibach Normal Forms': 'CNF and GNF', 'CYK Algorithm': 'CYK algorithm (numerical)', 'PDA for a^n b^n': 'PDA design (numerical)',
           'CFG to PDA Conversion': 'CFG to PDA', 'TM for a^n b^n': 'Turing machine design (numerical)', 'Decidability & The Halting Problem': 'Halting problem',
           'Closure Properties: GATE Table': 'Closure table', 'Decision Properties: GATE Table': 'Decidability table', 'P, NP & NP-Complete': 'P, NP, NP-complete'}
    if pg['kind'] == 'page' and pg['title'] in NUM:      # YouTube rejects < and > in descriptions, so no '->' here
        chap.append(f"{ts(int(pg['t0']))}   • {NUM[pg['title']]}")
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
with open(f'{OUT}/TOC_OneShot_English.srt', 'w') as f:
    for i, (a, b, s) in enumerate(subs, 1): f.write(f'{i}\n{srt_t(a)} --> {srt_t(b)}\n{s}\n\n')
print('\n'.join(chap)); print('subtitles', len(subs))
