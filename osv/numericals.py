'''Worked exam problems for the OS video, computed (not typed by hand) so every number on screen is right.'''
PROCS = [('P1', 0, 5), ('P2', 1, 3), ('P3', 2, 1), ('P4', 3, 2)]   # name, arrival, burst

def fcfs(ps):
    t, segs = 0, []
    for n, a, b in sorted(ps, key=lambda p: (p[1], p[0])):
        t = max(t, a); segs.append((n, t, t + b)); t += b
    return segs
def sjf(ps):
    t, segs, left = 0, [], list(ps)
    while left:
        ready = [p for p in left if p[1] <= t]
        if not ready: t = min(p[1] for p in left); continue
        p = min(ready, key=lambda p: (p[2], p[1])); segs.append((p[0], t, t + p[2])); t += p[2]; left.remove(p)
    return segs
def rr(ps, q):
    ps = sorted(ps, key=lambda p: p[1]); rem = {p[0]: p[2] for p in ps}; t = 0; i = 0; queue = []; segs = []
    while i < len(ps) and ps[i][1] <= t: queue.append(ps[i][0]); i += 1
    while queue or i < len(ps):
        if not queue: t = ps[i][1]; queue.append(ps[i][0]); i += 1; continue
        n = queue.pop(0); run = min(q, rem[n]); segs.append((n, t, t + run)); t += run; rem[n] -= run
        while i < len(ps) and ps[i][1] <= t: queue.append(ps[i][0]); i += 1   # new arrivals join before the preempted one
        if rem[n]: queue.append(n)
    merged = []
    for s in segs:
        if merged and merged[-1][0] == s[0] and merged[-1][2] == s[1]: merged[-1] = (s[0], merged[-1][1], s[2])
        else: merged.append(s)
    return merged
def results(ps, segs):
    ct = {}
    for n, s, e in segs: ct[n] = e
    rows = []
    for n, a, b in ps:
        tat = ct[n] - a; wt = tat - b; rows.append((n, a, b, ct[n], tat, wt))
    return rows, sum(r[4] for r in rows) / len(rows), sum(r[5] for r in rows) / len(rows)

# Banker's algorithm (classic 5 processes, resources A=10 B=5 C=7)
ALLOC = [(0, 1, 0), (2, 0, 0), (3, 0, 2), (2, 1, 1), (0, 0, 2)]
MAX = [(7, 5, 3), (3, 2, 2), (9, 0, 2), (2, 2, 2), (4, 3, 3)]
AVAIL = (3, 3, 2)
NEED = [tuple(m - a for m, a in zip(mx, al)) for mx, al in zip(MAX, ALLOC)]
def bankers():
    work = list(AVAIL); done = [False] * 5; seq = []; steps = []; i = 0; idle = 0
    while len(seq) < 5 and idle < 5:          # keep scanning P0..P4 in a circle (textbook order)
        if not done[i] and all(n <= w for n, w in zip(NEED[i], work)):
            before = tuple(work); work = [w + a for w, a in zip(work, ALLOC[i])]; done[i] = True; seq.append(i)
            steps.append((i, NEED[i], before, tuple(work))); idle = 0
        else: idle += 1
        i = (i + 1) % 5
    return (seq if len(seq) == 5 else None), steps

# memory placement (classic textbook question)
PARTS = [100, 500, 200, 300, 600]; JOBS = [212, 417, 112, 426]
def place(kind):
    holes = list(PARTS); out = []
    for j in JOBS:
        fits = [(i, h) for i, h in enumerate(holes) if h >= j]
        if not fits: out.append((j, None, None)); continue
        i = fits[0][0] if kind == 'first' else min(fits, key=lambda x: x[1])[0] if kind == 'best' else max(fits, key=lambda x: x[1])[0]
        out.append((j, i, holes[i])); holes[i] -= j
    return out

# page replacement (classic reference string, 3 frames)
REF = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]
def replace(ref, nf, kind):
    frames, hist, faults, last, order = [None] * nf, [], [], {}, []
    for k, p in enumerate(ref):
        if p in frames:
            faults.append(False)
        else:
            faults.append(True)
            if None in frames: slot = frames.index(None)
            elif kind == 'fifo': slot = frames.index(order[0])
            elif kind == 'lru': slot = min(range(nf), key=lambda s: last[frames[s]])
            else:
                def nxt(q):
                    try: return ref.index(q, k + 1)
                    except ValueError: return 10 ** 9
                slot = max(range(nf), key=lambda s: nxt(frames[s]))
            if frames[slot] is not None: order.remove(frames[slot])
            frames[slot] = p; order.append(p)
        last[p] = k; hist.append(list(frames))
    return hist, faults

# disk scheduling
QUEUE = [98, 183, 37, 122, 14, 124, 65, 67]; HEAD = 53; MAXCYL = 199
def total(path): return sum(abs(b - a) for a, b in zip(path, path[1:]))
def d_fcfs(): return [HEAD] + QUEUE
def d_sstf():
    left, cur, path = list(QUEUE), HEAD, [HEAD]
    while left: nxt = min(left, key=lambda c: abs(c - cur)); left.remove(nxt); path.append(nxt); cur = nxt
    return path
def d_scan_down(): lo = sorted([c for c in QUEUE if c < HEAD], reverse=True); hi = sorted(c for c in QUEUE if c > HEAD); return [HEAD] + lo + [0] + hi
def d_look_down(): lo = sorted([c for c in QUEUE if c < HEAD], reverse=True); hi = sorted(c for c in QUEUE if c > HEAD); return [HEAD] + lo + hi
def d_cscan_up(): hi = sorted(c for c in QUEUE if c > HEAD); lo = sorted(c for c in QUEUE if c < HEAD); return [HEAD] + hi + [MAXCYL, 0] + lo
def d_clook_up(): hi = sorted(c for c in QUEUE if c > HEAD); lo = sorted(c for c in QUEUE if c < HEAD); return [HEAD] + hi + lo

if __name__ == '__main__':
    for name, f in (('FCFS', fcfs), ('SJF', sjf)):
        s = f(PROCS); print(name, s, results(PROCS, s))
    s = rr(PROCS, 2); print('RR2', s, results(PROCS, s))
    print('need', NEED, 'bankers', bankers())
    for k in ('first', 'best', 'worst'): print(k, place(k))
    for k in ('fifo', 'opt', 'lru'): print(k, sum(replace(REF, 3, k)[1]))
    print('belady', sum(replace([1,2,3,4,1,2,5,1,2,3,4,5], 3, 'fifo')[1]), sum(replace([1,2,3,4,1,2,5,1,2,3,4,5], 4, 'fifo')[1]))
    for f in (d_fcfs, d_sstf, d_scan_down, d_look_down, d_cscan_up, d_clook_up): print(f.__name__, f(), total(f()))
    print('EAT', 0.8 * (20 + 100) + 0.2 * (20 + 200))
