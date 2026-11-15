'''Worked exam problems for the DBMS video, computed in code so every answer on screen is right.'''
import itertools, math, sqlite3

# ---------------------------------------------------------------- functional dependencies
def fd(s):
    '''"A->B, CG->H" -> [(set('A'), set('B')), ...]  (single-letter attributes)'''
    out = []
    for part in s.split(','):
        l, r = part.split('->'); out.append((frozenset(l.strip()), frozenset(r.strip())))
    return out
def closure(X, F):
    X = set(X); steps = []; changed = True
    while changed:
        changed = False
        for l, r in F:
            if l <= X and not r <= X: X |= r; steps.append((''.join(sorted(l)), ''.join(sorted(r)), ''.join(sorted(X)))); changed = True
    return X, steps
def candidate_keys(R, F):
    R = set(R); keys = []
    for n in range(1, len(R) + 1):
        for c in itertools.combinations(sorted(R), n):
            if any(set(k) <= set(c) for k in keys): continue
            if closure(c, F)[0] == R: keys.append(''.join(c))
    return keys
def superkeys(R, F):
    return [''.join(c) for n in range(1, len(R) + 1) for c in itertools.combinations(sorted(R), n) if closure(c, F)[0] == set(R)]
def canonical_cover(F):
    G = [(l, frozenset([a])) for l, r in F for a in sorted(r)]
    G = list(dict.fromkeys(G))
    changed = True
    while changed:                                   # remove extraneous left attributes
        changed = False
        for i, (l, r) in enumerate(G):
            for a in sorted(l):
                if len(l) > 1 and r <= closure(l - {a}, G)[0]: G[i] = (l - {a}, r); changed = True; break
    G = list(dict.fromkeys(G)); i = 0
    while i < len(G):                                # remove redundant dependencies
        rest = G[:i] + G[i + 1:]
        if G[i][1] <= closure(G[i][0], rest)[0]: G = rest
        else: i += 1
    merged = {}
    for l, r in G: merged.setdefault(l, set()).update(r)
    return [(l, frozenset(r)) for l, r in merged.items()]
def fd_str(F): return ', '.join(f"{''.join(sorted(l))} -> {''.join(sorted(r))}" for l, r in F)
def normal_form(R, F):
    keys = [set(k) for k in candidate_keys(R, F)]; prime = set().union(*keys)
    single = [(l, frozenset([a])) for l, r in F for a in r if a not in l]
    bcnf = all(closure(l, F)[0] == set(R) for l, r in single)
    nf3 = all(closure(l, F)[0] == set(R) or r <= prime for l, r in single)
    nf2 = not any(r - prime and any(l < k for k in keys) for l, r in single)
    return 'BCNF' if bcnf else '3NF' if nf3 else '2NF' if nf2 else '1NF'

# ---------------------------------------------------------------- serializability
def precedence(schedule):
    '''schedule like "R1(X) R2(Z) W1(X)" -> edges {(Ti, Tj): item}'''
    ops = [(o[0], int(o[1]), o[3]) for o in schedule.split()]
    edges = {}
    for i, (a, t, x) in enumerate(ops):
        for b, u, y in ops[i + 1:]:
            if t != u and x == y and 'W' in (a, b): edges.setdefault((t, u), x)
    return ops, edges
def topo(nodes, edges):
    nodes = sorted(nodes); indeg = {n: 0 for n in nodes}
    for a, b in edges: indeg[b] += 1
    order = []; avail = [n for n in nodes if indeg[n] == 0]
    while avail:
        n = avail.pop(0); order.append(n)
        for a, b in sorted(edges):
            if a == n:
                indeg[b] -= 1
                if indeg[b] == 0: avail.append(b)
    return order if len(order) == len(nodes) else None

# ---------------------------------------------------------------- indexing
def bplus_order(B, V, P, Pr):
    p = (B + V) // (P + V)                 # p*P + (p-1)*V <= B
    pl = (B - P) // (V + Pr)               # pl*(V+Pr) + P <= B
    return p, pl
def index_example(r=30000, B=1024, R=100, V=9, P=6):
    bfr = B // R; b = math.ceil(r / bfr); lin = b // 2; binary = math.ceil(math.log2(b))
    Ri = V + P; bfri = B // Ri; bi = math.ceil(b / bfri); idx = math.ceil(math.log2(bi)) + 1
    return dict(bfr=bfr, b=b, lin=lin, binary=binary, Ri=Ri, bfri=bfri, bi=bi, idx=idx)

class BPT:
    '''B+ tree, max `m` keys per node; leaves split as ceil/floor, middle key copied up (leaf) or moved up (internal).'''
    def __init__(self, m): self.m = m; self.root = {'leaf': True, 'keys': []}
    def insert(self, k):
        r = self._ins(self.root, k)
        if r: sep, right = r; self.root = {'leaf': False, 'keys': [sep], 'kids': [self.root, right]}
    def _ins(self, n, k):
        if n['leaf']:
            n['keys'] = sorted(n['keys'] + [k])
            if len(n['keys']) <= self.m: return None
            h = (len(n['keys']) + 1) // 2; right = {'leaf': True, 'keys': n['keys'][h:]}; n['keys'] = n['keys'][:h]
            return right['keys'][0], right
        i = sum(k >= s for s in n['keys']); r = self._ins(n['kids'][i], k)
        if not r: return None
        sep, right = r; n['keys'].insert(i, sep); n['kids'].insert(i + 1, right)
        if len(n['keys']) <= self.m: return None
        h = len(n['keys']) // 2; up = n['keys'][h]
        rn = {'leaf': False, 'keys': n['keys'][h + 1:], 'kids': n['kids'][h + 1:]}; n['keys'] = n['keys'][:h]; n['kids'] = n['kids'][:h + 1]
        return up, rn
    def levels(self):
        out, lvl = [], [self.root]
        while lvl:
            out.append([n['keys'] for n in lvl]); lvl = [c for n in lvl if not n['leaf'] for c in n['kids']]
        return out
    def shape(self):
        '''levels with child counts, for drawing'''
        out, lvl = [], [self.root]
        while lvl:
            out.append([(n['keys'], 0 if n['leaf'] else len(n['kids'])) for n in lvl]); lvl = [c for n in lvl if not n['leaf'] for c in n['kids']]
        return out

# ---------------------------------------------------------------- relational algebra + SQL on small tables (sqlite)
EMP = [(1, 'Asha', 'CSE', 60000), (2, 'Ravi', 'CSE', 45000), (3, 'Meena', 'ECE', 52000), (4, 'Kiran', 'ECE', 38000),
       (5, 'Arun', 'MECH', 41000), (6, 'Divya', 'CSE', 70000)]
DEPT = [('CSE', 'Block A'), ('ECE', 'Block B'), ('MECH', 'Block C'), ('CIVIL', 'Block D')]
ENROLL = [('S1', 'DBMS'), ('S1', 'OS'), ('S1', 'CN'), ('S2', 'DBMS'), ('S2', 'OS'), ('S3', 'DBMS'), ('S3', 'OS'), ('S3', 'CN'), ('S4', 'CN')]
COURSE = [('DBMS',), ('OS',), ('CN',)]
def db():
    c = sqlite3.connect(':memory:')
    c.execute('create table Emp(eid int, name text, dept text, salary int)'); c.executemany('insert into Emp values (?,?,?,?)', EMP)
    c.execute('create table Dept(dname text, block text)'); c.executemany('insert into Dept values (?,?)', DEPT)
    c.execute('create table Enroll(sid text, cid text)'); c.executemany('insert into Enroll values (?,?)', ENROLL)
    c.execute('create table Course(cid text)'); c.executemany('insert into Course values (?)', COURSE)
    return c
def q(sql): return db().execute(sql).fetchall()
def division():
    cs = {c for (c,) in COURSE}; by = {}
    for s, c in ENROLL: by.setdefault(s, set()).add(c)
    return sorted(s for s, v in by.items() if cs <= v)

def linear_probe(keys, m):
    T = [None] * m; probes = []
    for k in keys:
        h = k % m; i = h; n = 0
        while T[i] is not None: i = (i + 1) % m; n += 1
        T[i] = k; probes.append((k, h, i, n))
    return T, probes

if __name__ == '__main__':
    print('probe', linear_probe([10, 22, 31, 4, 15, 28, 17, 88, 59], 11))
    F = fd('A->B, A->C, CG->H, CG->I, B->H'); X, st = closure('AG', F); print('(AG)+', ''.join(sorted(X)), st)
    print('keys ABCGHI', candidate_keys('ABCGHI', F))
    F2 = fd('A->B, BC->E, ED->A'); print('keys ABCDE', candidate_keys('ABCDE', F2), normal_form('ABCDE', F2))
    F3 = fd('A->B'); print('superkeys of R(A,B,C,D) with key A only:', len(superkeys('ABCD', fd('A->BCD'))))
    F4 = fd('A->BCD, BC->AD'); print('keys', candidate_keys('ABCD', F4), 'superkeys', len(superkeys('ABCD', F4)))
    print('canon', fd_str(canonical_cover(fd('A->BC, B->C, A->B, AB->C'))))
    print('NF AB->C,C->B', candidate_keys('ABC', fd('AB->C, C->B')), normal_form('ABC', fd('AB->C, C->B')))
    print('NF R(ABCD) AB->C, C->D', candidate_keys('ABCD', fd('AB->C, C->D')), normal_form('ABCD', fd('AB->C, C->D')))
    print('NF R(ABCD) AB->C, A->D', candidate_keys('ABCD', fd('AB->C, A->D')), normal_form('ABCD', fd('AB->C, A->D')))
    S = 'R1(X) R2(Z) R1(Z) R3(X) R3(Y) W1(X) W3(Y) R2(Y) W2(Z) W2(Y)'; ops, E = precedence(S); print('edges', E, topo({1, 2, 3}, E))
    ops, E = precedence('R1(A) R2(A) W1(A) W2(A)'); print('edges', E, topo({1, 2}, E))
    print('B+ order', bplus_order(512, 9, 6, 7)); print('index', index_example())
    t = BPT(3)
    for k in [1, 4, 7, 10, 17, 21, 31, 25, 19, 20, 28, 42]: t.insert(k)
    print('B+', t.levels())
    print(q('select dept, count(*), avg(salary) from Emp group by dept having count(*) >= 2 order by dept'))
    print(q('select max(salary) from Emp where salary < (select max(salary) from Emp)'))
    print(q('select e.name, d.block from Emp e join Dept d on e.dept = d.dname where e.salary > 50000 order by e.eid'))
    print(q('select d.dname, e.name from Dept d left join Emp e on e.dept = d.dname where e.name is null'))
    print('division', division())
