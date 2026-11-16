'''YouTube chapters + English subtitles (SRT) from the final timeline.   python cnv/gen_meta.py OUT_DIR'''
import json, os, re, sys, textwrap
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
tl = json.load(open(f'{HERE}/build/tl.json'))
def ts(t): return '%d:%02d:%02d' % (t // 3600, t % 3600 // 60, t % 60) if t >= 3600 else '%d:%02d' % (t // 60, t % 60)
chap = ['0:00 Introduction & contents']
for pg in tl['pages']:
    if pg['kind'] == 'chapter': chap.append(f"{ts(int(pg['t0']))} Ch {pg['num']}: {pg['title']}")
    NUM = {'The OSI Model': 'OSI model', 'TCP/IP Model vs OSI': 'TCP/IP vs OSI', 'Network Devices': 'Network devices', 'Delays in a Network': 'Delays (numerical)',
           'Line Coding: NRZ & Manchester': 'Line coding (Manchester)', 'Nyquist & Shannon Capacity': 'Nyquist & Shannon (numerical)', 'Framing: Byte & Bit Stuffing': 'Byte & bit stuffing',
           'Error Detection: Parity & Checksum': 'Checksum (numerical)', 'CRC: Cyclic Redundancy Check': 'CRC (numerical)', 'Hamming Code': 'Hamming code (numerical)',
           'Stop-and-Wait ARQ': 'Stop-and-wait ARQ', 'Go-Back-N & Selective Repeat': 'Go-Back-N vs Selective Repeat', 'Sliding Window Numerical': 'Sliding window (numerical)',
           'ALOHA: Pure & Slotted': 'Pure & slotted ALOHA', 'CSMA, CSMA/CD & CSMA/CA': 'CSMA/CD & CSMA/CA', 'Ethernet (IEEE 802.3)': 'Ethernet frame',
           'IPv4 Address & Classes': 'IPv4 classes', 'Subnetting Numerical': 'Subnetting (numerical)', 'CIDR & VLSM': 'CIDR & VLSM (numerical)',
           'Private Addresses, NAT & Supernetting': 'NAT & supernetting', 'IPv4 Header': 'IPv4 header', 'IP Fragmentation Numerical': 'Fragmentation (numerical)', 'IPv6': 'IPv6',
           'ARP, ICMP & DHCP': 'ARP, ICMP, DHCP', 'Routing Basics: RIP, OSPF & BGP': 'RIP, OSPF, BGP', "Dijkstra's Algorithm (Link State)": 'Dijkstra (numerical)',
           'Distance Vector Routing': 'Distance vector (numerical)', 'Transport Layer: UDP vs TCP': 'TCP vs UDP', 'TCP Header & Connection': '3-way handshake',
           'TCP Congestion Control': 'TCP congestion (numerical)', 'Leaky Bucket & Token Bucket': 'Leaky & token bucket', 'DNS: Domain Name System': 'DNS',
           'HTTP, FTP & Email': 'HTTP, FTP, email & ports', 'Cryptography & RSA': 'RSA (numerical)', 'Formula Sheet': 'Formula sheet'}
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
with open(f'{OUT}/CN_OneShot_English.srt', 'w') as f:
    for i, (a, b, s) in enumerate(subs, 1): f.write(f'{i}\n{srt_t(a)} --> {srt_t(b)}\n{s}\n\n')
print('\n'.join(chap)); print('subtitles', len(subs))
