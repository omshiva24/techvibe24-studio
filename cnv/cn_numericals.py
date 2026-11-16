'''Worked exam problems for the Computer Networks video, computed in code so every answer on screen is right.'''
import math, ipaddress, heapq

def fmt(x, nd=2):
    s = f'{x:.{nd}f}'.rstrip('0').rstrip('.'); return s

# ---------------------------------------------------------------- delays
def delays(L_bytes=1000, B=1e6, d=2000e3, v=2e8):
    Tt = L_bytes * 8 / B; Tp = d / v; return dict(Tt=Tt, Tp=Tp, total=Tt + Tp, bdp=B * Tp)

# ---------------------------------------------------------------- channel capacity
def nyquist(B, L): return 2 * B * math.log2(L)
def shannon(B, snr_db):
    snr = 10 ** (snr_db / 10); return snr, B * math.log2(1 + snr)

# ---------------------------------------------------------------- line coding: list of (level per half bit), +1 high / -1 low
def encode(bits, scheme):
    out = []; lvl = -1                          # NRZ-I and differential Manchester start low before the first bit
    for b in bits:
        b = int(b)
        if scheme == 'NRZ-L': out += [1 if b else -1] * 2
        elif scheme == 'NRZ-I':
            if b: lvl = -lvl
            out += [lvl] * 2
        elif scheme == 'Manchester': out += [-1, 1] if b else [1, -1]      # IEEE 802.3: 1 = low->high, 0 = high->low
        elif scheme == 'Diff Manchester':
            if b == 0: lvl = -lvl                                         # 0 = transition at the start, 1 = no transition
            out += [lvl, -lvl]; lvl = -lvl                                 # always a transition in the middle
    return out

# ---------------------------------------------------------------- framing
def bit_stuff(s):
    out = ''; run = 0
    for c in s:
        out += c; run = run + 1 if c == '1' else 0
        if run == 5: out += '0'; run = 0
    return out
def supernet(nets): return str(list(ipaddress.collapse_addresses([ipaddress.ip_network(n) for n in nets]))[0])

# ---------------------------------------------------------------- CRC (mod-2 long division)
def crc(data, gen):
    r = len(gen) - 1; cur = data + '0' * r; steps = []
    rem = cur[:len(gen)]; i = len(gen)
    while True:
        q = rem[0]; sub = gen if q == '1' else '0' * len(gen)
        x = ''.join('0' if a == b else '1' for a, b in zip(rem, sub))
        steps.append((rem, sub, x[1:], i - len(gen)))
        if i == len(cur): rem = x[1:]; break
        rem = x[1:] + cur[i]; i += 1
    return rem, data + rem, steps
def crc_check(code, gen):
    return crc(code[:-(len(gen) - 1)], gen)[0] == code[-(len(gen) - 1):]

# ---------------------------------------------------------------- Hamming (7,4), even parity, positions 1..7 = p1 p2 d1 p4 d2 d3 d4
def hamming74(d):
    d = [int(c) for c in d]; c = [0] * 8
    c[3], c[5], c[6], c[7] = d
    c[1] = c[3] ^ c[5] ^ c[7]; c[2] = c[3] ^ c[6] ^ c[7]; c[4] = c[5] ^ c[6] ^ c[7]
    return ''.join(map(str, c[1:]))
def syndrome(code):
    c = [0] + [int(x) for x in code]
    s1 = c[1] ^ c[3] ^ c[5] ^ c[7]; s2 = c[2] ^ c[3] ^ c[6] ^ c[7]; s4 = c[4] ^ c[5] ^ c[6] ^ c[7]
    return s4, s2, s1, s4 * 4 + s2 * 2 + s1

# ---------------------------------------------------------------- checksum (8-bit words, one's complement)
def checksum8(words):
    s = 0; trace = []
    for w in words:
        s += int(w, 2)
        while s > 0xFF: s = (s & 0xFF) + (s >> 8)
        trace.append(f'{s:08b}')
    return f'{s:08b}', f'{(~s) & 0xFF:08b}', trace

# ---------------------------------------------------------------- sliding window
def sliding(B=1e6, L_bits=1000, Tp=10e-3, W=7):
    Tt = L_bits / B; a = Tp / Tt; sw = 1 / (1 + 2 * a); gbn = min(1, W / (1 + 2 * a))
    need = 1 + 2 * a; k_gbn = math.ceil(math.log2(need + 1)); k_sr = math.ceil(math.log2(need)) + 1
    return dict(Tt=Tt, a=a, sw=sw, gbn=gbn, need=need, k_gbn=k_gbn, k_sr=k_sr)

# ---------------------------------------------------------------- ALOHA
def aloha(frame_bits=200, rate=200e3, fps=1000):
    T = frame_bits / rate; G = fps * T
    pure = G * math.exp(-2 * G); slotted = G * math.exp(-G)
    return dict(T=T, G=G, pure=pure, slotted=slotted, pure_fps=pure * fps / G if G else 0, slotted_fps=slotted / T)
def csmacd_min(B=10e6, d=2000, v=2e8): Tp = d / v; return Tp, 2 * Tp * B

# ---------------------------------------------------------------- IP addressing
def subnets(net='192.168.10.0/24', n=4):
    N = ipaddress.ip_network(net); k = math.ceil(math.log2(n)); out = []
    for s in N.subnets(prefixlen_diff=k):
        h = list(s.hosts()); out.append((str(s), str(s.network_address), str(h[0]), str(h[-1]), str(s.broadcast_address)))
    return k, str(N.subnets(prefixlen_diff=k).__next__().netmask), out
def host_info(cidr='172.16.45.14/20'):
    i = ipaddress.ip_interface(cidr); n = i.network
    return str(n.netmask), str(n.network_address), str(n.broadcast_address), n.num_addresses - 2, str(list(n.hosts())[0]), str(list(n.hosts())[-1])
def vlsm(net='192.168.1.0/24', needs=(100, 50, 25)):
    base = ipaddress.ip_network(net); cur = int(base.network_address); out = []
    for h in sorted(needs, reverse=True):
        p = 32 - math.ceil(math.log2(h + 2)); s = ipaddress.ip_network(f'{ipaddress.ip_address(cur)}/{p}')
        out.append((h, str(s), 2 ** (32 - p) - 2, str(s.broadcast_address))); cur += 2 ** (32 - p)
    return out

# ---------------------------------------------------------------- fragmentation
def fragment(total=4000, hdr=20, mtu=1500):
    data = total - hdr; per = (mtu - hdr) // 8 * 8; out = []; off = 0
    while data > 0:
        d = min(per, data); data -= d; out.append((d, d + hdr, off // 8, 1 if data > 0 else 0)); off += d
    return per, out

# ---------------------------------------------------------------- routing
G = {'A': {'B': 4, 'C': 2}, 'B': {'A': 4, 'C': 1, 'D': 5}, 'C': {'A': 2, 'B': 1, 'D': 8, 'E': 10}, 'D': {'B': 5, 'C': 8, 'E': 2}, 'E': {'C': 10, 'D': 2}}
def dijkstra(g=G, s='A'):
    dist = {v: math.inf for v in g}; prev = {v: None for v in g}; dist[s] = 0; done = []; steps = []
    while len(done) < len(g):
        u = min((v for v in g if v not in done), key=lambda v: (dist[v], v)); done.append(u)
        for v, w in g[u].items():
            if v not in done and dist[u] + w < dist[v]: dist[v] = dist[u] + w; prev[v] = u
        steps.append((''.join(done), {v: (dist[v], prev[v]) for v in g if v != s}))
    return dist, prev, steps
def path(prev, t):
    p = [t]
    while prev[p[-1]]: p.append(prev[p[-1]])
    return '-'.join(reversed(p))
def dv_update(costs={'B': 1, 'C': 4}, vectors={'B': {'A': 1, 'B': 0, 'C': 2, 'D': 6}, 'C': {'A': 4, 'B': 2, 'C': 0, 'D': 1}}, me='A'):
    dests = ['A', 'B', 'C', 'D']; out = []
    for t in dests:
        if t == me: out.append((t, 0, '-', '')); continue
        opts = {n: costs[n] + vectors[n][t] for n in costs}; n = min(opts, key=opts.get)
        out.append((t, opts[n], n, ', '.join(f'{costs[k]}+{vectors[k][t]}' for k in costs)))
    return out

# ---------------------------------------------------------------- TCP congestion (Tahoe-style: timeout -> ssthresh = cwnd/2, cwnd = 1)
def tcp_cwnd(ssthresh=16, rounds=14, loss_at=None):
    cw = 1; th = ssthresh; out = []
    for r in range(1, rounds + 1):
        out.append(cw)
        if loss_at and r == loss_at: th = cw // 2; cw = 1; continue
        cw = min(cw * 2, th) if cw < th else cw + 1
    return out

# ---------------------------------------------------------------- token bucket
def token_bucket(C=1e6, rho=2e6, M=10e6): S = C / (M - rho); return S, M * S

# ---------------------------------------------------------------- RSA
def rsa(p=3, q=11, e=7, m=4):
    n = p * q; phi = (p - 1) * (q - 1); d = pow(e, -1, phi); c = pow(m, e, n)
    return dict(n=n, phi=phi, d=d, c=c, back=pow(c, d, n))

if __name__ == '__main__':
    print('delays', delays())
    print('nyquist', nyquist(3000, 2), nyquist(3000, 4), 'shannon', shannon(3000, 30))
    for s in ('NRZ-L', 'NRZ-I', 'Manchester', 'Diff Manchester'): print(s, encode('01001110', s))
    r, code, st = crc('100100', '1101'); print('crc', r, code, crc_check(code, '1101'), crc_check('100100011', '1101'))
    for x in st: print('   ', x)
    h = hamming74('1011'); bad = h[:4] + str(1 - int(h[4])) + h[5:]; print('hamming', h, bad, syndrome(bad), syndrome(h))
    print('checksum', checksum8(['10110011', '10101011', '01011010', '11010101']))
    print('sliding', sliding())
    print('aloha', aloha(), aloha(fps=500), aloha(fps=250)); print('csmacd', csmacd_min())
    print('subnets', subnets()); print('host', host_info()); print('vlsm', vlsm())
    print('frag', fragment())
    d, p, st = dijkstra(); print('dijkstra', d, {v: path(p, v) for v in d}); [print('   ', x) for x in st]
    print('dv', dv_update())
    print('tcp', tcp_cwnd(16, 14, loss_at=None), tcp_cwnd(16, 14, loss_at=10))
    print('token', token_bucket()); print('rsa', rsa())
