'''Worked exam problems for the Mathematical Foundations of Computer Science video, computed in code so every answer on screen is right.'''
import itertools, math
from math import comb, factorial, gcd

# ---------------------------------------------------------------- logic
OPS = {'¬': lambda a: not a}
def truth_table(fn, names='pq'):
    return [(vals, fn(*vals)) for vals in itertools.product([True, False], repeat=len(names))]
TF = lambda b: 'T' if b else 'F'
def normal_forms(fn, names='pqr'):
    mins, maxs = [], []
    for vals in itertools.product([False, True], repeat=len(names)):
        lit_min = ' ∧ '.join(n if v else '¬' + n for n, v in zip(names, vals))
        lit_max = ' ∨ '.join('¬' + n if v else n for n, v in zip(names, vals))
        (mins if fn(*vals) else maxs).append(('(' + lit_min + ')', '(' + lit_max + ')', ''.join('1' if v else '0' for v in vals)))
    return mins, maxs

# ---------------------------------------------------------------- sets & functions
def venn3(total=100, a=45, b=40, c=35, ab=15, bc=10, ac=12, abc=5):
    union = a + b + c - ab - bc - ac + abc
    only = dict(a=a - ab - ac + abc, b=b - ab - bc + abc, c=c - ac - bc + abc, ab=ab - abc, bc=bc - abc, ac=ac - abc, abc=abc)
    return union, total - union, only
def onto_count(m, n): return sum((-1) ** k * comb(n, k) * (n - k) ** m for k in range(n + 1))

# ---------------------------------------------------------------- relations
def props(R, A):
    S = set(R)
    refl = all((a, a) in S for a in A); sym = all((b, a) in S for a, b in S)
    anti = all(not ((b, a) in S and a != b) for a, b in S); trans = all((a, d) in S for a, b in S for c, d in S if b == c)
    return dict(reflexive=refl, symmetric=sym, antisymmetric=anti, transitive=trans)
def warshall(R, A):
    n = len(A); idx = {a: i for i, a in enumerate(A)}; W = [[0] * n for _ in range(n)]
    for a, b in R: W[idx[a]][idx[b]] = 1
    steps = [[r[:] for r in W]]
    for k in range(n):
        for i in range(n):
            for j in range(n): W[i][j] = W[i][j] or (W[i][k] and W[k][j])
        steps.append([r[:] for r in W])
    return steps
def hasse(n=12):
    D = [d for d in range(1, n + 1) if n % d == 0]
    return D, [(a, b) for a in D for b in D if a != b and b % a == 0 and not any(c not in (a, b) and c % a == 0 and b % c == 0 for c in D)]

# ---------------------------------------------------------------- matrices
def matmul(A, B): return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def bool_prod(A, B): return [[int(any(A[i][k] and B[k][j] for k in range(len(B)))) for j in range(len(B[0]))] for i in range(len(A))]

# ---------------------------------------------------------------- number theory
def divmod_pos(a, d): q = a // d; return q, a - d * q
def to_base(n, b):
    digs = '0123456789ABCDEF'; s = ''; steps = []
    while n: steps.append((n, n // b, n % b)); s = digs[n % b] + s; n //= b
    return s, steps
def mod_exp(b, n, m):
    x = 1; power = b % m; rows = []
    for i, bit in enumerate(reversed(bin(n)[2:])):
        if bit == '1': x = x * power % m
        rows.append((i, bit, x, power)); power = power * power % m
    return x, rows
def euclid(a, b):
    steps = []
    while b: steps.append((a, b, a // b, a % b)); a, b = b, a % b
    return a, steps
def ext_gcd(a, b):
    if b == 0: return a, 1, 0
    g, x, y = ext_gcd(b, a % b); return g, y, x - (a // b) * y
def inverse(a, m): return pow(a, -1, m)
def crt(rs, ms):
    M = math.prod(ms); x = 0; parts = []
    for r, m in zip(rs, ms):
        Mi = M // m; yi = pow(Mi, -1, m); parts.append((r, m, Mi, yi)); x += r * Mi * yi
    return x % M, M, parts
def factorize(n):
    f = []; d = 2
    while d * d <= n:
        while n % d == 0: f.append(d); n //= d
        d += 1
    if n > 1: f.append(n)
    return f
def sieve(n): return [p for p in range(2, n + 1) if all(p % q for q in range(2, int(p ** .5) + 1))]

# ---------------------------------------------------------------- sequences & recursion
def rec_f(n): v = [3]; [v.append(2 * v[-1] + 3) for _ in range(n)]; return v
def postage(lo=12, hi=21):
    out = {}
    for amt in range(lo, hi + 1):
        for b in range(amt // 5 + 1):
            if (amt - 5 * b) % 4 == 0: out[amt] = ((amt - 5 * b) // 4, b); break
    return out

# ---------------------------------------------------------------- counting
def multiset_perm(word):
    from collections import Counter
    c = Counter(word); return factorial(len(word)) // math.prod(factorial(v) for v in c.values()), c
def incl_excl_div(N=1000, ds=(3, 5, 7)):
    singles = [N // d for d in ds]; pairs = [N // (a * b) for a, b in itertools.combinations(ds, 2)]; trip = N // math.prod(ds)
    return singles, pairs, trip, sum(singles) - sum(pairs) + trip
def brute_div(N=1000, ds=(3, 5, 7)): return sum(1 for k in range(1, N + 1) if any(k % d == 0 for d in ds))
def derange(n): return round(factorial(n) * sum((-1) ** k / factorial(k) for k in range(n + 1)))

# ---------------------------------------------------------------- recurrences
def run_rec(c1, c2, a0, a1, n=6, f=lambda n: 0):
    a = [a0, a1]
    for k in range(2, n): a.append(c1 * a[-1] + c2 * a[-2] + f(k))
    return a

# ---------------------------------------------------------------- groups
def cayley(n=4): return [[(a + b) % n for b in range(n)] for a in range(n)]
def subgroups_zn(n): return [sorted({(k * g) % n for k in range(n)}) for g in sorted({gcd(n, g) for g in range(n)}, reverse=True)]

# ---------------------------------------------------------------- graphs
def kruskal(V, E):
    parent = {v: v for v in V}
    def find(v):
        while parent[v] != v: v = parent[v]
        return v
    out = []
    for w, a, b in sorted(E):
        ra, rb = find(a), find(b)
        out.append((a, b, w, ra != rb))
        if ra != rb: parent[ra] = rb
    return out
def bfs(G, s):
    seen = [s]; q = [s]
    while q:
        u = q.pop(0)
        for v in G[u]:
            if v not in seen: seen.append(v); q.append(v)
    return seen
def dfs(G, s, seen=None):
    seen = seen if seen is not None else []
    seen.append(s)
    for v in G[s]:
        if v not in seen: dfs(G, v, seen)
    return seen

if __name__ == '__main__':
    print('mp taut', all(r for _, r in truth_table(lambda p, q: (not (p and ((not p) or q))) or q)))
    mins, maxs = normal_forms(lambda p, q, r: (p and q) or ((not p) and r)); print('PDNF', [m[2] for m in mins], 'PCNF', [m[2] for m in maxs])
    print('venn', venn3()); print('onto 4->3', onto_count(4, 3), 3 ** 4)
    R = [(1, 1), (1, 2), (2, 1), (2, 2), (3, 3)]; print('props', props(R, [1, 2, 3]))
    for W in warshall([(1, 2), (2, 3), (3, 4), (2, 1)], [1, 2, 3, 4]): print('   W', W)
    print('hasse', hasse(12))
    A = [[1, 2, 0], [0, 1, 3]]; B = [[2, 1], [1, 0], [0, 4]]; print('AB', matmul(A, B))
    Z1 = [[1, 0, 1], [0, 1, 0]]; Z2 = [[1, 0], [0, 1], [1, 0]]; print('bool', bool_prod(Z1, Z2))
    print('div', divmod_pos(101, 11), divmod_pos(-11, 3), -133 % 9)
    print('base', to_base(241, 2), to_base(12345, 8)[0], to_base(241, 16)[0])
    print('modexp', mod_exp(3, 644, 645))
    print('euclid', euclid(662, 414), 414 * 662 // 2, 'ext', ext_gcd(252, 198), 'inv', inverse(3, 7), (inverse(3, 7) * 4) % 7)
    print('crt', crt([2, 3, 2], [3, 5, 7])); print('fermat', pow(7, 222, 11)); print('factor', factorize(999), factorize(100), sieve(50))
    print('sum k^2 50..100', sum(k * k for k in range(50, 101)))
    print('rec', rec_f(4), 'postage', postage())
    print('banana', multiset_perm('BANANA')[0], 'committee', comb(6, 3) * comb(5, 2), 'stars', comb(12, 2), 'coef', comb(5, 3) * 2 ** 3 * 3 ** 2, comb(8, 5))
    print('ie', incl_excl_div(), brute_div(), 'D4', derange(4), 'pigeon', math.ceil(100 / 12))
    print('rec1', run_rec(5, -6, 1, 4), [2 * 3 ** n - 2 ** n for n in range(6)])
    print('rec2', run_rec(6, -9, 1, 6), [(1 + n) * 3 ** n for n in range(6)])
    a = [2]; [a.append(3 * a[-1] + 2 ** k) for k in range(1, 6)]; print('rec3', a, [3 ** (n + 1) - 2 ** (n + 1) for n in range(6)])
    print('cayley', cayley(), subgroups_zn(4))
    E = [(4, 'A', 'B'), (2, 'A', 'C'), (1, 'B', 'C'), (5, 'B', 'D'), (8, 'C', 'D'), (10, 'C', 'E'), (2, 'D', 'E'), (6, 'B', 'E')]
    print('kruskal', kruskal('ABCDE', E))
    G = {'A': ['B', 'C'], 'B': ['A', 'D', 'E'], 'C': ['A', 'F'], 'D': ['B'], 'E': ['B', 'F'], 'F': ['C', 'E']}; print('bfs', bfs(G, 'A'), 'dfs', dfs(G, 'A'))
