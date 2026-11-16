'''Computer Networks one-shot: narration beats + handwritten note elements for every page.
Markup inside text: [r:red] [g:green] [k:black] [h:yellow highlight] [p:pink highlight]'''
import json, math
from cn_numericals import *

PAGES = []
def L(n): return 222 + 54 * n            # baseline of ruled line n (0..14)
def page(title, ch, kind='page', **kw): p = dict(kind=kind, title=title, ch=ch, beats=[], **kw); PAGES.append(p); return p
def beat(p, say, *els):
    flat = []
    for e in els:
        if isinstance(e, list): flat += e
        elif e: flat.append(e)
    p['beats'].append({'say': ' '.join(say.split()), 'els': flat})
def T(n, s, x=180, size=38, font='body', color='blue', y=None): return dict(t='text', x=int(round(x)), y=int(round(L(n) if y is None else y)), s=s, size=size, font=font, color=color)
def S(n, s, x=180, color='black', size=42, y=None): return T(n, s, x, size, 'bold', color, y)
def N(n, k, s, x=180, color='blue', size=38): return T(n, f'{k}) {s}', x, size, 'body', color)
def Box(x, y, w, h, label=None, color='black', size=32, fill=None, lc=None): return dict(t='rect', x=round(x), y=round(y), w=round(w), h=round(h), label=label, color=color, size=size, fill=fill, lc=lc or color)
def Ell(x, y, w, h, label=None, color='black', size=32, fill=None, lc=None): return dict(t='ellipse', x=round(x), y=round(y), w=round(w), h=round(h), label=label, color=color, size=size, fill=fill, lc=lc or color)
def Arr(x1, y1, x2, y2, color='black', label=None, lx=0, ly=-14, curve=0, head=True, size=28, both=False, lc=None): return dict(t='arrow', p1=(round(x1), round(y1)), p2=(round(x2), round(y2)), color=color, label=label, lx=round(lx), ly=round(ly), curve=curve, head=head, size=size, both=both, lc=lc or color)
def Ln(pts, color='black', w=4): return dict(t='line', pts=[(round(a), round(b)) for a, b in pts], color=color, w=w)
def Tab(x, y, cw, rh, rows, color='black', size=30, hdr=True, order='row', colors=None, fills=None): return dict(t='table', x=x, y=y, cw=cw, rh=rh, rows=rows, color=color, size=size, hdr=hdr, order=order, colors={f'{r},{c}': v for (r, c), v in (colors or {}).items()}, fills={f'{r},{c}': v for (r, c), v in (fills or {}).items()})
def Stamp(x, y, text='IMP!', color='red', rot=-8, size=34): return dict(t='stamp', x=x, y=y, text=text, color=color, rot=rot, size=size)
def Dash(x1, y1, x2, y2, color='grey', seg=18, gap=14, w=3):
    d = math.hypot(x2 - x1, y2 - y1); n = int(d // (seg + gap)) + 1; out = []
    for i in range(n):
        a = i * (seg + gap) / d; b = min(1, (i * (seg + gap) + seg) / d)
        if a < 1: out.append(Ln([(x1 + (x2 - x1) * a, y1 + (y2 - y1) * a), (x1 + (x2 - x1) * b, y1 + (y2 - y1) * b)], color, w))
    return out
def M(x, y, s, size=30, color='black'): return T(0, s, x=x, y=y, size=size, font='mono', color=color)
MW = .6                                   # JetBrains Mono advance = 0.6 x size

# ---------- diagram helpers
def Node(p, name, color='blue', r=36, size=28): return Ell(p[0] - r, p[1] - r, 2 * r, 2 * r, name, color=color, size=size)
def WEdge(a, b, w, color='black', r=36, side=1, size=28, off=24):
    (x1, y1), (x2, y2) = a, b; d = math.hypot(x2 - x1, y2 - y1); ux, uy = (x2 - x1) / d, (y2 - y1) / d; nx, ny = -uy, ux
    if ny > 0 or (abs(ny) < 1e-9 and nx < 0): nx, ny = -nx, -ny          # label goes on the upper / right side by default
    nx, ny = nx * side, ny * side; mx, my = (x1 + x2) / 2 + nx * off, (y1 + y2) / 2 + ny * off
    return [Ln([(x1 + ux * r, y1 + uy * r), (x2 - ux * r, y2 - uy * r)], color, 4), T(0, str(w), x=mx - size * .28, y=my + size * .35, size=size, color='red')]
def Wave(x0, yc, lv, hw=80, amp=34, color='blue'):
    Y = lambda v: yc - amp * v; pts = [(x0, Y(lv[0]))]
    for i in range(1, len(lv)):
        if lv[i] != lv[i - 1]: pts += [(x0 + i * hw, Y(lv[i - 1])), (x0 + i * hw, Y(lv[i]))]
    pts.append((x0 + len(lv) * hw, Y(lv[-1]))); return Ln(pts, color, 4)
def Msg(xa, xb, y, label, color='black', dy=40, size=26):
    return Arr(xa, y, xb, y + dy, color=color, label=label, ly=-30, size=size)
def Life(x, y1, y2, name, color='black'):
    return [T(0, name, x=x - len(name) * 8, y=y1 - 14, size=30, font='bold', color=color), Ln([(x, y1), (x, y2)], 'grey', 4)]

CHAPTERS = [
 (1, 'Introduction & Network Models', ['Types & topologies', 'OSI & TCP/IP models', 'Devices, switching & delays'], 5),
 (2, 'Physical Layer', ['Transmission media', 'Line coding', 'Nyquist & Shannon', 'Multiplexing'], 4),
 (3, 'Data Link Layer: Error Control', ['Framing & stuffing', 'Parity & checksum', 'CRC', 'Hamming code'], 5),
 (4, 'Flow Control: Sliding Window', ['Stop-and-wait', 'Go-Back-N', 'Selective Repeat'], 5),
 (5, 'Medium Access Control', ['ALOHA', 'CSMA/CD & CSMA/CA', 'Ethernet'], 5),
 (6, 'IP Addressing & Subnetting', ['IPv4 classes', 'Subnetting', 'CIDR & VLSM', 'NAT'], 5),
 (7, 'IPv4, IPv6 & Network Protocols', ['IPv4 header', 'Fragmentation', 'IPv6', 'ARP, ICMP, DHCP'], 5),
 (8, 'Routing Algorithms', ['RIP, OSPF, BGP', 'Dijkstra (link state)', 'Distance vector'], 5),
 (9, 'Transport Layer: TCP & UDP', ['UDP vs TCP', 'TCP header & handshake', 'TCP congestion control'], 5),
 (10, 'Congestion Control & QoS', ['Leaky bucket', 'Token bucket', 'Open & closed loop'], 4),
 (11, 'Application Layer & Security', ['DNS', 'HTTP, FTP, email', 'Cryptography & RSA'], 4),
 (12, 'Exam Revision', ['Formula sheet', 'Most asked questions'], 5),
]
def chapter(i):
    n, t, subs, stars = CHAPTERS[i - 1]
    return page(t, n, kind='chapter', num=n, subs=subs, stars=stars)

# =====================================================================================
p = page('Computer Networks', 0, kind='cover')
beat(p, '''Computer Networks. The complete subject in one video. Simple explanations, handwritten notes, neat diagrams,
and every important exam numerical solved step by step.''')
beat(p, '''This works for B Tech computer science in almost every university. A K T U, Anna University, V T U, J N T U,
Mumbai, Pune, and private universities too. And it covers the computer networks part of GATE. So grab a pen, and let's start.''')

p = page('Contents', 0)
items = ['Introduction, [h:OSI & TCP/IP]', 'Physical layer  (Nyquist, Shannon)', '[h:Error control]  (CRC, Hamming)', '[h:Sliding window]  protocols',
         'MAC: ALOHA, CSMA/CD, Ethernet', '[h:IP addressing & subnetting]', 'IPv4 header, fragmentation, IPv6', '[h:Routing]  (Dijkstra, distance vector)',
         '[h:TCP & UDP]  (congestion control)', 'Leaky & token bucket', 'DNS, HTTP, email, RSA', 'Exam revision & formula sheet']
beat(p, "Here's our plan. Twelve chapters, from the basics to the exam numericals.", T(0, 'What we will cover today', size=42, font='bold', color='black'))
beat(p, '''We start with network models and the physical layer, then error control, sliding window protocols, medium access control, and I P addressing.''',
     *[T(1 + k, f'{k + 1}.  {items[k]}', x=200) for k in range(6)])
beat(p, '''Then I P version six, routing, T C P and U D P, congestion control, the application layer, and security. At the end, a formula sheet and the most asked questions.
The highlighted topics are the most important.''',
     *[T(7 + k, f'{k + 7}.  {items[k + 6]}', x=200) for k in range(6)], Stamp(1520, 560, 'MOST ASKED', rot=-10))

# ===================================================================================== CH 1
p = chapter(1)
beat(p, "Chapter one. Introduction and network models. Let's build the basics first.")

p = page('Computer Network & Its Types', 1)
beat(p, '''A computer network is a group of computers and devices connected together to share data and resources, like files, printers and the internet.
Each device is called a node, and each connection is called a link.''',
     T(0, '[h:Computer network] = connected devices that share data & resources'), T(1, 'device = [k:node];   connection = [k:link]  (wired or wireless)'))
beat(p, '''By size, there are four types. A personal area network, or PAN, covers a few metres, like Bluetooth. A local area network, or LAN, covers a building or campus.
A metropolitan area network, MAN, covers a city. And a wide area network, WAN, covers countries. The internet is the biggest WAN.''',
     Stamp(1650, 140),
     Tab(180, 330, [170, 420, 560], 56, [['Type', 'Area', 'Example'], ['PAN', 'a few metres', 'Bluetooth, hotspot'], ['LAN', 'building / campus', 'college lab, Wi-Fi'],
         ['MAN', 'a city', 'cable TV network'], ['WAN', 'countries', 'the internet']], size=30, colors={(r, 0): 'red' for r in range(1, 5)}))
beat(p, '''Transmission modes. In simplex, data flows in only one direction, like a keyboard to a computer. In half duplex, both directions, but one at a time, like a walkie talkie.
In full duplex, both directions at the same time, like a phone call.''',
     T(11, '[k:Simplex]: one way (keyboard)'), T(12, '[k:Half duplex]: both ways, one at a time (walkie-talkie)'), T(13, '[k:Full duplex]: both ways at the same time (phone call)'))

p = page('Network Topologies', 1)
def topo_bus(x, y):
    return [Ln([(x, y), (x + 300, y)], 'black', 5)] + sum([[Ln([(x + 40 + 110 * k, y), (x + 40 + 110 * k, y - 50)], 'black', 3), Box(x + 15 + 110 * k, y - 100, 50, 50, None, 'blue')] for k in range(3)], [])
def topo_star(cx, cy):
    out = [Box(cx - 40, cy - 30, 80, 60, 'hub', 'red', size=22)]
    for a in range(4):
        t = math.radians(45 + 90 * a); px, py = cx + 130 * math.cos(t), cy + 110 * math.sin(t)
        out += [Ln([(cx + 45 * math.cos(t), cy + 35 * math.sin(t)), (px - 25 * math.cos(t), py - 25 * math.sin(t))], 'black', 3), Box(px - 25, py - 25, 50, 50, None, 'blue')]
    return out
def ring_pts(cx, cy, n, r): return [(cx + r * math.cos(math.radians(-90 + 360 * k / n)), cy + r * math.sin(math.radians(-90 + 360 * k / n))) for k in range(n)]
def topo_ring(cx, cy):
    P = ring_pts(cx, cy, 5, 110); out = []
    for k in range(5):
        a, b = P[k], P[(k + 1) % 5]; out.append(Ln([a, b], 'black', 3))
    return out + [Ell(px - 24, py - 24, 48, 48, None, 'blue') for px, py in P]
def topo_mesh(cx, cy):
    P = ring_pts(cx, cy, 5, 110); out = [Ln([P[i], P[j]], 'black', 3) for i in range(5) for j in range(i + 1, 5)]
    return out + [Ell(px - 24, py - 24, 48, 48, None, 'blue') for px, py in P]
beat(p, '''Topology means how the devices are connected. In a bus topology, all devices share one main cable. It is cheap, but if the main cable breaks, the whole network fails.
In a star topology, every device connects to a central hub or switch. It is easy to manage, but if the hub fails, everything stops.''',
     T(0, '[h:Topology] = layout of how devices are connected'),
     topo_bus(220, 520), T(0, 'Bus', x=330, y=585, size=32, font='bold', color='black'), topo_star(720, 430), T(0, 'Star', x=690, y=600, size=32, font='bold', color='black'),
     T(10, '[k:Bus]: one shared cable, cheap; cable break => network down', size=32), T(11, '[k:Star]: central hub / switch; easy to manage; hub fails => all down', size=32))
beat(p, '''In a ring topology, each device connects to the next one in a closed loop, and data travels around the ring. In a mesh topology, every device connects to every other device.
It is the most reliable, but also the most expensive.''',
     topo_ring(1200, 430), T(0, 'Ring', x=1165, y=600, size=32, font='bold', color='black'), topo_mesh(1620, 430), T(0, 'Mesh', x=1580, y=600, size=32, font='bold', color='black'),
     T(12, '[k:Ring]: closed loop, data goes around;  [k:Mesh]: everyone to everyone, most reliable', size=32))
beat(p, '''A common numerical: in a full mesh with n devices, we need n into n minus one by two links, and each device needs n minus one ports. So for five devices, we need ten links and four ports each.''',
     Stamp(1650, 140, 'NUMERICAL'), T(13, 'Mesh: links = [h:n(n - 1) / 2],  ports per device = n - 1', size=34, color='red'),
     T(14, 'n = 5  =>  links = 5 × 4 / 2 = [h:10],  ports = 4 each', size=34, color='black'))

osi = [['#', 'Layer', 'Main job', 'Data unit', 'Examples'], ['7', 'Application', 'services to the user', 'data', 'HTTP, FTP, SMTP, DNS'], ['6', 'Presentation', 'format, encrypt, compress', 'data', 'SSL/TLS, JPEG'],
       ['5', 'Session', 'start, manage, end sessions', 'data', 'RPC, NetBIOS'], ['4', 'Transport', 'process to process, reliable', 'segment', 'TCP, UDP'],
       ['3', 'Network', 'routing, logical (IP) address', 'packet', 'IP, router'], ['2', 'Data link', 'framing, MAC address, errors', 'frame', 'Ethernet, switch'],
       ['1', 'Physical', 'bits on the wire', 'bits', 'cable, hub, repeater']]
p = page('The OSI Model', 1)
beat(p, '''The O S I model, open systems interconnection, divides networking into seven layers. Each layer does one job and serves the layer above it.
Starting from the bottom: the physical layer sends raw bits over the cable. The data link layer makes frames and uses M A C addresses. The network layer routes packets using I P addresses.
And the transport layer gives process to process delivery, using T C P or U D P.''',
     Stamp(1650, 140, 'MOST ASKED'),
     Tab(180, 260, [70, 250, 540, 170, 420], 58, osi, size=29, colors={**{(r, 1): 'red' for r in range(1, 8)}}))
beat(p, '''The upper three layers are closer to the user. The session layer starts, manages and ends sessions. The presentation layer handles format, encryption and compression.
And the application layer gives services to the user, like the web and email.''',
     T(13, 'Data unit (PDU): [k:bits -> frame -> packet -> segment -> data]', size=34, color='green'))
beat(p, '''An easy way to remember the layers from top to bottom: All People Seem To Need Data Processing.''',
     T(14, 'Top -> bottom: [h:All People Seem To Need Data Processing]', size=34, color='red'))

p = page('TCP/IP Model vs OSI', 1)
ox, tx, y0, h = 1060, 1460, 250, 62
osi_names = ['Application', 'Presentation', 'Session', 'Transport', 'Network', 'Data link', 'Physical']
beat(p, '''The T C P slash I P model is the model the internet actually uses. It has four layers. The application layer combines the top three O S I layers.
Then the transport layer, the internet layer, and the network access layer, which combines the data link and physical layers.''',
     [Box(ox, y0 + h * k, 330, h, n_, 'blue', size=28) for k, n_ in enumerate(osi_names)], T(0, 'OSI (7)', x=ox + 110, y=y0 - 16, size=30, font='bold', color='black'),
     Box(tx, y0, 330, 3 * h, 'Application', 'green', size=28), Box(tx, y0 + 3 * h, 330, h, 'Transport', 'green', size=28), Box(tx, y0 + 4 * h, 330, h, 'Internet', 'green', size=28),
     Box(tx, y0 + 5 * h, 330, 2 * h, 'Network access', 'green', size=28), T(0, 'TCP/IP (4)', x=tx + 90, y=y0 - 16, size=30, font='bold', color='black'),
     T(0, 'TCP/IP: [k:4 layers]  (some books: 5)', size=34), T(1, 'Application = OSI layers 5, 6, 7', size=34), T(2, 'Network access = data link + physical', size=34))
beat(p, '''The main differences. O S I is a reference model, made before the protocols. T C P slash I P was made from real protocols, so it is practical. In T C P slash I P,
the transport layer can be connection oriented or connectionless, and the network layer is only connectionless.''',
     Stamp(1650, 140),
     Tab(180, 720, [400, 600, 640], 54, [['', 'OSI', 'TCP/IP'], ['layers', '7', '4'], ['type', 'reference (theory) model', 'practical, used by the internet'],
         ['made', 'model first, protocols later', 'protocols first, model later']], size=28, colors={(r, 0): 'red' for r in range(1, 4)}))

p = page('Network Devices', 1)
beat(p, '''Network devices work at different layers. A repeater regenerates a weak signal, at the physical layer. A hub is a multi port repeater. It sends every frame to all ports.
A bridge connects two L A N segments and filters frames using M A C addresses. A switch is a multi port bridge. It sends a frame only to the correct port.''',
     Stamp(1650, 140, 'MOST ASKED'),
     Tab(180, 240, [230, 170, 940], 58, [['Device', 'Layer', 'What it does'], ['Repeater', '1', 'regenerates a weak signal'], ['Hub', '1', 'multiport repeater: sends to [r:all] ports'],
         ['Bridge', '2', 'connects LAN segments, filters by MAC address'], ['Switch', '2', 'multiport bridge: sends to [g:one] port (MAC table)'],
         ['Router', '3', 'connects different networks, uses IP address'], ['Gateway', '4 - 7', 'connects different protocols (translator)']], size=29,
         colors={(r, 0): 'red' for r in range(1, 7)}))
beat(p, '''A router connects different networks and forwards packets using I P addresses. And a gateway connects networks that use different protocols, like a translator.''')
beat(p, '''GATE also asks about domains. A hub has one collision domain for all ports. A switch makes each port its own collision domain, but all ports are still one broadcast domain.
A router separates both collision and broadcast domains.''',
     T(11, 'Hub: 1 collision domain;  Switch: [h:each port] = 1 collision domain', size=32), T(12, 'Switch: 1 broadcast domain;  Router: each port = separate broadcast domain', size=32),
     T(13, 'e.g. 8-port switch => 8 collision domains, 1 broadcast domain', size=32, color='green'))

p = page('Switching Techniques', 1)
beat(p, '''Switching decides how data moves through the network. In circuit switching, a dedicated path is set up first, and kept for the whole call, like the old telephone network.
In packet switching, data is broken into packets, and each packet shares the links with others.''',
     T(0, '[h:Circuit switching]: dedicated path first (setup -> transfer -> teardown)', size=34), T(1, '[h:Packet switching]: data split into packets; links are shared', size=34))
beat(p, '''Packet switching has two types. In the datagram approach, each packet is routed on its own, and packets can arrive out of order. The internet works this way.
In the virtual circuit approach, a path is set up first, and all packets follow it in order.''',
     T(3, '[k:Datagram]: each packet routed independently (internet, IP)', size=34), T(4, '[k:Virtual circuit]: path set up first, packets in order (ATM, frame relay)', size=34))
beat(p, '''Here is a quick comparison.''',
     Stamp(1650, 140),
     Tab(180, 540, [380, 420, 420, 420], 56, [['', 'Circuit', 'Datagram', 'Virtual circuit'], ['setup phase', 'yes', 'no', 'yes'], ['path', 'dedicated', 'any, per packet', 'same for all'],
         ['order', 'in order', 'may be out of order', 'in order'], ['resources', 'reserved', 'on demand', 'on demand'], ['example', 'telephone', 'internet (IP)', 'ATM']], size=28,
         colors={(r, 0): 'red' for r in range(1, 6)}))

dl = delays()
p = page('Delays in a Network', 1)
beat(p, '''A packet faces four delays. Transmission delay is the time to push all the bits onto the link: length divided by bandwidth. Propagation delay is the time for a bit to travel
the distance: distance divided by signal speed. There is also queuing delay at routers, and processing delay.''',
     Stamp(1650, 140, 'NUMERICAL'), T(0, '[h:Transmission delay] Tt = L / B   (L = bits, B = bandwidth)', size=36), T(1, '[h:Propagation delay] Tp = d / v   (d = distance, v = speed)', size=36),
     T(2, '+ queuing delay + processing delay', size=34))
beat(p, '''Example. A packet of one thousand bytes is sent on a one megabit per second link, over two thousand kilometres, and the signal speed is two times ten to the power eight metres per second.
Transmission delay is eight thousand bits divided by ten to the power six, which is eight milliseconds. Propagation delay is two times ten to the power six metres divided by two times ten to the power eight, which is ten milliseconds.
So the total is eighteen milliseconds.''',
     T(4, 'L = 1000 bytes, B = 1 Mbps, d = 2000 km, v = 2 × 10^8 m/s', color='black', size=34),
     T(5, f'Tt = 8000 / 10^6 = [r:{fmt(dl["Tt"] * 1000)} ms]', size=36), T(6, f'Tp = 2 × 10^6 / 2 × 10^8 = [r:{fmt(dl["Tp"] * 1000)} ms]', size=36),
     T(7, f'Total = 8 + 10 = [h:{fmt(dl["total"] * 1000)} ms]', size=38, color='red'))
beat(p, '''The bandwidth delay product tells how many bits can be on the link at one time. It is bandwidth times propagation delay. Here, ten to the power six times ten milliseconds is ten thousand bits.
Also remember: transmission delay depends on the packet size, but propagation delay depends only on the distance.''',
     T(9, f'[k:Bandwidth-delay product] = B × Tp = 10^6 × 0.01 = [h:{int(dl["bdp"]):,} bits]', size=34),
     T(10, 'Tt depends on packet size & bandwidth;  Tp depends on distance & medium', size=32, color='green'))

# ===================================================================================== CH 2
p = chapter(2)
beat(p, 'Chapter two. The physical layer. How bits actually travel.')

p = page('Transmission Media', 2)
beat(p, '''Transmission media are of two types. Guided media use a cable. Twisted pair cable is cheap and used in L A N s, with R J forty five connectors. Coaxial cable is used for cable T V.
And optical fibre carries light. It has the highest bandwidth, and it is not affected by electrical noise, because of total internal reflection.''',
     S(0, 'Guided (wired)', color='red', size=38), N(1, 1, 'Twisted pair (UTP / STP): cheap, LANs, RJ-45', size=34), N(2, 2, 'Coaxial cable: cable TV, better shielding', size=34),
     N(3, 3, '[h:Optical fibre]: light, total internal reflection, highest bandwidth, no EMI', size=34))
beat(p, '''Unguided media use the air, without a cable. Radio waves go in all directions and pass through walls, used for F M radio and Wi-Fi. Microwaves need a line of sight, used for satellites and mobile towers.
Infrared works only at short range, and cannot pass through walls, like a T V remote.''',
     S(5, 'Unguided (wireless)', color='red', size=38), N(6, 1, 'Radio waves: all directions, pass walls (FM, Wi-Fi)', size=34),
     N(7, 2, 'Microwaves: line of sight (satellite, mobile towers)', size=34), N(8, 3, 'Infrared: short range, no walls (TV remote)', size=34))
beat(p, '''Also remember the three causes of signal problems: attenuation, which is loss of strength, distortion, which is change in shape, and noise.''',
     T(10, '[k:Transmission impairments]: attenuation (loss), distortion (shape), noise', size=34, color='green'))

bits = '01001110'; X0, HW = 560, 80
schemes = [('NRZ-L', 'NRZ-L:  1 = high, 0 = low'), ('NRZ-I', 'NRZ-I:  1 = invert, 0 = no change'), ('Manchester', 'Manchester:  0 = high->low, 1 = low->high (IEEE)'),
           ('Diff Manchester', 'Diff. Manchester:  0 = transition at start, 1 = no transition')]
ys = [430, 570, 710, 850]
p = page('Line Coding: NRZ & Manchester', 2)
beat(p, '''Line coding converts bits into a digital signal. Let's draw four schemes for the bits zero one zero zero one one one zero. In N R Z L, non return to zero level,
a one is a high level and a zero is a low level.''',
     Stamp(1650, 140, 'NUMERICAL'), T(0, 'Bits:', x=180, size=36, color='black'),
     *[T(0, b, x=X0 + HW * 2 * i + HW - 10, y=L(0), size=38, font='bold', color='black') for i, b in enumerate(bits)],
     *[Ln([(X0 + 2 * HW * i, L(0) + 30), (X0 + 2 * HW * i, 900)], 'grey', 2) for i in range(len(bits) + 1)],
     T(0, 'NRZ-L', x=200, y=ys[0] + 12, size=32, font='bold', color='red'), Wave(X0, ys[0], encode(bits, 'NRZ-L'), hw=HW, amp=34))
beat(p, '''In N R Z I, non return to zero invert, a one means invert the level, and a zero means no change. We start from low.''',
     T(0, 'NRZ-I', x=200, y=ys[1] + 12, size=32, font='bold', color='red'), Wave(X0, ys[1], encode(bits, 'NRZ-I'), hw=HW, amp=34))
beat(p, '''In Manchester encoding, there is always a transition in the middle of every bit, which helps synchronization. Following the I E E E convention, a zero goes from high to low,
and a one goes from low to high. Ethernet uses Manchester, but it needs double the bandwidth.''',
     T(0, 'Manchester', x=200, y=ys[2] + 12, size=32, font='bold', color='red'), Wave(X0, ys[2], encode(bits, 'Manchester'), hw=HW, amp=34))
beat(p, '''In differential Manchester, there is also a transition in the middle of every bit. A zero has an extra transition at the start of the bit, and a one has no transition at the start.''',
     T(0, 'Diff. Manch.', x=200, y=ys[3] + 12, size=32, font='bold', color='red'), Wave(X0, ys[3], encode(bits, 'Diff Manchester'), hw=HW, amp=34),
     T(14, 'Manchester & differential Manchester: transition in the [h:middle] of every bit (self-clocking)', size=30, color='green'))

ny2, ny4 = nyquist(3000, 2), nyquist(3000, 4); snr, cap = shannon(3000, 30)
p = page('Nyquist & Shannon Capacity', 2)
beat(p, '''How fast can a channel send data? For a noiseless channel, we use the Nyquist formula: bit rate equals two times bandwidth times log base two of L, where L is the number of signal levels.
For a bandwidth of three thousand hertz with two levels, the bit rate is six thousand bits per second. With four levels, it doubles to twelve thousand.''',
     Stamp(1650, 140, 'NUMERICAL'), S(0, 'Noiseless channel: Nyquist', color='red', size=38), T(1, '[h:Bit rate = 2 × B × log2(L)]   (L = signal levels)', size=38),
     T(2, f'B = 3000 Hz, L = 2:  2 × 3000 × 1 = [r:{int(ny2):,} bps]', size=34), T(3, f'L = 4:  2 × 3000 × 2 = [r:{int(ny4):,} bps]', size=34))
beat(p, '''For a noisy channel, we use Shannon's formula: capacity equals bandwidth times log base two of one plus S N R. Here S N R is the signal to noise ratio, not in decibels.
To convert decibels: S N R in decibels equals ten log base ten of S N R.''',
     S(5, 'Noisy channel: Shannon', color='red', size=38), T(6, '[h:C = B × log2(1 + SNR)]', size=38), T(7, 'SNR(dB) = 10 log10(SNR)', size=34))
beat(p, f'''Example: bandwidth three thousand hertz, and S N R is thirty decibels. Thirty decibels means S N R equals ten to the power three, which is one thousand.
So capacity equals three thousand times log base two of one thousand and one, which is about twenty nine thousand nine hundred bits per second, nearly thirty kilobits per second.
Shannon gives the upper limit. No method can send faster on that channel.''',
     T(9, f'SNR = 30 dB  =>  10^3 = {int(snr):,}', size=34, color='black'), T(10, f'C = 3000 × log2(1001) ≈ [h:{cap:,.0f} bps] ≈ 30 kbps', size=36, color='black'),
     T(11, 'Shannon = [r:upper limit];  Nyquist = levels needed for a bit rate', size=32, color='green'))

p = page('Multiplexing', 2)
beat(p, '''Multiplexing sends many signals over one link at the same time, to share the bandwidth. In frequency division multiplexing, F D M, each signal gets its own frequency band,
with guard bands in between to avoid overlap. It is used for analog signals, like radio and T V.''',
     T(0, '[h:Multiplexing]: many signals share one link', size=36), T(1, '[k:FDM]: each signal gets a frequency band (+ guard bands); analog, radio / TV', size=33))
beat(p, '''In time division multiplexing, T D M, each signal gets a time slot, one after another. In synchronous T D M, every input gets a fixed slot, even if it has nothing to send.
In statistical T D M, slots are given only to inputs that have data, so less bandwidth is wasted.''',
     T(3, '[k:TDM]: each signal gets a time slot; digital', size=33), T(4, 'synchronous TDM: fixed slots (wasted if idle);  statistical TDM: slots on demand', size=31),
     *[Box(560 + 120 * k, 520, 120, 70, 'ABCD'[k % 4], ['blue', 'green', 'red', 'black'][k % 4], size=30) for k in range(8)],
     T(0, 'frame 1', x=740, y=630, size=26, color='grey'), T(0, 'frame 2', x=1220, y=630, size=26, color='grey'), T(0, 'time ->', x=1550, y=565, size=28, color='black'))
beat(p, '''And wavelength division multiplexing, W D M, is F D M for optical fibre, where each signal uses a different colour of light. Finally, spread spectrum spreads the signal over a wider band
for security against jamming.''',
     T(9, '[k:WDM]: FDM for optical fibre (different wavelengths of light)', size=33), T(10, '[k:Spread spectrum] (FHSS, DSSS): spreads signal; secure, anti-jamming', size=33))

# ===================================================================================== CH 3
p = chapter(3)
beat(p, 'Chapter three. The data link layer, and error control. C R C and Hamming code are asked in almost every exam.')

stuffed = bit_stuff('011011111111111111110010')
stuffed_at, _run = set(), 0
for _i, _c in enumerate(stuffed):
    if _run == 5: stuffed_at.add(_i); _run = 0; continue
    _run = _run + 1 if _c == '1' else 0
p = page('Framing: Byte & Bit Stuffing', 3)
beat(p, '''The data link layer gives node to node delivery. Its jobs are framing, physical addressing with M A C addresses, flow control, error control, and access control.
Framing means dividing the bit stream into frames, with a header and a trailer. But how does the receiver know where a frame ends? We use a special flag, and stuffing.''',
     T(0, 'DLL jobs: [k:framing, MAC addressing, flow control, error control, access control]', size=33),
     Box(560, 300, 140, 70, 'Flag', 'red', size=28), Box(700, 300, 220, 70, 'Header', size=28), Box(920, 300, 400, 70, 'Data', 'blue', size=28), Box(1320, 300, 220, 70, 'Trailer', size=28),
     Box(1540, 300, 140, 70, 'Flag', 'red', size=28))
beat(p, '''In byte stuffing, a special flag byte marks the start and end. If the flag byte appears inside the data, the sender adds an escape byte, E S C, before it. If an E S C appears in the data, it also gets an extra E S C.
The receiver removes them.''',
     Stamp(1650, 140, 'NUMERICAL'), S(4, 'Byte stuffing', color='red', size=36), T(5, 'data:     A  [r:FLAG]  B  [r:ESC]  C', size=34, color='black'),
     T(6, 'sent:     A  [g:ESC] FLAG  B  [g:ESC] ESC  C', size=34, color='black'))
beat(p, f'''In bit stuffing, the flag is zero one one one one one one zero. Whenever the sender sees five ones in a row in the data, it adds a zero after them, so the data never looks like the flag.
The receiver removes the zero after five ones.''',
     S(8, 'Bit stuffing   (flag = 01111110)', color='red', size=36), T(9, 'after [h:five 1s] in a row, insert a 0', size=34),
     M(180, L(10) + 4, 'data:   011011111111111111110010', size=34), M(180, L(11) + 8, 'sent:', size=34),
     *[M(180 + MW * 34 * (8 + i), L(11) + 8, c, size=34, color='red' if i in stuffed_at else 'black') for i, c in enumerate(stuffed)],
     T(12, '(stuffed 0s in red)', size=28, color='green', y=L(12) + 14))

ck, ckc, ctr = checksum8(['10110011', '10101011', '01011010', '11010101'])
p = page('Error Detection: Parity & Checksum', 3)
beat(p, '''Errors happen when bits change during transmission. A single bit error changes one bit. A burst error changes two or more bits in a row.
The simplest check is a parity bit. In even parity, we add a bit so that the total number of ones is even. It can detect any odd number of errors, but not an even number.''',
     T(0, 'single-bit error vs [k:burst error] (2 or more bits)', size=34), T(1, '[h:Even parity]: add a bit so the number of 1s is even;  1011001 -> 1011001[r:0]', size=34),
     T(2, 'detects odd number of errors only;  2D parity detects more', size=32, color='green'))
beat(p, '''Hamming distance is the number of bit positions where two codewords differ. To detect s errors, the minimum Hamming distance must be s plus one. To correct t errors, it must be two t plus one.''',
     Stamp(1650, 140, 'GATE'), T(4, '[h:Hamming distance] d(10101, 11110) = 3', size=34), T(5, 'detect s errors: d_min = [r:s + 1];   correct t errors: d_min = [r:2t + 1]', size=34))
beat(p, f'''Checksum. The sender adds all the data words using one's complement addition, which means a carry out of the last bit is wrapped around and added back. Then it takes the complement of the sum.
For these four words, the sum is one zero zero zero one one one one, so the checksum is zero one one one zero zero zero zero. The receiver adds everything, including the checksum.
If the result is all ones, then after complement it is zero, and there is no error.''',
     Stamp(1650, 500, 'NUMERICAL'),
     M(1050, 610, '  10110011', size=32), M(1050, 650, '+ 10101011', size=32), M(1050, 690, '+ 01011010', size=32), M(1050, 730, '+ 11010101', size=32),
     Ln([(1050, 744), (1300, 744)], 'black', 3), M(1050, 784, '  ' + ck, size=32, color='blue'), T(0, '(carries wrapped around)', x=1320, y=784, size=26, color='green'),
     T(7, '1) add with wrap-around (one\'s complement)', size=34), T(8, '2) checksum = complement of sum', size=34),
     T(9, f'sum = {ck}  =>  checksum = [h:{ckc}]', size=34, color='black'), T(11, 'Receiver: sum of all + checksum = 11111111', size=32),
     T(12, '=> complement = 0  =>  [g:no error]', size=32))

D_, Gn = '100100', '1101'
rem, code, steps = crc(D_, Gn)
def crc_div(x0, y0, data, gen, size=30, rh=40):
    r_, code_, st = crc(data, gen); cw = MW * size; c0 = len(gen) + 3; out = []
    q = ''.join('1' if sub == gen else '0' for _, sub, _, _ in st)
    out.append(M(x0 + cw * (c0 + len(gen) - 1), y0, q, size, 'green'))
    out.append(M(x0, y0 + rh, gen + ' ) ' + data + '0' * (len(gen) - 1), size))
    out.append(Ln([(x0 + cw * (c0 - .6), y0 + 14), (x0 + cw * (c0 + len(data) + len(gen)), y0 + 14)], 'black', 3))
    y = y0 + rh
    for k, (rm, sub, x, off) in enumerate(st):
        y += rh; out.append(M(x0 + cw * (c0 + k), y, sub, size, 'grey' if sub[0] == '0' else 'black'))
        out.append(Ln([(x0 + cw * (c0 + k), y + 12), (x0 + cw * (c0 + k + len(gen)) + 6, y + 12)], 'black', 2))
        y += rh; nxt = st[k + 1][0] if k + 1 < len(st) else x
        out.append(M(x0 + cw * (c0 + k + 1), y, nxt, size, 'red' if k + 1 == len(st) else 'blue'))
    return out
p = page('CRC: Cyclic Redundancy Check', 3)
beat(p, f'''C R C is the most powerful error detection method. The sender and receiver agree on a generator, also called the divisor. If the generator has r plus one bits, we append r zeros to the data,
and divide using modulo two division, which is just X O R, with no carries. The remainder is the C R C. Let's take data one zero zero one zero zero, and generator one one zero one,
which is x cube plus x square plus one.''',
     Stamp(1650, 140, 'NUMERICAL'), T(0, 'Data = 100100,  generator = 1101  (x³ + x² + 1)', size=34, color='black'),
     T(1, 'generator has 4 bits  =>  append [h:3 zeros]', size=34), T(2, 'divide 100100[r:000] by 1101 using XOR', size=34))
beat(p, '''Now divide. At each step, if the leading bit is one, X O R with the generator. If the leading bit is zero, X O R with all zeros. Then bring down the next bit.
After six steps, the remainder is zero zero one.''',
     crc_div(1060, 270, D_, Gn, size=30, rh=40))
beat(p, f'''So the C R C is zero zero one, and the transmitted codeword is the data followed by the remainder: one zero zero one zero zero zero zero one.
The receiver divides the whole codeword by the same generator. If the remainder is zero, there is no error. A C R C with r bits detects all burst errors of length r or less.''',
     T(4, f'Remainder (CRC) = [h:{rem}]', size=36, color='red'), T(5, f'Codeword = 100100 + {rem} = [h:{code}]', size=36, color='black'),
     T(7, f'Receiver: {code} ÷ 1101  =>  remainder 000', size=32), T(8, '=> [g:no error] ' + ('✓' if crc_check(code, Gn) else ''), size=32),
     T(10, 'r-bit CRC detects all burst errors of length ≤ r', size=32, color='green'))

hm = hamming74('1011'); bad = hm[:4] + str(1 - int(hm[4])) + hm[5:]; s4, s2, s1, pos = syndrome(bad)
p = page('Hamming Code', 3)
beat(p, '''Hamming code can detect and also correct a single bit error. First, find the number of parity bits r, using two to the power r is greater than or equal to m plus r plus one,
where m is the number of data bits. For four data bits, r equals three, because eight is at least four plus three plus one. So we get a seven bit code.''',
     Stamp(1650, 140, 'NUMERICAL'), T(0, '[h:2^r ≥ m + r + 1]   m = 4  =>  r = 3  (8 ≥ 8)  =>  7-bit code', size=36),
     T(1, 'Parity bits at positions [r:1, 2, 4] (powers of 2)', size=34))
beat(p, f'''Let's send the data one zero one one, with even parity. The parity bits go at positions one, two and four. Data bits fill positions three, five, six and seven.
P one checks positions one, three, five and seven, so p one is zero. P two checks two, three, six and seven, so p two is one. P four checks four, five, six and seven, so p four is zero.
The codeword is zero one one zero zero one one.''',
     Tab(180, 360, [180] + [120] * 7, 54, [['position', *map(str, range(1, 8))], ['bit', 'p1', 'p2', 'd1', 'p4', 'd2', 'd3', 'd4'], ['value', *hm]], size=30,
         colors={(2, 1): 'red', (2, 2): 'red', (2, 4): 'red'}),
     T(0, 'p1: 1, 3, 5, 7  =>  p1 ⊕ 1 ⊕ 0 ⊕ 1 = 0  =>  p1 = 0', x=1240, y=L(3) + 6, size=28), T(0, 'p2: 2, 3, 6, 7  =>  p2 ⊕ 1 ⊕ 1 ⊕ 1 = 0  =>  p2 = 1', x=1240, y=L(4) + 6, size=28),
     T(0, 'p4: 4, 5, 6, 7  =>  p4 ⊕ 0 ⊕ 1 ⊕ 1 = 0  =>  p4 = 0', x=1240, y=L(5) + 6, size=28),
     T(8, f'Codeword (positions 1 to 7) = [h:{hm}]', size=36, color='black'))
beat(p, f'''Now suppose bit five gets flipped, and the receiver gets zero one one zero one one one. The receiver recomputes the three checks. Check four fails, check two passes, and check one fails.
Writing them as c four, c two, c one gives one zero one, which is five in binary. So the error is at position five. Flip it back, and we get the correct codeword.''',
     T(10, f'Received: {bad[:4]}[r:{bad[4]}]{bad[5:]}', size=36, color='black'),
     T(11, f'c4 c2 c1 = {s4} {s2} {s1} = [h:{pos}]  =>  error at position {pos}, flip it', size=36),
     T(13, 'Hamming code: corrects 1-bit errors, detects 2-bit errors (d_min = 3)', size=30, color='green'))

# ===================================================================================== CH 4
p = chapter(4)
beat(p, 'Chapter four. Flow control, and the sliding window protocols. Efficiency numericals come from here.')

sw = sliding()
p = page('Stop-and-Wait ARQ', 4)
sx, rx = 1180, 1660
beat(p, '''Flow control makes sure a fast sender does not overwhelm a slow receiver. A R Q means automatic repeat request: the receiver sends acknowledgements, and lost frames are sent again.
In stop and wait A R Q, the sender sends one frame, then stops and waits for its acknowledgement.''',
     T(0, '[h:Flow control]: don\'t overwhelm a slow receiver', size=34), T(1, '[h:ARQ]: ACKs + timer + retransmission', size=34), T(2, 'Stop-and-wait: send [r:one] frame, wait for its ACK', size=34),
     Life(sx, 300, 960, 'Sender'), Life(rx, 300, 960, 'Receiver'),
     Msg(sx, rx, 340, 'Frame 0', 'blue'), Msg(rx, sx, 400, 'ACK 1', 'green'), Msg(sx, rx, 470, 'Frame 1', 'blue'))
beat(p, '''If a frame is lost, the sender's timer runs out, and it sends the frame again. Sequence numbers zero and one are used, so the receiver can spot duplicate frames. One bit is enough.''',
     Ln([(1380, 495), (1420, 535)], 'red', 5), Ln([(1420, 495), (1380, 535)], 'red', 5), T(0, 'lost', x=1440, y=500, size=26, color='red'),
     Ln([(sx - 30, 480), (sx - 30, 650)], 'red', 4), T(0, 'timeout', x=sx - 160, y=575, size=26, color='red'),
     Msg(sx, rx, 680, 'Frame 1 (again)', 'blue'), Msg(rx, sx, 740, 'ACK 0', 'green'),
     T(4, 'Seq. numbers 0, 1  =>  [k:1 bit]', size=34), T(5, 'lost frame / lost ACK  =>  timeout => resend', size=34))
beat(p, '''The efficiency of stop and wait is one divided by one plus two a, where a is propagation delay divided by transmission delay. When the distance is large, a is large, and stop and wait wastes most of the time.''',
     Stamp(1650, 140), T(8, '[h:η = 1 / (1 + 2a)],   a = Tp / Tt', size=40, color='red'), T(9, 'large distance => large a => very low efficiency', size=32))

p = page('Go-Back-N & Selective Repeat', 4)
beat(p, '''Sliding window protocols send many frames before waiting. The window is the number of frames that can be sent without an acknowledgement. In go back N, the sender window can be up to two to the power k minus one,
where k is the number of sequence number bits. The receiver window is one, so it accepts frames only in order. If a frame is lost, the sender goes back and resends that frame and all frames after it.''',
     T(0, '[h:Window] = frames sent without waiting for ACK;  k = sequence bits', size=34),
     T(1, '[k:Go-Back-N]: sender window ≤ 2^k - 1, receiver window = 1', size=34), T(2, 'lost frame => resend it [r:and all after it];  cumulative ACK', size=34))
beat(p, '''In selective repeat, only the lost frame is sent again. The receiver keeps out of order frames in a buffer. Here both windows can be at most two to the power k minus one, which is half the sequence numbers.''',
     T(4, '[k:Selective Repeat]: sender = receiver window ≤ 2^(k-1)', size=34), T(5, 'only the lost frame is resent; receiver buffers out-of-order frames', size=34))
beat(p, '''Here is the comparison. For both, if the window W is less than one plus two a, the efficiency is W divided by one plus two a. Otherwise it is one hundred percent.''',
     Stamp(1650, 140, 'MOST ASKED'),
     Tab(180, 560, [380, 420, 420, 420], 54, [['', 'Stop & wait', 'Go-Back-N', 'Selective Repeat'], ['sender window', '1', '2^k - 1', '2^(k-1)'], ['receiver window', '1', '1', '2^(k-1)'],
         ['resend on loss', 'that frame', 'that + all after', 'only that frame'], ['efficiency', '1 / (1 + 2a)', 'W / (1 + 2a)', 'W / (1 + 2a)']], size=28,
         colors={(r, 0): 'red' for r in range(1, 5)}),
     T(14, 'Efficiency = min(1, W / (1 + 2a));  throughput = η × B', size=34, color='green'))

p = page('Sliding Window Numerical', 4)
beat(p, '''Numerical. A link has bandwidth one megabit per second, frames are one thousand bits, and propagation delay is ten milliseconds. Transmission delay is one thousand divided by ten to the power six,
which is one millisecond. So a equals ten divided by one, which is ten.''',
     Stamp(1650, 140, 'NUMERICAL'), T(0, 'B = 1 Mbps, frame = 1000 bits, Tp = 10 ms', color='black'),
     T(1, f'Tt = 1000 / 10^6 = {fmt(sw["Tt"] * 1000)} ms   =>   a = Tp / Tt = [h:{fmt(sw["a"])}]'))
beat(p, f'''For stop and wait, efficiency is one over twenty one, which is about four point seven six percent. So the throughput is only about forty seven point six kilobits per second.
For go back N with a window of seven, efficiency is seven over twenty one, which is thirty three point three percent.''',
     T(3, f'Stop & wait:  η = 1 / (1 + 20) = 1/21 = [r:{sw["sw"] * 100:.2f}%]  =>  {sw["sw"] * 1000:.1f} kbps', size=36),
     T(4, f'GBN, W = 7:   η = 7 / 21 = [r:{sw["gbn"] * 100:.1f}%]  =>  {sw["gbn"] * 1000:.0f} kbps', size=36))
beat(p, f'''For one hundred percent efficiency, the window must be at least one plus two a, which is twenty one. For go back N, two to the power k minus one must be at least twenty one, so k equals five bits.
For selective repeat, two to the power k minus one must be at least twenty one, so k minus one equals five, and k equals six bits.''',
     T(6, '100% efficiency  =>  W ≥ 1 + 2a = [h:21]', size=36, color='black'),
     T(7, f'GBN:  2^k - 1 ≥ 21  =>  k = [r:{sw["k_gbn"]} bits]   (31 ≥ 21)', size=36), T(8, f'SR:  2^(k-1) ≥ 21  =>  k - 1 = 5  =>  k = [r:{sw["k_sr"]} bits]', size=36),
     T(10, 'Tip: always find [k:a] first, then use the formula', size=32, color='green'))

# ===================================================================================== CH 5
p = chapter(5)
beat(p, 'Chapter five. Medium access control. Who gets to use the shared channel, and when.')

al = aloha(200, 200e3, 1000)
p = page('ALOHA: Pure & Slotted', 5)
beat(p, '''When many stations share one channel, we need rules for access. In pure ALOHA, a station sends whenever it has data. If there is a collision, it waits a random time and sends again.
The vulnerable time is two times the frame time. The throughput is S equals G e to the power minus two G, where G is the average number of frames per frame time. The maximum is eighteen point four percent, when G is one half.''',
     T(0, 'random access: [k:ALOHA, CSMA, CSMA/CD, CSMA/CA]', size=32, color='green'),
     S(1, 'Pure ALOHA', color='red', size=36), T(2, 'send any time;  vulnerable time = [h:2 × Tfr]', size=34), T(3, '[h:S = G × e^(-2G)],  S_max = 1 / 2e = [r:18.4%] at G = 0.5', size=34))
beat(p, '''In slotted ALOHA, time is divided into slots, and a station can send only at the start of a slot. This halves the vulnerable time to one frame time.
The throughput is G e to the power minus G, and the maximum is thirty six point eight percent, when G is one.''',
     S(5, 'Slotted ALOHA', color='red', size=36), T(6, 'send only at slot start;  vulnerable time = [h:Tfr]', size=34), T(7, '[h:S = G × e^(-G)],  S_max = 1 / e = [r:36.8%] at G = 1', size=34))
beat(p, f'''Numerical. Two hundred bit frames on a two hundred kilobit per second channel, so the frame time is one millisecond. If the stations produce one thousand frames per second, G equals one.
For pure ALOHA, S is e to the power minus two, which is zero point one three five, so about one hundred and thirty five frames per second succeed. For slotted ALOHA, S is e to the power minus one,
zero point three six eight, so about three hundred and sixty eight frames succeed.''',
     Stamp(1650, 140, 'NUMERICAL'), T(9, 'Frame = 200 bits, channel = 200 kbps  =>  Tfr = 1 ms;  1000 frames/s  =>  G = 1', size=31, color='black'),
     T(10, f'Pure:  S = 1 × e^-2 = {al["pure"]:.3f}  =>  [h:{al["pure"] * 1000:.0f} frames/s] succeed', size=34),
     T(11, f'Slotted:  S = 1 × e^-1 = {al["slotted"]:.3f}  =>  [h:{al["slotted"] * 1000:.0f} frames/s] succeed', size=34))

tp, lmin = csmacd_min()
p = page('CSMA, CSMA/CD & CSMA/CA', 5)
beat(p, '''C S M A means carrier sense multiple access: listen before you talk. In one persistent C S M A, if the channel is busy, keep sensing, and send as soon as it is free.
In non persistent, wait a random time before sensing again. In p persistent, used with slots, when the channel is free, send with probability p.''',
     T(0, '[h:CSMA]: sense the channel before sending', size=36), T(1, '1-persistent: send as soon as idle;  non-persistent: wait random time', size=32),
     T(2, 'p-persistent: when idle, send with probability p', size=32))
beat(p, f'''C S M A with collision detection, used in wired Ethernet, also listens while sending. If a collision happens, it stops and sends a jam signal. To detect a collision before finishing a frame,
transmission time must be at least two times propagation delay. So the minimum frame size is two times propagation delay times bandwidth.
For example, ten megabits per second, two kilometres, and speed two times ten to the power eight: propagation delay is ten microseconds, so the minimum frame is two hundred bits.''',
     Stamp(1650, 140, 'NUMERICAL'), S(4, 'CSMA/CD (wired Ethernet)', color='red', size=36), T(5, 'condition: Tt ≥ 2 × Tp   =>   [h:L_min = 2 × Tp × B]', size=36),
     T(6, f'B = 10 Mbps, d = 2 km, v = 2 × 10^8:  Tp = {tp * 1e6:.0f} μs  =>  L_min = 2 × 10^-5 × 10^7 = [r:{lmin:.0f} bits]', size=31, color='black'),
     T(7, 'after n collisions: wait K × slot, K random in 0 ... 2^n - 1 (binary exponential backoff)', size=30, color='green'))
beat(p, '''Wireless networks cannot detect collisions, so they use C S M A with collision avoidance. The station waits for a gap called I F S, then a random backoff, and the receiver sends an acknowledgement.
R T S and C T S messages, request to send and clear to send, solve the hidden terminal problem.''',
     S(9, 'CSMA/CA (wireless, 802.11)', color='red', size=36), T(10, 'can\'t detect collisions  =>  avoid them: IFS + random backoff + ACK', size=33),
     T(11, '[k:RTS / CTS] solves the hidden terminal problem', size=33))

p = page('Ethernet (IEEE 802.3)', 5)
fr = [('Preamble', 7, 190), ('SFD', 1, 90), ('Dest. addr', 6, 190), ('Src. addr', 6, 190), ('Type', 2, 120), ('Data', '46 - 1500', 400), ('CRC', 4, 120)]
xs = [300]
for _, _, w in fr: xs.append(xs[-1] + w)
beat(p, '''Ethernet is the most used wired L A N. Its frame has a preamble of seven bytes for synchronization, a start frame delimiter of one byte, a six byte destination address,
a six byte source address, a two byte type or length field, the data from forty six to one thousand five hundred bytes, and a four byte C R C.''',
     Stamp(1650, 140, 'MOST ASKED'),
     *[Box(xs[k], 300, w, 80, n_, 'blue' if n_ == 'Data' else 'black', size=24) for k, (n_, b, w) in enumerate(fr)],
     *[T(0, f'{b}', x=xs[k] + w / 2 - len(str(b)) * 7, y=420, size=26, color='red') for k, (n_, b, w) in enumerate(fr)], T(0, 'bytes', x=xs[-1] + 20, y=420, size=26, color='red'))
beat(p, '''So the minimum frame is sixty four bytes, and the maximum is one thousand five hundred and eighteen bytes, not counting the preamble. A M A C address is forty eight bits, written in hexadecimal.
If the first byte is even, it is unicast. If it is odd, it is multicast. And all F's is the broadcast address.''',
     T(5, 'frame: [h:min 64 bytes], max 1518 bytes (without preamble & SFD)', size=34), T(6, 'MAC address = [k:48 bits], e.g. 4A:30:10:21:10:1A', size=34),
     T(7, 'unicast (1st byte even), multicast (odd), broadcast FF:FF:FF:FF:FF:FF', size=32))
beat(p, '''Ethernet speeds: standard Ethernet is ten megabits per second, fast Ethernet is one hundred, gigabit Ethernet is one thousand, and ten gigabit is ten thousand.
Besides random access, there is controlled access: reservation, polling, and token passing, where only the station holding the token can send.''',
     T(9, 'Standard 10 Mbps · Fast 100 Mbps · Gigabit 1 Gbps · 10G', size=33),
     T(10, '[k:Controlled access]: reservation, polling, [h:token passing] (token ring 802.5)', size=33), T(11, '[k:Channelization]: FDMA, TDMA, CDMA', size=33))

# ===================================================================================== CH 6
p = chapter(6)
beat(p, 'Chapter six. I P addressing and subnetting. These numericals are asked in every exam, so go slowly here.')

p = page('IPv4 Address & Classes', 6)
beat(p, '''An I P version four address is thirty two bits long, written as four decimal numbers separated by dots, like one ninety two dot one sixty eight dot one dot ten. Each part is one byte, from zero to two fifty five.
So there are two to the power thirty two addresses in total.''',
     T(0, '[h:IPv4] = 32 bits = 4 bytes, dotted decimal: 192.168.1.10', size=36), T(1, 'each part 0 - 255;   total 2^32 ≈ 4.3 billion addresses', size=34))
beat(p, '''In classful addressing, the first byte tells the class. Class A runs from one to one twenty six, with mask two fifty five dot zero dot zero dot zero. Class B from one twenty eight to one ninety one.
Class C from one ninety two to two twenty three. Class D, from two twenty four to two thirty nine, is for multicast. And class E is reserved. One twenty seven is used for loopback testing.''',
     Stamp(1650, 140, 'MOST ASKED'),
     Tab(180, 360, [140, 160, 260, 340, 310, 330], 56, [['Class', 'Starts', '1st byte', 'Default mask', 'Networks', 'Hosts / network'],
         ['A', '0', '1 - 126', '255.0.0.0  (/8)', '2^7 - 2 = 126', '2^24 - 2'], ['B', '10', '128 - 191', '255.255.0.0  (/16)', '2^14', '2^16 - 2 = 65,534'],
         ['C', '110', '192 - 223', '255.255.255.0  (/24)', '2^21', '2^8 - 2 = 254'], ['D', '1110', '224 - 239', 'multicast', '-', '-'], ['E', '1111', '240 - 255', 'reserved', '-', '-']],
         size=27, colors={(r, 0): 'red' for r in range(1, 6)}))
beat(p, '''In every network, the address with all host bits zero is the network address, and the address with all host bits one is the broadcast address. So usable hosts are two to the power h, minus two.''',
     T(11, 'host bits all 0 = [k:network address];  all 1 = [k:broadcast address]', size=34), T(12, 'usable hosts = [h:2^h - 2]   (127.x.x.x = loopback)', size=36, color='red'))

k_, mask_, subs = subnets('192.168.10.0/24', 4)
p = page('Subnetting Numerical', 6)
beat(p, '''Subnetting divides one network into smaller networks. Question: divide one ninety two dot one sixty eight dot ten dot zero slash twenty four into four subnets.
We need four subnets, and two to the power two is four, so we borrow two bits from the host part. The new prefix is slash twenty six.''',
     Stamp(1650, 140, 'NUMERICAL'), T(0, 'Divide 192.168.10.0/24 into 4 subnets', color='black'),
     T(1, f'2^n ≥ 4  =>  borrow [h:{k_} bits]  =>  /24 + 2 = [r:/26]', size=36))
beat(p, f'''The new mask is two fifty five dot two fifty five dot two fifty five dot one ninety two. Six host bits are left, so each subnet has sixty four addresses, and sixty two usable hosts.
The block size is two fifty six minus one ninety two, which is sixty four.''',
     T(2, f'mask = [h:{mask_}];   host bits = 6', size=36), T(3, 'block size = 256 - 192 = [h:64];   hosts = 2^6 - 2 = [h:62]', size=36))
beat(p, '''So the four subnets start at zero, sixty four, one twenty eight and one ninety two. For each one, the first address is the network address, the last is the broadcast address,
and the hosts are in between.''',
     Tab(180, 470, [330, 330, 330, 330, 330], 58, [['Subnet', 'Network', 'First host', 'Last host', 'Broadcast']] +
         [[f'{i + 1}', a, b, c, d] for i, (_, a, b, c, d) in enumerate(subs)], size=29, colors={**{(r, 1): 'blue' for r in range(1, 5)}, **{(r, 4): 'red' for r in range(1, 5)}}))

hm_, hn_, hb_, hh_, hf_, hl_ = host_info('172.16.45.14/20')
vl = vlsm()
p = page('CIDR & VLSM', 6)
beat(p, '''Classless addressing, or C I D R, writes the network part as a prefix length, like slash twenty. A common question: for the address one seventy two dot sixteen dot forty five dot fourteen slash twenty,
find the network address, the broadcast address, and the number of hosts.''',
     Stamp(1650, 140, 'NUMERICAL'), T(0, '[h:CIDR]: a.b.c.d / n   (n = network bits)', size=36), T(1, 'Find network, broadcast, hosts for 172.16.45.14/20', color='black'))
beat(p, f'''Slash twenty means the mask is two fifty five dot two fifty five dot two forty dot zero. The interesting byte is the third one, with block size two fifty six minus two forty, which is sixteen.
Forty five lies between thirty two and forty eight. So the network address is one seventy two dot sixteen dot thirty two dot zero, the broadcast is one seventy two dot sixteen dot forty seven dot two fifty five,
and there are two to the power twelve minus two, which is four thousand and ninety four hosts.''',
     T(2, f'/20  =>  mask = {hm_};   block = 256 - 240 = 16 (3rd byte)', size=34), T(3, '45 is in 32 ... 47', size=34),
     T(4, f'Network = [h:{hn_}]     Broadcast = [h:{hb_}]', size=34), T(5, f'Hosts = 2^12 - 2 = [r:{hh_:,}]   (first {hf_}, last {hl_})', size=32))
beat(p, '''Variable length subnet masking, V L S M, gives each subnet only the size it needs. Example: from one ninety two dot one sixty eight dot one dot zero slash twenty four,
make subnets for one hundred, fifty, and twenty five hosts. Always start with the biggest. One hundred hosts needs slash twenty five, fifty needs slash twenty six, and twenty five needs slash twenty seven.''',
     S(7, 'VLSM: 192.168.1.0/24 for 100, 50, 25 hosts (biggest first)', color='red', size=34),
     Tab(180, 690, [220, 420, 300, 420], 54, [['Needs', 'Subnet', 'Usable hosts', 'Broadcast']] + [[str(h), s_, str(u), b_] for h, s_, u, b_ in vl], size=29,
         colors={(r, 1): 'blue' for r in range(1, 4)}))

p = page('Private Addresses, NAT & Supernetting', 6)
beat(p, '''Some address ranges are private. They are used inside homes and offices, and are not routed on the internet: ten dot anything slash eight, one seventy two dot sixteen slash twelve,
and one ninety two dot one sixty eight slash sixteen.''',
     Stamp(1650, 140), T(0, '[h:Private]: 10.0.0.0/8,  172.16.0.0/12,  192.168.0.0/16', size=36))
beat(p, '''Network address translation, or N A T, lets many devices with private addresses share one public address. The router keeps a translation table. With port numbers, called P A T, thousands of devices can share one address.''',
     T(2, '[k:NAT]: private IPs <-> one public IP (router keeps a table)', size=34),
     Tab(180, 400, [480, 480], 54, [['Private (inside)', 'Public (outside)'], ['10.0.0.5 : 3345', '200.24.5.8 : 5001'], ['10.0.0.7 : 4012', '200.24.5.8 : 5002']], size=30),
     T(7, 'NAT + port numbers = [k:PAT] (NAT overload)', size=32, color='green'))
beat(p, f'''Supernetting is the opposite of subnetting. It joins several small networks into one bigger block. For example, the four networks two hundred dot ten dot zero to two hundred dot ten dot three,
each slash twenty four, combine into two hundred dot ten dot zero dot zero slash twenty two. The blocks must be continuous, and the first one must be a multiple of the count.''',
     T(9, '[k:Supernetting]: join contiguous blocks', size=34),
     T(10, f'200.10.0.0/24 + 200.10.1.0/24 + 200.10.2.0/24 + 200.10.3.0/24 = [h:{supernet([f"200.10.{i}.0/24" for i in range(4)])}]', size=31, color='black'))

# ===================================================================================== CH 7
p = chapter(7)
beat(p, 'Chapter seven. The I P version four header, fragmentation, I P version six, and helper protocols.')

hx0, ppb, hy0, hh = 380, 38, 270, 58
hrows = [[('VER', 4), ('HLEN', 4), ('Service type', 8), ('Total length', 16)], [('Identification', 16), ('Flags', 3), ('Fragment offset', 13)],
         [('TTL', 8), ('Protocol', 8), ('Header checksum', 16)], [('Source IP address', 32)], [('Destination IP address', 32)], [('Options + padding (0 - 40 bytes)', 32)]]
def hdr_boxes():
    out = []
    for r, row in enumerate(hrows):
        x = hx0
        for name, b in row:
            out.append(Box(x, hy0 + hh * r, b * ppb, hh, name, 'grey' if r == 5 else ('red' if name in ('Flags', 'Fragment offset', 'Identification') else 'black'), size=24)); x += b * ppb
    return out
p = page('IPv4 Header', 7)
beat(p, '''The I P version four header is twenty to sixty bytes. Each row here is thirty two bits. The version is four. H L E N is the header length in units of four bytes, so five means twenty bytes.
Total length is the whole datagram, header plus data, up to sixty five thousand five hundred and thirty five bytes.''',
     Stamp(1650, 140, 'MOST ASKED'), hdr_boxes(), *[T(0, s_, x=hx0 + b * ppb - 6, y=hy0 - 12, size=22, color='grey') for s_, b in (('0', 0), ('4', 4), ('8', 8), ('16', 16), ('31', 31.6))],
     T(8, 'header = [h:20 to 60 bytes];  HLEN × 4 = header bytes (5 => 20)', size=32), T(9, 'total length ≤ 65,535 bytes (header + data)', size=32))
beat(p, '''Identification, flags and fragment offset are used for fragmentation. Time to live, T T L, is reduced by one at every router. When it reaches zero, the packet is dropped, so packets do not loop forever.
The protocol field tells what is inside: six for T C P, seventeen for U D P, and one for I C M P.''',
     T(10, '[k:TTL]: -1 at each router; 0 => drop (no endless loops)', size=32), T(11, '[k:Protocol]: TCP = 6, UDP = 17, ICMP = 1', size=32))
beat(p, '''The header checksum covers only the header, and is recalculated at every router, because T T L changes.''',
     T(12, 'header checksum: header only, recomputed at every hop', size=32, color='green'))

per, frs = fragment(4000, 20, 1500)
p = page('IP Fragmentation Numerical', 7)
beat(p, '''When a datagram is bigger than the M T U, the maximum transmission unit of the next link, it is split into fragments. The fragment offset is counted in units of eight bytes,
so the data in every fragment except the last must be a multiple of eight. The M F flag, more fragments, is one for every fragment except the last.''',
     Stamp(1650, 140, 'NUMERICAL'), T(0, 'datagram > [k:MTU]  =>  split into fragments', size=34), T(1, 'offset in [h:8-byte units];  MF = 1 except the last fragment', size=34))
beat(p, f'''Numerical. A datagram of four thousand bytes, with a twenty byte header, goes over a link with M T U one thousand five hundred. The data is three thousand nine hundred and eighty bytes.
Each fragment can carry one thousand five hundred minus twenty, which is one thousand four hundred and eighty bytes of data. That is already a multiple of eight.''',
     T(3, '4000-byte datagram (20 header + 3980 data),  MTU = 1500', size=34, color='black'), T(4, f'data per fragment = 1500 - 20 = [h:{per}]  (multiple of 8 ✓)', size=34))
beat(p, f'''So we get three fragments. The first two carry one thousand four hundred and eighty bytes each, and the last carries one thousand and twenty. The offsets are zero, one eighty five, and three seventy,
because one thousand four hundred and eighty divided by eight is one eighty five.''',
     Tab(180, 520, [240, 260, 320, 280, 160], 58, [['Fragment', 'Data', 'Total length', 'Offset', 'MF']] + [[str(i + 1), str(d), str(t), str(o), str(m)] for i, (d, t, o, m) in enumerate(frs)],
         size=30, colors={**{(r, 3): 'red' for r in range(1, 4)}}),
     T(0, 'offset = bytes before / 8', x=1500, y=620, size=30, color='green'), T(0, '1480 / 8 = 185', x=1500, y=670, size=30, color='green'), T(0, '2960 / 8 = 370', x=1500, y=720, size=30, color='green'))

p = page('IPv6', 7)
beat(p, '''I P version six was made because I P version four addresses ran out. It uses one hundred and twenty eight bit addresses, written as eight groups of four hexadecimal digits.
To shorten it, leading zeros in a group can be dropped, and one run of all zero groups can be replaced by a double colon, but only once.''',
     T(0, '[h:IPv6] = 128 bits, 8 groups of 4 hex digits', size=36), M(180, L(1) + 4, '2001:0DB8:0000:0000:0000:0000:1428:57AB', size=32),
     M(180, L(2) + 8, '=> 2001:DB8::1428:57AB', size=32, color='red'), T(3, 'drop leading zeros;  [r:::] only once', size=32, color='green'))
beat(p, '''The I P version six header is fixed at forty bytes. There is no header checksum, and routers do not fragment, only the source does. It has a flow label for real time traffic,
and extension headers for options. There is no broadcast. Instead it has unicast, multicast and anycast.''',
     Stamp(1650, 140),
     Tab(180, 440, [420, 520, 560], 52, [['', 'IPv4', 'IPv6'], ['address', '32 bits', '128 bits'], ['header', '20 - 60 bytes', '40 bytes (fixed)'], ['checksum', 'yes', 'no'],
         ['fragmentation', 'sender & routers', 'sender only'], ['broadcast', 'yes', 'no (anycast, multicast)'], ['config', 'manual / DHCP', 'auto (SLAAC) / DHCPv6']], size=28,
         colors={(r, 0): 'red' for r in range(1, 7)}))
beat(p, '''To move from version four to version six, we use three methods: dual stack, where devices run both, tunnelling, where version six packets travel inside version four packets, and header translation.''',
     T(14, 'Transition: [k:dual stack], [k:tunnelling], [k:header translation]', size=34))

p = page('ARP, ICMP & DHCP', 7)
beat(p, '''Some helper protocols work with I P. A R P, address resolution protocol, finds the M A C address for a given I P address. The request is broadcast to everyone, and the reply is unicast.
R A R P does the reverse. I C M P sends error and query messages. Ping uses I C M P echo request and reply, and traceroute uses time exceeded messages.''',
     Stamp(1650, 140, 'MOST ASKED'),
     Tab(180, 240, [180, 1000], 56, [['Protocol', 'Job'], ['ARP', 'IP address -> MAC address  (request broadcast, reply unicast)'], ['RARP', 'MAC -> IP (old; replaced by DHCP)'],
         ['ICMP', 'error & query messages: ping (echo), traceroute (TTL exceeded)'], ['IGMP', 'manages multicast group membership'],
         ['DHCP', 'gives IP address automatically (UDP ports 67 / 68)']], size=29, colors={(r, 0): 'red' for r in range(1, 6)}))
beat(p, '''D H C P gives a device its I P address automatically, in four steps, remembered as D O R A. Discover, which is broadcast by the client. Offer, from the server. Request, from the client. And acknowledgement, from the server.''',
     Life(1100, 640, 980, 'Client'), Life(1640, 640, 980, 'Server'),
     Msg(1100, 1640, 690, 'D: Discover (broadcast)', 'blue'), Msg(1640, 1100, 760, 'O: Offer', 'green'), Msg(1100, 1640, 830, 'R: Request', 'blue'), Msg(1640, 1100, 900, 'A: Acknowledge', 'green'),
     T(10, '[h:DHCP = DORA]', size=40, color='red'), T(11, 'Discover, Offer,', size=34), T(12, 'Request, Acknowledge', size=34))

# ===================================================================================== CH 8
p = chapter(8)
beat(p, 'Chapter eight. Routing algorithms. How a router finds the best path.')

p = page('Routing Basics: RIP, OSPF & BGP', 8)
beat(p, '''Routing finds the best path for packets. Forwarding is the act of sending a packet to the next hop using the routing table. Static routing is set by hand, and dynamic routing updates automatically.
Inside one organisation, called an autonomous system, we use intra domain protocols like R I P and O S P F. Between autonomous systems, we use the inter domain protocol B G P.''',
     T(0, '[k:Routing]: find best path;  [k:Forwarding]: send to next hop (table lookup)', size=33), T(1, 'static (manual) vs dynamic (automatic)', size=33),
     T(2, 'intra-domain (inside an AS): RIP, OSPF;   inter-domain (between ASes): BGP', size=33))
beat(p, '''R I P uses distance vector with hop count, and a maximum of fifteen hops. O S P F uses link state with Dijkstra's algorithm. B G P uses path vector.''',
     Stamp(1650, 140, 'MOST ASKED'),
     Tab(180, 420, [200, 380, 360, 520], 56, [['', 'RIP', 'OSPF', 'BGP'], ['type', 'distance vector', 'link state', 'path vector'], ['metric', 'hop count (max 15)', 'cost (bandwidth)', 'policy, AS path'],
         ['algorithm', 'Bellman-Ford', 'Dijkstra', 'path vector'], ['runs on', 'UDP 520', 'IP directly', 'TCP 179'], ['scope', 'small networks', 'large AS (areas)', 'between ASes']], size=28,
         colors={(r, 0): 'red' for r in range(1, 6)}))
beat(p, '''Flooding is the simplest method: send every packet on every link. It always finds the path, but creates a lot of duplicates.''',
     T(14, '[k:Flooding]: send on all links; reliable but many duplicates', size=32, color='green'))

dist, prev, dsteps = dijkstra()
gp = {'A': (1180, 620), 'B': (1420, 400), 'C': (1420, 840), 'D': (1700, 400), 'E': (1800, 760)}
p = page("Dijkstra's Algorithm (Link State)", 8)
beat(p, '''In link state routing, every router learns the full map of the network, and runs Dijkstra's shortest path algorithm. Let's find the shortest paths from A in this network.
Start with A. Its neighbours B and C get distances four and two. The rest are infinity.''',
     Stamp(1650, 140, 'NUMERICAL'), T(0, 'Link state: every router knows the full map  =>  Dijkstra', size=34),
     *[Node(gp[v], v) for v in gp], *sum([WEdge(gp[a], gp[b], w) for a in G for b, w in G[a].items() if a < b], []))
inf = lambda c: '∞' if c[0] == math.inf else f'{c[0]}, {c[1]}'
beat(p, '''At each step, pick the unvisited node with the smallest distance, and update its neighbours. C has two, so we visit C. Through C, B becomes three, D becomes ten, and E becomes twelve.
Next B has three. Through B, D improves to eight. Then D, and through D, E improves to ten. Finally E.''',
     Tab(180, 300, [100, 170, 150, 150, 150, 150], 56, [['Step', 'Visited', 'B', 'C', 'D', 'E']] + [[str(i + 1), vis, *[inf(t[v]) for v in 'BCDE']] for i, (vis, t) in enumerate(dsteps)],
         size=27, colors={(i + 1, 2 + 'BCDE'.index(vis[-1])): 'red' for i, (vis, t) in enumerate(dsteps) if vis[-1] != 'A'}))
beat(p, f'''So the shortest paths from A are: to C, cost two. To B, through C, cost three. To D, through C and B, cost eight. And to E, through C, B and D, cost ten.''',
     *[T(10 + i, f'A -> {v}:  {path(prev, v)}  = [h:{dist[v]}]', size=32, color='black') for i, v in enumerate('CBDE')])

dv = dv_update()
p = page('Distance Vector Routing', 8)
beat(p, '''In distance vector routing, each router knows only its neighbours. Every router sends its distance vector, its list of distances to all destinations, to its neighbours.
Then each router updates its table using the Bellman Ford equation: the distance from x to y is the minimum, over all neighbours v, of the cost to v plus v's distance to y.''',
     Stamp(1650, 140, 'NUMERICAL'), T(0, 'share your distance vector with neighbours only', size=34), T(1, '[h:D_x(y) = min over v { c(x, v) + D_v(y) }]', size=40, color='red'))
beat(p, '''Example. Router A has neighbours B, with cost one, and C, with cost four. A receives these vectors from B and C. To reach D: through B, it is one plus six, which is seven. Through C, it is four plus one, which is five.
So A reaches D at cost five, through C.''',
     T(3, 'A: c(A, B) = 1,  c(A, C) = 4', size=34, color='black'),
     Tab(180, 430, [170, 130, 130, 130, 130], 54, [['vector', 'A', 'B', 'C', 'D'], ['from B', '1', '0', '2', '6'], ['from C', '4', '2', '0', '1']], size=30),
     Tab(1000, 430, [170, 330, 140, 180], 54, [['to', 'via B, via C', 'cost', 'next hop']] + [[t, c_, str(cost), n_] for t, cost, n_, c_ in dv[1:]], size=30,
         colors={(3, 2): 'red', (3, 3): 'red'}), T(0, "A's new table", x=1000, y=410, size=30, font='bold', color='black'))
beat(p, '''The big problem with distance vector is count to infinity. When a link breaks, bad news travels slowly, and routers keep increasing the distance step by step. The fixes are split horizon,
poison reverse, and hold down timers. R I P limits the count by treating sixteen hops as infinity.''',
     T(10, '[r:Count-to-infinity]: good news fast, bad news slow', size=34), T(11, 'fixes: [k:split horizon], [k:poison reverse], hold-down;  RIP: 16 = ∞', size=34),
     T(13, 'DV: neighbours only, periodic, slow convergence;  LS: full map, flooding, fast', size=30, color='green'))

# ===================================================================================== CH 9
p = chapter(9)
beat(p, 'Chapter nine. The transport layer. T C P and U D P.')

p = page('Transport Layer: UDP vs TCP', 9)
beat(p, '''The transport layer gives process to process delivery. A port number, sixteen bits, identifies the process. Well known ports are zero to one thousand and twenty three.
An I P address plus a port number is called a socket.''',
     T(0, 'process-to-process delivery;  [k:port] = 16 bits (0 - 65535)', size=34), T(1, 'well-known 0 - 1023;  registered 1024 - 49151;  dynamic 49152 - 65535', size=32),
     T(2, '[h:Socket = IP address + port number]', size=36))
beat(p, '''U D P is simple and fast. It is connectionless and unreliable, with no acknowledgements and no ordering. Its header is just eight bytes: source port, destination port, length and checksum.
It is used for D N S, video streaming, online games and V o I P.''',
     Stamp(1650, 140, 'MOST ASKED'),
     Tab(180, 400, [400, 620, 620], 54, [['', 'UDP', 'TCP'], ['connection', 'connectionless', 'connection-oriented'], ['reliable', 'no', 'yes (ACK, retransmit)'],
         ['order', 'not guaranteed', 'in order (seq. numbers)'], ['header', '[h:8 bytes]', '[h:20 - 60 bytes]'], ['flow & congestion', 'no', 'yes'],
         ['used by', 'DNS, streaming, games, VoIP', 'HTTP, FTP, SMTP, SSH']], size=28, colors={(r, 0): 'red' for r in range(1, 7)}))
beat(p, '''T C P is connection oriented and reliable. It uses sequence numbers, acknowledgements, retransmission, flow control and congestion control. Its header is twenty to sixty bytes.
T C P is a byte stream, so sequence numbers count bytes, not segments.''',
     T(14, 'TCP: byte stream => sequence numbers count [h:bytes]', size=34, color='green'))

cx_, sx_ = 1180, 1680
p = page('TCP Header & Connection', 9)
beat(p, '''The T C P header has source and destination ports, a thirty two bit sequence number, a thirty two bit acknowledgement number, the header length, six flags, the window size, the checksum, and the urgent pointer.
The flags are U R G, A C K, P S H, R S T, S Y N and F I N.''',
     T(0, 'ports · seq. no (32) · ack no (32) · HLEN · flags · window · checksum · urgent ptr', size=30),
     T(1, 'flags: URG  ACK  PSH  RST  [h:SYN]  [h:FIN]', size=34))
beat(p, '''A connection starts with a three way handshake. The client sends S Y N with sequence number x. The server replies with S Y N plus A C K, with its own sequence number y, and acknowledgement x plus one.
Then the client sends A C K with acknowledgement y plus one. A S Y N uses up one sequence number, even though it carries no data.''',
     Stamp(1650, 140, 'MOST ASKED'), Life(cx_, 420, 760, 'Client'), Life(sx_, 420, 760, 'Server'),
     Msg(cx_, sx_, 470, 'SYN, seq = x', 'blue'), Msg(sx_, cx_, 560, 'SYN + ACK, seq = y, ack = x + 1', 'green'), Msg(cx_, sx_, 650, 'ACK, ack = y + 1', 'blue'),
     T(4, '[h:3-way handshake]', size=38, color='red'), T(5, 'SYN -> SYN+ACK -> ACK', size=34), T(6, 'SYN consumes 1 seq. number', size=32, color='green'))
beat(p, '''Closing takes four steps: F I N, A C K, F I N, A C K, because each side closes its own direction. The side that closes first waits in the time wait state, for two times the maximum segment lifetime.''',
     T(12, 'Close: [k:FIN -> ACK -> FIN -> ACK] (4-way);  TIME_WAIT = 2 × MSL', size=32))

cw = tcp_cwnd(16, 16, loss_at=10)
gx0, gy0, gdx, gdy = 1060, 860, 46, 22
gpts = [(gx0 + gdx * (r + 1), gy0 - gdy * v) for r, v in enumerate(cw)]
p = page('TCP Congestion Control', 9)
beat(p, '''T C P controls congestion with a congestion window, c w n d. In slow start, c w n d starts at one segment and doubles every round trip time, until it reaches the threshold, s s thresh.
After that, in congestion avoidance, it grows by just one segment per round trip.''',
     Stamp(1650, 140, 'NUMERICAL'), T(0, '[h:Slow start]: cwnd = 1, 2, 4, 8 ... (doubles each RTT)', size=33), T(1, '[h:Congestion avoidance]: after ssthresh, +1 per RTT', size=33),
     T(2, 'sender window = min(cwnd, rwnd)', size=32, color='green'))
beat(p, '''Numerical. s s thresh is sixteen, and a timeout happens in round ten. The window goes one, two, four, eight, sixteen, then seventeen, eighteen, nineteen, twenty, twenty one.
On the timeout, s s thresh becomes half of twenty one, which is ten, and c w n d goes back to one.''',
     Ln([(gx0, gy0), (gx0 + gdx * 17, gy0)], 'black', 3), Ln([(gx0, gy0), (gx0, gy0 - gdy * 23)], 'black', 3),
     T(0, 'RTT', x=gx0 + gdx * 17 - 20, y=gy0 + 40, size=26, color='black'), T(0, 'cwnd', x=gx0 - 80, y=gy0 - gdy * 23 + 10, size=26, color='black'),
     *[T(0, str(r), x=gx0 + gdx * r - 8, y=gy0 + 34, size=22, color='grey') for r in (1, 5, 10, 15)],
     *Dash(gx0, gy0 - gdy * 16, gx0 + gdx * 10, gy0 - gdy * 16), T(0, 'ssthresh 16', x=gx0 + 4, y=gy0 - gdy * 16 - 8, size=22, color='grey'),
     Ln(gpts[:10], 'blue', 4), *[Ell(x - 6, y - 6, 12, 12, None, 'blue') for x, y in gpts[:10]],
     T(0, '21', x=gpts[9][0] - 10, y=gpts[9][1] - 14, size=24, color='red'),
     T(4, 'ssthresh = 16, timeout at RTT 10', size=32, color='black'), T(5, ' '.join(map(str, cw[:10])), size=32))
beat(p, '''After the timeout, slow start begins again: one, two, four, eight, and then ten, because it cannot jump past the new threshold. Then eleven, in congestion avoidance.
This is T C P Tahoe. In T C P Reno, on three duplicate acknowledgements, c w n d drops only to the new threshold, which is called fast recovery.''',
     *Dash(gx0 + gdx * 11, gy0 - gdy * 10, gx0 + gdx * 16, gy0 - gdy * 10, 'red'), T(0, 'new ssthresh 10', x=gx0 + gdx * 11, y=gy0 - gdy * 10 - 10, size=22, color='red'),
     Ln(gpts[10:], 'green', 4), *[Ell(x - 6, y - 6, 12, 12, None, 'green') for x, y in gpts[10:]],
     T(6, 'timeout:  ssthresh = 21 / 2 = [h:10],  cwnd = [h:1]', size=32), T(7, 'then ' + ' '.join(map(str, cw[10:])), size=32),
     T(9, '[k:Tahoe]: timeout or 3 dup ACKs => cwnd = 1', size=30), T(10, '[k:Reno]: 3 dup ACKs => cwnd = ssthresh', size=30), T(11, '(fast retransmit + fast recovery)', size=30))

# ===================================================================================== CH 10
p = chapter(10)
beat(p, 'Chapter ten. Congestion control and quality of service. The leaky bucket and the token bucket.')

S_, burst = token_bucket(1e6, 2e6, 10e6)
p = page('Leaky Bucket & Token Bucket', 10)
beat(p, '''Traffic shaping controls the rate of data sent into the network. In the leaky bucket algorithm, packets enter a bucket and leave at a constant rate, like water from a hole in a bucket.
Bursts are smoothed out, and if the bucket is full, packets are dropped.''',
     T(0, '[h:Leaky bucket]: output at a [r:constant rate]; bursts smoothed; full => drop', size=33),
     Ln([(1300, 320), (1340, 520), (1480, 520), (1520, 320)], 'blue', 5), T(0, 'bursty in', x=1330, y=300, size=26, color='black'),
     Arr(1410, 520, 1410, 600, 'blue'), T(0, 'constant out', x=1440, y=580, size=26, color='blue'))
beat(p, '''In the token bucket algorithm, tokens are added to the bucket at a fixed rate. Sending data uses tokens. If the bucket has saved tokens, the host can send a burst at full speed.
So token bucket allows bursts, but leaky bucket does not.''',
     T(3, '[h:Token bucket]: tokens added at rate ρ, capacity C;  [g:allows bursts]', size=33))
beat(p, f'''Numerical. Bucket capacity is one megabit, the token rate is two megabits per second, and the maximum output rate is ten megabits per second. The maximum burst time is capacity divided by
output rate minus token rate. That is one divided by ten minus two, which is zero point one two five seconds, or one hundred and twenty five milliseconds. In that time, one point two five megabits are sent.''',
     Stamp(1650, 140, 'NUMERICAL'), T(5, '[h:S = C / (M - ρ)]', size=40, color='red'), T(6, 'C = 1 Mb,  ρ = 2 Mbps,  M = 10 Mbps', size=34, color='black'),
     T(7, f'S = 1 / (10 - 2) = [h:{S_:.3f} s = {S_ * 1000:.0f} ms]', size=36), T(8, f'burst data = M × S = 10 × 0.125 = [r:{burst / 1e6:.2f} Mb]', size=34),
     Tab(180, 760, [380, 520, 520], 54, [['', 'Leaky bucket', 'Token bucket'], ['bursts', 'not allowed', 'allowed (saved tokens)'], ['when full', 'drops packets', 'drops tokens']], size=28))

p = page('Congestion Control Techniques & QoS', 10)
beat(p, '''Congestion happens when too many packets are in the network, and routers start dropping them. Open loop methods try to prevent congestion before it happens:
good retransmission, window, acknowledgement and discard policies, and admission control.''',
     T(0, '[h:Open loop] (prevention): retransmission, window, ACK, discard policy; admission control', size=31))
beat(p, '''Closed loop methods remove congestion after it happens. In back pressure, a congested router stops accepting from the router before it. A choke packet is sent directly to the source to slow down.
With implicit signalling, the source guesses from delays or lost acknowledgements. And with explicit signalling, routers set a bit in the packets.''',
     Stamp(1650, 140), T(2, '[h:Closed loop] (removal):', size=34), N(3, 1, 'backpressure (hop by hop, towards the source)', size=32), N(4, 2, 'choke packet (sent to the source)', size=32),
     N(5, 3, 'implicit signalling (delay, lost ACKs)', size=32), N(6, 4, 'explicit signalling (bit in packet: ECN)', size=32))
beat(p, '''Quality of service measures how good the network is for an application. The four parameters are reliability, delay, jitter, which is variation in delay, and bandwidth.
Video calls need low delay and low jitter, while file transfer needs high reliability.''',
     T(9, '[k:QoS]: reliability, delay, [h:jitter] (variation in delay), bandwidth', size=33), T(10, 'video call: low delay & jitter;  file transfer: reliability', size=32, color='green'))

# ===================================================================================== CH 11
p = chapter(11)
beat(p, 'Chapter eleven. The application layer, and network security.')

dns_nodes = {'root': (1320, 300, 'root', 'red', 120), 'com': (1080, 450, '.com', 'blue', 110), 'in': (1320, 450, '.in', 'blue', 100), 'org': (1560, 450, '.org', 'blue', 110),
             'g': (1080, 600, 'google', 'green', 140), 'ac': (1320, 600, 'ac', 'green', 100), 'pu': (1320, 750, 'pondiuni', 'green', 160)}
def dns_tree():
    out = []; done = set()
    def ell(n): cx, cy, lab, col, w = dns_nodes[n]; return Ell(cx - w / 2, cy - 28, w, 56, lab, color=col, size=26, lc=col)
    for a, b in [('root', 'com'), ('root', 'in'), ('root', 'org'), ('com', 'g'), ('in', 'ac'), ('ac', 'pu')]:
        for n in (a, b):
            if n not in done: out.append(ell(n)); done.add(n)
        out.append(Ln([(dns_nodes[a][0], dns_nodes[a][1] + 30), (dns_nodes[b][0], dns_nodes[b][1] - 30)], 'black', 3))
    return out
p = page('DNS: Domain Name System', 11)
beat(p, '''D N S converts a domain name, like google dot com, into an I P address. It is a distributed, hierarchical database. At the top are the root servers. Below them are top level domains,
like dot com, dot org and dot in. Below those are the authoritative servers for each domain.''',
     T(0, '[h:DNS]: name -> IP address  (UDP port 53)', size=36), T(1, 'hierarchy: root -> TLD -> authoritative', size=34), dns_tree())
beat(p, '''There are two ways to resolve a name. In recursive resolution, each server asks the next server for you, and returns the final answer. In iterative resolution,
each server only tells you which server to ask next. D N S mostly uses U D P port fifty three.''',
     Stamp(1650, 140, 'MOST ASKED'), T(4, '[k:Recursive]: server finds the full answer for you', size=32), T(5, '[k:Iterative]: server says "ask that server next"', size=32))
beat(p, '''Common D N S records: A gives an I P version four address, quad A gives version six, M X gives the mail server, C name, the canonical name, gives an alias, and N S gives the name server.''',
     T(8, 'Records: [k:A] (IPv4), [k:AAAA] (IPv6), [k:MX] (mail), [k:CNAME] (alias), [k:NS]', size=32))

p = page('HTTP, FTP & Email', 11)
beat(p, '''H T T P is the protocol of the web. It is stateless, so it does not remember earlier requests. Cookies are used to remember users. It runs on T C P port eighty, and H T T P S uses port four four three.
In non persistent H T T P, a new T C P connection is opened for every object, which costs two round trips per object. Persistent H T T P keeps the connection open.''',
     T(0, '[h:HTTP]: stateless (cookies keep state);  port 80, HTTPS 443', size=33), T(1, 'non-persistent: new TCP connection per object (2 RTT each);  persistent: reuse', size=30),
     T(2, 'GET, POST, PUT, DELETE, HEAD;  200 OK, 301 moved, 404 not found, 500 error', size=30))
beat(p, '''F T P transfers files using two connections. The control connection on port twenty one stays open, and the data connection on port twenty opens for each file.
For email, S M T P pushes mail from the sender to the mail server, on port twenty five. To read mail, P O P three downloads it, and usually deletes it from the server, while I M A P keeps mail on the server.''',
     T(4, '[h:FTP]: 2 connections: control port 21 (persistent), data port 20', size=33),
     T(5, '[h:Email]: SMTP = send / push (25);  POP3 = download (110);  IMAP = keep on server (143)', size=31))
beat(p, '''Here are the port numbers you must remember.''',
     Stamp(1650, 140, 'MOST ASKED'),
     Tab(180, 560, [240, 150, 240, 150, 240, 150], 56, [['Protocol', 'Port', 'Protocol', 'Port', 'Protocol', 'Port'], ['FTP', '20, 21', 'DNS', '53', 'POP3', '110'],
         ['SSH', '22', 'DHCP', '67, 68', 'IMAP', '143'], ['Telnet', '23', 'HTTP', '80', 'SNMP', '161'], ['SMTP', '25', 'HTTPS', '443', 'BGP', '179']], size=29,
         colors={**{(r, 1): 'red' for r in range(1, 5)}, **{(r, 3): 'red' for r in range(1, 5)}, **{(r, 5): 'red' for r in range(1, 5)}}))

rs = rsa(3, 11, 7, 4)
p = page('Cryptography & RSA', 11)
beat(p, '''Cryptography keeps data secret. In symmetric key cryptography, the same secret key is used to encrypt and decrypt, like D E S and A E S. It is fast, but the key must be shared safely.
In asymmetric, or public key cryptography, each person has a public key and a private key. Data encrypted with the public key can only be decrypted with the private key. R S A is the famous example.''',
     T(0, '[k:Symmetric]: same key (DES, AES), fast;  key sharing is the problem', size=32), T(1, '[k:Asymmetric]: public key encrypts, private key decrypts (RSA)', size=32))
beat(p, f'''R S A numerical. Take p equals three and q equals eleven. n is p times q, which is thirty three. Phi of n is p minus one times q minus one, which is twenty. Choose e equals seven,
which has no common factor with twenty. Then find d so that e times d leaves remainder one when divided by twenty. Seven times three is twenty one, so d equals three.''',
     Stamp(1650, 140, 'NUMERICAL'), T(3, f'p = 3, q = 11  =>  n = [h:{rs["n"]}],  φ(n) = 2 × 10 = [h:{rs["phi"]}]', size=34),
     T(4, f'e = 7  (gcd(7, 20) = 1);   e × d mod 20 = 1  =>  d = [h:{rs["d"]}]  (7 × 3 = 21)', size=34),
     T(5, f'public key = (7, 33);   private key = ({rs["d"]}, 33)', size=34, color='green'))
beat(p, f'''To encrypt the message four: C equals four to the power seven mod thirty three. Four to the power seven is sixteen thousand three hundred and eighty four, which gives sixteen.
To decrypt: sixteen to the power three mod thirty three is four thousand and ninety six mod thirty three, which is four. We get the message back. Digital signatures use the reverse:
sign with the private key, and verify with the public key. And a firewall filters traffic between a trusted network and the internet.''',
     T(7, f'Encrypt M = 4:  C = 4^7 mod 33 = 16384 mod 33 = [r:{rs["c"]}]', size=34), T(8, f'Decrypt:  M = 16^3 mod 33 = 4096 mod 33 = [r:{rs["back"]}] ✓', size=34),
     T(10, '[k:Digital signature]: sign with private key, verify with public key', size=32), T(11, '[k:Firewall]: filters packets between trusted network & internet', size=32))

# ===================================================================================== CH 12
p = chapter(12)
beat(p, "Chapter twelve. Exam revision. If you're short on time, revise this formula sheet first.")

p = page('Formula Sheet', 12)
beat(p, '''Here are all the formulas in one place. Delays: transmission delay is L over B, and propagation delay is d over v. Bandwidth delay product is B times propagation delay.
Nyquist: two B log two L. Shannon: B log two of one plus S N R.''',
     Stamp(1650, 140, 'MOST ASKED'), T(0, 'Tt = L / B   ·   Tp = d / v   ·   BDP = B × Tp', size=34), T(1, 'Nyquist = 2B log2 L   ·   Shannon C = B log2(1 + SNR)', size=34))
beat(p, '''Flow control: a is propagation over transmission delay. Stop and wait efficiency is one over one plus two a, and sliding window efficiency is W over one plus two a.
Go back N window is two to the k minus one, and selective repeat is two to the k minus one, halved.''',
     T(3, 'a = Tp / Tt   ·   η(SW) = 1 / (1 + 2a)   ·   η = W / (1 + 2a)', size=34), T(4, 'GBN: W ≤ 2^k - 1   ·   SR: W ≤ 2^(k-1)', size=34))
beat(p, '''Access control: pure ALOHA throughput is G e to the minus two G, with maximum eighteen point four percent. Slotted ALOHA is G e to the minus G, with maximum thirty six point eight percent.
C S M A C D minimum frame size is two times propagation delay times bandwidth.''',
     T(6, 'Pure ALOHA: G e^(-2G), max 18.4%   ·   Slotted: G e^(-G), max 36.8%', size=34), T(7, 'CSMA/CD: L_min = 2 × Tp × B', size=34))
beat(p, '''Errors and addressing: Hamming code needs two to the r at least m plus r plus one. Detecting s errors needs distance s plus one, and correcting t errors needs two t plus one.
Usable hosts are two to the h minus two. Token bucket burst time is C over M minus rho. And fragment offset is bytes before divided by eight.''',
     T(9, 'Hamming: 2^r ≥ m + r + 1   ·   detect s: d = s + 1   ·   correct t: d = 2t + 1', size=33), T(10, 'hosts = 2^h - 2   ·   subnets = 2^borrowed bits', size=34),
     T(11, 'Token bucket: S = C / (M - ρ)   ·   offset = bytes before / 8', size=34), T(12, 'Mesh links = n(n - 1) / 2', size=34))

p = page('Most Asked Exam Questions', 12)
qs = ['OSI vs TCP/IP; network devices', 'Delays & bandwidth-delay product', 'Nyquist & Shannon numericals', 'CRC & Hamming code numericals',
      'Stop & wait, GBN, SR efficiency', 'Pure vs slotted ALOHA; CSMA/CD frame size', 'Subnetting, CIDR & VLSM', 'IPv4 header & fragmentation; IPv6',
      'Dijkstra & distance vector routing', 'TCP vs UDP; 3-way handshake', 'TCP congestion window numerical', 'Token bucket; DNS; ports; RSA']
beat(p, '''Here are the most asked questions. O S I versus T C P slash I P. Delay calculations. Nyquist and Shannon. And C R C with Hamming code.''', *[T(k, f'{k + 1}. {q}', x=200, size=36) for k, q in enumerate(qs[:4])])
beat(p, '''Sliding window efficiency. ALOHA and C S M A C D. Subnetting and C I D R. And fragmentation with I P version six.''',
     *[T(k, f'{k + 1}. {q}', x=200, size=36) for k, q in enumerate(qs) if 4 <= k < 8])
beat(p, '''Routing with Dijkstra and distance vector. T C P versus U D P and the handshake. The congestion window numerical. And token bucket, D N S, port numbers and R S A.''',
     *[T(k, f'{k + 1}. {q}', x=200, size=36) for k, q in enumerate(qs) if k >= 8])
beat(p, '''One last exam tip. For every numerical, first write the formula, then put in the values with units, and box the final answer. Convert all units before you start.
That way you get step marks even if the final number is a little off.''',
     T(13, 'Tip: [h:formula -> values with units -> boxed answer] => full marks!', color='red'))

p = page('All the Best!', 12, kind='outro')
beat(p, '''That's the complete computer networks subject. If this helped you, share it with your friends who have the exam,
and subscribe to TechVibe24 for more one shot videos. Tell me in the comments which subject you want next. All the best for your exam!''')

if __name__ == '__main__':
    json.dump({'pages': PAGES, 'chapters': CHAPTERS}, open('cn_script.json', 'w'), indent=1, ensure_ascii=False)
    nb = sum(len(p['beats']) for p in PAGES); nw = sum(len(b['say'].split()) for p in PAGES for b in p['beats'])
    print('pages', len(PAGES), 'beats', nb, 'words', nw, 'est minutes', round(nw / 150, 1))
