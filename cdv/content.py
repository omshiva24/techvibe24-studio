'''Compiler Design one-shot: narration beats + handwritten note elements for every page.
Markup inside text: [r:red] [g:green] [k:black] [h:yellow highlight] [p:pink highlight]'''
import json
from cd_numericals import *

PAGES = []
def L(n): return 222 + 54 * n            # baseline of ruled line n (0..14)
def page(title, ch, kind='page', **kw): p = dict(kind=kind, title=title, ch=ch, beats=[], **kw); PAGES.append(p); return p
def beat(p, say, *els): p['beats'].append({'say': ' '.join(say.split()), 'els': [e for e in els if e]})
def T(n, s, x=180, size=38, font='body', color='blue', y=None): return dict(t='text', x=x, y=L(n) if y is None else y, s=s, size=size, font=font, color=color)
def S(n, s, x=180, color='black', size=42, y=None): return T(n, s, x, size, 'bold', color, y)
def N(n, k, s, x=180, color='blue', size=38): return T(n, f'{k}) {s}', x, size, 'body', color)
def Box(x, y, w, h, label=None, color='black', size=32, fill=None, lc=None): return dict(t='rect', x=x, y=y, w=w, h=h, label=label, color=color, size=size, fill=fill, lc=lc or color)
def Ell(x, y, w, h, label=None, color='black', size=32, fill=None, lc=None): return dict(t='ellipse', x=x, y=y, w=w, h=h, label=label, color=color, size=size, fill=fill, lc=lc or color)
def Arr(x1, y1, x2, y2, color='black', label=None, lx=0, ly=-14, curve=0, head=True, size=28, both=False, lc=None): return dict(t='arrow', p1=(x1, y1), p2=(x2, y2), color=color, label=label, lx=lx, ly=ly, curve=curve, head=head, size=size, both=both, lc=lc or color)
def Ln(pts, color='black', w=4): return dict(t='line', pts=pts, color=color, w=w)
def Tab(x, y, cw, rh, rows, color='black', size=30, hdr=True, order='row', colors=None): return dict(t='table', x=x, y=y, cw=cw, rh=rh, rows=rows, color=color, size=size, hdr=hdr, order=order, colors={f'{r},{c}': v for (r, c), v in (colors or {}).items()}, fills={})
def Stamp(x, y, text='IMP!', color='red', rot=-8, size=34): return dict(t='stamp', x=x, y=y, text=text, color=color, rot=rot, size=size)
def Tree(nodes, edges, w=70, h=56, size=28, head=False, ecol='black'):
    '''nodes: {name: (cx, cy, label, color[, w])}; edges: [(parent, child)] in drawing order. Each child is drawn right after its edge.'''
    import math
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
        out.append(Arr(round(x1), round(y1), round(x2), round(y2), head=head, color=ecol))
        if b not in done: out.append(ell(b)); done.add(b)
    return out

CHAPTERS = [
 (1, 'Introduction to Compilers', ['Language processors', 'Compiler vs interpreter', 'Phases of a compiler', 'Passes & bootstrapping'], 4),
 (2, 'Lexical Analysis', ['Tokens, lexemes, patterns', 'Input buffering', 'Regular expressions & finite automata', 'RE -> NFA -> DFA', 'LEX'], 5),
 (3, 'Grammars & Syntax Analysis', ['Context-free grammar', 'Derivations & parse trees', 'Ambiguity', 'Left recursion & left factoring', 'Error recovery'], 5),
 (4, 'Top-Down Parsing', ['Recursive descent', 'FIRST & FOLLOW', 'LL(1) parsing table', 'LL(1) parsing moves'], 5),
 (5, 'Bottom-Up Parsing', ['Shift-reduce parsing', 'Handles', 'LR(0) items', 'SLR table', 'CLR vs LALR'], 5),
 (6, 'Syntax-Directed Translation', ['SDD & attributes', 'S- and L-attributed', 'Annotated parse tree', 'YACC'], 4),
 (7, 'Intermediate Code', ['Syntax tree & postfix', 'Three-address code', 'Quadruples & triples'], 5),
 (8, 'Runtime Environment', ['Storage organisation', 'Activation record', 'Parameter passing', 'Symbol table'], 4),
 (9, 'Code Optimization', ['Basic blocks & flow graph', 'DAG', 'Optimisation techniques', 'Peephole', 'Data-flow analysis'], 5),
 (10, 'Code Generation', ['Issues in code generation', 'Simple code generator', 'Register allocation'], 4),
 (11, 'Exam Revision', ['Most asked questions', 'Last-minute tips'], 5),
]
def chapter(i):
    n, t, subs, stars = CHAPTERS[i - 1]
    return page(t, n, kind='chapter', num=n, subs=subs, stars=stars)

# =====================================================================================
p = page('Compiler Design', 0, kind='cover')
beat(p, '''Compiler Design. The complete subject, in one video. Simple explanations, handwritten notes,
and every important exam problem solved step by step.''')
beat(p, '''This works for B Tech computer science in almost every university. A K T U, Anna University, V T U, J N T U,
Mumbai, Pune, and private universities too. And it covers the Compiler Design part of GATE. So grab a pen, and let's start.''')

p = page('Contents', 0)
items = ['Introduction to Compilers', '[h:Lexical Analysis]  (RE -> DFA)', 'Grammars & Syntax Analysis', '[h:Top-Down Parsing]  (FIRST, FOLLOW, LL(1))',
         '[h:Bottom-Up Parsing]  (LR(0), SLR)', 'Syntax-Directed Translation', '[h:Intermediate Code]  (quadruples, triples)',
         'Runtime Environment', '[h:Code Optimization]  (basic blocks, DAG)', 'Code Generation', 'Exam Revision - most asked questions']
beat(p, "Here's our plan. Eleven chapters, from the basics to the exam numericals.", T(0, 'What we will cover today', x=180, size=42, font='bold', color='black'))
beat(p, '''We start with what a compiler is and its phases. Then lexical analysis, grammars, and the big scoring topics:
top down and bottom up parsing.''', *[T(1 + k, f'{k + 1}.  {items[k]}', x=200) for k in range(5)])
beat(p, '''After that, syntax directed translation, intermediate code, runtime environment, code optimization, and code generation.
And at the end, a quick revision of the most asked questions. The highlighted ones are the most important.''',
     *[T(6 + k, f'{k + 6}.  {items[k + 5]}', x=200) for k in range(6)], Stamp(1520, 520, 'MOST ASKED', rot=-10))

# ===================================================================================== CH 1
p = chapter(1)
beat(p, "Chapter one. Introduction to compilers. Let's build the basics first.")

p = page('What is a Compiler?', 1)
beat(p, '''A compiler is a program that translates a program written in a high level language, like C or Java,
into an equivalent program in a low level language, like assembly or machine code. While translating,
it also reports errors to the programmer.''',
     T(0, '[h:Compiler] = translates high-level program'), T(1, '-> equivalent low-level (machine / assembly) program'),
     T(2, '+ reports errors', color='red'),
     Box(1100, 200, 220, 90, 'source\nprogram', size=28), Box(1420, 200, 220, 90, 'Compiler', color='red', size=32),
     Box(1420, 330, 220, 80, 'target\nprogram', size=28), Box(1700, 200, 180, 90, 'error\nmessages', color='red', size=26),
     Arr(1320, 245, 1420, 245), Arr(1530, 290, 1530, 330), Arr(1640, 245, 1700, 245))
beat(p, '''Compiler versus interpreter. A compiler translates the whole program at once, and then you run the output.
It is fast to run, but errors are shown after the whole program is checked. An interpreter translates and runs line by line.
It is slower, but it is easier to debug. C and C plus plus use compilers. Python mostly uses an interpreter.''',
     Tab(180, 420, [300, 420, 420], 54, [['', 'Compiler', 'Interpreter'], ['translates', 'whole program at once', 'line by line'],
         ['speed', '[g:fast] execution', '[r:slower]'], ['errors', 'after full check', 'one at a time (easy debug)'], ['examples', 'C, C++', 'Python, JavaScript']], size=28),
     Stamp(1560, 760))
beat(p, '''Other language processors. A preprocessor handles things like macros and include files. An assembler converts
assembly to machine code. And the linker and loader join object files and load the program into memory.''',
     T(12, 'Preprocessor -> Compiler -> Assembler -> Linker / Loader', color='green'))

p = page('Phases of a Compiler', 1)
phases = ['Lexical Analyzer', 'Syntax Analyzer', 'Semantic Analyzer', 'Intermediate Code Gen.', 'Code Optimizer', 'Code Generator']
beat(p, '''The phases of a compiler. This is the most asked question in unit one, so learn this diagram.
There are six phases. Lexical analysis, syntax analysis, semantic analysis, intermediate code generation,
code optimization, and code generation.''',
     Stamp(1650, 140, 'MUST DRAW'), *[Box(640, 240 + k * 116, 420, 78, s, size=30, color='blue') for k, s in enumerate(phases)],
     *[Arr(850, 318 + k * 116, 850, 356 + k * 116) for k in range(5)],
     T(0, 'source program  ↓', x=760, y=228, size=26, color='green'), T(0, 'target program', x=770, y=975, size=26, color='green'),
     Arr(850, 898, 850, 945, color='green'))
beat(p, '''Two things are used by every phase. The symbol table, which stores information about identifiers,
and the error handler, which reports and recovers from errors.''',
     Box(1260, 400, 330, 110, 'Symbol table', color='red', size=32), Box(1260, 640, 330, 110, 'Error handler', color='red', size=32),
     Arr(1060, 455, 1260, 455, both=True), Arr(1060, 695, 1260, 695, both=True))
beat(p, '''The first part, lexical to intermediate code, is called the front end. It depends on the source language.
The optimizer and code generator form the back end, which depends on the target machine.''',
     T(0, '[k:Front end]: analysis', x=180, y=420, size=32), T(0, '(depends on language)', x=180, y=465, size=28, color='green'),
     T(0, '[k:Back end]: synthesis', x=180, y=800, size=32), T(0, '(depends on machine)', x=180, y=845, size=28, color='green'))

p = page('Phases - Example: position = initial + rate * 60', 1)
beat(p, '''Let's see the phases with the famous example. Position equals initial plus rate times sixty.
The lexical analyzer breaks it into tokens: id one, equals, id two, plus, id three, times, the number sixty.''',
     T(0, 'position = initial + rate * 60', color='black', size=40),
     T(1, '[r:Lexical]:  id1  =  id2  +  id3  *  60'))
beat(p, '''The syntax analyzer builds a syntax tree from these tokens. The semantic analyzer checks types.
Since rate is a float, it converts sixty to a float.''',
     T(2, '[r:Syntax]: builds the syntax tree'), T(3, '[r:Semantic]: type check -> inttofloat(60)'),
     Ell(1500, 220, 90, 70, '=', size=30), Ell(1340, 330, 110, 70, 'id1', size=26), Ell(1650, 330, 90, 70, '+', size=30),
     Ell(1520, 440, 110, 70, 'id2', size=26), Ell(1790, 440, 90, 70, '*', size=30), Ell(1660, 550, 110, 70, 'id3', size=26),
     Ell(1790, 550, 120, 70, '60', size=26, color='red'),
     Arr(1520, 285, 1410, 330, head=False), Arr(1570, 285, 1680, 330, head=False), Arr(1670, 395, 1590, 440, head=False),
     Arr(1720, 395, 1820, 440, head=False), Arr(1810, 505, 1720, 550, head=False), Arr(1840, 505, 1850, 550, head=False))
beat(p, '''Then intermediate code is generated in three address form. The optimizer removes the extra conversion and temporary.
And finally, the code generator produces machine code with registers.''',
     T(5, '[r:Intermediate]:  t1 = inttofloat(60);  t2 = id3 * t1;', size=34), T(6, 't3 = id2 + t2;  id1 = t3', x=470, size=34),
     T(7, '[r:Optimized]:  t1 = id3 * 60.0;  id1 = id2 + t1', size=34),
     T(8, '[r:Code]:  LDF R2, id3;  MULF R2, R2, #60.0;', size=34), T(9, 'LDF R1, id2;  ADDF R1, R1, R2;  STF id1, R1', x=310, size=34))

p = page('Passes, Bootstrapping & Cross Compiler', 1)
beat(p, '''A pass means reading the whole program once. A one pass compiler does everything in one reading, so it is fast,
but it uses more memory and can do less optimization. A multi pass compiler reads it several times, and produces better code.''',
     T(0, '[h:Pass] = one complete reading of the program'), T(1, '[k:One-pass]: fast, less optimisation'), T(2, '[k:Multi-pass]: slower, better code, less memory per pass'))
beat(p, '''Bootstrapping means writing a compiler in its own language. For example, writing a C compiler in C.
We first write a small compiler for a subset of the language, and then use it to compile a bigger version.
It is shown using T diagrams.''',
     T(4, '[h:Bootstrapping] = write a compiler in its own language'), T(5, 'small compiler for a subset -> compiles the full one', color='green'),
     Box(1250, 520, 330, 80, 'C   ->   M', size=32), Box(1355, 600, 120, 120, 'C', size=32), T(0, 'T-diagram', x=1350, y=780, size=28, color='green'))
beat(p, '''A cross compiler runs on one machine but produces code for another machine. For example, compiling on a laptop
for a mobile phone or a microcontroller. Tools that help build compilers include LEX for scanners, and YACC for parsers.''',
     T(8, '[h:Cross compiler] = runs on machine A, code for machine B'), T(9, 'e.g. laptop -> mobile / microcontroller', color='green'),
     T(11, 'Tools: [k:LEX] (scanner generator), [k:YACC] (parser generator)'))

# ===================================================================================== CH 2
p = chapter(2)
beat(p, 'Chapter two. Lexical analysis. The first phase of the compiler.')

p = page('Lexical Analysis: Tokens, Lexemes, Patterns', 2)
beat(p, '''The lexical analyzer, also called the scanner, reads the source program character by character,
and groups them into meaningful units called tokens. It also removes white spaces and comments,
and enters identifiers into the symbol table.''',
     T(0, '[h:Lexical analyzer (scanner)]: characters -> tokens'), T(1, 'removes spaces & comments, fills symbol table'),
     Box(1150, 330, 230, 90, 'Lexical\nanalyzer', size=28, color='blue'), Box(1650, 330, 230, 90, 'Parser', size=30),
     Arr(1380, 355, 1650, 355, label='token', ly=-12, size=26), Arr(1650, 400, 1380, 400, label='get next token', ly=36, size=26))
beat(p, '''Three terms you must know. A token is a category, like identifier, number, or keyword.
A lexeme is the actual text that matches, like count, or ten. And a pattern is the rule that describes the token,
usually a regular expression.''',
     Stamp(1600, 600), Tab(180, 560, [260, 300, 600], 54, [['Token', 'Lexeme', 'Pattern'], ['id', 'count, sum', 'letter (letter | digit)*'],
         ['num', '10, 3.14', 'digit+ (. digit+)?'], ['if', 'if', 'the characters i, f'], ['relop', '<, <=, ==', '< | <= | = | > | >= | <>']], size=28))
beat(p, '''For example, in the statement int count equals ten semicolon, there are five tokens.''',
     T(13, 'int count = 10;  =>  [h:5 tokens]  (int, count, =, 10, ;)', color='red'))

p = page('Input Buffering', 2)
beat(p, '''Reading one character at a time from the disk is slow. So the scanner uses input buffering with two buffers,
each of size N. Two pointers are used. lexeme begin marks the start of the current lexeme,
and forward moves ahead until a token is found.''',
     T(0, 'Two-buffer scheme (each of size N)'), T(1, '[k:lexemeBegin]: start of lexeme   [k:forward]: scans ahead'),
     *[Box(180 + 90 * k, 400, 90, 80, c, size=32) for k, c in enumerate('E = M * C * * 2 eof'.split())],
     Arr(225, 570, 225, 488, color='green'), T(0, 'lexemeBegin', x=170, y=610, size=30, color='green'),
     Arr(765, 570, 765, 488, color='green'), T(0, 'forward', x=715, y=610, size=30, color='green'))
beat(p, '''To avoid checking for the end of the buffer every time, a special character called a sentinel, usually e o f,
is placed at the end of each buffer. Then only one check is needed for most characters.''',
     T(9, '[h:Sentinel] (eof) at the end of each buffer'), T(10, '=> fewer checks, faster scanning', color='green'))

p = page('Regular Expressions & Finite Automata', 2)
beat(p, '''Tokens are described using regular expressions. The basic operators are union, written as a bar, which means or.
Concatenation, which means one after another. And the Kleene star, which means zero or more times. Plus means one or more.''',
     T(0, 'a | b  = a [k:or] b      ab = a [k:then] b'), T(1, 'a*  = zero or more a      a+  = one or more a'),
     T(2, 'e.g. identifier = letter (letter | digit)*', color='green'))
beat(p, '''Regular expressions are recognised by finite automata. In an N F A, a non deterministic automaton,
a state can have many moves on the same symbol, and epsilon moves. In a D F A, a deterministic automaton,
each state has exactly one move for each symbol, and no epsilon moves. D F As are faster, so scanners use D F As.''',
     Tab(180, 420, [300, 450, 450], 54, [['', 'NFA', 'DFA'], ['moves per symbol', 'zero, one or many', 'exactly one'],
         ['ε-moves', 'allowed', 'not allowed'], ['speed', 'slower', '[g:faster]'], ['states', 'fewer', 'may be more']], size=28),
     Stamp(1560, 520))
beat(p, '''The steps to build a scanner are: regular expression, to N F A using Thompson's construction,
to D F A using subset construction, and then minimize the D F A.''',
     T(13, 'RE -> NFA (Thompson) -> DFA (subset construction) -> minimised DFA', color='red'))

D, Tr = subset(); names = 'ABCDE'
p = page('RE to DFA: (a|b)*abb', 2)
beat(p, '''Let's solve the classic question. Convert a or b star, a b b, into a D F A. Using Thompson's construction,
we get an N F A with eleven states, numbered zero to ten. State ten is the final state.''',
     T(0, 'RE = (a|b)*abb    NFA (Thompson): states 0 - 10, final = 10'))
beat(p, '''Now subset construction. Start with epsilon closure of state zero. That is zero, one, two, four, seven. Call it A.
From each set, find where a and b go, and take the epsilon closure again. Each new set becomes a new D F A state.''',
     T(1, 'A = ε-closure(0) = {0, 1, 2, 4, 7}', color='black'),
     Tab(180, 330, [130, 560, 160, 160], 50, [['DFA', 'NFA states', 'a', 'b']] +
         [[names[i] + (' *' if 10 in s else ''), '{' + ', '.join(map(str, sorted(s))) + '}', names[Tr[(i, 'a')]], names[Tr[(i, 'b')]]] for i, s in enumerate(D)],
         size=28, colors={(5, 0): 'red'}))
beat(p, '''We get five states, A to E. E contains state ten, so E is the final state. A and C have the same moves,
so after minimization they merge. The minimized D F A has just four states.''',
     T(0, 'E contains 10 => [r:final state]', x=1250, y=400, size=34), T(0, 'A and C have the same moves', x=1250, y=460, size=34),
     T(0, '=> merge: minimised DFA has [h:4 states]', x=1250, y=520, size=34),
     Ell(245, 805, 110, 90, 'A', size=32), Ell(625, 805, 110, 90, 'B', size=32), Ell(1005, 805, 110, 90, 'D', size=32),
     Ell(1385, 805, 110, 90, 'E', size=32, color='red'), Ell(1395, 815, 90, 70, color='red'),
     Arr(185, 850, 243, 850, color='green'),
     Arr(357, 850, 623, 850, label='a', ly=-14), Arr(737, 850, 1003, 850, label='b', ly=-14), Arr(1117, 850, 1383, 850, label='b', ly=-14),
     Arr(325, 897, 275, 897, curve=-110, label='b', ly=34), Arr(655, 804, 705, 804, curve=-110, label='a', ly=-10),
     Arr(1035, 893, 705, 893, curve=-70, label='a', ly=30), Arr(1415, 893, 690, 897, curve=-150, label='a', ly=30),
     Arr(1420, 806, 330, 812, curve=260, label='b', ly=-12))

p = page('LEX - Lexical Analyzer Generator', 2)
beat(p, '''LEX is a tool that generates a lexical analyzer automatically. You write the patterns and actions in a file
called lex dot l. LEX converts it to lex dot y y dot c, which the C compiler turns into the scanner.''',
     Box(180, 300, 230, 80, 'lex.l', size=30), Box(560, 300, 230, 80, 'LEX', color='red', size=30), Box(940, 300, 280, 80, 'lex.yy.c', size=30),
     Box(1370, 300, 230, 80, 'C compiler', size=28), Box(1700, 300, 160, 80, 'a.out', size=28),
     Arr(410, 340, 560, 340), Arr(790, 340, 940, 340), Arr(1220, 340, 1370, 340), Arr(1600, 340, 1700, 340))
beat(p, '''A LEX program has three parts, separated by double percent signs. Declarations, translation rules,
and auxiliary functions.''',
     T(5, 'declarations', x=240, color='black'), T(6, '%%', x=240, color='red'), T(7, 'translation rules   (pattern   { action })', x=240, color='black'),
     T(8, '%%', x=240, color='red'), T(9, 'auxiliary functions', x=240, color='black'), Stamp(1400, 600))

# ===================================================================================== CH 3
p = chapter(3)
beat(p, 'Chapter three. Grammars and syntax analysis.')

p = page('Context-Free Grammar & Derivations', 3)
beat(p, '''The syntax analyzer, or parser, checks if the tokens follow the grammar of the language, and builds a parse tree.
The grammar is written as a context free grammar, which has four parts. Terminals, non terminals, a start symbol, and productions.''',
     T(0, '[h:Parser]: tokens -> parse tree (checks grammar)'), T(1, '[k:CFG] G = (V, T, P, S): variables, terminals, productions, start'))
beat(p, '''Example grammar: E goes to E plus E, or E times E, or open bracket E close bracket, or id.
A derivation replaces non terminals step by step. In a leftmost derivation, we always replace the leftmost non terminal.
In a rightmost derivation, the rightmost one.''',
     T(3, 'E -> E + E  |  E * E  |  ( E )  |  id', color='black', size=40),
     T(4, '[r:Leftmost]: always replace the leftmost non-terminal'), T(5, '[r:Rightmost]: always replace the rightmost one'))
beat(p, '''For id plus id times id, the leftmost derivation is: E, to E plus E, to id plus E, to id plus E times E,
to id plus id times E, to id plus id times id.''',
     T(7, 'E => E + E => id + E => id + E * E', size=36), T(8, '=> id + id * E => id + id * id', size=36, x=210))

p = page('Ambiguity', 3)
beat(p, '''A grammar is ambiguous if one string has more than one parse tree, or more than one leftmost derivation.
Our grammar is ambiguous, because id plus id times id has two parse trees.''',
     T(0, '[h:Ambiguous] = a string has 2+ parse trees (or 2+ leftmost derivations)'),
     *Tree({'R': (420, 310, 'E', 'black'), 'L': (270, 410, 'E', 'black'), 'p': (420, 410, '+', 'black'), 'M': (570, 410, 'E', 'black'),
            'i1': (270, 510, 'id', 'green'), 'M1': (470, 510, 'E', 'black'), 'st': (570, 510, '*', 'black'), 'M2': (670, 510, 'E', 'black'),
            'i2': (470, 610, 'id', 'green'), 'i3': (670, 610, 'id', 'green')},
           [('R', 'L'), ('R', 'p'), ('R', 'M'), ('L', 'i1'), ('M', 'M1'), ('M', 'st'), ('M', 'M2'), ('M1', 'i2'), ('M2', 'i3')]),
     T(0, 'id + (id * id)', x=330, y=700, size=32, color='green'),
     *Tree({'R': (1270, 310, 'E', 'black'), 'L': (1120, 410, 'E', 'black'), 'st': (1270, 410, '*', 'black'), 'M': (1420, 410, 'E', 'black'),
            'L1': (1020, 510, 'E', 'black'), 'p': (1120, 510, '+', 'black'), 'L2': (1220, 510, 'E', 'black'), 'i3': (1420, 510, 'id', 'green'),
            'i1': (1020, 610, 'id', 'green'), 'i2': (1220, 610, 'id', 'green')},
           [('R', 'L'), ('R', 'st'), ('R', 'M'), ('L', 'L1'), ('L', 'p'), ('L', 'L2'), ('M', 'i3'), ('L1', 'i1'), ('L2', 'i2')], ecol='red'),
     T(0, '(id + id) * id', x=1170, y=700, size=32, color='red'))
beat(p, '''To remove ambiguity, we rewrite the grammar using precedence and associativity. Times binds tighter than plus.
So we get: E goes to E plus T or T. T goes to T times F or F. F goes to bracket E or id.''',
     T(11, 'Unambiguous:  E -> E + T | T     T -> T * F | F     F -> ( E ) | id', color='black', size=36),
     T(12, '( * has higher precedence than +, both left-associative)', color='green', size=32))

p = page('Left Recursion & Left Factoring', 3)
beat(p, '''Top down parsers cannot handle left recursion, because they go into an infinite loop.
A grammar is left recursive if A goes to A alpha. The rule to remove it is very important.
A goes to A alpha or beta, becomes: A goes to beta A dash. A dash goes to alpha A dash, or epsilon.''',
     Stamp(1600, 140), T(0, '[h:Left recursion]: A -> A α | β'), T(1, 'becomes:   A -> β A\'       A\' -> α A\' | ε', color='red', size=42))
beat(p, '''Example. E goes to E plus T or T. Here alpha is plus T, and beta is T. So we get: E goes to T E dash,
and E dash goes to plus T E dash, or epsilon. Same for T.''',
     T(3, 'E -> E + T | T   =>   E -> T E\'      E\' -> + T E\' | ε', color='black'),
     T(4, 'T -> T * F | F   =>   T -> F T\'      T\' -> * F T\' | ε', color='black'))
beat(p, '''Left factoring. When two productions start with the same symbols, the parser cannot decide which one to use.
So we take out the common part. A goes to alpha beta one, or alpha beta two, becomes:
A goes to alpha A dash, and A dash goes to beta one or beta two.''',
     T(6, '[h:Left factoring]: A -> α β1 | α β2'), T(7, 'becomes:   A -> α A\'       A\' -> β1 | β2', color='red', size=42),
     T(8, 'e.g.  S -> iEtS | iEtSeS | a   =>   S -> iEtS S\' | a,   S\' -> eS | ε', color='green', size=34))

p = page('Syntax Error Recovery', 3)
beat(p, '''When the parser finds an error, it should report it and continue. There are four recovery strategies.
Panic mode skips input symbols until a synchronizing token, like a semicolon. It is simple and never loops forever.''',
     N(0, 1, '[r:Panic mode] - skip till a synchronising token ( ; } )'))
beat(p, '''Phrase level recovery makes a small local fix, like inserting a missing semicolon. Error productions add rules
for common mistakes to the grammar. And global correction finds the smallest change to make the program correct,
but it is too costly in practice.''',
     N(1, 2, '[r:Phrase level] - local fix (insert missing ;)'), N(2, 3, '[r:Error productions] - grammar rules for common mistakes'),
     N(3, 4, '[r:Global correction] - minimum changes (too costly)'))
beat(p, '''Also remember the four types of errors. Lexical errors, like an invalid character. Syntax errors, like a missing semicolon.
Semantic errors, like a type mismatch. And logical errors, like an infinite loop, which the compiler cannot detect.''',
     S(5, 'Types of errors', size=38), T(6, '[k:Lexical]: invalid character, e.g. int a = 5 @;'), T(7, '[k:Syntax]: missing ; or unbalanced ( )'),
     T(8, '[k:Semantic]: type mismatch, undeclared variable'), T(9, '[k:Logical]: infinite loop, wrong formula  (compiler cannot detect)'),
     Stamp(1500, 560))

# ===================================================================================== CH 4
p = chapter(4)
beat(p, 'Chapter four. Top down parsing. FIRST, FOLLOW, and the LL one table. Numericals come from here every year.')

p = page('Top-Down Parsing & Recursive Descent', 4)
beat(p, '''Top down parsing builds the parse tree from the root, the start symbol, down to the leaves. It finds a leftmost derivation.
Recursive descent parsing uses one function for each non terminal. It may need backtracking, if it chooses the wrong production.''',
     T(0, '[h:Top-down]: root -> leaves, leftmost derivation'), T(1, '[k:Recursive descent]: one function per non-terminal'),
     T(2, 'may need [r:backtracking] (try another production)'))
beat(p, '''A predictive parser, also called L L one, never backtracks. It looks at just one input symbol to choose the production.
L L one means: scan input from Left, produce a Leftmost derivation, using one symbol of lookahead.
The grammar must have no left recursion and no ambiguity, and it should be left factored.''',
     T(4, '[h:LL(1)]: Left-to-right scan, Leftmost derivation, 1 lookahead'), T(5, 'no backtracking. Needs: no left recursion, no ambiguity,'),
     T(6, 'left-factored grammar', x=230), Stamp(1500, 440))

F_, Fo_, _ = first_follow(G_LL, 'E')
NTs = ['E', "E'", 'T', "T'", 'F']
def fs(sset): return '{ ' + ', '.join(sorted(sset, key=lambda x: ('ε' == x, x))) + ' }'
p = page('FIRST & FOLLOW', 4)
beat(p, '''Rules for FIRST. FIRST of a terminal is the terminal itself. If X goes to epsilon, add epsilon.
If X goes to Y one Y two, add FIRST of Y one. If Y one can be epsilon, also add FIRST of Y two, and so on.''',
     S(0, 'FIRST(X): first terminals X can start with', size=38, color='red'),
     T(1, 'terminal a: FIRST = {a};  X -> ε: add ε;  X -> Y1Y2: FIRST(Y1), if ε then FIRST(Y2) ...', size=32))
beat(p, '''Rules for FOLLOW. Put dollar in FOLLOW of the start symbol. For A goes to alpha B beta, add FIRST of beta, without epsilon,
to FOLLOW of B. If beta can be epsilon, or B is at the end, add FOLLOW of A to FOLLOW of B.''',
     S(2, 'FOLLOW(A): terminals that can come right after A', size=38, color='red'),
     T(3, '$ in FOLLOW(start);  A -> αBβ: FIRST(β) - ε into FOLLOW(B);', size=32), T(4, 'if β =>* ε or B at end: FOLLOW(A) into FOLLOW(B)', size=32, x=230))
beat(p, '''Now apply them to our expression grammar, after removing left recursion. FIRST of E, T and F are all
open bracket and id. FIRST of E dash is plus and epsilon. FIRST of T dash is star and epsilon.
FOLLOW of E and E dash is close bracket and dollar. FOLLOW of T and T dash is plus, close bracket, and dollar.
And FOLLOW of F is plus, star, close bracket, and dollar.''',
     T(6, "E -> TE'   E' -> +TE' | ε   T -> FT'   T' -> *FT' | ε   F -> (E) | id", color='black', size=32),
     Tab(240, 620, [200, 400, 420], 54, [['', 'FIRST', 'FOLLOW']] + [[A, fs(F_[A]), fs(Fo_[A])] for A in NTs], size=30,
         colors={(r, 2): 'red' for r in range(1, 6)}), Stamp(1500, 720, 'MOST ASKED'))

M = ll1_table(G_LL, 'E'); TS = ['id', '+', '*', '(', ')', '$']
def cellp(A, a):
    v = M.get((A, a)); return '' if not v else f"{A}->{''.join(v[0][1])}"
p = page('LL(1) Parsing Table', 4)
beat(p, '''Now we build the L L one table. For each production A goes to alpha: for each terminal in FIRST of alpha,
put the production in the row A and that terminal's column. If FIRST of alpha has epsilon, put it under every terminal in FOLLOW of A.''',
     T(0, 'For A -> α:  M[A, a] for every a in FIRST(α);  if ε in FIRST(α): M[A, b] for b in FOLLOW(A)', size=30))
beat(p, '''Here is the complete table. For example, E dash goes to epsilon is placed under close bracket and dollar,
because those are in FOLLOW of E dash. Empty cells mean error. Since no cell has two entries, this grammar is L L one.''',
     Tab(180, 300, [130, 260, 260, 260, 260, 220, 220], 64, [['', *TS]] + [[A, *[cellp(A, a) for a in TS]] for A in NTs], size=28),
     T(12, 'No cell has 2 entries => grammar is [h:LL(1)]', color='green'), Stamp(1600, 820))

moves = ll1_parse(G_LL, 'E', ['id', '+', 'id', '*', 'id'])
p = page('LL(1) Parsing: id + id * id', 4)
beat(p, '''Let's parse id plus id times id using the table. The stack starts with dollar and E. At each step, look at the top of the stack
and the current input symbol. If they match, pop and move ahead. Otherwise, replace the top with the production from the table.''',
     T(0, 'Stack starts: $ E.  Top = input => match;  else use M[top, input]', size=32))
mv = [[a, b, c if c.startswith(('match', 'accept')) else c.replace(' ', '')] for a, b, c in moves]
beat(p, '''E with id gives E goes to T E dash. T gives F T dash. F gives id, and it matches. T dash with plus gives epsilon,
and E dash with plus gives plus T E dash. Plus matches, and then T and F expand again for the second id.''',
     Tab(180, 290, [250, 250, 250], 52, [['Stack', 'Input', 'Action']] + mv[:9], size=28))
beat(p, '''id matches. With star, T dash goes to star F T dash. Star matches, F gives id, and id matches.
Finally T dash and E dash go to epsilon. Now the stack and the input are both just dollar, so the string is accepted.''',
     Tab(1000, 290, [250, 250, 250], 52, [['Stack', 'Input', 'Action']] + mv[9:], size=28, colors={(len(mv) - 9, 2): 'green'}),
     T(14, 'Stack = $ and input = $  =>  [h:accepted]', x=1000, color='green'))

# ===================================================================================== CH 5
p = chapter(5)
beat(p, 'Chapter five. Bottom up parsing. Shift reduce, and the LR parsers.')

sr = slr_parse(G_EXPR, 'E', ['id', '*', 'id'])
p = page('Shift-Reduce Parsing', 5)
beat(p, '''Bottom up parsing builds the tree from the leaves up to the root. It finds a rightmost derivation, in reverse.
A handle is the part of the string that matches the right side of a production, and reducing it is one step back
in the rightmost derivation.''',
     T(0, '[h:Bottom-up]: leaves -> root, rightmost derivation in reverse'), T(1, '[k:Handle]: substring matching a RHS, whose reduction is the right step'))
beat(p, '''A shift reduce parser has four actions. Shift, which pushes the next input symbol. Reduce, which replaces a handle
on top of the stack with its left side. Accept. And error.''',
     T(2, 'Actions: [r:shift], [r:reduce], [g:accept], error'))
beat(p, '''Example. Parse id times id with the grammar E goes to E plus T or T, T goes to T times F or F, F goes to id.
Shift id. Reduce F goes to id. Reduce T goes to F. Shift times, shift id. Reduce F goes to id. Then reduce T times F to T,
reduce T to E, and accept.''',
     Tab(180, 420, [360, 360, 480], 50, [['Stack', 'Input', 'Action']] + [[a, b, c.replace(' -> ', '->')] for a, b, c in sr], size=28,
         colors={(len(sr), 2): 'green'}), Stamp(1560, 520))
beat(p, '''Two conflicts can happen. A shift reduce conflict, when the parser cannot decide between shift and reduce.
And a reduce reduce conflict, when two reductions are possible.''',
     T(14, 'Conflicts: [r:shift-reduce], [r:reduce-reduce]', size=34))

Gp, C, trans, action, gto = slr(G_SAA, 'S')
p = page('LR(0) Items: S -> AA,  A -> aA | b', 5)
beat(p, '''L R parsers are the most powerful shift reduce parsers. L R means Left to right scan, Rightmost derivation in reverse.
They use items. An item is a production with a dot, showing how much has been seen. For example, A goes to dot a A.''',
     T(0, '[h:LR]: Left-to-right, Rightmost derivation in reverse.  Item = production + dot'))
beat(p, '''Classic example. S goes to A A, A goes to a A or b. First, augment the grammar with S dash goes to S.
I zero is the closure of S dash goes to dot S. Since the dot is before S, add S's productions. Since the dot is before A, add A's productions.''',
     T(1, "Augmented: S' -> S,  (1) S -> AA,  (2) A -> aA,  (3) A -> b", color='black', size=34))
SUB = '₀₁₂₃₄₅₆₇₈₉'
def In(i): return 'I' + SUB[i]
items_txt = []
for i, I in enumerate(C):
    its = [item_str(Gp, p_, d).replace(' -> ', '->').replace(' ', '') for p_, d in sorted(I, key=lambda it: (it[1] == 0 and it[0] != 0, it))]
    items_txt.append(f'{In(i)}: ' + ',  '.join(its))
beat(p, '''Now find goto on every symbol. Goto of I zero on S gives I one, the accept item. On A gives I two. On a gives I three.
On b gives I four. From I two, on A we get I five. From I three, on A we get I six. Goto of I two and I three on a and b
go back to I three and I four. So there are seven states, I zero to I six.''',
     *[T(2 + k, s, size=32, color='red' if k == 0 else 'blue') for k, s in enumerate(items_txt)],
     *[Box(cx - 60, cy - 32, 120, 64, In(i), size=32, color='red' if i == 0 else 'blue') for i, (cx, cy) in
       enumerate([(1050, 470), (1410, 280), (1410, 470), (1410, 680), (1410, 890), (1760, 470), (1760, 680)])],
     Arr(1112, 452, 1348, 292, label='S', ly=-12, color='green'), Arr(1112, 470, 1348, 470, label='A', color='green'),
     Arr(1112, 488, 1360, 646, label='a', ly=-12, color='green'), Arr(1100, 504, 1365, 856, label='b', lx=-34, color='green'),
     Arr(1472, 470, 1698, 470, label='A', color='green'), Arr(1472, 680, 1698, 680, label='A', color='green'),
     Arr(1440, 504, 1440, 646, label='a', lx=18, ly=6, color='green'), Arr(1395, 714, 1395, 856, label='b', lx=-18, ly=6, color='green'),
     Arr(1472, 494, 1472, 884, curve=-170, label='b', lx=14, ly=-56, color='green'),
     Arr(1350, 664, 1350, 700, curve=110, label='a', lx=-18, ly=8, color='green'),
     T(10, 'goto: I₀ on S -> I₁,  on A -> I₂,  on a -> I₃,  on b -> I₄', size=32, color='green'),
     T(11, 'I₂ on A -> I₅,   I₃ on A -> I₆,   I₂, I₃ on a -> I₃,  on b -> I₄', size=32, color='green'))

acts = lambda i, a: ', '.join(sorted(action.get((i, a), [])))
p = page('SLR Parsing Table', 5)
beat(p, '''Now the S L R table. For a transition on a terminal, write shift. For a completed item, A goes to alpha dot,
write reduce under every terminal in FOLLOW of A. FOLLOW of S is dollar. FOLLOW of A is a, b, and dollar.''',
     T(0, 'shift on terminal transitions;  A -> α.  => reduce on FOLLOW(A)', size=32),
     T(1, 'FOLLOW(S) = { $ }     FOLLOW(A) = { a, b, $ }', color='black', size=34))
beat(p, '''So I zero, I two and I three shift on a to three, and on b to four. I four reduces by production three on a, b, and dollar.
I five reduces by production one on dollar. I six reduces by production two. And I one accepts on dollar.''',
     Tab(240, 380, [140, 170, 170, 170, 170, 170], 60, [['State', 'a', 'b', '$', 'A', 'S']] +
         [[In(i), acts(i, 'a'), acts(i, 'b'), acts(i, '$'), str(gto.get((i, 'A'), '')), str(gto.get((i, 'S'), ''))] for i in range(len(C))],
         size=30, colors={(2, 3): 'green'}), T(0, 'ACTION', x=500, y=360, size=28, color='red'), T(0, 'GOTO', x=1060, y=360, size=28, color='red'),
     Stamp(1500, 520, 'MOST ASKED'))
beat(p, '''No cell has two entries, so this grammar is S L R one.''', T(14, 'No conflicts => grammar is [h:SLR(1)]', color='green'))

p = page('LR Parsers Compared', 5)
beat(p, '''There are four L R parsers. L R zero uses no lookahead. S L R uses FOLLOW sets for reduce entries.
Canonical L R, or C L R, uses L R one items with lookaheads, so it is the most powerful, but has the most states.
L A L R merges C L R states with the same core. It has the same number of states as S L R, and is used by YACC.''',
     Tab(180, 220, [260, 420, 300, 460], 56, [['Parser', 'Items / lookahead', 'States', 'Power'], ['LR(0)', 'LR(0), none', 'few', 'weakest'],
         ['SLR(1)', 'LR(0) + FOLLOW', 'few', 'weak'], ['LALR(1)', 'merged LR(1)', 'same as SLR', 'strong (YACC)'],
         ['CLR(1)', 'LR(1) items', '[r:most]', '[g:most powerful]']], size=30))
beat(p, '''Remember the order of power. L R zero is the weakest, then S L R, then L A L R, and canonical L R is the strongest.
Also, every L L one grammar is L R one.''',
     T(8, 'Power:  [h:LR(0) < SLR < LALR < CLR]', color='red', size=42), T(9, 'Every LL(1) grammar is LR(1)', color='green'), Stamp(1500, 700))
beat(p, '''Operator precedence parsing is another bottom up method for expression grammars, where no two non terminals
are next to each other, and no production has epsilon. It uses precedence relations: less than, equal, and greater than.''',
     T(11, '[k:Operator precedence]: no ε, no two adjacent non-terminals;'), T(12, 'relations  <·   =·   ·>  between terminals', x=230))

# ===================================================================================== CH 6
p = chapter(6)
beat(p, 'Chapter six. Syntax directed translation.')

p = page('Syntax-Directed Definitions', 6)
beat(p, '''A syntax directed definition attaches attributes to grammar symbols, and semantic rules to productions.
For example, E goes to E one plus T, with the rule E dot val equals E one dot val plus T dot val.''',
     T(0, '[h:SDD] = grammar + attributes + semantic rules'), T(1, 'E -> E1 + T     { E.val = E1.val + T.val }', color='black'))
beat(p, '''There are two kinds of attributes. A synthesized attribute gets its value from the children of the node.
An inherited attribute gets its value from the parent or the siblings.''',
     T(3, '[r:Synthesized]: from children (bottom-up)'), T(4, '[r:Inherited]: from parent / siblings'), Stamp(1500, 360))
beat(p, '''An S attributed definition uses only synthesized attributes, so it can be evaluated bottom up, with an L R parser.
An L attributed definition allows inherited attributes, but only from the parent or the siblings on the left.
Every S attributed definition is also L attributed.''',
     T(6, '[k:S-attributed]: only synthesized  (bottom-up, LR)'), T(7, '[k:L-attributed]: inherited only from parent / left siblings'),
     T(8, 'Every S-attributed SDD is L-attributed', color='green'))

p = page('Annotated Parse Tree: 3 * 5 + 4', 6)
beat(p, '''An annotated parse tree shows the attribute values at each node. Let's draw it for three times five plus four,
using the rules: E dot val equals E one dot val plus T dot val, T dot val equals T one dot val times F dot val,
and F dot val equals digit dot lexval.''',
     T(0, 'E.val = E1.val + T.val   T.val = T1.val * F.val   F.val = digit.lexval', size=30, color='black'))
nodes = {'E19': (900, 280, 'E.val = 19', 'red'), 'E15': (600, 400, 'E.val = 15', 'blue'), 'plus': (900, 400, '+', 'black'), 'T4': (1200, 400, 'T.val = 4', 'blue'),
         'T15': (600, 520, 'T.val = 15', 'blue'), 'F4': (1200, 520, 'F.val = 4', 'blue'), 'T3': (420, 640, 'T.val = 3', 'blue'), 'star': (620, 640, '*', 'black'),
         'F5': (800, 640, 'F.val = 5', 'blue'), 'd4': (1200, 640, 'digit 4', 'green'), 'F3': (420, 760, 'F.val = 3', 'blue'), 'd5': (800, 760, 'digit 5', 'green'),
         'd3': (420, 880, 'digit 3', 'green')}
edges = [('E19', 'E15'), ('E19', 'plus'), ('E19', 'T4'), ('E15', 'T15'), ('T4', 'F4'), ('T15', 'T3'), ('T15', 'star'), ('T15', 'F5'), ('F4', 'd4'),
         ('T3', 'F3'), ('F5', 'd5'), ('F3', 'd3')]
beat(p, '''The leaves are digits three, five and four. F gets three, so T gets three. Then T equals three times five, fifteen.
E gets fifteen. On the right, F and T get four. Finally, E equals fifteen plus four, which is nineteen.''',
     *[T(0, lab, x=x - len(lab) * 9, y=y, size=32, color=col) for (x, y, lab, col) in nodes.values()],
     *[Arr(nodes[a][0], nodes[a][1] + 12, nodes[b][0], nodes[b][1] - 40, head=False, color='black') for a, b in edges],
     T(0, 'Answer: [h:E.val = 19]', x=1350, y=820, size=40, color='red'))

p = page('YACC - Parser Generator', 6)
beat(p, '''YACC, yet another compiler compiler, generates an L A L R parser automatically. You write the grammar with actions
in a file called parse dot y. YACC produces y dot tab dot c. It is usually used together with LEX.''',
     Box(180, 300, 240, 80, 'parse.y', size=30), Box(560, 300, 220, 80, 'YACC', color='red', size=30), Box(920, 300, 280, 80, 'y.tab.c', size=30),
     Box(1340, 300, 240, 80, 'C compiler', size=28), Box(1700, 300, 160, 80, 'a.out', size=28),
     Arr(420, 340, 560, 340), Arr(780, 340, 920, 340), Arr(1200, 340, 1340, 340), Arr(1580, 340, 1700, 340),
     T(5, 'YACC builds an [h:LALR(1)] parser; works with LEX (yylex())'))

# ===================================================================================== CH 7
p = chapter(7)
beat(p, 'Chapter seven. Intermediate code generation. Quadruples and triples are asked every year.')

p = page('Intermediate Representations', 7)
beat(p, '''Why intermediate code? It makes the compiler portable. The front end produces intermediate code,
and different back ends can turn it into code for different machines. It also makes optimization easier.''',
     T(0, 'Why? [g:portability] (many back ends) + [g:easier optimisation]'))
beat(p, '''There are three common forms. A syntax tree, or a D A G. Postfix notation, where a plus b becomes a b plus.
And three address code, where each instruction has at most three addresses, like x equals y op z.''',
     N(2, 1, '[r:Syntax tree / DAG]'), N(3, 2, '[r:Postfix]:  a + b * c  ->  a b c * +'), N(4, 3, '[r:Three-address code]:  x = y op z  (at most 3 addresses)'),
     Stamp(1500, 360))
beat(p, '''Types of three address statements: assignment, copy, unconditional jump with goto, conditional jump with if,
procedure calls with param and call, indexed assignments with arrays, and address and pointer assignments.''',
     T(5, 'x = y op z,  x = op y,  x = y,  goto L,  if x relop y goto L,  param x,  call p, n,  x = y[i],  x = &y,  x = *y', size=30))
beat(p, '''Here is the syntax tree and the D A G for a plus a times, b minus c, plus, b minus c times d. In the syntax tree,
every sub expression gets its own node. In the D A G, common parts are shared. b minus c is drawn only once, and a is used from the same node.
So the D A G is smaller, and it shows the compiler what to compute only once.''',
     T(0, 'e.g.  a + a * (b - c) + (b - c) * d', x=180, y=L(6), size=34, color='black'),
     *Tree({'R': (560, 600, '+', 'black'), 'P': (380, 685, '+', 'black'), 'M2': (760, 685, '*', 'black'), 'a1': (270, 770, 'a', 'green'),
            'M1': (470, 770, '*', 'black'), 'S2': (720, 770, '-', 'black'), 'd': (860, 770, 'd', 'green'), 'a2': (400, 855, 'a', 'green'),
            'S1': (540, 855, '-', 'black'), 'b2': (670, 855, 'b', 'green'), 'c2': (770, 855, 'c', 'green'), 'b1': (490, 940, 'b', 'green'),
            'c1': (590, 940, 'c', 'green')},
           [('R', 'P'), ('R', 'M2'), ('P', 'a1'), ('P', 'M1'), ('M2', 'S2'), ('M2', 'd'), ('M1', 'a2'), ('M1', 'S1'), ('S2', 'b2'), ('S2', 'c2'),
            ('S1', 'b1'), ('S1', 'c1')], w=60, h=50, size=28),
     T(0, 'Syntax tree', x=180, y=650, size=32, color='blue'),
     *Tree({'R': (1450, 600, '+', 'red'), 'P': (1290, 685, '+', 'red'), 'M2': (1630, 685, '*', 'red'), 'M1': (1390, 770, '*', 'red'),
            'a': (1220, 855, 'a', 'green'), 'S': (1530, 855, '-', 'red'), 'd': (1740, 770, 'd', 'green'), 'b': (1470, 940, 'b', 'green'),
            'c': (1590, 940, 'c', 'green')},
           [('R', 'P'), ('R', 'M2'), ('P', 'M1'), ('P', 'a'), ('M1', 'a'), ('M1', 'S'), ('M2', 'S'), ('M2', 'd'), ('S', 'b'), ('S', 'c')],
           w=60, h=50, size=28, ecol='red'),
     T(0, 'DAG (shared nodes)', x=1560, y=L(6), size=32, color='red'))

p = page('Three-Address Code: a = b * -c + b * -c', 7)
tac = ['t1 = minus c', 't2 = b * t1', 't3 = minus c', 't4 = b * t3', 't5 = t2 + t4', 'a = t5']
beat(p, '''Classic question. Write the three address code, quadruples, and triples for a equals b times minus c plus b times minus c.
First, the three address code. t one equals minus c. t two equals b times t one. t three equals minus c. t four equals b times t three.
t five equals t two plus t four. And a equals t five.''',
     *[T(k, s, x=200, size=36) for k, s in enumerate(tac)], Stamp(1600, 140, 'MOST ASKED'))
beat(p, '''Quadruples have four fields: operator, argument one, argument two, and result. Each temporary gets its own name in the result field.''',
     T(0, '[h:Quadruples]', x=560, y=L(1), size=36),
     Tab(560, 300, [80, 140, 110, 110, 120], 50, [['#', 'op', 'arg1', 'arg2', 'result'], ['0', 'minus', 'c', '', 't1'], ['1', '*', 'b', 't1', 't2'],
         ['2', 'minus', 'c', '', 't3'], ['3', '*', 'b', 't3', 't4'], ['4', '+', 't2', 't4', 't5'], ['5', '=', 't5', '', 'a']], size=28))
beat(p, '''Triples have only three fields: operator, argument one, and argument two. Instead of temporaries,
we refer to the position of an earlier triple, written in brackets. Indirect triples keep a separate list of pointers to triples,
so the statements can be reordered easily during optimization.''',
     T(0, '[h:Triples]', x=1260, y=L(1), size=36),
     Tab(1260, 300, [80, 140, 120, 120], 50, [['#', 'op', 'arg1', 'arg2'], ['0', 'minus', 'c', ''], ['1', '*', 'b', '(0)'], ['2', 'minus', 'c', ''],
         ['3', '*', 'b', '(2)'], ['4', '+', '(1)', '(3)'], ['5', '=', 'a', '(4)']], size=28),
     T(10, '[k:Indirect triples]: a separate list of pointers to triples (easy reordering)', size=34),
     Tab(180, 820, [220] + [110] * 6, 50, [['statement', '35', '36', '37', '38', '39', '40'], ['points to', '(0)', '(1)', '(2)', '(3)', '(4)', '(5)']],
         size=28))

# ===================================================================================== CH 8
p = chapter(8)
beat(p, 'Chapter eight. Runtime environment and the symbol table.')

p = page('Storage Organisation & Activation Record', 8)
beat(p, '''At run time, memory for a program is divided into four parts. The code area, the static data area,
the stack, and the heap. The stack and heap grow towards each other. The stack holds activation records
for function calls. The heap holds dynamically allocated memory.''',
     Box(220, 240, 360, 80, 'Code', size=32), Box(220, 320, 360, 80, 'Static data', size=32), Box(220, 400, 360, 110, 'Stack', size=32, color='blue'),
     Box(220, 510, 360, 120, '', size=32), Box(220, 630, 360, 110, 'Heap', size=32, color='red'),
     Arr(400, 500, 400, 550, color='green'), Arr(400, 640, 400, 590, color='green'))
beat(p, '''Each time a function is called, an activation record is pushed on the stack. It contains the actual parameters,
the returned value, the control link which points to the caller's record, the access link for non local data,
the saved machine status, local data, and temporaries.''',
     Tab(1100, 230, [560], 56, [['Actual parameters'], ['Returned value'], ['Control link (caller)'], ['Access link (non-local)'],
         ['Saved machine status'], ['Local data'], ['Temporaries']], hdr=False, size=30, color='blue'),
     T(0, 'Activation record', x=1180, y=210, size=30, color='red'), Stamp(900, 860))
beat(p, '''Static allocation fixes memory at compile time, so it does not support recursion. Stack allocation supports recursion.
Heap allocation is for data that lives longer than the function call.''',
     T(14, '[k:Static]: no recursion   [k:Stack]: recursion OK   [k:Heap]: dynamic data', size=34))

p = page('Scoping & Parameter Passing', 8)
beat(p, '''Static scoping, also called lexical scoping, finds a variable's meaning from the program text, where it is written.
Dynamic scoping finds it from the calling sequence at run time. C and Java use static scoping.''',
     T(0, '[r:Static (lexical) scope]: decided by program text (C, Java)'), T(1, '[r:Dynamic scope]: decided by the calling sequence at run time'))
beat(p, '''Parameter passing methods. Call by value copies the value, so changes inside the function do not affect the caller.
Call by reference passes the address, so changes affect the caller. Copy restore, or value result, copies in,
and copies back at the end. And call by name substitutes the actual expression, like a macro.''',
     Stamp(1500, 360), N(3, 1, '[k:Call by value]: copy of value, caller unchanged'), N(4, 2, '[k:Call by reference]: address passed, caller changes'),
     N(5, 3, '[k:Copy-restore (value-result)]: copy in, copy back at end'), N(6, 4, '[k:Call by name]: argument text substituted (like macro)'))
beat(p, '''A quick GATE style example. x is ten globally. Function g declares its own x as twenty, and then calls f, which prints x.
With static scoping, f sees the global x, so it prints ten. With dynamic scoping, f uses the most recent x in the calling sequence,
so it prints twenty.''',
     T(8, 'int x = 10;', x=220, color='black'), T(9, 'void f() { print(x); }', x=220, color='black'), T(10, 'void g() { int x = 20; f(); }', x=220, color='black'),
     T(11, 'main() { g(); }', x=220, color='black'),
     T(9, 'Static scope  =>  prints [h:10]', x=1100, color='red'), T(10, 'Dynamic scope  =>  prints [h:20]', x=1100, color='red'),
     Stamp(1600, 820, 'GATE'))

p = page('Symbol Table', 8)
beat(p, '''The symbol table stores information about every identifier: its name, type, scope, size, and memory location.
Every phase of the compiler uses it.''',
     T(0, '[h:Symbol table]: name, type, scope, size, address of each identifier'),
     Tab(1100, 300, [200, 160, 160, 200], 52, [['Name', 'Type', 'Size', 'Address'], ['count', 'int', '4', '1000'], ['rate', 'float', '4', '1004'],
         ['name', 'char[20]', '20', '1008']], size=28))
beat(p, '''It can be organised as a linear list, which is simple but slow to search. A binary search tree, which is faster.
Or a hash table, which is the fastest and most commonly used.''',
     T(3, 'Organisation:'), N(4, 1, 'Linear list - simple, [r:slow] O(n)'), N(5, 2, 'Search tree - O(log n)'),
     N(6, 3, '[h:Hash table] - [g:fastest], most used'))

# ===================================================================================== CH 9
p = chapter(9)
beat(p, 'Chapter nine. Code optimization. Basic blocks, D A Gs, and optimization techniques.')

blk = ['(1) i = 1', '(2) t1 = 4 * i', '(3) t2 = a[t1]', '(4) sum = sum + t2', '(5) i = i + 1', '(6) if i <= 20 goto (2)', '(7) x = sum']
p = page('Basic Blocks & Flow Graph', 9)
beat(p, '''A basic block is a sequence of statements where control enters only at the beginning and leaves only at the end.
To find basic blocks, first find the leaders. Rule one, the first statement is a leader. Rule two, the target of any jump is a leader.
Rule three, the statement right after a jump is a leader.''',
     T(0, '[h:Basic block]: enter only at start, leave only at end'), S(1, 'Leaders:', size=36), N(2, 1, 'first statement'),
     N(3, 2, 'target of any goto'), N(4, 3, 'statement right after a goto'), Stamp(1600, 240))
beat(p, '''Example. Statement one is the first, so it is a leader. Statement two is the target of the goto, so it is a leader.
Statement seven comes right after the goto, so it is a leader too. So we get three basic blocks.''',
     *[T(6 + k, s, x=220, size=34, color='red' if k in (0, 1, 6) else 'blue') for k, s in enumerate(blk)],
     T(0, 'Leaders: (1), (2), (7)', x=760, y=L(6), size=34, color='red'))
beat(p, '''B one is statement one. B two is statements two to six, which is the loop. And B three is statement seven.
In the flow graph, B one goes to B two. B two goes back to itself, and also to B three.''',
     Box(1200, 560, 260, 70, 'B1: (1)', size=30), Box(1200, 690, 260, 70, 'B2: (2)-(6)', size=30, color='blue'), Box(1200, 820, 260, 70, 'B3: (7)', size=30),
     Arr(1330, 630, 1330, 690), Arr(1330, 760, 1330, 820), Arr(1460, 705, 1460, 745, curve=-150, label='loop', lx=58, ly=10, size=28))

p = page('DAG for a Basic Block', 9)
beat(p, '''A D A G, a directed acyclic graph, represents a basic block. It helps find common sub expressions automatically.
Example: a equals b plus c. b equals a minus d. c equals b plus c. d equals a minus d.''',
     *[T(k, s, x=200, size=36, color='black') for k, s in enumerate(['a = b + c', 'b = a - d', 'c = b + c', 'd = a - d'])])
beat(p, '''Look at the second and fourth statements. Both compute a minus d, and a and d have not changed in between.
So the D A G uses just one node for both, labelled b and d. That is a common sub expression.''',
     *Tree({'n3': (1500, 250, '+    c', 'red', 160), 'n2': (1280, 420, '-   b, d', 'red', 170), 'c0': (1600, 760, 'c0', 'black'),
            'n1': (1060, 590, '+    a', 'red', 160), 'd0': (1450, 590, 'd0', 'black'), 'b0': (960, 760, 'b0', 'black')},
           [('n3', 'n2'), ('n3', 'c0'), ('n2', 'n1'), ('n2', 'd0'), ('n1', 'b0'), ('n1', 'c0')], w=90, h=64, size=30, head=True))
beat(p, '''So the optimized block is: a equals b plus c. d equals a minus d. c equals d plus c. This works if b is not used after the block.''',
     T(6, 'Optimised:', color='green'), T(7, 'a = b + c;   d = a - d;   c = d + c', color='green', size=40),
     T(8, '(if b is not used after the block)', color='green', size=32), Stamp(560, 300))

p = page('Optimization Techniques', 9)
beat(p, '''The main machine independent optimizations. Common sub expression elimination: compute a repeated expression only once.
Constant folding: compute constant expressions at compile time, so two times three becomes six.''',
     Stamp(1650, 140, 'MOST ASKED'), N(0, 1, '[r:Common sub-expression elimination]: t = a * b; x = t; y = t'), N(1, 2, '[r:Constant folding]: x = 2 * 3  ->  x = 6'))
beat(p, '''Constant propagation and copy propagation: replace a variable with its known constant, or with the variable it was copied from.
Dead code elimination: remove code whose result is never used, or that can never run.''',
     N(2, 3, '[r:Constant / copy propagation]: x = 5; y = x + 1 -> y = 6'), N(3, 4, '[r:Dead code elimination]: remove unused / unreachable code'))
beat(p, '''Loop optimizations are the most important, because programs spend most of their time in loops. Code motion moves
loop invariant code, which gives the same result every time, outside the loop. Strength reduction replaces costly operations
with cheaper ones, like multiplication with addition. And induction variable elimination removes extra loop counters.''',
     S(5, 'Loop optimisations', size=38), N(6, 5, '[r:Code motion]: move loop-invariant code out of the loop'),
     N(7, 6, '[r:Strength reduction]: i * 4  ->  t = t + 4'), N(8, 7, '[r:Induction variable elimination]: remove extra counters'))
beat(p, '''Peephole optimization looks at a small window of instructions and improves them. It removes redundant loads and stores,
unreachable code, jumps to jumps, and uses algebraic simplification, like x equals x plus zero, and machine idioms like increment.''',
     S(10, 'Peephole optimisation', size=38), T(11, 'redundant load/store, unreachable code, jump-to-jump,'),
     T(12, 'algebraic simplification (x = x + 0), machine idioms (INC)'))

p = page('Data-Flow Analysis (GATE)', 9)
beat(p, '''Data flow analysis collects information about how values flow through the program. Reaching definitions
finds which assignments can reach a point. The equations are: out of B equals gen of B, union, in of B minus kill of B.
And in of B is the union of out of all predecessors.''',
     S(0, 'Reaching definitions (forward)', size=36, color='red'), T(1, 'out[B] = gen[B] ∪ (in[B] - kill[B])'), T(2, 'in[B] = ∪ out[P]  over predecessors P'))
beat(p, '''Live variable analysis finds which variables will be used later. It is used for register allocation and dead code elimination.
It works backwards: in of B equals use of B, union, out of B minus def of B. And out of B is the union of in of all successors.''',
     S(4, 'Live variables (backward)', size=36, color='red'), T(5, 'in[B] = use[B] ∪ (out[B] - def[B])'), T(6, 'out[B] = ∪ in[S]  over successors S'),
     Stamp(1500, 420))
beat(p, '''Available expressions finds expressions already computed, which helps common sub expression elimination.
And constant propagation tracks which variables hold constants. All of these are in the GATE syllabus.''',
     S(8, 'Available expressions (forward)', size=36, color='red'), T(9, 'used for common sub-expression elimination'),
     T(11, 'Also: constant propagation - in GATE syllabus', color='green'))

# ===================================================================================== CH 10
p = chapter(10)
beat(p, 'Chapter ten. Code generation. The last phase of the compiler.')

p = page('Issues in Code Generation', 10)
beat(p, '''The code generator converts intermediate code into target machine code. The main issues in its design are:
the input to the code generator, the target program, memory management, instruction selection,
register allocation, and the order of evaluation.''',
     Stamp(1600, 140), N(0, 1, 'Input to the code generator (IR + symbol table)'), N(1, 2, 'Target program (absolute / relocatable / assembly)'),
     N(2, 3, 'Memory management'), N(3, 4, 'Instruction selection'), N(4, 5, 'Register allocation & assignment'), N(5, 6, 'Evaluation order'))
beat(p, '''Register allocation is very important, because registers are the fastest storage. It is usually done using graph colouring.
Each variable is a node, and two nodes are connected if they are live at the same time. Colours are registers.''',
     T(7, '[h:Register allocation]: graph colouring'), T(8, 'node = variable, edge = live at same time, colour = register', color='green'))

p = page('Simple Code Generator - Example', 10)
code = ['MOV a, R0', 'SUB b, R0', 'MOV a, R1', 'SUB c, R1', 'ADD R1, R0', 'ADD R1, R0', 'MOV R0, d']
beat(p, '''Example. Generate code for: t equals a minus b, u equals a minus c, v equals t plus u, d equals v plus u.
The code generator uses a register descriptor, which says what each register holds, and an address descriptor,
which says where each variable's value is.''',
     *[T(k, s, x=220, size=36, color='black') for k, s in enumerate(['t = a - b', 'u = a - c', 'v = t + u', 'd = v + u'])],
     T(5, '[k:Register descriptor]: what each register holds', size=34), T(6, '[k:Address descriptor]: where each value is', size=34))
beat(p, '''Move a into R zero, subtract b, so R zero holds t. Move a into R one, subtract c, so R one holds u.
Add R one to R zero, so R zero holds v. Add R one again, so R zero holds d. Finally, store R zero into d.''',
     Tab(1000, 230, [380, 420], 54, [['Code', 'Register contents']] +
         [[c_, r] for c_, r in zip(code, ['R0: a', 'R0: t', 'R0: t, R1: a', 'R0: t, R1: u', 'R0: v, R1: u', 'R0: d, R1: u', 'd in memory'])], size=28),
     Stamp(1500, 760, 'NUMERICAL'))

# ===================================================================================== CH 11
p = chapter(11)
beat(p, "Chapter eleven. Exam revision. If you're short on time, revise these first.")

p = page('Most Asked Exam Questions', 11)
qs = ['Phases of a compiler (with example)', 'Token, lexeme, pattern + input buffering', 'RE -> NFA -> DFA, e.g. (a|b)*abb',
      'Ambiguity, left recursion, left factoring', 'FIRST & FOLLOW + LL(1) table + parsing moves', 'Shift-reduce parsing, handle',
      'LR(0) items + SLR table; CLR vs LALR', 'Annotated parse tree, S/L-attributed', 'Three-address code, quadruples, triples',
      'Activation record, parameter passing', 'Basic blocks, DAG, loop & peephole optimisation', 'Code generation issues + example']
beat(p, '''Here are the most asked questions. Phases of a compiler with an example. Tokens, lexemes and patterns. Regular expression to D F A.
And ambiguity, left recursion and left factoring.''', *[T(k, f'{k + 1}. {q}', x=200, size=36) for k, q in enumerate(qs[:4])])
beat(p, '''FIRST and FOLLOW with the L L one table. Shift reduce parsing. L R zero items and the S L R table, and C L R versus L A L R.
And annotated parse trees.''', *[T(k, f'{k + 1}. {q}', x=200, size=36) for k, q in enumerate(qs) if 4 <= k < 8])
beat(p, '''Three address code with quadruples and triples. Activation records and parameter passing. Basic blocks, D A G and optimization.
And code generation.''', *[T(k, f'{k + 1}. {q}', x=200, size=36) for k, q in enumerate(qs) if k >= 8])
beat(p, '''Here's one more tip for the exam. For numericals, draw the table neatly, and write the rule or formula first.
That way, you still get step marks, even if the final answer goes wrong.''',
     T(13, 'Tip: draw the table neatly, [h:write the rule first] => step marks!', color='red'))

p = page('All the Best!', 11, kind='outro')
beat(p, '''That's the complete compiler design subject. If this helped you, share it with your friends who have the exam,
and subscribe to TechVibe24 for more one shot videos. Tell me in the comments which subject you want next. All the best for your exam!''')

if __name__ == '__main__':
    json.dump({'pages': PAGES, 'chapters': CHAPTERS}, open('cd_script.json', 'w'), indent=1, ensure_ascii=False)
    nb = sum(len(p['beats']) for p in PAGES); nw = sum(len(b['say'].split()) for p in PAGES for b in p['beats'])
    print('pages', len(PAGES), 'beats', nb, 'words', nw, 'est minutes', round(nw / 150, 1))
