'''Worked exam problems for the Theory of Computation video, computed in code so every answer on screen is right.'''
import itertools, re

def strings(alpha, n):
    for k in range(n + 1):
        for t in itertools.product(alpha, repeat=k): yield ''.join(t)

# ---------------------------------------------------------------- DFAs
def run_dfa(d, start, s):
    q = start; trace = [q]
    for c in s: q = d[(q, c)]; trace.append(q)
    return trace
ENDS_AB = {('q0', 'a'): 'q1', ('q0', 'b'): 'q0', ('q1', 'a'): 'q1', ('q1', 'b'): 'q2', ('q2', 'a'): 'q1', ('q2', 'b'): 'q0'}
EVEN = {('q0', 'a'): 'q1', ('q1', 'a'): 'q0', ('q2', 'a'): 'q3', ('q3', 'a'): 'q2', ('q0', 'b'): 'q2', ('q2', 'b'): 'q0', ('q1', 'b'): 'q3', ('q3', 'b'): 'q1'}
MOD3 = {(f'q{r}', c): f'q{(2 * r + int(c)) % 3}' for r in range(3) for c in '01'}

# ---------------------------------------------------------------- NFA -> DFA (second last symbol is 1)
NFA = {('q0', '0'): {'q0'}, ('q0', '1'): {'q0', 'q1'}, ('q1', '0'): {'q2'}, ('q1', '1'): {'q2'}}
def subset(nfa=NFA, start='q0', alpha='01'):
    S0 = frozenset([start]); D = [S0]; T = {}; i = 0
    while i < len(D):
        for c in alpha:
            U = frozenset(r for q in D[i] for r in nfa.get((q, c), set()))
            if U not in D: D.append(U)
            T[(D[i], c)] = U
        i += 1
    return D, T
def sname(S): return '{' + ', '.join(sorted(S)) + '}' if S else '∅'

# ---------------------------------------------------------------- minimisation (partition method)
MIN = {('A', 'a'): 'B', ('A', 'b'): 'C', ('B', 'a'): 'B', ('B', 'b'): 'D', ('C', 'a'): 'B', ('C', 'b'): 'C',
       ('D', 'a'): 'B', ('D', 'b'): 'E', ('E', 'a'): 'B', ('E', 'b'): 'C', ('F', 'a'): 'D', ('F', 'b'): 'E'}
def minimise(d=MIN, start='A', finals={'E'}, alpha='ab'):
    reach = {start}; st = [start]
    while st:
        q = st.pop()
        for c in alpha:
            r = d[(q, c)]
            if r not in reach: reach.add(r); st.append(r)
    Q = sorted(reach); P = [sorted(set(Q) - finals), sorted(finals & set(Q))]; steps = [P]
    while True:
        blk = {q: i for i, b in enumerate(P) for q in b}; NP = []
        for b in P:
            groups = {}
            for q in b: groups.setdefault(tuple(blk[d[(q, c)]] for c in alpha), []).append(q)
            NP += list(groups.values())
        steps.append(NP)
        if len(NP) == len(P): return sorted(set(MIN_all := [k[0] for k in d]) - reach), steps
        P = NP

# ---------------------------------------------------------------- Arden's theorem check: (a + b a* b)* b a* = odd number of b
def arden_ok():
    rx = re.compile(r'(a|ba*b)*ba*')
    return all(bool(rx.fullmatch(s)) == (s.count('b') % 2 == 1) for s in strings('ab', 9))

# ---------------------------------------------------------------- CYK
CNF = [('S', ('A', 'B')), ('S', ('B', 'C')), ('A', ('B', 'A')), ('A', ('a',)), ('B', ('C', 'C')), ('B', ('b',)), ('C', ('A', 'B')), ('C', ('a',))]
def cyk(w, g=CNF):
    n = len(w); V = {}
    for i, c in enumerate(w): V[(i, i)] = {A for A, r in g if r == (c,)}
    for L in range(2, n + 1):
        for i in range(n - L + 1):
            j = i + L - 1; s = set()
            for k in range(i, j):
                for A, r in g:
                    if len(r) == 2 and r[0] in V[(i, k)] and r[1] in V[(k + 1, j)]: s.add(A)
            V[(i, j)] = s
    return V

# ---------------------------------------------------------------- PDA for a^n b^n
def pda_anbn(w):
    st = ['Z0']; q = 'q0'; ids = [(q, w, 'Z0')]; i = 0
    while True:
        top = st[-1]; c = w[i] if i < len(w) else None
        if q == 'q0' and c == 'a': st.append('a'); i += 1
        elif q in ('q0', 'q1') and c == 'b' and top == 'a': st.pop(); q = 'q1'; i += 1
        elif q == 'q1' and c is None and top == 'Z0': q = 'qf'
        else: return ids, False
        ids.append((q, w[i:] or 'ε', ''.join(reversed(st))))
        if q == 'qf': return ids, True

# ---------------------------------------------------------------- CFG -> PDA (one state, empty stack), S -> aSb | ab
GR = {'S': ['aSb', 'ab']}
def cfg_pda(w, choices):
    st = 'S'; i = 0; ids = [(w, st)]; ch = list(choices)
    while st:
        top = st[0]
        if top in GR: st = GR[top][ch.pop(0)] + st[1:]
        elif i < len(w) and w[i] == top: st = st[1:]; i += 1
        else: return ids, False
        ids.append((w[i:] or 'ε', st or 'ε'))
    return ids, i == len(w)

# ---------------------------------------------------------------- Turing machine for a^n b^n
TM = {('q0', 'a'): ('q1', 'X', 'R'), ('q0', 'Y'): ('q3', 'Y', 'R'), ('q1', 'a'): ('q1', 'a', 'R'), ('q1', 'Y'): ('q1', 'Y', 'R'),
      ('q1', 'b'): ('q2', 'Y', 'L'), ('q2', 'a'): ('q2', 'a', 'L'), ('q2', 'Y'): ('q2', 'Y', 'L'), ('q2', 'X'): ('q0', 'X', 'R'),
      ('q3', 'Y'): ('q3', 'Y', 'R'), ('q3', 'B'): ('q4', 'B', 'R')}
def run_tm(w, tm=TM):
    tape = list(w) + ['B']; h = 0; q = 'q0'; ids = []
    for _ in range(200):
        ids.append(''.join(tape[:h]) + q + ''.join(tape[h:]).rstrip('B'))
        if q == 'q4': return ids, True
        k = (q, tape[h])
        if k not in tm: return ids, False
        q, tape[h], m = tm[k]; h += 1 if m == 'R' else -1
        if h == len(tape): tape.append('B')
    return ids, False

# ---------------------------------------------------------------- PCP (Sipser)
PCP_T, PCP_B = ['b', 'a', 'ca', 'abc'], ['ca', 'ab', 'a', 'c']
def pcp_check(seq): return ''.join(PCP_T[i - 1] for i in seq), ''.join(PCP_B[i - 1] for i in seq)

if __name__ == '__main__':
    print('ends ab', [s for s in strings('ab', 4) if run_dfa(ENDS_AB, 'q0', s)[-1] == 'q2'][:8])
    print('mod3', run_dfa(MOD3, 'q0', '1100'), run_dfa(MOD3, 'q0', '1010'), [int(s, 2) for s in ('1100', '1010')])
    D, T = subset(); print([sname(S) for S in D]); print({(sname(a), c): sname(b) for (a, c), b in T.items()})
    print('min', minimise()); print('arden', arden_ok())
    V = cyk('baaba'); n = 5
    for L in range(1, n + 1): print(L, [sorted(V[(i, i + L - 1)]) for i in range(n - L + 1)])
    print('pda', pda_anbn('aabb')); print('pda bad', pda_anbn('aab')[1])
    ids, ok = run_tm('aabb'); print('tm', ok, len(ids), ids)
    print('even', [x for x in strings('ab', 4) if run_dfa(EVEN, 'q0', x)[-1] == 'q0'][:10], run_dfa(EVEN, 'q0', 'abab'))
    print('cfgpda', cfg_pda('aabb', [0, 1]))
    print('pcp', pcp_check([2, 1, 3, 2, 4]))
