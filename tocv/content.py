'''Theory of Computation one-shot: narration beats + handwritten note elements for every page.
Markup inside text: [r:red] [g:green] [k:black] [h:yellow highlight] [p:pink highlight]'''
import json, math
from toc_numericals import *

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
def Arr(x1, y1, x2, y2, color='black', label=None, lx=0, ly=-14, curve=0, head=True, size=28, both=False, lc=None): return dict(t='arrow', p1=(round(x1), round(y1)), p2=(round(x2), round(y2)), color=color, label=label, lx=round(lx), ly=round(ly), curve=curve, head=head, size=size, both=both, lc=lc or color)
def Ln(pts, color='black', w=4): return dict(t='line', pts=[(round(a), round(b)) for a, b in pts], color=color, w=w)
def Tab(x, y, cw, rh, rows, color='black', size=30, hdr=True, order='row', colors=None, fills=None): return dict(t='table', x=x, y=y, cw=cw, rh=rh, rows=rows, color=color, size=size, hdr=hdr, order=order, colors={f'{r},{c}': v for (r, c), v in (colors or {}).items()}, fills={f'{r},{c}': v for (r, c), v in (fills or {}).items()})
def Stamp(x, y, text='IMP!', color='red', rot=-8, size=34): return dict(t='stamp', x=x, y=y, text=text, color=color, rot=rot, size=size)

# ---------- automata drawing
R0 = 42
def State(p, name, final=False, start=False, color='blue', size=28):
    cx, cy = p; out = [Ell(cx - R0, cy - R0, 2 * R0, 2 * R0, name, color=color, size=size)]
    if final: out.append(Ell(cx - R0 + 8, cy - R0 + 8, 2 * R0 - 16, 2 * R0 - 16, None, color=color))
    if start: out.append(Arr(cx - R0 - 90, cy, cx - R0 - 4, cy, color='green'))
    return out
def Edge(a, b, label, curve=0, color='black', off=0, size=28, pad=20):
    (x1, y1), (x2, y2) = a, b; dx, dy = x2 - x1, y2 - y1; d = math.hypot(dx, dy); ux, uy = dx / d, dy / d; nx, ny = -uy, ux
    p1 = (x1 + ux * R0 + nx * off, y1 + uy * R0 + ny * off); p2 = (x2 - ux * (R0 + 4) + nx * off, y2 - uy * (R0 + 4) + ny * off)
    # the renderer already puts the label at the apex of a curve; we only push it a little outwards
    if curve: sx, sy = (nx, ny) if curve > 0 else (-nx, -ny)
    else: sx, sy = (0, -1) if abs(dx) >= abs(dy) else (1, 0)
    if sy > .5: lx, ly = 0, 16 + size * .8              # below
    elif sy < -.5: lx, ly = 0, -16                      # above
    else: lx, ly = sx * (pad + 12), size * .35          # beside
    return Arr(*p1, *p2, color=color, label=label, lx=lx, ly=ly, curve=curve, size=size)
def Loop(p, label, pos='top', color='black', size=28):
    cx, cy = p
    if pos == 'top': return Arr(cx - 22, cy - R0 + 3, cx + 22, cy - R0 + 3, color=color, curve=-140, label=label, ly=-12, size=size)
    return Arr(cx + 22, cy + R0 - 3, cx - 22, cy + R0 - 3, color=color, curve=-140, label=label, ly=34, size=size)

CHAPTERS = [
 (1, 'Basics of Theory of Computation', ['Alphabet, string, language', 'Operations on languages', 'Chomsky hierarchy'], 3),
 (2, 'Deterministic Finite Automata', ['DFA as a 5-tuple', 'Designing DFAs', 'Divisibility DFA'], 5),
 (3, 'NFA & Epsilon-NFA', ['NFA vs DFA', 'NFA to DFA (subset construction)', 'Epsilon-closure'], 5),
 (4, 'DFA Minimization & Moore/Mealy', ['Equivalent states', 'Partition method', 'Moore & Mealy machines'], 5),
 (5, 'Regular Expressions', ['Identities', 'RE to FA', "FA to RE (Arden's theorem)"], 5),
 (6, 'Properties of Regular Languages', ['Pumping lemma', 'Closure properties', 'Myhill-Nerode'], 5),
 (7, 'Context-Free Grammars', ['Derivations & parse trees', 'Ambiguity', 'Simplification', 'CNF & GNF'], 5),
 (8, 'CYK & Properties of CFLs', ['CYK algorithm', 'Pumping lemma for CFL', 'Closure properties'], 5),
 (9, 'Pushdown Automata', ['PDA as a 7-tuple', 'PDA for a^n b^n', 'DPDA vs NPDA'], 5),
 (10, 'Turing Machines', ['TM as a 7-tuple', 'TM for a^n b^n', 'Variants & LBA', 'Chomsky hierarchy'], 5),
 (11, 'Decidability & Complexity', ['Halting problem', "Rice's theorem & PCP", 'Decision properties', 'P, NP, NP-complete'], 5),
 (12, 'Exam Revision', ['Most asked questions', 'Last-minute tips'], 5),
]
def chapter(i):
    n, t, subs, stars = CHAPTERS[i - 1]
    return page(t, n, kind='chapter', num=n, subs=subs, stars=stars)

# =====================================================================================
p = page('Theory of Computation', 0, kind='cover')
beat(p, '''Theory of Computation. The complete subject in one video. Simple explanations, handwritten notes, state diagrams,
and every important exam problem solved step by step.''')
beat(p, '''This works for B Tech computer science in almost every university. A K T U, Anna University, V T U, J N T U,
Mumbai, Pune, and private universities too. And it covers the full theory of computation part of GATE. So grab a pen, and let's start.''')

p = page('Contents', 0)
items = ['Basics & Chomsky hierarchy', '[h:DFA]  (design, divisibility)', '[h:NFA]  (NFA to DFA)', '[h:DFA minimization]  & Moore / Mealy',
         "Regular expressions  (Arden's theorem)", '[h:Pumping lemma]  & closure properties', '[h:CFG]  (ambiguity, CNF)', 'CYK & properties of CFLs',
         '[h:Pushdown automata]', '[h:Turing machines]', '[h:Decidability]  & P vs NP', 'Exam revision']
beat(p, "Here's our plan. Twelve chapters, from the basics to the exam problems.", T(0, 'What we will cover today', size=42, font='bold', color='black'))
beat(p, '''We start with the basics, then finite automata: D F A, N F A, minimization, regular expressions, and the pumping lemma.''',
     *[T(1 + k, f'{k + 1}.  {items[k]}', x=200) for k in range(6)])
beat(p, '''Then context free grammars, the C Y K algorithm, pushdown automata, Turing machines, decidability, and P versus N P.
At the end, a quick revision of the most asked questions. The highlighted topics are the most important.''',
     *[T(7 + k, f'{k + 7}.  {items[k + 6]}', x=200) for k in range(6)], Stamp(1520, 560, 'MOST ASKED', rot=-10))

# ===================================================================================== CH 1
p = chapter(1)
beat(p, "Chapter one. The basics. Let's learn the language of this subject first.")

p = page('Alphabet, String & Language', 1)
beat(p, '''Theory of computation studies what computers can and cannot do, using simple mathematical machines called automata.
An alphabet, written as sigma, is a finite, non empty set of symbols. For example, sigma equals zero and one, or sigma equals a and b.''',
     T(0, '[h:Automata] = simple mathematical models of computers'), T(1, '[h:Alphabet Σ] = finite, non-empty set of symbols'),
     T(2, 'Σ = {0, 1}   or   Σ = {a, b}', color='black'))
beat(p, '''A string is a finite sequence of symbols from the alphabet, like a b b a. Its length is the number of symbols, so the length of a b b a is four.
The empty string, written epsilon, has length zero. Sigma star is the set of all strings over sigma, including epsilon. Sigma plus is the same, without epsilon.''',
     T(4, '[h:String]: finite sequence of symbols, e.g. w = abba,  |w| = 4'), T(5, '[h:ε] = empty string,  |ε| = 0'),
     T(6, 'Σ* = all strings (including ε);   Σ+ = Σ* - {ε}'), T(7, 'Σ^k = strings of length k;  |Σ^k| = |Σ|^k', color='green'))
beat(p, '''A language is any set of strings over an alphabet. It can be finite, like the strings of length two, or infinite, like all strings that start with a.
The empty language, written phi, has no strings at all, which is different from the language that contains only epsilon.''',
     T(9, '[h:Language L] ⊆ Σ*  (any set of strings)'), T(10, 'e.g. L = {aa, ab, ba, bb} (finite),  L = {w | w starts with a} (infinite)', size=34),
     T(11, '∅ = no strings  ≠  {ε} = one string (the empty one)', color='red'), Stamp(1600, 700))

p = page('Operations & The Chomsky Hierarchy', 1)
beat(p, '''Operations on languages. Union, intersection and complement work like sets. Concatenation joins every string of L one with every string of L two.
The Kleene star of L is all strings formed by joining zero or more strings of L. And the reverse of a string writes it backwards.''',
     T(0, 'L1 ∪ L2,  L1 ∩ L2,  complement,  [k:L1L2] (concatenation)'), T(1, '[k:L*] = ε ∪ L ∪ LL ∪ LLL ...   (Kleene star);   reverse: (abc)^R = cba'))
beat(p, '''The Chomsky hierarchy arranges languages in four types. Type three, regular languages, are generated by regular grammars and accepted by finite automata.
Type two, context free languages, are accepted by pushdown automata. Type one, context sensitive languages, by linear bounded automata.
And type zero, recursively enumerable languages, are accepted by Turing machines. Each type contains the one below it.''',
     Stamp(1650, 140, 'MOST ASKED'),
     Tab(180, 330, [170, 380, 520, 500], 56, [['Type', 'Language', 'Grammar', 'Machine'], ['3', 'Regular', 'regular (A -> aB | a)', 'finite automata'],
         ['2', 'Context-free', 'A -> α', 'pushdown automata'], ['1', 'Context-sensitive', 'αAβ -> αγβ  (|γ| ≥ 1)', 'linear bounded automata'],
         ['0', 'Recursively enumerable', 'unrestricted', 'Turing machine']], size=28, colors={(r, 3): 'red' for r in range(1, 5)}))
beat(p, '''Remember it as nested circles. Regular is the smallest, inside context free, inside context sensitive, inside recursively enumerable.''',
     Ell(980, 640, 840, 370, None, color='blue'), Ell(1090, 685, 620, 280, None, color='green'), Ell(1200, 730, 400, 190, None, color='red'),
     Ell(1300, 775, 200, 100, 'Regular', size=26, color='black'), T(0, 'RE', x=1015, y=835, size=28, color='blue'), T(0, 'CSL', x=1115, y=835, size=28, color='green'),
     T(0, 'CFL', x=1222, y=835, size=28, color='red'), T(12, 'Regular ⊂ CFL ⊂ CSL ⊂ RE', color='red', size=36))

# ===================================================================================== CH 2
p = chapter(2)
beat(p, 'Chapter two. Deterministic finite automata. Designing D F As is the most common exam question.')

p = page('DFA: Definition', 2)
beat(p, '''A deterministic finite automaton, or D F A, is a machine with a finite number of states. It reads the input one symbol at a time,
and moves from state to state. It has no memory other than its current state.''',
     T(0, '[h:DFA]: finite states, reads input left to right, no extra memory'))
beat(p, '''Formally, a D F A is a five tuple: Q, sigma, delta, q zero, F. Q is the finite set of states. Sigma is the input alphabet.
Delta is the transition function, from Q cross sigma to Q. q zero is the start state. And F is the set of final, or accepting, states.''',
     Stamp(1650, 140), T(2, 'M = (Q, Σ, δ, q0, F)', color='black', size=42), N(3, 'Q', 'finite set of states', size=34), N(4, 'Σ', 'input alphabet', size=34),
     N(5, 'δ', 'transition function  δ : Q × Σ -> Q', size=34), N(6, 'q0', 'start state', size=34), N(7, 'F', 'set of final states, F ⊆ Q', size=34))
beat(p, '''In a D F A, every state has exactly one move for every input symbol. The string is accepted if the machine ends in a final state after reading the whole input.
We draw states as circles, the start state with an arrow, and final states as double circles.''',
     T(9, 'exactly [r:one] move for each state and symbol;  accept if it ends in F'),
     *State((1300, 820), 'q', start=True), T(0, 'start state', x=1210, y=915, size=26, color='green'),
     *State((1600, 820), 'f', final=True), T(0, 'final state', x=1530, y=915, size=26, color='blue'))

pos = {'q0': (1050, 640), 'q1': (1380, 640), 'q2': (1710, 640)}
trace = run_dfa(ENDS_AB, 'q0', 'abab')
p = page('DFA Design: Strings Ending with "ab"', 2)
beat(p, '''Let's design a D F A for all strings over a and b that end with a b. First, write a few strings in the language: a b, a a b, b a b, a b a b.
We need three states. q zero means we have not seen anything useful. q one means the last symbol was a. q two means the last two symbols were a b, which is the final state.''',
     Stamp(1650, 140, 'NUMERICAL'), T(0, 'L = { w ∈ {a, b}* | w ends with ab }', color='black'), T(1, 'e.g. ab, aab, bab, abab ...', size=34),
     T(2, '[k:q0]: nothing useful   [k:q1]: last symbol a   [k:q2]: last two ab ([r:final])', size=32))
beat(p, '''Now the moves. From q zero, a goes to q one, and b stays in q zero. From q one, a stays in q one, because the last symbol is still a, and b goes to q two.
From q two, a goes back to q one, and b goes back to q zero, because b b does not help us.''',
     *State(pos['q0'], 'q0', start=True), *State(pos['q1'], 'q1'), *State(pos['q2'], 'q2', final=True),
     Edge(pos['q0'], pos['q1'], 'a'), Edge(pos['q1'], pos['q2'], 'b', off=-10, curve=-60), Edge(pos['q2'], pos['q1'], 'a', curve=-60, off=-10),
     Edge(pos['q2'], pos['q0'], 'b', curve=-300), Loop(pos['q0'], 'b'), Loop(pos['q1'], 'a'),
     Tab(180, 420, [150, 150, 150], 54, [['δ', 'a', 'b'], ['-> q0', 'q1', 'q0'], ['q1', 'q1', 'q2'], ['* q2', 'q1', 'q0']], size=30))
beat(p, f'''Let's test the string a b a b. Start at q zero. a goes to q one, b to q two, a to q one, and b to q two. We end in q two, a final state, so a b a b is accepted.''',
     T(10, 'abab:  ' + ' -> '.join(trace) + '   [g:accepted ✓]', size=34, color='black'),
     T(11, 'Minimal DFA for "ends with a string of length n" has n + 1 states', size=32, color='green'))

pm = {'q0': (1100, 640), 'q1': (1420, 640), 'q2': (1740, 640)}
p = page('DFA for Binary Numbers Divisible by 3', 2)
beat(p, '''Another favourite: a D F A for binary numbers divisible by three. The trick is to keep the remainder. There are three possible remainders, zero, one and two,
so we need three states. When we read a new bit, the number doubles and the bit is added. So the new remainder is two times the old remainder plus the bit, mod three.''',
     Stamp(1650, 140, 'NUMERICAL'), T(0, 'States = remainders 0, 1, 2  (q0 = start & [r:final])'), T(1, 'new remainder = (2 × r + bit) mod 3', color='red', size=40))
beat(p, '''From q zero: zero gives zero, one gives one. From q one: zero gives two, and one gives three mod three, which is zero. From q two: zero gives four mod three, one,
and one gives five mod three, two.''',
     Tab(180, 380, [170, 170, 170], 54, [['δ', '0', '1'], ['->* q0', 'q0', 'q1'], ['q1', 'q2', 'q0'], ['q2', 'q1', 'q2']], size=30),
     *State(pm['q0'], 'q0', start=True, final=True), *State(pm['q1'], 'q1'), *State(pm['q2'], 'q2'),
     Edge(pm['q0'], pm['q1'], '1', curve=-70), Edge(pm['q1'], pm['q0'], '1', curve=-70), Edge(pm['q1'], pm['q2'], '0', curve=-70), Edge(pm['q2'], pm['q1'], '0', curve=-70),
     Loop(pm['q0'], '0'), Loop(pm['q2'], '1'))
beat(p, f'''Check: twelve is one one zero zero in binary. The path is q zero, q one, q zero, q zero, q zero. It ends in q zero, so twelve is divisible by three.
Ten is one zero one zero, which ends in q one, so it is not divisible. In general, binary numbers divisible by n need n states.''',
     T(10, f"12 = 1100: {' -> '.join(run_dfa(MOD3, 'q0', '1100'))}  [g:✓]", size=32, color='black'),
     T(11, f"10 = 1010: {' -> '.join(run_dfa(MOD3, 'q0', '1010'))}  [r:✗]", size=32, color='black'),
     T(12, 'Divisible by n (binary)  =>  n states', size=34, color='red'),
     T(13, 'Tip: #a mod 3 = 0 AND #b mod 2 = 0  =>  3 × 2 = 6 states (product)', size=32, color='green'))

pv = {'q0': (1150, 420), 'q1': (1560, 420), 'q2': (1150, 780), 'q3': (1560, 780)}
p = page("DFA for Even a's and Even b's", 2)
beat(p, '''Next: a D F A for strings with an even number of a's and an even number of b's. We track two things at once, whether the count of a's is even or odd,
and whether the count of b's is even or odd. That gives two times two, four states.''',
     Stamp(1650, 140, 'NUMERICAL'), T(0, "L = { w | #a even  AND  #b even }", color='black'),
     T(1, '[k:q0]: (even, even)  [r:start & final]', size=34), T(2, '[k:q1]: (odd a, even b)', size=34), T(3, '[k:q2]: (even a, odd b)', size=34), T(4, '[k:q3]: (odd, odd)', size=34))
beat(p, '''Reading a changes only the a count, so it moves left and right: q zero and q one swap, and q two and q three swap. Reading b changes only the b count, so it moves up and down:
q zero and q two swap, and q one and q three swap.''',
     *State(pv['q0'], 'q0', start=True, final=True), *State(pv['q1'], 'q1'), *State(pv['q2'], 'q2'), *State(pv['q3'], 'q3'),
     Edge(pv['q0'], pv['q1'], 'a', curve=-60), Edge(pv['q1'], pv['q0'], 'a', curve=-60), Edge(pv['q2'], pv['q3'], 'a', curve=-60), Edge(pv['q3'], pv['q2'], 'a', curve=-60),
     Edge(pv['q0'], pv['q2'], 'b', curve=-60), Edge(pv['q2'], pv['q0'], 'b', curve=-60), Edge(pv['q1'], pv['q3'], 'b', curve=-60), Edge(pv['q3'], pv['q1'], 'b', curve=-60))
beat(p, f'''Test a b a b. q zero, then a to q one, b to q three, a to q two, and b back to q zero. Two a's and two b's, and we end in q zero, so it is accepted.
If the question changes to even a's or even b's, keep the same machine, and only change the final states.''',
     T(7, "abab: " + ' -> '.join(run_dfa(EVEN, 'q0', 'abab')) + "  [g:✓]", size=32, color='black'),
     T(9, 'Same 4 states, change only F:', size=32, color='green'), T(10, '#a odd, #b odd => F = {q3}', size=32), T(11, '#a even OR #b even => F = {q0, q1, q2}', size=32))

# ===================================================================================== CH 3
p = chapter(3)
beat(p, 'Chapter three. Non deterministic finite automata, and how to convert them into D F As.')

pn = {'q0': (1100, 600), 'q1': (1420, 600), 'q2': (1740, 600)}
p = page('NFA: Definition', 3)
beat(p, '''In a non deterministic finite automaton, or N F A, a state can have zero, one, or many moves on the same symbol. So the machine can be in many states at once.
A string is accepted if at least one path ends in a final state. The only change in the five tuple is delta, which goes from Q cross sigma to the power set of Q.''',
     T(0, '[h:NFA]: zero, one or many moves on a symbol'), T(1, 'accept if [r:at least one] path ends in a final state'),
     T(2, 'M = (Q, Σ, δ, q0, F),   δ : Q × Σ -> 2^Q', color='black'))
beat(p, '''Example: strings over zero and one whose second last symbol is one. q zero loops on zero and one, and guesses on one that this is the second last symbol, moving to q one.
Then any symbol takes it to q two, the final state. This N F A has only three states, and it is much easier to design than the D F A.''',
     Stamp(1650, 140), T(4, 'L = { w | second last symbol is 1 }', color='black'),
     *State(pn['q0'], 'q0', start=True), *State(pn['q1'], 'q1'), *State(pn['q2'], 'q2', final=True),
     Loop(pn['q0'], '0, 1'), Edge(pn['q0'], pn['q1'], '1'), Edge(pn['q1'], pn['q2'], '0, 1'))
beat(p, '''Important facts. Every N F A can be converted to an equivalent D F A, so both accept exactly the regular languages. But the D F A may need up to two to the power n states.''',
     Tab(180, 690, [380, 520, 520], 54, [['', 'DFA', 'NFA'], ['moves per symbol', 'exactly one', 'zero, one or many'], ['ε-moves', 'no', 'allowed (ε-NFA)'],
         ['power', 'regular languages', '[g:same] (regular languages)']], size=28, colors={(r, 0): 'red' for r in range(1, 4)}),
     T(14, 'n-state NFA  ->  DFA with up to [h:2^n] states', size=34, color='red'))

D, Tr = subset(); names = 'ABCD'
p = page('NFA to DFA: Subset Construction', 3)
beat(p, '''To convert an N F A to a D F A, we use subset construction. Each D F A state is a set of N F A states. Start with the set containing only q zero.
For each set and each symbol, find all the N F A states we can reach. If it is a new set, add it as a new D F A state.''',
     Stamp(1650, 140, 'NUMERICAL'), T(0, 'DFA state = set of NFA states;  start = {q0}'), T(1, 'δ_D(S, a) = ∪ δ_N(q, a) for q in S'))
beat(p, '''Let's convert our N F A. From q zero, zero gives q zero, and one gives q zero and q one, a new state. From q zero q one, zero gives q zero and q two,
and one gives q zero, q one and q two. We continue until no new sets appear. We get four states.''',
     Tab(180, 330, [130, 380, 380, 380], 56, [['DFA', 'NFA states', 'on 0', 'on 1']] +
         [[names[i] + (' *' if 'q2' in S else ''), sname(S), names[D.index(Tr[(S, '0')])] + ' = ' + sname(Tr[(S, '0')]), names[D.index(Tr[(S, '1')])] + ' = ' + sname(Tr[(S, '1')])]
          for i, S in enumerate(D)], size=28, colors={(3, 0): 'red', (4, 0): 'red'}))
beat(p, '''Any set that contains the N F A final state q two is a final state of the D F A. So C and D are final. The N F A had three states, and the D F A has four.''',
     T(9, 'Final DFA states: any set containing q2  =>  [h:C, D]', color='red'),
     T(10, 'NFA: 3 states  ->  DFA: 4 states  (≤ 2^3 = 8)', color='green'))

pe = {'q0': (1100, 560), 'q1': (1420, 560), 'q2': (1740, 560)}
p = page('Epsilon-NFA & Epsilon-Closure', 3)
beat(p, '''An epsilon N F A can also move without reading any input, using epsilon moves. The epsilon closure of a state is the set of all states we can reach
using only epsilon moves, including the state itself.''',
     T(0, '[h:ε-NFA]: can move without reading input'), T(1, '[h:ε-closure(q)] = q + all states reachable by ε-moves only'))
beat(p, '''Example. q zero has an epsilon move to q one, q one loops on a, q one has an epsilon move to q two, and q two loops on b. The epsilon closure of q zero is q zero, q one and q two.
The epsilon closure of q one is q one and q two. And the epsilon closure of q two is only q two.''',
     Stamp(1650, 140),
     *State(pe['q0'], 'q0', start=True), *State(pe['q1'], 'q1'), *State(pe['q2'], 'q2', final=True),
     Edge(pe['q0'], pe['q1'], 'ε'), Edge(pe['q1'], pe['q2'], 'ε'), Loop(pe['q1'], 'a'), Loop(pe['q2'], 'b'),
     T(9, 'ε-closure(q0) = {q0, q1, q2}', color='red'), T(10, 'ε-closure(q1) = {q1, q2}', color='red'), T(11, 'ε-closure(q2) = {q2}', color='red'))
beat(p, '''To convert an epsilon N F A to a D F A, the start state becomes the epsilon closure of q zero, and after every move we take the epsilon closure again.
This machine accepts a star b star.''',
     T(13, 'ε-NFA -> DFA: start = ε-closure(q0); after each move, take ε-closure', size=32), T(14, 'This ε-NFA accepts a*b*', size=34, color='green'))

# ===================================================================================== CH 4
p = chapter(4)
beat(p, 'Chapter four. D F A minimization, and Moore and Mealy machines.')

unreach, steps = minimise()
mrows = [['δ', 'a', 'b']] + [[('-> ' if q == 'A' else '* ' if q == 'E' else '') + q, MIN[(q, 'a')], MIN[(q, 'b')]] for q in 'ABCDEF']
p = page('DFA Minimization: Partition Method', 4)
beat(p, '''Minimization finds the D F A with the fewest states for the same language. Two states are equivalent if, for every input string, both lead to final states or both lead to non final states.
Step one: remove unreachable states. Step two: split the states into groups again and again, until no group changes.''',
     Stamp(1650, 140, 'NUMERICAL'), T(0, '[h:Equivalent states]: same accept / reject result for every string', size=34),
     T(1, '1) remove unreachable states   2) refine groups until no change', size=34))
beat(p, '''Here is a D F A with six states, A to F. A is the start state, and E is the final state. No arrow comes into F, so F is unreachable. We remove it.''',
     Tab(180, 330, [140, 120, 120], 50, mrows, size=28, colors={(6, 0): 'red', (6, 1): 'red', (6, 2): 'red'}),
     T(0, 'F is [r:unreachable]  ->  remove', x=180, y=L(9) + 8, size=32, color='red'))
def blk(P): return '  '.join('{' + ''.join(b) + '}' for b in P)
beat(p, f'''Zero equivalence: split into non final states A, B, C, D, and the final state E. One equivalence: on input b, D goes to the final state E, but A, B and C do not.
So D separates. Two equivalence: on b, B goes to D, but A and C go to C. So B separates. Three equivalence: nothing changes, so we stop. A and C are equivalent.''',
     T(0, f'P0:  {blk(steps[0])}', x=720, y=L(2), size=34), T(0, f'P1:  {blk(steps[1])}', x=720, y=L(3), size=34),
     T(0, f'P2:  {blk(steps[2])}', x=720, y=L(4), size=34), T(0, f'P3:  {blk(steps[3])}   (no change)', x=720, y=L(5), size=34),
     T(0, '=> [h:A ≡ C]', x=720, y=L(6), size=38, color='red'))
pq = {'AC': (900, 830), 'B': (1180, 830), 'D': (1460, 830), 'E': (1740, 830)}
beat(p, '''So the minimized D F A has four states: A C together, B, D and E. This is the D F A for a or b star, a b b.''',
     *State(pq['AC'], 'AC', start=True), *State(pq['B'], 'B'), *State(pq['D'], 'D'), *State(pq['E'], 'E', final=True),
     Edge(pq['AC'], pq['B'], 'a'), Edge(pq['B'], pq['D'], 'b'), Edge(pq['D'], pq['E'], 'b'), Edge(pq['D'], pq['B'], 'a', curve=-80, off=8),
     Edge(pq['E'], pq['B'], 'a', curve=-170), Edge(pq['E'], pq['AC'], 'b', curve=450), Loop(pq['AC'], 'b', pos='bottom'), Loop(pq['B'], 'a'),
     T(14, '4 states;  accepts (a|b)*abb', x=180, size=32, color='green'))

p = page('Moore & Mealy Machines', 4)
beat(p, '''Finite automata only say yes or no. Moore and Mealy machines produce an output. In a Moore machine, the output depends only on the current state.
It is a six tuple, with an output alphabet delta, and an output function lambda from Q to delta. For an input of length n, a Moore machine gives n plus one outputs.''',
     T(0, '[h:Moore]: output depends on [r:state] only;   λ : Q -> Δ', size=34), T(1, 'input length n  =>  n + 1 outputs', size=34))
beat(p, '''In a Mealy machine, the output depends on the state and the current input, so the output is written on the transitions. For an input of length n, it gives n outputs.
Every Moore machine can be converted to a Mealy machine and back, so they are equivalent.''',
     T(3, '[h:Mealy]: output depends on [r:state + input];   λ : Q × Σ -> Δ', size=34), T(4, 'input length n  =>  n outputs', size=34))
beat(p, '''Here is the comparison.''',
     Stamp(1650, 140, 'MOST ASKED'),
     Tab(180, 470, [360, 560, 560], 56, [['', 'Moore', 'Mealy'], ['output depends on', 'present state only', 'present state + input'], ['output written', 'inside the state', 'on the transition'],
         ['outputs for n inputs', 'n + 1', 'n'], ['number of states', 'usually more', 'usually fewer'], ['reaction to input', 'one step later', 'immediate']], size=28,
         colors={(r, 0): 'red' for r in range(1, 6)}))

# ===================================================================================== CH 5
p = chapter(5)
beat(p, "Chapter five. Regular expressions, and Arden's theorem.")

p = page('Regular Expressions & Identities', 5)
beat(p, '''A regular expression describes a regular language using three operators: union, written plus, concatenation, and the Kleene star. The basic expressions are phi,
epsilon, and single symbols. For example, a plus b, star, a b b means any string that ends with a b b.''',
     T(0, '[h:RE operators]: + (union), concatenation, * (star);   base: ∅, ε, a'),
     T(1, 'Precedence: * > concatenation > +', color='red'), T(2, '(a + b)*abb = strings ending with abb', color='green'))
beat(p, '''Some common examples. All strings of a and b: a plus b star. Strings with at least one a: a plus b star, a, a plus b star.
Strings of even length: open bracket a plus b, a plus b, close bracket, star. Strings that start and end with the same symbol: a, a plus b star, a, plus b, a plus b star, b, plus a, plus b.''',
     Stamp(1650, 140),
     Tab(180, 380, [660, 660], 52, [['Language', 'Regular expression'], ['all strings', '(a + b)*'], ['at least one a', '(a + b)* a (a + b)*'], ['even length', '((a + b)(a + b))*'],
         ['no two consecutive a', '(b + ab)* (ε + a)'], ['start & end with same symbol', 'a(a+b)*a + b(a+b)*b + a + b']], size=28))
beat(p, '''Identities you must remember: phi plus R is R. phi R is phi. epsilon R is R. epsilon star is epsilon, and phi star is epsilon.
R plus R is R. R star R star is R star. R R star is R plus. And a plus b star equals a star b star, star.''',
     T(10, '∅ + R = R   ∅R = ∅   εR = R   ε* = ε   ∅* = ε', size=34, color='black'), T(11, 'R + R = R   R*R* = R*   RR* = R+   (R*)* = R*', size=34, color='black'),
     T(12, '(a + b)* = (a*b*)* = (a* + b*)*', size=34, color='red'))

p = page('RE to Finite Automata', 5)
beat(p, '''To convert a regular expression to an automaton, we use Thompson's construction, which builds an epsilon N F A from small pieces.
For a single symbol a, two states with an a move.''',
     T(0, "[h:Thompson's construction]: RE -> ε-NFA, piece by piece"), S(1, 'a', size=36, color='red'),
     *State((480, 300), 'i'), *State((780, 300), 'f', final=True), Edge((480, 300), (780, 300), 'a'))
beat(p, '''For union, R plus S, add a new start state with epsilon moves to both machines, and epsilon moves from both to a new final state.
For concatenation, R S, connect the final state of R to the start of S with an epsilon move.''',
     S(4, 'R + S', size=36, color='red'),
     *State((300, 600), 'i'), Box(470, 470, 200, 80, 'R', size=30, color='blue'), Box(470, 650, 200, 80, 'S', size=30, color='blue'), *State((860, 600), 'f', final=True),
     Arr(330, 570, 470, 515, label='ε', size=26), Arr(330, 630, 470, 690, label='ε', ly=30, size=26), Arr(670, 510, 820, 570, label='ε', size=26), Arr(670, 690, 820, 630, label='ε', ly=30, size=26),
     S(4, 'RS', x=1150, size=36, color='red'), Box(1150, 560, 200, 80, 'R', size=30, color='blue'), Box(1460, 560, 200, 80, 'S', size=30, color='blue'),
     Arr(1350, 600, 1460, 600, label='ε', size=26))
beat(p, '''For the star, R star, add a new start and final state. Add epsilon moves to enter R, to skip it completely, and to go back from the end of R to its start, to repeat it.''',
     S(9, 'R*', x=1150, size=36, color='red'), *State((1260, 860), 'i'), Box(1440, 820, 200, 80, 'R', size=30, color='blue'), *State((1820, 860), 'f', final=True),
     Arr(1302, 860, 1440, 860, label='ε', size=26), Arr(1640, 860, 1778, 860, label='ε', size=26), Arr(1260, 902, 1820, 902, curve=120, label='ε (skip)', ly=30, size=24),
     Arr(1620, 820, 1460, 820, curve=80, label='ε (repeat)', size=24))

p = page("FA to RE: Arden's Theorem", 5)
beat(p, '''To convert a finite automaton to a regular expression, we use Arden's theorem. It says: if R equals Q plus R P, and P does not contain epsilon,
then R equals Q P star. We write one equation for each state, showing how we can enter it, and add epsilon for the start state.''',
     Stamp(1650, 140, 'NUMERICAL'), T(0, "[h:Arden]: R = Q + RP  (ε ∉ P)  =>  [r:R = QP*]", size=40),
     T(1, 'Write an equation for each state: incoming moves (+ ε for start)', size=34))
pa = {'q1': (1220, 520), 'q2': (1620, 520)}
beat(p, '''Example. q one is the start state and q two is final. q one loops on a, q two loops on a, and b moves between them both ways.
So q one equals epsilon, plus q one a, plus q two b. And q two equals q one b, plus q two a.''',
     *State(pa['q1'], 'q1', start=True), *State(pa['q2'], 'q2', final=True), Loop(pa['q1'], 'a'), Loop(pa['q2'], 'a'),
     Edge(pa['q1'], pa['q2'], 'b', curve=-70), Edge(pa['q2'], pa['q1'], 'b', curve=-70),
     T(3, 'q1 = ε + q1 a + q2 b', color='black'), T(4, 'q2 = q1 b + q2 a', color='black'))
beat(p, '''Apply Arden to q two: q two equals q one b, a star. Put this in the first equation: q one equals epsilon plus q one, open bracket a plus b a star b. By Arden, q one equals a plus b a star b, star.
So q two equals a plus b a star b, star, b a star. Since q two is final, that is the answer. It means all strings with an odd number of b's.''',
     T(6, 'q2 = q1 b a*        (Arden on q2)'), T(7, 'q1 = ε + q1 (a + b a* b)  =>  q1 = (a + ba*b)*'),
     T(8, 'q2 = (a + ba*b)* b a*'), T(10, 'RE = [h:(a + ba*b)* ba*]   = odd number of b\'s' + ('  ✓' if arden_ok() else ''), color='red', size=40))

p = page('Regular Grammar & Finite Automata', 5)
beat(p, '''Regular grammars are type three grammars. In a right linear grammar, every production looks like A goes to a B, or A goes to a. A left linear grammar has the variable on the left, like A goes to B a.
Both generate exactly the regular languages.''',
     T(0, '[h:Right linear]: A -> aB | a      [h:Left linear]: A -> Ba | a', size=36), T(1, 'both generate exactly the regular languages', size=34))
beat(p, '''Converting a D F A to a right linear grammar is easy. Each state becomes a variable. For every move from A to B on a, write A goes to a B. And for every final state, add a production to epsilon.
For our D F A for strings ending with a b, we get this grammar.''',
     Stamp(1650, 140), T(3, 'δ(A, a) = B   =>   A -> aB;     final state F   =>   F -> ε', size=34, color='red'),
     T(5, 'q0 -> a q1 | b q0', color='black'), T(6, 'q1 -> a q1 | b q2', color='black'), T(7, 'q2 -> a q1 | b q0 | ε', color='black'),
     T(8, '(DFA for strings ending with ab)', size=30, color='green'))
beat(p, '''To go the other way, from a right linear grammar to a finite automaton, just reverse the steps. Variables become states, and each production becomes a move.''',
     T(10, 'Grammar -> FA: variables = states, A -> aB = move from A to B on a', size=32))

# ===================================================================================== CH 6
p = chapter(6)
beat(p, 'Chapter six. Properties of regular languages. The pumping lemma is asked in almost every exam.')

p = page('Pumping Lemma for Regular Languages', 6)
beat(p, '''The pumping lemma is used to prove that a language is not regular. It says: if L is regular, there is a number n, the pumping length,
such that every string w in L with length at least n can be split as x y z, where the length of x y is at most n, y is not empty,
and x y to the power i z is in L for every i greater than or equal to zero.''',
     Stamp(1650, 140, 'MOST ASKED'), T(0, 'L regular  =>  ∃ n: every w ∈ L, |w| ≥ n, w = xyz with', size=36),
     T(1, '[r:|xy| ≤ n],   [r:|y| ≥ 1],   [r:x y^i z ∈ L for all i ≥ 0]', size=36))
beat(p, '''We use it by contradiction. Let's prove that a to the power n, b to the power n is not regular. Assume it is regular, with pumping length n.
Take w equals a to the n, b to the n. Since x y has length at most n, y contains only a's. Say y is a to the k, with k at least one.''',
     S(3, 'Prove L = {a^n b^n | n ≥ 0} is not regular', size=36, color='red'), N(4, 1, 'Assume L is regular, pumping length n', size=34),
     N(5, 2, 'w = a^n b^n;  |xy| ≤ n  =>  y = a^k,  k ≥ 1', size=34))
beat(p, '''Now pump with i equals two. x y y z has n plus k a's but only n b's. So it is not in L. This is a contradiction, so a to the n b to the n is not regular.
A finite automaton cannot count without limit.''',
     N(6, 3, 'i = 2:  x y² z = a^(n+k) b^n  ∉ L', size=34), N(7, 4, '[r:Contradiction]  =>  L is not regular', size=34),
     Box(1080, 690, 300, 70, 'a a a ... a', size=28, color='blue'), Box(1380, 690, 280, 70, 'b b b ... b', size=28, color='green'),
     T(0, 'x', x=1110, y=800, size=30, color='red'), T(0, 'y (pump)', x=1210, y=800, size=30, color='red'), T(0, 'z', x=1500, y=800, size=30, color='red'),
     T(13, 'Not regular: a^n b^n, ww, palindromes, a^(n²), a^p (p prime), equal a\'s and b\'s', size=30, color='green'))

p = page('Closure & Decision Properties of Regular Languages', 6)
beat(p, '''Regular languages are closed under almost every operation. If L one and L two are regular, then their union, intersection, complement, difference,
concatenation, Kleene star, reverse, homomorphism and inverse homomorphism are all regular.''',
     Stamp(1650, 140), T(0, '[h:Closed under]: ∪, ∩, complement, difference, concatenation, *,', size=34), T(1, 'reverse, homomorphism, inverse homomorphism, quotient', size=34, x=330))
beat(p, '''Watch out for GATE traps. A finite union of regular languages is regular, but an infinite union may not be. A subset of a regular language may not be regular:
a to the n b to the n is a subset of a star b star, which is regular. Every finite language is regular.''',
     T(3, '[r:Traps]: infinite union may not be regular', size=34), T(4, 'subset of regular may not be regular:  a^n b^n ⊆ a*b*', size=34),
     T(5, 'every [g:finite] language is regular', size=34))
beat(p, '''Decision properties: for regular languages, membership, emptiness, finiteness, and equivalence of two automata are all decidable. Emptiness is checked by seeing
if any final state is reachable. Finiteness is checked by looking for a cycle on a path from the start to a final state.''',
     T(7, '[h:Decidable]: membership, emptiness, finiteness, equivalence', size=34), T(8, 'empty: no final state reachable;  infinite: a useful cycle', size=34))
beat(p, '''The Myhill Nerode theorem says a language is regular if and only if it has a finite number of equivalence classes. That number is exactly the number of states
in the minimal D F A.''',
     T(10, '[k:Myhill-Nerode]: L regular <=> finitely many equivalence classes', size=34), T(11, '#classes = #states of the minimal DFA', size=34, color='green'))

# ===================================================================================== CH 7
p = chapter(7)
beat(p, 'Chapter seven. Context free grammars.')

p = page('Context-Free Grammar & Derivations', 7)
beat(p, '''A context free grammar is a four tuple: V, T, P, S. V is the set of variables, or non terminals. T is the set of terminals. P is the set of productions,
where the left side is a single variable. And S is the start symbol. For example, S goes to a S b, or epsilon, generates a to the n b to the n, which is not regular.''',
     T(0, 'G = (V, T, P, S);   production: A -> α  (A is one variable)', color='black'), T(1, 'S -> aSb | ε   generates  {a^n b^n | n ≥ 0}', color='red'))
beat(p, '''A derivation replaces variables step by step. In a leftmost derivation, we always replace the leftmost variable. In a rightmost derivation, the rightmost one.
For the grammar E goes to E plus E, E times E, or id, the leftmost derivation of id plus id times id is shown here.''',
     T(3, '[k:Leftmost]: replace leftmost variable    [k:Rightmost]: rightmost'), T(4, 'E -> E + E | E * E | id', color='black'),
     T(5, 'E => E + E => id + E => id + E * E => id + id * E => id + id * id', size=32))
beat(p, '''A parse tree shows a derivation as a tree. The root is the start symbol, the inside nodes are variables, and the leaves, read from left to right, form the string, called the yield.''',
     T(7, '[h:Parse tree]: root = start symbol'), T(8, 'leaves (left to right) = the string (yield)'),
     Ell(1180, 560, 80, 60, 'E', size=28), Ell(1040, 660, 80, 60, 'E', size=28), Ell(1190, 660, 60, 60, '+', size=28), Ell(1320, 660, 80, 60, 'E', size=28),
     Ell(1040, 760, 80, 60, 'id', size=26, color='green'), Ell(1230, 760, 80, 60, 'E', size=26), Ell(1330, 760, 60, 60, '*', size=26), Ell(1420, 760, 80, 60, 'E', size=26),
     Ell(1230, 860, 80, 60, 'id', size=26, color='green'), Ell(1420, 860, 80, 60, 'id', size=26, color='green'),
     Ln([(1205, 616), (1090, 660)], 'black', 3), Ln([(1220, 620), (1220, 660)], 'black', 3), Ln([(1235, 616), (1350, 660)], 'black', 3),
     Ln([(1080, 720), (1080, 760)], 'black', 3), Ln([(1345, 718), (1275, 760)], 'black', 3), Ln([(1360, 720), (1360, 760)], 'black', 3),
     Ln([(1375, 718), (1450, 760)], 'black', 3), Ln([(1270, 820), (1270, 860)], 'black', 3), Ln([(1460, 820), (1460, 860)], 'black', 3))

p = page('Ambiguous Grammar', 7)
beat(p, '''A grammar is ambiguous if some string has two or more different parse trees, or two leftmost derivations. The expression grammar is ambiguous,
because id plus id times id can be grouped as id plus, id times id, or as id plus id, times id.''',
     T(0, '[h:Ambiguous]: a string has ≥ 2 parse trees (or 2 leftmost derivations)'), T(1, 'E -> E + E | E * E | id:   id + (id * id)   and   (id + id) * id', size=34))
beat(p, '''We remove ambiguity by adding precedence and associativity: E goes to E plus T or T, T goes to T times F or F, F goes to id.
Some languages are inherently ambiguous, which means every grammar for them is ambiguous. For example, a to the i b to the j c to the k, where i equals j or j equals k.''',
     T(3, 'Unambiguous: E -> E + T | T,  T -> T * F | F,  F -> id', color='black', size=34),
     T(4, '[r:Inherently ambiguous]: { a^i b^j c^k | i = j or j = k }', size=34))
beat(p, '''Remember for GATE: checking whether any given context free grammar is ambiguous is undecidable. There is no algorithm that works for every grammar.''',
     Stamp(1650, 140, 'GATE'), T(6, 'Is a CFG ambiguous?  =>  [r:undecidable]', size=38))

p = page('Simplifying a CFG', 7)
beat(p, '''Before converting to a normal form, we simplify the grammar in three steps. First, remove null productions, that is, productions to epsilon. Second, remove unit productions,
like A goes to B. And third, remove useless symbols, which are never reached from S or never produce a terminal string.''',
     Stamp(1650, 140, 'NUMERICAL'), N(0, 1, 'remove [r:ε-productions]', size=34), N(1, 2, 'remove [r:unit productions] (A -> B)', size=34),
     N(2, 3, 'remove [r:useless symbols] (unreachable / non-generating)', size=34))
beat(p, '''Example of null removal. S goes to A B A, A goes to a A or epsilon, B goes to b B or epsilon. A and B are nullable, so S is nullable too.
For each production, add every version with the nullable symbols left out. From A B A we get A B A, A B, B A, A A, A and B. A goes to a A or a. B goes to b B or b.''',
     T(4, 'S -> ABA,  A -> aA | ε,  B -> bB | ε', color='black'), T(5, 'Nullable: A, B, S'),
     T(6, 'S -> ABA | AB | BA | AA | A | B', color='red'), T(7, 'A -> aA | a       B -> bB | b', color='red'))
beat(p, '''Example of unit removal. S goes to A or b b, A goes to B or b, and B goes to S or a. Through unit chains, S, A and B can all reach each other.
So each gets all the non unit productions: a, b and b b.''',
     T(9, 'S -> A | bb,   A -> B | b,   B -> S | a', color='black'), T(10, 'unit pairs: S, A, B all reach each other'),
     T(11, 'S -> a | b | bb     A -> a | b | bb     B -> a | b | bb', color='red'))

p = page('Chomsky & Greibach Normal Forms', 7)
beat(p, '''In Chomsky normal form, or C N F, every production is either A goes to B C, two variables, or A goes to a, a single terminal. To convert, first simplify the grammar.
Then replace terminals in long productions with new variables, and break long right sides into pairs.''',
     Stamp(1650, 140, 'MOST ASKED'), T(0, '[h:CNF]: A -> BC  or  A -> a', size=40), T(1, 'simplify -> replace terminals -> break into pairs', size=34))
beat(p, '''Example. S goes to a S b, or a b. Add A goes to a, and B goes to b. Then S goes to A S B, or A B. A S B has three variables, so add C goes to S B.
The C N F is: S goes to A C or A B, C goes to S B, A goes to a, and B goes to b.''',
     T(3, 'S -> aSb | ab', color='black'), T(4, 'A -> a,  B -> b   =>   S -> ASB | AB'), T(5, 'C -> SB          =>   S -> AC | AB'),
     T(6, 'CNF:  S -> AC | AB,   C -> SB,   A -> a,   B -> b', color='red', size=40))
beat(p, '''In C N F, a string of length n always takes exactly two n minus one steps to derive, and its parse tree is a binary tree.
In Greibach normal form, G N F, every production is A goes to a, followed by zero or more variables. A string of length n then takes exactly n steps.''',
     T(8, 'CNF: |w| = n  =>  [h:2n - 1] derivation steps', size=36, color='green'), T(10, '[h:GNF]: A -> a α   (α = string of variables)', size=40),
     T(11, 'GNF: |w| = n  =>  [h:n] derivation steps', size=36, color='green'))

# ===================================================================================== CH 8
p = chapter(8)
beat(p, 'Chapter eight. The C Y K algorithm, and properties of context free languages.')

V = cyk('baaba'); w = 'baaba'; n = 5
def cell(i, j): s = sorted(V[(i, j)]); return '{' + ', '.join(s) + '}' if s else '∅'
cy_rows = [[f'len {Lx}'] + [cell(i, i + Lx - 1) if i + Lx - 1 < n else '' for i in range(n)] for Lx in range(n, 0, -1)] + [[''] + list(w)]
p = page('CYK Algorithm', 8)
beat(p, '''The C Y K algorithm checks if a string belongs to a context free grammar. The grammar must be in Chomsky normal form. It uses dynamic programming,
filling a triangular table from short substrings to the whole string. It takes order n cube time.''',
     Stamp(1650, 140, 'NUMERICAL'), T(0, '[h:CYK]: membership test, grammar in CNF, dynamic programming, O(n³)', size=34),
     T(1, 'S -> AB | BC   A -> BA | a   B -> CC | b   C -> AB | a', size=34, color='black'), T(2, 'w = baaba', size=34, color='black'))
beat(p, '''Step one, single symbols. b comes from B. a comes from A and C. Step two, length two. For b a, we combine B with A or C. B A gives A, and B C gives S. So the cell is A and S.
We continue for longer substrings, trying every way to split them into two parts.''',
     Tab(240, 390, [150] + [210] * 5, 60, cy_rows, size=28, hdr=False, colors={(0, 1): 'red', **{(5, c): 'black' for c in range(1, 6)}}))
beat(p, '''The top cell, for the whole string, contains S. So b a a b a is generated by the grammar, and it is accepted.''',
     T(14, 'S ∈ top cell  =>  "baaba" is [h:accepted]', size=36, color='red'))

p = page('Pumping Lemma for CFLs & Closure Properties', 8)
beat(p, '''The pumping lemma for context free languages: every long string w can be split into five parts, u v x y z, where the length of v x y is at most n,
v y is not empty, and u v to the i, x, y to the i, z is in L for every i. Using it, we can prove that a to the n b to the n c to the n is not context free.''',
     T(0, 'w = uvxyz,  |vxy| ≤ n,  |vy| ≥ 1,  u v^i x y^i z ∈ L  ∀ i ≥ 0', size=34), T(1, 'Not CFL: a^n b^n c^n,  ww,  a^(n²),  a^p (p prime)', size=34, color='red'))
beat(p, '''Closure properties. Context free languages are closed under union, concatenation, Kleene star, reverse and homomorphism.
But they are not closed under intersection and complement. For example, a to the n b to the n c to the m and a to the m b to the n c to the n are both context free,
but their intersection, a to the n b to the n c to the n, is not.''',
     Stamp(1650, 140, 'GATE'), T(3, '[g:Closed]: ∪, concatenation, *, reverse, homomorphism', size=34), T(4, '[r:Not closed]: ∩, complement', size=34),
     T(5, 'a^n b^n c^m ∩ a^m b^n c^n = a^n b^n c^n  (not CFL)', size=34, color='black'))
beat(p, '''Two useful facts. The intersection of a context free language and a regular language is always context free. And deterministic context free languages
are closed under complement, but not under union or intersection.''',
     T(7, 'CFL ∩ Regular = [h:CFL]', size=36, color='red'), T(8, 'DCFL: closed under complement; not under ∪, ∩', size=34))

# ===================================================================================== CH 9
p = chapter(9)
beat(p, 'Chapter nine. Pushdown automata.')

p = page('Pushdown Automata', 9)
beat(p, '''A pushdown automaton, or P D A, is a finite automaton with a stack. The stack gives it unlimited memory, but it can only use the top of the stack.
That is why it can accept context free languages like a to the n b to the n.''',
     T(0, '[h:PDA] = finite automaton + [r:stack] (last in, first out)'), T(1, 'accepts exactly the context-free languages'),
     Box(1300, 360, 400, 70, 'a  a  b  b  ...', size=28), T(0, 'input tape', x=1720, y=405, size=26), Box(1360, 520, 280, 110, 'Finite\ncontrol', size=28, color='blue'),
     Arr(1420, 520, 1360, 432, color='red'), Box(1380, 700, 120, 60, 'a', size=28), Box(1380, 760, 120, 60, 'a', size=28), Box(1380, 820, 120, 60, 'Z0', size=28),
     T(0, 'stack', x=1520, y=780, size=26), Arr(1500, 630, 1460, 700, color='red'))
beat(p, '''A P D A is a seven tuple: Q, sigma, gamma, delta, q zero, Z zero, and F. Gamma is the stack alphabet, and Z zero is the initial stack symbol.
The transition function delta takes the state, an input symbol or epsilon, and the top of the stack, and gives a new state and a string to replace the top.''',
     Stamp(1650, 140), T(3, 'M = (Q, Σ, Γ, δ, q0, Z0, F)', color='black', size=40), T(4, 'Γ = stack alphabet,  Z0 = initial stack symbol', size=34),
     T(5, 'δ(q, a, X) = (p, γ):  read a, pop X, push γ', size=34))
beat(p, '''A P D A can accept in two ways: by final state, or by empty stack. Both are equivalent for non deterministic P D As.''',
     T(7, 'Acceptance: by [k:final state]  or  by [k:empty stack]  (equivalent)', size=34))

ids, ok = pda_anbn('aabb')
p = page('PDA for a^n b^n', 9)
beat(p, '''Let's design a P D A for a to the n b to the n, with n at least one. The idea: push every a onto the stack. Then for each b, pop one a.
If the stack is back to Z zero when the input ends, the counts were equal, so we accept.''',
     Stamp(1650, 140, 'NUMERICAL'), T(0, 'Idea: push each a;  pop one a for each b;  accept when only Z0 is left', size=34))
beat(p, '''The transitions are: in q zero, on a with Z zero on top, push a. On a with a on top, push another a. On b with a on top, pop it and go to q one.
In q one, on b with a on top, pop. And on epsilon with Z zero on top, go to the final state q f.''',
     T(2, 'δ(q0, a, Z0) = (q0, aZ0)       δ(q0, a, a) = (q0, aa)', size=34, color='black'), T(3, 'δ(q0, b, a) = (q1, ε)          δ(q1, b, a) = (q1, ε)', size=34, color='black'),
     T(4, 'δ(q1, ε, Z0) = (qf, Z0)', size=34, color='black'))
beat(p, '''Now the moves on a a b b, written as instantaneous descriptions: the state, the remaining input, and the stack. We push two a's, pop two a's, and reach q f. So a a b b is accepted.''',
     Tab(180, 520, [200, 260, 260, 420], 50, [['step', 'state', 'input', 'stack (top first)']] + [[str(k), q, i, st] for k, (q, i, st) in enumerate(ids)], size=28,
         colors={(len(ids), 1): 'green'}),
     T(0, '[g:accepted ✓]', x=1360, y=860, size=36))

p = page('DPDA vs NPDA & CFG to PDA', 9)
beat(p, '''A deterministic P D A has at most one move in every situation. Non deterministic P D As are more powerful than deterministic ones. For example, even length palindromes,
w w reverse, need a non deterministic P D A, because the machine must guess where the middle is. But w c w reverse, with a marker c in the middle, can be done by a D P D A.''',
     Stamp(1650, 140, 'MOST ASKED'), T(0, '[h:NPDA > DPDA]  (unlike DFA = NFA)', size=38, color='red'), T(1, 'ww^R needs NPDA (guess the middle);   wcw^R: DPDA is enough', size=34))
beat(p, '''So the power of machines: D F A equals N F A, but D P D A is less than N P D A. For Turing machines, deterministic and non deterministic are equal again.''',
     Tab(180, 380, [420, 520, 360], 56, [['Machine', 'Deterministic vs non-det.', 'Language'], ['Finite automata', 'DFA = NFA', 'regular'],
         ['Pushdown automata', '[r:DPDA < NPDA]', 'DCFL ⊂ CFL'], ['Turing machine', 'DTM = NTM', 'RE']], size=28))
beat(p, '''Every context free grammar can be converted to a P D A, and every P D A to a context free grammar. Deterministic context free languages are never inherently ambiguous,
which is why they are used to build parsers for programming languages.''',
     T(10, 'CFG <=> PDA (always convertible)', size=36, color='green'), T(11, 'DCFLs have unambiguous grammars (used in parsers: LR(k))', size=34))

cids, cok = cfg_pda('aabb', [0, 1])
p = page('CFG to PDA Conversion', 9)
beat(p, '''A common exam question: convert a C F G to a P D A. We use a P D A with just one state, which accepts by empty stack. Start with S on the stack.
For every production A goes to alpha, add a move that pops A and pushes alpha, without reading input. And for every terminal a, add a move that reads a and pops a.''',
     Stamp(1650, 140, 'NUMERICAL'), T(0, 'one state q, accept by empty stack, start with S on the stack', size=34),
     T(1, 'A -> α   =>   δ(q, ε, A) = (q, α)', size=36, color='red'), T(2, 'terminal a   =>   δ(q, a, a) = (q, ε)', size=36, color='red'))
beat(p, '''Example: S goes to a S b, or a b. The moves are: on epsilon with S on top, replace S with a S b, or with a b. On a with a on top, pop. And on b with b on top, pop.''',
     T(4, 'S -> aSb | ab', color='black'), T(5, 'δ(q, ε, S) = { (q, aSb), (q, ab) }', size=34), T(6, 'δ(q, a, a) = (q, ε)      δ(q, b, b) = (q, ε)', size=34))
beat(p, '''Let's run it on a a b b. Replace S with a S b, match a, replace S with a b, then match a, b, and b. The input is finished and the stack is empty, so the string is accepted.
Notice that the P D A simply follows a leftmost derivation.''',
     Tab(1080, 520, [80, 260, 260], 48, [['#', 'input', 'stack']] + [[str(k), i, st] for k, (i, st) in enumerate(cids)], size=26),
     T(9, 'PDA follows the leftmost derivation', size=32, color='green'), T(10, '[g:empty stack => accepted ✓]', size=34))

# ===================================================================================== CH 10
p = chapter(10)
beat(p, 'Chapter ten. Turing machines, the most powerful model of computation.')

p = page('Turing Machine', 10)
beat(p, '''A Turing machine has a finite control and an infinite tape divided into cells. The head can read and write a symbol, and move left or right.
Unlike a P D A, it can go back and change the input. The Church Turing thesis says that anything that can be computed by an algorithm can be computed by a Turing machine.''',
     T(0, '[h:TM]: finite control + infinite tape;  read, write, move L / R'), T(1, '[k:Church-Turing thesis]: algorithm = Turing machine', color='red'),
     *[Box(1060 + 80 * k, 400, 80, 70, c, size=28) for k, c in enumerate(['a', 'a', 'b', 'b', 'B', 'B', 'B', 'B'])], T(0, '...', x=1710, y=445, size=32),
     Box(1150, 560, 220, 90, 'Control', size=28, color='blue'), Arr(1220, 560, 1180, 472, color='red'), T(0, 'head', x=1090, y=525, size=26, color='red'))
beat(p, '''A Turing machine is a seven tuple: Q, sigma, gamma, delta, q zero, B, and F. Gamma is the tape alphabet, and B is the blank symbol.
Delta of q and X gives a new state, a symbol to write, and a direction, left or right.''',
     Stamp(1650, 140), T(4, 'M = (Q, Σ, Γ, δ, q0, B, F)', color='black', size=40), T(5, 'δ(q, X) = (p, Y, L / R):  write Y, move left or right', size=34),
     T(6, 'B = blank symbol;  Σ ⊂ Γ', size=34))
beat(p, '''A Turing machine can accept, reject, or run forever. The languages it accepts are recursively enumerable. If it always halts, the language is recursive, or decidable.''',
     T(8, 'halts & accepts  ·  halts & rejects  ·  [r:loops forever]', size=34), T(9, '[k:Recursive (decidable)]: TM always halts', size=34),
     T(10, '[k:Recursively enumerable]: TM halts on every string in L', size=34))

ids, ok = run_tm('aabb')
p = page('TM for a^n b^n', 10)
beat(p, '''Let's design a Turing machine for a to the n b to the n. The idea: mark the first a as X, go right to the first b and mark it as Y, then come back to the next a.
Repeat. When no a's are left, check that only Y's remain.''',
     Stamp(1650, 140, 'NUMERICAL'), T(0, 'Idea: a -> X, find b -> Y, come back; repeat; then only Y\'s left', size=34))
beat(p, '''Here is the transition table. q zero marks an a as X. q one moves right to find a b. q two moves back left to the X. And q three checks that only Y's are left, then accepts in q four.''',
     Tab(180, 330, [130, 220, 220, 220, 220, 220], 54, [['', 'a', 'b', 'X', 'Y', 'B'], ['-> q0', '(q1, X, R)', '', '', '(q3, Y, R)', ''],
         ['q1', '(q1, a, R)', '(q2, Y, L)', '', '(q1, Y, R)', ''], ['q2', '(q2, a, L)', '', '(q0, X, R)', '(q2, Y, L)', ''], ['q3', '', '', '', '(q3, Y, R)', '(q4, B, R)'],
         ['* q4', '', '', '', '', '']], size=26))
half = (len(ids) + 1) // 2
beat(p, f'''Now run it on a a b b. The instantaneous description shows the tape with the state written just before the head. After {len(ids) - 1} moves, the machine reaches q four, so a a b b is accepted.''',
     Tab(180, 700, [230] * half, 44, [ids[:half], ids[half:] + [''] * (2 * half - len(ids))], size=24, hdr=False, colors={(1, len(ids) - half - 1): 'green'}),
     T(14, 'ID: tape with the state written before the head symbol', size=30, color='green'))

p = page('TM Variants, LBA & Chomsky Hierarchy', 10)
beat(p, '''Variants of Turing machines, like multi tape, multi track, two way infinite tape, and non deterministic Turing machines, all have the same power as the basic Turing machine.
They may be faster, but they accept the same languages. A universal Turing machine can simulate any other Turing machine, given its description.''',
     T(0, 'multi-tape, multi-track, two-way tape, [k:non-deterministic] TM', size=34), T(1, '=> [h:same power] as the basic TM', size=34),
     T(2, '[k:Universal TM]: simulates any TM from its description', size=34))
beat(p, '''A linear bounded automaton, or L B A, is a non deterministic Turing machine whose tape is limited to the length of the input. L B As accept the context sensitive languages.''',
     T(4, '[h:LBA] = TM with tape limited to input length  ->  context-sensitive languages', size=32))
beat(p, '''Here is the complete Chomsky hierarchy in one table. Remember: each machine is more powerful than the one above it.''',
     Stamp(1650, 140, 'MOST ASKED'),
     Tab(180, 460, [140, 360, 400, 400, 300], 56, [['Type', 'Language', 'Grammar', 'Machine', 'Example'], ['3', 'Regular', 'A -> aB | a', 'finite automata', 'a*b*'],
         ['2', 'Context-free', 'A -> α', 'pushdown automata', 'a^n b^n'], ['1', 'Context-sensitive', '|α| ≤ |β|', 'linear bounded automata', 'a^n b^n c^n'],
         ['0', 'Recursively enumerable', 'unrestricted', 'Turing machine', 'halting problem']], size=28, colors={(r, 3): 'red' for r in range(1, 5)}))

# ===================================================================================== CH 11
p = chapter(11)
beat(p, 'Chapter eleven. Decidability and complexity. These are pure theory questions, and GATE asks them every year.')

p = page('Decidability & The Halting Problem', 11)
beat(p, '''A problem is decidable if some Turing machine always halts and gives the correct yes or no answer. Recursive languages are decidable.
Recursively enumerable languages are semi decidable: the machine says yes for strings in the language, but may loop forever for others.''',
     T(0, '[h:Decidable] = TM always halts with yes / no  (recursive)', size=34), T(1, '[h:Semi-decidable] = halts on yes, may loop on no  (RE)', size=34))
beat(p, '''The halting problem asks: given a Turing machine M and an input w, does M halt on w? Alan Turing proved this is undecidable. The idea: suppose a machine H solves it.
Build a machine D that runs H on itself, and does the opposite: if H says D halts, D loops, and if H says D loops, D halts. This is a contradiction, so H cannot exist.''',
     Stamp(1650, 140, 'MOST ASKED'), T(3, '[r:Halting problem]: does M halt on w?  =>  undecidable (but RE)', size=34),
     Box(300, 520, 260, 90, 'H(M, w)', size=30, color='blue'), Arr(560, 545, 760, 500, label='halts', size=24), Arr(560, 585, 760, 640, label='loops', ly=30, size=24),
     Box(760, 460, 330, 70, 'D loops forever', size=26, color='red'), Box(760, 610, 330, 70, 'D halts', size=26, color='red'),
     T(0, 'D runs H on itself and does the opposite  =>  contradiction', x=300, y=740, size=30, color='red'))
beat(p, '''Important results. If a language and its complement are both recursively enumerable, then the language is recursive. The complement of the halting problem is not even recursively enumerable.''',
     T(11, 'L and complement(L) both RE  =>  L is [h:recursive]', size=34), T(12, 'complement of halting problem: [r:not RE]', size=34))

pc = pcp_check([2, 1, 3, 2, 4])
p = page("Reductions, Rice's Theorem & PCP", 11)
beat(p, '''To prove a new problem is undecidable, we reduce a known undecidable problem to it. If A reduces to B, and A is undecidable, then B is undecidable too.''',
     T(0, '[h:Reduction]: A ≤ B and A undecidable  =>  B undecidable', size=36))
beat(p, '''Rice's theorem says: every non trivial property of the language of a Turing machine is undecidable. Non trivial means some machines have the property and some do not.
So questions like "is the language of M empty?", "is it finite?", or "is it regular?" are all undecidable.''',
     Stamp(1650, 140), T(2, "[h:Rice's theorem]: every non-trivial property of L(M) is undecidable", size=34),
     T(3, 'e.g. is L(M) empty? finite? regular? = Σ*?  =>  all undecidable', size=34))
beat(p, f'''The Post correspondence problem, P C P, gives a set of dominoes, each with a top and a bottom string. The question: is there a sequence where the top and bottom strings match?
P C P is undecidable in general. For this instance, the sequence two, one, three, two, four works: both the top and the bottom read a b c a a a b c.''',
     T(5, '[k:PCP]: find dominoes whose top string = bottom string  =>  [r:undecidable]', size=34),
     Tab(180, 530, [140, 140, 140, 140, 140], 54, [['#', '1', '2', '3', '4'], ['top', *PCP_T], ['bottom', *PCP_B]], size=30),
     T(0, f'Sequence 2, 1, 3, 2, 4:', x=1000, y=L(6), size=32), T(0, f'top    = {pc[0]}', x=1000, y=L(7), size=32, color='black'),
     T(0, f'bottom = {pc[1]}  [g:✓ match]', x=1000, y=L(8), size=32, color='black'))

Y_, N_ = '[g:Y]', '[r:N]'
p = page('Closure Properties: GATE Table', 11)
beat(p, '''Now the closure table for all language classes. Y means closed, N means not closed. Regular languages are closed under everything.
Context free languages are not closed under intersection and complement. Deterministic context free languages are closed under complement, but not under union, intersection or concatenation.''',
     Stamp(1650, 140, 'GATE'),
     Tab(180, 230, [240, 150, 150, 180, 160, 140, 160, 190, 180], 58, [['Class', '∪', '∩', 'compl.', 'concat', 'star', 'reverse', 'homom.', '∩ Reg'],
         ['Regular', Y_, Y_, Y_, Y_, Y_, Y_, Y_, Y_], ['DCFL', N_, N_, Y_, N_, N_, N_, N_, Y_], ['CFL', Y_, N_, N_, Y_, Y_, Y_, Y_, Y_],
         ['CSL', Y_, Y_, Y_, Y_, Y_, Y_, N_, Y_], ['Recursive', Y_, Y_, Y_, Y_, Y_, Y_, N_, Y_], ['RE', Y_, Y_, N_, Y_, Y_, Y_, Y_, Y_]], size=28))
beat(p, '''Context sensitive and recursive languages are closed under complement, but not under general homomorphism. Recursively enumerable languages are closed under union and intersection,
but not under complement. And every class is closed under intersection with a regular language.''',
     T(10, 'complement: [g:REG, DCFL, CSL, REC]  ·  [r:not CFL, not RE]', size=32), T(11, 'homomorphism: [r:not CSL, not REC]  (ε-free homomorphism is fine)', size=32),
     T(12, 'every class ∩ regular  =>  same class', size=32, color='green'))

p = page('Countability & Non-RE Languages', 11)
beat(p, '''Why do non R E languages exist? Sigma star is countable, because we can list all strings by length. Every Turing machine can be written as a string, so there are only countably many Turing machines.
But the set of all languages, the power set of sigma star, is uncountable, by Cantor's diagonal argument. So there are more languages than Turing machines.''',
     T(0, 'Σ* is [h:countable] (list strings by length)', size=34), T(1, 'TMs are countable (each TM is a string)', size=34),
     T(2, 'all languages 2^Σ* are [r:uncountable] (diagonal argument)', size=34), T(3, '=> some languages are [r:not RE]', size=36))
beat(p, '''A famous example is the diagonal language, L d. Number all strings and all Turing machines. L d contains string number i whenever machine number i does not accept it. No Turing machine can accept it, so L d is not even R E.''',
     Stamp(1650, 140), T(5, '[k:L_d] = { w_i | M_i does not accept w_i }  =>  [r:not RE]', size=34))
beat(p, '''The universal language, L u, contains a machine M and a string w whenever M accepts w. It is R E, because a universal Turing machine can simulate M on w. But it is not recursive.
So remember three levels: recursive, R E but not recursive, and not R E.''',
     T(7, '[k:L_u] = { <M, w> | M accepts w }  =>  RE but not recursive', size=34),
     Tab(180, 650, [520, 520, 520], 56, [['Recursive', 'RE, not recursive', 'not RE'], ['a^n b^n c^n, any CFL', 'L_u, halting problem', 'L_d, complement of L_u'],
         ['TM always halts', 'TM halts on yes', 'no TM at all']], size=28, colors={(0, 0): 'green', (0, 1): 'blue', (0, 2): 'red'}))

D_, U_ = '[g:D]', '[r:U]'
p = page('Decision Properties: GATE Table', 11)
beat(p, '''This table is asked in almost every GATE paper. It shows which questions are decidable, D, or undecidable, U, for each class of languages.
For regular languages, everything is decidable. For context free languages, membership, emptiness and finiteness are decidable, but equivalence is not.''',
     Stamp(1650, 140, 'GATE'),
     Tab(180, 240, [340, 230, 230, 230, 230, 300], 58, [['Problem', 'Regular', 'DCFL', 'CFL', 'CSL', 'Recursive / RE'],
         ['Membership', D_, D_, D_, D_, D_ + ' / ' + U_], ['Emptiness', D_, D_, D_, U_, U_], ['Finiteness', D_, D_, D_, U_, U_],
         ['Equivalence', D_, D_, U_, U_, U_], ['Is L = Σ* ?', D_, D_, U_, U_, U_], ['Ambiguity', '-', '-', U_, '-', '-']], size=28))
beat(p, '''Remember the special ones. Membership is decidable all the way up to recursive languages, but not for recursively enumerable. Equivalence of two D C F Ls is decidable,
but equivalence of two C F Ls is not. And for context sensitive languages, only membership is decidable.''',
     T(10, 'membership: decidable up to recursive;  [r:undecidable for RE]', size=32), T(11, 'equivalence: DCFL [g:decidable], CFL [r:undecidable]', size=32),
     T(12, 'CSL: only membership is decidable', size=32))

p = page('P, NP & NP-Complete', 11)
beat(p, '''Complexity theory asks how much time a problem needs. P is the class of problems solved in polynomial time by a deterministic machine, like sorting and shortest path.
N P is the class of problems whose solutions can be checked in polynomial time, or solved in polynomial time by a non deterministic machine. Every problem in P is also in N P.''',
     T(0, '[h:P]: solvable in polynomial time (sorting, shortest path)', size=34), T(1, '[h:NP]: solution [r:verifiable] in polynomial time', size=34),
     T(2, 'P ⊆ NP;   P = NP ?  is still unsolved', size=34, color='red'))
beat(p, '''A problem is N P hard if every N P problem reduces to it in polynomial time. It is N P complete if it is N P hard and also in N P. The first N P complete problem was S A T,
by the Cook Levin theorem. Others are three S A T, clique, vertex cover, Hamiltonian cycle, the travelling salesman decision problem, and subset sum.''',
     Stamp(1650, 140, 'MOST ASKED'), T(4, '[k:NP-hard]: every NP problem reduces to it', size=34), T(5, '[k:NP-complete] = NP-hard ∩ NP', size=34),
     T(6, 'SAT (Cook-Levin), 3-SAT, clique, vertex cover, Hamiltonian cycle, TSP, subset sum', size=30),
     Ell(1080, 600, 520, 300, None, color='blue'), Ell(1120, 680, 200, 140, 'P', size=34, color='green'), T(0, 'NP', x=1330, y=650, size=34, color='blue'),
     Ell(1400, 560, 460, 380, None, color='red'), T(0, 'NP-hard', x=1660, y=700, size=28, color='red'), T(0, 'NP-complete', x=1406, y=764, size=26, color='red'))
beat(p, '''To prove a new problem B is N P complete: show B is in N P, then reduce a known N P complete problem A to B in polynomial time. The direction matters: from the known problem to the new one.
If any N P complete problem is solved in polynomial time, then P equals N P. Note that two SAT is in P, but three SAT is N P complete.''',
     T(10, 'Prove B NP-complete: B ∈ NP, and known NPC A ≤p B', size=32, color='red'), T(11, 'any NPC problem in P  =>  P = NP', size=32),
     T(12, '[g:2-SAT ∈ P]   but   [r:3-SAT is NP-complete]', size=32))

# ===================================================================================== CH 12
p = chapter(12)
beat(p, "Chapter twelve. Exam revision. If you're short on time, revise these first.")

p = page('Most Asked Exam Questions', 12)
qs = ['Chomsky hierarchy (grammar + machine)', 'DFA design: ends with ab, divisible by 3', 'NFA to DFA (subset construction)', 'DFA minimization (partition method)',
      "RE identities; Arden's theorem (FA to RE)", 'Pumping lemma: a^n b^n not regular', 'Ambiguity; simplification; CNF & GNF', 'CYK algorithm; closure of CFLs',
      'PDA for a^n b^n (with IDs); DPDA vs NPDA', 'TM for a^n b^n; variants; LBA', "Halting problem; Rice's theorem; PCP", 'Decidability table; P, NP, NP-complete']
beat(p, '''Here are the most asked questions. The Chomsky hierarchy. D F A design. N F A to D F A. And D F A minimization.''', *[T(k, f'{k + 1}. {q}', x=200, size=36) for k, q in enumerate(qs[:4])])
beat(p, '''Arden's theorem and regular expressions. The pumping lemma. Ambiguity, simplification and normal forms. And C Y K with the closure properties of context free languages.''',
     *[T(k, f'{k + 1}. {q}', x=200, size=36) for k, q in enumerate(qs) if 4 <= k < 8])
beat(p, '''P D A design with instantaneous descriptions. Turing machine design. The halting problem, Rice's theorem and P C P. And the decidability table with P and N P.''',
     *[T(k, f'{k + 1}. {q}', x=200, size=36) for k, q in enumerate(qs) if k >= 8])
beat(p, '''One last exam tip. For every machine design, write the idea in one line, draw the diagram neatly, and test it on one example string.
That way you still get step marks, even if a small transition is wrong.''',
     T(13, 'Tip: [h:idea + neat diagram + test one string] => full marks!', color='red'))

p = page('All the Best!', 12, kind='outro')
beat(p, '''That's the complete theory of computation subject. If this helped you, share it with your friends who have the exam,
and subscribe to TechVibe24 for more one shot videos. Tell me in the comments which subject you want next. All the best for your exam!''')

if __name__ == '__main__':
    json.dump({'pages': PAGES, 'chapters': CHAPTERS}, open('toc_script.json', 'w'), indent=1, ensure_ascii=False)
    nb = sum(len(p['beats']) for p in PAGES); nw = sum(len(b['say'].split()) for p in PAGES for b in p['beats'])
    print('pages', len(PAGES), 'beats', nb, 'words', nw, 'est minutes', round(nw / 150, 1))
