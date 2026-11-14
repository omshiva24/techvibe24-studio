'''Worked exam problems for the Compiler Design video, computed in code so every table on screen is right.'''
EPS = 'ε'
# ---------------- FIRST / FOLLOW / LL(1) for the classic expression grammar
G_LL = [('E', ['T', "E'"]), ("E'", ['+', 'T', "E'"]), ("E'", [EPS]), ('T', ['F', "T'"]), ("T'", ['*', 'F', "T'"]), ("T'", [EPS]),
        ('F', ['(', 'E', ')']), ('F', ['id'])]
def nonterms(G): return list(dict.fromkeys(a for a, _ in G))
def first_follow(G, start):
    NT = nonterms(G); FIRST = {A: set() for A in NT}
    def first_seq(seq):
        out = set()
        for X in seq:
            if X == EPS: continue
            f = FIRST[X] if X in FIRST else {X}
            out |= f - {EPS}
            if EPS not in f: return out
        return out | {EPS}
    changed = True
    while changed:
        changed = False
        for A, rhs in G:
            f = first_seq(rhs)
            if not f <= FIRST[A]: FIRST[A] |= f; changed = True
    FOLLOW = {A: set() for A in NT}; FOLLOW[start].add('$'); changed = True
    while changed:
        changed = False
        for A, rhs in G:
            for i, X in enumerate(rhs):
                if X not in FOLLOW: continue
                f = first_seq(rhs[i + 1:]) if rhs[i + 1:] else {EPS}
                add = (f - {EPS}) | (FOLLOW[A] if EPS in f else set())
                if not add <= FOLLOW[X]: FOLLOW[X] |= add; changed = True
    return FIRST, FOLLOW, first_seq
def ll1_table(G, start):
    FIRST, FOLLOW, fs = first_follow(G, start); M = {}
    for A, rhs in G:
        f = fs(rhs)
        for a in f - {EPS}: M.setdefault((A, a), []).append((A, rhs))
        if EPS in f:
            for b in FOLLOW[A]: M.setdefault((A, b), []).append((A, rhs))
    return M
def ll1_parse(G, start, tokens):
    M = ll1_table(G, start); stack = ['$', start]; inp = tokens + ['$']; moves = []
    while True:
        X, a = stack[-1], inp[0]
        st = ''.join(reversed(stack)) if False else ' '.join(stack)
        if X == '$' and a == '$': moves.append((' '.join(stack), ' '.join(inp), 'accept')); return moves
        if X == a: moves.append((' '.join(stack), ' '.join(inp), f'match {a}')); stack.pop(); inp.pop(0); continue
        A, rhs = M[(X, a)][0]; moves.append((' '.join(stack), ' '.join(inp), f"{A} -> {' '.join(rhs)}")); stack.pop()
        for s in reversed(rhs):
            if s != EPS: stack.append(s)

# ---------------- LR(0) items + SLR table
def lr0(G, start):
    Gp = [(start + "'", [start])] + G
    def closure(items):
        items = set(items); changed = True
        while changed:
            changed = False
            for (p, d) in list(items):
                rhs = Gp[p][1]
                if d < len(rhs) and rhs[d] in nonterms(Gp):
                    for q, (A, r) in enumerate(Gp):
                        if A == rhs[d] and (q, 0) not in items: items.add((q, 0)); changed = True
        return frozenset(items)
    def goto(I, X): return closure({(p, d + 1) for (p, d) in I if d < len(Gp[p][1]) and Gp[p][1][d] == X})
    C = [closure({(0, 0)})]; trans = {}; syms = []
    for A, r in Gp:
        for s in [A] + r:
            if s not in syms and s != EPS: syms.append(s)
    i = 0
    while i < len(C):
        for X in syms:
            J = goto(C[i], X)
            if J:
                if J not in C: C.append(J)
                trans[(i, X)] = C.index(J)
        i += 1
    return Gp, C, trans
def item_str(Gp, p, d):
    A, r = Gp[p]; r = list(r); r.insert(d, '.'); return f"{A} -> {' '.join(r)}"
def slr(G, start):
    Gp, C, trans = lr0(G, start); _, FOLLOW, _ = first_follow(G, start); NT = nonterms(G)
    action, gto = {}, {}
    for i, I in enumerate(C):
        for (p, d) in I:
            r = Gp[p][1]
            if d < len(r):
                X = r[d]
                if X not in NT and (i, X) in trans: action.setdefault((i, X), set()).add(f's{trans[(i, X)]}')
            elif p == 0: action.setdefault((i, '$'), set()).add('acc')
            else:
                for b in FOLLOW[Gp[p][0]]: action.setdefault((i, b), set()).add(f'r{p}')
        for A in NT:
            if (i, A) in trans: gto[(i, A)] = trans[(i, A)]
    return Gp, C, trans, action, gto
def slr_parse(G, start, tokens):
    Gp, C, trans, action, gto = slr(G, start); st = [0]; sym = ['$']; inp = tokens + ['$']; moves = []
    while True:
        a = inp[0]; act = sorted(action[(st[-1], a)])[0]
        if act == 'acc': moves.append((' '.join(sym), ' '.join(inp), 'accept')); return moves
        if act[0] == 's': moves.append((' '.join(sym), ' '.join(inp), 'shift')); st.append(int(act[1:])); sym.append(a); inp.pop(0)
        else:
            A, r = Gp[int(act[1:])]; moves.append((' '.join(sym), ' '.join(inp), f"reduce {A} -> {' '.join(r)}"))
            for _ in r: st.pop(); sym.pop()
            sym.append(A); st.append(gto[(st[-1], A)])
G_SAA = [('S', ['A', 'A']), ('A', ['a', 'A']), ('A', ['b'])]
G_EXPR = [('E', ['E', '+', 'T']), ('E', ['T']), ('T', ['T', '*', 'F']), ('T', ['F']), ('F', ['(', 'E', ')']), ('F', ['id'])]

# ---------------- (a|b)*abb : Thompson NFA (textbook numbering) -> DFA by subset construction
NFA = {0: [(None, 1), (None, 7)], 1: [(None, 2), (None, 4)], 2: [('a', 3)], 3: [(None, 6)], 4: [('b', 5)], 5: [(None, 6)],
       6: [(None, 1), (None, 7)], 7: [('a', 8)], 8: [('b', 9)], 9: [('b', 10)], 10: []}
def eclose(S):
    S = set(S); st = list(S)
    while st:
        q = st.pop()
        for c, r in NFA[q]:
            if c is None and r not in S: S.add(r); st.append(r)
    return frozenset(S)
def subset():
    A = eclose({0}); D = [A]; T = {}; i = 0
    while i < len(D):
        for c in 'ab':
            U = eclose({r for q in D[i] for cc, r in NFA[q] if cc == c})
            if U not in D: D.append(U)
            T[(i, c)] = D.index(U)
        i += 1
    return D, T
def accepts(s, T, acc):
    q = 0
    for ch in s: q = T[(q, ch)]
    return q in acc

if __name__ == '__main__':
    F, Fo, _ = first_follow(G_LL, 'E'); print('FIRST', F); print('FOLLOW', Fo)
    M = ll1_table(G_LL, 'E'); print('LL1 conflicts', [k for k, v in M.items() if len(v) > 1]); print(sorted((k, v[0][1]) for k, v in M.items()))
    for m in ll1_parse(G_LL, 'E', ['id', '+', 'id', '*', 'id']): print(m)
    Gp, C, trans, action, gto = slr(G_SAA, 'S')
    for i, I in enumerate(C): print('I%d' % i, [item_str(Gp, p, d) for p, d in sorted(I)])
    print('trans', trans); print('action', {k: v for k, v in action.items()}); print('goto', gto)
    for m in slr_parse(G_EXPR, 'E', ['id', '*', 'id']): print(m)
    D, T = subset(); print('DFA', [sorted(s) for s in D], T, 'accepting', [i for i, s in enumerate(D) if 10 in s])
    acc = {i for i, s in enumerate(D) if 10 in s}
    print([s for s in ['abb', 'aabb', 'babb', 'ab', 'abba', 'bbabb'] if accepts(s, T, acc)])
