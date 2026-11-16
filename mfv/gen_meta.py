'''YouTube chapters + English subtitles (SRT) from the final timeline.   python mfv/gen_meta.py OUT_DIR'''
import json, os, re, sys, textwrap
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
tl = json.load(open(f'{HERE}/build/tl.json'))
def ts(t): return '%d:%02d:%02d' % (t // 3600, t % 3600 // 60, t % 60) if t >= 3600 else '%d:%02d' % (t // 60, t % 60)
chap = ['0:00 Introduction & contents']
for pg in tl['pages']:
    if pg['kind'] == 'chapter': chap.append(f"{ts(int(pg['t0']))} Ch {pg['num']}: {pg['title']}")
    NUM = {'Truth Tables & Tautology': 'Truth tables & tautology', 'Logical Equivalences': 'Logical equivalences (laws)', 'Normal Forms: PDNF & PCNF': 'PDNF & PCNF (numerical)',
           'Rules of Inference': 'Rules of inference', 'Valid Argument: Step by Step': 'Valid argument (numerical)', 'Predicates & Quantifiers': 'Predicates & quantifiers',
           'Methods of Proof': 'Proof methods', 'Venn Diagram Numerical': 'Venn diagram (numerical)', 'Functions': 'Functions', 'Sequences & Summations': 'Sequences & summations',
           'Matrices & Zero-One Matrices': 'Matrices', 'Relations & Their Properties': 'Properties of relations', "Representing Relations & Warshall's Algorithm": "Warshall's algorithm",
           'Equivalence Relations & Partial Orders': 'Equivalence & Hasse diagram', 'Divisibility & Modular Arithmetic': 'Division algorithm & mod', 'Integer Representations': 'Base conversion',
           'Modular Exponentiation': 'Modular exponentiation', 'Primes & Prime Factorization': 'Primes', 'GCD: Euclidean Algorithm': 'GCD (Euclid) numerical',
           'Linear Congruences & CRT': 'Linear congruence & CRT', "Fermat's Little Theorem": "Fermat's little theorem", 'Mathematical Induction': 'Mathematical induction',
           'Strong Induction & Well-Ordering': 'Strong induction', 'Recursive Definitions & Structural Induction': 'Recursive definitions', 'Pigeonhole Principle': 'Pigeonhole principle',
           'Permutations & Combinations': 'Permutations & combinations', 'Binomial Theorem & Inclusion-Exclusion': 'Binomial theorem & inclusion-exclusion',
           'Groups & Algebraic Structures': 'Groups', 'Subgroups, Lagrange & Homomorphism': "Lagrange's theorem", 'Solving Recurrence Relations': 'Recurrence relations (numerical)',
           'Non-homogeneous Recurrences & Generating Functions': 'Generating functions', 'Euler & Hamiltonian Graphs': 'Euler & Hamiltonian', 'Planar Graphs & Graph Colouring': 'Planar graphs & colouring',
           'Trees & Minimum Spanning Tree': 'Trees & MST (numerical)', 'Formula Sheet': 'Formula sheet'}
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
with open(f'{OUT}/MFCS_OneShot_English.srt', 'w') as f:
    for i, (a, b, s) in enumerate(subs, 1): f.write(f'{i}\n{srt_t(a)} --> {srt_t(b)}\n{s}\n\n')
print('\n'.join(chap)); print('subtitles', len(subs))
