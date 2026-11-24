'''Worked exam problems for the DSA (MCA) + Advanced DSA (M.Tech) one-shot, computed in code so every answer on screen is right.'''
import math, heapq, itertools
from collections import deque, Counter

# ---------------------------------------------------------------- arrays & searching
def addr(base, size, rows, cols, i, j, order='row'):
    return base + size * ((i * cols + j) if order == 'row' else (j * rows + i))
def bsearch_trace(a, x):
    lo, hi, steps = 0, len(a) - 1, []
    while lo <= hi:
        mid = (lo + hi) // 2; steps.append((lo, hi, mid, a[mid]))
        if a[mid] == x: return mid, steps
        if a[mid] < x: lo = mid + 1
        else: hi = mid - 1
    return -1, steps

# ---------------------------------------------------------------- stacks
PREC = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
def to_postfix(expr):
    st, out, rows = [], [], []
    for ch in expr:
        if ch.isalnum(): out.append(ch)
        elif ch == '(': st.append(ch)
        elif ch == ')':
            while st[-1] != '(': out.append(st.pop())
            st.pop()
        else:
            while st and st[-1] != '(' and (PREC[st[-1]] > PREC[ch] or (PREC[st[-1]] == PREC[ch] and ch != '^')): out.append(st.pop())
            st.append(ch)
        rows.append((ch, ''.join(st) or '-', ''.join(out)))
    while st: out.append(st.pop())
    rows.append(('end', '-', ''.join(out)))
    return ''.join(out), rows
def eval_postfix(tokens):
    st, rows = [], []
    for t in tokens.split():
        if t.isdigit(): st.append(int(t))
        else:
            b, a = st.pop(), st.pop(); st.append({'+': a + b, '-': a - b, '*': a * b, '/': a // b}[t])
        rows.append((t, ' '.join(map(str, st))))
    return st[0], rows

# ---------------------------------------------------------------- trees
TREE = {'A': ('B', 'C'), 'B': ('D', 'E'), 'C': (None, 'F'), 'D': (None, None), 'E': ('G', None), 'F': (None, None), 'G': (None, None)}
def pre(t, n): return [] if n is None else [n] + pre(t, t[n][0]) + pre(t, t[n][1])
def ino(t, n): return [] if n is None else ino(t, t[n][0]) + [n] + ino(t, t[n][1])
def post(t, n): return [] if n is None else post(t, t[n][0]) + post(t, t[n][1]) + [n]
def level(t, r):
    q, out = deque([r]), []
    while q:
        n = q.popleft(); out.append(n)
        for c in t[n]:
            if c: q.append(c)
    return out
def bst_insert(keys):
    t = {}; root = None
    for k in keys:
        if root is None: root = k; t[k] = [None, None]; continue
        n = root
        while True:
            side = 0 if k < n else 1
            if t[n][side] is None: t[n][side] = k; t[k] = [None, None]; break
            n = t[n][side]
    return root, t

# ---------------------------------------------------------------- graphs
UG = {'A': ['B', 'C'], 'B': ['A', 'D', 'E'], 'C': ['A', 'F'], 'D': ['B'], 'E': ['B', 'F'], 'F': ['C', 'E']}
def bfs(g, s):
    seen, q = [s], deque([s])
    while q:
        u = q.popleft()
        for v in g[u]:
            if v not in seen: seen.append(v); q.append(v)
    return seen
def dfs(g, s, seen=None):
    seen = [] if seen is None else seen; seen.append(s)
    for v in g[s]:
        if v not in seen: dfs(g, v, seen)
    return seen
DAG = {'1': ['2', '3'], '2': ['4'], '3': ['4', '5'], '4': ['6'], '5': ['6'], '6': []}
def kahn(g):
    indeg = {v: 0 for v in g}
    for u in g:
        for v in g[u]: indeg[v] += 1
    q = sorted(v for v in g if indeg[v] == 0); out = []
    while q:
        u = q.pop(0); out.append(u)
        for v in g[u]:
            indeg[v] -= 1
            if indeg[v] == 0: q.append(v); q.sort()
    return out
WG = [(4, 'A', 'B'), (2, 'A', 'C'), (1, 'B', 'C'), (5, 'B', 'D'), (8, 'C', 'D'), (10, 'C', 'E'), (2, 'D', 'E'), (6, 'B', 'E')]
def kruskal(V, E):
    par = {v: v for v in V}
    def f(v):
        while par[v] != v: v = par[v]
        return v
    out = []
    for w, a, b in sorted(E):
        ok = f(a) != f(b)
        if ok: par[f(a)] = f(b)
        out.append((a, b, w, ok))
    return out
def prim(V, E, s='A'):
    adj = {v: [] for v in V}
    for w, a, b in E: adj[a].append((w, b)); adj[b].append((w, a))
    inT, out, pq = {s}, [], [(w, s, b) for w, b in adj[s]]; heapq.heapify(pq)
    while pq and len(inT) < len(V):
        w, a, b = heapq.heappop(pq)
        if b in inT: continue
        inT.add(b); out.append((a, b, w))
        for w2, c in adj[b]:
            if c not in inT: heapq.heappush(pq, (w2, b, c))
    return out
def dijkstra(V, E, s='A'):
    adj = {v: [] for v in V}
    for w, a, b in E: adj[a].append((w, b)); adj[b].append((w, a))
    dist = {v: math.inf for v in V}; prev = {v: None for v in V}; dist[s] = 0; done = []; steps = []
    while len(done) < len(V):
        u = min((v for v in V if v not in done), key=lambda v: (dist[v], v)); done.append(u)
        for w, v in adj[u]:
            if v not in done and dist[u] + w < dist[v]: dist[v] = dist[u] + w; prev[v] = u
        steps.append((''.join(done), {v: dist[v] for v in V}))
    return dist, prev, steps
def path(prev, t):
    p = [t]
    while prev[p[-1]]: p.append(prev[p[-1]])
    return '-'.join(reversed(p))

# ---------------------------------------------------------------- divide & conquer
def merge_sort_levels(a):
    levels = [[a]]
    while any(len(x) > 1 for x in levels[-1]):
        nxt = []
        for x in levels[-1]:
            if len(x) > 1: m = (len(x) + 1) // 2; nxt += [x[:m], x[m:]]
            else: nxt.append(x)
        levels.append(nxt)
    return levels
def partition(a):
    a = a[:]; x = a[-1]; i = -1; rows = []
    for j in range(len(a) - 1):
        if a[j] <= x: i += 1; a[i], a[j] = a[j], a[i]
        rows.append((j, i, a[:]))
    a[i + 1], a[-1] = a[-1], a[i + 1]; rows.append(('swap', i + 1, a[:]))
    return a, i + 1, rows
STOCK = [13, -3, -25, 20, -3, -16, -23, 18, 20, -7, 12, -5, -22, 15, -4, 7]
def max_subarray(a):
    best = (-math.inf, 0, 0)
    for i in range(len(a)):
        s = 0
        for j in range(i, len(a)):
            s += a[j]
            if s > best[0]: best = (s, i, j)
    return best
def strassen2(A, B):
    (a, b), (c, d) = A; (e, f), (g, h) = B
    P = [a * (f - h), (a + b) * h, (c + d) * e, d * (g - e), (a + d) * (e + h), (b - d) * (g + h), (a - c) * (e + f)]
    C = [[P[4] + P[3] - P[1] + P[5], P[0] + P[1]], [P[2] + P[3], P[4] + P[0] - P[2] - P[6]]]
    return P, C

# ---------------------------------------------------------------- greedy
def frac_knap(items, W):
    out, val = [], 0
    for v, w in sorted(items, key=lambda x: -x[0] / x[1]):
        take = min(w, W); val += v * take / w; W -= take; out.append((v, w, take))
        if W == 0: break
    return val, out
JOBS = [('J1', 100, 2), ('J2', 19, 1), ('J3', 27, 2), ('J4', 25, 1), ('J5', 15, 3)]
def job_seq(jobs):
    T = max(d for _, _, d in jobs); slot = [None] * (T + 1); rows = []
    for n, p, d in sorted(jobs, key=lambda x: -x[1]):
        for s in range(d, 0, -1):
            if slot[s] is None: slot[s] = n; rows.append((n, p, d, f'slot {s}')); break
        else: rows.append((n, p, d, 'rejected'))
    return slot[1:], sum(p for n, p, d in jobs if n in slot), rows
HUFF = {'a': 45, 'b': 13, 'c': 12, 'd': 16, 'e': 9, 'f': 5}
def huffman(freq):
    cnt = itertools.count(); h = [(f, next(cnt), c) for c, f in sorted(freq.items(), key=lambda x: x[1])]; heapq.heapify(h); merges = []
    while len(h) > 1:
        f1, _, a = heapq.heappop(h); f2, _, b = heapq.heappop(h); merges.append((f1, f2, f1 + f2)); heapq.heappush(h, (f1 + f2, next(cnt), (a, b)))
    codes = {}
    def walk(n, s):
        if isinstance(n, str): codes[n] = s; return
        walk(n[0], s + '0'); walk(n[1], s + '1')
    walk(h[0][2], ''); return codes, merges, h[0][2]

# ---------------------------------------------------------------- dynamic programming
def knap01(items, W):
    n = len(items); K = [[0] * (W + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        w, v = items[i - 1]
        for c in range(W + 1): K[i][c] = max(K[i - 1][c], K[i - 1][c - w] + v if w <= c else 0)
    pick, c = [], W
    for i in range(n, 0, -1):
        if K[i][c] != K[i - 1][c]: pick.append(i); c -= items[i - 1][0]
    return K, sorted(pick)
ROD = [1, 5, 8, 9, 10, 17, 17, 20, 24, 30]
def rod(p, n):
    r = [0] * (n + 1); s = [0] * (n + 1)
    for j in range(1, n + 1):
        q = -1
        for i in range(1, j + 1):
            if q < p[i - 1] + r[j - i]: q = p[i - 1] + r[j - i]; s[j] = i
        r[j] = q
    return r, s
def matrix_chain(p):
    n = len(p) - 1; m = [[0] * (n + 1) for _ in range(n + 1)]; s = [[0] * (n + 1) for _ in range(n + 1)]
    for L in range(2, n + 1):
        for i in range(1, n - L + 2):
            j = i + L - 1; m[i][j] = math.inf
            for k in range(i, j):
                q = m[i][k] + m[k + 1][j] + p[i - 1] * p[k] * p[j]
                if q < m[i][j]: m[i][j] = q; s[i][j] = k
    def par(i, j): return f'A{i}' if i == j else '(' + par(i, s[i][j]) + par(s[i][j] + 1, j) + ')'
    return m, s, par(1, n)
def lcs(X, Y):
    c = [[0] * (len(Y) + 1) for _ in range(len(X) + 1)]
    for i in range(1, len(X) + 1):
        for j in range(1, len(Y) + 1):
            c[i][j] = c[i - 1][j - 1] + 1 if X[i - 1] == Y[j - 1] else max(c[i - 1][j], c[i][j - 1])
    i, j, out = len(X), len(Y), ''
    while i and j:
        if X[i - 1] == Y[j - 1]: out = X[i - 1] + out; i -= 1; j -= 1
        elif c[i - 1][j] >= c[i][j - 1]: i -= 1
        else: j -= 1
    return c, out
OB_P = [.15, .10, .05, .10, .20]; OB_Q = [.05, .10, .05, .05, .05, .10]
def obst(p=OB_P, q=OB_Q):
    n = len(p); e = [[0] * (n + 2) for _ in range(n + 2)]; w = [[0] * (n + 2) for _ in range(n + 2)]; root = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 2): e[i][i - 1] = q[i - 1]; w[i][i - 1] = q[i - 1]
    for L in range(1, n + 1):
        for i in range(1, n - L + 2):
            j = i + L - 1; e[i][j] = math.inf; w[i][j] = w[i][j - 1] + p[j - 1] + q[j]
            for r in range(i, j + 1):
                t = e[i][r - 1] + e[r + 1][j] + w[i][j]
                if t < e[i][j] - 1e-12: e[i][j] = t; root[i][j] = r
    def tree(i, j):
        if j < i: return None
        r = root[i][j]; return (f'k{r}', tree(i, r - 1), tree(r + 1, j))
    return round(e[1][n], 4), tree(1, n)
TSP = [[0, 10, 15, 20], [5, 0, 9, 10], [6, 13, 0, 12], [8, 8, 9, 0]]
def tsp_dp(d):
    n = len(d); g = {}
    for k in range(1, n): g[(k, frozenset())] = (d[k][0], 0)
    for size in range(1, n - 1):
        for S in itertools.combinations(range(1, n), size):
            S = frozenset(S)
            for k in range(1, n):
                if k in S: continue
                g[(k, S)] = min((d[k][m] + g[(m, S - {m})][0], m) for m in S)
    full = frozenset(range(1, n)); best = min((d[0][m] + g[(m, full - {m})][0], m) for m in full)
    tour, cur, S = [0, best[1]], best[1], full - {best[1]}
    while S: nxt = g[(cur, S)][1]; tour.append(nxt); S = S - {nxt}; cur = nxt
    return best[0], [t + 1 for t in tour] + [1], g

# ---------------------------------------------------------------- backtracking
def nqueens(n):
    sols = []
    def place(row, cols):
        if row == n: sols.append(cols[:]); return
        for c in range(n):
            if all(c != cc and abs(c - cc) != row - r for r, cc in enumerate(cols)): cols.append(c); place(row + 1, cols); cols.pop()
    place(0, []); return [[c + 1 for c in s] for s in sols]
CG = {'A': 'BC', 'B': 'ACD', 'C': 'ABD', 'D': 'BC'}
def colourings(g, m):
    V = sorted(g); out = []
    def go(i, col):
        if i == len(V): out.append(dict(col)); return
        for c in range(1, m + 1):
            if all(col.get(u) != c for u in g[V[i]]): col[V[i]] = c; go(i + 1, col); del col[V[i]]
    go(0, {}); return out

# ---------------------------------------------------------------- B-tree (CLRS, minimum degree t, proactive splitting)
class BNode:
    def __init__(s, leaf=True): s.keys, s.kids, s.leaf = [], [], leaf
def btree_insert(keys, t=2):
    root = BNode(); snaps = []
    def split(x, i):
        y = x.kids[i]; z = BNode(y.leaf); mid = y.keys[t - 1]
        z.keys = y.keys[t:]; y.keys = y.keys[:t - 1]
        if not y.leaf: z.kids = y.kids[t:]; y.kids = y.kids[:t]
        x.kids.insert(i + 1, z); x.keys.insert(i, mid)
    def nonfull(x, k):
        if x.leaf: x.keys.append(k); x.keys.sort(); return
        i = sum(1 for q in x.keys if q < k)
        if len(x.kids[i].keys) == 2 * t - 1:
            split(x, i)
            if k > x.keys[i]: i += 1
        nonfull(x.kids[i], k)
    for k in keys:
        if len(root.keys) == 2 * t - 1:
            s = BNode(False); s.kids = [root]; split(s, 0); root = s
        nonfull(root, k); snaps.append((k, dump(root)))
    return root, snaps
def dump(n): return (list(n.keys), [dump(c) for c in n.kids])

# ---------------------------------------------------------------- disjoint sets
def dsu_run(n, unions):
    par = list(range(n + 1)); rank = [0] * (n + 1)
    def find(x):
        if par[x] != x: par[x] = find(par[x])
        return par[x]
    rows = []
    for a, b in unions:
        ra, rb = find(a), find(b)
        if ra != rb:
            if rank[ra] < rank[rb]: ra, rb = rb, ra
            par[rb] = ra
            if rank[ra] == rank[rb]: rank[ra] += 1
        rows.append(((a, b), par[1:].copy(), rank[1:].copy()))
    return rows

# ---------------------------------------------------------------- hashing (CLRS 11.4-1)
HK = [10, 22, 31, 4, 15, 28, 17, 88, 59]
def open_address(keys, m, kind):
    T = [None] * m; probes = {}
    for k in keys:
        for i in range(m):
            if kind == 'linear': j = (k + i) % m
            elif kind == 'quadratic': j = (k + 1 * i + 3 * i * i) % m
            else: j = (k + i * (1 + k % (m - 1))) % m
            if T[j] is None: T[j] = k; probes[k] = i; break
    return T, probes

# ---------------------------------------------------------------- randomized & amortized
def harmonic(n): return sum(1 / k for k in range(1, n + 1))
def counter_flips(n, bits=8):
    x, flips = 0, 0
    for _ in range(n):
        y = (x + 1) % (1 << bits); flips += bin(x ^ y).count('1'); x = y
    return flips

# ---------------------------------------------------------------- Johnson (CLRS fig 25.6)
JE = [(1, 2, 3), (1, 3, 8), (1, 5, -4), (2, 4, 1), (2, 5, 7), (3, 2, 4), (4, 1, 2), (4, 3, -5), (5, 4, 6)]
def bellman(n, E, s):
    d = {v: math.inf for v in range(n + 1)}; d[s] = 0
    for _ in range(n):
        for u, v, w in E:
            if d[u] + w < d[v]: d[v] = d[u] + w
    return d
def johnson(E=JE, n=5):
    E2 = E + [(0, v, 0) for v in range(1, n + 1)]; h = bellman(n, E2, 0)
    rew = [(u, v, w + h[u] - h[v]) for u, v, w in E]
    return {v: h[v] for v in range(1, n + 1)}, rew

# ---------------------------------------------------------------- max flow (CLRS fig 26.1)
FN = {('s', 'v1'): 16, ('s', 'v2'): 13, ('v1', 'v3'): 12, ('v2', 'v1'): 4, ('v2', 'v4'): 14, ('v3', 'v2'): 9, ('v3', 't'): 20, ('v4', 'v3'): 7, ('v4', 't'): 4}
def edmonds_karp(cap=FN, s='s', t='t'):
    res = Counter(); V = set()
    for (u, v), c in cap.items(): res[(u, v)] += c; V |= {u, v}
    flow, paths = 0, []
    while True:
        par = {s: None}; q = deque([s])
        while q and t not in par:
            u = q.popleft()
            for v in sorted(V):
                if v not in par and res[(u, v)] > 0: par[v] = u; q.append(v)
        if t not in par: break
        p = [t]
        while par[p[-1]] is not None: p.append(par[p[-1]])
        p = p[::-1]; b = min(res[(p[i], p[i + 1])] for i in range(len(p) - 1))
        for i in range(len(p) - 1): res[(p[i], p[i + 1])] -= b; res[(p[i + 1], p[i])] += b
        flow += b; paths.append(('-'.join(p), b))
    reach = set(par)
    cut = [(u, v, c) for (u, v), c in cap.items() if u in reach and v not in reach]
    return flow, paths, reach, cut

# ---------------------------------------------------------------- string matching
def naive(T, P): return [s for s in range(len(T) - len(P) + 1) if T[s:s + len(P)] == P]
def rabin_karp(T, P, q=13, d=10):
    m = len(P); p = int(P) % q; hits = []
    for s in range(len(T) - m + 1):
        w = int(T[s:s + m]);
        if w % q == p: hits.append((s, T[s:s + m], T[s:s + m] == P))
    return p, hits
def fa_table(P, alpha):
    m = len(P); D = []
    for q in range(m + 1):
        row = {}
        for a in alpha:
            k = min(m, q + 1)
            while k > 0 and not (P[:q] + a).endswith(P[:k]): k -= 1
            row[a] = k
        D.append(row)
    return D
def prefix_fn(P):
    pi = [0] * len(P); k = 0
    for q in range(1, len(P)):
        while k and P[k] != P[q]: k = pi[k - 1]
        if P[k] == P[q]: k += 1
        pi[q] = k
    return pi
def kmp(T, P):
    pi, q, out = prefix_fn(P), 0, []
    for i, c in enumerate(T):
        while q and P[q] != c: q = pi[q - 1]
        if P[q] == c: q += 1
        if q == len(P): out.append(i - len(P) + 1); q = pi[q - 1]
    return out

# ---------------------------------------------------------------- approximation
VCG = [('a', 'b'), ('b', 'c'), ('c', 'd'), ('c', 'e'), ('d', 'e'), ('d', 'f'), ('d', 'g'), ('e', 'f')]
def approx_vc(E):
    E = list(E); C = []; picked = []
    while E:
        u, v = E[0]; C += [u, v]; picked.append((u, v)); E = [e for e in E if u not in e and v not in e]
    return C, picked
def min_vc(E):
    V = sorted({x for e in E for x in e})
    for k in range(1, len(V) + 1):
        for S in itertools.combinations(V, k):
            if all(u in S or v in S for u, v in E): return list(S)

# ---------------------------------------------------------------- other universities
def bloom_fp(m, n, k): return (1 - math.exp(-k * n / m)) ** k

if __name__ == '__main__':
    print('addr', addr(1000, 4, 10, 20, 5, 7), addr(1000, 4, 10, 20, 5, 7, 'col'))
    print('bsearch', bsearch_trace([3, 8, 12, 17, 25, 31, 42, 56, 63, 77], 42))
    print('postfix', to_postfix('A+B*C-D/E')); print('eval', eval_postfix('6 2 3 + - 3 8 2 / + *'))
    print('trav', pre(TREE, 'A'), ino(TREE, 'A'), post(TREE, 'A'), level(TREE, 'A'))
    print('bst', bst_insert([50, 30, 70, 20, 40, 60, 80]))
    print('bfs', bfs(UG, 'A'), 'dfs', dfs(UG, 'A'), 'topo', kahn(DAG))
    print('kruskal', kruskal('ABCDE', WG)); print('prim', prim('ABCDE', WG))
    d, pv, st = dijkstra('ABCDE', WG); print('dijkstra', d, {v: path(pv, v) for v in d})
    print('msort', merge_sort_levels([38, 27, 43, 3, 9, 82, 10]))
    print('partition', partition([2, 8, 7, 1, 3, 5, 6, 4])[:2])
    print('maxsub', max_subarray(STOCK)); print('strassen', strassen2([[1, 3], [7, 5]], [[6, 8], [4, 2]]))
    print('frac', frac_knap([(60, 10), (100, 20), (120, 30)], 50)); print('jobs', job_seq(JOBS))
    c, m, t = huffman(HUFF); print('huff', c, m, sum(HUFF[k] * len(v) for k, v in c.items()))
    K, pick = knap01([(2, 3), (3, 4), (4, 5), (5, 6)], 5); print('knap01', K[-1][-1], pick)
    print('rod', rod(ROD, 10)); print('mcm', matrix_chain([5, 4, 6, 2, 7])[0][1][4], matrix_chain([5, 4, 6, 2, 7])[2])
    print('lcs', lcs('ABCBDAB', 'BDCABA')[1]); print('obst', obst()); print('tsp', tsp_dp(TSP)[:2])
    print('4q', nqueens(4), len(nqueens(8))); print('colour', len(colourings(CG, 3)), colourings(CG, 3)[0], len(colourings(CG, 2)))
    r, snaps = btree_insert([10, 20, 5, 6, 12, 30, 7, 17]); [print('  bt', k, s) for k, s in snaps]
    for row in dsu_run(6, [(1, 2), (3, 4), (5, 6), (2, 4), (4, 6)]): print('  dsu', row)
    for kind in ('linear', 'quadratic', 'double'): print(kind, open_address(HK, 11, kind))
    print('H10', harmonic(10)); print('counter', counter_flips(16))
    print('johnson', johnson()); print('flow', edmonds_karp())
    print('naive', naive('acaabc', 'aab')); print('RK', rabin_karp('2359023141526739921', '31415'))
    print('FA', fa_table('ababaca', 'abc')); print('pi', prefix_fn('ababaca'), kmp('bacbababacaab', 'ababaca'))
    print('vc', approx_vc(VCG), min_vc(VCG)); print('bloom', bloom_fp(1000, 100, 7))
