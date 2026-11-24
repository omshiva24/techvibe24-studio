'''YouTube chapters + English subtitles (SRT) from the final timeline.   python adv/gen_meta.py OUT_DIR'''
import json, os, re, sys, textwrap
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
tl = json.load(open(f'{HERE}/build/tl.json'))
def ts(t): return '%d:%02d:%02d' % (t // 3600, t % 3600 // 60, t % 60) if t >= 3600 else '%d:%02d' % (t // 60, t % 60)
chap = ['0:00 Introduction & contents']; LAST = [0]
for pg in tl['pages']:
    if pg['kind'] == 'chapter': chap.append(f"{ts(int(pg['t0']))} Ch {pg['num']}: {pg['title']}"); LAST[0] = pg['t0']
    NUM = {'Asymptotic Notations': 'Big O, Omega, Theta', 'Arrays & Address Calculation': 'Address calculation (numerical)', 'Linear & Binary Search': 'Binary search trace',
           'Stack: Operations & Infix to Postfix': 'Infix to postfix (numerical)', 'Queues: Linear, Circular & Deque': 'Circular queue & deque', 'Singly Linked List': 'Singly linked list',
           'Doubly & Circular Linked Lists': 'Doubly & circular lists', 'Trees & Binary Tree Traversals': 'Tree traversals (numerical)', 'Binary Search Tree': 'BST insert & delete',
           'Graph Representation, BFS & DFS': 'BFS & DFS', 'Topological Sorting': 'Topological sort', 'Minimum Spanning Tree: Prim & Kruskal': 'Prim & Kruskal (numerical)',
           'Single Source Shortest Path: Dijkstra': 'Dijkstra (numerical)', 'Merge Sort & Quick Sort': 'Merge sort & quick sort', 'Maximum Subarray & Strassen': 'Max subarray & Strassen',
           'Solving Recurrences: Master Method': 'Master method (numerical)', 'Greedy: Fractional Knapsack & Job Sequencing': 'Fractional knapsack & job sequencing',
           'Huffman Codes & Matroids': 'Huffman coding (numerical)', 'Dynamic Programming & 0/1 Knapsack': '0/1 knapsack (numerical)',
           'Rod Cutting & Matrix Chain Multiplication': 'Rod cutting & matrix chain', 'Dynamic Programming: LCS': 'LCS (numerical)', 'Optimal BST & Travelling Salesman': 'Optimal BST & TSP',
           'Backtracking: n-Queens': 'n-Queens', 'Graph Colouring': 'Graph colouring', 'B-Trees': 'B-tree insertion', 'Fibonacci Heaps': 'Fibonacci heaps',
           'Disjoint Sets: Union-Find': 'Union-find', 'Hash Tables': 'Hashing (open addressing)', 'Randomized Algorithms: Hiring Problem': 'Hiring problem',
           'Amortized Analysis': 'Amortized analysis', "Johnson's Algorithm": "Johnson's algorithm", 'Maximum Flow: Ford-Fulkerson': 'Max flow (Ford-Fulkerson)',
           'Dynamic Multithreading: Work & Span': 'Work, span & parallelism', 'Multithreaded Matrix Multiply & Merge Sort': 'Multithreaded matrix multiply & merge sort',
           'Naive & Rabin-Karp': 'Rabin-Karp (numerical)', 'Finite Automata & KMP': 'Finite automata & KMP', 'P, NP & NP-Completeness': 'P, NP & NP-complete',
           'Approximation Algorithms': 'Vertex cover approximation', 'AVL Trees': 'AVL trees', 'Red-Black Trees': 'Red-black trees', 'Skip Lists & Bloom Filters': 'Skip lists & Bloom filters',
           'Complexity Cheat Sheet': 'Complexity cheat sheet', 'Most Asked Exam Questions': 'Most asked questions'}
    if pg['kind'] == 'page' and pg['title'] in NUM and pg['t0'] - LAST[0] >= 12:      # YouTube rejects < and > in descriptions, so no '->' here
        chap.append(f"{ts(int(pg['t0']))}   • {NUM[pg['title']]}"); LAST[0] = pg['t0']
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
with open(f'{OUT}/DSA_OneShot_English.srt', 'w') as f:
    for i, (a, b, s) in enumerate(subs, 1): f.write(f'{i}\n{srt_t(a)} --> {srt_t(b)}\n{s}\n\n')
print('\n'.join(chap)); print('subtitles', len(subs))
