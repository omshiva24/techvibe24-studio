'''Software Engineering one-shot: narration beats + handwritten note elements for every page.
Markup inside text: [r:red] [g:green] [k:black] [h:yellow highlight] [p:pink highlight]'''
import json, math
from se_numericals import *

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
def Box(x, y, w, h, label=None, color='black', size=32, fill=None, lc=None): return dict(t='rect', x=x, y=y, w=w, h=h, label=label, color=color, size=size, fill=fill, lc=lc or color)
def Ell(x, y, w, h, label=None, color='black', size=32, fill=None, lc=None): return dict(t='ellipse', x=x, y=y, w=w, h=h, label=label, color=color, size=size, fill=fill, lc=lc or color)
def Arr(x1, y1, x2, y2, color='black', label=None, lx=0, ly=-14, curve=0, head=True, size=28, both=False, lc=None): return dict(t='arrow', p1=(round(x1), round(y1)), p2=(round(x2), round(y2)), color=color, label=label, lx=lx, ly=ly, curve=curve, head=head, size=size, both=both, lc=lc or color)
def Ln(pts, color='black', w=4): return dict(t='line', pts=[(round(a), round(b)) for a, b in pts], color=color, w=w)
def Tab(x, y, cw, rh, rows, color='black', size=30, hdr=True, order='row', colors=None, fills=None): return dict(t='table', x=x, y=y, cw=cw, rh=rh, rows=rows, color=color, size=size, hdr=hdr, order=order, colors={f'{r},{c}': v for (r, c), v in (colors or {}).items()}, fills={f'{r},{c}': v for (r, c), v in (fills or {}).items()})
def Stamp(x, y, text='IMP!', color='red', rot=-8, size=34): return dict(t='stamp', x=x, y=y, text=text, color=color, rot=rot, size=size)
def Dash(x1, y1, x2, y2, color='black', seg=18, gap=12, w=3):
    d = math.hypot(x2 - x1, y2 - y1); n = int(d // (seg + gap)) + 1; out = []
    for i in range(n):
        a = i * (seg + gap) / d; b = min(1, (i * (seg + gap) + seg) / d)
        if a < 1: out.append(Ln([(x1 + (x2 - x1) * a, y1 + (y2 - y1) * a), (x1 + (x2 - x1) * b, y1 + (y2 - y1) * b)], color, w))
    return out
def Actor(cx, top, name, color='black', size=28):
    return [Ell(cx - 22, top, 44, 44, None, color=color), Ln([(cx, top + 44), (cx, top + 110)], color, 4), Ln([(cx - 40, top + 66), (cx + 40, top + 66)], color, 4),
            Ln([(cx - 34, top + 160), (cx, top + 110), (cx + 34, top + 160)], color, 4), T(0, name, x=cx - len(name) * size * .23, y=top + 200, size=size, color=color)]
def Cls(x, y, w, name, attrs, methods, color='black', size=26, rh=36):
    h1 = 50; h2 = max(1, len(attrs)) * rh + 10; h3 = max(1, len(methods)) * rh + 10
    out = [Box(x, y, w, h1, name, color=color, size=size + 2), Box(x, y + h1, w, h2), Box(x, y + h1 + h2, w, h3)]
    out += [T(0, a_, x=x + 8, y=y + h1 + 32 + i * rh, size=size, color='blue') for i, a_ in enumerate(attrs)]
    out += [T(0, m_, x=x + 8, y=y + h1 + h2 + 32 + i * rh, size=size, color='blue') for i, m_ in enumerate(methods)]
    return out, y + h1 + h2 + h3
def Tree(nodes, edges, w=70, h=56, size=28, head=False, ecol='black'):
    def ell(n):
        cx, cy, lab, col, *ww = nodes[n]; nw = ww[0] if ww else w
        return Ell(cx - nw / 2, cy - h / 2, nw, h, lab, color=col, size=size, lc=col)
    def rim(n, dx, dy):
        cx, cy, lab, col, *ww = nodes[n]; nw = ww[0] if ww else w; a, b = nw / 2 + 4, h / 2 + 4
        k = 1 / math.sqrt((dx / a) ** 2 + (dy / b) ** 2); return cx + dx * k, cy + dy * k
    out = [ell(edges[0][0])]; done = {edges[0][0]}
    for a, b in edges:
        dx, dy = nodes[b][0] - nodes[a][0], nodes[b][1] - nodes[a][1]
        x1, y1 = rim(a, dx, dy); x2, y2 = rim(b, -dx, -dy)
        out.append(Arr(x1, y1, x2, y2, head=head, color=ecol))
        if b not in done: out.append(ell(b)); done.add(b)
    return out
def f2(v): return f'{v:,.2f}'

CHAPTERS = [
 (1, 'Introduction to Software Engineering', ['What is software engineering', 'Software characteristics', 'Software crisis', 'SDLC phases'], 4),
 (2, 'SDLC Models', ['Waterfall & iterative waterfall', 'Prototyping, incremental, RAD', 'Spiral model', 'V-model & comparison'], 5),
 (3, 'Agile Development', ['Agile manifesto', 'Scrum framework', 'XP, Kanban & DevOps'], 4),
 (4, 'Requirements Engineering', ['Feasibility & elicitation', 'Functional vs non-functional', 'SRS document', 'DFD, data dictionary, decision table'], 5),
 (5, 'Software Design', ['Design concepts', 'Cohesion', 'Coupling', 'Architecture & structure chart'], 5),
 (6, 'UML Diagrams', ['Use case diagram', 'Class diagram', 'Sequence & activity diagrams'], 4),
 (7, 'Software Metrics', ['LOC & Halstead', 'Function points', 'Cyclomatic complexity'], 5),
 (8, 'Software Testing', ['Testing basics', 'Levels of testing', 'Black-box: EP & BVA', 'White-box testing'], 5),
 (9, 'Project Management & Estimation', ['COCOMO', 'CPM & PERT', 'Risk management'], 5),
 (10, 'Quality, Reliability & Maintenance', ['SQA & ISO 9001', 'CMM levels', 'Reliability', 'Maintenance & SCM'], 5),
 (11, 'Exam Revision', ['Most asked questions', 'Last-minute tips'], 5),
]
def chapter(i):
    n, t, subs, stars = CHAPTERS[i - 1]
    return page(t, n, kind='chapter', num=n, subs=subs, stars=stars)

# =====================================================================================
p = page('Software Engineering', 0, kind='cover')
beat(p, '''Software Engineering. The complete subject in one video. Simple explanations, handwritten notes,
diagrams, and every important exam numerical solved step by step.''')
beat(p, '''This works for B Tech computer science in almost every university. A K T U, Anna University, V T U, J N T U,
Mumbai, Pune, and private universities too. It also helps for U G C NET. So grab a pen, and let's start.''')

p = page('Contents', 0)
items = ['Introduction to Software Engineering', '[h:SDLC Models]  (waterfall, spiral, V-model)', 'Agile Development  (Scrum)', '[h:Requirements Engineering]  (SRS, DFD)',
         '[h:Software Design]  (cohesion, coupling)', 'UML Diagrams', '[h:Software Metrics]  (FP, cyclomatic)', '[h:Software Testing]  (BVA, white-box)',
         '[h:Project Management]  (COCOMO, CPM)', 'Quality, Reliability & Maintenance  (CMM)', 'Exam Revision - most asked questions']
beat(p, "Here's our plan. Eleven chapters, from the basics to the exam numericals.", T(0, 'What we will cover today', size=42, font='bold', color='black'))
beat(p, '''We start with what software engineering is, then the S D L C models, agile and scrum, requirements engineering, and software design.''',
     *[T(1 + k, f'{k + 1}.  {items[k]}', x=200) for k in range(5)])
beat(p, '''Then U M L diagrams, software metrics, testing, project management with COCOMO, and quality and maintenance.
At the end, a quick revision of the most asked questions. The highlighted ones are the most important.''',
     *[T(6 + k, f'{k + 6}.  {items[k + 5]}', x=200) for k in range(6)], Stamp(1520, 520, 'MOST ASKED', rot=-10))

# ===================================================================================== CH 1
p = chapter(1)
beat(p, "Chapter one. Introduction to software engineering. Let's build the basics first.")

p = page('What is Software Engineering?', 1)
beat(p, '''Software is not just a program. It is the programs, plus the documents and the data needed to use and maintain them.
Software engineering is the systematic, disciplined and measurable way of developing, operating and maintaining software.
This is the I E E E definition. In simple words, it means building software the way engineers build bridges: with a plan, standards and quality checks.''',
     T(0, '[h:Software] = programs + documentation + data'), T(1, '[h:Software engineering] = systematic, disciplined, measurable'),
     T(2, 'approach to develop, operate & maintain software (IEEE)', x=230, size=34), Stamp(1650, 140))
beat(p, '''Software is different from hardware. Software is developed, not manufactured. It does not wear out, but it does deteriorate because of changes.
Look at the curves. Hardware follows a bathtub curve: many failures at the start, a low steady rate, and then failures rise again as parts wear out.
Software has no wear out phase, but every change adds new bugs, so the actual failure rate shows spikes and slowly goes up.''',
     T(5, 'Software is [k:developed], not manufactured;  it does [r:not wear out], but deteriorates', size=34),
     Ln([(220, 640), (220, 920), (820, 920)], 'black', 3), Ln([(240, 650), (300, 790), (380, 850), (640, 850), (720, 790), (790, 660)], 'red', 5),
     T(0, 'Hardware: bathtub curve', x=300, y=965, size=30, color='red'), T(0, 'failure rate', x=160, y=620, size=26, color='black'), T(0, 'time', x=760, y=950, size=26),
     Ln([(1020, 640), (1020, 920), (1620, 920)], 'black', 3), Ln([(1040, 650), (1110, 820), (1600, 860)], 'green', 4),
     Ln([(1110, 820), (1180, 800), (1220, 740), (1260, 810), (1340, 790), (1380, 720), (1420, 790), (1500, 760), (1540, 690), (1580, 760)], 'red', 5),
     T(0, 'Software: idealized (green), actual with change spikes (red)', x=1020, y=965, size=28, color='red'))
beat(p, '''The software crisis was the problem in the nineteen sixties and seventies, when projects ran over budget, finished late, had poor quality,
and were hard to maintain. Software engineering was created to solve this crisis. It is a layered technology:
a quality focus at the bottom, then process, then methods, and tools at the top.''',
     T(6, '[r:Software crisis]: over budget, late, poor quality, hard to maintain', size=34),
     Box(1320, 236, 500, 54, 'Tools', color='blue', size=28), Box(1320, 290, 500, 54, 'Methods', color='blue', size=28),
     Box(1320, 344, 500, 54, 'Process', color='blue', size=28), Box(1320, 398, 500, 54, 'A quality focus', color='red', size=28))

p = page('Software Development Life Cycle (SDLC)', 1)
phases = ['Feasibility study', 'Requirements', 'Design', 'Coding', 'Testing', 'Deployment', 'Maintenance']
cx, cy, R = 1340, 600, 300
pos = [(cx + R * math.cos(-math.pi / 2 + 2 * math.pi * k / 7), cy + R * 0.95 * math.sin(-math.pi / 2 + 2 * math.pi * k / 7)) for k in range(7)]
beat(p, '''The software development life cycle, or S D L C, is the set of phases a software product goes through, from the idea to its retirement.
It gives a clear plan, so everyone knows what to do and when.''',
     T(0, '[h:SDLC] = phases from idea to retirement'), Stamp(1650, 140, 'MUST DRAW'))
beat(p, '''The phases are: feasibility study, to check if the project is worth doing. Requirements analysis, to find what the users need.
Design, to plan the architecture and modules. Coding, to write the programs. Testing, to find bugs. Deployment, to deliver it to users.
And maintenance, to fix and improve it after delivery.''',
     *[N(1 + k, k + 1, s, size=34) for k, s in enumerate(phases)],
     *[Box(x - 135, y - 34, 270, 68, s, color='blue', size=26) for (x, y), s in zip(pos, phases)],
     *[Arr(pos[k][0] + (pos[(k + 1) % 7][0] - pos[k][0]) * .32, pos[k][1] + (pos[(k + 1) % 7][1] - pos[k][1]) * .32,
           pos[k][0] + (pos[(k + 1) % 7][0] - pos[k][0]) * .68, pos[k][1] + (pos[(k + 1) % 7][1] - pos[k][1]) * .68, color='green') for k in range(7)])
beat(p, '''Remember: maintenance is the longest and most costly phase. It often takes more than sixty percent of the total cost of the software.''',
     T(10, 'Maintenance = [r:longest & costliest] phase (often 60%+ of cost)', size=34))

# ===================================================================================== CH 2
p = chapter(2)
beat(p, 'Chapter two. S D L C models. Almost every exam asks you to explain and compare these.')

wf = ['Feasibility', 'Requirements', 'Design', 'Coding & unit test', 'Integration & testing', 'Maintenance']
p = page('Waterfall & Iterative Waterfall', 2)
beat(p, '''The classical waterfall model is the oldest model. The phases flow one after another, like water falling down steps.
A phase starts only when the previous phase is fully finished, and there is no going back.''',
     T(0, '[h:Waterfall]: phases in order, one after another', size=34), T(1, 'next phase starts only after previous ends', size=34),
     *[Box(860 + 140 * k, 240 + 108 * k, 300, 66, s, color='blue', size=26) for k, s in enumerate(wf)],
     *[Arr(860 + 140 * k + 230, 306 + 108 * k, 860 + 140 * (k + 1) + 60, 240 + 108 * (k + 1)) for k in range(5)])
beat(p, '''It is simple, easy to manage, and well documented. But it is rigid: requirements must be fixed at the start, errors found late are very costly,
and the customer sees working software only at the end. So it suits small projects with clear, stable requirements.''',
     T(3, '[g:+] simple, easy to manage, good documentation', size=34), T(4, '[r:-] fixed requirements, late testing, no early product', size=34),
     T(5, 'Use: [k:small project, clear & stable requirements]', size=34))
beat(p, '''The iterative waterfall model adds feedback paths. If an error is found in a later phase, we can go back to the phase where it happened and fix it.
This is the most widely used form of waterfall in practice. There is no feedback to the feasibility study.''',
     T(7, '[h:Iterative waterfall]: adds [r:feedback paths] back to', size=34), T(8, 'earlier phases (none to feasibility)', size=34, x=230),
     *[Arr(860 + 140 * (k + 1) + 20, 240 + 108 * (k + 1) + 20, 860 + 140 * k - 2, 240 + 108 * k + 40, color='red', curve=60) for k in range(1, 5)])

p = page('Prototyping, Incremental & RAD Models', 2)
beat(p, '''In the prototyping model, we first build a quick, rough working model, called a prototype, and show it to the customer.
The customer gives feedback, we refine the prototype again and again, and then build the real system. It is best when requirements are not clear.
A throwaway prototype is thrown away after it is used. An evolutionary prototype slowly grows into the final product.''',
     T(0, '[h:Prototyping]: quick model -> customer feedback -> refine -> real system', size=34), T(1, 'Best when [k:requirements are unclear];  throwaway vs evolutionary', size=34),
     Box(1060, 360, 230, 64, 'Requirements', size=24), Box(1350, 360, 220, 64, 'Quick design', size=24), Box(1630, 360, 230, 64, 'Build prototype', size=24),
     Box(1630, 480, 230, 64, 'Customer eval.', size=24, color='red'), Box(1350, 480, 220, 64, 'Refine', size=24),
     Arr(1290, 392, 1350, 392), Arr(1570, 392, 1630, 392), Arr(1745, 424, 1745, 480), Arr(1630, 512, 1570, 512), Arr(1460, 480, 1460, 424, color='red'))
beat(p, '''In the incremental model, the software is built and delivered in small parts, called increments. The first increment has the core features,
and each next increment adds more. Customers get working software early, and the risk is lower.''',
     T(6, '[h:Incremental]: deliver in parts; core first, add features later', size=34), T(7, '[g:+] early working software, lower risk, easy to test', size=34),
     *[Box(1060 + 200 * k, 620 - 0, 180, 60, f'Increment {k + 1}', color='green', size=24) for k in range(4)])
beat(p, '''R A D, rapid application development, builds software very fast, in about sixty to ninety days, using reusable components, code generators and strong user involvement.
It needs skilled developers and a project that can be split into modules.''',
     T(9, '[h:RAD]: very fast (60-90 days), reusable components,', size=34), T(10, 'high user involvement; needs skilled team & modular project', size=34, x=230))

p = page('Spiral Model', 2)
sx, sy = 1340, 610
spiral = [(sx + (12 + 26 * t) * math.cos(t), sy - (12 + 26 * t) * math.sin(t) * 0.85) for t in [i * 0.08 for i in range(0, int(4.2 * math.pi / 0.08))]]
beat(p, '''The spiral model was given by Barry Boehm. It is a risk driven model. The project moves in loops, and each loop of the spiral is one phase.
It is called a meta model, because it includes the other models: each loop can work like waterfall or prototyping.''',
     T(0, '[h:Spiral (Boehm)]: risk-driven; each loop = one phase', size=34), T(1, '"[k:meta model]": contains waterfall, prototyping ...', size=34),
     Stamp(1650, 140, 'MOST ASKED'), Ln([(sx - 380, sy), (sx + 380, sy)], 'black', 2), Ln([(sx, sy - 330), (sx, sy + 330)], 'black', 2))
beat(p, '''Each loop has four quadrants. One: determine objectives and alternatives. Two: identify and resolve risks, which is the special feature of this model.
Three: develop and test the next level of the product. Four: review and plan the next phase.''',
     N(3, 1, 'Objectives & alternatives', size=32), N(4, 2, '[r:Risk analysis] & resolution', size=32), N(5, 3, 'Develop & test', size=32), N(6, 4, 'Plan next phase', size=32),
     Ln(spiral, 'blue', 4), T(0, '1. Objectives', x=sx - 370, y=sy - 290, size=28, color='black'), T(0, '2. Risk analysis', x=sx + 70, y=sy - 290, size=28, color='red'),
     T(0, '3. Develop & test', x=sx + 70, y=sy + 315, size=28, color='black'), T(0, '4. Plan next', x=sx - 370, y=sy + 315, size=28, color='black'))
beat(p, '''It is best for large, complex and high risk projects. Its weak points: it is costly, needs risk experts, and is not good for small projects.''',
     T(8, '[g:+] large, high-risk projects, early risk handling', size=34), T(9, '[r:-] costly, needs risk experts, not for small projects', size=34))

vl = ['Requirements', 'System design', 'Architecture design', 'Module design']; vr = ['Acceptance testing', 'System testing', 'Integration testing', 'Unit testing']
p = page('V-Model', 2)
beat(p, '''The V model, or verification and validation model, is an extension of waterfall. The left side of the V is the development phases, going down.
The bottom is coding. The right side is the testing phases, going up.''',
     T(0, '[h:V-model] = Verification & Validation model (extended waterfall)', size=34),
     *[Box(200 + 80 * k, 300 + 120 * k, 380, 66, s, color='blue', size=26) for k, s in enumerate(vl)],
     Box(760, 780, 400, 66, 'Coding', color='black', size=28),
     *[Box(1340 - 80 * k, 300 + 120 * k, 380, 66, s, color='green', size=26) for k, s in enumerate(vr)],
     *[Arr(390 + 80 * k, 366 + 120 * k, 470 + 80 * k, 420 + 120 * k) for k in range(3)], Arr(710, 726, 800, 780),
     Arr(1120, 780, 1210, 726), *[Arr(1530 - 80 * k, 420 + 120 * k, 1530 - 80 * (k + 1) + 80 + 30, 366 + 120 * (k - 1) + 120) for k in range(0)],
     *[Arr(1530 - 80 * (k + 1), 300 + 120 * (k + 1), 1530 - 80 * k - 60, 366 + 120 * k) for k in range(3)])
beat(p, '''Each development phase has a matching testing phase. Requirements match acceptance testing, system design matches system testing,
architecture design matches integration testing, and module design matches unit testing. The test plans are written early, during the matching development phase.''',
     *[Dash(580 + 80 * k, 333 + 120 * k, 1340 - 80 * k, 333 + 120 * k, color='red') for k in range(4)],
     T(0, 'test plans', x=900, y=320, size=26, color='red'))
beat(p, '''Verification asks: are we building the product right? Validation asks: are we building the right product?
The V model is good for safety critical systems, like medical and aviation software, where requirements are clear.''',
     T(13, '[k:Verification]: building the product right?   [k:Validation]: building the right product?', size=32),
     T(14, 'Use: safety-critical systems with clear requirements', size=32, color='green'))

p = page('Comparing SDLC Models', 2)
beat(p, '''Here is the comparison table, which is very useful in exams. Use waterfall when requirements are clear and stable.
Prototyping when requirements are unclear. Incremental when you want early delivery. Spiral for large high risk projects.
V model for safety critical systems. And agile when requirements keep changing and the customer is closely involved.''',
     Stamp(1650, 140, 'MOST ASKED'),
     Tab(180, 240, [260, 330, 270, 280, 400], 60, [['Model', 'Requirements', 'Risk', 'Customer', 'Best for'],
         ['Waterfall', 'clear, fixed', '[r:high]', 'only at start', 'small, stable projects'], ['Prototyping', '[g:unclear]', 'medium', 'high', 'new / unclear needs'],
         ['Incremental', 'mostly clear', 'low', 'each release', 'early delivery'], ['Spiral', 'complex', '[g:handled]', 'each loop', 'large, high-risk'],
         ['V-model', 'clear, fixed', 'low', 'at start', 'safety-critical'], ['RAD', 'clear, modular', 'medium', 'high', 'quick delivery'],
         ['Agile', '[g:changing]', 'low', '[g:continuous]', 'changing needs']], size=28, colors={(r, 0): 'red' for r in range(1, 8)}))

# ===================================================================================== CH 3
p = chapter(3)
beat(p, 'Chapter three. Agile development. This is how most software is built today.')

p = page('Agile Manifesto & Principles', 3)
beat(p, '''Agile is a group of methods that build software in short cycles, with close customer involvement, and welcome changing requirements.
In two thousand one, a group of developers wrote the agile manifesto. It has four values.''',
     T(0, '[h:Agile]: short iterations, customer involvement, welcome change'), T(1, 'Agile Manifesto (2001): 4 values', color='black'))
beat(p, '''Individuals and interactions over processes and tools. Working software over comprehensive documentation. Customer collaboration over contract negotiation.
And responding to change over following a plan. The items on the left are valued more, but the items on the right are still useful.''',
     Stamp(1650, 140, 'MOST ASKED'), N(2, 1, '[r:Individuals & interactions] over processes & tools', size=34), N(3, 2, '[r:Working software] over comprehensive documentation', size=34),
     N(4, 3, '[r:Customer collaboration] over contract negotiation', size=34), N(5, 4, '[r:Responding to change] over following a plan', size=34))
beat(p, '''There are also twelve principles. The main ideas: satisfy the customer through early and continuous delivery, welcome change even late,
deliver working software every few weeks, business people and developers work together daily, face to face talk is best,
working software measures progress, keep a sustainable pace, keep it simple, and the team reflects and improves regularly.''',
     S(7, '12 principles - key ideas', size=36, color='red'), T(8, 'early & continuous delivery · welcome change · deliver every few weeks', size=32),
     T(9, 'business + developers daily · face-to-face talk · working software = progress', size=32), T(10, 'sustainable pace · simplicity · self-organising teams · reflect & improve', size=32))

p = page('Scrum Framework', 3)
beat(p, '''Scrum is the most popular agile framework. It has three roles. The product owner owns the product backlog and decides priorities.
The scrum master is a servant leader who removes obstacles and makes sure scrum is followed. And the development team is small, about three to nine people, and self organising.''',
     S(0, 'Roles', size=36, color='red'), T(1, '[k:Product owner]: owns backlog, sets priorities', size=32), T(2, '[k:Scrum master]: servant leader, removes blockers', size=32),
     T(3, '[k:Dev team]: 3-9 people, self-organising', size=32), Stamp(1650, 140, 'MUST DRAW'))
beat(p, '''There are three artifacts. The product backlog is the full list of features. The sprint backlog is the work chosen for this sprint.
And the increment is the working product at the end of the sprint.''',
     S(5, 'Artifacts', size=36, color='red'), T(6, 'Product backlog · Sprint backlog · Increment', size=32),
     Box(1000, 300, 230, 90, 'Product\nbacklog', color='blue', size=26), Box(1300, 300, 230, 90, 'Sprint\nbacklog', color='blue', size=26),
     Ell(1300, 470, 300, 220, None, color='green'), T(0, 'Sprint', x=1405, y=570, size=30, color='green'), T(0, '1-4 weeks', x=1390, y=610, size=26, color='green'),
     Ell(1560, 420, 160, 120, None, color='red'), T(0, 'Daily scrum', x=1572, y=470, size=24, color='red'), T(0, '15 min', x=1605, y=505, size=24, color='red'),
     Box(1660, 620, 200, 90, 'Increment', color='black', size=26), Arr(1230, 345, 1300, 345, label='plan', ly=-12, size=22), Arr(1415, 390, 1435, 470),
     Arr(1600, 600, 1660, 650))
beat(p, '''And the events. The sprint is a fixed time box of one to four weeks. It starts with sprint planning. Every day there is a fifteen minute daily scrum,
where each member says what they did yesterday, what they will do today, and any blockers. At the end there is a sprint review with the customer,
and a sprint retrospective, where the team discusses how to improve.''',
     S(8, 'Events', size=36, color='red'), T(9, 'Sprint (1-4 weeks) · Sprint planning', size=32), T(10, 'Daily scrum (15 min): yesterday? today? blockers?', size=32),
     T(11, 'Sprint review (show customer) · Retrospective (improve)', size=32))

p = page('XP, Kanban & DevOps', 3)
beat(p, '''Extreme programming, or X P, takes good practices to the extreme. Pair programming, where two people code at one computer.
Test driven development, where tests are written before the code. Continuous integration, small releases, refactoring, simple design,
and collective code ownership.''',
     S(0, 'Extreme Programming (XP)', size=38, color='red'), T(1, 'pair programming · [h:test-driven development (TDD)]', size=34),
     T(2, 'continuous integration · small releases · refactoring', size=34), T(3, 'simple design · collective code ownership · customer on-site', size=34))
beat(p, '''Kanban uses a board with columns like to do, in progress, and done. It shows all work visually and limits the work in progress,
so the team does not take too many tasks at once.''',
     S(5, 'Kanban', size=38, color='red'), T(6, 'visual board + [h:WIP limits] (work in progress)', size=34),
     Tab(1080, 380, [230, 230, 230], 56, [['To do', 'In progress', 'Done'], ['Login page', 'Payment API', 'Signup'], ['Reports', 'Search', 'Home page'], ['Settings', '', '']],
         size=26, colors={(0, 1): 'red'}),
     T(0, 'WIP limit = 2', x=1320, y=360, size=24, color='red'))
beat(p, '''DevOps joins development and operations teams. It uses automation for building, testing and deploying software, called C I C D,
continuous integration and continuous delivery. This makes releases fast and reliable.''',
     S(9, 'DevOps', size=38, color='red'), T(10, 'Dev + Ops together; automate build, test, deploy', size=34), T(11, '[h:CI/CD] = continuous integration / delivery', size=34))

# ===================================================================================== CH 4
p = chapter(4)
beat(p, 'Chapter four. Requirements engineering. Getting the requirements right is the first step to good software.')

p = page('Requirements Engineering Process', 4)
beat(p, '''Requirements engineering is the process of finding, writing and checking what the system must do. It has these steps:
feasibility study, elicitation, analysis, specification, validation, and requirements management.''',
     T(0, '[h:Requirements engineering]: find, write & check what the system must do', size=34),
     *[Box(200 + 295 * k, 320, 235, 66, s, color='blue', size=24) for k, s in enumerate(['Feasibility', 'Elicitation', 'Analysis', 'Specification', 'Validation'])],
     *[Arr(435 + 295 * k, 353, 495 + 295 * k, 353) for k in range(4)], T(0, '+ requirements management (handle changes)', x=200, y=440, size=30, color='green'))
beat(p, '''The feasibility study checks if the project is worth doing. Technical feasibility: do we have the technology and skills? Economic feasibility:
do the benefits exceed the cost? Operational feasibility: will users actually use it? Schedule and legal feasibility are also checked.''',
     S(6, 'Feasibility study', size=36, color='red'), T(7, '[k:Technical] (tech & skills) · [k:Economic] (cost-benefit) · [k:Operational] (will users use it?)', size=30),
     T(8, '+ schedule & legal feasibility', size=30))
beat(p, '''Elicitation means collecting requirements from stakeholders. Techniques are interviews, questionnaires, brainstorming, observation,
use cases and scenarios, and J A D, joint application development, where users and developers work together in workshops. F A S T is a similar method.''',
     S(10, 'Elicitation techniques', size=36, color='red'), T(11, 'interviews · questionnaires · brainstorming · observation', size=32),
     T(12, 'use cases / scenarios · [h:JAD] workshops · FAST · prototyping', size=32), Stamp(1600, 820))

p = page('Functional vs Non-Functional Requirements', 4)
beat(p, '''Functional requirements say what the system should do: its services and functions. For an A T M: the user can withdraw cash,
check balance, and change the PIN.''',
     T(0, '[h:Functional] = WHAT the system does (services)'), T(1, 'ATM: withdraw cash, check balance, change PIN', color='green'))
beat(p, '''Non functional requirements say how well the system does it: quality constraints. For example: the A T M must respond within three seconds,
must be available twenty four by seven, must keep data secure, and must be easy to use.''',
     T(3, '[h:Non-functional] = HOW WELL (quality constraints)'), T(4, 'ATM: respond < 3 s, available 24x7, secure, easy to use', color='green'))
beat(p, '''Here is the comparison. Functional requirements describe features, are tested by functional testing, and are usually written as use cases.
Non functional requirements describe qualities like performance, security, reliability, usability, portability and maintainability,
and are tested by performance and security testing. There are also domain requirements, which come from the application domain, like banking rules.''',
     Stamp(1650, 140, 'MOST ASKED'),
     Tab(180, 500, [300, 600, 640], 56, [['', 'Functional', 'Non-functional'], ['describes', 'what the system does', 'how well it does it'],
         ['examples', 'login, search, payment', 'performance, security, usability'], ['testing', 'functional testing', 'performance / load / security testing'],
         ['if missing', 'system does not work', 'system works, but badly']], size=28, colors={(r, 0): 'red' for r in range(1, 5)}),
     T(14, '[k:Domain requirements]: from the application area (e.g. banking rules)', size=32))

p = page('SRS Document', 4)
beat(p, '''The S R S, software requirements specification, is the official document of all the requirements. It is a contract between the customer and the developer.
It says what the system must do, not how to build it.''',
     T(0, '[h:SRS] = official document of all requirements'), T(1, 'contract between customer & developer; says WHAT, not HOW'))
beat(p, '''A good S R S must be correct, unambiguous, complete, consistent, ranked for importance, verifiable, modifiable, and traceable.
Unambiguous means each requirement has only one meaning. Verifiable means we can test it. Traceable means we can link each requirement to its design and code.''',
     Stamp(1650, 140, 'MOST ASKED'), S(3, 'Characteristics of a good SRS', size=36, color='red'),
     T(4, 'correct · [h:unambiguous] · complete · consistent', size=34), T(5, 'ranked · [h:verifiable] · modifiable · [h:traceable]', size=34))
beat(p, '''The I E E E eight three zero standard gives the S R S structure. One, introduction, with purpose, scope, definitions and references.
Two, overall description, with product perspective, functions, user characteristics, constraints and assumptions.
Three, specific requirements, with functional, interface, performance and other non functional requirements. Then appendices and index.''',
     S(7, 'IEEE 830 SRS structure', size=36, color='red'), N(8, 1, 'Introduction: purpose, scope, definitions, references', size=32),
     N(9, 2, 'Overall description: perspective, functions, users, constraints', size=32), N(10, 3, 'Specific requirements: functional, interfaces, performance ...', size=32),
     T(11, 'Appendices, index', size=32))

p = page('Data Flow Diagrams (DFD)', 4)
beat(p, '''A data flow diagram shows how data moves through a system. It has four symbols. A circle is a process, which changes data.
A rectangle is an external entity, a source or destination of data. An arrow is a data flow. And two parallel lines are a data store.''',
     Ell(200, 250, 120, 90, 'Process', size=22, color='blue'), T(0, 'process', x=340, y=305, size=28),
     Box(560, 255, 150, 76, 'Entity', size=24), T(0, 'external entity', x=730, y=305, size=28),
     Arr(1000, 293, 1120, 293), T(0, 'data flow', x=1140, y=305, size=28),
     Ln([(1400, 260), (1580, 260)], 'black', 3), Ln([(1400, 326), (1580, 326)], 'black', 3), Ln([(1400, 260), (1400, 326)], 'black', 3), T(0, 'Store', x=1440, y=305, size=26),
     T(0, 'data store', x=1600, y=305, size=28), Stamp(1650, 160, 'MUST DRAW'))
beat(p, '''The level zero D F D, also called the context diagram, shows the whole system as one process with its external entities.
Here, a student result system: the student and teacher send data to it, and it sends results back.''',
     S(4, 'Level 0 (context diagram)', size=34, color='red'),
     Ell(560, 560, 300, 150, 'Result\nSystem', size=28, color='blue'), Box(190, 590, 200, 80, 'Teacher', size=28), Box(1040, 590, 200, 80, 'Student', size=28),
     Arr(390, 615, 560, 615, label='marks', size=24), Arr(1040, 615, 860, 615, label='roll no', size=24), Arr(860, 660, 1040, 660, label='result', ly=30, size=24),
     Box(560, 820, 300, 76, 'Admin', size=28), Arr(710, 820, 710, 712, label='rules', lx=50, ly=8, size=24))
beat(p, '''In level one, we open the main process into sub processes: enter marks, calculate result, and generate report, with data stores for marks and students.
Rules: data must be balanced between levels, a process must have both input and output, and data cannot flow directly between two entities or two stores.''',
     S(4, 'Level 1', x=1350, size=34, color='red'),
     Ell(1300, 520, 200, 100, '1.0 Enter\nmarks', size=22, color='blue'), Ell(1590, 520, 220, 100, '2.0 Calc.\nresult', size=22, color='blue'),
     Ell(1590, 760, 220, 100, '3.0 Gen.\nreport', size=22, color='blue'), Arr(1500, 570, 1590, 570), Arr(1700, 620, 1700, 760),
     Ln([(1280, 740), (1470, 740)], 'black', 3), Ln([(1280, 796), (1470, 796)], 'black', 3), Ln([(1280, 740), (1280, 796)], 'black', 3), T(0, 'D1 Marks', x=1300, y=780, size=24),
     Arr(1400, 620, 1380, 740), T(14, 'Rules: balance levels · no entity-to-entity or store-to-store flow', size=30, color='green'))

p = page('Data Dictionary & Decision Table', 4)
beat(p, '''A data dictionary stores the meaning of every data item used in the D F D. It uses simple notation. Equals means "is made of".
Plus means "and". Square brackets with a bar mean "either or". Curly brackets mean repetition. And round brackets mean optional.''',
     S(0, 'Data dictionary notation', size=36, color='red'),
     Tab(180, 290, [180, 460], 44, [['Symbol', 'Meaning'], ['=', 'is composed of'], ['+', 'and'], ['[ a | b ]', 'either a or b'], ['{ }', 'repetition (0 or more)'], ['( )', 'optional']], size=28),
     T(0, 'name = first_name + (middle_name) + last_name', x=900, y=L(2), size=32, color='black'),
     T(0, 'phone = [ mobile | landline ]', x=900, y=L(3), size=32, color='black'), T(0, 'order = customer + { item }', x=900, y=L(4), size=32, color='black'))
beat(p, '''A decision table shows complex logic as conditions and actions. For example, a loan rule: if the salary is above thirty thousand and the credit score is good,
approve the loan. If only one condition is true, send the case for manual review. If both are false, reject it. With two conditions, there are four rules.''',
     Stamp(1650, 140), S(8, 'Decision table: loan approval', size=34, color='red'),
     Tab(180, 680, [420, 120, 120, 120, 120], 46, [['Conditions / actions', 'R1', 'R2', 'R3', 'R4'], ['salary > 30,000', 'Y', 'Y', 'N', 'N'], ['good credit score', 'Y', 'N', 'Y', 'N'],
         ['approve', 'X', '', '', ''], ['manual review', '', 'X', 'X', ''], ['reject', '', '', '', 'X']], size=26, colors={(3, 0): 'green', (4, 0): 'green', (5, 0): 'green'}),
     T(0, '2 conditions => 2^2 = 4 rules', x=1140, y=790, size=32, color='red'))

# ===================================================================================== CH 5
p = chapter(5)
beat(p, 'Chapter five. Software design. Cohesion and coupling are asked in almost every exam.')

p = page('Design Concepts', 5)
beat(p, '''Software design turns the S R S into a plan for the code. Key design concepts are: abstraction, which hides details and shows only the important parts.
Modularity, which divides the software into smaller modules. Information hiding, where a module hides its internal data from others.
Stepwise refinement, which breaks a big task into smaller steps. And separation of concerns.''',
     T(0, '[h:Design]: SRS -> blueprint for code'), N(1, 1, '[k:Abstraction]: show what matters, hide details', size=34), N(2, 2, '[k:Modularity]: split into modules', size=34),
     N(3, 3, '[k:Information hiding]: module hides its internal data', size=34), N(4, 4, '[k:Stepwise refinement]: big task -> smaller steps', size=34),
     N(5, 5, '[k:Separation of concerns], [k:refactoring]', size=34))
beat(p, '''Design is done at two levels. High level design, or architectural design, decides the modules and how they connect. Low level design, or detailed design,
decides the logic and data structures inside each module.''',
     T(7, '[r:High-level (architectural)]: modules & connections', size=34), T(8, '[r:Low-level (detailed)]: logic & data structures inside modules', size=34))
beat(p, '''There are two approaches. Function oriented design divides the system into functions, using D F Ds and structure charts. Object oriented design divides it into objects,
which combine data and functions, using U M L. Top down design starts from the main module and breaks it down. Bottom up design starts from small modules and combines them.''',
     Tab(180, 680, [330, 580, 580], 56, [['', 'Function-oriented', 'Object-oriented'], ['unit', 'functions', 'objects (data + methods)'], ['tools', 'DFD, structure chart', 'UML diagrams'],
         ['state', 'shared / global data', 'hidden inside objects']], size=28),
     T(14, '[k:Top-down]: main -> sub-modules     [k:Bottom-up]: small modules -> system', size=32))

coh = [('Coincidental', 'unrelated tasks together', 'red'), ('Logical', 'similar kind of tasks (all I/O)', 'red'), ('Temporal', 'done at the same time (init)', 'red'),
       ('Procedural', 'follow a sequence of steps', 'blue'), ('Communicational', 'work on the same data', 'blue'), ('Sequential', "output of one = input of next", 'green'),
       ('Functional', 'one single well-defined task', 'green')]
p = page('Cohesion', 5)
beat(p, '''Cohesion measures how strongly the parts inside one module are related to each other. High cohesion is good. A highly cohesive module does just one job.
There are seven types, from worst to best.''',
     T(0, '[h:Cohesion] = how related the parts INSIDE a module are;  [g:HIGH is good]', size=34), Stamp(1650, 140, 'MOST ASKED'))
beat(p, '''Coincidental cohesion is the worst: unrelated tasks are put together. Logical cohesion: tasks of a similar kind, like all input output functions.
Temporal cohesion: tasks done at the same time, like initialisation. Procedural: tasks that follow a sequence.''',
     *[T(2 + k, f'{k + 1}. ' + (f'[{c[0]}:{n}]' if c != 'blue' else n) + f' - {d}', x=200, size=34) for k, (n, d, c) in enumerate(coh[:4])])
beat(p, '''Communicational: tasks that work on the same data. Sequential: the output of one task is the input of the next. And functional cohesion is the best:
all parts work together for one single, well defined task. Trick to remember the order: "Can Lazy Teachers Prepare Clear Simple Functions".''',
     *[T(6 + k, f'{k + 5}. ' + (f'[{c[0]}:{n}]' if c != 'blue' else n) + f' - {d}', x=200, size=34) for k, (n, d, c) in enumerate(coh[4:])],
     Arr(1680, 330, 1680, 760, color='green', label='better', lx=60, ly=0, size=26), T(10, 'Trick: "[h:C]an [h:L]azy [h:T]eachers [h:P]repare [h:C]lear [h:S]imple [h:F]unctions"', size=32, color='red'))

cop = [('Data', 'pass only needed simple data', 'green'), ('Stamp', 'pass a whole structure / record', 'green'), ('Control', 'pass a flag that controls logic', 'blue'),
       ('External', 'share an external format / device', 'blue'), ('Common', 'share global data', 'red'), ('Content', 'one module changes code / data of another', 'red')]
p = page('Coupling', 5)
beat(p, '''Coupling measures how much one module depends on other modules. Low coupling is good, because a change in one module does not break the others.
The golden rule of design is: high cohesion and low coupling.''',
     T(0, '[h:Coupling] = dependence BETWEEN modules;  [g:LOW is good]', size=34), T(1, 'Golden rule: [r:high cohesion, low coupling]', size=38, color='black'),
     Stamp(1650, 140, 'MOST ASKED'))
beat(p, '''There are six types, from best to worst. Data coupling is the best: modules pass only the simple data needed. Stamp coupling: they pass a whole structure,
when only part of it is needed. Control coupling: one module passes a flag that controls the logic of another.''',
     *[T(3 + k, f'{k + 1}. ' + (f'[{c[0]}:{n}]' if c != 'blue' else n) + f' - {d}', x=200, size=34) for k, (n, d, c) in enumerate(cop[:3])])
beat(p, '''External coupling: modules share an external data format, device or protocol. Common coupling: modules share global data. And content coupling is the worst:
one module directly changes the code or data of another. Trick: "Don't Say Can't Ever Come Clean".''',
     *[T(6 + k, f'{k + 4}. ' + (f'[{c[0]}:{n}]' if c != 'blue' else n) + f' - {d}', x=200, size=34) for k, (n, d, c) in enumerate(cop[3:])],
     Arr(1680, 380, 1680, 760, color='red', label='worse', lx=60, ly=0, size=26), T(10, 'Trick: "[h:D]on\'t [h:S]ay [h:C]an\'t [h:E]ver [h:C]ome [h:C]lean"', size=32, color='red'))

p = page('Architectural Styles & Structure Chart', 5)
beat(p, '''Software architecture is the overall structure of the system. Common styles: layered architecture, like the presentation, business and data layers.
Client server, where clients request services from a server. Pipe and filter, where data flows through a chain of processing steps.
M V C, model view controller. And repository, or data centred architecture, where all parts share a central database.''',
     N(0, 1, '[k:Layered]: presentation -> business -> data', size=34), N(1, 2, '[k:Client-server]: clients request, server serves', size=34),
     N(2, 3, '[k:Pipe & filter]: data flows through steps (compiler)', size=34), N(3, 4, '[k:MVC]: model · view · controller', size=34),
     N(4, 5, '[k:Repository]: central shared database', size=34))
beat(p, '''A structure chart shows the modules of a program as a hierarchy, and how they call each other. Here the main module calls get input, compute, and display.
Compute calls validate and calculate. Small arrows with circles show data and control passed between modules.''',
     Stamp(1650, 140), Box(830, 560, 260, 70, 'Main', size=28, color='red'), Box(440, 700, 240, 66, 'Get input', size=26), Box(840, 700, 240, 66, 'Compute', size=26),
     Box(1240, 700, 240, 66, 'Display', size=26), Box(660, 850, 220, 62, 'Validate', size=24), Box(1030, 850, 220, 62, 'Calculate', size=24),
     Arr(900, 630, 560, 700), Arr(960, 630, 960, 700), Arr(1020, 630, 1360, 700), Arr(930, 766, 770, 850), Arr(990, 766, 1140, 850),
     Ell(700, 640, 18, 18, None, color='green'), Arr(709, 649, 640, 680, color='green', label='marks', lx=-70, ly=-4, size=22))

# ===================================================================================== CH 6
p = chapter(6)
beat(p, 'Chapter six. U M L diagrams. Drawing these neatly gives you full marks.')

p = page('UML & Use Case Diagram', 6)
beat(p, '''U M L, the unified modeling language, is a standard visual language to model software. It has two groups of diagrams. Structural diagrams show the static structure,
like class, object, component and deployment diagrams. Behavioural diagrams show how the system behaves, like use case, sequence, activity and state diagrams.''',
     T(0, '[h:UML] = standard visual modelling language', size=34), T(1, '[k:Structural]: class, object, component, deployment', size=32),
     T(2, '[k:Behavioural]: use case, sequence, activity, state', size=32))
beat(p, '''A use case diagram shows what the users, called actors, can do with the system. An actor is a stick figure, a use case is an oval,
and the system boundary is a rectangle. Here, the customer of an A T M can withdraw cash, check balance and deposit money. The bank is a second actor.''',
     Stamp(1650, 140, 'MUST DRAW'), Box(560, 390, 760, 560, None, color='black'), T(0, 'ATM System', x=800, y=430, size=30, color='black'),
     *Actor(320, 520, 'Customer'), *Actor(1560, 520, 'Bank'),
     Ell(620, 470, 300, 80, 'Withdraw cash', size=24, color='blue'), Ell(620, 600, 300, 80, 'Check balance', size=24, color='blue'), Ell(620, 730, 300, 80, 'Deposit', size=24, color='blue'),
     Arr(365, 590, 620, 515, head=False), Arr(365, 595, 620, 640, head=False), Arr(365, 600, 620, 765, head=False), Arr(1515, 595, 920, 515, head=False))
beat(p, '''Include means a use case always uses another one: every transaction includes authenticate. Extend means an optional extra behaviour:
print receipt extends withdraw cash, only if the user wants it. Both are drawn as dashed arrows.''',
     Ell(1000, 600, 280, 80, 'Authenticate', size=24, color='green'), Ell(1000, 820, 280, 80, 'Print receipt', size=24, color='green'),
     *Dash(920, 530, 975, 580, color='green'), Arr(975, 580, 1015, 614, color='green'), T(0, '<<include>>', x=960, y=560, size=22, color='green'),
     *Dash(1120, 820, 905, 588, color='red'), Arr(905, 588, 868, 548, color='red'), T(0, '<<extend>>', x=1020, y=730, size=22, color='red'),
     T(14, '[k:include]: always needed    [k:extend]: optional behaviour', size=32))

p = page('Class Diagram', 6)
cP, yP = Cls(800, 230, 300, 'Person', ['- name : String', '- age : int'], ['+ getName()'])
cS, yS = Cls(560, 560, 280, 'Student', ['- rollNo : int'], ['+ enroll()'])
cT, yT = Cls(1060, 560, 280, 'Teacher', ['- empId : int'], ['+ teach()'])
cD, yD = Cls(1560, 560, 280, 'Department', ['- name : String'], ['+ addTeacher()'])
cC, yC = Cls(180, 560, 260, 'Course', ['- code : String'], ['+ getCode()'])
beat(p, '''A class diagram shows the classes of the system and the relationships between them. A class box has three parts: the class name,
the attributes, and the methods. A minus sign means private, and a plus sign means public. A hash means protected.''',
     T(0, 'Class = name · attributes · methods;   - private  + public  # protected', size=32), *cP)
beat(p, '''Inheritance, or generalization, is an "is a" relationship. Student is a person, and teacher is a person. It is drawn with a hollow triangle arrow pointing to the parent.''',
     *cS, *cT, Ln([(700, 560), (700, 520), (1200, 520), (1200, 560)], 'black', 3), Ln([(950, 520), (950, yP + 26)], 'black', 3),
     T(0, '△', x=930, y=yP + 38, size=44, color='black'), T(0, 'inheritance ("is-a")', x=980, y=505, size=24, color='red'))
beat(p, '''Association is a general link: a student enrolls in many courses, and a course has many students. The numbers at the ends are the multiplicity, like one,
zero dot dot star, or one dot dot star. Aggregation is a weak "has a" relationship, drawn with a hollow diamond: a department has teachers, but teachers can exist without it.
Composition is a strong "has a", drawn with a filled diamond: if the house is destroyed, its rooms are destroyed too.''',
     *cC, Ln([(440, 640), (560, 640)], 'black', 3), T(0, '*', x=450, y=630, size=28, color='red'), T(0, '*', x=535, y=630, size=28, color='red'),
     *cD, Ln([(1340, 640), (1540, 640)], 'black', 3), T(0, '◇', x=1530, y=655, size=40, color='black'), T(0, '1', x=1515, y=625, size=26, color='red'), T(0, '1..*', x=1350, y=625, size=26, color='red'),
     T(0, 'aggregation ◇ (weak has-a)', x=1360, y=870, size=26, color='blue'), T(0, 'composition ◆ (strong has-a: house-rooms)', x=1360, y=910, size=26, color='blue'),
     T(0, 'association (multiplicity *)', x=180, y=870, size=26, color='blue'))

p = page('Sequence & Activity Diagrams', 6)
objs = [('Customer', 260), ('ATM', 560), ('Bank', 860)]
msgs = [(0, 1, 'insert card, PIN', 400), (1, 2, 'verify(PIN)', 460), (2, 1, 'OK', 520), (0, 1, 'withdraw(amount)', 580), (1, 2, 'debit(amount)', 640), (2, 1, 'done', 700), (1, 0, 'cash + card', 760)]
beat(p, '''A sequence diagram shows how objects talk to each other over time. Objects are at the top, and dashed vertical lines below them are their lifelines.
Arrows are messages, and time goes from top to bottom. Here, the customer inserts a card, the A T M verifies the PIN with the bank, then the customer withdraws money,
the bank debits the account, and the A T M gives the cash.''',
     T(0, '[h:Sequence]: objects talk over time (top -> bottom)', size=32),
     *[Box(x - 100, 300, 200, 60, n, size=26, color='blue') for n, x in objs], *[d for n, x in objs for d in Dash(x, 360, x, 820, color='black', w=2)],
     *[Arr(objs[a][1] + (8 if b > a else -8), y, objs[b][1] + (-8 if b > a else 8), y, color='green' if b < a else 'black', label=t, ly=-10, size=22) for a, b, t, y in msgs])
beat(p, '''An activity diagram shows the flow of activities, like a flowchart. A filled circle is the start, rounded boxes are activities, a diamond is a decision,
and a thick bar is a fork or join for parallel activities. A circle with a ring is the end.''',
     T(0, '[h:Activity]: flow of activities (like a flowchart)', x=1080, y=L(0), size=32),
     Ell(1430, 300, 40, 40, None, color='black'), Ell(1436, 306, 28, 28, None, color='black'), Arr(1450, 340, 1450, 380),
     Box(1330, 380, 240, 60, 'Enter PIN', size=24, color='blue'), Arr(1450, 440, 1450, 480),
     Ln([(1450, 480), (1530, 530), (1450, 580), (1370, 530), (1450, 480)], 'red', 4), T(0, 'valid?', x=1418, y=540, size=22, color='red'),
     Arr(1370, 530, 1230, 530, label='no', ly=-10, size=22), Box(1060, 500, 170, 60, 'Retry', size=22, color='blue'),
     Arr(1450, 580, 1450, 630, label='yes', lx=30, ly=10, size=22), Ln([(1340, 640), (1560, 640)], 'black', 9),
     Box(1250, 680, 180, 60, 'Dispense', size=22, color='blue'), Box(1470, 680, 180, 60, 'Print slip', size=22, color='blue'),
     Arr(1340, 644, 1340, 680), Arr(1560, 644, 1560, 680), Ln([(1340, 790), (1560, 790)], 'black', 9), Arr(1340, 740, 1340, 786), Arr(1560, 740, 1560, 786),
     Arr(1450, 794, 1450, 840), Ell(1430, 840, 40, 40, None, color='black'), Ell(1438, 848, 24, 24, None, color='black'), T(0, 'fork / join', x=1600, y=650, size=22, color='red'))
beat(p, '''A state diagram shows the states of one object and the events that change them. For example, an order goes from placed, to paid, to shipped, to delivered.
The difference: an activity diagram shows the flow of work, while a state diagram shows the life of one object.''',
     T(14, '[k:State diagram]: states of ONE object (placed -> paid -> shipped -> delivered)', size=30))

# ===================================================================================== CH 7
p = chapter(7)
beat(p, 'Chapter seven. Software metrics. Function points and cyclomatic complexity are favourite numericals.')

H = halstead(10, 8, 40, 30)
p = page('Size Metrics: LOC & Halstead', 7)
beat(p, '''A metric is a number that measures some property of software. Lines of code, or L O C, is the simplest size metric. It counts the lines of the program,
without comments and blank lines, and is usually written in K L O C, thousands of lines. It is easy to count, but it depends on the language and the programmer,
and cannot be known at the start of a project.''',
     T(0, '[h:Metric] = a number that measures software'), T(1, '[k:LOC / KLOC]: easy; but language-dependent, known only after coding', size=34))
beat(p, '''Halstead's software science measures a program by counting operators and operands. Small n one is the number of distinct operators,
small n two is distinct operands. Capital N one and N two are the total occurrences. Example: n one is ten, n two is eight, N one is forty, and N two is thirty.''',
     Stamp(1650, 140, 'NUMERICAL'), T(3, 'n1 = distinct operators, n2 = distinct operands, N1, N2 = totals', size=32),
     T(4, 'Given: n1 = 10, n2 = 8, N1 = 40, N2 = 30', color='black'))
beat(p, f'''Vocabulary n is n one plus n two, eighteen. Length N is N one plus N two, seventy. Estimated length is n one log n one plus n two log n two, about fifty seven point two.
Volume V is N times log base two of n, about two hundred ninety one point nine bits. Difficulty D is n one by two, times N two by n two, which is eighteen point seven five.
Effort E is D times V, about five thousand four hundred seventy three. And time T is E divided by eighteen, about three hundred and four seconds.''',
     Tab(180, 520, [420, 560, 300], 52, [['Measure', 'Formula', 'Value'], ['Vocabulary n', 'n1 + n2', str(H['n'])], ['Length N', 'N1 + N2', str(H['N'])],
         ['Estimated length', 'n1 log2 n1 + n2 log2 n2', f"{H['Nh']:.2f}"], ['Volume V', 'N log2 n', f"{H['V']:.2f} bits"],
         ['Difficulty D', '(n1 / 2) × (N2 / n2)', f"{H['D']:.2f}"], ['Effort E', 'D × V', f"{H['E']:,.0f}"], ['Time T', 'E / 18 seconds', f"{H['T']:.0f} s"]], size=28,
         colors={(r, 2): 'red' for r in range(1, 8)}))

ufp, caf, fp = function_points({'EI': 50, 'EO': 40, 'EQ': 35, 'ILF': 6, 'EIF': 4})
p = page('Function Point Analysis', 7)
beat(p, '''Function point analysis measures software size by its functionality, not by lines of code. So it can be done early, from the requirements.
It counts five things: external inputs, external outputs, external enquiries, internal logical files, and external interface files.
Each is given a weight for simple, average, or complex.''',
     T(0, '[h:Function points]: size from functionality (early, language-independent)', size=34),
     Tab(180, 300, [460, 150, 150, 150], 50, [['Function type', 'Simple', 'Average', 'Complex'], ['External inputs (EI)', '3', '4', '6'], ['External outputs (EO)', '4', '5', '7'],
         ['External enquiries (EQ)', '3', '4', '6'], ['Internal logical files (ILF)', '7', '10', '15'], ['External interface files (EIF)', '5', '7', '10']], size=28,
         fills={(r, 2): 'yellow' for r in range(1, 6)}), Stamp(1650, 140, 'NUMERICAL'))
beat(p, f'''Classic question. Fifty inputs, forty outputs, thirty five enquiries, six internal files, and four external interfaces. All weights are average.
Unadjusted function points: fifty times four, plus forty times five, plus thirty five times four, plus six times ten, plus four times seven. That is six hundred twenty eight.''',
     T(0, 'Given: EI 50, EO 40, EQ 35, ILF 6, EIF 4 (average)', x=1100, y=L(2), size=30, color='black'),
     T(0, 'UFP = 50×4 + 40×5 + 35×4 + 6×10 + 4×7', x=1100, y=L(3), size=30), T(0, f'= 200 + 200 + 140 + 60 + 28 = [h:{ufp}]', x=1100, y=L(4), size=30))
beat(p, f'''Next, the complexity adjustment factor. There are fourteen general system characteristics, each rated zero to five. If all are average, each is three,
so the sum is forty two. C A F is zero point six five plus zero point zero one times forty two, which is one point zero seven.
So the function points are six hundred twenty eight times one point zero seven, which is six hundred seventy one point nine six.''',
     T(9, 'CAF = 0.65 + 0.01 × ΣFi,   14 factors × 3 (average) = 42', size=34), T(10, f'CAF = 0.65 + 0.42 = {caf:.2f}', size=34),
     T(11, f'FP = UFP × CAF = {ufp} × {caf:.2f} = [h:{fp:.2f}]', size=40, color='red'))

cy = cyclomatic()
gn = {1: (1450, 280), 2: (1450, 390), 3: (1450, 500), 4: (1340, 620), 5: (1560, 620), 6: (1450, 740), 7: (1720, 390)}
p = page('Cyclomatic Complexity', 7)
beat(p, '''Cyclomatic complexity, given by McCabe, measures the logical complexity of a program. It equals the number of independent paths,
so it tells us the minimum number of test cases for path testing. First we draw the control flow graph, where nodes are statements and edges are the flow of control.''',
     T(0, '[h:V(G)] = number of independent paths (McCabe)', size=34), T(1, '= minimum test cases for basis-path testing', size=34), Stamp(1650, 140, 'NUMERICAL'))
beat(p, '''Example: G C D by subtraction. Node one reads a and b. Node two is "while a not equal to b". Node three is "if a greater than b". Node four is a equals a minus b,
node five is b equals b minus a, node six joins the if and goes back to the loop, and node seven prints a.''',
     T(3, '1: read a, b', x=200, size=30, color='black'), T(4, '2: while (a != b)', x=200, size=30, color='black'), T(5, '3:    if (a > b)', x=200, size=30, color='black'),
     T(6, '4:       a = a - b', x=200, size=30, color='black'), T(7, '5:    else b = b - a', x=200, size=30, color='black'), T(8, '6: end-if (back to 2)', x=200, size=30, color='black'),
     T(9, '7: print a', x=200, size=30, color='black'),
     *Tree({k: (x, y, str(k), 'red' if k in (2, 3) else 'blue') for k, (x, y) in gn.items()}, [(1, 2), (2, 3), (2, 7), (3, 4), (3, 5), (4, 6), (5, 6)], w=64, h=56, head=True),
     Arr(1418, 750, 1418, 400, curve=-300, color='black'))
beat(p, f'''Now three ways to find V of G. One: edges minus nodes plus two. There are eight edges and seven nodes, so eight minus seven plus two is three.
Two: predicate nodes plus one. There are two decisions, node two and node three, so two plus one is three. Three: the number of regions in the graph, which is also three.''',
     T(11, f"V(G) = E - N + 2 = {cy['E']} - {cy['N']} + 2 = [h:{cy['V']}]", size=34, color='red'), T(12, f"V(G) = P + 1 = {cy['P']} + 1 = [h:{cy['Vp']}]", size=34, color='red'),
     T(13, 'V(G) = number of regions = [h:3]', size=34, color='red'), T(0, 'R1', x=1432, y=632, size=26, color='green'), T(0, 'R2', x=1310, y=540, size=26, color='green'),
     T(0, 'R3', x=1680, y=660, size=26, color='green'))
beat(p, '''So we need three test cases, one for each independent path. Path one: one, two, seven. Path two: one, two, three, four, six, two, seven.
Path three: one, two, three, five, six, two, seven. If V of G is more than ten, the module is considered too complex and should be split.''',
     T(14, 'Paths: 1-2-7 | 1-2-3-4-6-2-7 | 1-2-3-5-6-2-7     (V(G) > 10 => too complex)', size=30, color='green'))

# ===================================================================================== CH 8
p = chapter(8)
beat(p, 'Chapter eight. Software testing.')

p = page('Testing Basics', 8)
beat(p, '''Testing is the process of running a program to find errors. Remember these terms. An error, or mistake, is made by a human.
It causes a fault, also called a defect or bug, in the code. When the faulty code runs, it may cause a failure, which means the output is wrong.''',
     T(0, '[h:Testing] = run the program to find errors'), Box(220, 330, 260, 70, 'Error (human)', size=26, color='red'), Box(620, 330, 340, 70, 'Fault / defect / bug', size=26, color='red'),
     Box(1100, 330, 300, 70, 'Failure (wrong output)', size=26, color='red'), Arr(480, 365, 620, 365), Arr(960, 365, 1100, 365))
beat(p, '''Verification checks if we are building the product right, by reviews, walkthroughs and inspections, without running the code. It is static.
Validation checks if we are building the right product, by actually running and testing the software. It is dynamic.''',
     Stamp(1650, 140, 'MOST ASKED'),
     Tab(180, 470, [280, 560, 560], 56, [['', 'Verification', 'Validation'], ['question', 'building the product right?', 'building the right product?'],
         ['how', 'reviews, walkthroughs, inspections', 'testing by running the code'], ['type', 'static (no execution)', 'dynamic (execution)'], ['when', 'before validation', 'after verification']],
         size=28, colors={(r, 0): 'red' for r in range(1, 5)}))
beat(p, '''Some testing principles: testing shows the presence of bugs, not their absence. Exhaustive testing is impossible. Test early.
Bugs cluster together in a few modules. And the pesticide paradox: running the same tests again and again finds no new bugs, so tests must be updated.''',
     T(12, 'Principles: shows bugs, not absence · exhaustive testing impossible · test early', size=30), T(13, 'defect clustering · pesticide paradox (update tests)', size=30))

p = page('Levels of Testing', 8)
beat(p, '''There are four levels of testing. Unit testing tests each module alone, usually by the developer. Integration testing tests modules joined together, to check their interfaces.
System testing tests the complete system against the S R S. And acceptance testing is done by the customer, to decide whether to accept the software.''',
     *[Box(200 + 390 * k, 240, 320, 66, s, size=26, color='blue') for k, s in enumerate(['Unit', 'Integration', 'System', 'Acceptance'])],
     *[Arr(520 + 390 * k, 273, 590 + 390 * k, 273) for k in range(3)],
     T(3, '[k:Unit]: each module alone   [k:Integration]: modules together (interfaces)', size=32), T(4, '[k:System]: whole system vs SRS   [k:Acceptance]: by customer', size=32))
beat(p, '''Acceptance testing has two types. Alpha testing is done by users at the developer's site. Beta testing is done by real users at their own site, before the final release.
System testing also includes performance, load, stress, security, usability and recovery testing.''',
     T(6, '[r:Alpha]: users at developer site   [r:Beta]: real users at their site', size=32), T(7, 'System testing: performance, load, stress, security, usability, recovery', size=32))
beat(p, '''Integration can be done in four ways. Big bang joins everything at once, which makes bugs hard to find. Top down starts from the main module and needs stubs,
which are dummy modules that are called. Bottom up starts from the lowest modules and needs drivers, which are dummy modules that call them.
And sandwich, or hybrid, combines top down and bottom up.''',
     Stamp(1650, 140), S(9, 'Integration approaches', size=36, color='red'), T(10, '[k:Big bang]: all at once (hard to locate bugs)', size=32),
     T(11, '[k:Top-down]: needs [h:stubs] (dummy called modules)', size=32), T(12, '[k:Bottom-up]: needs [h:drivers] (dummy calling modules)', size=32),
     T(13, '[k:Sandwich / hybrid]: both together', size=32))

bv1, bvr = bva(1, 100), bva(1, 100, True); bv2 = bva_two((1, 100), (1, 200))
p = page('Black-Box Testing: EP & BVA', 8)
beat(p, '''Black box testing tests the software from the outside, using only the inputs and outputs, without looking at the code. It is also called functional testing.
The main techniques are equivalence partitioning, boundary value analysis, decision table testing and cause effect graphing.''',
     T(0, '[h:Black-box]: test inputs/outputs only, no code (functional testing)', size=34))
beat(p, '''Equivalence partitioning divides the inputs into classes, where all values in a class behave the same way. Then we test one value from each class.
For example, if a valid mark is one to one hundred, there are three classes: less than one, which is invalid, one to one hundred, which is valid, and more than one hundred, which is invalid.''',
     S(2, 'Equivalence partitioning', size=36, color='red'), T(3, 'valid input 1..100  =>  3 classes:', size=34),
     T(4, '[r:< 1 (invalid)]   [g:1 to 100 (valid)]   [r:> 100 (invalid)]', size=34), T(5, 'test one value from each: e.g. -5, 50, 150', size=34, color='black'))
beat(p, f'''Boundary value analysis tests at the edges, because most errors happen at the boundaries. For one to one hundred, normal B V A tests the minimum, just above minimum,
a nominal value, just below maximum, and maximum: one, two, fifty, ninety nine and one hundred. Robust B V A also tests zero and one hundred one, just outside the range.''',
     Stamp(1650, 140, 'NUMERICAL'), S(7, 'Boundary value analysis (BVA)', size=36, color='red'),
     T(8, f"Normal (4n + 1): {', '.join(map(str, bv1))}", size=34), T(9, f"Robust (6n + 1): {', '.join(map(str, bvr))}", size=34))
beat(p, f'''For n variables, normal B V A needs four n plus one test cases. With two variables, x from one to one hundred, and y from one to two hundred,
we need nine test cases. We keep one variable at its nominal value, and move the other through its boundaries.''',
     T(11, 'n variables: 4n + 1;  two variables => 4(2) + 1 = [h:9] test cases', size=32),
     T(12, 'x ∈ [1, 100], y ∈ [1, 200]:', size=30, color='black'), T(13, '  '.join(f'({a},{b})' for a, b in bv2[:5]), size=28, color='black'),
     T(14, '  '.join(f'({a},{b})' for a, b in bv2[5:]), size=28, color='black'))

p = page('White-Box Testing', 8)
beat(p, '''White box testing tests the internal logic of the code. It is also called structural or glass box testing. Statement coverage checks that every statement runs at least once.
Branch coverage checks that every branch, true and false, of every decision is taken. Path coverage checks every independent path, using cyclomatic complexity.
Branch coverage is stronger than statement coverage.''',
     T(0, '[h:White-box]: tests internal logic (structural / glass-box)'), N(1, 1, '[k:Statement coverage]: every statement once', size=34),
     N(2, 2, '[k:Branch coverage]: every true & false branch', size=34), N(3, 3, '[k:Path coverage]: every independent path (V(G))', size=34),
     T(4, 'path ⊇ branch ⊇ statement coverage', size=34, color='green'))
beat(p, '''Mutation testing makes small changes, called mutants, to the program, like changing a plus to a minus. If the tests catch the change, the mutant is killed.
It measures how good the test cases are. Regression testing re runs old tests after every change, to make sure nothing that worked before is now broken.''',
     T(6, '[k:Mutation testing]: small changes (mutants); good tests kill them', size=32), T(7, '[k:Regression testing]: re-run old tests after every change', size=32),
     T(8, '[k:Smoke testing]: quick check that main functions work', size=32))
beat(p, '''Here is the comparison between black box and white box testing.''',
     Stamp(1650, 140, 'MOST ASKED'),
     Tab(180, 690, [280, 560, 560], 46, [['', 'Black-box', 'White-box'], ['knowledge of code', 'not needed', 'needed'], ['done by', 'testers, users', 'developers'],
         ['based on', 'requirements (SRS)', 'code structure'], ['techniques', 'EP, BVA, decision table', 'statement, branch, path coverage'], ['also called', 'functional / behavioural', 'structural / glass-box']],
         size=28, colors={(r, 0): 'red' for r in range(1, 6)}))

# ===================================================================================== CH 9
p = chapter(9)
beat(p, 'Chapter nine. Project management and estimation. COCOMO is the most asked numerical in this subject.')

p = page('Project Planning & COCOMO Modes', 9)
beat(p, '''The project manager plans the project: estimating size, effort, cost and time, scheduling, staffing, and managing risks.
Estimation techniques include L O C and function points for size, expert judgement, the Delphi technique where experts estimate anonymously in rounds,
and algorithmic models like COCOMO and Putnam.''',
     T(0, 'Planning: size -> effort -> cost & duration -> schedule -> staff -> risks', size=32),
     T(1, 'Estimation: LOC, FP, expert judgement, [k:Delphi], COCOMO, Putnam', size=32))
beat(p, '''COCOMO, the constructive cost model, was given by Barry Boehm in nineteen eighty one. It estimates effort from the size in K L O C.
It has three project types. Organic: a small, simple project by an experienced team, like a payroll system. Semi detached: medium size, mixed experience,
like a database system. Embedded: complex, with tight hardware and real time constraints, like an air traffic control system.''',
     Stamp(1650, 140, 'MOST ASKED'),
     Tab(180, 380, [300, 420, 420, 440], 56, [['Mode', 'Size / team', 'Constraints', 'Example'], ['Organic', '2-50 KLOC, experienced', 'few, flexible', 'payroll, inventory'],
         ['Semi-detached', '50-300 KLOC, mixed', 'medium', 'database, compiler'], ['Embedded', '300+ KLOC, tight', '[r:strict hardware / real-time]', 'air traffic control']], size=28,
         colors={(r, 0): 'red' for r in range(1, 4)}))
beat(p, '''Basic COCOMO formulas. Effort E equals a times K L O C to the power b, in person months. Development time D equals c times E to the power d, in months.
The constants for organic are two point four, one point zero five, two point five and zero point three eight. Semi detached: three, one point one two, two point five, zero point three five.
Embedded: three point six, one point two zero, two point five, zero point three two.''',
     T(9, '[h:E = a (KLOC)^b]  person-months       [h:D = c (E)^d]  months', size=34, color='red'),
     Tab(180, 760, [300, 140, 140, 140, 140], 50, [['Mode', 'a', 'b', 'c', 'd'], ['Organic', '2.4', '1.05', '2.5', '0.38'], ['Semi-detached', '3.0', '1.12', '2.5', '0.35'],
         ['Embedded', '3.6', '1.20', '2.5', '0.32']], size=28))

cb = {m: cocomo_basic(400, m) for m in BASIC}
p = page('Basic COCOMO - Numerical', 9)
beat(p, '''Classic numerical. A project has an estimated size of four hundred K L O C. Find the effort and development time for all three modes.
For organic: E equals two point four, times four hundred to the power one point zero five.''',
     Stamp(1650, 140, 'NUMERICAL'), T(0, 'Size = 400 KLOC. Find E and D for all three modes.', color='black'),
     T(1, f"Organic: E = 2.4 × (400)^1.05 = [h:{cb['Organic']['E']:,.2f} PM]", size=34), T(2, f"D = 2.5 × ({cb['Organic']['E']:,.2f})^0.38 = [h:{cb['Organic']['D']:.2f} months]", size=34, x=330))
beat(p, f'''That gives one thousand two hundred ninety five person months, and a time of about thirty eight months. In the same way, semi detached needs about two thousand four hundred sixty three
person months, and embedded needs about four thousand seven hundred seventy three person months, with almost the same time of about thirty eight months.''',
     Tab(180, 420, [300, 300, 280, 280, 330], 56, [['Mode', 'Effort E (PM)', 'Time D (months)', 'Avg staff E/D', 'Productivity (LOC/PM)']] +
         [[m, f"{r['E']:,.2f}", f"{r['D']:.2f}", f"{r['staff']:.0f}", f"{r['prod']:.1f}"] for m, r in cb.items()], size=28,
         colors={(r, 1): 'red' for r in range(1, 4)}))
beat(p, '''From these we can also find the average staff size, which is effort divided by time, and productivity, which is size divided by effort.
Notice: for the same size, embedded projects need almost four times the effort of organic ones.''',
     T(10, 'Average staff = E / D;   Productivity = KLOC / E', size=34), T(11, 'Same size: embedded ≈ 3.7 × organic effort', size=34, color='green'))

nom, adj = cocomo_inter(32, 'Organic', 1.15 * 0.86)
p = page('Intermediate COCOMO & COCOMO II', 9)
beat(p, '''Intermediate COCOMO makes the estimate more accurate using fifteen cost drivers. They are grouped as product attributes, like required reliability and complexity;
hardware attributes, like memory and time limits; personnel attributes, like analyst and programmer capability; and project attributes, like tools and schedule.''',
     T(0, '[h:Intermediate COCOMO]: 15 cost drivers', size=34), T(1, '[k:Product]: reliability, complexity · [k:Hardware]: memory, time', size=32),
     T(2, '[k:Personnel]: analyst & programmer capability · [k:Project]: tools, schedule', size=32))
beat(p, f'''Each driver gets a multiplier, and their product is the effort adjustment factor, E A F. Effort equals a times K L O C to the power b, times E A F.
For organic, a is three point two. Example: thirty two K L O C organic, with high reliability, one point one five, and high analyst capability, zero point eight six.
E A F is zero point nine nine. The nominal effort is about one hundred twenty one point eight, so the adjusted effort is about one hundred twenty point four person months.''',
     Stamp(1650, 140, 'NUMERICAL'), T(4, 'E = a (KLOC)^b × EAF;   organic a = 3.2, b = 1.05 (intermediate)', size=32, color='red'),
     T(5, f'32 KLOC: E_nominal = 3.2 × 32^1.05 = {nom:.2f} PM', size=32), T(6, f'EAF = 1.15 × 0.86 = {1.15 * 0.86:.3f}', size=32),
     T(7, f'E = {nom:.2f} × {1.15 * 0.86:.3f} = [h:{adj:.2f} PM]', size=36, color='red'))
beat(p, '''Detailed COCOMO applies the cost drivers to each phase separately. And COCOMO two is the modern version, with three stages: application composition,
using object points; early design, using function points; and post architecture, using detailed size and cost drivers.''',
     T(9, '[k:Detailed COCOMO]: drivers applied phase-wise', size=32), T(10, '[k:COCOMO II]: application composition (object points) ·', size=32),
     T(11, 'early design (FP) · post-architecture', size=32, x=360))

T_, rows = cpm(); te, sd, var = pert(2, 4, 12)
crit = [r[0] for r in rows if r[6] == 0]
p = page('Project Scheduling: CPM & PERT', 9)
nodes = {'S': (230, 720), 'A': (480, 610), 'B': (480, 830), 'C': (780, 720), 'D': (780, 560), 'E': (1080, 830), 'F': (1380, 680), 'End': (1650, 680)}
dur = {a: d for a, d, _ in ACT}
def nb(n):
    x, y = nodes[n]
    if n in ('S', 'End'): return Ell(x - 70, y - 36, 140, 72, 'Start' if n == 'S' else 'End', size=26)
    return Box(x - 75, y - 36, 150, 72, f'{n} ({dur[n]})', size=28, color='red' if n in crit else 'blue')
links = [('S', 'A'), ('S', 'B'), ('A', 'C'), ('A', 'D'), ('B', 'E'), ('C', 'E'), ('D', 'F'), ('E', 'F'), ('F', 'End')]
def ln(a, b):
    (x1, y1), (x2, y2) = nodes[a], nodes[b]; red = (a in crit or a == 'S') and (b in crit or b == 'End') and not (a == 'S' and b == 'B')
    return Arr(x1 + 75 if a != 'S' else x1 + 70, y1, x2 - 75 if b != 'End' else x2 - 70, y2, color='red' if red else 'black')
beat(p, '''Scheduling uses a network of activities. In C P M, the critical path method, we find the longest path through the network. That is the minimum time to finish the project.
Here are six activities with their times in weeks and their predecessors.''',
     Stamp(1650, 140, 'NUMERICAL'), T(0, '[h:Critical path] = longest path = minimum project time', size=32),
     T(1, 'A(3), B(4) start;  C(2), D(6) after A;  E(3) after B, C;  F(2) after D, E', size=30, color='black'),
     *[nb(n) for n in nodes], *[ln(a, b) for a, b in links])
beat(p, f'''Forward pass gives the earliest start and finish. Backward pass gives the latest start and finish. Slack is latest start minus earliest start.
Activities with zero slack are critical. Here the critical path is A, D, F, with a total of eleven weeks. C and E have one week of slack, and B has two weeks.''',
     Tab(1060, 300, [70, 70, 90, 90, 90, 90, 100], 42, [['Act', 'Dur', 'ES', 'EF', 'LS', 'LF', 'Slack']] + [[str(c) for c in r] for r in rows], size=24,
         colors={(i + 1, 6): 'red' for i, r in enumerate(rows) if r[6] == 0}),
     T(4, f"Critical path: [h:{' - '.join(crit)}] = {T_} weeks", size=32, color='red'))
beat(p, f'''PERT handles uncertain times using three estimates: optimistic a, most likely m, and pessimistic b. Expected time is a plus four m plus b, divided by six.
For a equals two, m equals four, and b equals twelve, the expected time is five weeks. The standard deviation is b minus a by six, about one point six seven.''',
     T(13, f'[k:PERT]: te = (a + 4m + b) / 6 = (2 + 16 + 12) / 6 = [h:{te:.0f}]', size=32), T(14, f'σ = (b - a) / 6 = {sd:.2f};  variance σ² = {var:.2f}', size=32))

p = page('Risk Management', 9)
beat(p, '''A risk is a problem that may happen in the future and hurt the project. There are project risks, like budget and schedule problems;
technical risks, like new technology that may not work; and business risks, like no market for the product.''',
     T(0, '[h:Risk] = possible future problem'), T(1, '[k:Project] (budget, schedule) · [k:Technical] (new tech) · [k:Business] (market)', size=32))
beat(p, '''Risk management has four steps. Identify the risks. Analyse them, by estimating the probability and the impact. Plan how to handle them,
by avoiding, transferring, reducing or accepting. And monitor them throughout the project. The R M M M plan means risk mitigation, monitoring and management.''',
     *[Box(200 + 390 * k, 380, 320, 66, s, size=26, color='blue') for k, s in enumerate(['Identify', 'Analyse', 'Plan', 'Monitor'])],
     *[Arr(520 + 390 * k, 413, 590 + 390 * k, 413) for k in range(3)], T(6, '[h:RMMM] = Risk Mitigation, Monitoring & Management', size=34),
     Stamp(1650, 140))
beat(p, f'''Risk exposure is the probability of the risk, times the loss if it happens. Example: there is a forty percent chance that a key developer leaves,
and the loss would be two lakh rupees. Risk exposure is zero point four times two lakh, which is eighty thousand rupees. Higher exposure means higher priority.''',
     T(8, '[h:Risk exposure RE = P × C]  (probability × cost of loss)', size=36, color='red'), T(9, 'P = 0.4 (key developer leaves), C = Rs 2,00,000', size=34),
     T(10, f'RE = 0.4 × 2,00,000 = [h:Rs {risk_exposure(0.4, 200000):,.0f}]', size=36, color='red'))

# ===================================================================================== CH 10
p = chapter(10)
beat(p, 'Chapter ten. Quality, reliability and maintenance.')

p = page('Software Quality & SQA', 10)
beat(p, '''Software quality means the software meets its requirements and the user's needs. McCall's quality model groups quality factors into three groups.
Product operation: correctness, reliability, efficiency, integrity and usability. Product revision: maintainability, flexibility and testability.
And product transition: portability, reusability and interoperability.''',
     S(0, "McCall's quality factors", size=36, color='red'), T(1, '[k:Operation]: correctness, reliability, efficiency, integrity, usability', size=32),
     T(2, '[k:Revision]: maintainability, flexibility, testability', size=32), T(3, '[k:Transition]: portability, reusability, interoperability', size=32))
beat(p, '''S Q A, software quality assurance, is a set of planned activities to make sure the process and the product meet quality standards.
It includes reviews, audits, standards and testing. Formal technical reviews include the walkthrough, which is informal and led by the author,
and the inspection, which is formal, led by a trained moderator, and uses checklists.''',
     T(5, '[h:SQA] = planned activities to ensure quality of process & product', size=32), T(6, '[k:Walkthrough]: informal, led by author', size=32),
     T(7, '[k:Inspection]: formal, moderator, checklists, most effective', size=32))
beat(p, '''I S O nine thousand one is an international standard for quality management systems. It is general, for any industry, and focuses on documented processes.
The company is certified after an audit. The difference from C M M: I S O is a pass or fail certificate, while C M M has five levels of maturity.''',
     Stamp(1650, 140), T(9, '[h:ISO 9001]: quality management standard (any industry)', size=32), T(10, 'ISO = certificate (pass / fail);  CMM = 5 maturity levels', size=32, color='green'))

lv = [('1 Initial', 'ad hoc, chaotic'), ('2 Repeatable', 'basic project mgmt'), ('3 Defined', 'standard org process'), ('4 Managed', 'measured (metrics)'), ('5 Optimizing', 'continuous improvement')]
p = page('SEI CMM Levels & Six Sigma', 10)
beat(p, '''The capability maturity model, C M M, was developed by the Software Engineering Institute at Carnegie Mellon. It rates how mature an organisation's software process is,
on five levels.''',
     T(0, '[h:CMM] (SEI, Carnegie Mellon): process maturity in 5 levels', size=34), Stamp(1650, 140, 'MOST ASKED'),
     *[Box(980 + 140 * k, 760 - 110 * k, 300, 80, None, color='blue') for k in range(5)],
     *[T(0, a, x=995 + 140 * k, y=800 - 110 * k, size=28, color='red') for k, (a, b) in enumerate(lv)],
     *[T(0, b, x=995 + 140 * k, y=830 - 110 * k, size=20, color='blue') for k, (a, b) in enumerate(lv)])
beat(p, '''Level one, initial: the process is ad hoc and chaotic, and success depends on individual heroes. Level two, repeatable: basic project management,
so earlier successes can be repeated. Level three, defined: a standard process is documented for the whole organisation. Level four, managed: the process and quality are measured with metrics.
Level five, optimizing: continuous process improvement.''',
     *[T(2 + k, f'[r:L{k + 1}] {a[2:]}: {b}', size=32) for k, (a, b) in enumerate(lv)],
     T(8, 'KPAs: L2 req. mgmt, planning, SQA, SCM · L3 training, peer reviews', size=28, color='green'), T(9, 'L4 quantitative mgmt · L5 defect prevention', size=28, color='green'))
beat(p, '''C M M I, capability maturity model integration, is the newer version. Six Sigma is a quality method that aims for at most three point four defects per million opportunities.
It uses D M A I C: define, measure, analyse, improve and control.''',
     T(11, '[k:CMMI] = newer, integrated version', size=32), T(12, '[k:Six Sigma]: ≤ 3.4 defects per million;  [h:DMAIC]', size=32),
     T(13, 'Define · Measure · Analyse · Improve · Control', size=32, color='green'))

av = availability(500, 20)
p = page('Software Reliability', 10)
beat(p, '''Software reliability is the probability that the software works without failure for a given time, in a given environment. Measures of reliability are:
M T T F, mean time to failure. M T T R, mean time to repair. M T B F, mean time between failures, which is M T T F plus M T T R.
Also POFOD, the probability of failure on demand, and ROCOF, the rate of occurrence of failures.''',
     T(0, '[h:Reliability] = P(no failure for time t in an environment)', size=34), T(1, '[k:MTTF]: mean time to failure   [k:MTTR]: mean time to repair', size=32),
     T(2, '[k:MTBF] = MTTF + MTTR   ·   POFOD   ·   ROCOF', size=32))
beat(p, f'''Availability is the fraction of time the system is working: M T T F divided by M T T F plus M T T R. Example: M T T F is five hundred hours and M T T R is twenty hours.
M T B F is five hundred twenty hours, and availability is five hundred by five hundred twenty, which is about ninety six point one five percent.''',
     Stamp(1650, 140, 'NUMERICAL'), T(4, '[h:Availability = MTTF / (MTTF + MTTR)]', size=36, color='red'),
     T(5, 'MTTF = 500 h, MTTR = 20 h', size=34, color='black'), T(6, f'MTBF = 500 + 20 = {av[0]} h', size=34),
     T(7, f'Availability = 500 / 520 = [h:{av[1] * 100:.2f}%]', size=36, color='red'))
beat(p, '''Reliability growth models, like the Jelinski Moranda model and Musa's basic execution time model, predict how reliability improves as bugs are found and fixed during testing.''',
     T(9, 'Reliability growth models: Jelinski-Moranda, Musa (basic execution time)', size=32))

mt = [('Perfective', 50, 'new features, better performance'), ('Adaptive', 25, 'new OS, hardware, laws'), ('Corrective', 21, 'fix bugs'), ('Preventive', 4, 'prevent future problems')]
p = page('Software Maintenance & Re-engineering', 10)
beat(p, '''Software maintenance means changing the software after delivery. There are four types. Corrective maintenance fixes bugs. Adaptive maintenance adapts the software
to a new environment, like a new operating system or new laws. Perfective maintenance adds new features or improves performance, as users ask.
And preventive maintenance improves the code to prevent future problems. Perfective maintenance takes the largest share, about half.''',
     Stamp(1650, 140, 'MOST ASKED'), *[T(k, f'[r:{n}] - {d}', size=34) for k, (n, s_, d) in enumerate(mt)],
     *[x for k, (n, s_, d) in enumerate(mt) for x in (Box(1100, L(k) - 34, max(30, s_ * 11), 42, None, color='blue', fill='yellow'), T(0, f'{s_}%', x=1112 + max(30, s_ * 11), y=L(k) - 4, size=28, color='black'))])
beat(p, '''Reverse engineering analyses existing software to recover its design and specification, for example from old code with no documents.
Re engineering means reverse engineering, then restructuring, then forward engineering, to build an improved version. Forward engineering is the normal process,
from requirements to code. Legacy systems are old but important systems that are often re engineered.''',
     T(6, '[k:Reverse engineering]: code -> design & specification', size=32), T(7, '[k:Forward engineering]: requirements -> design -> code', size=32),
     T(8, '[k:Re-engineering] = reverse + restructure + forward', size=32),
     Box(200, 730, 260, 66, 'Old system', size=26), Box(560, 730, 300, 66, 'Reverse eng.', size=26, color='red'), Box(960, 730, 280, 66, 'Restructure', size=26, color='blue'),
     Box(1340, 730, 300, 66, 'Forward eng.', size=26, color='green'), Arr(460, 763, 560, 763), Arr(860, 763, 960, 763), Arr(1240, 763, 1340, 763))
beat(p, '''The maintenance cost depends on the program's age, structure, documentation, staff and the domain. Belady and Lehman's model says that maintenance effort grows
when the code is complex and the team does not know it well.''',
     T(14, 'Maintenance cost: age, structure, documentation, staff, domain (Belady-Lehman)', size=30))

p = page('Configuration Management & CASE Tools', 10)
beat(p, '''Software configuration management, S C M, controls changes to software. A software configuration item is any part of the project that is controlled,
like the code, the S R S or test cases. A baseline is a reviewed and approved version that can be changed only through a formal change process.''',
     T(0, '[h:SCM] = control changes to software', size=34), T(1, '[k:SCI]: controlled item (code, SRS, tests)   [k:Baseline]: approved version', size=32))
beat(p, '''S C M activities are: identification of items, version control, change control, configuration auditing, and status reporting. In change control,
a change request is evaluated by the change control board, and if approved, the change is made, tested, and a new baseline is released. Tools like Git are used for version control.''',
     Stamp(1650, 140), T(3, 'Activities: identification · [h:version control] · [h:change control] · audit · status reporting', size=30),
     *[Box(200 + 320 * k, 470, 255, 70, s, size=24, color='blue') for k, s in enumerate(['Change request', 'CCB evaluates', 'Approve?', 'Make & test', 'New baseline'])],
     *[Arr(455 + 320 * k, 505, 520 + 320 * k, 505) for k in range(4)], T(0, 'CCB = change control board;  Git for version control', x=200, y=600, size=30, color='green'))
beat(p, '''CASE tools, computer aided software engineering tools, help in software development. Upper CASE tools help in the early phases, like requirements and design,
for example U M L and D F D tools. Lower CASE tools help in the later phases, like coding, testing and maintenance, for example code generators, debuggers and test tools.
Integrated CASE tools cover the whole life cycle.''',
     T(11, '[h:CASE] = Computer-Aided Software Engineering', size=34), T(12, '[k:Upper CASE]: requirements & design (UML, DFD tools)', size=32),
     T(13, '[k:Lower CASE]: coding, testing (code generators, debuggers)', size=32), T(14, '[k:Integrated CASE]: whole life cycle', size=32))

# ===================================================================================== CH 11
p = chapter(11)
beat(p, "Chapter eleven. Exam revision. If you're short on time, revise these first.")

p = page('Most Asked Exam Questions', 11)
qs = ['SDLC phases; waterfall vs spiral vs prototyping', 'Spiral model with diagram; V-model', 'Agile manifesto; Scrum roles, events, artifacts',
      'Functional vs non-functional; good SRS (IEEE 830)', 'DFD levels; data dictionary; decision table', 'Cohesion & coupling types (best to worst)',
      'UML: use case, class, sequence diagrams', 'Function points; Halstead; cyclomatic complexity', 'Black-box (EP, BVA) vs white-box testing',
      'Levels of testing; stubs & drivers; alpha / beta', 'COCOMO numerical; CPM / PERT; risk exposure', 'CMM levels; reliability (MTTF); maintenance types']
beat(p, '''Here are the most asked questions. S D L C phases and the comparison of models. The spiral model with its diagram, and the V model.
The agile manifesto and scrum. And functional versus non functional requirements, with the characteristics of a good S R S.''', *[T(k, f'{k + 1}. {q}', x=200, size=36) for k, q in enumerate(qs[:4])])
beat(p, '''D F D levels, data dictionary and decision tables. Cohesion and coupling types. U M L diagrams. And the metrics numericals: function points, Halstead,
and cyclomatic complexity.''', *[T(k, f'{k + 1}. {q}', x=200, size=36) for k, q in enumerate(qs) if 4 <= k < 8])
beat(p, '''Black box versus white box testing, with boundary value analysis. Levels of testing with stubs and drivers. The COCOMO numerical, C P M and risk exposure.
And C M M levels, reliability, and the types of maintenance.''', *[T(k, f'{k + 1}. {q}', x=200, size=36) for k, q in enumerate(qs) if k >= 8])
beat(p, '''One last exam tip. Draw neat diagrams for every model and U M L question; diagrams carry a lot of marks. And in numericals, write the formula first.
That way you still get step marks, even if your final answer goes wrong.''',
     T(13, 'Tip: [h:draw neat diagrams] & write the formula first => step marks!', color='red'))

p = page('All the Best!', 11, kind='outro')
beat(p, '''That's the complete software engineering subject. If this helped you, share it with your friends who have the exam,
and subscribe to TechVibe24 for more one shot videos. Tell me in the comments which subject you want next. All the best for your exam!''')

if __name__ == '__main__':
    json.dump({'pages': PAGES, 'chapters': CHAPTERS}, open('se_script.json', 'w'), indent=1, ensure_ascii=False)
    nb = sum(len(p['beats']) for p in PAGES); nw = sum(len(b['say'].split()) for p in PAGES for b in p['beats'])
    print('pages', len(PAGES), 'beats', nb, 'words', nw, 'est minutes', round(nw / 150, 1))
