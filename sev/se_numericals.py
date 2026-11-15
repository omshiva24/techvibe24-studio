'''Worked exam problems for the Software Engineering video, computed in code so every answer on screen is right.'''
import math

# ---------------------------------------------------------------- COCOMO
BASIC = {'Organic': (2.4, 1.05, 2.5, 0.38), 'Semi-detached': (3.0, 1.12, 2.5, 0.35), 'Embedded': (3.6, 1.20, 2.5, 0.32)}
INTER = {'Organic': (3.2, 1.05), 'Semi-detached': (3.0, 1.12), 'Embedded': (2.8, 1.20)}
def cocomo_basic(kloc, mode):
    a, b, c, d = BASIC[mode]; E = a * kloc ** b; D = c * E ** d
    return dict(E=E, D=D, staff=E / D, prod=kloc * 1000 / E)
def cocomo_inter(kloc, mode, eaf):
    a, b = INTER[mode]; nom = a * kloc ** b; return nom, nom * eaf

# ---------------------------------------------------------------- function points
FP_W = {'EI': (3, 4, 6), 'EO': (4, 5, 7), 'EQ': (3, 4, 6), 'ILF': (7, 10, 15), 'EIF': (5, 7, 10)}
def function_points(counts, level=1, fi_sum=42):
    ufp = sum(n * FP_W[k][level] for k, n in counts.items()); caf = 0.65 + 0.01 * fi_sum
    return ufp, caf, ufp * caf

# ---------------------------------------------------------------- Halstead
def halstead(n1, n2, N1, N2):
    n = n1 + n2; N = N1 + N2; Nh = n1 * math.log2(n1) + n2 * math.log2(n2); V = N * math.log2(n)
    D = (n1 / 2) * (N2 / n2); E = D * V
    return dict(n=n, N=N, Nh=Nh, V=V, D=D, L=1 / D, E=E, T=E / 18)

# ---------------------------------------------------------------- cyclomatic complexity (GCD by subtraction)
CFG_NODES = [1, 2, 3, 4, 5, 6, 7]
CFG_EDGES = [(1, 2), (2, 3), (2, 7), (3, 4), (3, 5), (4, 6), (5, 6), (6, 2)]
def cyclomatic(nodes=CFG_NODES, edges=CFG_EDGES):
    N, E = len(nodes), len(edges); out = {}
    for a, b in edges: out.setdefault(a, []).append(b)
    pred = sum(1 for v in out.values() if len(v) == 2)
    return dict(N=N, E=E, V=E - N + 2, P=pred, Vp=pred + 1)
def basis_paths():
    return ['1-2-7', '1-2-3-4-6-2-7', '1-2-3-5-6-2-7']

# ---------------------------------------------------------------- CPM
ACT = [('A', 3, []), ('B', 4, []), ('C', 2, ['A']), ('D', 6, ['A']), ('E', 3, ['B', 'C']), ('F', 2, ['D', 'E'])]
def cpm(acts=ACT):
    es, ef = {}, {}
    for a, d, pre in acts:
        es[a] = max([ef[p] for p in pre], default=0); ef[a] = es[a] + d
    T = max(ef.values()); lf, ls = {}, {}
    for a, d, pre in reversed(acts):
        succ = [s for s, _, ps in acts if a in ps]
        lf[a] = min([ls[s] for s in succ], default=T); ls[a] = lf[a] - d
    rows = [(a, d, es[a], ef[a], ls[a], lf[a], ls[a] - es[a]) for a, d, _ in acts]
    return T, rows
def pert(a, m, b):
    te = (a + 4 * m + b) / 6; sd = (b - a) / 6; return te, sd, sd * sd

# ---------------------------------------------------------------- testing
def bva(lo, hi, robust=False):
    nom = (lo + hi) // 2; v = [lo, lo + 1, nom, hi - 1, hi]
    return ([lo - 1] if robust else []) + v + ([hi + 1] if robust else [])
def bva_two(xr, yr):
    xn = (xr[0] + xr[1]) // 2; yn = (yr[0] + yr[1]) // 2
    cases = [(x, yn) for x in (xr[0], xr[0] + 1, xr[1] - 1, xr[1])] + [(xn, y) for y in (yr[0], yr[0] + 1, yr[1] - 1, yr[1])] + [(xn, yn)]
    return cases

# ---------------------------------------------------------------- reliability & risk
def availability(mttf, mttr): return mttf + mttr, mttf / (mttf + mttr)
def risk_exposure(p, cost): return p * cost

if __name__ == '__main__':
    for m in BASIC: r = cocomo_basic(400, m); print(m, {k: round(v, 2) for k, v in r.items()})
    print('inter', cocomo_inter(32, 'Organic', 1.15 * 0.86))
    print('FP', function_points({'EI': 50, 'EO': 40, 'EQ': 35, 'ILF': 6, 'EIF': 4}))
    print('Halstead', {k: round(v, 2) for k, v in halstead(10, 8, 40, 30).items()})
    print('cyclo', cyclomatic())
    print('cpm', cpm()); print('pert', pert(2, 4, 12))
    print('bva', bva(1, 100), bva(1, 100, True), bva_two((1, 100), (1, 200)))
    print('avail', availability(500, 20)); print('RE', risk_exposure(0.4, 200000))
