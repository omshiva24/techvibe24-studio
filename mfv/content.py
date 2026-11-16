'''Mathematical Foundations of Computer Science one-shot: narration beats + handwritten note elements for every page.
Markup inside text: [r:red] [g:green] [k:black] [h:yellow highlight] [p:pink highlight]'''
import json, math
from math import comb
from mf_numericals import *

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
def M(x, y, s, size=30, color='black'): return T(0, s, x=x, y=y, size=size, font='mono', color=color)
def Node(p, name, color='blue', r=34, size=28): return Ell(p[0] - r, p[1] - r, 2 * r, 2 * r, name, color=color, size=size)
def WEdge(a, b, w=None, color='black', r=34, side=1, size=28, off=24, width=4):
    (x1, y1), (x2, y2) = a, b; d = math.hypot(x2 - x1, y2 - y1); ux, uy = (x2 - x1) / d, (y2 - y1) / d; nx, ny = -uy, ux
    if ny > 0 or (abs(ny) < 1e-9 and nx < 0): nx, ny = -nx, -ny
    nx, ny = nx * side, ny * side; mx, my = (x1 + x2) / 2 + nx * off, (y1 + y2) / 2 + ny * off
    out = [Ln([(x1 + ux * r, y1 + uy * r), (x2 - ux * r, y2 - uy * r)], color, width)]
    if w is not None: out.append(T(0, str(w), x=mx - size * .28, y=my + size * .35, size=size, color='red'))
    return out
TFc = lambda b: '[g:T]' if b else '[r:F]'

CHAPTERS = [
 (1, 'Propositional Logic', ['Propositions & connectives', 'Truth tables & tautology', 'Logical equivalences'], 5),
 (2, 'Normal Forms & Rules of Inference', ['PDNF & PCNF', 'Rules of inference', 'Valid arguments'], 5),
 (3, 'Predicates, Quantifiers & Proofs', ['Quantifiers & negation', 'Nested quantifiers', 'Proof methods'], 4),
 (4, 'Sets & Functions', ['Set operations', 'Venn diagram numerical', 'Types of functions'], 4),
 (5, 'Sequences, Summations & Matrices', ['AP, GP & summations', 'Matrix multiplication', 'Zero-one matrices'], 3),
 (6, 'Relations', ['Properties of relations', 'Matrix, digraph & closure', 'Equivalence & partial order'], 5),
 (7, 'Divisibility & Integer Representations', ['Division algorithm', 'Modular arithmetic', 'Base conversion', 'Modular exponentiation'], 4),
 (8, 'Primes, GCD & Congruences', ['Primes', 'Euclidean algorithm', 'Linear congruences & CRT', "Fermat's little theorem"], 5),
 (9, 'Induction & Recursion', ['Mathematical induction', 'Strong induction & well-ordering', 'Recursive definitions'], 5),
 (10, 'Counting', ['Sum & product rules', 'Pigeonhole principle', 'Permutations & combinations', 'Binomial theorem'], 5),
 (11, 'Algebraic Structures', ['Semigroup, monoid, group', 'Subgroups & Lagrange'], 3),
 (12, 'Recurrence Relations', ['Characteristic roots', 'Non-homogeneous', 'Generating functions'], 4),
 (13, 'Graph Theory & Trees', ['Graph basics', 'Euler & Hamilton', 'Planar & colouring', 'Trees & MST'], 4),
 (14, 'Exam Revision', ['Formula sheet', 'Most asked questions'], 5),
]
def chapter(i):
    n, t, subs, stars = CHAPTERS[i - 1]
    return page(t, n, kind='chapter', num=n, subs=subs, stars=stars)

# =====================================================================================
p = page('Mathematical Foundations of Computer Science', 0, kind='cover')
beat(p, '''Mathematical Foundations of Computer Science. The complete subject in one video. Simple explanations, handwritten notes,
and every important exam problem solved step by step.''')
beat(p, '''This video follows the Pondicherry University B Sc Honours computer science syllabus, all five units, and it also covers the extra topics that other universities ask,
like algebraic structures, recurrence relations and graph theory. So it works for B Sc, B C A and B Tech students everywhere. Grab a pen, and let's start.''')

p = page('Contents', 0)
items = ['[h:Propositional logic]', 'Normal forms & [h:rules of inference]', 'Predicates, quantifiers & proofs', 'Sets & functions', 'Sequences, summations & matrices',
         '[h:Relations]', 'Divisibility & integer representations', '[h:Primes, GCD & congruences]', '[h:Induction] & recursion', '[h:Counting]',
         'Algebraic structures', 'Recurrence relations', 'Graph theory & trees', 'Exam revision']
beat(p, "Here's our plan. Fourteen chapters.", T(0, 'What we will cover today', size=40, font='bold', color='black'))
beat(p, '''Chapters one to three are unit one of Pondicherry University: logic and proofs. Chapters four to six are unit two: sets, functions, sequences, matrices and relations.''',
     *[T(1 + k, f'{k + 1}.  {items[k]}', x=200, size=34) for k in range(6)], T(0, '<- PU Unit I', x=1000, y=L(2), size=30, color='red'), T(0, '<- PU Unit II', x=1000, y=L(5), size=30, color='red'))
beat(p, '''Chapters seven and eight are unit three, number theory. Chapter nine is unit four, induction and recursion. And chapter ten is unit five, counting.''',
     *[T(7 + k, f'{k + 7}.  {items[k + 6]}', x=200, size=34) for k in range(4)], T(0, '<- PU Unit III', x=1000, y=L(7) + 27, size=30, color='red'),
     T(0, '<- PU Unit IV', x=1000, y=L(9), size=30, color='red'), T(0, '<- PU Unit V', x=1000, y=L(10), size=30, color='red'))
beat(p, '''Chapters eleven to thirteen are for other universities: algebraic structures, recurrence relations, and graph theory. And chapter fourteen is a quick revision.''',
     *[T(11 + k, f'{k + 11}.  {items[k + 10]}', x=200, size=34) for k in range(4)], T(0, '<- other universities', x=1000, y=L(12), size=30, color='green'))

# ===================================================================================== CH 1
p = chapter(1)
beat(p, "Chapter one. Propositional logic. This is the language of every proof, and the base of digital circuits.")

p = page('Propositions & Connectives', 1)
beat(p, '''A proposition is a statement that is either true or false, but not both. For example, "two plus three equals five" is true, and "Delhi is in Japan" is false.
A question like "what time is it?", or a sentence like "x plus one equals two", is not a proposition, because it is not simply true or false.''',
     T(0, '[h:Proposition]: a statement that is either true (T) or false (F)', size=36), T(1, '2 + 3 = 5 ([g:T]),   Delhi is in Japan ([r:F])', size=34),
     T(2, 'Not propositions: "What time is it?",  "x + 1 = 2"', size=34, color='red'))
beat(p, '''We join propositions using connectives. Negation, not p, flips the truth value. Conjunction, p and q, is true only when both are true. Disjunction, p or q, is false only when both are false.
Exclusive or is true when exactly one is true.''',
     Stamp(1650, 140),
     Tab(180, 370, [260, 230, 960], 54, [['Connective', 'Symbol', 'True when ...'], ['negation', '¬p', 'p is false'], ['conjunction (AND)', 'p ∧ q', 'both are true'],
         ['disjunction (OR)', 'p ∨ q', 'at least one is true'], ['exclusive OR', 'p ⊕ q', 'exactly one is true'], ['implication', 'p → q', 'everything except T → F'],
         ['biconditional', 'p ↔ q', 'both have the same value']], size=29, colors={(r, 1): 'red' for r in range(1, 7)}))
beat(p, '''The implication, p implies q, means "if p then q". It is false only when p is true and q is false. Its converse is q implies p, its inverse is not p implies not q, and its contrapositive is not q implies not p.
An implication is always equivalent to its contrapositive.''',
     T(12, 'p → q: [r:false only when p = T, q = F]', size=34), T(13, 'converse q → p · inverse ¬p → ¬q · [h:contrapositive ¬q → ¬p ≡ p → q]', size=32))

tt = [(p_, q_) for p_ in (True, False) for q_ in (True, False)]
p = page('Truth Tables & Tautology', 1)
beat(p, '''A truth table lists the value of a compound proposition for every combination of its variables. With n variables, there are two to the power n rows. Here is the table for all the basic connectives.''',
     Stamp(1650, 140, 'NUMERICAL'), T(0, 'n variables  =>  [h:2^n rows]', size=36),
     Tab(180, 290, [110, 110, 150, 150, 150, 170, 170], 54, [['p', 'q', '¬p', 'p ∧ q', 'p ∨ q', 'p → q', 'p ↔ q']] +
         [[TFc(a), TFc(b), TFc(not a), TFc(a and b), TFc(a or b), TFc((not a) or b), TFc(a == b)] for a, b in tt], size=30))
beat(p, '''A tautology is always true, a contradiction is always false, and a contingency is sometimes true and sometimes false. Let's check whether p and p implies q, all implies q, is a tautology.
Build it column by column. In every row the final column is true, so it is a tautology. This is the rule called modus ponens.''',
     T(7, '[k:Tautology]: always T · [k:Contradiction]: always F · [k:Contingency]: both', size=32),
     T(8, 'Check: (p ∧ (p → q)) → q', size=34, color='black'),
     Tab(180, 690, [110, 110, 200, 290, 380], 52, [['p', 'q', 'p → q', 'p ∧ (p → q)', '(p ∧ (p → q)) → q']] +
         [[TFc(a), TFc(b), TFc((not a) or b), TFc(a and ((not a) or b)), TFc((not (a and ((not a) or b))) or b)] for a, b in tt], size=29),
     T(0, 'all [g:T]  =>  [h:tautology] ✓', x=1320, y=850, size=36, color='green'))

p = page('Logical Equivalences', 1)
beat(p, '''Two propositions are logically equivalent if they have the same truth value in every row. We write p is equivalent to q with three lines. Here are the laws you must know.''',
     Stamp(1650, 140, 'MOST ASKED'), T(0, 'p ≡ q  <=>  p ↔ q is a tautology', size=36),
     Tab(180, 300, [380, 760], 52, [['Law', 'Equivalence'], ['Identity', 'p ∧ T ≡ p,   p ∨ F ≡ p'], ['Domination', 'p ∨ T ≡ T,   p ∧ F ≡ F'], ['Idempotent', 'p ∨ p ≡ p,   p ∧ p ≡ p'],
         ['Double negation', '¬(¬p) ≡ p'], ['Distributive', 'p ∨ (q ∧ r) ≡ (p ∨ q) ∧ (p ∨ r)'], ['[h:De Morgan]', '¬(p ∧ q) ≡ ¬p ∨ ¬q,   ¬(p ∨ q) ≡ ¬p ∧ ¬q'],
         ['Absorption', 'p ∨ (p ∧ q) ≡ p'], ['Negation', 'p ∨ ¬p ≡ T,   p ∧ ¬p ≡ F'], ['[h:Implication]', 'p → q ≡ ¬p ∨ q']], size=28))
beat(p, '''Now let's prove one without a truth table. Show that not of, p or, not p and q, is equivalent to not p and not q. Use De Morgan, then De Morgan again with double negation, then distributive,
then the negation law, and finally the identity law.''',
     T(0, 'Prove: ¬(p ∨ (¬p ∧ q)) ≡ ¬p ∧ ¬q', x=1340, y=L(2), size=30, color='black'),
     T(0, '≡ ¬p ∧ ¬(¬p ∧ q)      De Morgan', x=1340, y=L(3), size=28), T(0, '≡ ¬p ∧ (p ∨ ¬q)      De Morgan, ¬¬', x=1340, y=L(4), size=28),
     T(0, '≡ (¬p ∧ p) ∨ (¬p ∧ ¬q)   distributive', x=1340, y=L(5), size=28), T(0, '≡ F ∨ (¬p ∧ ¬q)      negation', x=1340, y=L(6), size=28),
     T(0, '≡ [h:¬p ∧ ¬q]   identity ✓', x=1340, y=L(7), size=30, color='red'))

# ===================================================================================== CH 2
p = chapter(2)
beat(p, 'Chapter two. Normal forms, and rules of inference.')

f_mins, f_maxs = normal_forms(lambda p_, q_, r_: (p_ and q_) or ((not p_) and r_))
p = page('Normal Forms: PDNF & PCNF', 2)
beat(p, '''A formula is in disjunctive normal form, D N F, when it is an OR of AND terms, and in conjunctive normal form, C N F, when it is an AND of OR terms.
A minterm is an AND of every variable or its negation. The principal disjunctive normal form, P D N F, is the OR of the minterms where the formula is true.
The principal conjunctive normal form, P C N F, is the AND of the maxterms where the formula is false.''',
     Stamp(1650, 140, 'NUMERICAL'), T(0, '[k:DNF]: OR of ANDs   ·   [k:CNF]: AND of ORs', size=34),
     T(1, '[h:PDNF] = ∨ of minterms where f = T   ·   [h:PCNF] = ∧ of maxterms where f = F', size=32))
beat(p, '''Example: f equals, p and q, or, not p and r. Make the truth table with eight rows. f is true in rows zero zero one, zero one one, one one zero and one one one.''',
     T(3, 'f = (p ∧ q) ∨ (¬p ∧ r)', size=36, color='black'),
     Tab(180, 430, [90, 90, 90, 110], 50, [['p', 'q', 'r', 'f']] + [[b[0], b[1], b[2], ('[g:1]' if b in [m[2] for m in f_mins] else '[r:0]')]
         for b in [f'{i:03b}' for i in range(8)]], size=28))
beat(p, f'''So the P D N F is the OR of those four minterms. And the P C N F is the AND of the maxterms for the four false rows. In a maxterm, a variable that is one appears negated, and a variable that is zero appears plain.''',
     T(0, 'PDNF:', x=650, y=L(5), size=32, color='red'), *[T(0, m[0] + ('  ∨' if i < 3 else ''), x=780, y=L(5) + 50 * i, size=30) for i, m in enumerate(f_mins)],
     T(0, 'PCNF:', x=650, y=L(10) + 4, size=32, color='red'), *[T(0, m[1] + ('  ∧' if i < 3 else ''), x=780, y=L(10) + 4 + 50 * i, size=30) for i, m in enumerate(f_maxs)])

p = page('Rules of Inference', 2)
beat(p, '''An argument is a list of premises followed by a conclusion. It is valid if the conclusion must be true whenever all the premises are true. Rules of inference are small valid arguments that we chain together.''',
     T(0, '[h:Valid argument]: premises all true  =>  conclusion true', size=36))
beat(p, '''Modus ponens: from p, and p implies q, conclude q. Modus tollens: from not q, and p implies q, conclude not p. Hypothetical syllogism: from p implies q and q implies r, conclude p implies r.
Disjunctive syllogism: from p or q, and not p, conclude q. Then addition, simplification, conjunction, and resolution.''',
     Stamp(1650, 140, 'MOST ASKED'),
     Tab(180, 300, [420, 480, 280], 54, [['Rule', 'Premises', 'Conclusion'], ['[h:Modus ponens]', 'p,  p → q', '∴ q'], ['[h:Modus tollens]', '¬q,  p → q', '∴ ¬p'],
         ['Hypothetical syllogism', 'p → q,  q → r', '∴ p → r'], ['Disjunctive syllogism', 'p ∨ q,  ¬p', '∴ q'], ['Addition', 'p', '∴ p ∨ q'], ['Simplification', 'p ∧ q', '∴ p'],
         ['Conjunction', 'p,  q', '∴ p ∧ q'], ['Resolution', 'p ∨ q,  ¬p ∨ r', '∴ q ∨ r']], size=29, colors={(r, 2): 'red' for r in range(1, 9)}))
beat(p, '''Watch out for two common mistakes. From p implies q and q, you cannot conclude p. This is called affirming the conclusion. And from p implies q and not p, you cannot conclude not q.''',
     T(13, '[r:Fallacies]: p → q, q ∴ p  ✗      p → q, ¬p ∴ ¬q  ✗', size=34))

p = page('Valid Argument: Step by Step', 2)
beat(p, '''Exam question. Show that these premises lead to the conclusion. It is not sunny and it is colder than yesterday. We will go swimming only if it is sunny. If we do not go swimming, we will take a canoe trip.
If we take a canoe trip, we will be home by sunset. Conclusion: we will be home by sunset. First, name the propositions.''',
     Stamp(1650, 140, 'NUMERICAL'), T(0, 'p: sunny   q: colder   r: swimming   s: canoe trip   t: home by sunset', size=31, color='black'),
     T(1, 'Premises: ¬p ∧ q,   r → p,   ¬r → s,   s → t        Conclusion: t', size=33))
beat(p, '''Now the steps. One, not p and q, a premise. Two, not p, by simplification. Three, r implies p, a premise. Four, not r, by modus tollens using two and three.
Five, not r implies s, a premise. Six, s, by modus ponens. Seven, s implies t, a premise. And eight, t, by modus ponens. So we will be home by sunset.''',
     Tab(180, 360, [100, 360, 600], 54, [['Step', 'Statement', 'Reason'], ['1', '¬p ∧ q', 'premise'], ['2', '¬p', 'simplification (1)'], ['3', 'r → p', 'premise'],
         ['4', '¬r', '[h:modus tollens] (2, 3)'], ['5', '¬r → s', 'premise'], ['6', 's', '[h:modus ponens] (4, 5)'], ['7', 's → t', 'premise'], ['8', '[g:t]', 'modus ponens (6, 7) ✓']],
         size=30, colors={(8, 1): 'red'}))

# ===================================================================================== CH 3
p = chapter(3)
beat(p, 'Chapter three. Predicates, quantifiers, and methods of proof.')

p = page('Predicates & Quantifiers', 3)
beat(p, '''A predicate is a statement with a variable, like P of x: x is greater than three. It becomes a proposition when we give x a value: P of four is true, and P of two is false.
The universal quantifier, for all x, P of x, is true when P of x is true for every x in the domain. The existential quantifier, there exists x, P of x, is true when at least one x works.''',
     T(0, '[h:Predicate] P(x): x > 3;   P(4) = [g:T],   P(2) = [r:F]', size=36),
     T(1, '[k:∀x P(x)]: true for [r:every] x in the domain   ·   [k:∃x P(x)]: true for [r:at least one] x', size=32),
     T(2, 'domain = integers:  ∀x (x > 3) is [r:F] (x = 1),   ∃x (x > 3) is [g:T] (x = 4)', size=32))
beat(p, '''Negating a quantifier flips it. Not, for all x, P of x, is the same as, there exists x, not P of x. And not, there exists x, P of x, is the same as, for all x, not P of x.
These are De Morgan's laws for quantifiers. For example, "not every student passed" means "some student did not pass".''',
     Stamp(1650, 140, 'MOST ASKED'), T(4, '[h:¬∀x P(x) ≡ ∃x ¬P(x)]      [h:¬∃x P(x) ≡ ∀x ¬P(x)]', size=38, color='red'),
     T(5, '"Not every student passed"  ≡  "Some student did not pass"', size=34))
beat(p, '''With nested quantifiers, the order matters. Over the integers, for all x there exists y such that x plus y equals zero is true, because y can be minus x.
But there exists y such that for all x, x plus y equals zero is false, because one y cannot work for every x.''',
     T(7, 'Nested (domain = integers):', size=34, color='black'), T(8, '∀x ∃y (x + y = 0)   [g:T]  (take y = -x)', size=34), T(9, '∃y ∀x (x + y = 0)   [r:F]  (one y can\'t work for all x)', size=34),
     T(10, '[h:order of quantifiers matters]', size=34, color='red'),
     T(12, 'Translate: "Every student has a laptop":  ∀x (S(x) → L(x))', size=32, color='green'), T(13, '"Some student has a laptop":  ∃x (S(x) ∧ L(x))', size=32, color='green'))

p = page('Methods of Proof', 3)
beat(p, '''In a direct proof of p implies q, assume p and show q. Example: if n is odd, then n squared is odd. Write n as two k plus one. Then n squared is four k squared plus four k plus one,
which is two times something, plus one. So n squared is odd.''',
     Stamp(1650, 140, 'MOST ASKED'), S(0, '1) Direct proof', color='red', size=36), T(1, 'n odd => n = 2k + 1 => n² = 4k² + 4k + 1 = 2(2k² + 2k) + 1 => [h:odd] ✓', size=32))
beat(p, '''In proof by contrapositive, we prove not q implies not p instead. Example: if three n plus two is odd, then n is odd. Assume n is even, n equals two k. Then three n plus two is six k plus two, which is even.
So the contrapositive is true, and the statement is true.''',
     S(3, '2) Contrapositive (prove ¬q → ¬p)', color='red', size=36), T(4, 'If 3n + 2 odd then n odd:  n = 2k => 3n + 2 = 6k + 2 = 2(3k + 1) even ✓', size=32))
beat(p, '''In proof by contradiction, assume the statement is false and reach something impossible. Example: root two is irrational. Assume root two equals a over b in lowest terms.
Then a squared equals two b squared, so a is even. Write a as two c. Then b squared equals two c squared, so b is also even. But a over b was in lowest terms. Contradiction.''',
     S(6, '3) Contradiction', color='red', size=36), T(7, '√2 = a/b (lowest terms) => a² = 2b² => a even, a = 2c => b² = 2c² => b even', size=32),
     T(8, '=> a, b both even  [r:contradiction]  =>  √2 is irrational ✓', size=32))
beat(p, '''Other methods: proof by cases, an existence proof that shows an example, and a counterexample to disprove a "for all" statement. For example, "every prime is odd" is false, because two is prime and even.''',
     T(10, '4) [k:Cases]   5) [k:Existence] (give an example)   6) [k:Counterexample]', size=32), T(11, '"Every prime is odd" ✗  counterexample: 2', size=32, color='green'))

# ===================================================================================== CH 4
p = chapter(4)
beat(p, 'Chapter four. Sets and functions.')

p = page('Sets & Set Operations', 4)
beat(p, '''A set is an unordered collection of distinct objects, called elements. We can list them, like A equals one, two, three, or describe them with set builder notation.
A is a subset of B if every element of A is in B. The empty set, phi, is a subset of every set. The power set of A is the set of all subsets of A. If A has n elements, its power set has two to the power n elements.''',
     T(0, '[h:Set]: unordered, distinct elements;  A = {1, 2, 3},  B = {x | x is even}', size=34), T(1, 'A ⊆ B: every element of A is in B;   ∅ ⊆ every set', size=34),
     T(2, 'P({a, b}) = {∅, {a}, {b}, {a, b}}   ·   |A| = n  =>  [h:|P(A)| = 2^n]', size=34))
beat(p, '''The operations: union, A union B, has elements in A or B. Intersection has elements in both. Difference, A minus B, has elements in A but not in B. And the complement has everything not in A.
The Cartesian product, A cross B, is the set of all ordered pairs, a comma b. Its size is the size of A times the size of B.''',
     Stamp(1650, 140),
     Tab(180, 400, [300, 360, 760], 52, [['Operation', 'Symbol', 'Example: A = {1, 2, 3}, B = {3, 4}'], ['union', 'A ∪ B', '{1, 2, 3, 4}'], ['intersection', 'A ∩ B', '{3}'],
         ['difference', 'A - B', '{1, 2}'], ['symmetric diff.', 'A ⊕ B', '{1, 2, 4}'], ['Cartesian product', 'A × B', '{(1,3), (1,4), (2,3), ... }  6 pairs']], size=29,
         colors={(r, 1): 'red' for r in range(1, 6)}))
beat(p, '''The set identities match the logic laws. De Morgan's laws for sets: the complement of A union B is the complement of A intersect the complement of B, and the other way round.''',
     T(12, '[h:De Morgan]:  (A ∪ B)\' = A\' ∩ B\'      (A ∩ B)\' = A\' ∪ B\'', size=36, color='red'), T(13, '|A × B| = |A| × |B|;   |A ∪ B| = |A| + |B| - |A ∩ B|', size=34))

un, none_, only = venn3()
vc = {'A': (1240, 520), 'B': (1460, 520), 'C': (1350, 700)}; vr = 175
p = page('Venn Diagram Numerical', 4)
beat(p, '''A favourite exam problem. In a class of one hundred students, forty five like C, forty like Java, and thirty five like Python. Fifteen like C and Java, ten like Java and Python,
twelve like C and Python, and five like all three. How many like none?''',
     Stamp(1650, 140, 'NUMERICAL'), T(0, 'U = 100:  |C| = 45, |J| = 40, |P| = 35', size=34, color='black'), T(1, '|C ∩ J| = 15, |J ∩ P| = 10, |C ∩ P| = 12, |C ∩ J ∩ P| = 5', size=34, color='black'))
beat(p, f'''Use the inclusion exclusion principle for three sets. The size of the union is forty five plus forty plus thirty five, minus fifteen, minus ten, minus twelve, plus five. That is eighty eight.
So one hundred minus eighty eight, which is twelve students, like none of them.''',
     T(3, '|C ∪ J ∪ P| = |C| + |J| + |P|', size=34), T(4, '   - |C ∩ J| - |J ∩ P| - |C ∩ P| + |C ∩ J ∩ P|', size=34),
     T(5, f'= 45 + 40 + 35 - 15 - 10 - 12 + 5 = [h:{un}]', size=36, color='red'), T(6, f'None = 100 - {un} = [h:{none_}]', size=36, color='red'))
beat(p, f'''Fill the Venn diagram from the centre outwards. Five in the middle. C and Java only is fifteen minus five, ten. Java and Python only is five. C and Python only is seven.
Then only C is forty five minus ten minus seven minus five, which is twenty three. Only Java is twenty, and only Python is eighteen.''',
     Box(1020, 300, 660, 640, None, 'grey'), T(0, 'U = 100', x=1040, y=340, size=28, color='grey'), T(0, f'none = {none_}', x=1500, y=920, size=28, color='red'),
     *[Ell(c[0] - vr, c[1] - vr, 2 * vr, 2 * vr, None, col) for c, col in zip(vc.values(), ('blue', 'green', 'red'))],
     T(0, 'C', x=1110, y=380, size=34, font='bold', color='blue'), T(0, 'Java', x=1560, y=380, size=34, font='bold', color='green'), T(0, 'Python', x=1300, y=915, size=30, font='bold', color='red'),
     *[T(0, str(v), x=x, y=y, size=34, color='black') for v, x, y in ((only['a'], 1150, 500), (only['b'], 1520, 500), (only['c'], 1335, 780), (only['ab'], 1335, 470),
       (only['ac'], 1245, 630), (only['bc'], 1430, 630), (only['abc'], 1340, 575))])

p = page('Functions', 4)
beat(p, '''A function f from A to B assigns exactly one element of B to each element of A. A is the domain, B is the codomain, and the set of actual outputs is the range.
A function is one to one, or injective, if different inputs give different outputs. It is onto, or surjective, if every element of B is an output. And it is a bijection if it is both.''',
     T(0, '[h:f : A -> B]: each element of A gets [r:exactly one] element of B', size=34), T(1, 'domain A · codomain B · range = actual outputs', size=32),
     T(2, '[k:one-one]: f(a) = f(b) => a = b   ·   [k:onto]: range = B   ·   [k:bijection]: both', size=32))
beat(p, '''Example: f of x equals two x plus three, on the real numbers, is a bijection. Its inverse is f inverse of y equals y minus three, over two. And with g of x equals x squared,
f of g of x is two x squared plus three, but g of f of x is two x plus three, whole squared. So composition is not commutative.''',
     Stamp(1650, 140, 'NUMERICAL'), T(4, 'f(x) = 2x + 3 on ℝ: bijection;   f⁻¹(y) = (y - 3) / 2', size=34),
     T(5, 'g(x) = x²:   (f ∘ g)(x) = 2x² + 3    (g ∘ f)(x) = (2x + 3)²', size=34), T(6, 'f ∘ g ≠ g ∘ f  (composition is not commutative)', size=32, color='red'))
beat(p, f'''Counting functions from a set with m elements to a set with n elements: there are n to the power m functions. For four to three, that is eighty one. Using inclusion exclusion,
thirty six of them are onto. The floor function rounds down, and the ceiling function rounds up: floor of three point seven is three, and ceiling of minus three point seven is minus three.''',
     T(8, f'|A| = m, |B| = n:  functions = n^m  (4 -> 3: 3^4 = {3 ** 4})', size=32), T(9, f'onto (4 -> 3) = 3^4 - 3·2^4 + 3·1^4 = [h:{onto_count(4, 3)}]', size=32),
     T(10, '⌊3.7⌋ = 3,   ⌈3.2⌉ = 4,   ⌊-3.7⌋ = -4,   ⌈-3.7⌉ = -3', size=34, color='black'))

# ===================================================================================== CH 5
p = chapter(5)
beat(p, 'Chapter five. Sequences, summations, and matrices.')

p = page('Sequences & Summations', 5)
beat(p, '''A sequence is an ordered list of numbers. In an arithmetic progression, each term adds a fixed difference d: a, a plus d, a plus two d, and so on. The n th term is a plus n minus one times d.
In a geometric progression, each term multiplies by a fixed ratio r: a, a r, a r squared. The n th term is a times r to the power n minus one.''',
     T(0, '[h:AP]: a, a + d, a + 2d, ...   nth term = a + (n - 1)d,   S_n = n/2 [2a + (n - 1)d]', size=32),
     T(1, '[h:GP]: a, ar, ar², ...   nth term = a r^(n-1),   S_n = a(r^n - 1) / (r - 1)', size=32))
beat(p, '''Summation notation uses the Greek letter sigma. Three formulas you must remember: the sum of the first n numbers is n into n plus one by two. The sum of squares is n into n plus one into two n plus one, by six.
And the sum of cubes is the square of n into n plus one by two.''',
     Stamp(1650, 140, 'MOST ASKED'), T(3, 'Σ k = n(n + 1) / 2', size=38, color='red'), T(4, 'Σ k² = n(n + 1)(2n + 1) / 6', size=38, color='red'), T(5, 'Σ k³ = [n(n + 1) / 2]²', size=38, color='red'))
beat(p, f'''Example: find the sum of k squared, for k from fifty to one hundred. Take the sum up to one hundred, and subtract the sum up to forty nine. That is three lakh thirty eight thousand three hundred and fifty,
minus forty thousand four hundred and twenty five, which gives two lakh ninety seven thousand nine hundred and twenty five.''',
     T(7, 'Σ k² (k = 50 to 100) = Σ (1 to 100) - Σ (1 to 49)', size=34, color='black'), T(8, f'= 100·101·201/6 - 49·50·99/6 = {100 * 101 * 201 // 6:,} - {49 * 50 * 99 // 6:,}', size=34),
     T(9, f'= [h:{sum(k * k for k in range(50, 101)):,}]', size=36, color='red'),
     T(11, 'Infinite GP (|r| < 1):  Σ ar^k = a / (1 - r)', size=32, color='green'))

MA = [[1, 2, 0], [0, 1, 3]]; MB = [[2, 1], [1, 0], [0, 4]]; MAB = matmul(MA, MB)
Z1 = [[1, 0, 1], [0, 1, 0]]; Z2 = [[1, 0], [0, 1], [1, 0]]; ZB = bool_prod(Z1, Z2)
def mat(x, y, Mx, cw=60, rh=48, size=30, color='black'): return Tab(x, y, [cw] * len(Mx[0]), rh, [[str(v) for v in r] for r in Mx], size=size, hdr=False, color=color)
p = page('Matrices & Zero-One Matrices', 5)
beat(p, '''A matrix is a rectangular array of numbers. An m by k matrix can be multiplied by a k by n matrix, and the result is m by n. Each entry is the sum of products of a row of the first and a column of the second.
For example, the first entry here is one times two, plus two times one, plus zero times zero, which is four.''',
     Stamp(1650, 140, 'NUMERICAL'), T(0, '(m × k) × (k × n) = (m × n);   c_ij = row i · column j', size=34),
     mat(240, 300, MA), T(0, '×', x=450, y=360, size=40), mat(500, 290, MB), T(0, '=', x=650, y=360, size=40), mat(700, 300, MAB, color='red'),
     T(6, 'c11 = 1·2 + 2·1 + 0·0 = 4,   c22 = 0·1 + 1·0 + 3·4 = 12', size=32))
beat(p, '''The transpose swaps rows and columns. Matrix multiplication is not commutative: A B is usually not equal to B A. The identity matrix has ones on the diagonal.''',
     T(7, '(A^T)_ij = A_ji   ·   AB ≠ BA (usually)   ·   AI = IA = A', size=32))
beat(p, '''A zero one matrix has only zeros and ones. The join is OR, entry by entry, and the meet is AND. The Boolean product is like multiplication, but uses AND for times and OR for plus.
These matrices are used to represent relations.''',
     T(9, '[h:Zero-one matrix]: join (∨), meet (∧), Boolean product ⊙ (AND inside, OR outside)', size=31),
     mat(240, 760, Z1), T(0, '⊙', x=450, y=820, size=40), mat(500, 736, Z2), T(0, '=', x=650, y=820, size=40), mat(700, 760, ZB, color='red'),
     T(0, '(1∧1) ∨ (0∧0) ∨ (1∧1) = 1', x=900, y=820, size=30, color='green'))

# ===================================================================================== CH 6
p = chapter(6)
beat(p, 'Chapter six. Relations.')

R1 = [(1, 1), (1, 2), (2, 1), (2, 2), (3, 3)]; pr = props(R1, [1, 2, 3])
p = page('Relations & Their Properties', 6)
beat(p, '''A relation from A to B is any subset of A cross B. A relation on A is a subset of A cross A. If A has n elements, there are two to the power n squared relations on A.''',
     T(0, '[h:Relation] R ⊆ A × B;   on A: R ⊆ A × A;   number of relations on A = 2^(n²)', size=33))
beat(p, '''Four properties. Reflexive: every a is related to itself. Symmetric: if a is related to b, then b is related to a. Antisymmetric: if a is related to b and b to a, then a equals b.
Transitive: if a is related to b and b to c, then a is related to c.''',
     Stamp(1650, 140, 'MOST ASKED'),
     Tab(180, 330, [290, 640, 480], 54, [['Property', 'Condition', 'Example'], ['[h:Reflexive]', '(a, a) ∈ R for every a', '≤ on integers'], ['[h:Symmetric]', '(a, b) ∈ R => (b, a) ∈ R', '"is sibling of"'],
         ['[h:Antisymmetric]', '(a, b), (b, a) ∈ R => a = b', '≤,  divides'], ['[h:Transitive]', '(a, b), (b, c) ∈ R => (a, c) ∈ R', '<,  ≤,  divides']], size=29))
beat(p, f'''Check this relation on one, two, three. Every element is related to itself, so it is reflexive. Every pair has its reverse, so it is symmetric. And it is transitive.
It is not antisymmetric, because one is related to two and two to one. A relation that is reflexive, symmetric and transitive is called an equivalence relation.''',
     T(10, 'A = {1, 2, 3},  R = {(1,1), (1,2), (2,1), (2,2), (3,3)}', size=34, color='black'),
     T(11, 'reflexive ' + ('[g:✓]' if pr['reflexive'] else '[r:✗]') + '   symmetric ' + ('[g:✓]' if pr['symmetric'] else '[r:✗]') + '   antisymmetric ' + ('[g:✓]' if pr['antisymmetric'] else '[r:✗]') +
       '   transitive ' + ('[g:✓]' if pr['transitive'] else '[r:✗]'), size=34),
     T(12, 'reflexive + symmetric + transitive = [h:equivalence relation]', size=34, color='red'))

WS = warshall([(1, 2), (2, 3), (3, 4), (2, 1)], [1, 2, 3, 4])
p = page("Representing Relations & Warshall's Algorithm", 6)
dg = {1: (1200, 330), 2: (1420, 330), 3: (1420, 490), 4: (1200, 490)}
beat(p, '''A relation can be shown as a zero one matrix, with a one in row a, column b when a is related to b, or as a directed graph, with an arrow from a to b.
Here is the relation one two, two three, three four, and two one.''',
     T(0, 'R = {(1,2), (2,3), (3,4), (2,1)} on {1, 2, 3, 4}', size=34, color='black'), T(1, 'matrix M_R:  m_ij = 1 if (i, j) ∈ R', size=32), mat(260, 300, WS[0], cw=56, rh=46),
     *[Node(dg[k], str(k)) for k in dg], Arr(1236, 318, 1384, 318), Arr(1384, 344, 1236, 344), Arr(1420, 366, 1420, 452), Arr(1384, 490, 1236, 490))
beat(p, '''The transitive closure is the smallest transitive relation that contains R. Warshall's algorithm finds it. For each k from one to n, if there is a path from i to k and from k to j, put a one at i, j.''',
     Stamp(1650, 140, 'NUMERICAL'), T(7, "[h:Warshall]: W_k[i][j] = W_(k-1)[i][j] ∨ (W_(k-1)[i][k] ∧ W_(k-1)[k][j])", size=31))
beat(p, '''Running it for k equals one, two, three and four, we get these matrices. The final matrix shows that one and two can reach everything, three reaches only four, and four reaches nothing.''',
     *sum([[T(0, f'W{k}', x=180 + 300 * (k - 1), y=L(8) + 40, size=30, color='red'), mat(180 + 300 * (k - 1), L(8) + 60, WS[k], cw=56, rh=44, size=28, color='green' if k == 4 else 'black')]
           for k in range(1, 5)], []))

D12, cov = hasse(12)
hp = {1: (1450, 900), 2: (1320, 760), 3: (1600, 760), 4: (1200, 620), 6: (1460, 620), 12: (1330, 480)}
p = page('Equivalence Relations & Partial Orders', 6)
beat(p, '''An equivalence relation splits the set into equivalence classes, which do not overlap. For example, congruence mod three on the integers has three classes: remainder zero, remainder one, and remainder two.''',
     T(0, '[h:Equivalence classes] partition the set', size=36), T(1, 'a ≡ b (mod 3):  [0] = {..., -3, 0, 3, 6, ...}', size=32), T(2, '[1] = {..., -2, 1, 4, 7, ...}    [2] = {..., -1, 2, 5, 8, ...}', size=32))
beat(p, '''A partial order is reflexive, antisymmetric and transitive. A set with a partial order is called a poset. For example, the divisors of twelve under "divides".
A Hasse diagram draws it simply: drop the self loops, drop the arrows implied by transitivity, and put larger elements higher.''',
     Stamp(1650, 140, 'MOST ASKED'), T(4, '[h:Partial order]: reflexive + antisymmetric + transitive (poset)', size=33),
     T(5, 'Hasse diagram: no loops, no transitive edges, bigger = higher', size=32),
     *[Ln([(hp[a][0], hp[a][1] - 30), (hp[b][0], hp[b][1] + 30)], 'black', 3) for a, b in cov], *[Node(hp[d], str(d), r=30, color='blue') for d in D12],
     T(0, 'D12 under "divides"', x=1500, y=470, size=28, color='green'))
beat(p, '''In a poset, the least upper bound of two elements is the smallest element above both, and the greatest lower bound is the largest element below both. For four and six, the least upper bound is twelve,
and the greatest lower bound is two. If every pair has both, the poset is called a lattice. So D twelve is a lattice.''',
     T(8, 'LUB(4, 6) = [h:12] (lcm)   ·   GLB(4, 6) = [h:2] (gcd)', size=32), T(9, 'every pair has LUB & GLB  =>  [k:lattice]', size=32),
     T(10, 'maximal = 12, minimal = 1 (greatest & least elements)', size=30, color='green'))

# ===================================================================================== CH 7
p = chapter(7)
beat(p, 'Chapter seven. Number theory part one. Divisibility, modular arithmetic, and number systems.')

q1, r1 = divmod_pos(101, 11); q2, r2 = divmod_pos(-11, 3)
p = page('Divisibility & Modular Arithmetic', 7)
beat(p, '''a divides b, written a bar b, if b equals a times some integer. For example, three divides twelve, but three does not divide seven. If a divides b and a divides c, then a divides b plus c.''',
     T(0, '[h:a | b]  <=>  b = a·k for some integer k;   3 | 12,  3 ∤ 7', size=36), T(1, 'a | b and a | c  =>  a | (b + c);   a | b  =>  a | bc', size=34))
beat(p, f'''The division algorithm says: for any integer a and positive d, there are unique q and r with a equals d q plus r, where r is between zero and d minus one.
For one hundred and one divided by eleven, q is nine and r is two. For minus eleven divided by three, q is minus four and r is one, because the remainder can never be negative.''',
     Stamp(1650, 140, 'MOST ASKED'), T(3, '[h:Division algorithm]: a = d·q + r,   0 ≤ r < d', size=38, color='red'),
     T(4, f'101 = 11 × {q1} + {r1}   =>   q = {q1}, r = {r1}', size=34), T(5, f'-11 = 3 × ({q2}) + {r2}   =>   q = {q2}, r = {r2}   (r is never negative)', size=34))
beat(p, f'''a mod m is the remainder when a is divided by m. So seventeen mod five is two, and minus one thirty three mod nine is two. We say a is congruent to b mod m if m divides a minus b.
For example, seventeen is congruent to five mod six. Congruences can be added and multiplied like equations.''',
     T(7, f'[k:a mod m] = remainder:  17 mod 5 = {17 % 5},   -133 mod 9 = {-133 % 9}', size=34), T(8, '[h:a ≡ b (mod m)]  <=>  m | (a - b);   17 ≡ 5 (mod 6)', size=36),
     T(9, 'a ≡ b, c ≡ d (mod m)  =>  a + c ≡ b + d,   ac ≡ bd (mod m)', size=34),
     T(11, 'Uses: hashing h(k) = k mod m, check digits, pseudo-random numbers, cryptography', size=30, color='green'))

b2, st2 = to_base(241, 2)
p = page('Integer Representations', 7)
beat(p, '''Computers store numbers in binary, base two. To convert a decimal number to base b, keep dividing by b and write down the remainders. Then read the remainders from bottom to top.
For two hundred and forty one: divide by two again and again. Reading the remainders upwards gives one one one one zero zero zero one.''',
     Stamp(1650, 140, 'NUMERICAL'), T(0, 'decimal -> base b: divide by b, read remainders [h:bottom to top]', size=34),
     Tab(180, 300, [180, 180, 200], 46, [['n', 'n / 2', 'remainder']] + [[str(n), str(q), f'[r:{r}]'] for n, q, r in st2], size=28),
     Arr(800, 700, 800, 330, 'red'), T(0, 'read up', x=760, y=310, size=26, color='red'), T(0, f'241 = ([h:{b2}])₂', x=900, y=520, size=40, color='black'))
beat(p, f'''To convert binary to octal, group the bits in threes from the right. For hexadecimal, group them in fours. So two hundred and forty one is F one in hexadecimal. And twelve thousand three hundred and forty five
is three zero zero seven one in octal. To go back to decimal, multiply each digit by the power of the base and add.''',
     T(0, '[k:binary -> hex]: groups of 4 bits;  binary -> octal: groups of 3', x=900, y=L(8), size=30),
     M(900, L(9) + 6, '1111 0001 = F1 (hex)', size=32, color='blue'), T(0, f'(12345)₁₀ = ({to_base(12345, 8)[0]})₈', x=900, y=L(10) + 6, size=32),
     T(0, '(F1)₁₆ = 15·16 + 1 = 241', x=900, y=L(11) + 6, size=32, color='green'))

me, mrows = mod_exp(3, 644, 645)
p = page('Modular Exponentiation', 7)
beat(p, '''Exam question: find three to the power six hundred and forty four, mod six hundred and forty five. We cannot compute the huge power directly. Instead, use fast modular exponentiation.
Write six forty four in binary: one zero one zero zero zero zero one zero zero. Then keep squaring three mod six forty five, and multiply into x only where the bit is one.''',
     Stamp(1650, 140, 'NUMERICAL'), T(0, 'Find 3^644 mod 645;   644 = (1010000100)₂', size=36, color='black'),
     T(1, 'power = power² mod 645 each step;   if bit = 1: x = x · power mod 645', size=32))
beat(p, f'''Here is the table. The bits are read from the right. Where the bit is one, at steps two, seven and nine, we multiply. The final answer is thirty six.''',
     Tab(180, 330, [130, 130, 220, 280], 46, [['i', 'bit', 'x', 'power']] + [[str(i), f'[r:{b}]' if b == '1' else b, str(x), str(pw)] for i, b, x, pw in mrows], size=27),
     T(0, f'3^644 mod 645 = [h:{me}]', x=1060, y=600, size=44, color='red'), T(0, 'only ~10 squarings instead of 643 multiplications', x=1060, y=670, size=28, color='green'))

# ===================================================================================== CH 8
p = chapter(8)
beat(p, 'Chapter eight. Number theory part two. Primes, G C D, and congruences.')

p = page('Primes & Prime Factorization', 8)
beat(p, '''A prime is an integer greater than one whose only positive divisors are one and itself. A number greater than one that is not prime is composite.
The fundamental theorem of arithmetic says every integer greater than one can be written as a product of primes in exactly one way. For example, one hundred is two squared times five squared,
and nine hundred ninety nine is three cubed times thirty seven.''',
     T(0, '[h:Prime]: > 1, divisors only 1 and itself;   2, 3, 5, 7, 11, ...', size=34), T(1, '[k:Fundamental theorem]: unique product of primes', size=34),
     T(2, '100 = 2² · 5²     999 = 3³ · 37     1024 = 2^10', size=36, color='black'))
beat(p, '''To test if n is prime, we only need to check prime divisors up to the square root of n. For one hundred and one, the square root is about ten, and two, three, five and seven do not divide it, so it is prime.
The sieve of Eratosthenes finds all primes up to n by crossing out multiples. There are infinitely many primes.''',
     Stamp(1650, 140), T(4, 'n composite  =>  it has a prime factor ≤ √n', size=34, color='red'), T(5, '101: √101 ≈ 10;  2, 3, 5, 7 ∤ 101  =>  [h:prime]', size=34),
     T(6, 'Primes ≤ 50 (sieve): ' + ', '.join(map(str, sieve(50))), size=30, color='black'), T(7, 'infinitely many primes (Euclid)', size=32, color='green'))
beat(p, '''Two numbers are relatively prime if their greatest common divisor is one, like eight and fifteen. The G C D times the L C M equals the product of the two numbers.''',
     T(9, '[k:relatively prime]: gcd(a, b) = 1, e.g. 8 and 15', size=34), T(10, '[h:gcd(a, b) × lcm(a, b) = a × b]', size=36, color='red'))

g, est = euclid(662, 414); gg, xs, ys = ext_gcd(252, 198)
p = page('GCD: Euclidean Algorithm', 8)
beat(p, '''The Euclidean algorithm finds the G C D quickly. It uses the fact that G C D of a and b equals G C D of b and a mod b. Keep dividing until the remainder is zero. The last non zero remainder is the G C D.
Example: G C D of six hundred sixty two and four hundred fourteen.''',
     Stamp(1650, 140, 'MOST ASKED'), T(0, '[h:gcd(a, b) = gcd(b, a mod b)];  stop when remainder = 0', size=36), T(1, 'gcd(662, 414) = ?', size=36, color='black'))
beat(p, f'''Six sixty two equals four fourteen times one plus two forty eight. Four fourteen equals two forty eight times one plus one sixty six. Two forty eight equals one sixty six times one plus eighty two.
One sixty six equals eighty two times two plus two. And eighty two equals two times forty one, remainder zero. So the G C D is two, and the L C M is six sixty two times four fourteen divided by two.''',
     *[T(3 + i, f'{a} = {b} × {q} + {r}', size=34, color='red' if r == 0 else 'blue') for i, (a, b, q, r) in enumerate(est)],
     T(9, f'gcd(662, 414) = [h:{g}]     lcm = 662 × 414 / 2 = [h:{662 * 414 // g:,}]', size=36, color='black'))
beat(p, f'''Bezout's theorem says the G C D can be written as s times a plus t times b, for some integers s and t. Working backwards through the Euclidean steps, G C D of two fifty two and one ninety eight,
which is eighteen, equals four times two fifty two minus five times one ninety eight.''',
     T(11, "[k:Bézout]: gcd(a, b) = s·a + t·b", size=34), T(12, f'gcd(252, 198) = {gg} = {xs} × 252 - {-ys} × 198', size=34, color='red'))

inv3 = inverse(3, 7); xcrt, Mc, parts = crt([2, 3, 2], [3, 5, 7])
p = page('Linear Congruences & CRT', 8)
beat(p, f'''A linear congruence looks like a x is congruent to b mod m. If G C D of a and m is one, a has an inverse mod m, a number that gives one when multiplied by a.
Solve three x congruent to four mod seven. The inverse of three mod seven is five, because three times five is fifteen, which is one mod seven. Multiply both sides by five: x is congruent to twenty, which is six mod seven.''',
     Stamp(1650, 140, 'NUMERICAL'), T(0, '[h:ax ≡ b (mod m)]; inverse ā exists if gcd(a, m) = 1:  a·ā ≡ 1 (mod m)', size=32),
     T(1, f'3x ≡ 4 (mod 7):  3 × {inv3} = 15 ≡ 1  =>  inverse = {inv3}', size=34), T(2, f'x ≡ {inv3} × 4 = 20 ≡ [h:{20 % 7}] (mod 7)   check: 3 × 6 = 18 ≡ 4 ✓', size=34))
beat(p, '''The Chinese remainder theorem solves several congruences at once, when the moduli are pairwise relatively prime. The classic puzzle: x is two mod three, three mod five, and two mod seven.
M is three times five times seven, one hundred and five. For each modulus, M i is M divided by m i, and y i is the inverse of M i mod m i.''',
     T(4, '[h:CRT]: x ≡ a_i (mod m_i), m_i pairwise coprime  =>  unique x mod M = m1 m2 m3', size=31),
     T(5, 'x ≡ 2 (mod 3),  x ≡ 3 (mod 5),  x ≡ 2 (mod 7);   M = 105', size=34, color='black'),
     Tab(180, 540, [160, 160, 220, 200], 52, [['a_i', 'm_i', 'M_i = M/m_i', 'y_i = M_i⁻¹']] + [[str(a), str(m), str(Mi), str(yi)] for a, m, Mi, yi in parts], size=29))
beat(p, f'''Then x is the sum of a i times M i times y i, mod M. That is two times thirty five times two, plus three times twenty one times one, plus two times fifteen times one, which is two hundred and thirty three.
Mod one hundred and five, that is twenty three. Check: twenty three is two mod three, three mod five, and two mod seven.''',
     T(0, 'x = Σ a_i M_i y_i mod M', x=1000, y=L(6) + 30, size=32), T(0, '= 2·35·2 + 3·21·1 + 2·15·1', x=1000, y=L(7) + 30, size=32),
     T(0, f'= 233 ≡ [h:{xcrt}] (mod 105)', x=1000, y=L(8) + 30, size=36, color='red'), T(0, '23 = 3·7 + 2 = 5·4 + 3 = 7·3 + 2 ✓', x=1000, y=L(9) + 30, size=28, color='green'))

p = page("Fermat's Little Theorem", 8)
beat(p, '''Fermat's little theorem: if p is prime and p does not divide a, then a to the power p minus one is congruent to one mod p. This makes big powers easy.
Find seven to the power two hundred and twenty two, mod eleven. Since eleven is prime, seven to the power ten is one mod eleven.''',
     Stamp(1650, 140, 'NUMERICAL'), T(0, '[h:p prime, p ∤ a  =>  a^(p-1) ≡ 1 (mod p)]', size=38, color='red'), T(1, 'Find 7^222 mod 11', size=36, color='black'))
beat(p, f'''Two hundred and twenty two is ten times twenty two, plus two. So seven to the power two twenty two is, seven to the ten, to the power twenty two, times seven squared.
That is one times forty nine, and forty nine mod eleven is five. So the answer is five.''',
     T(3, '222 = 10 × 22 + 2', size=34), T(4, '7^222 = (7^10)^22 × 7² ≡ 1^22 × 49 (mod 11)', size=34), T(5, f'49 mod 11 = [h:{pow(7, 222, 11)}]', size=38, color='red'))
beat(p, '''Fermat's theorem is used in the R S A cryptosystem and in primality tests. A simple check: if a to the n minus one is not one mod n, then n is definitely not prime.''',
     T(7, 'Uses: RSA cryptography, primality testing', size=32, color='green'), T(8, 'a^(n-1) ≢ 1 (mod n)  =>  n is [r:not] prime', size=32))

# ===================================================================================== CH 9
p = chapter(9)
beat(p, 'Chapter nine. Induction and recursion. Every exam has an induction proof, so learn the format.')

p = page('Mathematical Induction', 9)
beat(p, '''Mathematical induction proves that P of n is true for all positive integers n. It has two steps. The basis step: prove P of one. The inductive step: assume P of k is true,
which is the inductive hypothesis, and prove P of k plus one. Like dominoes: the first falls, and each one knocks down the next.''',
     Stamp(1650, 140, 'MOST ASKED'), T(0, '[h:Basis]: prove P(1)   ·   [h:Inductive step]: P(k) => P(k + 1)', size=36), T(1, '(P(k) assumed true = inductive hypothesis)  -> like falling dominoes', size=32, color='green'))
beat(p, '''Example: prove that one plus three plus five, up to two n minus one, equals n squared. Basis: for n equals one, the left side is one and the right side is one squared. True.
Inductive step: assume the sum up to two k minus one is k squared. Add the next odd number, two k plus one. We get k squared plus two k plus one, which is k plus one, whole squared. So P of k plus one is true.''',
     S(3, 'Prove: 1 + 3 + 5 + ... + (2n - 1) = n²', size=36, color='red'),
     T(4, 'Basis: n = 1:  LHS = 1 = 1² = RHS ✓', size=34), T(5, 'Assume: 1 + 3 + ... + (2k - 1) = k²', size=34),
     T(6, 'Then: 1 + 3 + ... + (2k - 1) + (2k + 1) = k² + 2k + 1 = [h:(k + 1)²] ✓', size=34), T(7, 'By induction, true for all n ≥ 1  ∎', size=34, color='green'))
beat(p, '''Induction also proves divisibility. Prove n cubed minus n is divisible by three. Basis: n equals one gives zero, which is divisible. For the step, k plus one cubed minus k plus one equals
k cubed minus k, plus three k squared plus three k. The first part is divisible by three by the hypothesis, and the second part has a factor of three.''',
     S(9, 'Prove: 3 | n³ - n', size=36, color='red'), T(10, 'n = 1: 0 ✓;  (k + 1)³ - (k + 1) = (k³ - k) + 3(k² + k)', size=34), T(11, '= (divisible by 3) + 3(...)  =>  divisible by 3 ✓', size=34))

pst = postage()
p = page('Strong Induction & Well-Ordering', 9)
beat(p, '''In strong induction, the inductive step assumes P of every number up to k, not just P of k. It is useful when k plus one depends on a smaller case.
Example: every amount of postage of twelve rupees or more can be made using four rupee and five rupee stamps.''',
     Stamp(1650, 140), T(0, '[h:Strong induction]: assume P(1), P(2), ..., P(k)  =>  prove P(k + 1)', size=34),
     T(1, 'Prove: every amount ≥ 12 can be made with 4 and 5 stamps', size=34, color='black'))
beat(p, f'''Basis: check twelve, thirteen, fourteen and fifteen. Twelve is three fours. Thirteen is two fours and a five. Fourteen is one four and two fives. Fifteen is three fives.
Inductive step: for k plus one at least sixteen, k minus three is at least twelve, so it can be made. Add one more four rupee stamp. Done.''',
     *[T(3 + i, f'{a} = {f}×4 + {v}×5', size=34) for i, (a, (f, v)) in enumerate(list(pst.items())[:4])],
     T(7, 'k + 1 ≥ 16:  (k + 1) - 4 = k - 3 ≥ 12 → possible; add one 4-stamp ✓', size=32, color='red'))
beat(p, '''The well ordering principle says every non empty set of positive integers has a smallest element. It is the reason induction works.''',
     T(9, '[k:Well-ordering]: every non-empty set of positive integers has a least element', size=32), T(10, '(the foundation of induction)', size=30, color='green'))

rf = rec_f(4)
p = page('Recursive Definitions & Structural Induction', 9)
beat(p, f'''A recursive definition has a basis, which gives the first value, and a recursive step, which defines the next value from earlier ones. For example, f of zero equals three, and f of n plus one equals two f of n plus three.
Then f of one is nine, f of two is twenty one, f of three is forty five, and f of four is ninety three.''',
     Stamp(1650, 140, 'NUMERICAL'), T(0, 'Basis + recursive step', size=36), T(1, 'f(0) = 3,   f(n + 1) = 2 f(n) + 3', size=36, color='black'),
     T(2, '  '.join(f'f({i}) = [h:{v}]' for i, v in enumerate(rf)), size=34))
beat(p, '''Other examples: factorial, where zero factorial is one and n plus one factorial is n plus one times n factorial. And the Fibonacci numbers: f zero is zero, f one is one, and each term is the sum of the previous two.''',
     T(4, 'n! :  0! = 1,   (n + 1)! = (n + 1) · n!', size=34), T(5, 'Fibonacci: f0 = 0, f1 = 1, f_n = f_(n-1) + f_(n-2):  0, 1, 1, 2, 3, 5, 8, 13', size=32))
beat(p, '''Sets can also be defined recursively. For example: three is in S, and if x and y are in S, so is x plus y. This S is the set of all positive multiples of three.
To prove things about such sets, we use structural induction: prove it for the basis elements, then show the recursive step keeps the property.''',
     T(7, '[h:Recursive set]: 3 ∈ S;  x, y ∈ S  =>  x + y ∈ S   (S = multiples of 3)', size=32),
     T(8, '[k:Structural induction]: prove for basis elements, then for each recursive step', size=32),
     T(9, 'e.g. strings: λ ∈ Σ*;  w ∈ Σ*, x ∈ Σ  =>  wx ∈ Σ*', size=32, color='green'))

# ===================================================================================== CH 10
p = chapter(10)
beat(p, 'Chapter ten. Counting. Permutations, combinations and the pigeonhole principle are asked every single year.')

p = page('Sum & Product Rules', 10)
beat(p, '''The product rule: if a task has two steps, with m ways for the first and n ways for the second, the task can be done in m times n ways.
For example, a licence plate with three letters followed by three digits has twenty six cubed times ten cubed, which is one crore seventy five lakh seventy six thousand plates.''',
     Stamp(1650, 140, 'NUMERICAL'), T(0, '[h:Product rule]: step 1 in m ways, step 2 in n ways  =>  m × n', size=36),
     T(1, f'3 letters + 3 digits:  26³ × 10³ = [h:{26 ** 3 * 10 ** 3:,}]', size=34))
beat(p, '''The sum rule: if a task can be done in one of m ways or in one of n ways, with no overlap, there are m plus n ways. For example, choosing one project from thirty seven in one list or twenty three in another gives sixty choices.''',
     T(3, '[h:Sum rule]: m ways OR n ways (no overlap)  =>  m + n', size=36), T(4, 'pick 1 project from list A (37) or list B (23): 37 + 23 = 60', size=34))
beat(p, '''Combining them: how many bit strings of length eight are there? Each bit has two choices, so two to the power eight, two hundred and fifty six. And the subtraction rule says, if the two ways overlap,
subtract the overlap: that is the inclusion exclusion principle.''',
     T(6, 'bit strings of length 8:  2^8 = [h:256]', size=34), T(7, 'functions from m-set to n-set: n^m;   one-to-one: n(n - 1)...(n - m + 1)', size=32),
     T(8, '[k:Subtraction rule]: |A ∪ B| = |A| + |B| - |A ∩ B|', size=34))

p = page('Pigeonhole Principle', 10)
beat(p, '''The pigeonhole principle: if more than k objects are placed into k boxes, at least one box has two or more objects. For example, among thirteen people, at least two have their birthday in the same month.''',
     Stamp(1650, 140, 'MOST ASKED'), T(0, '[h:k + 1 objects into k boxes  =>  some box has ≥ 2]', size=38, color='red'), T(1, '13 people, 12 months  =>  2 share a birth month', size=34),
     *[Box(1260 + 120 * k, 380, 100, 90, None, 'blue') for k in range(4)], *[Ell(1285 + 120 * k, 400, 50, 50, None, 'red') for k in range(4)], Ell(1295, 330, 40, 40, None, 'red'),
     T(0, '5 pigeons, 4 holes', x=1310, y=520, size=28, color='green'))
beat(p, f'''The generalized pigeonhole principle: if N objects are placed in k boxes, some box has at least the ceiling of N over k objects. Among one hundred people, at least the ceiling of one hundred over twelve,
which is nine, were born in the same month.''',
     T(5, '[h:Generalized]: N objects, k boxes  =>  some box has ≥ ⌈N / k⌉', size=36), T(6, f'100 people  =>  ⌈100 / 12⌉ = [h:{math.ceil(100 / 12)}] share a month', size=34))
beat(p, '''A typical exam question: how many students must be in a class to make sure at least six get the same grade, if there are five grades? We need the ceiling of N over five to be at least six,
so N is five times five plus one, which is twenty six.''',
     T(8, 'At least 6 with the same grade (5 grades):  ⌈N/5⌉ ≥ 6', size=34, color='black'), T(9, 'N = 5 × 5 + 1 = [h:26]', size=36, color='red'),
     T(11, 'Pick 5 numbers from 1..8: two of them add up to 9 (pairs {1,8} {2,7} {3,6} {4,5})', size=30, color='green'))

bn, _ = multiset_perm('BANANA')
p = page('Permutations & Combinations', 10)
beat(p, '''A permutation is an ordered arrangement. The number of ways to arrange r objects out of n is P of n comma r, which is n factorial over n minus r factorial.
A combination is a selection where order does not matter. C of n comma r is n factorial over r factorial times n minus r factorial. For example, P of five comma three is sixty, and C of five comma three is ten.''',
     Stamp(1650, 140, 'NUMERICAL'), T(0, '[h:P(n, r) = n! / (n - r)!]   (order matters)', size=38), T(1, '[h:C(n, r) = n! / (r! (n - r)!)]   (order doesn\'t matter)', size=38),
     T(2, f'P(5, 3) = {math.perm(5, 3)},   C(5, 3) = {comb(5, 3)}', size=34, color='black'))
beat(p, f'''Examples. A committee of three men and two women from six men and five women: C of six comma three, times C of five comma two, which is twenty times ten, two hundred.
Arrangements of the letters of BANANA: six letters, with three A's and two N's, so six factorial over three factorial times two factorial, which is sixty.''',
     T(4, f'Committee: C(6, 3) × C(5, 2) = 20 × 10 = [h:{comb(6, 3) * comb(5, 2)}]', size=34),
     T(5, f'BANANA: 6! / (3! × 2!) = 720 / 12 = [h:{bn}]', size=34))
beat(p, f'''With repetition allowed: the number of ways to choose r items from n types is C of n plus r minus one comma r. This also counts solutions of x one plus x two plus x three equals ten, with each x at least zero:
C of twelve comma two, which is sixty six.''',
     T(7, '[k:With repetition]: C(n + r - 1, r)', size=36), T(8, f'x1 + x2 + x3 = 10, xi ≥ 0:  C(12, 2) = [h:{comb(12, 2)}]', size=34),
     Tab(180, 680, [440, 420, 420], 52, [['', 'repetition not allowed', 'repetition allowed'], ['order matters', 'P(n, r)', 'n^r'], ['order doesn\'t matter', 'C(n, r)', 'C(n + r - 1, r)']], size=29,
         colors={(1, 0): 'red', (2, 0): 'red'}))

sg, pa, tr, tot = incl_excl_div()
p = page('Binomial Theorem & Inclusion-Exclusion', 10)
beat(p, f'''The binomial theorem: x plus y to the power n is the sum of C of n comma k, times x to the n minus k, times y to the k. The coefficients form Pascal's triangle, using Pascal's identity:
C of n plus one comma k equals C of n comma k minus one plus C of n comma k. Example: the coefficient of x cubed in two x plus three, to the power five, is C of five comma three, times two cubed, times three squared, which is seven hundred and twenty.''',
     Stamp(1650, 140, 'MOST ASKED'), T(0, '[h:(x + y)^n = Σ C(n, k) x^(n-k) y^k]', size=38), T(1, "Pascal: C(n + 1, k) = C(n, k - 1) + C(n, k);   Σ C(n, k) = 2^n", size=32),
     T(2, f'coeff. of x³ in (2x + 3)^5 = C(5, 3) · 2³ · 3² = 10 · 8 · 9 = [h:{comb(5, 3) * 8 * 9}]', size=33),
     *[T(0, '  '.join(str(comb(n, k)) for k in range(n + 1)), x=1460 - 22 * n, y=L(4) + 46 * n, size=30, color='black') for n in range(6)])
beat(p, f'''Inclusion exclusion: how many integers from one to one thousand are divisible by three, five, or seven? Add the singles: three thirty three, two hundred, and one forty two. Subtract the pairs: sixty six, forty seven and twenty eight.
Add back the triple: nine. The answer is five hundred and forty three.''',
     T(10, '|A ∪ B ∪ C| = Σ|A| - Σ|A ∩ B| + |A ∩ B ∩ C|', size=34),
     T(11, f'1..1000 divisible by 3, 5 or 7:  {" + ".join(map(str, sg))} - {" - ".join(map(str, pa))} + {tr} = [h:{tot}]', size=32))
beat(p, f'''One more classic: derangements, where nobody gets their own item back. For four letters in four envelopes, the number of derangements is nine.''',
     T(13, f'Derangements D_n = n! (1 - 1/1! + 1/2! - ... ± 1/n!);   D_4 = [h:{derange(4)}]', size=32, color='green'))

# ===================================================================================== CH 11
p = chapter(11)
beat(p, 'Chapter eleven. Algebraic structures. This chapter is for universities that include groups in this subject.')

cy = cayley(4)
p = page('Groups & Algebraic Structures', 11)
beat(p, '''An algebraic structure is a set with one or more operations. A binary operation on G is closed if combining two elements of G gives an element of G.
A semigroup is closed and associative. A monoid is a semigroup with an identity element. A group is a monoid where every element has an inverse. And if the operation is also commutative, it is an abelian group.''',
     Stamp(1650, 140, 'MOST ASKED'),
     Tab(180, 260, [300, 200, 230, 200, 200, 260], 54, [['', 'Closure', 'Associative', 'Identity', 'Inverse', 'Commutative'], ['Semigroup', '✓', '✓', '', '', ''], ['Monoid', '✓', '✓', '✓', '', ''],
         ['[h:Group]', '✓', '✓', '✓', '✓', ''], ['Abelian group', '✓', '✓', '✓', '✓', '✓']], size=29, colors={(r, cc): 'green' for r in range(1, 5) for cc in range(1, 6)}),
     T(7, 'e.g. (ℕ, +): monoid (identity 0, no inverses)   ·   (ℤ, +): abelian group', size=32))
beat(p, '''Example: the integers mod four under addition mod four. Here is its Cayley table. Every row has each element exactly once. The identity is zero. The inverse of one is three, of two is two, and of three is one.
It is commutative, so it is an abelian group. It is also cyclic, because one generates every element: one, two, three, zero.''',
     Tab(1200, 600, [90] * 5, 52, [['+₄', '0', '1', '2', '3']] + [[str(a)] + [str(v) for v in cy[a]] for a in range(4)], size=30, colors={(r, 0): 'red' for r in range(1, 5)}),
     T(9, '(ℤ4, +₄): identity 0;  inverses 1 ↔ 3, 2 ↔ 2', size=32), T(10, 'abelian ✓   [k:cyclic]: generated by 1 (and 3)', size=32), T(11, 'order of 2 = 2;  order of 1 = 4', size=32))

p = page('Subgroups, Lagrange & Homomorphism', 11)
beat(p, f'''A subgroup is a subset H of a group that is itself a group under the same operation. A quick test: H is non empty, and for all a and b in H, a times b inverse is in H.
Lagrange's theorem: the order of a subgroup divides the order of the group. The subgroups of Z four are: zero alone, zero and two, and the whole group, with orders one, two and four.''',
     Stamp(1650, 140), T(0, '[h:Subgroup H]: H ≠ ∅,  a, b ∈ H  =>  a·b⁻¹ ∈ H', size=36), T(1, '[h:Lagrange]: |H| divides |G|', size=38, color='red'),
     T(2, 'Subgroups of ℤ4: ' + ',   '.join('{' + ', '.join(map(str, s)) + '}' for s in subgroups_zn(4)) + '   (orders 1, 2, 4)', size=32))
beat(p, '''So a group of prime order has no proper subgroups other than the identity, and it must be cyclic. And the order of every element divides the order of the group.''',
     T(4, 'group of prime order  =>  cyclic;   order of element | |G|', size=34))
beat(p, '''A homomorphism is a function f from group G to group H that keeps the operation: f of a times b equals f of a times f of b. If f is also a bijection, it is called an isomorphism, and the two groups have the same structure.
For example, f of n equals n mod four, from the integers to Z four, is a homomorphism. Also remember: a ring has two operations, like addition and multiplication of integers.''',
     T(6, '[h:Homomorphism]: f(a * b) = f(a) ∘ f(b)', size=36), T(7, 'bijective homomorphism = [k:isomorphism] (same structure)', size=34),
     T(8, 'f(n) = n mod 4 : (ℤ, +) -> (ℤ4, +₄) is a homomorphism', size=32), T(9, '[k:Ring]: (R, +, ×); abelian group under +, associative ×, distributive', size=32, color='green'))

# ===================================================================================== CH 12
p = chapter(12)
beat(p, 'Chapter twelve. Recurrence relations. This chapter is for universities that include them.')

r1 = run_rec(5, -6, 1, 4); r2 = run_rec(6, -9, 1, 6)
p = page('Solving Recurrence Relations', 12)
beat(p, '''A recurrence relation defines each term using earlier terms, like a n equals five a n minus one minus six a n minus two. For linear homogeneous recurrences with constant coefficients, we use the characteristic equation.
Replace a n with r to the power n, which gives r squared minus five r plus six equals zero. The roots are two and three.''',
     Stamp(1650, 140, 'NUMERICAL'), T(0, 'a_n = 5a_(n-1) - 6a_(n-2),   a0 = 1,  a1 = 4', size=36, color='black'),
     T(1, 'characteristic eq.:  r² - 5r + 6 = 0  =>  r = 2, 3', size=36))
beat(p, f'''For distinct roots, a n equals c one times two to the n, plus c two times three to the n. Use the initial values. From a zero, c one plus c two equals one. From a one, two c one plus three c two equals four.
Solving, c two is two and c one is minus one. So a n equals two times three to the n, minus two to the n. Check: a two is five times four minus six, fourteen, and the formula gives eighteen minus four, fourteen.''',
     T(3, '[h:distinct roots]:  a_n = c1·2^n + c2·3^n', size=34), T(4, 'a0: c1 + c2 = 1     a1: 2c1 + 3c2 = 4   =>  c2 = 2, c1 = -1', size=34),
     T(5, 'a_n = [h:2·3^n - 2^n]', size=38, color='red'), T(6, f'check: a2 = 5·4 - 6·1 = {r1[2]};  2·9 - 4 = {2 * 9 - 4} ✓', size=32, color='green'))
beat(p, f'''For a repeated root, multiply by n. Example: a n equals six a n minus one minus nine a n minus two, with a zero equals one and a one equals six. The characteristic equation has the double root three.
So a n equals c one plus c two n, times three to the n. From the initial values, c one is one and c two is one. So a n equals one plus n, times three to the n.''',
     T(8, 'a_n = 6a_(n-1) - 9a_(n-2),  a0 = 1, a1 = 6:   (r - 3)² = 0', size=34, color='black'), T(9, '[h:repeated root]:  a_n = (c1 + c2·n) 3^n', size=34),
     T(10, 'a0: c1 = 1;   a1: 3(1 + c2) = 6  =>  c2 = 1', size=34), T(11, f'a_n = [h:(1 + n) 3^n]     check a2 = {r2[2]} = 3 · 9 ✓', size=36, color='red'))

nh = [1]; [nh.append(3 * nh[-1] + 2 ** k) for k in range(1, 5)]
p = page('Non-homogeneous Recurrences & Generating Functions', 12)
beat(p, f'''For a non homogeneous recurrence, the answer is the homogeneous solution plus a particular solution. Example: a n equals three a n minus one plus two to the n, with a zero equals one.
The homogeneous part gives c times three to the n. Try a particular solution A times two to the n. Substituting gives A equals minus two. So a n equals c times three to the n, minus two to the n plus one.
From a zero equals one, c is three. So a n equals three to the n plus one, minus two to the n plus one.''',
     Stamp(1650, 140, 'NUMERICAL'), T(0, 'a_n = 3a_(n-1) + 2^n,   a0 = 1', size=36, color='black'),
     T(1, 'homogeneous: c·3^n;   particular: try A·2^n', size=34), T(2, 'A·2^n = 3A·2^(n-1) + 2^n  =>  A = 3A/2 + 1  =>  A = -2', size=34),
     T(3, f'a_n = c·3^n - 2^(n+1);  a0 = 1 => c = 3  =>  [h:a_n = 3^(n+1) - 2^(n+1)]', size=34, color='red'),
     T(4, f'check: a1 = 3·1 + 2 = {nh[1]};  9 - 4 = {9 - 4} ✓', size=32, color='green'))
beat(p, '''A generating function turns a sequence into a power series: G of x is the sum of a k times x to the k. The most important one is one over one minus a x, which equals the sum of a to the k, x to the k.''',
     T(6, '[h:G(x) = Σ a_k x^k]', size=38), T(7, '1/(1 - x) = Σ x^k     1/(1 - ax) = Σ a^k x^k     1/(1 - x)² = Σ (k + 1) x^k', size=32, color='black'))
beat(p, '''Example: solve a k equals three a k minus one, with a zero equals two, using generating functions. G of x minus three x G of x equals two, because all the other terms cancel. So G of x equals two over one minus three x,
and a k equals two times three to the k.''',
     T(9, 'a_k = 3a_(k-1), a0 = 2:   G(x) - 3x·G(x) = a0 = 2', size=34), T(10, 'G(x) = 2 / (1 - 3x) = 2 Σ 3^k x^k   =>   [h:a_k = 2·3^k]', size=34, color='red'))

# ===================================================================================== CH 13
p = chapter(13)
beat(p, 'Chapter thirteen. Graph theory and trees. This chapter is for universities that include graphs in this subject.')

gb = {'a': (1180, 380), 'b': (1440, 340), 'c': (1640, 520), 'd': (1420, 700), 'e': (1160, 640)}
gbe = [('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'e'), ('e', 'a'), ('b', 'd')]
deg = {v: sum(v in e for e in gbe) for v in gb}
p = page('Graph Basics & Handshaking Lemma', 13)
beat(p, '''A graph G is a set of vertices V and a set of edges E. The degree of a vertex is the number of edges touching it. In this graph, b and d have degree three, and the others have degree two.''',
     T(0, '[h:G = (V, E)];  degree = number of edges at a vertex', size=36),
     *sum([WEdge(gb[a], gb[b]) for a, b in gbe], []), *[Node(gb[v], v) for v in gb], *[T(0, str(deg[v]), x=gb[v][0] + 60 * (gb[v][0] - 1400) / math.hypot(gb[v][0] - 1400, gb[v][1] - 520) - 7, y=gb[v][1] + 60 * (gb[v][1] - 520) / math.hypot(gb[v][0] - 1400, gb[v][1] - 520) + 9, size=26, color='red') for v in gb])
beat(p, f'''The handshaking lemma: the sum of all degrees equals twice the number of edges, because each edge adds two to the total. Here the degrees add up to twelve, so there are six edges.
A result: the number of vertices with odd degree is always even.''',
     Stamp(1650, 140, 'MOST ASKED'), T(2, '[h:Σ deg(v) = 2|E|]', size=40, color='red'), T(3, f'{" + ".join(str(deg[v]) for v in gb)} = {sum(deg.values())} = 2 × {len(gbe)} ✓', size=34),
     T(4, 'number of odd-degree vertices is [r:even]', size=34))
beat(p, '''Special graphs. The complete graph K n has every pair joined, so it has n into n minus one by two edges. A cycle C n is a ring. A bipartite graph splits its vertices into two sets, with edges only between the sets.
K m comma n has m times n edges. Graphs are stored as an adjacency matrix or adjacency lists. Two graphs are isomorphic if one can be relabelled to give the other. They must have the same number of vertices, edges and degrees.''',
     T(6, '[k:K_n]: n(n - 1)/2 edges   ·   [k:C_n]: cycle   ·   [k:K_m,n]: m × n edges', size=32),
     T(7, 'adjacency matrix / adjacency list', size=32),
     T(8, '[k:Isomorphic]: same structure; need same |V|, |E|, degree sequence', size=32))

p = page('Euler & Hamiltonian Graphs', 13)
beat(p, '''An Euler circuit uses every edge exactly once and returns to the start. A connected graph has an Euler circuit if and only if every vertex has even degree. It has an Euler path, which need not return,
if and only if it has exactly zero or two vertices of odd degree. This solves the famous Königsberg bridges problem, which has four odd vertices, so no walk is possible.''',
     Stamp(1650, 140, 'MOST ASKED'), T(0, '[h:Euler circuit]: every [r:edge] once, back to start  <=>  all degrees even', size=34),
     T(1, '[h:Euler path]: exactly 0 or 2 odd-degree vertices', size=34), T(2, 'Königsberg: 4 odd vertices  =>  no Euler path', size=32, color='green'),
     T(4, 'Our graph: deg(b) = deg(d) = 3 (two odd)  =>  Euler path from b to d ✓', size=32))
beat(p, '''A Hamiltonian circuit visits every vertex exactly once and returns to the start. There is no simple test. But Dirac's theorem says: if a graph has n at least three vertices,
and every vertex has degree at least n over two, then it has a Hamiltonian circuit.''',
     T(6, '[h:Hamiltonian circuit]: every [r:vertex] once, back to start', size=34), T(7, "[k:Dirac]: n ≥ 3 and every deg(v) ≥ n/2  =>  Hamiltonian", size=34),
     T(8, "[k:Ore]: deg(u) + deg(v) ≥ n for non-adjacent u, v  =>  Hamiltonian", size=32))
beat(p, '''Remember the difference with one word. Euler is about edges. Hamilton is about vertices.''',
     Tab(180, 720, [360, 520, 520], 54, [['', 'Euler', 'Hamilton'], ['visits every', 'edge once', 'vertex once'], ['simple test?', 'yes (degrees)', 'no (NP-complete)']], size=30,
         colors={(r, 0): 'red' for r in range(1, 3)}))

k4 = {'1': (1300, 380), '2': (1120, 700), '3': (1480, 700), '4': (1300, 590)}
p = page('Planar Graphs & Graph Colouring', 13)
beat(p, '''A planar graph can be drawn without any edges crossing. For a connected planar graph, Euler's formula says vertices minus edges plus faces equals two. For a simple planar graph with at least three vertices,
edges is at most three times vertices minus six. K five has ten edges, but three times five minus six is nine, so K five is not planar. K three comma three is also not planar.''',
     Stamp(1650, 140, 'MOST ASKED'), T(0, '[h:Euler\'s formula]: V - E + F = 2', size=38, color='red'), T(1, 'simple planar, V ≥ 3:  E ≤ 3V - 6', size=34),
     T(2, 'K5: E = 10 > 3·5 - 6 = 9  =>  [r:not planar];  K3,3: E = 9 > 2·6 - 4 = 8 => [r:not planar]', size=30),
     T(3, '[k:Kuratowski]: planar <=> no subdivision of K5 or K3,3', size=30, color='green'))
beat(p, '''Graph colouring gives each vertex a colour so that joined vertices get different colours. The smallest number of colours needed is the chromatic number. K n needs n colours. A bipartite graph needs two.
An even cycle needs two, and an odd cycle needs three. The four colour theorem says every planar graph needs at most four colours. Here K four, drawn without crossings, needs four colours.''',
     *sum([WEdge(k4[a], k4[b]) for a, b in [('1', '2'), ('1', '3'), ('2', '3'), ('1', '4'), ('2', '4'), ('3', '4')]], []),
     *[Node(k4[v], v, color=c) for v, c in zip('1234', ('blue', 'red', 'green', 'black'))],
     T(5, '[h:Chromatic number χ(G)]: fewest colours, neighbours differ', size=34),
     T(6, 'χ(K_n) = n · bipartite = 2 · even cycle = 2 · odd cycle = 3', size=32), T(7, '[k:Four colour theorem]: planar => χ ≤ 4', size=32),
     T(9, 'K4 (planar, F = 4): 4 - 6 + 4 = 2 ✓', size=32, color='green'))

E_ = [(4, 'A', 'B'), (2, 'A', 'C'), (1, 'B', 'C'), (5, 'B', 'D'), (8, 'C', 'D'), (10, 'C', 'E'), (2, 'D', 'E'), (6, 'B', 'E')]
kr = kruskal('ABCDE', E_); mst = [(a, b) for a, b, w, ok in kr if ok]
tp = {'A': (1160, 600), 'B': (1400, 400), 'C': (1400, 820), 'D': (1680, 400), 'E': (1780, 760)}
p = page('Trees & Minimum Spanning Tree', 13)
beat(p, '''A tree is a connected graph with no cycles. A tree with n vertices always has exactly n minus one edges, and there is exactly one path between any two vertices.
A spanning tree of a graph is a tree that includes all its vertices. By Cayley's formula, K n has n to the power n minus two spanning trees.''',
     T(0, '[h:Tree]: connected, no cycles;  n vertices => [r:n - 1 edges]', size=34), T(1, 'unique path between any two vertices', size=32),
     T(2, "Spanning tree: all vertices, no cycles;  K_n has n^(n-2) (Cayley)", size=32),
     *sum([WEdge(tp[a], tp[b], w, side=1) for w, a, b in E_], []), *[Node(tp[v], v) for v in tp])
beat(p, f'''A minimum spanning tree has the smallest total weight. Kruskal's algorithm sorts the edges by weight and adds the smallest edge that does not form a cycle. Here: B C with weight one, A C with two, D E with two.
A B with four would make a cycle, so skip it. Then B D with five. That is four edges for five vertices, so we stop. The total weight is ten.''',
     Stamp(1650, 140, 'NUMERICAL'),
     Tab(180, 380, [180, 140, 340], 50, [['Edge', 'w', 'Action']] + [[f'{a}{b}', str(w), '[g:add]' if ok else '[r:skip (cycle)]'] for a, b, w, ok in kr[:5]], size=29),
     *sum([WEdge(tp[a], tp[b], None, color='green', width=8) for a, b in mst], []), *[Node(tp[v], v) for v in tp],
     T(10, f'MST = {", ".join(a + b for a, b in mst)};  total = [h:{sum(w for a, b, w, ok in kr if ok)}]', size=34, color='red'))
beat(p, '''Prim's algorithm grows the tree from one vertex, always adding the cheapest edge that connects a new vertex. It gives the same total. And to visit all vertices, breadth first search goes level by level using a queue,
while depth first search goes as deep as possible using a stack.''',
     T(12, "[k:Prim]: grow from one vertex, cheapest edge to a new vertex", size=32), T(13, '[k:BFS]: level by level (queue)   ·   [k:DFS]: go deep first (stack)', size=32))

# ===================================================================================== CH 14
p = chapter(14)
beat(p, "Chapter fourteen. Exam revision. If you're short on time, revise this formula sheet first.")

p = page('Formula Sheet', 14)
beat(p, '''Logic: p implies q is the same as not p or q, and it is equal to its contrapositive. De Morgan's laws work for propositions, sets and quantifiers.''',
     Stamp(1650, 140, 'MOST ASKED'), T(0, 'p → q ≡ ¬p ∨ q ≡ ¬q → ¬p   ·   ¬(p ∧ q) ≡ ¬p ∨ ¬q   ·   ¬∀x P ≡ ∃x ¬P', size=32))
beat(p, '''Sets and functions: the power set has two to the n elements, and there are n to the m functions. The sums: n into n plus one by two, and for squares, n into n plus one into two n plus one by six.''',
     T(2, '|P(A)| = 2^n · |A × B| = |A||B| · functions = n^m · relations on A = 2^(n²)', size=31), T(3, 'Σk = n(n + 1)/2 · Σk² = n(n + 1)(2n + 1)/6 · GP: a(r^n - 1)/(r - 1)', size=31))
beat(p, '''Number theory: a equals d q plus r. G C D of a and b equals G C D of b and a mod b. G C D times L C M equals a times b. And Fermat: a to the p minus one is one mod p.''',
     T(5, 'a = dq + r (0 ≤ r < d) · gcd(a, b) = gcd(b, a mod b) · gcd × lcm = ab', size=31), T(6, 'Fermat: a^(p-1) ≡ 1 (mod p) · CRT: x = Σ a_i M_i y_i mod M', size=31))
beat(p, '''Counting: P of n comma r, C of n comma r, combinations with repetition, the pigeonhole ceiling, and inclusion exclusion. Graphs: the sum of degrees is twice the edges, V minus E plus F equals two, and a tree has n minus one edges.''',
     T(8, 'P(n, r) = n!/(n - r)! · C(n, r) = n!/(r!(n - r)!) · repetition: C(n + r - 1, r)', size=31), T(9, 'pigeonhole: ⌈N/k⌉ · |A ∪ B| = |A| + |B| - |A ∩ B|', size=31),
     T(11, 'Σ deg = 2|E| · V - E + F = 2 · E ≤ 3V - 6 · tree: n - 1 edges · K_n: n(n - 1)/2', size=31),
     T(12, 'recurrence: distinct roots c1 r1^n + c2 r2^n · repeated (c1 + c2 n) r^n', size=31))

p = page('Most Asked Exam Questions', 14)
qs = ['Truth table; tautology check', 'Prove equivalences with laws', 'PDNF & PCNF', 'Valid argument (rules of inference)', 'Quantifiers; proof by contradiction (√2)',
      'Venn diagram (3 sets); functions', 'Relation properties; Hasse diagram', 'Division algorithm; base conversion', 'Euclid GCD; linear congruence; CRT',
      'Induction proof (sum / divisibility)', 'Pigeonhole; permutations & combinations', 'Groups, recurrences, graphs (other univ.)']
beat(p, '''Here are the most asked questions. Truth tables and tautologies. Proving equivalences. P D N F and P C N F. And valid arguments using rules of inference.''', *[T(k, f'{k + 1}. {q}', x=200, size=34) for k, q in enumerate(qs[:4])])
beat(p, '''Quantifiers and proof by contradiction. Venn diagrams and functions. Relation properties and Hasse diagrams. And the division algorithm with base conversion.''',
     *[T(k, f'{k + 1}. {q}', x=200, size=34) for k, q in enumerate(qs) if 4 <= k < 8])
beat(p, '''Euclid's algorithm, linear congruences and the Chinese remainder theorem. Induction proofs. Pigeonhole, permutations and combinations. And for other universities, groups, recurrence relations and graphs.''',
     *[T(k, f'{k + 1}. {q}', x=200, size=34) for k, q in enumerate(qs) if k >= 8])
beat(p, '''One last exam tip. In every proof, write each step with its reason, like "by De Morgan's law" or "by the inductive hypothesis". Examiners give marks for the reasons, not just the answer.''',
     T(13, 'Tip: [h:write the reason for every step] => full marks!', color='red'))

p = page('All the Best!', 14, kind='outro')
beat(p, '''That's the complete mathematical foundations of computer science subject. If this helped you, share it with your friends who have the exam,
and subscribe to TechVibe24 for more one shot videos. Tell me in the comments which subject you want next. All the best for your exam!''')

if __name__ == '__main__':
    json.dump({'pages': PAGES, 'chapters': CHAPTERS}, open('mf_script.json', 'w'), indent=1, ensure_ascii=False)
    nb = sum(len(p['beats']) for p in PAGES); nw = sum(len(b['say'].split()) for p in PAGES for b in p['beats'])
    print('pages', len(PAGES), 'beats', nb, 'words', nw, 'est minutes', round(nw / 150, 1))
