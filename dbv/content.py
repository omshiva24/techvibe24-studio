'''DBMS one-shot: narration beats + handwritten note elements for every page.
Markup inside text: [r:red] [g:green] [k:black] [h:yellow highlight] [p:pink highlight]'''
import json, math
from db_numericals import *

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
def Arr(x1, y1, x2, y2, color='black', label=None, lx=0, ly=-14, curve=0, head=True, size=28, both=False, lc=None): return dict(t='arrow', p1=(x1, y1), p2=(x2, y2), color=color, label=label, lx=lx, ly=ly, curve=curve, head=head, size=size, both=both, lc=lc or color)
def Ln(pts, color='black', w=4): return dict(t='line', pts=pts, color=color, w=w)
def Tab(x, y, cw, rh, rows, color='black', size=30, hdr=True, order='row', colors=None, fills=None): return dict(t='table', x=x, y=y, cw=cw, rh=rh, rows=rows, color=color, size=size, hdr=hdr, order=order, colors={f'{r},{c}': v for (r, c), v in (colors or {}).items()}, fills={f'{r},{c}': v for (r, c), v in (fills or {}).items()})
def Stamp(x, y, text='IMP!', color='red', rot=-8, size=34): return dict(t='stamp', x=x, y=y, text=text, color=color, rot=rot, size=size)
def Dia(cx, cy, w, h, label, color='black', size=28, double=False):
    pts = [(cx, cy - h // 2), (cx + w // 2, cy), (cx, cy + h // 2), (cx - w // 2, cy), (cx, cy - h // 2)]
    out = [Ln(pts, color, 4)]
    if double: out.append(Ln([(cx, cy - h // 2 + 10), (cx + w // 2 - 16, cy), (cx, cy + h // 2 - 10), (cx - w // 2 + 16, cy), (cx, cy - h // 2 + 10)], color, 3))
    out.append(T(0, label, x=cx - len(label) * size * .24, y=cy + size * .35, size=size, color=color)); return out
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
        out.append(Arr(round(x1), round(y1), round(x2), round(y2), head=head, color=ecol))
        if b not in done: out.append(ell(b)); done.add(b)
    return out
def fmtn(v): return f'{v:,.2f}'.rstrip('0').rstrip('.') if isinstance(v, float) else str(v)

CHAPTERS = [
 (1, 'Introduction to DBMS', ['DBMS vs file system', 'Three-schema architecture', 'Data independence', 'Languages & data models'], 4),
 (2, 'ER Model', ['Entities & attributes', 'Relationships & cardinality', 'Weak entity, ISA, aggregation', 'ER to tables'], 5),
 (3, 'Relational Model & Keys', ['Relation, tuple, domain', 'Super, candidate, primary, foreign keys', 'Counting super keys', 'Integrity constraints'], 5),
 (4, 'Relational Algebra & Calculus', ['Select, project, set operators', 'Joins', 'Division', 'Tuple & domain calculus'], 5),
 (5, 'SQL', ['DDL, DML, DCL, TCL', 'GROUP BY & HAVING', 'Joins & nested queries', 'Views & triggers'], 5),
 (6, 'Functional Dependencies', ["Armstrong's axioms", 'Attribute closure', 'Candidate keys', 'Canonical cover'], 5),
 (7, 'Normalization', ['Anomalies', '1NF, 2NF, 3NF, BCNF', 'Finding the normal form', 'Lossless & dependency preserving'], 5),
 (8, 'Transactions & Serializability', ['ACID & states', 'Schedules & conflicts', 'Conflict serializability', 'View serializability, recoverability'], 5),
 (9, 'Concurrency Control & Recovery', ['Locks & 2PL', 'Deadlocks', 'Timestamp ordering', 'Log-based recovery'], 5),
 (10, 'Indexing, B+ Trees & Hashing', ['Index types', 'Block-access numerical', 'B+ tree order & insertion', 'Hashing, query processing'], 5),
 (11, 'Exam Revision', ['Most asked questions', 'Last-minute tips'], 5),
]
def chapter(i):
    n, t, subs, stars = CHAPTERS[i - 1]
    return page(t, n, kind='chapter', num=n, subs=subs, stars=stars)

# =====================================================================================
p = page('DBMS', 0, kind='cover')
beat(p, '''Database Management Systems. The complete D B M S subject in one video. Simple explanations, handwritten notes,
and every important exam problem solved step by step.''')
beat(p, '''This works for B Tech computer science in almost every university. A K T U, Anna University, V T U, J N T U,
Mumbai, Pune, and private universities too. And it covers the full database part of GATE. So grab a pen, and let's start.''')

p = page('Contents', 0)
items = ['Introduction to DBMS', '[h:ER Model]  (ER to tables)', '[h:Relational Model & Keys]  (super keys)', 'Relational Algebra & Calculus',
         '[h:SQL]  (GROUP BY, nested queries)', '[h:Functional Dependencies]  (closure, keys)', '[h:Normalization]  (1NF to BCNF)',
         '[h:Transactions]  (serializability)', 'Concurrency Control & Recovery', '[h:Indexing & B+ Trees]', 'Exam Revision - most asked questions']
beat(p, "Here's our plan. Eleven chapters, from the basics to the exam numericals.", T(0, 'What we will cover today', size=42, font='bold', color='black'))
beat(p, '''We start with what a D B M S is, then the E R model, keys, relational algebra, and S Q L.''',
     *[T(1 + k, f'{k + 1}.  {items[k]}', x=200) for k in range(5)])
beat(p, '''Then the big scoring topics: functional dependencies, normalization, transactions, concurrency control, and indexing with B plus trees.
And at the end, a quick revision of the most asked questions. The highlighted ones are the most important.''',
     *[T(6 + k, f'{k + 6}.  {items[k + 5]}', x=200) for k in range(6)], Stamp(1520, 520, 'MOST ASKED', rot=-10))

# ===================================================================================== CH 1
p = chapter(1)
beat(p, "Chapter one. Introduction to D B M S. Let's build the basics first.")

p = page('What is a DBMS?', 1)
beat(p, '''Data means raw facts, like a name or a marks value. A database is an organised collection of related data.
And a D B M S, a database management system, is the software that stores, retrieves, and manages that data safely.
Examples are MySQL, Oracle, PostgreSQL, and SQL Server.''',
     T(0, '[h:Database] = organised collection of related data'), T(1, '[h:DBMS] = software to store, retrieve & manage data safely'),
     T(2, 'e.g. MySQL, Oracle, PostgreSQL, SQL Server', color='green'))
beat(p, '''Before D B M S, data was kept in plain files. That caused many problems. The same data was stored again and again,
called redundancy, so copies became inconsistent. Data was hard to search, there was weak security, and many users could not work at the same time safely.
A D B M S solves all of these.''',
     Tab(180, 380, [330, 520, 520], 54, [['', 'File system', 'DBMS'], ['redundancy', '[r:high], data repeated', '[g:controlled]'],
         ['consistency', '[r:copies disagree]', '[g:constraints keep it correct]'], ['access', 'write a program each time', 'easy queries (SQL)'],
         ['security', 'weak', 'user-level permissions'], ['concurrency', 'unsafe', 'many users safely'], ['recovery', 'manual backup', 'automatic (logs)']], size=28),
     Stamp(1640, 470))

p = page('Three-Schema Architecture', 1)
beat(p, '''The three schema architecture separates how users see data from how it is stored. It has three levels.
The external level, also called the view level, shows each user only the part of the data they need.''',
     Stamp(1650, 140, 'MUST DRAW'), S(0, '3 levels:', size=38), N(1, 1, '[r:External / view level] - what each user sees', size=34),
     *[Box(960 + 300 * k, 230, 250, 72, f'View {k + 1}', color='green', size=30) for k in range(3)])
beat(p, '''The conceptual level, or logical level, describes the whole database: all tables, attributes and relationships.
The internal level, or physical level, describes how data is actually stored on disk, with files, indexes and blocks.''',
     N(2, 2, '[r:Conceptual / logical level] - all tables & links', size=34), N(3, 3, '[r:Internal / physical level] - storage, files, indexes', size=34),
     Box(1010, 420, 750, 80, 'Conceptual schema', color='blue', size=32), Box(1010, 590, 750, 80, 'Internal schema', color='red', size=32),
     Ell(1235, 760, 300, 110, 'Stored database', size=28),
     *[Arr(1085 + 300 * k, 302, 1180 + 150 * k, 420) for k in range(3)], Arr(1385, 500, 1385, 590), Arr(1385, 670, 1385, 760))
beat(p, '''Between the levels there are mappings. Because of these mappings we get data independence. Physical data independence means
we can change the storage, like adding an index, without changing the logical schema. Logical data independence means we can change the logical schema,
like adding a column, without changing user views. Logical independence is harder to achieve.''',
     S(5, 'Data independence', size=38), T(6, '[k:Physical]: change storage, logical schema unchanged', size=34),
     T(7, '[k:Logical]: change logical schema, views unchanged', size=34), T(8, 'Logical independence is [r:harder]', size=34, color='green'))
beat(p, '''One more pair of terms. A schema is the design, or structure, of the database, which rarely changes.
An instance is the actual data stored at a particular moment, which changes all the time.''',
     T(10, '[h:Schema] = design (rarely changes)', size=34), T(11, '[h:Instance] = data at a moment (changes often)', size=34))

p = page('Database Languages, Users & Data Models', 1)
beat(p, '''D B M S languages. D D L, data definition language, defines structure: CREATE, ALTER, DROP, TRUNCATE. D M L, data manipulation language,
works on data: SELECT, INSERT, UPDATE, DELETE. D C L controls access: GRANT and REVOKE. And T C L controls transactions: COMMIT, ROLLBACK, SAVEPOINT.''',
     Tab(180, 240, [200, 520, 560], 56, [['Type', 'Meaning', 'Commands'], ['DDL', 'define structure', 'CREATE, ALTER, DROP, TRUNCATE'],
         ['DML', 'work on data', 'SELECT, INSERT, UPDATE, DELETE'], ['DCL', 'control access', 'GRANT, REVOKE'], ['TCL', 'control transactions', 'COMMIT, ROLLBACK, SAVEPOINT']],
         size=30, colors={(r, 0): 'red' for r in range(1, 5)}), Stamp(1640, 300))
beat(p, '''The D B A, database administrator, is in charge of the database. The D B A defines the schema, gives permissions, takes backups,
and tunes performance. Other users are application programmers, and end users.''',
     T(8, '[h:DBA]: schema, permissions, backup & recovery, performance tuning', size=34), T(9, 'Users: DBA, application programmers, end users', size=34))
beat(p, '''A data model is a way to describe data. Older models are hierarchical, which is a tree, and network, which is a graph.
The relational model uses tables and is the most popular. The E R model is used for design. And object oriented and No S Q L models are used for special needs.''',
     T(11, 'Data models: hierarchical (tree), network (graph), [h:relational (tables)],', size=34), T(12, 'ER (design), object-oriented, NoSQL', size=34, x=330))

# ===================================================================================== CH 2
p = chapter(2)
beat(p, 'Chapter two. The E R model. This is how we design a database before building it.')

p = page('ER Model: Entities & Attributes', 2)
beat(p, '''The entity relationship model, or E R model, describes data as entities, attributes and relationships.
An entity is a real world object, like a student. An entity set is a collection of similar entities, like all students. An entity is drawn as a rectangle.''',
     T(0, '[h:Entity] = real-world object (a student)'), T(1, '[h:Entity set] = all similar entities (all students)'),
     Box(1240, 420, 260, 90, 'STUDENT', size=34))
beat(p, '''Attributes are properties of an entity, drawn as ovals. The key attribute uniquely identifies an entity and is underlined, like roll number.
A composite attribute can be divided, like name into first and last name. A multi valued attribute can have many values, like phone numbers,
drawn as a double oval. And a derived attribute is calculated from another, like age from date of birth, drawn as a dashed oval.''',
     T(3, '[r:Key] (underlined): roll_no'), T(4, '[r:Composite]: name = first + last'), T(5, '[r:Multi-valued] (double oval): phone'),
     T(6, '[r:Derived] (dashed oval): age, from DOB'), T(7, '[r:Simple / single-valued]: gender'),
     Ell(1000, 250, 200, 80, 'roll_no', size=30), Ln([(1040, 312), (1160, 312)], 'black', 3), Arr(1150, 328, 1270, 420, head=False),
     Ell(1300, 230, 170, 80, 'name', size=30), Arr(1385, 310, 1370, 420, head=False),
     Ell(1230, 120 + 0, 150, 64, 'first', size=26), Ell(1420, 120, 150, 64, 'last', size=26), Arr(1310, 184, 1360, 230, head=False), Arr(1480, 184, 1410, 230, head=False),
     Ell(1580, 300, 200, 80, 'phone', size=30), Ell(1590, 308, 180, 64), Arr(1600, 378, 1490, 430, head=False),
     Ell(1580, 560, 160, 80, 'age', size=30, color='green'), Arr(1600, 580, 1500, 490, head=False, color='green'),
     Ell(1000, 560, 200, 80, 'gender', size=30), Arr(1180, 570, 1240, 500, head=False))

p = page('Relationships, Cardinality & Participation', 2)
beat(p, '''A relationship connects entities and is drawn as a diamond. For example, a student enrolls in a course.
The degree of a relationship is the number of entity sets in it: unary, binary or ternary.''',
     Box(240, 260, 260, 90, 'STUDENT', size=32), *Dia(800, 305, 260, 120, 'Enrolls'), Box(1100, 260, 260, 90, 'COURSE', size=32),
     Arr(500, 305, 670, 305, head=False), Arr(930, 305, 1100, 305, head=False),
     T(0, 'M', x=560, y=290, size=32, color='red'), T(0, 'N', x=1020, y=290, size=32, color='red'),
     T(0, 'Degree: unary, [h:binary], ternary', x=1450, y=L(1), size=32))
beat(p, '''Cardinality tells how many entities can be linked. One to one, like a person and a passport. One to many, like a department and its employees.
Many to one is the reverse. And many to many, like students and courses, where a student takes many courses and a course has many students.''',
     S(4, 'Cardinality ratio', size=38), T(5, '[k:1 : 1] person - passport', size=34), T(6, '[k:1 : N] department - employees', size=34),
     T(7, '[k:N : 1] employees - department', size=34), T(8, '[k:M : N] students - courses', size=34), Stamp(900, 520))
beat(p, '''Participation tells whether every entity must take part. Total participation means every entity must be in the relationship,
like every loan must belong to a branch. It is drawn with a double line. Partial participation means some may not take part, drawn with a single line.''',
     S(10, 'Participation', size=38), T(11, '[r:Total] (double line): every loan has a branch', size=34), T(12, '[r:Partial] (single line): not every customer has a loan', size=34),
     Box(1150, 640, 220, 80, 'LOAN', size=30), *Dia(1560, 680, 220, 110, 'Of'), Ln([(1370, 674), (1450, 674)], 'black', 3), Ln([(1370, 688), (1450, 688)], 'black', 3),
     Box(1150, 820, 220, 80, 'BRANCH', size=30), Arr(1560, 735, 1300, 820, head=False))

p = page('Weak Entity, Generalization & Aggregation', 2)
beat(p, '''A weak entity cannot be identified by its own attributes. It depends on a strong entity, called its owner.
For example, a payment depends on a loan. A weak entity is drawn as a double rectangle, its identifying relationship as a double diamond,
and its partial key, also called the discriminator, is underlined with a dashed line.''',
     T(0, '[h:Weak entity]: no key of its own, depends on owner'), T(1, 'double rectangle + double diamond + partial key (dashed)'),
     Box(240, 360, 240, 90, 'LOAN', size=32), *Dia(760, 405, 260, 130, 'Pays', double=True), Box(1040, 360, 260, 90, 'PAYMENT', size=32), Box(1050, 370, 240, 70),
     Arr(480, 405, 630, 405, head=False), Ln([(890, 398), (1040, 398)], 'black', 3), Ln([(890, 412), (1040, 412)], 'black', 3),
     Ell(1400, 330, 230, 76, 'payment_no', size=28), Arr(1400, 380, 1300, 400, head=False),
     Ln([(1440, 393), (1460, 393)], 'black', 3), Ln([(1475, 393), (1495, 393)], 'black', 3), Ln([(1510, 393), (1530, 393)], 'black', 3), Ln([(1545, 393), (1565, 393)], 'black', 3))
beat(p, '''Generalization is a bottom up process. We combine common features of lower entities into a higher entity, like car and bike into vehicle.
Specialization is the top down opposite: we split an entity into sub groups, like employee into engineer and manager. Both use an I S A triangle.''',
     T(9, '[r:Generalization] (bottom-up): car + bike -> vehicle', size=34), T(10, '[r:Specialization] (top-down): employee -> engineer, manager', size=34),
     Box(1250, 560, 240, 76, 'EMPLOYEE', size=28), Ln([(1370, 650), (1310, 730), (1430, 730), (1370, 650)], 'black', 4), T(0, 'ISA', x=1344, y=718, size=24),
     Arr(1370, 636, 1370, 650, head=False), Box(1130, 800, 220, 70, 'ENGINEER', size=26), Box(1400, 800, 220, 70, 'MANAGER', size=26),
     Arr(1330, 730, 1240, 800, head=False), Arr(1410, 730, 1510, 800, head=False))
beat(p, '''Aggregation treats a relationship as an entity, so that it can take part in another relationship. For example, the relationship
"employee works on project" can be monitored by a manager.''',
     T(12, '[r:Aggregation]: a relationship treated as an entity', size=34), T(13, 'e.g. (employee works-on project) monitored-by manager', size=34, color='green'))

p = page('ER Diagram to Tables', 2)
beat(p, '''Converting an E R diagram to tables is a common exam question. Rule one: each strong entity becomes a table, and its key becomes the primary key.
Rule two: a weak entity becomes a table that includes the owner's primary key. Rule three: a multi valued attribute becomes a separate table.''',
     Stamp(1650, 140, 'MOST ASKED'), N(0, 1, 'Strong entity -> table, key -> primary key', size=34), N(1, 2, "Weak entity -> table + owner's key", size=34),
     N(2, 3, 'Multi-valued attribute -> separate table', size=34))
beat(p, '''Rule four is about relationships. For one to one, put the key of one side into the other table. For one to many, put the key of the one side
as a foreign key in the many side. For many to many, make a new table with both keys, plus the relationship's own attributes.''',
     N(3, 4, '1 : 1 -> key of either side into the other', size=34), N(4, 5, '1 : N -> key of the "1" side into the "N" side', size=34),
     N(5, 6, '[h:M : N -> new table with both keys]', size=34))
beat(p, '''Example. Student and course with a many to many relationship enrolls, which has a grade attribute. We get three tables.
Student with student id and name. Course with course id and title. And enrolls with student id, course id and grade, where the two ids together form the primary key.''',
     Tab(180, 560, [180, 220], 54, [['sid', 'name']], size=30), T(0, 'STUDENT', x=180, y=545, size=30, color='red'),
     Tab(640, 560, [180, 220], 54, [['cid', 'title']], size=30), T(0, 'COURSE', x=640, y=545, size=30, color='red'),
     Tab(1100, 560, [160, 160, 180], 54, [['sid', 'cid', 'grade']], size=30), T(0, 'ENROLLS', x=1100, y=545, size=30, color='red'),
     T(0, 'primary key = (sid, cid)', x=1100, y=665, size=30, color='green'))
beat(p, '''GATE often asks for the minimum number of tables. For two entities with a many to many relationship, you need three tables.
For one to many, two tables are enough. And for one to one with total participation on both sides, a single table is enough.''',
     T(13, 'Minimum tables: [h:M:N -> 3]   1:N -> 2   1:1 (total both sides) -> 1', size=34, color='red'), Stamp(1600, 900, 'GATE'))

# ===================================================================================== CH 3
p = chapter(3)
beat(p, 'Chapter three. The relational model and keys.')

p = page('Relational Model Terms', 3)
beat(p, '''In the relational model, data is stored in tables called relations. Each row is a tuple, and each column is an attribute.
The domain of an attribute is the set of allowed values, like the age must be a positive number.''',
     Tab(180, 250, [180, 220, 180, 200], 56, [['roll', 'name', 'dept', 'age'], ['101', 'Asha', 'CSE', '20'], ['102', 'Ravi', 'ECE', '21'], ['103', 'Meena', 'CSE', '20']], size=30),
     Arr(1040, 360, 970, 360, color='red'), T(0, 'tuple (row)', x=1050, y=370, size=32, color='red'),
     T(0, 'attribute (column)', x=420, y=520, size=32, color='red'), Arr(470, 495, 470, 470, color='red'))
beat(p, '''The degree of a relation is the number of attributes, so here it is four. The cardinality is the number of tuples, here three.
Remember: degree is columns, cardinality is rows.''',
     T(7, '[h:Degree] = number of attributes (columns) = 4'), T(8, '[h:Cardinality] = number of tuples (rows) = 3'), Stamp(1500, 640))
beat(p, '''A relation schema is written like student, roll, name, dept, age. In a relation, the order of rows and columns does not matter,
there are no duplicate rows, and each value is atomic.''',
     T(10, 'Schema: STUDENT(roll, name, dept, age)', color='black'), T(11, 'no duplicate rows · order does not matter · atomic values', color='green', size=34))

p = page('Keys in DBMS', 3)
beat(p, '''Keys are used to identify rows uniquely. A super key is any set of attributes that can uniquely identify a row, like roll number,
or roll number with name. A candidate key is a minimal super key, which means no attribute can be removed from it.''',
     Stamp(1650, 140, 'MOST ASKED'), T(0, '[r:Super key]: any set that identifies a row uniquely'), T(1, '[r:Candidate key]: a [h:minimal] super key'),
     Tab(1100, 420, [140, 200, 220, 190], 54, [['roll', 'email', 'name', 'phone'], ['101', 'a@pu.in', 'Asha', '98400'], ['102', 'r@pu.in', 'Ravi', '98411']], size=28))
beat(p, '''The primary key is the candidate key chosen by the designer. It cannot be null and must be unique. The other candidate keys are alternate keys.
A composite key has more than one attribute. And a foreign key is an attribute in one table that refers to the primary key of another table.''',
     T(2, '[r:Primary key]: chosen candidate key (unique, not NULL)'), T(3, '[r:Alternate key]: other candidate keys'),
     T(4, '[r:Composite key]: more than one attribute'), T(5, '[r:Foreign key]: refers to primary key of another table'))
beat(p, '''In our table, roll number, email and phone are candidate keys. If we choose roll number as primary key, email and phone become alternate keys.
And every candidate key is a super key, but not every super key is a candidate key.''',
     T(8, 'Candidate keys: roll, email, phone', size=34, color='black'), T(9, 'Primary: roll  ->  alternate: email, phone', size=34, color='black'),
     T(11, 'primary key  ⊆  candidate keys  ⊆  super keys', color='green'),
     Ell(1150, 700, 640, 260, None, color='blue'), Ell(1250, 750, 440, 170, None, color='green'), Ell(1340, 790, 260, 90, 'primary', size=28, color='red'),
     T(0, 'super', x=1440, y=948, size=26, color='blue'), T(0, 'candidate', x=1420, y=908, size=24, color='green'))

kA = len(superkeys('ABCD', fd('A->BCD'))); kAB = len(superkeys('ABCD', fd('A->BCD, BC->AD')))
p = page('Number of Super Keys', 3)
beat(p, '''A favourite GATE question is counting super keys. Take a relation R with four attributes A, B, C, D. If the only candidate key is A,
then any set containing A is a super key. The other three attributes can be in or out, so there are 2 to the power 3, which is 8 super keys.''',
     Stamp(1600, 140, 'GATE'), T(0, 'R(A, B, C, D),  only candidate key = A'), T(1, 'A must be in;  B, C, D each in or out', color='black'),
     T(2, f'Super keys = 2^3 = [h:{kA}]', color='red', size=42))
beat(p, '''If there are two candidate keys, A and B C, we use inclusion and exclusion. Sets containing A: 2 to the power 3, which is 8.
Sets containing B and C: 2 to the power 2, which is 4. Sets containing both A and B C: 2 to the power 1, which is 2. So the total is 8 plus 4 minus 2, which is 10.''',
     T(4, 'Candidate keys = A and BC'), T(5, 'containing A: 2^3 = 8'), T(6, 'containing BC: 2^2 = 4'), T(7, 'containing A and BC (ABC): 2^1 = 2'),
     T(8, f'Super keys = 8 + 4 - 2 = [h:{kAB}]', color='red', size=42))
beat(p, '''The general formula: with n attributes and a candidate key of k attributes, the number of super keys is 2 to the power n minus k.''',
     T(10, 'Formula: one key of k attributes, n attributes -> 2^(n - k)', color='green'),
     T(11, 'Two keys K1, K2: 2^(n-|K1|) + 2^(n-|K2|) - 2^(n-|K1 ∪ K2|)', color='green', size=34))

p = page('Integrity Constraints', 3)
beat(p, '''Integrity constraints are rules that keep data correct. A domain constraint says each value must come from the attribute's domain,
like age must be a number. A key constraint says key values must be unique.''',
     N(0, 1, '[r:Domain constraint]: value must be from the domain'), N(1, 2, '[r:Key constraint]: key values are unique'))
beat(p, '''Entity integrity says the primary key can never be null. Referential integrity says a foreign key value must either match a primary key
value in the referenced table, or be null.''',
     N(2, 3, '[r:Entity integrity]: primary key is never NULL'), N(3, 4, '[r:Referential integrity]: foreign key matches a primary key, or NULL'),
     Stamp(1600, 320),
     Tab(180, 500, [140, 190, 160], 54, [['eid', 'name', 'dept'], ['1', 'Asha', 'CSE'], ['3', 'Meena', 'ECE']], size=28), T(0, 'EMP', x=180, y=485, size=30, color='red'),
     Tab(1000, 500, [170, 200], 54, [['dname', 'block'], ['CSE', 'Block A'], ['ECE', 'Block B']], size=28), T(0, 'DEPT', x=1000, y=485, size=30, color='red'),
     Arr(650, 580, 1000, 580, color='green', label='foreign key -> primary key', ly=-16, size=26))
beat(p, '''What happens when we delete a department that employees refer to? We can reject the delete, use ON DELETE CASCADE to also delete those employees,
or use ON DELETE SET NULL to set their department to null.''',
     T(12, 'Delete DEPT row: reject  |  ON DELETE CASCADE  |  ON DELETE SET NULL', size=34, color='black'))

# ===================================================================================== CH 4
p = chapter(4)
beat(p, 'Chapter four. Relational algebra and relational calculus. These are the theory behind every query.')

p = page('Relational Algebra Operators', 4)
beat(p, '''Relational algebra is a procedural query language. It takes relations as input and gives a relation as output.
Select, written with sigma, picks rows that satisfy a condition. Project, written with pi, picks columns, and removes duplicate rows.''',
     T(0, 'Procedural: relation(s) in -> relation out', color='black'),
     T(1, '[r:σ Select]: picks rows      σ salary > 50000 (Emp)'), T(2, '[r:π Project]: picks columns      π name, dept (Emp)'))
beat(p, '''Union, intersection and set difference work like sets, but the two relations must be union compatible: same number of attributes, with matching domains.
Cartesian product, written with a cross, pairs every row of one table with every row of the other. Rename, written with rho, gives a new name.''',
     T(3, '[r:∪ Union], [r:∩ Intersection], [r:- Difference]: need union compatibility'), T(4, '[r:× Cartesian product]: every row with every row'),
     T(5, '[r:ρ Rename]: ρ E(Emp)'))
beat(p, '''The basic operators are select, project, union, difference, cartesian product and rename. Join, intersection and division can be built from them.''',
     T(7, 'Basic: σ, π, ∪, -, ×, ρ        Derived: ∩, ⋈ (join), ÷ (division)', color='green'), Stamp(1600, 600))

emp_rows = [['eid', 'name', 'dept', 'salary']] + [[str(a), b, c, str(d)] for a, b, c, d in EMP]
r1 = q("select name, salary from Emp where dept='CSE' and salary > 50000 order by eid")
r2 = q('select name from Emp where salary < 45000 order by eid')
p = page('Relational Algebra Examples', 4)
beat(p, '''Let's use this employee table with six rows. It has employee id, name, department and salary.''',
     Tab(180, 220, [110, 170, 150, 170], 50, emp_rows, size=28), T(0, 'EMP', x=180, y=205, size=30, color='red'))
beat(p, '''Query one. Find employees of C S E with salary more than fifty thousand. In relational algebra: project name and salary, of select dept equals C S E
and salary greater than fifty thousand, on Emp. The answer is Asha with sixty thousand, and Divya with seventy thousand.''',
     T(0, 'π name, salary (σ dept=\'CSE\' ∧ salary>50000 (Emp))', x=860, y=L(0), size=32, color='black'),
     Tab(900, 260, [200, 200], 50, [['name', 'salary']] + [[a, str(b)] for a, b in r1], size=28, colors={(1, 0): 'green', (2, 0): 'green'}))
beat(p, '''Query two. Find names of employees earning less than forty five thousand. Project name, of select salary less than forty five thousand.
The answer is Kiran and Arun.''',
     T(0, 'π name (σ salary < 45000 (Emp))', x=860, y=L(7), size=32, color='black'),
     Tab(900, 640, [200], 50, [['name']] + [[a] for (a,) in r2], size=28, colors={(1, 0): 'green', (2, 0): 'green'}))

rj = q('select e.name, e.dept, d.block from Emp e join Dept d on e.dept = d.dname order by e.eid')
p = page('Joins', 4)
beat(p, '''A join combines related rows from two tables. A theta join uses any condition. An equi join uses only equality.
A natural join is an equi join on attributes with the same name, and it shows the common column only once.''',
     T(0, '[r:Theta join]: any condition (<, >, =, ...)'), T(1, '[r:Equi join]: only ='), T(2, '[r:Natural join ⋈]: equal on common names, column shown once'))
beat(p, '''Outer joins also keep the rows that have no match. A left outer join keeps every row of the left table, and puts null on the right side.
A right outer join keeps every row of the right table. And a full outer join keeps every row from both tables.''',
     T(4, '[r:Left outer join]: all rows of left, NULL if no match'), T(5, '[r:Right outer join]: all rows of right'), T(6, '[r:Full outer join]: all rows of both'),
     Stamp(1600, 300))
beat(p, '''Example. Join Emp and Dept on department name. Every employee gets the block of their department. With a left outer join from Dept to Emp,
the civil department also appears, with null for the employee, because nobody works there.''',
     Tab(180, 640, [170, 150, 190], 46, [['name', 'dept', 'block']] + [[a, b, c] for a, b, c in rj], size=26),
     T(0, 'Emp ⋈ Dept', x=180, y=625, size=30, color='red'),
     Tab(900, 640, [170, 190], 46, [['dname', 'name']] + [[a, b or 'NULL'] for a, b in q('select d.dname, e.name from Dept d left join Emp e on e.dept = d.dname order by d.dname, e.eid')], size=26,
         colors={(4, 1): 'red', (4, 0): 'red'}),
     T(0, 'Dept LEFT OUTER JOIN Emp', x=900, y=625, size=30, color='red'))

dv = division()
p = page('Division Operator', 4)
beat(p, '''Division is used for "for all" questions, like: find students who have enrolled in all courses. Enroll divided by Course gives the students
who are paired with every course in the course table.''',
     T(0, '[h:Division ÷]: for "ALL" queries'), T(1, 'Find students enrolled in [r:all] courses  ->  Enroll ÷ Course', color='black'), Stamp(1600, 140, 'GATE'),
     Tab(180, 360, [150, 150], 48, [['sid', 'cid']] + [list(r) for r in ENROLL], size=28), T(0, 'ENROLL', x=180, y=345, size=30, color='red'),
     Tab(620, 360, [150], 48, [['cid']] + [list(r) for r in COURSE], size=28), T(0, 'COURSE', x=620, y=345, size=30, color='red'))
beat(p, '''Check each student. S1 has D B M S, O S and C N, which is all three, so S1 qualifies. S2 has only D B M S and O S, so no.
S3 has all three, so yes. S4 has only C N, so no. The answer is S1 and S3.''',
     T(0, 'S1: DBMS, OS, CN  ✓', x=900, y=L(4), size=34, color='green'), T(0, 'S2: DBMS, OS  ✗', x=900, y=L(5), size=34, color='red'),
     T(0, 'S3: DBMS, OS, CN  ✓', x=900, y=L(6), size=34, color='green'), T(0, 'S4: CN  ✗', x=900, y=L(7), size=34, color='red'),
     Tab(900, 680, [150], 48, [['sid']] + [[s] for s in dv], size=28, colors={(1, 0): 'green', (2, 0): 'green'}), T(0, 'Result', x=900, y=665, size=30, color='red'))
beat(p, '''Division can be written with basic operators too: the student ids in Enroll, minus the student ids that have some course missing.''',
     T(14, 'R ÷ S = π sid (R) - π sid ((π sid (R) × S) - R)', size=34, color='green'))

p = page('Relational Calculus', 4)
beat(p, '''Relational calculus is non procedural. It says what we want, not how to get it. In tuple relational calculus, we write the set of tuples t,
such that a condition holds. For example: all t such that t is in Emp, and t dot salary is greater than fifty thousand.''',
     T(0, '[h:Non-procedural]: says WHAT, not HOW'), S(1, 'Tuple relational calculus (TRC)', size=36, color='red'),
     T(2, '{ t | t ∈ Emp ∧ t.salary > 50000 }', color='black', size=40))
beat(p, '''In domain relational calculus, variables stand for single values of attributes, not whole tuples. For example: the names n, such that there exist
e, d and s, with e, n, d, s in Emp, and s greater than fifty thousand.''',
     S(4, 'Domain relational calculus (DRC)', size=36, color='red'), T(5, '{ <n> | ∃ e, d, s ( <e, n, d, s> ∈ Emp ∧ s > 50000 ) }', color='black', size=38))
beat(p, '''Expressions must be safe, which means they give a finite answer. Safe relational calculus and relational algebra have the same power.
A language with this power is called relationally complete, and S Q L is relationally complete.''',
     T(7, '[k:Safe] expression = finite answer'), T(8, 'Algebra = safe TRC = safe DRC  (same power)', color='green'), T(9, '"Relationally complete": SQL', color='green'))

# ===================================================================================== CH 5
p = chapter(5)
beat(p, 'Chapter five. S Q L, the language every database uses.')

p = page('SQL: Creating & Changing Tables', 5)
beat(p, '''S Q L means structured query language. We create a table with CREATE TABLE. Here, the employee id is the primary key, name cannot be null,
department refers to the Dept table, and salary must be positive.''',
     T(0, 'CREATE TABLE Emp (', color='black', size=36), T(1, 'eid INT PRIMARY KEY,', x=240, size=36), T(2, 'name VARCHAR(30) NOT NULL,', x=240, size=36),
     T(3, 'dept VARCHAR(10) REFERENCES Dept(dname),', x=240, size=36), T(4, 'salary INT CHECK (salary > 0) );', x=240, size=36))
beat(p, '''We add rows with INSERT, change them with UPDATE, and remove them with DELETE.''',
     T(6, "INSERT INTO Emp VALUES (7, 'Neha', 'CSE', 55000);", size=34, color='black'),
     T(7, "UPDATE Emp SET salary = salary * 1.1 WHERE dept = 'ECE';", size=34, color='black'), T(8, 'DELETE FROM Emp WHERE eid = 7;', size=34, color='black'))
beat(p, '''Exam favourite: DELETE versus TRUNCATE versus DROP. DELETE removes chosen rows, and can be rolled back. TRUNCATE removes all rows quickly,
and keeps the structure. DROP removes the whole table, data and structure.''',
     Tab(180, 690, [260, 520, 420], 52, [['', 'What it removes', 'Type'], ['DELETE', 'chosen rows (WHERE)', 'DML, can rollback'],
         ['TRUNCATE', 'all rows, keeps structure', 'DDL, fast'], ['DROP', 'whole table + structure', 'DDL']], size=28, colors={(r, 0): 'red' for r in range(1, 4)}),
     Stamp(1600, 720, 'MOST ASKED'))

gb = q('select dept, count(*), avg(salary) from Emp group by dept having count(*) >= 2 order by dept')
p = page('SELECT, GROUP BY & HAVING', 5)
beat(p, '''The SELECT statement. SELECT columns FROM tables WHERE condition GROUP BY columns HAVING group condition ORDER BY columns.
Aggregate functions are COUNT, SUM, AVG, MIN and MAX.''',
     T(0, 'SELECT ... FROM ... WHERE ... GROUP BY ... HAVING ... ORDER BY ...', size=34, color='black'),
     T(1, 'Aggregates: COUNT, SUM, AVG, MIN, MAX', size=34))
beat(p, '''Question. For each department with at least two employees, show the count and the average salary.
SELECT department, COUNT star, average of salary, FROM Emp, GROUP BY department, HAVING COUNT star greater than or equal to two.''',
     Stamp(1650, 140, 'NUMERICAL'),
     T(3, 'SELECT dept, COUNT(*), AVG(salary)', size=34, color='red'), T(4, 'FROM Emp GROUP BY dept', x=240, size=34, color='red'), T(5, 'HAVING COUNT(*) >= 2;', x=240, size=34, color='red'))
beat(p, '''Group by makes three groups: C S E with three employees, E C E with two, and mechanical with one. HAVING removes mechanical, because it has only one.
So we get C S E, three, with average fifty eight thousand three hundred and thirty three, and E C E, two, with average forty five thousand.''',
     Tab(1060, 420, [170, 170, 260], 52, [['dept', 'COUNT(*)', 'AVG(salary)']] + [[a, str(b), fmtn(round(c, 2))] for a, b, c in gb], size=28,
         colors={(1, 2): 'green', (2, 2): 'green'}),
     T(0, 'MECH removed by HAVING (only 1)', x=1060, y=620, size=30, color='red'))
beat(p, '''Remember the order in which S Q L runs a query: FROM, then WHERE, then GROUP BY, then HAVING, then SELECT, and finally ORDER BY.
That is why WHERE filters rows before grouping, and HAVING filters groups after grouping.''',
     T(9, 'Order: FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY', size=34, color='green'),
     T(10, '[h:WHERE] filters rows (before groups)   [h:HAVING] filters groups', size=34))

sh = q('select max(salary) from Emp where salary < (select max(salary) from Emp)')[0][0]
p = page('Joins & Nested Queries in SQL', 5)
beat(p, '''A join in S Q L. Show names and blocks of employees earning above fifty thousand. SELECT name and block, FROM Emp JOIN Dept, ON department equals department name,
WHERE salary greater than fifty thousand. We get Asha in block A, Meena in block B and Divya in block A.''',
     T(0, 'SELECT e.name, d.block FROM Emp e JOIN Dept d', size=32, color='black'), T(1, 'ON e.dept = d.dname WHERE e.salary > 50000;', x=240, size=32, color='black'),
     Tab(1300, 250, [180, 200], 46, [['name', 'block']] + [list(r) for r in q('select e.name, d.block from Emp e join Dept d on e.dept = d.dname where e.salary > 50000 order by e.eid')], size=26))
beat(p, '''A nested query has a query inside another. The most asked one: find the second highest salary. SELECT MAX salary FROM Emp WHERE salary is less than
the maximum salary. The highest is seventy thousand, so the answer is sixty thousand.''',
     Stamp(1650, 470, 'MOST ASKED'), S(4, 'Second highest salary', size=38, color='red'),
     T(5, 'SELECT MAX(salary) FROM Emp', size=34, color='black'), T(6, 'WHERE salary < (SELECT MAX(salary) FROM Emp);', x=240, size=34, color='black'),
     T(7, f'Answer: [h:{sh}]', size=38, color='green'))
beat(p, '''Useful operators with sub queries: IN checks membership, EXISTS checks if the sub query returns any row, and ANY and ALL compare with some or every value.
A correlated sub query uses a column of the outer query, so it runs once for each outer row.''',
     T(9, '[r:IN], [r:NOT IN], [r:EXISTS], [r:ANY], [r:ALL]', size=34),
     T(10, '[k:Correlated] subquery: uses outer row, runs once per row', size=34),
     T(11, 'e.g. SELECT name FROM Emp e WHERE salary > (SELECT AVG(salary)', size=30, color='green'), T(12, 'FROM Emp WHERE dept = e.dept);', x=330, size=30, color='green'))

p = page('Views, Triggers & More', 5)
beat(p, '''A view is a virtual table, stored only as a query. It gives security, because users see only what they need, and makes complex queries simple.''',
     T(0, '[h:View] = virtual table (stored query)'), T(1, 'CREATE VIEW HighPaid AS SELECT name, salary FROM Emp WHERE salary > 50000;', size=30, color='black'))
beat(p, '''A trigger is code that runs automatically when an event happens, like an insert or update. It follows the event, condition, action rule.
For example, log every salary change into an audit table.''',
     T(3, '[h:Trigger] = runs automatically on INSERT / UPDATE / DELETE'), T(4, 'Event -> Condition -> Action  (e.g. log salary changes)', color='green'))
beat(p, '''A stored procedure is a saved program inside the database. A cursor lets us process query results one row at a time.
And DCL commands GRANT and REVOKE give and take back permissions.''',
     T(6, '[k:Stored procedure]: saved program in the DB'), T(7, '[k:Cursor]: process results row by row'),
     T(8, "GRANT SELECT ON Emp TO ravi;   REVOKE SELECT ON Emp FROM ravi;", size=32, color='black'))

# ===================================================================================== CH 6
p = chapter(6)
beat(p, 'Chapter six. Functional dependencies. This is the base of normalization, and GATE asks numericals from here every year.')

p = page('Functional Dependencies', 6)
beat(p, '''A functional dependency X arrow Y means: if two rows have the same X value, they must have the same Y value. We say X determines Y.
For example, roll number determines name.''',
     T(0, '[h:X -> Y]: same X value  =>  same Y value'), T(1, 'e.g. roll -> name     (roll determines name)', color='green'))
beat(p, '''A dependency is trivial if Y is a part of X, like A B determines A. Otherwise it is non trivial.''',
     T(2, '[k:Trivial]: Y ⊆ X  (AB -> A)      [k:Non-trivial]: otherwise'))
beat(p, '''Armstrong's axioms let us find all dependencies. Reflexivity: if Y is a part of X, then X determines Y. Augmentation: if X determines Y,
then X Z determines Y Z. Transitivity: if X determines Y and Y determines Z, then X determines Z.''',
     Stamp(1600, 360), S(4, "Armstrong's axioms", size=38, color='red'), N(5, 1, 'Reflexivity: Y ⊆ X  =>  X -> Y'), N(6, 2, 'Augmentation: X -> Y  =>  XZ -> YZ'),
     N(7, 3, 'Transitivity: X -> Y, Y -> Z  =>  X -> Z'))
beat(p, '''From these we get three more rules. Union: if X determines Y and X determines Z, then X determines Y Z. Decomposition is the reverse.
And pseudo transitivity: if X determines Y and W Y determines Z, then W X determines Z.''',
     S(9, 'Derived rules', size=38, color='red'), N(10, 4, 'Union: X -> Y, X -> Z  =>  X -> YZ'), N(11, 5, 'Decomposition: X -> YZ  =>  X -> Y, X -> Z'),
     N(12, 6, 'Pseudo-transitivity: X -> Y, WY -> Z  =>  WX -> Z'))

Fk = fd('A->B, A->C, CG->H, CG->I, B->H'); X, steps = closure('AG', Fk)
p = page('Attribute Closure', 6)
beat(p, '''The closure of a set of attributes X, written X plus, is the set of all attributes that X determines. Start with X itself,
and keep adding attributes using the dependencies, until nothing changes.''',
     T(0, '[h:X+] = all attributes X determines'), T(1, 'Start with X; keep applying FDs until nothing changes', color='green'))
beat(p, '''Classic example. R is A, B, C, G, H, I with dependencies: A determines B, A determines C, C G determines H, C G determines I, and B determines H.
Find the closure of A G.''',
     Stamp(1650, 140, 'NUMERICAL'), T(3, 'R(A, B, C, G, H, I)', color='black'), T(4, 'F = { A -> B, A -> C, CG -> H, CG -> I, B -> H }', color='black'))
beat(p, '''Start with A G. A determines B, so add B. A determines C, so add C. Now we have C and G, so C G determines H, add H.
And C G determines I, add I. So A G plus is A, B, C, G, H, I, which is all the attributes. So A G is a super key.''',
     Tab(180, 480, [140, 200, 340], 52, [['step', 'use', 'AG+ so far'], ['start', '', 'AG']] + [[str(k + 1), f'{l} -> {r}', x] for k, (l, r, x) in enumerate(steps)], size=28,
         colors={(len(steps) + 1, 2): 'green'}),
     T(0, '(AG)+ = ABCGHI = all  =>  AG is a [h:super key]', x=960, y=L(6), size=34, color='red'))
beat(p, '''Is it a candidate key? Check the smaller sets. A plus is A, B, C, H, which misses G and I. G plus is just G. So no smaller set works,
and A G is a candidate key.''',
     T(0, 'A+ = ABCH,  G+ = G  (neither is all)', x=960, y=L(8), size=34), T(0, '=> AG is a [h:candidate key]', x=960, y=L(9), size=34, color='green'))

F2 = fd('A->B, BC->E, ED->A'); K2 = candidate_keys('ABCDE', F2)
p = page('Finding Candidate Keys', 6)
beat(p, '''Now let's find all candidate keys. R is A, B, C, D, E, with A determines B, B C determines E, and E D determines A.
Trick one: an attribute that never appears on the right side must be in every key. Here C and D never appear on the right.''',
     Stamp(1650, 140, 'GATE'), T(0, 'R(A, B, C, D, E)    F = { A -> B, BC -> E, ED -> A }', color='black'),
     T(1, 'Never on right side: [h:C, D]  =>  in every key'), T(2, '(CD)+ = CD   not all, so add one more attribute', color='red'))
beat(p, '''C D plus is just C D, so we try adding one more attribute. A C D plus: A gives B, B C gives E. So we get all five, and A C D is a key.
B C D plus: B C gives E, E D gives A. All five, so B C D is a key. C D E plus: E D gives A, A gives B. All five, so C D E is a key too.''',
     T(4, '(ACD)+ : A->B, BC->E  =>  ABCDE  ✓'), T(5, '(BCD)+ : BC->E, ED->A  =>  ABCDE  ✓'), T(6, '(CDE)+ : ED->A, A->B  =>  ABCDE  ✓'))
beat(p, f'''So we get three candidate keys: A C D, B C D, and C D E. A prime attribute is one that appears in some candidate key. In this example, all five attributes are prime.''',
     T(8, f"Candidate keys: [h:{', '.join(K2)}]", size=40, color='red'), T(9, 'Prime attributes: A, B, C, D, E (all)', color='green'))

cc = canonical_cover(fd('A->BC, B->C, A->B, AB->C'))
p = page('Canonical Cover', 6)
beat(p, '''A canonical cover, or minimal cover, is the smallest set of dependencies that means the same as the original set.
Steps: split the right sides into single attributes, remove extra attributes on the left side, and remove redundant dependencies.''',
     T(0, '[h:Canonical (minimal) cover]: smallest equivalent set of FDs'), N(1, 1, 'single attribute on the right'), N(2, 2, 'remove extraneous left attributes'),
     N(3, 3, 'remove redundant FDs'))
beat(p, '''Example. F is A determines B C, B determines C, A determines B, and A B determines C. Split: A determines B, A determines C, B determines C, A B determines C.
In A B determines C, B is extra, because A alone gives C. So it becomes A determines C, a duplicate.''',
     Stamp(1650, 140, 'NUMERICAL'), T(5, 'F = { A -> BC, B -> C, A -> B, AB -> C }', color='black'),
     T(6, 'Split: A -> B, A -> C, B -> C, AB -> C'), T(7, 'AB -> C: A+ already has C  =>  B is extraneous  =>  A -> C'))
beat(p, f'''Now A determines C is redundant, because A determines B and B determines C already give it. So the canonical cover is A determines B, and B determines C.''',
     T(8, 'A -> C is redundant (A -> B -> C)'), T(10, f'Canonical cover: [h:{{ {fd_str(cc)} }}]', size=42, color='red'))

# ===================================================================================== CH 7
p = chapter(7)
beat(p, 'Chapter seven. Normalization. One of the most asked chapters in every exam.')

p = page('Why Normalize? Anomalies', 7)
beat(p, '''Look at this table. The course name and instructor are repeated for every student in the course. This repetition causes three problems, called anomalies.''',
     Tab(180, 230, [120, 160, 140, 180, 220], 50, [['sid', 'sname', 'cid', 'cname', 'instructor'], ['S1', 'Asha', 'C1', 'DBMS', 'Dr. Rao'],
         ['S2', 'Ravi', 'C1', 'DBMS', 'Dr. Rao'], ['S3', 'Meena', 'C2', 'OS', 'Dr. Iyer']], size=28, fills={(1, 3): 'yellow', (2, 3): 'yellow', (1, 4): 'yellow', (2, 4): 'yellow'}))
beat(p, '''An insertion anomaly: we cannot add a new course until some student joins it. An update anomaly: if Dr Rao's course changes, we must update many rows,
or the data becomes inconsistent. A deletion anomaly: if the only student of O S leaves, we lose the course details too.''',
     N(6, 1, "[r:Insertion]: can't add a course without a student"), N(7, 2, '[r:Update]: change in many rows, else inconsistent'),
     N(8, 3, '[r:Deletion]: deleting last student loses course details'), Stamp(1600, 500))
beat(p, '''Normalization removes these anomalies by splitting a big table into smaller, well designed tables, using functional dependencies.''',
     T(10, '[h:Normalization] = split tables using FDs to remove anomalies', color='green'))

p = page('Normal Forms: 1NF to BCNF', 7)
beat(p, '''First normal form: every value must be atomic, so no lists or repeating groups in a cell.''',
     Stamp(1650, 140, 'MOST ASKED'), T(0, '[r:1NF]:  atomic values only (no lists in a cell)'))
beat(p, '''Second normal form: it is in first normal form, and there is no partial dependency. That means no non prime attribute depends on only a part of a candidate key.''',
     T(1, '[r:2NF]:  1NF + no partial dependency'), T(2, '(non-prime attribute depends on PART of a key)', x=320, size=32, color='green'))
beat(p, '''Third normal form: for every non trivial dependency X determines A, either X is a super key, or A is a prime attribute. This removes transitive dependencies.''',
     T(3, '[r:3NF]:  for X -> A: X is a super key [k:OR] A is prime'), T(4, '(removes transitive dependency)', x=320, size=32, color='green'))
beat(p, '''Boyce Codd normal form, B C N F, is stricter: for every non trivial dependency X determines A, X must be a super key. No exception for prime attributes.''',
     T(5, '[r:BCNF]:  for X -> A: X must be a super key'), T(6, '(stricter than 3NF)', x=320, size=32, color='green'))
beat(p, '''Fourth normal form removes multi valued dependencies, and fifth normal form removes join dependencies. Remember the order:
B C N F is inside third normal form, which is inside second, which is inside first.''',
     T(7, '[r:4NF]:  BCNF + no multi-valued dependency'), T(8, '[r:5NF]:  4NF + no join dependency'),
     Ell(1050, 600, 760, 360, None, color='blue'), Ell(1130, 650, 600, 270, None, color='green'), Ell(1210, 700, 440, 180, None, color='red'),
     Ell(1290, 745, 280, 90, 'BCNF', size=30, color='black'), T(0, '1NF', x=1075, y=790, size=28, color='blue'), T(0, '2NF', x=1150, y=800, size=28, color='green'),
     T(0, '3NF', x=1222, y=800, size=28, color='red'))

nf1 = normal_form('ABCD', fd('AB->C, A->D')); nf2 = normal_form('ABCD', fd('AB->C, C->D')); nf3 = normal_form('ABC', fd('AB->C, C->B'))
p = page('Finding the Normal Form', 7)
beat(p, '''Now let's find the highest normal form. First, always find the candidate keys. Example one: R is A B C D, where A B determines C, and A determines D.
The key is A B. Now, A determines D is a partial dependency, because D depends only on A, which is just a part of the key. So this relation is only in first normal form.''',
     Stamp(1650, 140, 'NUMERICAL'), S(0, 'Ex 1: R(ABCD), AB -> C, A -> D', size=36), T(1, 'Key = AB.  A -> D: D depends on part of key (partial)'),
     T(2, f'=> highest normal form: [h:{nf1}]', color='red'))
beat(p, '''Example two: A B determines C, and C determines D. The key is A B. No partial dependency, so it is in second normal form.
But C determines D, where C is not a super key and D is not prime. That is a transitive dependency, so it is not in third normal form.''',
     S(4, 'Ex 2: R(ABCD), AB -> C, C -> D', size=36), T(5, 'Key = AB.  C -> D: C not super key, D not prime (transitive)'),
     T(6, f'=> highest normal form: [h:{nf2}]', color='red'))
beat(p, '''Example three: R is A B C, with A B determines C, and C determines B. The candidate keys are A B and A C, so B is prime.
C determines B is allowed in third normal form because B is prime. But C is not a super key, so it is not in B C N F.''',
     S(8, 'Ex 3: R(ABC), AB -> C, C -> B', size=36), T(9, 'Keys = AB, AC  =>  B is prime'), T(10, 'C -> B: OK for 3NF (B prime), not BCNF (C not super key)'),
     T(11, f'=> highest normal form: [h:{nf3}]', color='red'))
beat(p, '''Quick tip: if all attributes are prime, the relation is at least in third normal form, like our earlier example with keys A C D, B C D and C D E.''',
     T(13, 'Tip: all attributes prime  =>  at least 3NF', color='green'))

p = page('Decomposition: Lossless & Dependency Preserving', 7)
beat(p, '''When we split R into R one and R two, the split must be lossless, which means joining them back gives exactly the original table, with no extra rows.
The test: the common attributes, R one intersect R two, must be a key of R one or of R two.''',
     T(0, '[h:Lossless join]: R1 ⋈ R2 = R (no extra rows)'), T(1, 'Test: (R1 ∩ R2) -> R1   or   (R1 ∩ R2) -> R2', color='red'), Stamp(1600, 200))
beat(p, '''Dependency preserving means every original dependency can still be checked inside one of the smaller tables, without a join.''',
     T(3, '[h:Dependency preserving]: every FD checkable within one table'))
beat(p, '''Example. R is A B C, with A B determines C, and C determines B. It is not in B C N F because of C determines B. Decompose into R one, C B, and R two, A C.
The common attribute is C, and C determines B, so C is a key of R one: lossless. But A B determines C cannot be checked in either table, so the dependency is lost.''',
     S(5, 'R(ABC): AB -> C, C -> B  (not BCNF)', size=36), T(6, 'R1(C, B), R2(A, C);  R1 ∩ R2 = C, C -> B  =>  [g:lossless ✓]'),
     T(7, 'AB -> C not inside R1 or R2  =>  [r:not dependency preserving ✗]'))
beat(p, '''Remember this result. Decomposition into third normal form is always lossless and dependency preserving. Decomposition into B C N F is always lossless,
but may not preserve dependencies.''',
     Tab(180, 680, [300, 330, 460], 56, [['', 'Lossless', 'Dependency preserving'], ['3NF', '[g:always]', '[g:always]'], ['BCNF', '[g:always]', '[r:not always]']], size=30))

# ===================================================================================== CH 8
p = chapter(8)
beat(p, 'Now, chapter eight. We move on to transactions and serializability.')

p = page('Transaction & ACID Properties', 8)
beat(p, '''A transaction is a set of operations that form one logical unit of work. For example, transferring five hundred rupees from account A to account B:
read A, subtract five hundred, write A, read B, add five hundred, write B.''',
     T(0, '[h:Transaction] = one logical unit of work'), T(1, 'Transfer 500: R(A); A = A - 500; W(A); R(B); B = B + 500; W(B)', size=34, color='black'))
beat(p, '''A C I D. Atomicity: all or nothing. If the system fails after writing A, the change to A is undone. Consistency: the database moves from one correct state to another,
so A plus B stays the same. Isolation: transactions running together do not disturb each other. Durability: once committed, changes survive even a crash.''',
     Stamp(1650, 140, 'MOST ASKED'),
     Tab(180, 360, [260, 640, 480], 60, [['Property', 'Meaning', 'Ensured by'], ['Atomicity', 'all or nothing', 'recovery manager (undo)'],
         ['Consistency', 'correct state -> correct state (A + B same)', 'programmer + constraints'], ['Isolation', 'concurrent = as if alone', 'concurrency control'],
         ['Durability', 'committed changes survive crashes', 'recovery manager (redo)']], size=28, colors={(r, 0): 'red' for r in range(1, 5)}))

p = page('Transaction States', 8)
beat(p, '''A transaction moves through states. It starts in the active state while running. After the last statement, it is partially committed.
If all changes are saved safely, it becomes committed.''',
     Ell(180, 420, 220, 90, 'Active', size=32, color='blue'), Ell(560, 280, 330, 90, 'Partially\ncommitted', size=28, color='blue'),
     Ell(1060, 280, 260, 90, 'Committed', size=30, color='green'),
     Arr(360, 430, 600, 360, label='last statement', lx=-80, ly=-6, size=24), Arr(890, 325, 1060, 325))
beat(p, '''If something goes wrong, it goes to the failed state. Then it is rolled back to the aborted state. After an abort, we can restart or kill the transaction.
Committed and aborted transactions are finally terminated.''',
     Ell(560, 600, 230, 90, 'Failed', size=32, color='red'), Ell(1060, 600, 260, 90, 'Aborted', size=30, color='red'),
     Ell(1500, 440, 280, 90, 'Terminated', size=30, color='black'),
     Arr(330, 500, 590, 610, label='error', lx=-30, ly=10, size=24), Arr(720, 370, 680, 600, label='fail', lx=40, size=24), Arr(790, 645, 1060, 645, label='rollback', size=24),
     Arr(1300, 330, 1520, 445), Arr(1300, 615, 1520, 515), T(0, 'restart or kill', x=1080, y=760, size=30, color='red'))

p = page('Schedules & Conflicting Operations', 8)
beat(p, '''A schedule is the order in which operations of many transactions run. In a serial schedule, one transaction finishes before the next starts.
It is always correct but slow. A concurrent schedule interleaves them, which is faster but can cause problems.''',
     T(0, '[h:Serial]: one after another (correct, slow)'), T(1, '[h:Concurrent]: interleaved (fast, risky)'))
beat(p, '''Two operations conflict if they belong to different transactions, use the same data item, and at least one of them is a write.
So read write, write read and write write pairs conflict. Read read never conflicts.''',
     Stamp(1600, 280), T(3, 'Conflict: different T, same item, [r:at least one write]', color='black'),
     Tab(180, 430, [200, 200, 260], 52, [['', 'R(X)', 'W(X)'], ['R(X)', '[g:no]', '[r:conflict]'], ['W(X)', '[r:conflict]', '[r:conflict]']], size=30))
beat(p, '''Problems without control: the lost update, where one write overwrites another. The dirty read, where a transaction reads uncommitted data.
The unrepeatable read, where the same read gives different values. And the phantom problem, where new rows appear in a repeated query.''',
     N(9, 1, '[r:Lost update] (W-W)'), N(10, 2, '[r:Dirty read] (W-R, uncommitted)'), N(11, 3, '[r:Unrepeatable read] (R-W)'), N(12, 4, '[r:Phantom] (new rows appear)'))

SCH = 'R1(X) R2(Z) R1(Z) R3(X) R3(Y) W1(X) W3(Y) R2(Y) W2(Z) W2(Y)'; ops, E = precedence(SCH); order = topo({1, 2, 3}, E)
p = page('Conflict Serializability', 8)
beat(p, '''A schedule is conflict serializable if it can be turned into a serial schedule by swapping non conflicting operations. We test it with a precedence graph.
Draw a node for each transaction. For each conflicting pair, draw an edge from the transaction that comes first to the one that comes later.
If the graph has no cycle, the schedule is conflict serializable.''',
     Stamp(1650, 140, 'NUMERICAL'), T(0, 'Precedence graph: Ti -> Tj if Ti\'s op conflicts with a later Tj op'), T(1, '[h:No cycle => conflict serializable]', color='red'))
cols = {1: [], 2: [], 3: []}
rows = [['', 'T1', 'T2', 'T3']] + [[str(i + 1)] + [f'{a}({x})' if t == c else '' for c in (1, 2, 3)] for i, (a, t, x) in enumerate(ops)]
beat(p, '''Example. Here is a schedule of three transactions. Look for conflicts. T1 reads Z, and later T2 writes Z, so draw T1 to T2.
T3 reads X, and later T1 writes X, so draw T3 to T1. T3 writes Y, and later T2 reads and writes Y, so draw T3 to T2.''',
     Tab(180, 300, [70, 150, 150, 150], 40, rows, size=26),
     *Tree({'T3': (1150, 420, 'T3', 'red'), 'T1': (1000, 650, 'T1', 'blue'), 'T2': (1400, 650, 'T2', 'blue')}, [('T3', 'T1'), ('T3', 'T2')], w=110, h=76, size=32, head=True),
     Arr(1058, 650, 1342, 650, color='black', label='Z', ly=-14), T(0, 'X', x=1050, y=530, size=28, color='red'), T(0, 'Y', x=1300, y=530, size=28, color='red'))
beat(p, f'''There is no cycle in this graph. So the schedule is conflict serializable. To get the equivalent serial order, do a topological sort, which gives T3 first, then T1, and then T2.''',
     T(0, 'No cycle  =>  [h:conflict serializable]', x=960, y=L(12), size=34, color='green'),
     T(0, f"Serial order: {' -> '.join('T' + str(t) for t in order)}", x=960, y=L(13), size=36, color='red'))
beat(p, '''Second example: R1 A, R2 A, W1 A, W2 A. T1 reads A before T2 writes it, so T1 to T2. T2 reads A before T1 writes it, so T2 to T1. That is a cycle,
so it is not conflict serializable. This is exactly the lost update problem.''',
     T(14, 'R1(A) R2(A) W1(A) W2(A): T1->T2 and T2->T1  =>  [r:cycle, not serializable]', size=32, color='black'))

p = page('View Serializability & Recoverability', 8)
beat(p, '''Two schedules are view equivalent if three things match. The same transaction does the initial read of each item, each read gets its value from the same write,
and the same transaction does the final write. Every conflict serializable schedule is view serializable, but not the other way.
A view serializable schedule that is not conflict serializable always has a blind write, which is a write without a read.''',
     S(0, 'View equivalent if same:', size=36), N(1, 1, 'initial reads'), N(2, 2, 'read-from (who wrote the value read)'), N(3, 3, 'final writes'),
     T(4, 'Conflict serializable ⊆ View serializable  (blind writes)', color='green'))
beat(p, '''Recoverability. A schedule is recoverable if a transaction commits only after every transaction it read from has committed.
If T2 reads a value written by T1 and commits first, and then T1 fails, we cannot undo T2. That schedule is not recoverable.''',
     Stamp(1600, 420), T(6, '[h:Recoverable]: Tj reads from Ti  =>  Ti commits before Tj'),
     T(7, 'W1(A) R2(A) C2 ... T1 fails  =>  [r:not recoverable]', color='black'))
beat(p, '''A cascading rollback happens when one failure forces many transactions to roll back. A cascadeless schedule avoids this,
because transactions read only committed data. A strict schedule is even stronger: no read or write of an item until the last writer commits.''',
     T(9, '[k:Cascadeless]: read only committed data'), T(10, '[k:Strict]: no read / write until the writer commits'),
     T(12, 'Strict ⊆ Cascadeless ⊆ Recoverable', color='green', size=40))

# ===================================================================================== CH 9
p = chapter(9)
beat(p, 'Chapter nine. Concurrency control and recovery.')

p = page('Locks & Two-Phase Locking', 9)
beat(p, '''Locks control access to data. A shared lock, S, is for reading. Many transactions can hold shared locks together.
An exclusive lock, X, is for writing. Only one transaction can hold it, and nobody else can read or write.''',
     T(0, '[h:Shared (S)]: read, many can share'), T(1, '[h:Exclusive (X)]: write, only one'),
     Tab(1200, 230, [150, 150, 150], 56, [['', 'S', 'X'], ['S', '[g:yes]', '[r:no]'], ['X', '[r:no]', '[r:no]']], size=30), T(0, 'Compatibility', x=1200, y=215, size=30, color='red'))
beat(p, '''Two phase locking, or two P L. Each transaction has two phases. In the growing phase it can only take locks. In the shrinking phase it can only release locks.
Once it releases any lock, it cannot take a new one. Two phase locking guarantees conflict serializability. But it does not prevent deadlocks.''',
     Stamp(1650, 440, 'MOST ASKED'), S(4, 'Two-Phase Locking (2PL)', size=38, color='red'), T(5, '[k:Growing phase]: only acquire locks'), T(6, '[k:Shrinking phase]: only release locks'),
     T(7, '[g:✓ conflict serializable]   [r:✗ deadlock possible]'),
     Ln([(1100, 820), (1350, 600), (1600, 820)], 'blue', 5), T(0, 'lock point', x=1270, y=580, size=28, color='red'),
     T(0, 'growing', x=1110, y=700, size=28, color='green'), T(0, 'shrinking', x=1480, y=700, size=28, color='green'), Ln([(1060, 830), (1660, 830)], 'black', 3))
beat(p, '''Strict two phase locking holds all exclusive locks until commit or abort, which avoids cascading rollbacks. Rigorous two phase locking holds all locks,
shared and exclusive, until commit.''',
     T(9, '[k:Strict 2PL]: hold X locks till commit (no cascading)'), T(10, '[k:Rigorous 2PL]: hold ALL locks till commit'))

p = page('Deadlock Handling', 9)
beat(p, '''A deadlock happens when transactions wait for each other forever. For example, T1 holds A and wants B, while T2 holds B and wants A.
We detect it with a wait for graph. A cycle means a deadlock.''',
     T(0, '[h:Deadlock]: T1 holds A, wants B;  T2 holds B, wants A'),
     *Tree({'T1': (1250, 330, 'T1', 'red'), 'T2': (1650, 330, 'T2', 'red')}, [('T1', 'T2')], w=120, h=80, size=32, head=True),
     Arr(1590, 370, 1310, 370, color='black', curve=-60, label='waits', ly=40, size=26), T(0, 'waits', x=1410, y=300, size=26),
     T(1, 'Wait-for graph: [r:cycle = deadlock]'))
beat(p, '''To prevent deadlocks, we can use timestamps. An older transaction has a smaller timestamp. In the wait die scheme, when an older transaction needs a lock that a younger one holds,
the older one simply waits. But when a younger one needs a lock that an older one holds, the younger one dies, which means it is rolled back.''',
     Stamp(1650, 470), S(3, 'Prevention (older = smaller timestamp)', size=36, color='red'),
     Tab(180, 470, [330, 420, 420], 58, [['Requester', 'Wait-die', 'Wound-wait'], ['Older', '[g:waits]', '[r:wounds] (kills) younger'], ['Younger', '[r:dies] (rollback)', '[g:waits]']],
         size=30))
beat(p, '''In wound wait, an older transaction wounds the younger one, which means forces it to roll back, and a younger transaction waits.
In both methods, the rolled back transaction restarts with its old timestamp, so it never starves. Another method is detection: find a cycle and roll back a victim.''',
     T(9, 'Restart with the [h:same old timestamp] => no starvation'), T(10, 'Detection: find cycle, roll back a victim (least cost)', color='green'))

p = page('Timestamp Ordering Protocol', 9)
beat(p, '''In timestamp ordering, each transaction gets a timestamp when it starts. Each data item keeps a read timestamp and a write timestamp,
the largest timestamps of transactions that read and wrote it.''',
     T(0, 'TS(T) = start time;   item X keeps [k:RTS(X)] and [k:WTS(X)]'))
beat(p, '''Read rule: if T wants to read X, but a younger transaction already wrote X, meaning TS of T is less than the write timestamp, T is rolled back.
Otherwise the read is allowed. Write rule: if a younger transaction already read or wrote X, T is rolled back. Otherwise the write is allowed.''',
     S(2, 'Read(X) by T', size=36, color='red'), T(3, 'TS(T) < WTS(X)  =>  rollback T;   else read, RTS = max(RTS, TS(T))', size=34),
     S(5, 'Write(X) by T', size=36, color='red'), T(6, 'TS(T) < RTS(X)  or  TS(T) < WTS(X)  =>  rollback T;   else write', size=34),
     Stamp(1650, 300))
beat(p, '''Thomas write rule improves this. If T wants to write X but a younger transaction has already written it, T's write is outdated,
so we simply ignore it instead of rolling back. Timestamp ordering is deadlock free, because no transaction ever waits.''',
     T(8, "[h:Thomas write rule]: TS(T) < WTS(X)  =>  ignore the old write"), T(9, '[g:✓ conflict serializable]  [g:✓ deadlock-free]  (no waiting)'))

p = page('Log-Based Recovery & Checkpoints', 9)
beat(p, '''Recovery brings the database back to a correct state after a crash. The system keeps a log on stable storage, with records like
T start, T writes X from old value to new value, and T commit. In deferred update, changes are written to the database only after commit, so we only need redo.
In immediate update, changes can be written before commit, so we need both undo and redo.''',
     T(0, 'Log: <T start>, <T, X, old, new>, <T commit>', color='black'),
     T(1, '[k:Deferred update]: write after commit  =>  only REDO'), T(2, '[k:Immediate update]: write anytime  =>  UNDO + REDO'))
tx = [('T1', 220, 520, True), ('T2', 380, 1000, True), ('T3', 600, None, False), ('T4', 950, 1250, True), ('T5', 1150, None, False)]
CK, CR = 800, 1450
els = [Ln([(CK, 400), (CK, 880)], 'green', 4), T(0, 'checkpoint', x=CK - 70, y=390, size=28, color='green'),
       Ln([(CR, 400), (CR, 880)], 'red', 5), T(0, 'crash', x=CR - 35, y=390, size=28, color='red')]
for i, (n, a, b, c) in enumerate(tx):
    y = 460 + i * 90; e = b if b else CR
    els += [T(0, n, x=168, y=y + 10, size=32, color='black'), Ln([(a, y), (e, y)], 'blue', 6)]
    if c: els.append(T(0, 'commit', x=b - 40, y=y - 14, size=22, color='green'))
act = {'T1': 'ignore', 'T2': '[g:REDO]', 'T3': '[r:UNDO]', 'T4': '[g:REDO]', 'T5': '[r:UNDO]'}
beat(p, '''A checkpoint saves everything to disk at a point in time, so after a crash we only look at the log after the last checkpoint.
Here, five transactions run, and the system crashes at the red line.''', *els)
beat(p, '''T1 committed before the checkpoint, so we ignore it. T2 and T4 committed after the checkpoint but before the crash, so we redo them.
T3 and T5 had not committed when the crash happened, so we undo them. Shadow paging is another method that keeps two page tables and needs no log.''',
     *[T(0, f'{n}: {act[n]}', x=1550, y=470 + i * 90, size=32, color='black') for i, (n, *_r) in enumerate(tx)],
     T(14, 'committed after checkpoint -> REDO;  not committed -> UNDO;  before checkpoint -> ignore', size=30, color='red'))

# ===================================================================================== CH 10
p = chapter(10)
beat(p, 'Chapter ten. Indexing, B plus trees and hashing. GATE numericals come from here.')

p = page('File Organization & Index Types', 10)
beat(p, '''Records are stored in files. A heap file stores records in any order. A sequential file keeps them sorted on a key. A hash file uses a hash function on a key.''',
     T(0, 'Files: [k:heap] (any order), [k:sequential] (sorted), [k:hash]'))
beat(p, '''An index is like the index of a book. It helps find records without reading the whole file. A dense index has an entry for every record.
A sparse index has an entry for only some records, usually one per block, so the file must be sorted.''',
     T(2, '[h:Dense]: entry for every record'), T(3, '[h:Sparse]: entry per block (file must be sorted)'), Stamp(1600, 280))
beat(p, '''A primary index is built on the ordering key field of a sorted file, and it is sparse. A clustering index is built on an ordering field that is not a key.
A secondary index is built on a non ordering field, and it is dense. Each file can have just one primary or clustering index, but it can have many secondary indexes.
And when an index grows too big, we build a multilevel index, which is simply an index on the index.''',
     Tab(180, 470, [280, 540, 300], 54, [['Index', 'Built on', 'Dense / sparse'], ['Primary', 'ordering KEY field', 'sparse'], ['Clustering', 'ordering NON-key field', 'sparse'],
         ['Secondary', 'non-ordering field', 'dense']], size=30, colors={(r, 0): 'red' for r in range(1, 4)}),
     T(13, 'one primary OR clustering, many secondary;  big index -> [h:multilevel index]', size=32, color='green'))

ix = index_example()
p = page('Index Numerical: Block Accesses', 10)
beat(p, '''A classic numerical. A file has thirty thousand records. The block size is one thousand twenty four bytes, and each record is one hundred bytes.
So the blocking factor is one thousand twenty four divided by one hundred, which is ten records per block, and the file needs three thousand blocks.''',
     Stamp(1650, 140, 'NUMERICAL'), T(0, 'r = 30,000 records, B = 1024 bytes, R = 100 bytes', color='black'),
     T(1, f'bfr = ⌊1024 / 100⌋ = {ix["bfr"]} records per block'), T(2, f'blocks b = 30,000 / {ix["bfr"]} = [h:{ix["b"]}]'))
beat(p, f'''With no index, a linear search reads about half of the blocks on average, so fifteen hundred block accesses. If the file is sorted on the key, a binary search needs
log base two of three thousand, rounded up. That is twelve block accesses.''',
     T(4, f'Linear search: b / 2 = {ix["lin"]} block accesses (average)'), T(5, f'Binary search: ⌈log2 {ix["b"]}⌉ = [h:{ix["binary"]}]'))
beat(p, f'''Now build a primary index. Each index entry has a nine byte key and a six byte block pointer, so fifteen bytes. That gives sixty eight entries per block.
We need one entry per data block, so three thousand entries, which fit in forty five index blocks. Binary search on the index takes six accesses,
plus one to read the data block. That is seven, instead of twelve.''',
     T(7, f'Index entry = 9 + 6 = {ix["Ri"]} bytes  =>  {ix["bfri"]} entries per block'), T(8, f'Index blocks = ⌈{ix["b"]} / {ix["bfri"]}⌉ = {ix["bi"]}'),
     T(9, f'Accesses = ⌈log2 {ix["bi"]}⌉ + 1 = 6 + 1 = [h:{ix["idx"]}]', color='red', size=40), T(10, f'{ix["binary"]} -> {ix["idx"]} block accesses with the index', color='green'))

p = page('B Tree vs B+ Tree', 10)
beat(p, '''B trees and B plus trees are balanced search trees, and they are used for multilevel indexes. Every leaf sits at the same level, so searching is always fast.
In a B tree, data pointers are kept in every node. In a B plus tree, the data pointers are kept only in the leaves, and the internal nodes just guide the search.''',
     T(0, 'Balanced: all leaves at the same level'),
     Tab(180, 320, [380, 520, 560], 56, [['', 'B tree', 'B+ tree'], ['data pointers', 'in all nodes', 'only in leaves'], ['keys repeated?', 'no', 'yes (copied up)'],
         ['leaves linked?', 'no', '[g:yes], easy range queries'], ['fan-out', 'smaller', '[g:larger] (more keys per node)'], ['used in', 'less common', 'most DBMS indexes']], size=28,
         colors={(r, 0): 'red' for r in range(1, 6)}),
     Stamp(1650, 140, 'MOST ASKED'))
beat(p, '''Because internal nodes of a B plus tree hold only keys, more keys fit in a block, so the tree is shorter. And because the leaves are linked,
range queries like salary between forty and sixty thousand are very fast. That is why most databases use B plus trees.''',
     T(13, 'B+ tree: shorter tree + linked leaves  =>  [h:fast range queries]', color='green'))

po, pl = bplus_order(512, 9, 6, 7)
p = page('B+ Tree Order', 10)
beat(p, '''GATE asks for the order of a B plus tree. Example: block size five hundred twelve bytes, key nine bytes, block pointer six bytes, and record pointer seven bytes.
An internal node with order p has p block pointers and p minus one keys.''',
     Stamp(1650, 140, 'GATE'), T(0, 'B = 512, key V = 9, block ptr P = 6, record ptr Pr = 7 (bytes)', color='black'))
beat(p, f'''So p times six, plus p minus one times nine, must be at most five hundred twelve. That gives fifteen p at most five hundred twenty one,
so p is thirty four.''',
     S(2, 'Internal node', size=38, color='red'), T(3, 'p × P + (p - 1) × V ≤ B'), T(4, '6p + 9(p - 1) ≤ 512  =>  15p ≤ 521'),
     T(5, f'p = ⌊521 / 15⌋ = [h:{po}]', size=42, color='red'))
beat(p, f'''A leaf node has p leaf pairs of key and record pointer, plus one block pointer to the next leaf. So p leaf times nine plus seven,
plus six, must be at most five hundred twelve. Sixteen p leaf at most five hundred six, so p leaf is thirty one.''',
     S(7, 'Leaf node', size=38, color='red'), T(8, 'p_leaf × (V + Pr) + P ≤ B'), T(9, '16 p_leaf + 6 ≤ 512  =>  16 p_leaf ≤ 506'),
     T(10, f'p_leaf = ⌊506 / 16⌋ = [h:{pl}]', size=42, color='red'))

bt = BPT(3)
for k in [1, 4, 7, 10, 17, 21, 31, 25, 19, 20, 28, 42]: bt.insert(k)
lv = bt.shape(); CW = 64
def node(x, y, keys, color='blue'):
    return Tab(x, y, [CW] * 3, 56, [[str(k) for k in keys] + [''] * (3 - len(keys))], size=28, hdr=False, color=color)
leaves = lv[2]; LW = 3 * CW; gap = 52; tot = len(leaves) * LW + (len(leaves) - 1) * gap; lx0 = (1920 - tot) // 2 + 60
leaf_x = [lx0 + i * (LW + gap) for i in range(len(leaves))]
mid = lv[1]; mid_x = [(leaf_x[0] + leaf_x[2] + LW) // 2 - LW // 2, (leaf_x[3] + leaf_x[5] + LW) // 2 - LW // 2]
root_x = (mid_x[0] + mid_x[1]) // 2
Y0, Y1, Y2 = 470, 640, 810
p = page('B+ Tree Insertion', 10)
beat(p, '''Let's build a B plus tree. Each node holds at most three keys. Insert one, four, seven, ten, seventeen, twenty one, thirty one, twenty five, nineteen, twenty,
twenty eight, and forty two. When a leaf gets four keys, it splits into two leaves, and the first key of the right leaf is copied up to the parent.''',
     Stamp(1650, 140, 'NUMERICAL'), T(0, 'Max 3 keys per node.  Insert: 1, 4, 7, 10, 17, 21, 31, 25, 19, 20, 28, 42', color='black', size=34),
     T(1, '[k:Leaf split]: copy first key of right leaf up', size=34), T(2, '[k:Internal split]: move middle key up', size=34))
beat(p, '''After all insertions, the root holds twenty. The internal nodes hold seven and seventeen on the left, and twenty five and thirty one on the right.
The leaves hold all the keys in order: one four, seven ten, seventeen nineteen, twenty twenty one, twenty five twenty eight, and thirty one forty two.''',
     node(root_x, Y0, lv[0][0][0], 'red'),
     *[node(mid_x[i], Y1, mid[i][0]) for i in range(2)],
     *[node(leaf_x[i], Y2, leaves[i][0], 'green') for i in range(len(leaves))],
     *[Arr(root_x + 10 + i * 160, Y0 + 56, mid_x[i] + LW // 2, Y1) for i in range(2)],
     *[Arr(mid_x[i // 3] + 8 + (i % 3) * CW, Y1 + 56, leaf_x[i] + LW // 2, Y2) for i in range(6)],
     *[Arr(leaf_x[i] + LW, Y2 + 28, leaf_x[i + 1], Y2 + 28, color='green') for i in range(5)])
beat(p, '''Notice: every key appears in a leaf, the leaves are linked for range queries, and the tree stays balanced, with all leaves at the same level.''',
     T(14, 'All keys in leaves · leaves linked · all leaves on one level', color='green', size=34))

HT, probes = linear_probe([10, 22, 31, 4, 15, 28, 17, 88, 59], 11)
p = page('Hashing', 10)
beat(p, '''Hashing finds a record directly, by applying a hash function to the key, for example the key mod the table size. When two keys land in the same slot, we call it a collision.
Chaining keeps a linked list in every slot. Open addressing looks for another free slot, using linear probing, quadratic probing, or double hashing.''',
     T(0, 'h(k) = k mod m;   same slot = [r:collision]'), T(1, '[k:Chaining]: list per slot   [k:Open addressing]: linear / quadratic probing'))
beat(p, '''Example. Insert ten, twenty two, thirty one, four, fifteen, twenty eight, seventeen, eighty eight and fifty nine into a table of size eleven with linear probing.
Fifteen goes to slot four, which is taken by four, so it moves to five. Seventeen moves from six to seven. Eighty eight moves from zero to one.
And fifty nine starts at four and moves to eight.''',
     Stamp(1650, 140, 'NUMERICAL'),
     Tab(180, 360, [110] + [100] * 11, 56, [['slot'] + [str(i) for i in range(11)], ['key'] + [str(v) if v is not None else '' for v in HT]], size=28,
         colors={(1, i + 1): 'red' for i, v in enumerate(HT) if v in (15, 17, 88, 59)}),
     T(8, '15: 4 -> 5   17: 6 -> 7   88: 0 -> 1   59: 4 -> 5 -> 6 -> 7 -> 8', size=34, color='red'))
beat(p, '''Static hashing has a fixed number of buckets. Dynamic hashing grows with the data. Extendible hashing uses a directory with a global depth,
and buckets with local depths. When a bucket overflows, it splits, and the directory doubles only if needed.''',
     T(10, '[h:Extendible hashing]: directory (global depth) + buckets (local depth)', size=34), T(11, 'bucket overflow -> split;  directory doubles if local = global', size=34, color='green'))

p = page('Query Processing & NoSQL', 10)
beat(p, '''Query processing has three steps. Parsing and translation checks the query and converts it to relational algebra. Optimization chooses the cheapest plan.
And evaluation runs that plan. The cost is mostly the number of disk block transfers and seeks.''',
     Box(180, 230, 360, 80, 'Parse & translate', size=30), Box(680, 230, 300, 80, 'Optimize', color='red', size=30), Box(1120, 230, 280, 80, 'Evaluate', size=30),
     Box(1540, 230, 200, 80, 'Result', color='green', size=30), Arr(540, 270, 680, 270), Arr(980, 270, 1120, 270), Arr(1400, 270, 1540, 270),
     T(3, 'Cost = disk block transfers + seeks', size=34))
beat(p, '''Heuristic optimization rules: do selections as early as possible, do projections early, and join small results first. This keeps intermediate tables small.''',
     S(5, 'Heuristics', size=36, color='red'), T(6, 'push σ (selection) down · do π (projection) early · join small results first', size=34))
beat(p, '''No S Q L databases store data without fixed tables, and scale across many servers. There are four types: key value stores like Redis,
document stores like MongoDB, column family stores like Cassandra, and graph databases like Neo four J. The C A P theorem says a distributed system can fully guarantee
only two of consistency, availability and partition tolerance at the same time.''',
     S(8, 'NoSQL types', size=36, color='red'), T(9, 'key-value (Redis) · document (MongoDB) · column-family (Cassandra) · graph (Neo4j)', size=32),
     T(11, '[h:CAP theorem]: only 2 of Consistency, Availability, Partition tolerance', size=34))

# ===================================================================================== CH 11
p = chapter(11)
beat(p, "Chapter eleven. Exam revision. If you're short on time, revise these first.")

p = page('Most Asked Exam Questions', 11)
qs = ['DBMS vs file system; three-schema architecture', 'Data independence (physical vs logical)', 'ER diagram + convert to tables',
      'Keys; count super keys', 'Relational algebra queries; division', 'SQL: GROUP BY, HAVING, second highest salary',
      'Attribute closure + candidate keys', '1NF, 2NF, 3NF, BCNF + find the normal form', 'Lossless join, dependency preservation',
      'ACID; conflict serializability (precedence graph)', '2PL, deadlock (wait-die / wound-wait), timestamps', 'B+ tree order + insertion; indexing numerical']
beat(p, '''Here are the most asked questions. D B M S versus file system, and the three schema architecture. Data independence. E R diagrams and converting them to tables.
And keys, with counting super keys.''', *[T(k, f'{k + 1}. {qq}', x=200, size=36) for k, qq in enumerate(qs[:4])])
beat(p, '''Relational algebra queries and division. S Q L with group by, having, and the second highest salary. Attribute closure and candidate keys.
And the normal forms, with finding the highest normal form.''', *[T(k, f'{k + 1}. {qq}', x=200, size=36) for k, qq in enumerate(qs) if 4 <= k < 8])
beat(p, '''Lossless join and dependency preservation. A C I D and conflict serializability with the precedence graph. Two phase locking, deadlocks and timestamps.
And the B plus tree order, insertion, and the indexing numerical.''', *[T(k, f'{k + 1}. {qq}', x=200, size=36) for k, qq in enumerate(qs) if k >= 8])
beat(p, '''Here's one last exam tip. In normalization questions, always start by finding the candidate keys. And in numericals, write the formula before the answer.
This way you still earn step marks, even if your final answer goes wrong.''',
     T(13, 'Tip: find candidate keys first; [h:write the formula first] => step marks!', color='red'))

p = page('All the Best!', 11, kind='outro')
beat(p, '''That's the complete D B M S subject. If this helped you, share it with your friends who have the exam,
and subscribe to TechVibe24 for more one shot videos. Tell me in the comments which subject you want next. All the best for your exam!''')

if __name__ == '__main__':
    json.dump({'pages': PAGES, 'chapters': CHAPTERS}, open('db_script.json', 'w'), indent=1, ensure_ascii=False)
    nb = sum(len(p['beats']) for p in PAGES); nw = sum(len(b['say'].split()) for p in PAGES for b in p['beats'])
    print('pages', len(PAGES), 'beats', nb, 'words', nw, 'est minutes', round(nw / 150, 1))
