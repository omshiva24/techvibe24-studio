'''Data Structures & Algorithms (MCA) + Advanced DSA (M.Tech) one-shot: narration beats + handwritten note elements.
Markup inside text: [r:red] [g:green] [k:black] [h:yellow highlight] [p:pink highlight]'''
import json, math
from ds_numericals import *

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
def Node(p, name, color='blue', r=32, size=26): return Ell(p[0] - r, p[1] - r, 2 * r, 2 * r, str(name), color=color, size=size)
def WEdge(a, b, w=None, color='black', r=32, side=1, size=26, off=22, width=4, at=.5):
    (x1, y1), (x2, y2) = a, b; d = math.hypot(x2 - x1, y2 - y1); ux, uy = (x2 - x1) / d, (y2 - y1) / d; nx, ny = -uy, ux
    if ny > 0 or (abs(ny) < 1e-9 and nx < 0): nx, ny = -nx, -ny
    nx, ny = nx * side, ny * side; mx, my = x1 + (x2 - x1) * at + nx * off, y1 + (y2 - y1) * at + ny * off
    out = [Ln([(x1 + ux * r, y1 + uy * r), (x2 - ux * r, y2 - uy * r)], color, width)]
    if w is not None: out.append(T(0, str(w), x=mx - size * .3 * len(str(w)), y=my + size * .35, size=size, color='red'))
    return out
def DEdge(a, b, w=None, color='black', r=32, side=1, size=24, off=20, curve=0, at=.5):
    (x1, y1), (x2, y2) = a, b; d = math.hypot(x2 - x1, y2 - y1); ux, uy = (x2 - x1) / d, (y2 - y1) / d; nx, ny = -uy, ux
    p1 = (x1 + ux * r, y1 + uy * r); p2 = (x2 - ux * (r + 3), y2 - uy * (r + 3))
    if ny > 0 or (abs(ny) < 1e-9 and nx < 0): nx, ny = -nx, -ny
    nx, ny = nx * side, ny * side
    out = [Arr(*p1, *p2, color=color, curve=curve)]
    if w is not None:
        mx, my = x1 + (x2 - x1) * at + nx * (off + abs(curve) / 2), y1 + (y2 - y1) * at + ny * (off + abs(curve) / 2)
        out.append(T(0, str(w), x=mx - size * .3 * len(str(w)), y=my + size * .35, size=size, color='red'))
    return out
def Cells(x, y, vals, cw=64, h=56, size=28, colors=None, fills=None, color='black'):
    return Tab(x, y, [cw] * len(vals), h, [[str(v) for v in vals]], size=size, hdr=False, colors={(0, c): v for c, v in (colors or {}).items()}, fills={(0, c): v for c, v in (fills or {}).items()}, color=color)
def BinTree(t, root, x0, y0, w, dy=100, r=30, size=26, colors=None, ecol='black'):
    order = ino(t, root); pos = {}; depth = {}
    def dep(n, d):
        if n is None: return
        depth[n] = d; dep(t[n][0], d + 1); dep(t[n][1], d + 1)
    dep(root, 0); gap = w / max(1, len(order) - 1)
    for i, n in enumerate(order): pos[n] = (x0 + i * gap, y0 + depth[n] * dy)
    out = []
    for n in order:
        for c in t[n]:
            if c is not None: out += WEdge(pos[n], pos[c], None, ecol, r=r, width=3)
    out += [Node(pos[n], n, (colors or {}).get(n, 'blue'), r=r, size=size) for n in order]
    return out, pos
def BTreeDraw(node, x, y, cw=56, h=52, gapx=40, dy=120, size=26):
    '''node = (keys, kids) from ds_numericals.dump; returns elements, centred at x'''
    keys, kids = node; out = []
    def width(nd):
        k, ch = nd; own = len(k) * cw
        return max(own, sum(width(c) for c in ch) + gapx * (len(ch) - 1)) if ch else own
    def draw(nd, cx, top):
        k, ch = nd; w0 = len(k) * cw; x0 = cx - w0 / 2
        out.append(Cells(x0, top, k, cw, h, size))
        if ch:
            tw = sum(width(c) for c in ch) + gapx * (len(ch) - 1); xx = cx - tw / 2
            for i, c in enumerate(ch):
                cwid = width(c); ccx = xx + cwid / 2
                out.append(Ln([(x0 + i * cw, top + h), (ccx, top + dy)], 'black', 3)); draw(c, ccx, top + dy); xx += cwid + gapx
    draw(node, x, y); return out

CHAPTERS = [
 (1, 'Algorithms & Complexity', ['Algorithm & pseudocode', 'Time & space complexity', 'Asymptotic notations'], 5),
 (2, 'Arrays & Searching', ['1-D & 2-D arrays', 'Address calculation', 'Linear & binary search'], 4),
 (3, 'Stacks & Queues', ['Stack operations', 'Infix to postfix', 'Queue, circular queue, deque'], 5),
 (4, 'Linked Lists', ['Singly linked list', 'Doubly & circular lists', 'Applications'], 4),
 (5, 'Trees & Binary Search Trees', ['Terminology & types', 'Traversals', 'BST insert & delete'], 5),
 (6, 'Graphs', ['Representation', 'BFS & DFS', 'Topological sort', "MST & Dijkstra"], 5),
 (7, 'Divide & Conquer, Recurrences', ['Merge sort & quick sort', 'Max subarray & Strassen', 'Master method'], 5),
 (8, 'Greedy Method', ['Fractional knapsack', 'Job sequencing', 'Huffman codes & matroids'], 5),
 (9, 'Dynamic Programming', ['0/1 knapsack', 'Rod cutting & matrix chain', 'LCS & optimal BST', 'TSP'], 5),
 (10, 'Backtracking', ['n-Queens', 'Graph colouring'], 4),
 (11, 'B-Trees & Fibonacci Heaps', ['B-tree properties', 'B-tree insertion', 'Fibonacci heap'], 5),
 (12, 'Disjoint Sets & Hash Tables', ['Union by rank', 'Path compression', 'Open addressing'], 5),
 (13, 'Randomized & Amortized Analysis', ['Hiring problem', 'Aggregate analysis', 'Accounting method'], 4),
 (14, 'Johnson & Maximum Flow', ["Johnson's algorithm", 'Ford-Fulkerson', 'Bipartite matching'], 5),
 (15, 'Multithreaded Algorithms', ['Work, span, parallelism', 'Multithreaded matrix multiply', 'Multithreaded merge sort'], 4),
 (16, 'String Matching', ['Naive & Rabin-Karp', 'Finite automata', 'KMP'], 5),
 (17, 'NP-Completeness & Approximation', ['P, NP, NP-complete', 'Vertex cover', 'TSP approximation'], 5),
 (18, 'Balanced Trees & More', ['AVL trees', 'Red-black trees', 'Skip lists & Bloom filters'], 4),
 (19, 'Exam Revision', ['Complexity table', 'Most asked questions'], 5),
]
def chapter(i):
    n, t, subs, stars = CHAPTERS[i - 1]
    return page(t, n, kind='chapter', num=n, subs=subs, stars=stars)

# =====================================================================================
p = page('Data Structures and Algorithms', 0, kind='cover')
beat(p, '''Data Structures and Algorithms. Basic and advanced, the complete subject in one video. Simple explanations, handwritten notes,
and every important exam problem solved step by step.''')
beat(p, '''This video follows the Pondicherry University syllabus for M C A, Data Structures and Algorithms, and for M Tech computer science, Advanced Data Structures and Algorithms.
It also covers the topics other universities ask, like A V L trees and red black trees. So it works for M C A, M Tech, M Sc and B Tech students everywhere.''')

p = page('Contents', 0)
beat(p, "Here's our plan. Nineteen chapters, from the basics to the advanced topics.", T(0, 'What we will cover today', size=40, font='bold', color='black'))
beat(p, '''Chapters one to ten are the M C A paper, and the base for everyone: complexity, arrays, stacks, queues, linked lists, trees, graphs, divide and conquer, greedy, dynamic programming and backtracking.''',
     *[T(1 + k, f'{k + 1}. {CHAPTERS[k][1]}', x=200, size=31) for k in range(10)], T(12, '1-10: MCA (MCAP 411) + base for M.Tech', x=200, size=30, color='red'))
beat(p, '''Chapters eleven to seventeen are the M Tech advanced topics: B trees, Fibonacci heaps, disjoint sets, hashing, amortized analysis, max flow, multithreading, string matching and N P completeness.
Then extra topics for other universities, and a final revision.''',
     *[T(k - 9, f'{k + 1}. {CHAPTERS[k][1]}', x=1000, size=31) for k in range(10, 19)],
     T(12, '11-17: M.Tech (CSCE 614)   18: other universities', x=1000, size=30, color='red'))

# ===================================================================================== CH 1
p = chapter(1)
beat(p, "Chapter one. Algorithms and complexity. This is the language we use for the whole subject.")

p = page('Algorithm & Complexity', 1)
beat(p, '''An algorithm is a finite set of clear steps that solves a problem. It takes input, gives output, and every step must be definite and must finish.
We usually write it in pseudocode, which looks like simple code without the language details.''',
     T(0, '[h:Algorithm]: finite, clear steps -> input, output, definite, finite, effective', size=34),
     T(1, 'Pseudocode:  for i = 1 to n:  sum = sum + A[i]', size=34, color='black'))
beat(p, '''A data structure is a way of storing and organizing data so it can be used efficiently. Linear data structures, like arrays, stacks, queues and linked lists, store items in a sequence.
Non linear ones, like trees and graphs, store items in a hierarchy or a network.''',
     T(3, '[h:Data structure]: way to store & organize data efficiently', size=34),
     T(4, '[k:Linear]: array, stack, queue, linked list   ·   [k:Non-linear]: tree, graph', size=34))
beat(p, '''Time complexity measures how the running time grows with the input size n. Space complexity measures the extra memory needed.
For example, a single loop over n items takes order n time. Two nested loops take order n squared. And halving the problem each step, like binary search, takes order log n.''',
     Stamp(1650, 140),
     Tab(180, 560, [520, 300, 520], 54, [['Code pattern', 'Time', 'Example'], ['one loop over n', 'O(n)', 'linear search'], ['two nested loops', 'O(n²)', 'bubble sort'],
         ['halve each step', 'O(log n)', 'binary search'], ['divide + merge', 'O(n log n)', 'merge sort'], ['try all subsets', 'O(2ⁿ)', 'brute-force knapsack']], size=29,
         colors={(r, 1): 'red' for r in range(1, 6)}))

p = page('Asymptotic Notations', 1)
beat(p, '''Asymptotic notations describe growth for large n, ignoring constants. Big O gives an upper bound: f of n is O of g of n if f is at most c times g for all n beyond some n zero.
Big Omega gives a lower bound. And Theta gives a tight bound, both upper and lower.''',
     Stamp(1650, 140, 'MOST ASKED'),
     T(0, '[h:O]: f(n) ≤ c·g(n) for n ≥ n₀   (upper bound, worst case)', size=34), T(1, '[h:Ω]: f(n) ≥ c·g(n) for n ≥ n₀   (lower bound)', size=34),
     T(2, '[h:Θ]: c₁g(n) ≤ f(n) ≤ c₂g(n)   (tight bound)', size=34), T(3, 'little o: strictly smaller;   little ω: strictly larger', size=32, color='green'))
beat(p, '''Example: f of n equals three n squared plus five n plus two. For n at least one, this is at most ten n squared, so f is O of n squared. It is also at least three n squared, so it is Omega of n squared.
That makes it Theta of n squared. The rule is simple: keep the fastest growing term and drop the constant.''',
     T(5, 'f(n) = 3n² + 5n + 2', size=36, color='black'), T(6, '≤ 3n² + 5n² + 2n² = 10n²  (n ≥ 1)  =>  O(n²)', size=34), T(7, '≥ 3n²  =>  Ω(n²)   =>   [h:Θ(n²)]', size=34))
beat(p, '''Remember the order of common growth functions, from slowest to fastest: constant, log n, square root of n, n, n log n, n squared, n cubed, two to the n, and n factorial.''',
     T(9, 'Growth order:', size=34, color='black'), T(10, '1 < log n < √n < n < n log n < n² < n³ < 2ⁿ < n!', size=40, color='red'),
     T(12, 'n = 1024:  log n = 10,  n log n = 10,240,  n² ≈ 10⁶', size=32, color='green'))

# ===================================================================================== CH 2
p = chapter(2)
beat(p, 'Chapter two. Arrays and searching.')

p = page('Arrays & Address Calculation', 2)
beat(p, '''An array stores elements of the same type in continuous memory. Any element can be reached directly using its index, in constant time. A two dimensional array is a table of rows and columns.''',
     T(0, '[h:Array]: same type, continuous memory, index access in O(1)', size=34),
     Cells(300, 300, [12, 45, 7, 23, 56], 90, 60, 30), *[T(0, f'[{i}]', x=325 + 90 * i, y=400, size=24, color='grey') for i in range(5)])
beat(p, '''A common numerical: find the address of an element. In row major order, rows are stored one after another, so the address of A i j is base plus size times, i into number of columns plus j.
In column major order, it is base plus size times, j into number of rows plus i.''',
     Stamp(1650, 140, 'NUMERICAL'), T(5, '[k:Row-major]:  Loc(A[i][j]) = Base + w × (i × C + j)', size=34), T(6, '[k:Column-major]:  Loc(A[i][j]) = Base + w × (j × R + i)', size=34))
beat(p, f'''Example: A has ten rows and twenty columns, base address one thousand, and each element takes four bytes. Find the address of A five seven, with indexes starting at zero.
Row major: one thousand plus four times, five into twenty plus seven, which is one thousand four hundred and twenty eight. Column major: one thousand plus four times, seven into ten plus five, which is one thousand three hundred.''',
     T(8, 'A[10][20], Base = 1000, w = 4 bytes, find A[5][7]', size=34, color='black'),
     T(9, f'Row-major: 1000 + 4 × (5 × 20 + 7) = [h:{addr(1000, 4, 10, 20, 5, 7)}]', size=34),
     T(10, f'Column-major: 1000 + 4 × (7 × 10 + 5) = [h:{addr(1000, 4, 10, 20, 5, 7, "col")}]', size=34))

BS = [3, 8, 12, 17, 25, 31, 42, 56, 63, 77]; bi, bst = bsearch_trace(BS, 42)
p = page('Linear & Binary Search', 2)
beat(p, '''Linear search checks each element one by one. It works on any list, and takes order n time in the worst case.
Binary search works only on a sorted array. It compares with the middle element, and throws away half of the array each time, so it takes order log n time.''',
     T(0, '[k:Linear search]: check one by one;  O(n);  any list', size=34), T(1, '[k:Binary search]: sorted array only;  halve each step;  [h:O(log n)]', size=34))
beat(p, f'''Let's search for forty two in this sorted array of ten numbers. Low is zero, high is nine, so mid is four, which holds twenty five. Forty two is bigger, so low becomes five.
Now mid is seven, holding fifty six. Forty two is smaller, so high becomes six. Mid is five, holding thirty one, so low becomes six. Mid is six, holding forty two. Found in four comparisons.''',
     Stamp(1650, 140, 'NUMERICAL'),
     Cells(300, 340, BS, 100, 58, 30, fills={bi: 'yellow'}), *[T(0, str(i), x=340 + 100 * i, y=440, size=24, color='grey') for i in range(10)],
     Tab(300, 480, [160, 160, 160, 260], 52, [['low', 'high', 'mid', 'A[mid]']] + [[str(a), str(b), str(c), str(d_)] for a, b, c, d_ in bst], size=29, colors={(len(bst), 3): 'green'}),
     T(0, 'mid = ⌊(low + high) / 2⌋', x=1160, y=560, size=32, color='red'), T(0, f'found at index {bi} ✓', x=1160, y=620, size=32, color='green'),
     T(0, 'max comparisons ≈ ⌊log₂ n⌋ + 1', x=1160, y=680, size=30))

# ===================================================================================== CH 3
p = chapter(3)
beat(p, 'Chapter three. Stacks and queues.')

pf, prow = to_postfix('A+B*C-D/E'); ev, erow = eval_postfix('6 2 3 + - 3 8 2 / + *')
p = page('Stack: Operations & Infix to Postfix', 3)
beat(p, '''A stack is a list where insertion and deletion happen at one end, called the top. It follows last in, first out. Push adds an element, pop removes the top, and peek reads the top.
Pushing onto a full stack is called overflow, and popping from an empty stack is underflow. Stacks are used for function calls, undo, expression conversion and recursion.''',
     T(0, '[h:Stack] = LIFO;  push, pop, peek — all O(1)', size=34), T(1, 'overflow (push on full),  underflow (pop on empty)', size=32),
     *[Box(1500, 260 + 60 * k, 160, 60, v, 'blue', size=28) for k, v in enumerate(['30', '20', '10'])], T(0, '<- top', x=1680, y=300, size=28, color='red'))
beat(p, f'''The most asked stack question: convert infix to postfix. Scan left to right. Operands go straight to the output. An operator pops all operators of higher or equal precedence first, then is pushed.
For A plus B times C minus D by E: times has higher precedence than plus, so it waits on the stack. When minus comes, it pops times and plus. The answer is A B C times plus D E divide minus.''',
     Stamp(1650, 140, 'NUMERICAL'),
     Tab(180, 360, [150, 200, 300], 46, [['symbol', 'stack', 'postfix']] + [[v.replace('*', '×') for v in r] for r in prow], size=27, colors={(len(prow), 2): 'red'}),
     T(0, f'A+B×C-D/E  =>  [h:{pf.replace("*", "×")}]', x=900, y=420, size=36, color='black'))
beat(p, f'''To evaluate a postfix expression, push numbers, and when you see an operator, pop two numbers, apply it, and push the result. For six two three plus minus three eight two divide plus times,
we get six minus five, which is one, then three plus four, which is seven, and finally one times seven, which is seven.''',
     T(0, 'Evaluate: 6 2 3 + - 3 8 2 / + ×', x=900, y=540, size=32, color='black'),
     T(0, '6 - (2 + 3) = 1;   3 + 8 / 2 = 7', x=900, y=600, size=32), T(0, f'1 × 7 = [h:{ev}]', x=900, y=660, size=36, color='red'))

p = page('Queues: Linear, Circular & Deque', 3)
beat(p, '''A queue inserts at the rear and deletes from the front. It follows first in, first out, like a ticket line. Enqueue adds, and dequeue removes.
In a simple array queue, the space at the front is wasted after deletions. A circular queue fixes this by wrapping around: rear becomes rear plus one, mod the size.''',
     T(0, '[h:Queue] = FIFO;  enqueue at rear, dequeue at front', size=34),
     Cells(300, 300, ['', '', 10, 20, 30, ''], 100, 58, 30), T(0, 'front', x=515, y=392, size=26, color='green'), T(0, 'rear', x=725, y=392, size=26, color='red'),
     T(4, '[k:Circular queue]: rear = (rear + 1) mod N;  full when (rear + 1) mod N = front', size=32))
beat(p, '''A deque, or double ended queue, allows insertion and deletion at both ends. A priority queue removes the element with the highest priority first, and is usually built with a heap.''',
     Stamp(1650, 140),
     Tab(180, 520, [360, 620, 520], 54, [['Type', 'Rule', 'Use'], ['Simple queue', 'insert rear, delete front', 'printer jobs'], ['Circular queue', 'wraps around, no wasted space', 'CPU scheduling'],
         ['Deque', 'insert & delete at both ends', 'undo / redo, sliding window'], ['Priority queue', 'highest priority leaves first', 'Dijkstra, heaps']], size=29,
         colors={(r, 0): 'red' for r in range(1, 5)}))

# ===================================================================================== CH 4
p = chapter(4)
beat(p, 'Chapter four. Linked lists.')

def llnode(x, y, v, dbl=False, col='blue'):
    if not dbl: return [Box(x, y, 90, 60, str(v), col, size=28), Box(x + 90, y, 50, 60, None, col)]
    return [Box(x, y, 40, 60, None, col), Box(x + 40, y, 90, 60, str(v), col, size=28), Box(x + 130, y, 40, 60, None, col)]
p = page('Singly Linked List', 4)
beat(p, '''A linked list stores elements in nodes. Each node has data and a pointer to the next node. The nodes need not be next to each other in memory, so the list can grow and shrink easily.
The head points to the first node, and the last node points to null.''',
     T(0, '[h:Node] = data + next pointer;  head -> ... -> NULL', size=34), T(0, 'head', x=190, y=L(2) + 20, size=28, color='red'),
     Arr(262, L(2) + 10, 336, L(2) + 10),
     *sum([llnode(340 + 230 * k, L(2) - 20, v) for k, v in enumerate([10, 20, 30])], []), *[Arr(455 + 230 * k, L(2) + 10, 566 + 230 * k, L(2) + 10) for k in range(2)],
     T(0, 'NULL', x=1010, y=L(2) + 20, size=28, color='grey'), Arr(915, L(2) + 10, 1002, L(2) + 10))
beat(p, '''To insert at the beginning, make the new node point to the head, then move head to the new node. That takes constant time. To insert after a node p, set new next to p next, then p next to new.
To delete a node, change the previous node's pointer to skip it. Searching needs a walk from the head, so it takes order n time.''',
     Stamp(1650, 140),
     T(5, 'Insert at front:  new->next = head;  head = new        O(1)', size=32), T(6, 'Insert after p:  new->next = p->next;  p->next = new', size=32),
     T(7, 'Delete after p:  p->next = p->next->next', size=32), T(8, 'Search / access k-th element: [r:O(n)] (no direct index)', size=32))
beat(p, '''Array versus linked list: an array gives direct access but has a fixed size and costly insertion in the middle. A linked list grows freely and inserts easily, but needs extra memory for pointers and has no direct access.''',
     Tab(180, 720, [380, 560, 560], 52, [['', 'Array', 'Linked list'], ['access k-th', 'O(1)', 'O(n)'], ['insert / delete (middle)', 'O(n) shifting', 'O(1) after finding'], ['size', 'fixed', 'dynamic']], size=28,
         colors={(r, 0): 'red' for r in range(1, 4)}))

p = page('Doubly & Circular Linked Lists', 4)
beat(p, '''In a doubly linked list, each node has two pointers, previous and next. So we can move in both directions, and deleting a given node is easy. The cost is one extra pointer per node.''',
     T(0, '[h:Doubly linked list]: prev + data + next  (both directions)', size=34),
     *sum([llnode(300 + 300 * k, L(2) - 20, v, True) for k, v in enumerate([10, 20, 30])], []),
     *[Arr(470 + 300 * k, L(2) - 5, 600 + 300 * k, L(2) - 5) for k in range(2)], *[Arr(600 + 300 * k, L(2) + 25, 470 + 300 * k, L(2) + 25) for k in range(2)])
beat(p, '''In a circular linked list, the last node points back to the first node instead of null. There is no end, so we can loop around forever. It is used in round robin scheduling and music playlists.''',
     T(5, '[h:Circular linked list]: last node -> first node', size=34),
     *sum([llnode(300 + 230 * k, L(7) - 20, v) for k, v in enumerate([10, 20, 30])], []), *[Arr(415 + 230 * k, L(7) + 10, 526 + 230 * k, L(7) + 10) for k in range(2)],
     Arr(875, L(7) + 42, 345, L(7) + 44, curve=-110, color='red'), T(0, 'last -> first', x=1000, y=L(7) + 20, size=28, color='red'))
beat(p, '''Applications of linked lists: representing polynomials, where each node stores a coefficient and a power, implementing stacks and queues, adjacency lists for graphs, and memory management.''',
     Stamp(1650, 140),
     T(11, 'Applications: polynomials (coef, exp), stacks & queues, adjacency lists, memory', size=32),
     T(12, '5x³ + 4x + 2:  [5|3] -> [4|1] -> [2|0] -> NULL', size=32, color='green'))

# ===================================================================================== CH 5
p = chapter(5)
beat(p, 'Chapter five. Trees and binary search trees.')

p = page('Trees & Binary Tree Traversals', 5)
beat(p, '''A tree is a non linear structure with a root and child nodes, and no cycles. A node with no children is a leaf. The height is the longest path from the root to a leaf.
A binary tree allows at most two children. In a full binary tree, every node has zero or two children. In a complete binary tree, all levels are full except possibly the last, which fills from the left.''',
     T(0, '[k:root, parent, child, leaf, degree, level, height]', size=32), T(1, 'Binary tree: ≤ 2 children;  max nodes at level i = 2^i', size=32),
     T(2, '[k:Full]: 0 or 2 children   [k:Complete]: last level filled left to right', size=32),
     T(3, 'height h  =>  at most 2^(h+1) - 1 nodes', size=32, color='green'),
     BinTree(TREE, 'A', 1180, 560, 560, dy=100)[0])
beat(p, f'''Traversal means visiting every node once. In preorder, we visit the root, then left, then right. In inorder: left, root, right. In postorder: left, right, root.
And level order visits level by level, using a queue. For this tree, preorder is A B D E G C F, and inorder is D B G E A C F.''',
     Stamp(1650, 140, 'NUMERICAL'),
     T(6, f'[k:Preorder] (Root L R):   {" ".join(pre(TREE, "A"))}', size=34), T(7, f'[k:Inorder] (L Root R):    {" ".join(ino(TREE, "A"))}', size=34),
     T(8, f'[k:Postorder] (L R Root):  {" ".join(post(TREE, "A"))}', size=34), T(9, f'[k:Level order]:  {" ".join(level(TREE, "A"))}', size=34))
beat(p, '''Postorder is D G E B F C A. A tip: given inorder with preorder, or inorder with postorder, we can build the tree uniquely.
A binary tree can be stored in an array: the children of index i are at two i plus one and two i plus two.''',
     T(11, 'inorder + (preorder or postorder)  =>  unique tree', size=32, color='red'), T(12, 'Array storage: children of i at 2i + 1, 2i + 2;  parent at ⌊(i - 1)/2⌋', size=32))

br, bt = bst_insert([50, 30, 70, 20, 40, 60, 80])
bt2 = {k: list(v) for k, v in bt.items()}; bt2[50] = [40, 70]; del bt2[30]; bt2[40] = [20, None]
p = page('Binary Search Tree', 5)
beat(p, '''A binary search tree keeps every key in the left subtree smaller than the node, and every key in the right subtree larger. So an inorder traversal gives the keys in sorted order.
Insert fifty, thirty, seventy, twenty, forty, sixty, eighty. Each key goes left if smaller and right if larger.''',
     T(0, '[h:BST]: left < node < right;  inorder = sorted order', size=34), T(1, 'Insert: 50, 30, 70, 20, 40, 60, 80', size=34, color='black'),
     BinTree(bt, 50, 300, 390, 640, dy=100)[0])
beat(p, '''Search, insert and delete take order h time, where h is the height. That is log n for a balanced tree, but n for a skewed tree, like inserting sorted keys one by one.''',
     Stamp(1650, 140), T(8, 'search / insert / delete = O(h):  balanced [g:O(log n)], skewed [r:O(n)]', size=32))
beat(p, '''Deletion has three cases. A leaf is simply removed. A node with one child is replaced by that child. A node with two children is replaced by its inorder successor, the smallest key in its right subtree,
or its inorder predecessor. Deleting thirty, which has two children, we can replace it with its inorder predecessor forty.''',
     T(10, 'Delete: 1) leaf -> remove   2) one child -> replace by child', size=32), T(11, '3) two children -> replace by inorder successor / predecessor', size=32),
     T(0, 'delete 30:', x=1100, y=L(1), size=30, color='red'), BinTree(bt2, 50, 1150, 390, 560, dy=100, colors={40: 'red'})[0])

# ===================================================================================== CH 6
p = chapter(6)
beat(p, 'Chapter six. Graphs. Traversals, topological sorting, minimum spanning trees and shortest paths.')

ug = {'A': (1180, 330), 'B': (1400, 330), 'C': (1180, 540), 'D': (1620, 260), 'E': (1620, 470), 'F': (1400, 600)}
p = page('Graph Representation, BFS & DFS', 6)
beat(p, '''A graph has vertices and edges. In a directed graph, edges have a direction. In a weighted graph, edges have a cost. The degree of a vertex is the number of edges touching it.
We store a graph as an adjacency matrix, which uses order V squared space, or as adjacency lists, which use order V plus E space and are better for sparse graphs.''',
     T(0, 'G = (V, E);  directed / undirected;  weighted', size=32), T(1, '[k:Adjacency matrix]: V × V, O(V²)  ·  [k:Adjacency list]: O(V + E)', size=32),
     *sum([WEdge(ug[a], ug[b]) for a in UG for b in UG[a] if a < b], []), *[Node(ug[v], v) for v in ug])
beat(p, f'''Breadth first search visits vertices level by level using a queue. From A, B F S visits A, then its neighbours B and C, then D, E and F. Depth first search goes as deep as possible first, using a stack or recursion.
From A, D F S visits A, B, D, then backtracks to E, F, and C. Both take order V plus E time.''',
     Stamp(1650, 140, 'MOST ASKED'),
     T(4, f'[h:BFS] (queue):  {" ".join(bfs(UG, "A"))}', size=36), T(5, f'[h:DFS] (stack):  {" ".join(dfs(UG, "A"))}', size=36), T(6, 'both O(V + E)', size=32, color='green'),
     T(8, 'BFS: shortest path in unweighted graphs, level order', size=30), T(9, 'DFS: cycle detection, topological sort, connected components', size=30))

dag = {'1': (1180, 420), '2': (1380, 300), '3': (1380, 540), '4': (1580, 420), '5': (1580, 640), '6': (1780, 520)}
p = page('Topological Sorting', 6)
beat(p, '''Topological sorting orders the vertices of a directed acyclic graph, so that for every edge from u to v, u comes before v. It is used for task scheduling and course prerequisites.
Kahn's algorithm: find all vertices with in degree zero, remove one, reduce the in degree of its neighbours, and repeat.''',
     T(0, '[h:Topological sort]: DAG only; u before v for every edge u -> v', size=34), T(1, "[k:Kahn]: repeatedly remove a vertex of in-degree 0", size=32),
     *sum([DEdge(dag[a], dag[b]) for a in DAG for b in DAG[a]], []), *[Node(dag[v], v) for v in dag])
beat(p, f'''In this graph, only vertex one has in degree zero. Remove it, and two and three become free. Remove two, then three, then four and five, and finally six.
One valid order is one, two, three, four, five, six. A graph can have more than one topological order, and if there is a cycle, no order exists.''',
     Stamp(1650, 140, 'NUMERICAL'), T(4, f'Order: [h:{"  ".join(kahn(DAG))}]', size=38), T(5, 'another valid order: 1 3 5 2 4 6', size=32, color='green'),
     T(6, 'cycle  =>  no topological order;   O(V + E)', size=32, color='red'))

kr = kruskal('ABCDE', WG); pr = prim('ABCDE', WG); dd, dp_, dst = dijkstra('ABCDE', WG)
wg = {'A': (1160, 560), 'B': (1400, 360), 'C': (1400, 760), 'D': (1680, 360), 'E': (1780, 720)}
WAT = {('C', 'D'): .3, ('B', 'E'): .3}
p = page('Minimum Spanning Tree: Prim & Kruskal', 6)
beat(p, '''A spanning tree connects all vertices with exactly V minus one edges and no cycle. The minimum spanning tree has the smallest total weight. Kruskal's algorithm sorts all edges by weight,
and adds the smallest edge that does not form a cycle. It uses a disjoint set to check for cycles, and takes order E log E time.''',
     T(0, '[h:MST]: V - 1 edges, no cycle, minimum total weight', size=34), T(1, "[k:Kruskal]: sort edges, add smallest that makes no cycle;  O(E log E)", size=32),
     *sum([WEdge(wg[a], wg[b], w, at=WAT.get((a, b), .5)) for w, a, b in WG], []), *[Node(wg[v], v) for v in wg])
beat(p, f'''Here: B C with one, A C with two, D E with two. A B with four would make a cycle, so skip it. Then B D with five. Four edges for five vertices, so we stop. The total weight is ten.
Prim's algorithm grows the tree from one vertex, always adding the cheapest edge to a new vertex. From A, it adds A C, C B, B D and D E: the same total, ten.''',
     Stamp(1650, 140, 'NUMERICAL'),
     Tab(180, 360, [150, 100, 280], 48, [['Edge', 'w', 'Kruskal']] + [[a + b, str(w), '[g:add]' if ok else '[r:skip (cycle)]'] for a, b, w, ok in kr[:5]], size=28),
     *sum([WEdge(wg[a], wg[b], None, 'green', width=9) for a, b, w, ok in kr if ok], []), *[Node(wg[v], v) for v in wg],
     T(9, f'Kruskal total = [h:{sum(w for a, b, w, ok in kr if ok)}]', size=34), T(10, f"[k:Prim] from A: {', '.join(a + b for a, b, w in pr)}  =>  total {sum(w for a, b, w in pr)}", size=32),
     T(11, "Prim: O(E log V) with a heap", size=30, color='green'))

p = page("Single Source Shortest Path: Dijkstra", 6)
beat(p, '''Dijkstra's algorithm finds the shortest path from one source to all vertices, when all edge weights are non negative. It keeps a distance for every vertex. At each step, it picks the unvisited vertex with the smallest distance,
and relaxes its edges: if going through it is shorter, update the neighbour's distance.''',
     T(0, "[h:Dijkstra]: non-negative weights;  greedy;  O((V + E) log V) with heap", size=32), T(1, 'relax(u, v): if d[u] + w < d[v] then d[v] = d[u] + w', size=32, color='black'),
     *sum([WEdge(wg[a], wg[b], w, at=WAT.get((a, b), .5)) for w, a, b in WG], []), *[Node(wg[v], v) for v in wg])
beat(p, f'''From A: C gets two and B gets four. Visit C: B improves to three, D becomes ten, and E becomes twelve. Visit B: D improves to eight, and E improves to nine. Then D, and E.
So the shortest distances are: B three, C two, D eight, and E nine, through A, C, B, E.''',
     Stamp(1650, 140, 'NUMERICAL'),
     Tab(180, 380, [110, 180, 120, 120, 120, 120], 50, [['Step', 'Visited', 'B', 'C', 'D', 'E']] + [[str(i + 1), vis, *[('∞' if t[v] == math.inf else str(t[v])) for v in 'BCDE']] for i, (vis, t) in enumerate(dst)], size=27),
     *[T(0, f'A -> {v}: {path(dp_, v)} = [h:{dd[v]}]', x=180, y=L(10) + 44 * i, size=30, color='black') for i, v in enumerate('BCDE')],
     T(0, 'negative edges -> Bellman-Ford O(VE);  all pairs -> Floyd-Warshall O(V³)', x=180, y=L(14) + 6, size=28, color='red'))

# ===================================================================================== CH 7
p = chapter(7)
beat(p, 'Chapter seven. Divide and conquer, and solving recurrences.')

ml = merge_sort_levels([38, 27, 43, 3, 9, 82, 10]); pa, pq, prow2 = partition([2, 8, 7, 1, 3, 5, 6, 4])
p = page('Merge Sort & Quick Sort', 7)
beat(p, '''Divide and conquer has three steps: divide the problem into smaller parts, conquer each part recursively, and combine the results. Binary search, merge sort and quick sort all use it.
Merge sort splits the array into halves until each part has one element, then merges the sorted halves back. It always takes order n log n time, and needs order n extra space.''',
     T(0, '[h:Divide -> Conquer -> Combine]', size=36), T(1, '[k:Merge sort]: T(n) = 2T(n/2) + n = [h:Θ(n log n)] always;  stable;  O(n) space', size=31),
     *[T(0, '   '.join('[' + ' '.join(map(str, part)) + ']' for part in lv), x=200, y=L(2) + 10 + 46 * i, size=28, color='black' if i < 3 else 'green') for i, lv in enumerate(ml)],
     T(0, 'merge up:  [3 27 38 43]  [9 10 82]  ->  [h:[3 9 10 27 38 43 82]]', x=200, y=L(2) + 10 + 46 * 4, size=28, color='red'))
beat(p, f'''Quick sort picks a pivot, and partitions the array so that smaller elements go left and larger elements go right. Then it sorts both sides. Using the last element four as the pivot,
two eight seven one three five six four becomes two one three, four, seven five six eight. The average time is n log n, but the worst case is n squared, when the pivot is always the smallest or largest.''',
     Stamp(1650, 140, 'NUMERICAL'),
     T(8, '[k:Quick sort]: partition around a pivot, sort both sides, in place', size=32),
     M(180, L(9) + 6, 'before: 2 8 7 1 3 5 6 [4]', size=32), M(180, L(10) + 10, 'after:  ' + ' '.join(map(str, pa[:pq])) + ' [' + str(pa[pq]) + '] ' + ' '.join(map(str, pa[pq + 1:])), size=32, color='blue'),
     T(11, 'average [g:O(n log n)];  worst [r:O(n²)] (sorted input, bad pivot);  not stable', size=31),
     T(12, 'fix: random pivot / median of three', size=30, color='green'))

ms, mi, mj = max_subarray(STOCK); sP, sC = strassen2([[1, 3], [7, 5]], [[6, 8], [4, 2]])
p = page('Maximum Subarray & Strassen', 7)
beat(p, f'''The maximum subarray problem finds the continuous part of an array with the largest sum. It models buying and selling a stock at the best days. Divide and conquer splits the array in the middle.
The best subarray is either fully in the left half, fully in the right half, or it crosses the middle. This gives order n log n time.''',
     Stamp(1650, 140, 'NUMERICAL'), T(0, '[h:Max subarray]: left half, right half, or [k:crossing the middle]  =>  Θ(n log n)', size=31),
     Cells(180, 270, STOCK, 98, 54, 26, fills={k: 'yellow' for k in range(mi, mj + 1)}),
     T(3, f'Best: A[{mi + 1}..{mj + 1}] = 18 + 20 - 7 + 12 = [h:{ms}]', size=34), T(4, "(Kadane's algorithm does it in O(n))", size=30, color='green'))
beat(p, '''Strassen's algorithm multiplies two n by n matrices with seven multiplications of half size matrices instead of eight. So the recurrence is seven T of n by two plus order n squared,
which gives n to the power log two of seven, about n to the power two point eight one. That beats the normal n cubed.''',
     T(6, '[k:Strassen]: 7 products instead of 8:  T(n) = 7T(n/2) + Θ(n²) = [h:Θ(n^2.81)]', size=31))
beat(p, f'''Example with two by two matrices: one three, seven five, times six eight, four two. The seven products are six, eight, seventy two, minus ten, forty eight, minus twelve, and minus eighty four.
Combining them gives eighteen, fourteen, sixty two, sixty six, which matches normal multiplication.''',
     M(180, L(8) + 6, 'A = |1 3|   B = |6 8|', size=32), M(180, L(9) + 6, '    |7 5|       |4 2|', size=32),
     T(0, 'P1 = a(f - h) = 6    P2 = (a + b)h = 8    P3 = (c + d)e = 72', x=820, y=L(8) + 6, size=27),
     T(0, 'P4 = d(g - e) = -10   P5 = (a + d)(e + h) = 48', x=820, y=L(9) + 6, size=27), T(0, 'P6 = (b - d)(g + h) = -12   P7 = (a - c)(e + f) = -84', x=820, y=L(10) + 6, size=27),
     T(11, f'C11 = P5 + P4 - P2 + P6 = {sC[0][0]}   C12 = P1 + P2 = {sC[0][1]}', size=30, color='black'), T(12, f'C21 = P3 + P4 = {sC[1][0]}   C22 = P5 + P1 - P3 - P7 = {sC[1][1]}', size=30, color='black'),
     T(13, f'C = [h:[[{sC[0][0]}, {sC[0][1]}], [{sC[1][0]}, {sC[1][1]}]]] ✓', size=32))

p = page('Solving Recurrences: Master Method', 7)
beat(p, '''Recursive algorithms give recurrences. In the substitution method, we guess the answer and prove it by induction. In the recursion tree method, we draw the tree of costs and add each level.
For example, T of n equals two T of n by two plus n gives a tree with log n levels, each costing n, so the total is n log n.''',
     T(0, '[k:Substitution]: guess, then prove by induction', size=32), T(1, '[k:Recursion tree]: sum the cost of every level', size=32),
     T(2, 'T(n) = 2T(n/2) + n:  log n levels × n per level = [h:Θ(n log n)]', size=32, color='black'))
beat(p, '''The master method solves T of n equals a T of n by b plus f of n directly. Compare f of n with n to the power log base b of a. Case one: f is smaller, so the answer is n to the log b a.
Case two: they are equal, so multiply by log n. Case three: f is larger, and the regularity condition holds, so the answer is f of n.''',
     Stamp(1650, 140, 'MOST ASKED'), T(4, 'T(n) = a T(n/b) + f(n);   compare f(n) with [h:n^(log_b a)]', size=34),
     T(5, '1) f smaller  =>  Θ(n^(log_b a))', size=32), T(6, '2) f equal  =>  Θ(n^(log_b a) · log n)', size=32), T(7, '3) f larger (+ regularity)  =>  Θ(f(n))', size=32))
beat(p, '''Examples. Nine T of n by three plus n: n to the log three of nine is n squared, which is bigger than n, so case one gives n squared. T of two n by three plus one: n to the zero is one, equal to f, so case two gives log n.
Three T of n by four plus n log n: n to the zero point seven nine is smaller than n log n, so case three gives n log n. Binary search, T of n by two plus one, is log n.''',
     Stamp(1650, 520, 'NUMERICAL'),
     Tab(180, 640, [520, 300, 200, 420], 52, [['Recurrence', 'n^(log_b a)', 'case', 'Answer'], ['9T(n/3) + n', 'n²', '1', '[h:Θ(n²)]'], ['T(2n/3) + 1', '1', '2', '[h:Θ(log n)]'],
         ['3T(n/4) + n log n', 'n^0.79', '3', '[h:Θ(n log n)]'], ['2T(n/2) + n  (merge sort)', 'n', '2', '[h:Θ(n log n)]'], ['T(n/2) + 1  (binary search)', '1', '2', '[h:Θ(log n)]']], size=28))

# ===================================================================================== CH 8
p = chapter(8)
beat(p, 'Chapter eight. The greedy method.')

fv, fo = frac_knap([(60, 10), (100, 20), (120, 30)], 50); jslot, jprofit, jrows = job_seq(JOBS)
p = page('Greedy: Fractional Knapsack & Job Sequencing', 8)
beat(p, '''A greedy algorithm makes the choice that looks best right now, and never goes back. It works when the problem has the greedy choice property and optimal substructure.
Fractional knapsack: we can take parts of items. Sort items by value per weight, and take the best first. With capacity fifty, and items sixty for ten, one hundred for twenty, and one hundred twenty for thirty,
we take the first two fully, and twenty out of thirty of the third, for a total value of two hundred forty.''',
     Stamp(1650, 140, 'NUMERICAL'), T(0, '[h:Greedy]: best choice now, never undo;  needs greedy-choice + optimal substructure', size=30),
     Tab(180, 300, [140, 150, 150, 160, 220], 50, [['Item', 'Value', 'Weight', 'v / w', 'Take']] + [[f'I{i + 1}', str(v), str(w), str(v // w), f'{t}/{w}'] for i, (v, w, t) in enumerate(fo)], size=28),
     T(0, f'W = 50  =>  60 + 100 + 120 × 20/30 = [h:{fv:.0f}]', x=1060, y=420, size=34, color='black'), T(0, '(0/1 knapsack needs DP!)', x=1060, y=480, size=30, color='red'))
beat(p, f'''Job sequencing with deadlines: each job takes one unit of time and gives a profit if done by its deadline. Sort jobs by profit, and put each one in the latest free slot before its deadline.
J1 goes to slot two, J3 to slot one, J4 and J2 are rejected because slot one is taken, and J5 goes to slot three. The order is J3, J1, J5, with profit one hundred forty two.''',
     Tab(180, 640, [130, 150, 170, 240], 48, [['Job', 'Profit', 'Deadline', 'Result']] + [[n, str(pr_), str(d_), r] for n, pr_, d_, r in jrows], size=27,
         colors={(i + 1, 3): ('red' if r == 'rejected' else 'green') for i, (_, _, _, r) in enumerate(jrows)}),
     T(0, f'Schedule: {" -> ".join(jslot)}', x=1060, y=760, size=32), T(0, f'Profit = [h:{jprofit}]', x=1060, y=820, size=36, color='red'))

hc, hm, ht = huffman(HUFF)
p = page('Huffman Codes & Matroids', 8)
beat(p, '''Huffman coding gives shorter codes to more frequent characters, to compress data. Repeatedly take the two smallest frequencies, join them under a new node, and put the sum back.
For frequencies a forty five, b thirteen, c twelve, d sixteen, e nine, f five: first join f and e into fourteen, then c and b into twenty five, then fourteen and d into thirty, then twenty five and thirty into fifty five, and finally a and fifty five.''',
     Stamp(1650, 140, 'NUMERICAL'), T(0, 'merge two smallest, repeat;  left = 0, right = 1', size=32),
     T(1, 'a:45  b:13  c:12  d:16  e:9  f:5   (thousands)', size=32, color='black'),
     *[T(0, f'{a} + {b} = {c}', x=180, y=L(2) + 10 + 44 * i, size=30) for i, (a, b, c) in enumerate(hm)])
hp = {'100': (1350, 280), 'a': (1150, 400), '55': (1550, 400), '25': (1420, 520), '30': (1700, 520), 'c': (1340, 650), 'b': (1500, 650), '14': (1620, 650), 'd': (1800, 650), 'f': (1560, 780), 'e': (1690, 780)}
hed = [('100', 'a', '0'), ('100', '55', '1'), ('55', '25', '0'), ('55', '30', '1'), ('25', 'c', '0'), ('25', 'b', '1'), ('30', '14', '0'), ('30', 'd', '1'), ('14', 'f', '0'), ('14', 'e', '1')]
beat(p, f'''Reading the tree, left is zero and right is one. a gets zero, c gets one zero zero, b gets one zero one, d gets one one one, f gets one one zero zero, and e gets one one zero one.
The total is two hundred twenty four thousand bits, compared to three hundred thousand with a fixed three bit code. Huffman takes order n log n time with a heap.''',
     *sum([WEdge(hp[a], hp[b], lab, 'black', r=30, size=24, off=18) for a, b, lab in hed], []),
     *[Node(hp[k], k if k.isdigit() else f'{k}', 'green' if not k.isdigit() else 'blue', r=30, size=24) for k in hp],
     T(9, '  '.join(f'{k}={hc[k]}' for k in 'abcdef'), size=30, color='black'), T(10, f'bits = Σ f × len = [h:{sum(HUFF[k] * len(v) for k, v in hc.items())},000] vs 300,000 fixed', size=31))
beat(p, '''Why does greedy work? A matroid is a structure where greedy always gives the best answer. It has a ground set and a family of independent subsets, with two rules: every subset of an independent set is independent,
and the exchange property. Finding a minimum spanning tree is a greedy algorithm on the graphic matroid.''',
     T(12, '[k:Matroid] (S, I): hereditary + exchange property  =>  greedy is optimal', size=31), T(13, 'e.g. graphic matroid: independent = acyclic edge sets  ->  Kruskal', size=30, color='green'))

# ===================================================================================== CH 9
p = chapter(9)
beat(p, 'Chapter nine. Dynamic programming. The most asked numericals come from here.')

KN = [(2, 3), (3, 4), (4, 5), (5, 6)]; KT, kpick = knap01(KN, 5)
p = page('Dynamic Programming & 0/1 Knapsack', 9)
beat(p, '''Dynamic programming solves a problem by combining answers to overlapping subproblems, and stores each answer in a table so it is never computed twice. It needs two properties: optimal substructure and overlapping subproblems.
Greedy picks one choice, but D P tries all choices and keeps the best.''',
     T(0, '[h:DP] = optimal substructure + overlapping subproblems -> store in a table', size=32), T(1, 'top-down (memoization)  or  bottom-up (tabulation)', size=32))
beat(p, f'''In the zero one knapsack, each item is taken fully or not at all. K of i comma w is the best value using the first i items with capacity w. It is the max of skipping item i, or taking it if it fits.
For items of weight two, three, four, five with values three, four, five, six, and capacity five, the table gives seven, by taking items one and two.''',
     Stamp(1650, 140, 'NUMERICAL'), T(3, 'K[i][w] = max( K[i-1][w],  v_i + K[i-1][w - w_i] )', size=34, color='red'),
     T(4, 'items (w, v): (2, 3) (3, 4) (4, 5) (5, 6);   W = 5', size=32, color='black'),
     Tab(180, 500, [170] + [90] * 6, 50, [['i \\ w', '0', '1', '2', '3', '4', '5']] + [[f'{i}' + (f' ({KN[i - 1][0]},{KN[i - 1][1]})' if i else '')] + [str(v) for v in KT[i]] for i in range(5)], size=27,
         fills={(5, 6): 'yellow'}),
     T(0, f'max value = [h:{KT[-1][-1]}]', x=1060, y=600, size=36, color='red'), T(0, f'items taken: {", ".join(map(str, kpick))}', x=1060, y=660, size=32),
     T(0, 'O(nW) time', x=1060, y=720, size=30, color='green'))

rr, rs = rod(ROD, 10); mm, msplit, mpar = matrix_chain([5, 4, 6, 2, 7])
p = page('Rod Cutting & Matrix Chain Multiplication', 9)
beat(p, f'''Rod cutting: given prices for each length, cut a rod of length n to get the most money. r of n is the max over the first cut i of price i plus r of n minus i.
With the textbook prices, a rod of four gives ten by cutting into two plus two, and a rod of seven gives eighteen.''',
     Stamp(1650, 140, 'NUMERICAL'), T(0, '[h:r(n) = max (p_i + r(n - i))],  1 ≤ i ≤ n', size=34),
     Tab(180, 300, [140] + [90] * 10, 48, [['length', *map(str, range(1, 11))], ['price', *map(str, ROD)], ['r(n)', *map(str, rr[1:])]], size=27, colors={(2, c): 'red' for c in range(1, 11)}))
beat(p, f'''Matrix chain multiplication finds the cheapest order to multiply a chain of matrices. m i j is the min over k of m i k plus m k plus one j plus p i minus one times p k times p j.
For dimensions five by four, four by six, six by two, and two by seven, the minimum is one hundred fifty eight scalar multiplications, with the order A1 times A2 A3, then times A4.''',
     T(6, '[h:m[i][j] = min (m[i][k] + m[k+1][j] + p_(i-1) p_k p_j)]', size=32, color='black'), T(7, 'p = 5, 4, 6, 2, 7   (A1: 5×4, A2: 4×6, A3: 6×2, A4: 2×7)', size=31),
     Tab(180, 680, [100] + [140] * 4, 50, [['m', '1', '2', '3', '4']] + [[str(i)] + [str(mm[i][j]) if j >= i else '' for j in range(1, 5)] for i in range(1, 5)], size=28, fills={(1, 4): 'yellow'}),
     T(0, f'min cost = [h:{mm[1][4]}]', x=1000, y=760, size=36, color='red'), T(0, f'order: {mpar}', x=1000, y=820, size=34), T(0, 'O(n³) time', x=1000, y=880, size=30, color='green'))

lc, ls = lcs('ABCBDAB', 'BDCABA')
p = page('Dynamic Programming: LCS', 9)
beat(p, '''The longest common subsequence of two strings is the longest sequence that appears in both, in order, but not necessarily together. If the characters match, c i j is the diagonal value plus one.
Otherwise, it is the max of the value above and the value to the left.''',
     Stamp(1650, 140, 'MOST ASKED'), T(0, 'match: c[i][j] = c[i-1][j-1] + 1;   else max(c[i-1][j], c[i][j-1])', size=32, color='black'))
beat(p, f'''For X equals A B C B D A B, and Y equals B D C A B A, we fill the table row by row. The bottom right cell is four. Tracing back through the matches gives the L C S: B C B A.
The time and space are order m times n.''',
     Tab(300, 300, [90] * 8, 50, [['', '', *'BDCABA']] + [[('' if i == 0 else 'ABCBDAB'[i - 1]), *[str(v) for v in lc[i]]] for i in range(8)], size=27, hdr=True,
         fills={(8, 7): 'yellow'}, colors={(0, c): 'red' for c in range(2, 8)}),
     T(0, f'X = ABCBDAB,  Y = BDCABA', x=1140, y=380, size=32, color='black'), T(0, f'LCS length = [h:{lc[-1][-1]}]', x=1140, y=450, size=36, color='red'),
     T(0, f'LCS = [h:{ls}]', x=1140, y=520, size=36, color='red'), T(0, 'O(mn) time & space', x=1140, y=590, size=30, color='green'))

oc, otree = obst(); tc, ttour, _ = tsp_dp(TSP)
def ttree(tr, out=None, par=None):
    out = {} if out is None else out
    if tr is None: return out
    k, l, r = tr; out[k] = (l[0] if l else None, r[0] if r else None)
    ttree(l, out); ttree(r, out); return out
ot = ttree(otree)
p = page('Optimal BST & Travelling Salesman', 9)
beat(p, '''An optimal binary search tree minimizes the expected search cost, when each key has a known search probability. Frequently searched keys should be near the root.
D P tries every key as the root of each range. For the textbook example with five keys, the minimum expected cost is two point seven five, with k two as the root.''',
     Stamp(1650, 140, 'NUMERICAL'), T(0, 'e[i][j] = min over root r ( e[i][r-1] + e[r+1][j] + w(i, j) )', size=31, color='black'),
     T(1, 'p = .15 .10 .05 .10 .20,  q = .05 .10 .05 .05 .05 .10', size=30), T(2, f'expected cost = [h:{oc}],  root = k2', size=34),
     BinTree(ot, 'k2', 1150, 420, 520, dy=90, r=32, size=24)[0])
beat(p, f'''The travelling salesman problem finds the shortest tour that visits every city once and returns home. D P uses g of i comma S, the shortest path from i through all cities in S back to the start.
For this four city cost matrix, the best tour is one, two, four, three, one, with cost thirty five. D P takes order n squared times two to the n, which is much better than n factorial.''',
     T(8, '[h:g(i, S) = min over j in S ( c_ij + g(j, S - {j}) )]', size=32, color='black'),
     Tab(180, 700, [90] * 5, 48, [['', '1', '2', '3', '4']] + [[str(i + 1), *map(str, r)] for i, r in enumerate(TSP)], size=28),
     T(0, f'tour: {" -> ".join(map(str, ttour))}', x=760, y=760, size=34), T(0, f'cost = 10 + 10 + 9 + 6 = [h:{tc}]', x=760, y=820, size=34, color='red'),
     T(0, 'O(n² 2ⁿ) vs brute force O(n!)', x=760, y=880, size=30, color='green'))

# ===================================================================================== CH 10
p = chapter(10)
beat(p, 'Chapter ten. Backtracking.')

Q4 = nqueens(4)
def board(x, y, sol, cs=62):
    out = [Box(x + c * cs, y + r * cs, cs, cs, None, 'black', fill=('grey' if (r + c) % 2 else None)) for r in range(4) for c in range(4)]
    out += [T(0, 'Q', x=x + (sol[r] - 1) * cs + 18, y=y + r * cs + 46, size=36, font='bold', color='red') for r in range(4)]
    return out
p = page('Backtracking: n-Queens', 10)
beat(p, '''Backtracking builds a solution one step at a time. When a partial solution cannot lead to an answer, it goes back and tries the next choice. It explores a state space tree,
and prunes branches that break the rules.''',
     T(0, '[h:Backtracking]: build step by step;  dead end -> go back, try next option', size=33), T(1, 'state space tree + bounding (pruning)', size=32))
beat(p, f'''The n Queens problem places n queens on an n by n board, so that no two attack each other: no two in the same row, column or diagonal.
For four queens, place queen one in column one, queen two in column three, then queen three has no safe column, so we backtrack. Continuing, we find two solutions: two four one three, and three one four two.''',
     Stamp(1650, 140, 'MOST ASKED'),
     T(3, 'safe if no queen in same column or diagonal:  |c1 - c2| ≠ |r1 - r2|', size=31, color='black'),
     *board(260, 470, Q4[0]), *board(700, 470, Q4[1]),
     T(0, f'({",".join(map(str, Q4[0]))})', x=320, y=780, size=32, color='green'), T(0, f'({",".join(map(str, Q4[1]))})', x=760, y=780, size=32, color='green'),
     T(0, '4-queens: 2 solutions', x=1200, y=560, size=34), T(0, f'8-queens: [h:{len(nqueens(8))}] solutions', x=1200, y=630, size=34))

cg = {'A': (1200, 420), 'B': (1450, 300), 'C': (1450, 560), 'D': (1700, 420)}
cs3 = colourings(CG, 3); col_names = {1: 'red', 2: 'green', 3: 'blue'}
p = page('Graph Colouring', 10)
beat(p, '''Graph colouring gives each vertex a colour so that no two adjacent vertices share a colour. The m colouring problem asks: can we colour the graph with at most m colours?
Backtracking colours vertices one by one, and backtracks when no colour is safe. The smallest m that works is the chromatic number.''',
     T(0, '[h:m-colouring]: adjacent vertices get different colours', size=34), T(1, 'chromatic number χ(G) = smallest m that works', size=32),
     *sum([WEdge(cg[a], cg[b]) for a in CG for b in CG[a] if a < b], []), *[Node(cg[v], v, 'black') for v in cg])
beat(p, f'''In this graph, B and C are joined, and both touch A and D. So two colours are not enough, there are zero ways. With three colours, there are six valid colourings.
One is A red, B green, C blue, and D red. So the chromatic number is three. N Queens and graph colouring both take exponential time in the worst case.''',
     Stamp(1650, 140, 'NUMERICAL'), T(4, f'm = 2: [r:{len(colourings(CG, 2))} ways]   m = 3: [g:{len(cs3)} ways]  =>  χ = 3', size=34),
     *[Node(cg[v], v, col_names[cs3[0][v]]) for v in cg],
     T(5, 'A = red, B = green, C = blue, D = red', size=32, color='black'), T(7, 'worst case: O(mⁿ)', size=30, color='green'))

# ===================================================================================== CH 11
p = chapter(11)
beat(p, 'Chapter eleven. Now the M Tech advanced data structures. B trees and Fibonacci heaps.')

bt_root, bsnaps = btree_insert([10, 20, 5, 6, 12, 30, 7, 17])
p = page('B-Trees', 11)
beat(p, '''A B tree is a balanced search tree designed for disks, where reading one block is slow. Each node holds many keys, so the tree is short and needs very few disk reads. Databases and file systems use B trees.
With minimum degree t, every node except the root has at least t minus one keys and at most two t minus one keys. All leaves are at the same depth.''',
     Stamp(1650, 140, 'MOST ASKED'), T(0, '[h:B-tree] (min degree t): t - 1 ≤ keys ≤ 2t - 1  (root: ≥ 1)', size=32),
     T(1, 'internal node with k keys has k + 1 children;  all leaves at same depth', size=31),
     T(2, 'height h ≤ log_t ((n + 1) / 2)  =>  search, insert, delete = O(t log_t n)', size=31, color='red'))
beat(p, '''To insert, go down to a leaf. If a node on the way is full, with two t minus one keys, split it first: the middle key moves up to the parent, and the node becomes two nodes. The tree grows taller only when the root splits.
Let's insert ten, twenty, five, six, twelve, thirty, seven and seventeen, with t equals two, so each node holds at most three keys.''',
     T(4, 'insert: go to leaf;  split full nodes on the way;  middle key moves up', size=31),
     T(5, 't = 2 (max 3 keys):  insert 10, 20, 5, 6, 12, 30, 7, 17', size=32, color='black'))
beat(p, f'''After ten, twenty and five, the root five ten twenty is full. Inserting six splits it: ten moves up, with five and twenty as children. Then six, twelve, thirty and seven fill the leaves.
Inserting seventeen goes to the full leaf twelve twenty thirty, which splits, sending twenty up. The final tree has root ten twenty, and leaves five six seven, twelve seventeen, and thirty.''',
     T(0, 'after 5:', x=180, y=L(7) + 20, size=28, color='grey'), BTreeDraw(bsnaps[2][1], 460, L(7) - 16),
     T(0, 'after 6 (root splits):', x=780, y=L(7) + 20, size=28, color='grey'), BTreeDraw(bsnaps[3][1], 1400, L(7) - 16, dy=100),
     T(0, 'final (after 17):', x=180, y=L(11) + 10, size=28, color='red'), BTreeDraw(bsnaps[-1][1], 900, L(10) + 10, dy=100),
     T(0, 'B+ tree: data only in leaves, leaves linked', x=1300, y=L(13) + 20, size=26, color='green'))

p = page('Fibonacci Heaps', 11)
beat(p, '''A Fibonacci heap is a collection of min heap ordered trees, kept in a circular root list, with a pointer to the minimum root. It is lazy: insert and union just add trees to the root list,
so they take constant time. The real work happens only during extract min.''',
     T(0, '[h:Fibonacci heap]: root list of heap-ordered trees + min pointer', size=34), T(1, 'lazy: insert & union just add to the root list', size=32),
     *[Ell(300 + 170 * k, 380, 80, 80, str(v), 'red' if v == 3 else 'blue', size=28) for k, v in enumerate([23, 7, 3, 17, 24])],
     *[Arr(380 + 170 * k, 420, 470 + 170 * k, 420, both=True) for k in range(4)], T(0, 'min', x=630, y=350, size=28, color='red'), Arr(650, 355, 650, 378, 'red'),
     Ln([(840, 460), (800, 530)], 'black', 3), Ln([(840, 460), (880, 530)], 'black', 3), Ell(760, 530, 70, 70, '18', size=26), Ell(850, 530, 70, 70, '39', size=26))
beat(p, '''Extract min removes the minimum root, adds its children to the root list, and then consolidates: trees with the same degree are linked until all roots have different degrees. That costs order log n amortized.
Decrease key cuts the node from its parent if the heap order breaks, and uses cascading cuts with marked nodes, in constant amortized time.''',
     T(8, '[k:Extract-min]: remove min, add children to root list, [h:consolidate] (link equal degrees)', size=30),
     T(9, '[k:Decrease-key]: cut from parent + cascading cuts (marked nodes)', size=30))
beat(p, '''Here is the comparison. These fast bounds make Dijkstra's algorithm run in order E plus V log V, and Prim's algorithm too.''',
     Stamp(1650, 140, 'MOST ASKED'),
     Tab(180, 740, [400, 300, 300, 520], 50, [['Operation', 'Binary heap', 'Binomial heap', 'Fibonacci heap (amortized)'], ['insert', 'O(log n)', 'O(log n)', '[h:O(1)]'], ['find-min', 'O(1)', 'O(log n)', 'O(1)'],
         ['extract-min', 'O(log n)', 'O(log n)', 'O(log n)'], ['decrease-key', 'O(log n)', 'O(log n)', '[h:O(1)]']], size=27, colors={(r, 0): 'red' for r in range(1, 5)}))

# ===================================================================================== CH 12
p = chapter(12)
beat(p, 'Chapter twelve. Disjoint sets and hash tables.')

dsu = dsu_run(6, [(1, 2), (3, 4), (5, 6), (2, 4), (4, 6)])
p = page('Disjoint Sets: Union-Find', 12)
beat(p, '''A disjoint set data structure keeps a collection of non overlapping sets. Make set creates a set with one element. Find returns the representative of an element's set. And union joins two sets.
It is used in Kruskal's algorithm and for finding connected components. We store each set as a tree, where each node points to its parent, and the root is the representative.''',
     T(0, '[h:MAKE-SET, FIND-SET, UNION];  forest of trees, root = representative', size=32), T(1, "uses: Kruskal's MST, connected components", size=31))
beat(p, '''Two tricks make it fast. Union by rank attaches the shorter tree under the taller one. Path compression makes every node on a find path point directly to the root.
With both, a sequence of m operations takes order m alpha of n, where alpha is the inverse Ackermann function, which is at most four in practice. So it is almost constant time.''',
     Stamp(1650, 140, 'MOST ASKED'), T(3, '[k:Union by rank]: smaller-rank root under larger-rank root', size=32),
     T(4, '[k:Path compression]: every node on the find path points to the root', size=32), T(5, 'both  =>  O(m α(n)),  α(n) ≤ 4  =>  almost O(1)', size=34, color='red'))
beat(p, f'''Example: start with one to six, then union one two, three four, five six, two four, and four six. The parent array after each step is shown here. In the end, every element has root one.''',
     Tab(180, 560, [220] + [100] * 6, 48, [['after', *map(str, range(1, 7))]] + [[f'U{a}{b}', *map(str, par)] for (a, b), par, rk in dsu], size=28,
         colors={(len(dsu), c): 'green' for c in range(1, 7)}),
     T(0, 'parent array', x=1100, y=620, size=30, color='black'), T(0, 'final: one set {1..6}, root 1', x=1100, y=680, size=30, color='red'))

lin, _ = open_address(HK, 11, 'linear'); quad, _ = open_address(HK, 11, 'quadratic'); dbl, _ = open_address(HK, 11, 'double')
p = page('Hash Tables', 12)
beat(p, '''A hash table stores keys in an array using a hash function h of k, so search, insert and delete take order one time on average. The division method uses k mod m, where m is a prime not close to a power of two.
When two keys hash to the same slot, we have a collision. Chaining keeps a linked list in each slot. The load factor alpha is n by m, and a search takes order one plus alpha.''',
     T(0, '[h:h(k) = k mod m]   (m prime);   multiplication: ⌊m (kA mod 1)⌋', size=32), T(1, '[k:Chaining]: list in each slot;  load factor α = n/m;  search O(1 + α)', size=32))
beat(p, '''Open addressing keeps all keys in the table itself, and probes for another slot on a collision. Linear probing tries h plus i. Quadratic probing adds c one i plus c two i squared.
Double hashing adds i times a second hash function, which spreads keys best.''',
     Stamp(1650, 140, 'NUMERICAL'), T(3, 'linear: (h(k) + i) mod m   quadratic: (h(k) + i + 3i²) mod m', size=31),
     T(4, 'double: (h1(k) + i·h2(k)) mod m,  h2(k) = 1 + (k mod (m - 1))', size=31))
beat(p, f'''Insert ten, twenty two, thirty one, four, fifteen, twenty eight, seventeen, eighty eight and fifty nine into a table of size eleven. With linear probing, fifteen hits slot four, which is taken, so it moves to five.
Fifty nine needs five probes and lands in slot eight. Here are all three final tables.''',
     T(6, 'keys: 10, 22, 31, 4, 15, 28, 17, 88, 59;   m = 11', size=31, color='black'),
     Tab(180, 640, [220] + [110] * 11, 52, [['slot', *map(str, range(11))], ['linear', *[str(v) if v else '' for v in lin]], ['quadratic', *[str(v) if v else '' for v in quad]],
         ['double', *[str(v) if v else '' for v in dbl]]], size=27, colors={(r, 0): 'red' for r in range(1, 4)}))

# ===================================================================================== CH 13
p = chapter(13)
beat(p, 'Chapter thirteen. Randomized algorithms and amortized analysis.')

p = page('Randomized Algorithms: Hiring Problem', 13)
beat(p, '''A randomized algorithm uses random choices. Its running time is studied as an expected value. The hiring problem: you interview n candidates in random order, and hire each one who is better than everyone before.
Each hire costs money. How many people do you hire on average?''',
     T(0, '[h:Randomized algorithm]: uses random choices;  expected running time', size=33), T(1, 'Hiring problem: hire candidate i if better than all before', size=32))
beat(p, f'''Use indicator random variables. X i is one if candidate i is hired, and zero otherwise. Candidate i is hired only if they are the best of the first i, which has probability one over i.
So the expected number of hires is the sum of one over i, which is the harmonic number H n, about the natural log of n. For ten candidates, that is about two point nine three hires, instead of ten in the worst case.''',
     Stamp(1650, 140, 'MOST ASKED'), T(3, '[k:Indicator] X_i = 1 if candidate i is hired;   E[X_i] = Pr = 1/i', size=33),
     T(4, '[h:E[X] = Σ 1/i = H_n ≈ ln n]', size=38, color='red'), T(5, f'n = 10:  H₁₀ = {harmonic(10):.2f} hires (worst case: 10)', size=34),
     T(6, 'hiring cost: O(c_h ln n) expected', size=32))
beat(p, '''Randomized quick sort picks a random pivot, so no particular input is always bad. Its expected running time is n log n for every input. Algorithms that are always correct but have random running time are called Las Vegas algorithms.
Those that are fast but may be wrong with small probability are called Monte Carlo algorithms.''',
     T(8, '[k:Randomized quicksort]: random pivot  =>  expected O(n log n) for every input', size=31),
     T(9, '[k:Las Vegas]: always correct, random time   [k:Monte Carlo]: fixed time, may err', size=31))

p = page('Amortized Analysis', 13)
beat(p, '''Amortized analysis finds the average cost per operation over a whole sequence of operations, in the worst case. It is not about probability. Some operations are costly, but they are rare.
In aggregate analysis, we find the total cost of n operations, and divide by n.''',
     T(0, '[h:Amortized cost] = worst-case total cost / n   (no probability)', size=34), T(1, '[k:Aggregate]: total for n operations ÷ n', size=32))
beat(p, f'''Example: a stack with push, pop, and multipop, which pops k items. One multipop can cost order n. But each item is popped at most once after it is pushed, so n operations cost at most two n. That is order one each.
Another example: a binary counter. Incrementing it sixteen times flips thirty one bits in total, less than two n. So each increment costs order one amortized.''',
     Stamp(1650, 140, 'NUMERICAL'), T(3, 'Stack with MULTIPOP: each item popped ≤ once  =>  n ops ≤ 2n  =>  [h:O(1)] each', size=31),
     T(4, f'Binary counter: 16 increments flip {counter_flips(16)} bits < 2n  =>  [h:O(1)] each', size=31),
     M(1200, L(6) + 6, '0000 -> 0001 -> 0010', size=28), M(1200, L(7) + 6, '-> 0011 -> 0100 ...', size=28), T(0, 'bit i flips n/2^i times', x=1200, y=L(8) + 6, size=28, color='green'))
beat(p, '''In the accounting method, we charge each operation an amortized cost, and extra charge is saved as credit for later. For the stack, charge two for push, one to pay for the push and one saved to pay for its pop later.
Pop and multipop are charged zero. The credit never goes negative, so the total is at most two n. The third method, the potential method, stores the credit as the potential energy of the data structure.''',
     T(10, '[k:Accounting]: push = 2 (1 now + 1 credit),  pop = 0,  multipop = 0', size=31), T(11, 'credit ≥ 0 always  =>  total ≤ 2n', size=31),
     T(12, '[k:Potential]: ĉ = c + Φ(after) - Φ(before)', size=31, color='green'))

# ===================================================================================== CH 14
p = chapter(14)
beat(p, "Chapter fourteen. Advanced graph algorithms. Johnson's algorithm, and maximum flow.")

jh, jrew = johnson()
jp = {1: (1150, 430), 2: (1460, 270), 3: (1770, 430), 4: (1650, 740), 5: (1270, 740)}
JLAB = {(1, 3): dict(at=.8, side=-1), (4, 1): dict(at=.3)}
p = page("Johnson's Algorithm", 14)
beat(p, '''Johnson's algorithm finds shortest paths between all pairs of vertices in a sparse graph, even with negative edge weights, as long as there is no negative cycle. Running Dijkstra from every vertex is fast,
but Dijkstra cannot handle negative edges. So Johnson first reweights the edges to make them all non negative, without changing which paths are shortest.''',
     T(0, "[h:Johnson]: all-pairs shortest paths, sparse graphs, negative edges OK", size=32), T(1, 'reweight -> all w ≥ 0 -> run Dijkstra from each vertex', size=31),
     *sum([DEdge(jp[u], jp[v], w, **JLAB.get((u, v), {})) for u, v, w in JE], []), *[Node(jp[v], v) for v in jp])
beat(p, f'''Add a new vertex s with zero weight edges to every vertex. Run Bellman Ford from s to get h of v: zero, minus one, minus five, zero, minus four. Then each new weight is w plus h of u minus h of v.
For example, the edge from four to three had weight minus five, and becomes minus five plus zero minus minus five, which is zero. All new weights are non negative.''',
     Stamp(1650, 140, 'NUMERICAL'), T(4, "1) add s, edges s -> v with weight 0;  Bellman-Ford from s", size=30),
     T(5, '   h = ' + ', '.join(f'h({v}) = {jh[v]}' for v in jh), size=30, color='black'),
     T(6, "2) [h:ŵ(u, v) = w(u, v) + h(u) - h(v)] ≥ 0", size=32, color='red'), T(7, '3) Dijkstra from every vertex', size=30),
     Tab(180, 680, [140] + [86] * 9, 48, [['edge', *[f'{u}{v}' for u, v, _ in JE]], ['w', *[str(w) for _, _, w in JE]], ['ŵ', *[str(w) for _, _, w in jrew]]], size=26,
         colors={(2, c): 'green' for c in range(1, 10)}),
     T(0, 'O(V E log V)', x=1200, y=L(13), size=30, color='green'))

fl, fpaths, freach, fcut = edmonds_karp()
fp = {'s': (1120, 520), 'v1': (1340, 340), 'v2': (1340, 700), 'v3': (1640, 340), 'v4': (1640, 700), 't': (1840, 520)}
p = page('Maximum Flow: Ford-Fulkerson', 14)
beat(p, '''A flow network is a directed graph where each edge has a capacity. Flow leaves the source s and arrives at the sink t. Flow on an edge cannot exceed its capacity, and at every other vertex, flow in equals flow out.
The Ford Fulkerson method keeps finding an augmenting path from s to t in the residual graph, and pushes as much flow along it as the smallest residual capacity allows.''',
     Stamp(1650, 140, 'MOST ASKED'), T(0, 'capacity constraint + flow conservation', size=31), T(1, '[h:Ford-Fulkerson]: augment along s -> t paths in the residual graph', size=31),
     *sum([DEdge(fp[u], fp[v], c, curve=(-50 if (u, v) == ('v2', 'v1') else (50 if (u, v) == ('v3', 'v2') else 0))) for (u, v), c in FN.items()], []), *[Node(fp[v], v, size=22) for v in fp])
beat(p, f'''Using breadth first search for the shortest augmenting path, called Edmonds Karp: the first path s, v1, v3, t carries twelve. The second, s, v2, v4, t, carries four. The third, s, v2, v4, v3, t, carries seven.
No more paths exist, so the max flow is twenty three.''',
     *[T(3 + i, f'path {i + 1}: {pth}   +{b}', size=31, color='black') for i, (pth, b) in enumerate(fpaths)],
     T(6, f'max flow = 12 + 4 + 7 = [h:{fl}]', size=36, color='red'), T(7, '[k:Edmonds-Karp] (BFS paths): O(V E²)', size=30))
beat(p, f'''The max flow min cut theorem says the maximum flow equals the capacity of the minimum cut. Here the cut separating s, v1, v2, v4 from v3 and t crosses edges with capacities twelve, seven and four, which add to twenty three.
Maximum bipartite matching is solved by adding a source to the left side and a sink to the right side, with all capacities one. The max flow equals the size of the largest matching.''',
     T(9, '[h:max flow = min cut]', size=36, color='red'), T(10, f'cut {{s, v1, v2, v4}} | {{v3, t}}:  ' + ' + '.join(str(c) for _, _, c in fcut) + f' = {sum(c for _, _, c in fcut)}', size=30),
     T(12, '[k:Bipartite matching]: source -> L, R -> sink, all capacities 1;  max flow = max matching', size=29))

# ===================================================================================== CH 15
p = chapter(15)
beat(p, 'Chapter fifteen. Multithreaded algorithms.')

p = page('Dynamic Multithreading: Work & Span', 15)
beat(p, '''Multithreaded algorithms run on many processors at once. We use three keywords. Spawn starts a sub call that can run in parallel. Sync waits for all spawned children to finish. And parallel for runs loop iterations in parallel.
The computation is drawn as a directed acyclic graph of tasks.''',
     T(0, '[h:spawn]: run child in parallel   [h:sync]: wait for children   [h:parallel for]', size=31),
     M(180, L(2) + 6, 'P-FIB(n):  if n ≤ 1 return n', size=30), M(180, L(3) + 6, '  x = spawn P-FIB(n - 1)', size=30), M(180, L(4) + 6, '  y = P-FIB(n - 2);  sync;  return x + y', size=30))
beat(p, '''Work, T one, is the total time on one processor. Span, T infinity, is the longest path in the D A G, the time with unlimited processors. Parallelism is work divided by span: the maximum useful number of processors.
A greedy scheduler on P processors finishes in at most T one over P plus T infinity.''',
     Stamp(1650, 140, 'MOST ASKED'), T(6, '[k:Work] T₁ = total time on 1 processor   [k:Span] T∞ = critical path', size=31),
     T(7, '[h:Parallelism = T₁ / T∞]', size=36, color='red'), T(8, 'Greedy scheduler:  T_P ≤ T₁/P + T∞;   speedup = T₁ / T_P', size=32))
beat(p, '''Example: if the work is one hundred and the span is ten, the parallelism is ten. On four processors, the time is at most twenty five plus ten, which is thirty five. Using more than ten processors gives no extra speedup.
For P fib, the work is exponential, but the span is only order n, so the parallelism is huge.''',
     Stamp(1650, 520, 'NUMERICAL'), T(10, 'T₁ = 100, T∞ = 10:  parallelism = [h:10]', size=33), T(11, 'P = 4:  T₄ ≤ 100/4 + 10 = [h:35]', size=33),
     T(12, 'P-FIB: work Θ(φⁿ), span Θ(n)', size=31, color='green'))

p = page('Multithreaded Matrix Multiply & Merge Sort', 15)
beat(p, '''Multithreaded matrix multiplication uses parallel for loops over rows and columns. The simple version has work n cubed and span n, so parallelism n squared.
The divide and conquer version spawns eight half size products and adds them in parallel. Its work is n cubed and its span is log squared n.''',
     Tab(180, 260, [560, 260, 300, 340], 54, [['Algorithm', 'Work T₁', 'Span T∞', 'Parallelism'], ['P-SQUARE-MATRIX-MULTIPLY', 'Θ(n³)', 'Θ(n)', 'Θ(n²)'],
         ['P-MATRIX-MULTIPLY-RECURSIVE', 'Θ(n³)', 'Θ(log² n)', '[h:Θ(n³ / log² n)]']], size=28))
beat(p, '''For merge sort, simply spawning the two recursive sorts gives span order n, because the merge is still serial. So the parallelism is only log n.
Multithreaded merge, called P merge, splits the merge itself using binary search, so its span is log squared n. Then the full sort has work n log n and span log cubed n.''',
     Stamp(1650, 140, 'MOST ASKED'),
     Tab(180, 560, [560, 260, 300, 340], 54, [['Algorithm', 'Work T₁', 'Span T∞', 'Parallelism'], ['MERGE-SORT′ (serial merge)', 'Θ(n log n)', 'Θ(n)', 'Θ(log n)'],
         ['P-MERGE-SORT (P-MERGE)', 'Θ(n log n)', 'Θ(log³ n)', '[h:Θ(n / log² n)]']], size=28),
     T(13, 'race condition: two strands write the same memory -> avoid (determinacy race)', size=29, color='red'))

# ===================================================================================== CH 16
p = chapter(16)
beat(p, 'Chapter sixteen. String matching. Rabin Karp and K M P are asked in almost every exam.')

rkp, rkh = rabin_karp('2359023141526739921', '31415')
p = page('Naive & Rabin-Karp', 16)
beat(p, '''String matching finds every position where a pattern P of length m occurs in a text T of length n. The naive method tries every shift, and compares character by character. It takes order n minus m plus one times m in the worst case.''',
     T(0, 'find all shifts s where T[s+1 .. s+m] = P', size=32), T(1, '[k:Naive]: try every shift;  O((n - m + 1) m)', size=32),
     M(180, L(2) + 10, 'T: a c a a b c', size=32), M(180, L(3) + 12, 'P:     a a b', size=32, color='blue'), T(0, '(shift 2 ✓)', x=640, y=L(3) + 12, size=32, color='green'))
beat(p, f'''Rabin Karp treats the pattern as a number, and compares hash values mod q first. Only when the hashes match does it check the characters. The window hash is updated in constant time as it slides.
For the text two three five nine zero two three one four one five two six seven three nine nine two one, and pattern three one four one five, with q equals thirteen, the pattern hash is seven.''',
     Stamp(1650, 140, 'NUMERICAL'), T(5, '[h:Rabin-Karp]: compare p = P mod q with each window t_s mod q', size=32),
     T(6, 't_(s+1) = (d (t_s - T[s+1]·h) + T[s+m+1]) mod q,   h = d^(m-1) mod q', size=29, color='black'),
     T(7, 'T = 2359023141526739921,  P = 31415,  q = 13  =>  p = 31415 mod 13 = 7', size=30))
beat(p, f'''Two windows have hash seven: three one four one five, a valid match at shift six, and six seven three nine nine, which is a spurious hit, a false alarm caught by the character check.
The expected time is order n plus m, but the worst case is order n minus m plus one times m.''',
     *[T(9 + i, f'shift {s}: {w} mod 13 = 7  ->  ' + ('[g:valid match ✓]' if ok else '[r:spurious hit ✗]'), size=32) for i, (s, w, ok) in enumerate(rkh)],
     T(12, 'expected O(n + m);  worst O((n - m + 1) m)', size=31, color='green'))

FA = fa_table('ababaca', 'abc'); PI = prefix_fn('ababaca')
p = page('Finite Automata & KMP', 16)
beat(p, f'''String matching with a finite automaton builds a machine with m plus one states for the pattern. State q means the last q characters read match the first q characters of the pattern. Reaching state m means a match.
Here is the transition table for the pattern a b a b a c a. After building it, matching takes just order n time.''',
     T(0, 'state q = length of longest prefix of P that is a suffix of text read', size=31),
     Tab(180, 290, [130] + [100] * 8, 46, [['δ', *map(str, range(8))]] + [[a, *[str(FA[q][a]) for q in range(8)]] for a in 'abc'], size=27, colors={(r, c): 'blue' for r in range(1, 4) for c in range(1, 9)}),
     T(0, 'P = ababaca', x=1140, y=340, size=34, color='black'), T(0, 'matching: [h:Θ(n)]', x=1140, y=400, size=32), T(0, 'building: O(m³ |Σ|)', x=1140, y=460, size=30, color='red'))
beat(p, f'''The Knuth Morris Pratt algorithm avoids building the full automaton. It uses the prefix function pi: for each position q, pi of q is the length of the longest proper prefix of the pattern that is also a suffix of the first q characters.
For a b a b a c a, pi is zero, zero, one, two, three, zero, one.''',
     Stamp(1650, 140, 'MOST ASKED'), T(7, '[h:KMP prefix function] π[q] = longest proper prefix that is also a suffix', size=31),
     Tab(180, 640, [130] + [90] * 7, 48, [['q', *map(str, range(1, 8))], ['P[q]', *'ababaca'], ['π[q]', *map(str, PI)]], size=28, colors={(2, c): 'red' for c in range(1, 8)}))
beat(p, f'''On a mismatch, K M P does not move back in the text. It shifts the pattern using pi, and continues. So the total time is order n plus m. In the text b a c b a b a b a c a a b, the pattern is found at shift four.''',
     T(0, 'mismatch at q  ->  q = π[q]  (text pointer never moves back)', x=1060, y=700, size=28),
     T(0, f'T = bacbababacaab  ->  match at shift [h:{kmp("bacbababacaab", "ababaca")[0]}]', x=1060, y=760, size=28, color='black'), T(0, '[h:O(n + m)]', x=1060, y=820, size=34, color='red'))

# ===================================================================================== CH 17
p = chapter(17)
beat(p, 'Chapter seventeen. N P completeness, and approximation algorithms.')

p = page('P, NP & NP-Completeness', 17)
beat(p, '''P is the class of problems solvable in polynomial time, like sorting and shortest paths. N P is the class of problems whose solutions can be verified in polynomial time. Every problem in P is also in N P.
Whether P equals N P is still unsolved.''',
     T(0, '[h:P]: solvable in polynomial time   [h:NP]: verifiable in polynomial time', size=32), T(1, 'P ⊆ NP;   P = NP ?  (unsolved)', size=32, color='red'))
beat(p, '''A problem is N P hard if every N P problem reduces to it in polynomial time. It is N P complete if it is N P hard and also in N P. The first one was circuit satisfiability, and S A T by the Cook Levin theorem.
To prove a new problem is N P complete, show it is in N P, and reduce a known N P complete problem to it.''',
     Stamp(1650, 140, 'MOST ASKED'), T(3, '[k:NP-hard]: every NP problem reduces to it   [k:NP-complete] = NP-hard ∩ NP', size=31),
     T(4, 'Prove B is NPC: 1) B ∈ NP   2) known NPC A ≤p B', size=32),
     T(5, 'NPC: SAT, 3-SAT, clique, vertex cover, Hamiltonian cycle, TSP (decision), subset sum', size=29, color='black'),
     Ell(1080, 600, 520, 320, None, color='blue'), Ell(1120, 680, 200, 140, 'P', size=32, color='green'), T(0, 'NP', x=1330, y=650, size=32, color='blue'),
     Ell(1400, 560, 440, 380, None, color='red'), T(0, 'NP-hard', x=1650, y=700, size=28, color='red'), T(0, 'NPC', x=1450, y=770, size=28, color='red'))
beat(p, '''Remember the reduction chain from the textbook: circuit S A T, to S A T, to three S A T, which reduces to clique, then vertex cover, and also to Hamiltonian cycle and the travelling salesman problem.''',
     T(10, 'CIRCUIT-SAT -> SAT -> 3-SAT -> CLIQUE -> VERTEX-COVER', size=30, color='black'), T(11, '3-SAT -> HAM-CYCLE -> TSP;   VERTEX-COVER -> SUBSET-SUM', size=30, color='black'))

vcC, vcP = approx_vc(VCG); vmin = min_vc(VCG)
vp = {'a': (1120, 340), 'b': (1320, 340), 'c': (1520, 340), 'd': (1720, 340), 'e': (1420, 600), 'f': (1620, 600), 'g': (1820, 600)}
p = page('Approximation Algorithms', 17)
beat(p, '''For N P complete problems, we often accept a near optimal answer in polynomial time. An approximation algorithm has ratio rho if its answer is within a factor rho of the optimum.
For vertex cover, pick any edge, add both its ends to the cover, remove every edge they touch, and repeat.''',
     T(0, '[h:ratio ρ(n)]: max(C / C*, C* / C) ≤ ρ(n)', size=34), T(1, 'APPROX-VERTEX-COVER: pick edge (u, v), add u and v, delete their edges', size=30),
     *sum([WEdge(vp[a], vp[b], None, 'red' if (a, b) in vcP else 'black', width=(8 if (a, b) in vcP else 4)) for a, b in VCG], []), *[Node(vp[v], v) for v in vp])
beat(p, f'''In this graph, picking edges a b, c d and e f gives a cover of six vertices. The optimal cover is b, d, e, with three vertices. So the answer is at most two times the optimum: this is a two approximation.''',
     Stamp(1650, 140, 'NUMERICAL'), T(4, f'picked edges: {", ".join(a + b for a, b in vcP)}  ->  C = {{{", ".join(vcC)}}}  ({len(vcC)})', size=30),
     T(5, f'optimal C* = {{{", ".join(vmin)}}}  ({len(vmin)})   =>   [h:2-approximation]', size=30))
beat(p, '''For the travelling salesman problem with the triangle inequality, build a minimum spanning tree, walk it in preorder, and skip repeated cities. The tour costs at most twice the optimum, so it is also a two approximation.
Without the triangle inequality, no good approximation exists unless P equals N P.''',
     T(8, 'TSP (triangle inequality): MST -> preorder walk -> tour ≤ 2 × optimal', size=31),
     T(9, 'general TSP: no constant approximation unless P = NP', size=31, color='red'))

# ===================================================================================== CH 18
p = chapter(18)
beat(p, 'Chapter eighteen. Extra topics that many universities ask: A V L trees, red black trees, skip lists and Bloom filters.')

p = page('AVL Trees', 18)
beat(p, '''An A V L tree is a self balancing binary search tree. For every node, the balance factor, height of left subtree minus height of right subtree, must be minus one, zero or one. So the height is always order log n.
After an insert or delete, if a node becomes unbalanced, we fix it with rotations.''',
     Stamp(1650, 140, 'MOST ASKED'), T(0, '[h:Balance factor] = height(left) - height(right) ∈ {-1, 0, +1}', size=32), T(1, 'height = O(log n)  =>  all operations O(log n)', size=32))
beat(p, '''There are four cases. L L: insert into the left child's left subtree, fixed with one right rotation. R R: a left rotation. L R: a left rotation on the child, then a right rotation. And R L: a right then a left rotation.
For example, inserting thirty, twenty, ten makes thirty unbalanced with balance factor two, an L L case. One right rotation makes twenty the root, with ten and thirty as children.''',
     Tab(180, 380, [180, 600], 50, [['Case', 'Fix'], ['LL', 'single right rotation'], ['RR', 'single left rotation'], ['LR', 'left rotate child, then right rotate'], ['RL', 'right rotate child, then left rotate']], size=28,
         colors={(r, 0): 'red' for r in range(1, 5)}),
     BinTree({30: (20, None), 20: (10, None), 10: (None, None)}, 30, 1100, 420, 200, dy=90)[0], T(0, 'BF(30) = 2', x=1080, y=680, size=28, color='red'),
     Arr(1360, 520, 1480, 520, 'red', label='right rotate', size=24),
     BinTree({20: (10, 30), 10: (None, None), 30: (None, None)}, 20, 1540, 440, 260, dy=100, colors={20: 'green'})[0])

p = page('Red-Black Trees', 18)
beat(p, '''A red black tree is another balanced binary search tree. Every node is red or black. The root is black. Leaves, the nil nodes, are black. A red node cannot have a red child.
And every path from a node down to its leaves has the same number of black nodes, called the black height. These rules keep the height at most two log n plus one.''',
     Stamp(1650, 140, 'MOST ASKED'), N(0, 1, 'every node is red or black', size=31), N(1, 2, 'root is black;  NIL leaves are black', size=31), N(2, 3, 'red node -> both children black (no red-red)', size=31),
     N(3, 4, 'same black-height on every path', size=31), T(4, 'height ≤ 2 log(n + 1)', size=32, color='red'))
beat(p, '''Insert works like a B S T insert, with the new node coloured red. If its parent is also red, we fix it. If the uncle is red, recolour. If the uncle is black, rotate and recolour.
Inserting ten, twenty and thirty: thirty's parent twenty is red, and the uncle is nil, which is black. So we rotate left at ten and recolour, making twenty a black root with two red children.''',
     T(6, 'insert red;  red parent -> uncle red: [k:recolour];  uncle black: [k:rotate + recolour]', size=30),
     BinTree({20: (10, 30), 10: (None, None), 30: (None, None)}, 20, 1200, 560, 300, dy=100, colors={20: 'black', 10: 'red', 30: 'red'})[0],
     T(0, 'insert 10, 20, 30  ->', x=760, y=620, size=30, color='black'))
beat(p, '''Compare: A V L trees are more strictly balanced, so searches are faster. Red black trees need fewer rotations on insert and delete, so they are used in libraries, like Java's TreeMap and C plus plus map.''',
     Tab(180, 780, [380, 560, 560], 50, [['', 'AVL', 'Red-black'], ['balance', 'strict (BF ≤ 1)', 'looser (height ≤ 2 log n)'], ['best for', 'search-heavy', 'insert / delete-heavy (TreeMap)']], size=28))

p = page('Skip Lists & Bloom Filters', 18)
beat(p, '''A skip list is a sorted linked list with extra express lanes. Each node is promoted to the next level with probability one half. Searching starts at the top level and moves right, then drops down.
Search, insert and delete take order log n expected time, and it is much simpler to code than a balanced tree.''',
     T(0, '[h:Skip list]: sorted list + express levels (promote with prob. ½);  expected O(log n)', size=31),
     *[Cells(300 + 130 * i, L(lv) + 10, [v], 100, 48, 26) for lv, vals in ((2, [3, 25]), (3, [3, 12, 25, 40]), (4, [3, 7, 12, 19, 25, 31, 40])) for i, v in
       [(sorted([3, 7, 12, 19, 25, 31, 40]).index(v), v) for v in vals]],
     T(0, 'level 2', x=180, y=L(2) + 44, size=24, color='grey'), T(0, 'level 1', x=180, y=L(3) + 44, size=24, color='grey'), T(0, 'level 0', x=180, y=L(4) + 44, size=24, color='grey'))
beat(p, f'''A Bloom filter checks if an item might be in a set, using a bit array of size m and k hash functions. To add an item, set k bits to one. To check, see if all k bits are one.
It can give false positives but never false negatives. The false positive rate is about one minus e to the minus k n by m, to the power k. With m one thousand bits, n one hundred items and k seven, that is about zero point eight percent.''',
     Stamp(1650, 140, 'NUMERICAL'), T(6, '[h:Bloom filter]: m bits, k hash functions;  "maybe yes" or "definitely no"', size=31),
     T(7, 'false positive ≈ (1 - e^(-kn/m))^k', size=34, color='red'), T(8, f'm = 1000, n = 100, k = 7:  ≈ [h:{bloom_fp(1000, 100, 7) * 100:.2f}%]', size=34),
     T(10, 'Also asked: tries (prefix search), segment trees (range queries), binomial heaps, splay trees', size=29, color='green'))

# ===================================================================================== CH 19
p = chapter(19)
beat(p, "Chapter nineteen. Exam revision. If you're short on time, revise this page first.")

p = page('Complexity Cheat Sheet', 19)
beat(p, '''Here are the complexities you must remember. Sorting: merge sort is n log n always. Quick sort is n log n on average and n squared in the worst case. Heap sort is n log n. Bubble, insertion and selection sorts are n squared.''',
     Stamp(1650, 140, 'MOST ASKED'),
     Tab(180, 240, [420, 300, 300, 300], 48, [['Sorting', 'Best', 'Average', 'Worst'], ['Bubble / Insertion', 'O(n)', 'O(n²)', 'O(n²)'], ['Selection', 'O(n²)', 'O(n²)', 'O(n²)'],
         ['Merge sort', 'O(n log n)', 'O(n log n)', 'O(n log n)'], ['Quick sort', 'O(n log n)', 'O(n log n)', '[r:O(n²)]'], ['Heap sort', 'O(n log n)', 'O(n log n)', 'O(n log n)']], size=27))
beat(p, '''Graphs: B F S and D F S are V plus E. Dijkstra with a heap is E log V, Bellman Ford is V E, and Floyd Warshall is V cubed. Kruskal is E log E. Edmonds Karp is V E squared.
String matching: naive is n m, and K M P is n plus m. And dynamic programming: knapsack is n W, L C S is m n, and matrix chain is n cubed.''',
     Tab(180, 560, [420, 360, 420, 360], 48, [['Algorithm', 'Time', 'Algorithm', 'Time'], ['BFS / DFS', 'O(V + E)', 'Bellman-Ford', 'O(VE)'], ['Dijkstra (heap)', 'O(E log V)', 'Floyd-Warshall', 'O(V³)'],
         ['Kruskal / Prim', 'O(E log V)', 'Edmonds-Karp', 'O(VE²)'], ['KMP', 'O(n + m)', 'Rabin-Karp (exp.)', 'O(n + m)'], ['0/1 knapsack', 'O(nW)', 'LCS / matrix chain', 'O(mn) / O(n³)']], size=27))

p = page('Most Asked Exam Questions', 19)
qs = ['Asymptotic notations; master method', 'Infix to postfix; circular queue', 'Tree traversals; BST delete', 'BFS, DFS, topological sort, MST, Dijkstra',
      'Merge / quick sort; Strassen', 'Knapsack (fractional & 0/1); job sequencing', 'Huffman; LCS; matrix chain; OBST; TSP', 'n-Queens; graph colouring',
      'B-tree insertion; Fibonacci heap costs', 'Union-find; hashing (open addressing)', 'Hiring problem; amortized analysis', 'Johnson; max flow; KMP; NP-complete']
beat(p, '''Here are the most asked questions. For M C A: asymptotic notations, infix to postfix, tree traversals and B S T deletion, and the graph algorithms.''', *[T(k, f'{k + 1}. {q}', x=200, size=34) for k, q in enumerate(qs[:4])])
beat(p, '''Then sorting, the knapsack problems, the classic dynamic programming problems, and backtracking. These are asked in both M C A and M Tech exams.''',
     *[T(k, f'{k + 1}. {q}', x=200, size=34) for k, q in enumerate(qs) if 4 <= k < 8])
beat(p, '''For M Tech: B tree insertion and Fibonacci heaps, union find and hashing, the hiring problem and amortized analysis, and finally Johnson's algorithm, max flow, K M P and N P completeness.''',
     *[T(k, f'{k + 1}. {q}', x=200, size=34) for k, q in enumerate(qs) if k >= 8])
beat(p, '''One last exam tip. For every algorithm question, write the idea in one line, show a small worked example, and state the time complexity. That is exactly what examiners look for.''',
     T(13, 'Tip: [h:idea + worked example + time complexity] => full marks!', color='red'))

p = page('All the Best!', 19, kind='outro')
beat(p, '''That's the complete data structures and algorithms subject, basic and advanced. If this helped you, share it with your friends who have the exam,
and subscribe to TechVibe24 for more one shot videos. Tell me in the comments which subject you want next. All the best for your exam!''')

if __name__ == '__main__':
    json.dump({'pages': PAGES, 'chapters': CHAPTERS}, open('ds_script.json', 'w'), indent=1, ensure_ascii=False)
    nb = sum(len(p['beats']) for p in PAGES); nw = sum(len(b['say'].split()) for p in PAGES for b in p['beats'])
    print('pages', len(PAGES), 'beats', nb, 'words', nw, 'est minutes', round(nw / 150, 1))
