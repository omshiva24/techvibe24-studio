'''Operating System one-shot: narration beats + handwritten note elements for every page.
Markup inside text: [r:red] [g:green] [k:black] [h:yellow highlight] [p:pink highlight]'''
import json
from numericals import *

PAGES = []
def L(n): return 222 + 54 * n            # baseline of ruled line n (0..14)
def page(title, ch, kind='page', **kw): p = dict(kind=kind, title=title, ch=ch, beats=[], **kw); PAGES.append(p); return p
def beat(p, say, *els): p['beats'].append({'say': ' '.join(say.split()), 'els': [e for e in els if e]})
def T(n, s, x=180, size=36, font='body', color='blue', y=None): return dict(t='text', x=x, y=L(n) if y is None else y, s=s, size=size, font=font, color=color)
def S(n, s, x=180, color='black', size=42, y=None): return T(n, s, x, size, 'bold', color, y)
def B(n, s, x=180, color='blue', size=36, mark='•'): return T(n, f'{mark} {s}', x, size, 'body', color)
def N(n, k, s, x=180, color='blue', size=36): return T(n, f'{k}) {s}', x, size, 'body', color)
def Box(x, y, w, h, label=None, color='black', size=32, fill=None, lc=None): return dict(t='rect', x=x, y=y, w=w, h=h, label=label, color=color, size=size, fill=fill, lc=lc or color)
def Ell(x, y, w, h, label=None, color='black', size=32, fill=None, lc=None): return dict(t='ellipse', x=x, y=y, w=w, h=h, label=label, color=color, size=size, fill=fill, lc=lc or color)
def Arr(x1, y1, x2, y2, color='black', label=None, lx=0, ly=-14, curve=0, head=True, size=28, both=False, lc=None): return dict(t='arrow', p1=(x1, y1), p2=(x2, y2), color=color, label=label, lx=lx, ly=ly, curve=curve, head=head, size=size, both=both, lc=lc or color)
def Ln(pts, color='black', w=4): return dict(t='line', pts=pts, color=color, w=w)
def Tab(x, y, cw, rh, rows, color='black', size=30, hdr=True, order='row', colors=None, fills=None): return dict(t='table', x=x, y=y, cw=cw, rh=rh, rows=rows, color=color, size=size, hdr=hdr, order=order, colors={f'{r},{c}': v for (r, c), v in (colors or {}).items()}, fills={f'{r},{c}': v for (r, c), v in (fills or {}).items()})
def Gantt(x, y, u, h, segs, color='blue', size=30): return dict(t='gantt', x=x, y=y, u=u, h=h, segs=segs, color=color, size=size)
def Stamp(x, y, text='IMP!', color='red', rot=-8, size=34): return dict(t='stamp', x=x, y=y, text=text, color=color, rot=rot, size=size)
def HL(x, y, w, h, color='yellow'): return dict(t='hl', x=x, y=y, w=w, h=h, color=color)
def fmt(v): return ('%.2f' % v).rstrip('0').rstrip('.')

CHAPTERS = [
 (1, 'Introduction to OS', ['What is an OS', 'Functions', 'Types of OS', 'System calls & dual mode', 'OS structures'], 3),
 (2, 'Processes & Threads', ['Process & its states', 'PCB & context switch', 'Schedulers', 'Threads', 'IPC'], 4),
 (3, 'CPU Scheduling', ['Terms & formulas', 'FCFS', 'SJF / SRTF', 'Round Robin', 'Priority & multilevel queue'], 5),
 (4, 'Process Synchronization', ['Race condition', 'Critical section', "Peterson's solution", 'Semaphores', 'Classical problems'], 5),
 (5, 'Deadlocks', ['4 necessary conditions', 'Resource allocation graph', 'Prevention / avoidance', "Banker's algorithm", 'Detection & recovery'], 5),
 (6, 'Memory Management', ['Logical vs physical address', 'First / best / worst fit', 'Fragmentation', 'Paging & TLB', 'Segmentation'], 5),
 (7, 'Virtual Memory', ['Demand paging', 'Page fault', 'FIFO / Optimal / LRU', "Belady's anomaly", 'Thrashing'], 5),
 (8, 'File Systems', ['File & access methods', 'Directory structures', 'Allocation methods', 'Free space management'], 4),
 (9, 'Disk Scheduling', ['Disk structure & access time', 'FCFS & SSTF', 'SCAN, C-SCAN, LOOK, C-LOOK', 'RAID levels'], 4),
 (10, 'Exam Revision', ['Most asked questions', 'Last-minute tips'], 5),
]
def chapter(i):
    n, t, subs, stars = CHAPTERS[i - 1]
    return page(t, n, kind='chapter', num=n, subs=subs, stars=stars)

# =====================================================================================
p = page('Operating System', 0, kind='cover')
beat(p, '''Operating System. The complete subject, in one video. Simple explanations, handwritten notes,
and every important exam problem solved step by step.''')
beat(p, '''This works for B Tech computer science in almost every university. A K T U, Anna University, V T U, J N T U,
Mumbai, Pune, and private universities too. And it covers the Operating System part of GATE. So grab a pen, and let's start.''')

p = page('Contents', 0)
beat(p, "Here's our plan for today. Ten chapters, from the basics to the exam numericals.",
     S(0, 'What we will cover today', color='black'))
items = ['Introduction to OS', 'Processes & Threads', '[h:CPU Scheduling]  (numericals)', '[h:Process Synchronization]',
         "[h:Deadlocks]  (Banker's algorithm)", '[h:Memory Management]  (paging, TLB)', '[h:Virtual Memory]  (page replacement)',
         'File Systems', '[h:Disk Scheduling]  (numericals)', 'Exam Revision - most asked questions']
beat(p, '''We start with what an operating system is, then processes and threads. Then the big scoring topics:
CPU scheduling, synchronization, and deadlocks.''', *[T(1 + k, f'{k + 1}.  {items[k]}', x=200) for k in range(5)])
beat(p, '''After that, memory management and virtual memory, file systems, and disk scheduling.
And at the end, a quick revision of the most asked exam questions. The highlighted ones are the most important.''',
     *[T(6 + k, f'{k + 6}.  {items[k + 5]}', x=200) for k in range(5)], Stamp(1500, 520, 'MOST ASKED', rot=-10))

# ===================================================================================== CH 1
p = chapter(1)
beat(p, "Chapter one. Introduction to operating systems. Let's build the basics first.")

p = page('What is an Operating System?', 1)
beat(p, '''An operating system is a program that sits between you and the hardware. It manages all the
resources of the computer, and gives you an easy way to use it.''',
     T(0, 'OS = a program that acts as an [h:interface]'), T(1, 'between the [r:user] and the [r:computer hardware].'),
     Box(1290, 250, 460, 80, 'User', size=34), Box(1290, 380, 460, 80, 'Application programs', size=32),
     Box(1290, 510, 460, 80, 'Operating System', color='red', size=34, fill='pink'), Box(1290, 640, 460, 80, 'Hardware', size=34),
     Arr(1520, 330, 1520, 380, both=True), Arr(1520, 460, 1520, 510, both=True), Arr(1520, 590, 1520, 640, both=True))
beat(p, '''Think of it like a manager in a company. The hardware is the workers. The apps are the customers.
And the operating system decides who gets what, and when.''',
     T(3, 'Example: [k:OS = manager] of the computer'), T(4, 'e.g. Windows, Linux, macOS, Android', color='green'))
beat(p, '''An OS has two main goals. Convenience, which means the computer is easy to use. And efficiency,
which means the hardware is used well, without waste. It is also called a resource manager,
and the kernel is the core part of the OS that is always running in memory.''',
     S(6, 'Goals of OS'), N(7, 1, '[r:Convenience] - easy to use'), N(8, 2, '[r:Efficiency] - use hardware well'),
     T(10, '[h:Resource manager]: CPU, memory, files, I/O devices'), T(11, '[k:Kernel] = core of OS, always in memory'))

p = page('Functions of OS', 1)
beat(p, '''Now, functions of an operating system. This is a very common 5 mark question.
First, process management. The OS creates and deletes processes, schedules them on the CPU, and handles synchronization.''',
     Stamp(1600, 140), N(0, 1, '[r:Process management] - create, delete, schedule, sync processes'))
beat(p, '''Second, memory management. It keeps track of which part of memory is used by whom, and allocates or frees memory.
Third, file management. Creating, deleting, and organizing files and directories.''',
     N(1, 2, '[r:Memory management] - track & allocate/free RAM'), N(2, 3, '[r:File management] - create, delete, organise files & folders'))
beat(p, '''Fourth, device or I O management. The OS talks to devices through device drivers, and uses buffering and spooling.
Fifth, security and protection, like passwords and access control.
And sixth, the user interface, which can be a command line or a graphical interface.''',
     N(3, 4, '[r:Device (I/O) management] - drivers, buffering, spooling'), N(4, 5, '[r:Security & protection] - passwords, access control'),
     N(5, 6, '[r:User interface] - CLI or GUI'))
beat(p, '''An easy way to remember them: P M F D S U. Process, memory, file, device, security, and user interface.''',
     T(7, 'Trick to remember:  [h:P - M - F - D - S - U]', size=40, color='green'))

p = page('Types of Operating Systems', 1)
beat(p, '''Next, types of operating systems. One. Batch operating system. Similar jobs are grouped into batches
and run one after another, without any user interaction. Example, payroll processing.''',
     N(0, 1, '[r:Batch OS] - jobs grouped in batches, no interaction (payroll)'))
beat(p, '''Two. Multiprogramming. Many programs are kept in memory. When one program waits for I O,
the CPU switches to another one. So the CPU is never idle.''',
     N(1, 2, '[r:Multiprogramming] - many programs in memory;'), T(2, 'when one waits for I/O, CPU runs another => [h:CPU never idle]', x=230))
beat(p, '''Three. Multitasking, also called time sharing. CPU time is cut into small slices, and it switches so fast
that every user feels the computer is only theirs.''',
     N(3, 3, '[r:Multitasking / Time-sharing] - small time slices,'), T(4, 'fast switching => every user feels it is only theirs', x=230))
beat(p, '''Four. Real time operating systems. Here the answer must come within a fixed deadline.
Hard real time means missing the deadline is a failure, like an airbag or a pacemaker.
Soft real time means small delays are okay, like video streaming.''',
     N(5, 4, '[r:Real-time OS] - response within a strict deadline'), T(6, '[k:Hard]: airbag, pacemaker  |  [k:Soft]: video streaming', x=230))
beat(p, '''Five. Distributed operating system. Many computers connected by a network work together like one system.
You may also see network OS and mobile OS like Android and iOS.''',
     N(7, 5, '[r:Distributed OS] - many computers work as one'), T(8, 'Others: Network OS, Mobile OS (Android, iOS)', x=230, color='green'))

p = page('System Calls & Dual Mode', 1)
beat(p, '''A system call is how a program asks the operating system for a service. For example, opening a file,
reading, writing, or creating a new process with fork.''',
     T(0, '[h:System call] = the way a program asks the OS for a service'), T(1, 'e.g.  open(), read(), write(), fork(), exit()', color='green'))
beat(p, '''Now, dual mode. The CPU works in two modes. User mode, where normal programs run, with mode bit one.
And kernel mode, where the OS runs, with mode bit zero. Dangerous instructions, called privileged instructions,
can run only in kernel mode.''',
     Box(1180, 330, 600, 90, 'User mode  (mode bit = 1)', color='blue', size=30),
     Box(1180, 560, 600, 90, 'Kernel mode  (mode bit = 0)', color='red', size=30),
     Arr(1330, 420, 1330, 560, label='system call / trap', lx=-150, ly=0, size=26), Arr(1630, 560, 1630, 420, label='return', lx=70, ly=0, size=26),
     T(3, '[r:User mode]: normal programs'), T(4, '[r:Kernel mode]: OS code'), T(5, 'Privileged instructions -> kernel mode only'))
beat(p, '''Types of system calls. Process control, file management, device management, information maintenance,
and communication. Remember these five.''',
     S(7, 'Types of system calls', size=38), N(8, 1, 'Process control (fork, exit)'), N(9, 2, 'File management (open, read)'),
     N(10, 3, 'Device management'), N(11, 4, 'Information maintenance (time, date)'), N(12, 5, 'Communication (pipe, send)'), Stamp(1500, 860))

p = page('OS Structures', 1)
beat(p, '''How is an OS built inside? Three common structures. First, monolithic. The whole OS is one big kernel.
It is fast, but hard to maintain, because one bug can crash everything. Example, early UNIX.''',
     S(0, '1) Monolithic', color='red', size=38), T(1, 'whole OS = one big kernel. [g:fast]  but  [r:hard to maintain]'),
     Box(1450, 210, 330, 170, 'Kernel (all)', color='black', size=30))
beat(p, '''Second, layered. The OS is divided into layers. Each layer uses only the layer below it.
Easy to build and debug, but it can be slower.''',
     S(3, '2) Layered', color='red', size=38), T(4, 'layers; each uses only the one below. [g:easy debug], [r:slower]'),
     Box(1450, 400, 330, 50, 'Layer N (UI)', size=26), Box(1450, 455, 330, 50, '...', size=26), Box(1450, 510, 330, 50, 'Layer 0 (hardware)', size=26))
beat(p, '''Third, microkernel. Only the most basic things stay in the kernel, like scheduling, memory basics, and message passing.
Everything else runs in user space. It is reliable and secure, but message passing adds overhead. Example, Mach and QNX.''',
     S(6, '3) Microkernel', color='red', size=38), T(7, 'only basics in kernel (IPC, scheduling, memory)'),
     T(8, 'rest in user space. [g:reliable, secure], [r:message overhead]'),
     Box(1450, 640, 330, 80, 'drivers  files  UI', color='blue', size=26), Box(1520, 760, 190, 70, 'micro kernel', color='red', size=24),
     Arr(1615, 720, 1615, 760, both=True))
beat(p, '''Modern systems like Linux and Windows are hybrids. They mix these ideas.''',
     T(10, 'Modern OS (Linux, Windows) = [h:hybrid]', color='green'))

# ===================================================================================== CH 2
p = chapter(2)
beat(p, 'Chapter two. Processes and threads. This is the heart of the operating system.')

p = page('Process', 2)
beat(p, '''A program is just a file on the disk. It is passive. When you run it, it becomes a process.
So a process is a program in execution. It is active.''',
     T(0, '[r:Program] = passive (code file on disk)'), T(1, '[r:Process] = [h:program in execution] (active)'))
beat(p, '''In memory, a process has four parts. Text, which is the code. Data, which holds global variables.
Heap, for memory allocated while running. And stack, for function calls and local variables.
Stack and heap grow towards each other.''',
     Box(1350, 230, 340, 90, 'Stack', size=32), Box(1350, 320, 340, 150, '', size=32), Box(1350, 470, 340, 90, 'Heap', size=32),
     Box(1350, 560, 340, 90, 'Data', size=32), Box(1350, 650, 340, 90, 'Text (code)', size=32),
     Arr(1520, 330, 1520, 380, color='green'), Arr(1520, 460, 1520, 410, color='green'),
     T(3, '[k:Text] - program code'), T(4, '[k:Data] - global variables'), T(5, '[k:Heap] - dynamic memory (malloc / new)'),
     T(6, '[k:Stack] - function calls, local variables'), T(8, 'Stack & heap grow towards each other', color='green'))

p = page('Process States', 2)
beat(p, '''The process state diagram. This is asked in almost every exam, so learn to draw it.
A process starts in the New state. When it is admitted, it goes to Ready, waiting for the CPU.''',
     Stamp(1640, 140, 'MUST DRAW'),
     Ell(200, 280, 230, 90, 'New', size=34), Ell(560, 540, 250, 90, 'Ready', size=34, color='blue'),
     Arr(380, 370, 600, 545, label='admitted', lx=-110, ly=0))
beat(p, '''The scheduler picks it, and it goes to Running. If an interrupt comes, or its time slice ends,
it goes back to Ready.''',
     Ell(1100, 540, 270, 90, 'Running', size=34, color='green'),
     Arr(810, 600, 1100, 600, label='scheduler dispatch', ly=36), Arr(1180, 540, 760, 545, curve=-110, label='interrupt', ly=-6))
beat(p, '''If it needs I O, or waits for some event, it goes to Waiting. When the I O completes,
it goes back to Ready, not directly to Running. And when it finishes, it goes to Terminated.''',
     Ell(830, 800, 260, 90, 'Waiting', size=34, color='red'), Ell(1460, 280, 290, 90, 'Terminated', size=34),
     Arr(1240, 630, 1040, 805, label='I/O or event wait', lx=150, ly=10), Arr(860, 805, 690, 630, label='I/O completed', lx=-120, ly=10),
     Arr(1300, 540, 1500, 370, label='exit', lx=40, ly=0),
     T(14, 'Waiting -> Ready (never directly to Running)', x=1080, size=30, color='red'))

p = page('PCB & Context Switch', 2)
beat(p, '''Every process has a Process Control Block, or P C B. It is like an ID card of the process.
The OS stores everything about the process here.''',
     T(0, '[h:PCB] = Process Control Block = "ID card" of a process'),
     Tab(1300, 250, [460], 52, [['Process ID'], ['Process state'], ['Program counter'], ['CPU registers'], ['Scheduling info'],
                                 ['Memory info'], ['I/O status'], ['Accounting info']], hdr=False, size=30, color='blue'))
beat(p, '''It holds the process I D, the state, the program counter, which is the address of the next instruction,
the CPU registers, scheduling information like priority, memory information, I O status, and accounting information.''',
     T(2, '[k:Program counter] = address of next instruction'), T(3, '[k:Scheduling info] = priority, queue pointers'))
beat(p, '''Context switch. When the CPU moves from one process to another, the OS saves the state of the old process
in its P C B, and loads the state of the new process from its P C B. During a context switch, no useful work is done,
so it is pure overhead.''',
     S(5, 'Context switch'), T(6, 'save old process state -> its PCB'), T(7, 'load new process state <- its PCB'),
     T(8, '[r:Pure overhead] - no useful work during the switch'), Stamp(900, 880, 'IMP!'))

p = page('Schedulers', 2)
beat(p, '''There are three types of schedulers. The long term scheduler, also called the job scheduler, picks processes from
the job pool and brings them into memory, into the ready queue. It controls the degree of multiprogramming.''',
     N(0, 1, '[r:Long-term] (job scheduler): new -> ready'), T(1, 'controls [h:degree of multiprogramming]', x=230))
beat(p, '''The short term scheduler, or CPU scheduler, picks a process from the ready queue and gives it the CPU.
It runs very often, so it must be very fast.''',
     N(2, 2, '[r:Short-term] (CPU scheduler): ready -> running'), T(3, 'runs very often => must be fast', x=230))
beat(p, '''The medium term scheduler does swapping. It removes a process from memory for some time, and brings it back later.
This reduces the load on memory.''',
     N(4, 3, '[r:Medium-term]: swapping (suspend / resume)'), T(5, 'reduces load on memory', x=230))
beat(p, '''Also remember. An I O bound process spends more time doing I O. A CPU bound process spends more time computing.
A good system keeps a mix of both.''',
     T(7, '[k:I/O-bound] - more I/O, short CPU bursts', color='green'), T(8, '[k:CPU-bound] - long CPU bursts', color='green'),
     T(9, 'Good scheduler = [h:mix of both]', color='green'))

p = page('Threads', 2)
beat(p, '''A thread is a lightweight process. It is the smallest unit of CPU execution.
All threads of a process share the code, the data, and open files. But each thread has its own stack,
registers, and program counter.''',
     T(0, '[h:Thread] = lightweight process, smallest unit of CPU use'),
     T(1, 'share: [g:code, data, files]   own: [r:stack, registers, PC]'),
     Box(1280, 330, 520, 80, 'code | data | files', size=30), Box(1280, 410, 170, 200, 'T1 stack', size=24, color='blue'),
     Box(1455, 410, 170, 200, 'T2 stack', size=24, color='blue'), Box(1630, 410, 170, 200, 'T3 stack', size=24, color='blue'))
beat(p, '''Why threads? Responsiveness, resource sharing, economy, because creating a thread is cheaper than a process,
and scalability on multicore CPUs.''',
     T(3, 'Benefits: responsiveness, resource sharing,'), T(4, 'economy (cheap to create), scalability (multicore)'))
beat(p, '''There are user level threads, managed by a library without the kernel knowing, which are fast.
And kernel level threads, managed by the OS, which are slower to create, but if one blocks, others can still run.''',
     T(6, '[r:User-level]: managed by library, fast, kernel unaware'), T(7, '[r:Kernel-level]: managed by OS, slower, one block ≠ all block'))
beat(p, '''Multithreading models. Many to one: many user threads on one kernel thread. If one blocks, all block.
One to one: each user thread gets its own kernel thread, used by Linux and Windows.
Many to many: many user threads on a smaller or equal number of kernel threads. The best of both.''',
     S(9, 'Multithreading models', size=38), T(10, '[k:Many-to-one]: one blocks => all block'),
     T(11, '[k:One-to-one]: Linux, Windows'), T(12, '[k:Many-to-many]: best of both'), Stamp(1500, 820))

p = page('Inter-Process Communication (IPC)', 2)
beat(p, '''Processes often need to talk to each other. This is called inter process communication.
There are two models. Shared memory, where processes share a region of memory. It is fast, but needs synchronization.''',
     T(0, '[h:IPC] - processes exchange data. Two models:'), S(1, '1) Shared memory', color='red', size=38),
     T(2, 'common memory region. [g:fast], but needs synchronization'),
     Box(1250, 230, 170, 110, 'P1', size=32), Box(1610, 230, 170, 110, 'P2', size=32), Box(1390, 380, 250, 90, 'shared', color='red', size=30),
     Arr(1335, 340, 1420, 380), Arr(1695, 340, 1610, 380))
beat(p, '''And message passing, where processes send and receive messages through the kernel.
It is easier to use and good for distributed systems, but slower. Pipes and sockets are examples.''',
     S(4, '2) Message passing', color='red', size=38), T(5, 'send() / receive() through kernel. [g:easy], [r:slower]'),
     T(6, 'e.g. pipes, message queues, sockets', color='green'),
     Box(1250, 560, 170, 110, 'P1', size=32), Box(1610, 560, 170, 110, 'P2', size=32), Arr(1420, 615, 1610, 615, label='message', ly=-16))

# ===================================================================================== CH 3
p = chapter(3)
beat(p, '''Chapter three. CPU scheduling. This chapter gives you guaranteed marks, because numericals come from here every year.''')

p = page('CPU Scheduling - Basics', 3)
beat(p, '''CPU scheduling means deciding which process in the ready queue gets the CPU next.
In non preemptive scheduling, once a process gets the CPU, it keeps it until it finishes or waits.
In preemptive scheduling, the OS can take the CPU away in the middle.''',
     T(0, 'Which ready process gets the CPU next?'), T(1, '[r:Non-preemptive]: keeps CPU till it finishes / waits'),
     T(2, '[r:Preemptive]: OS can take CPU away in between'))
beat(p, '''Scheduling criteria. We want high CPU utilization and high throughput, which is processes finished per unit time.
And we want low turnaround time, low waiting time, and low response time.''',
     S(4, 'Criteria'), T(5, 'Maximise: CPU utilisation, throughput', color='green'), T(6, 'Minimise: turnaround, waiting, response time', color='green'))
beat(p, '''Now the formulas. Write them down. Turnaround time equals completion time minus arrival time.
Waiting time equals turnaround time minus burst time. Response time equals the time it first gets the CPU, minus arrival time.''',
     Stamp(1500, 520, 'FORMULAS'), T(8, '[h:TAT = CT - AT]', size=44, color='red'), T(9, '[h:WT = TAT - BT]', size=44, color='red'),
     T(10, '[h:RT = first CPU time - AT]', size=44, color='red'),
     T(12, 'AT = arrival, BT = burst, CT = completion time', size=32, color='black'))

def sched_page(title, segs, say_algo, say_gantt, say_res, note_lines, note_say):
    p = page(title, 3)
    rows, atat, awt = results(PROCS, segs)
    beat(p, say_algo, Tab(180, 200, [110, 110, 110], 50, [['P', 'AT', 'BT']] + [[n, str(a), str(b)] for n, a, b in PROCS], size=30))
    beat(p, say_gantt, T(0, 'Gantt chart', x=640, color='black', size=36),
         Gantt(640, 260, 78, 80, segs))
    tab = [['P', 'CT', 'TAT', 'WT']] + [[r[0], str(r[3]), str(r[4]), str(r[5])] for r in rows]
    beat(p, say_res, Tab(180, 500, [110, 110, 120, 110], 50, tab, size=30, colors={(i, 3): 'red' for i in range(1, 5)}),
         T(0, f'Avg TAT = {sum(r[4] for r in rows)}/4 = [h:{fmt(atat)}]', x=700, y=600, color='black', size=40),
         T(0, f'Avg WT = {sum(r[5] for r in rows)}/4 = [h:{fmt(awt)}]', x=700, y=670, color='black', size=40))
    beat(p, note_say, *[T(0, s, x=700, y=760 + 56 * k, size=34, color='green') for k, s in enumerate(note_lines)])
    return p

segs = fcfs(PROCS); rows, atat, awt = results(PROCS, segs)
sched_page('FCFS - First Come First Serve', segs,
    '''First come first serve. The simplest one. Whoever comes first, gets the CPU first. It is non preemptive.
Let's solve this example. Four processes, P1 to P4, with these arrival times and burst times.''',
    '''P1 arrives at zero and runs for five units, till five. Then P2 runs from five to eight. P3 from eight to nine.
And P4 from nine to eleven.''',
    f'''Now apply the formulas. Turnaround time is completion minus arrival. Waiting time is turnaround minus burst.
So the average turnaround time is {fmt(atat)}, and the average waiting time is {fmt(awt)}.''',
    ['Non-preemptive, simple', 'Problem: [r:convoy effect] - short jobs', 'wait behind one long job'],
    '''FCFS is simple, but it has the convoy effect. Short processes get stuck waiting behind one long process.''')

segs = sjf(PROCS); rows, atat, awt = results(PROCS, segs)
sched_page('SJF - Shortest Job First', segs,
    '''Shortest job first. Among the processes that have arrived, pick the one with the smallest burst time.
Same example. Watch carefully.''',
    '''At time zero, only P1 has arrived, so P1 runs till five. At five, P2, P3 and P4 are all waiting.
P3 has the smallest burst, one, so it runs next. Then P4 with two. And finally P2.''',
    f'''Calculating again, the average turnaround time is {fmt(atat)}, and the average waiting time drops to {fmt(awt)}.
Better than FCFS.''',
    ['[h:Optimal] - minimum avg waiting time', 'Problem: [r:starvation] of long jobs', 'Preemptive SJF = [k:SRTF]'],
    '''SJF gives the minimum average waiting time, so it is called optimal. But long jobs can starve,
and in real life we do not know the burst time in advance. The preemptive version is called
shortest remaining time first, or S R T F.''')

segs = rr(PROCS, 2); rows, atat, awt = results(PROCS, segs)
sched_page('Round Robin (time quantum = 2)', segs,
    '''Round robin. Every process gets a fixed time slice, called the time quantum. Here the quantum is two.
When the time is up, the process goes to the back of the ready queue. This is preemptive.''',
    '''P1 runs from zero to two. Meanwhile P2 and P3 have arrived, so they are ahead of P1 in the queue.
P2 runs two to four. P3 needs only one unit, so it finishes at five. Then P1 again, five to seven.
P4 from seven to nine. P2 finishes at ten, and P1 at eleven.''',
    f'''The average turnaround time is {fmt(atat)}, and the average waiting time is {fmt(awt)}.
Round robin is not about the lowest waiting time. It is about fairness and quick response.''',
    ['Fair, good response time (time-sharing)', '[r:Large q] -> becomes FCFS', '[r:Small q] -> too many context switches'],
    '''If the quantum is very large, round robin becomes FCFS. If it is very small, there are too many context switches.
So choose it carefully.''')

p = page('Priority & Multilevel Queue', 3)
beat(p, '''Priority scheduling. Each process has a priority, and the highest priority runs first. Usually a smaller number
means higher priority, but always check the question. It can be preemptive or non preemptive.''',
     S(0, 'Priority scheduling', color='red', size=38), T(1, 'highest priority first (usually [k:small number = high])'))
beat(p, '''The problem is starvation. A low priority process may wait forever. The solution is aging.
We slowly increase the priority of processes that wait for a long time.''',
     T(2, 'Problem: [r:starvation]   Solution: [h:aging]'), T(3, 'aging = slowly raise priority of waiting processes', x=230, color='green'))
beat(p, '''Multilevel queue. The ready queue is split into separate queues. For example system processes, interactive processes,
and batch processes. Each queue can have its own algorithm. In a multilevel feedback queue,
a process can move between queues based on its behaviour.''',
     S(5, 'Multilevel queue', color='red', size=38),
     Box(1250, 470, 520, 70, 'System  (highest)', color='red', size=28), Box(1250, 545, 520, 70, 'Interactive  (RR)', color='blue', size=28),
     Box(1250, 620, 520, 70, 'Batch  (FCFS, lowest)', size=28),
     T(6, 'separate queues, each with its own algorithm'), T(7, '[k:Feedback queue]: process can move between queues'))
beat(p, '''Here's a quick summary to revise. FCFS is non preemptive, and has the convoy effect. SJF is optimal for waiting time,
but long jobs can starve. Round robin is preemptive and fair. Priority can starve, fixed with aging.''',
     Tab(180, 640, [260, 230, 360], 52, [['Algorithm', 'Preemptive?', 'Key point'], ['FCFS', 'No', 'convoy effect'],
         ['SJF', 'No', 'optimal avg WT'], ['SRTF', 'Yes', 'starvation'], ['Round Robin', 'Yes', 'fair, time quantum'], ['Priority', 'Both', 'starvation -> aging']],
         size=28))

# ===================================================================================== CH 4
p = chapter(4)
beat(p, 'Chapter four. Process synchronization. Theory questions from here are very common.')

p = page('Race Condition & Critical Section', 4)
beat(p, '''Imagine two processes updating the same shared variable, counter, at the same time. One adds one, the other subtracts one.
Because their steps mix up, the final answer can be wrong. When the result depends on the order of execution,
it is called a race condition.''',
     T(0, '[h:Race condition] = result depends on the order of execution'),
     T(1, 'e.g. P1: counter++   P2: counter--   (shared) => wrong value', color='green'))
beat(p, '''The part of the code where a process uses shared data is called the critical section.
Each process follows this structure. Entry section, then critical section, then exit section, then remainder section.''',
     T(3, '[r:Critical section] = code that uses shared data'),
     Box(1300, 380, 420, 64, 'entry section', size=28), Box(1300, 444, 420, 74, 'CRITICAL SECTION', color='red', size=30),
     Box(1300, 518, 420, 64, 'exit section', size=28), Box(1300, 582, 420, 64, 'remainder section', size=28))
beat(p, '''Any solution to the critical section problem must satisfy three requirements. Remember them.
Mutual exclusion: only one process inside the critical section at a time.
Progress: if nobody is inside, the decision of who enters next cannot be postponed forever.
And bounded waiting: there is a limit on how many times others can enter before you.''',
     S(5, '3 requirements', color='black'), Stamp(700, 480),
     N(6, 1, '[r:Mutual exclusion] - only one inside at a time'), N(7, 2, '[r:Progress] - no indefinite postponement'),
     N(8, 3, '[r:Bounded waiting] - limit on others entering first'))

p = page("Peterson's Solution", 4)
beat(p, '''Peterson's solution works for two processes. It uses two shared variables.
A flag array, where flag of i is true means process i wants to enter. And turn, which says whose turn it is.''',
     T(0, 'For [k:2 processes]. Shared: [r:flag[2]] (I want to enter), [r:turn] (whose turn)'))
beat(p, '''Process i sets its flag to true, and politely gives the turn to the other process, j.
Then it waits while the other process wants to enter and it is the other's turn.
After the critical section, it sets its flag back to false.''',
     Box(240, 300, 900, 420, None, color='blue'),
     T(0, 'do {', x=280, y=360, color='black'), T(0, 'flag[i] = true;', x=340, y=410, color='black'),
     T(0, 'turn = j;', x=340, y=460, color='black'), T(0, 'while (flag[j] && turn == j);', x=340, y=510, color='black'),
     T(0, '[r:// critical section]', x=340, y=570), T(0, 'flag[i] = false;', x=340, y=630, color='black'),
     T(0, '[g:// remainder section]', x=340, y=680), T(0, '} while (true);', x=280, y=710, color='black'))
beat(p, '''Peterson's solution satisfies all three requirements: mutual exclusion, progress, and bounded waiting.''',
     T(0, 'Satisfies all 3:', x=1200, y=420, color='black'), T(0, '[g:Mutual exclusion]', x=1200, y=480), T(0, '[g:Progress]', x=1200, y=540),
     T(0, '[g:Bounded waiting]', x=1200, y=600), Stamp(1300, 700, 'IMP!'))

p = page('Semaphores', 4)
beat(p, '''A semaphore is an integer variable, S, that can be changed only by two atomic operations.
Wait, also called P. And signal, also called V.''',
     T(0, '[h:Semaphore] S = integer, changed only by 2 atomic operations'))
beat(p, '''Wait checks if S is less than or equal to zero, and waits. Otherwise it decreases S by one.
Signal simply increases S by one.''',
     Box(240, 300, 760, 260, None, color='blue'),
     T(0, 'wait(S)  [k:/ P(S)]:', x=280, y=360, color='red'), T(0, 'while (S <= 0);  // wait', x=330, y=410, color='black'),
     T(0, 'S--;', x=330, y=455, color='black'), T(0, 'signal(S)  [k:/ V(S)]:  S++;', x=280, y=525, color='red'))
beat(p, '''There are two types. A binary semaphore takes only zero or one, and works like a mutex lock.
A counting semaphore can take any value, and is used when there are many copies of a resource.''',
     T(0, '[r:Binary semaphore] - 0 or 1 (like mutex lock)', x=1080, y=360), T(0, '[r:Counting semaphore] - any value', x=1080, y=420),
     T(0, '(many instances of a resource)', x=1110, y=470, color='green'))
beat(p, '''One problem. This version keeps looping while waiting. That is called busy waiting, or a spinlock.
And if semaphores are used in the wrong order, they can cause deadlock and starvation.''',
     T(10, 'Busy waiting = [r:spinlock] (wastes CPU)'), T(11, 'Wrong order of wait() => [r:deadlock / starvation]'))

p = page('Classical Synchronization Problems', 4)
beat(p, '''First, the producer consumer problem, also called the bounded buffer problem. The producer puts items in a buffer of size n,
the consumer takes them out. We use three semaphores. Mutex starts at one. Empty starts at n. Full starts at zero.''',
     S(0, '1) Producer-Consumer (bounded buffer)', color='red', size=38), T(1, 'mutex = 1,   empty = n,   full = 0', color='black'))
beat(p, '''The producer does: wait empty, wait mutex, add the item, signal mutex, signal full.
The consumer does the opposite: wait full, wait mutex, remove the item, signal mutex, signal empty.''',
     T(2, '[k:Producer]: wait(empty); wait(mutex); add; signal(mutex); signal(full);'),
     T(3, '[k:Consumer]: wait(full); wait(mutex); remove; signal(mutex); signal(empty);'))
beat(p, '''Second, readers writers. Many readers can read at the same time, but a writer needs the data alone.''',
     S(5, '2) Readers-Writers', color='red', size=38), T(6, 'many readers together OK; writer needs [h:exclusive] access'))
beat(p, '''Third, dining philosophers. Five philosophers sit at a round table with five chopsticks. Each needs two chopsticks to eat.
If all of them pick up their left chopstick at once, nobody can eat. That's a deadlock.
Fixes: allow only four at the table, pick both chopsticks together, or odd ones pick left first and even ones pick right first.''',
     S(8, '3) Dining Philosophers', color='red', size=38), T(9, '5 philosophers, 5 chopsticks, need 2 to eat'),
     T(10, 'all pick left => [r:deadlock]'), T(11, 'Fix: max 4 sit / pick both / odd-even order', color='green'),
     Ell(1420, 600, 280, 280, None, color='black'),
     *[Ell(1560 + int(200 * __import__('math').cos(a)) - 40, 740 + int(200 * __import__('math').sin(a)) - 40, 80, 80, f'P{k}', size=24, color='blue')
       for k, a in enumerate([-1.571 + 1.2566 * j for j in range(5)])])
beat(p, '''A monitor is a higher level tool. Only one process can be active inside a monitor at a time,
and it uses condition variables with wait and signal.''',
     T(13, '[k:Monitor]: high-level; one process inside at a time; condition variables'))

# ===================================================================================== CH 5
p = chapter(5)
beat(p, "Chapter five. Deadlocks. Banker's algorithm is one of the most asked numericals in the whole subject.")

p = page('Deadlock', 5)
beat(p, '''A deadlock is when a set of processes are all waiting for resources held by each other,
so none of them can ever continue. Like two cars facing each other on a one lane bridge.''',
     T(0, '[h:Deadlock] = processes wait for each other\'s resources forever'),
     T(1, 'e.g. two cars on a one-lane bridge', color='green'))
beat(p, '''A deadlock can happen only if all four of these conditions hold at the same time.
Mutual exclusion: a resource can be used by only one process. Hold and wait: a process holds one resource and waits for another.
No preemption: a resource cannot be taken away by force. And circular wait: P1 waits for P2, P2 waits for P1, in a circle.''',
     S(3, '4 necessary conditions (all must hold)', color='black'), Stamp(1500, 360),
     N(4, 1, '[r:Mutual exclusion]'), N(5, 2, '[r:Hold and wait]'), N(6, 3, '[r:No preemption]'), N(7, 4, '[r:Circular wait]'),
     T(8, 'Trick: [h:M - H - N - C]', color='green'))
beat(p, '''We show this with a resource allocation graph. Circles are processes, boxes are resources.
An arrow from a process to a resource is a request. An arrow from a resource to a process means it is allocated.
Here P1 holds R2 and wants R1, while P2 holds R1 and wants R2. There's a cycle, so there's a deadlock.''',
     Ell(1180, 560, 130, 130, 'P1', size=34, color='blue'), Ell(1600, 560, 130, 130, 'P2', size=34, color='blue'),
     Box(1400, 420, 100, 90, 'R1', size=32, color='red'), Box(1400, 780, 100, 90, 'R2', size=32, color='red'),
     Arr(1300, 580, 1400, 480, label='request', lx=-80, ly=-10, size=24), Arr(1500, 480, 1610, 580, label='held', lx=60, ly=-10, size=24),
     Arr(1610, 670, 1500, 800, label='request', lx=80, ly=10, size=24), Arr(1400, 800, 1300, 670, label='held', lx=-60, ly=10, size=24),
     T(10, 'RAG: single instance => [r:cycle = deadlock]'), T(11, 'multiple instances => cycle = [k:maybe] deadlock'))

p = page('Handling Deadlocks', 5)
beat(p, '''There are four ways to handle deadlocks. First, prevention. Make sure at least one of the four conditions can never hold.
For example, ask for all resources at once, so there's no hold and wait. Or number the resources and request them in order,
so there's no circular wait.''',
     N(0, 1, '[r:Prevention] - break one of the 4 conditions'), T(1, 'all resources at once => no hold & wait', x=230, color='green'),
     T(2, 'request in fixed order => no circular wait', x=230, color='green'))
beat(p, '''Second, avoidance. Before giving a resource, check if the system will still be in a safe state.
If not, make the process wait. Banker's algorithm does this.''',
     N(4, 2, "[r:Avoidance] - grant only if system stays in [h:safe state]"), T(5, "=> Banker's algorithm", x=230, color='green'))
beat(p, '''Third, detection and recovery. Let deadlocks happen, detect them using a wait for graph, and then recover,
by killing a process or taking resources away.''',
     N(7, 3, '[r:Detection & recovery] - wait-for graph; kill process /'), T(8, 'preempt resources', x=230))
beat(p, '''Fourth, just ignore it. This is called the ostrich approach, and most systems like Windows and Linux actually do this,
because deadlocks are rare and prevention is costly.''',
     N(10, 4, '[r:Ignore] (ostrich approach) - Windows, Linux'))

p = page("Banker's Algorithm - Example", 5)
need_rows = [[f'P{i}', ' '.join(map(str, ALLOC[i])), ' '.join(map(str, MAX[i])), ' '.join(map(str, NEED[i]))] for i in range(5)]
beat(p, '''Now the famous Banker's algorithm example. Five processes, P0 to P4, and three resource types, A, B, and C.
Here is the allocation, what each process currently holds. And max, the most each process may ever need.''',
     Tab(180, 200, [120, 230, 230], 54, [['', 'Alloc A B C', 'Max A B C']] + [r[:3] for r in need_rows], size=30),
     T(0, 'Available = [h:3 3 2]', x=1200, y=260, color='black', size=40))
beat(p, '''Step one. Find the need matrix. Need equals max minus allocation. For P0, seven five three minus zero one zero,
is seven four three. Do the same for every process.''',
     T(0, '[r:Need = Max - Allocation]', x=1200, y=340, size=38),
     Tab(760, 200, [230], 54, [['Need A B C']] + [[r[3]] for r in need_rows], size=30, colors={(i, 0): 'red' for i in range(1, 6)}))
seq, steps = bankers()
beat(p, '''Step two. Start with work equal to available, three three two. Find a process whose need is less than or equal to work.
When it finishes, it releases its allocation, so add its allocation to work. Repeat.''',
     T(0, 'Work = Available', x=1200, y=430, color='black'), T(0, 'if Need <= Work:', x=1200, y=480, color='black'),
     T(0, 'Work = Work + Alloc', x=1240, y=530, color='black'))

p = page("Banker's Algorithm - Safe Sequence", 5)
lines = []
for i, need, before, after in steps:
    lines.append(f'P{i}: Need ({" ".join(map(str, need))}) <= Work ({" ".join(map(str, before))})  =>  Work = [g:{" ".join(map(str, after))}]')
say_steps = ['P1 needs one two two, which is less than three three two. So P1 runs. Work becomes five three two.',
             'P2 needs six zero zero. That is more than five three two, so skip it. P3 needs zero one one. Yes. Work becomes seven four three.',
             'P4 needs four three one. Yes. Work becomes seven four five.',
             'Back to P0. It needs seven four three. Yes. Work becomes seven five five.',
             'Finally P2, six zero zero. Yes. Work becomes ten five seven.']
for k in range(5): beat(p, say_steps[k], T(k * 1 + 0, lines[k], size=36))
beat(p, f'''All processes can finish, so the system is in a safe state. The safe sequence is
P1, P3, P4, P0, P2. Remember, there can be more than one safe sequence, and any correct one gets full marks.''',
     T(7, 'Safe sequence:  [h:< ' + ', '.join(f'P{i}' for i in seq) + ' >]', size=46, color='red'),
     T(9, 'All can finish => [g:SAFE state]  (more than one safe sequence possible)', color='black'), Stamp(1500, 560, 'MOST ASKED'))

# ===================================================================================== CH 6
p = chapter(6)
beat(p, 'Chapter six. Memory management. Paging and TLB questions come here.')

p = page('Logical vs Physical Address', 6)
beat(p, '''The CPU generates a logical address, also called a virtual address. The actual location in RAM is the physical address.
A hardware unit called the M M U, the memory management unit, converts logical to physical.''',
     T(0, '[r:Logical address] - generated by CPU (virtual)'), T(1, '[r:Physical address] - actual location in RAM'),
     T(2, '[h:MMU] (Memory Management Unit) converts logical -> physical'))
beat(p, '''A simple example with a relocation register. If the relocation register holds fourteen thousand,
and the logical address is three four six, the physical address is fourteen thousand three hundred forty six.''',
     Box(240, 520, 200, 90, 'CPU', size=34), Ell(640, 515, 140, 100, '+', size=48, color='red'),
     Box(620, 380, 180, 70, '14000', size=30, color='red'), T(0, 'relocation register', x=580, y=360, size=26, color='green'),
     Box(1000, 520, 240, 90, 'Memory', size=34),
     Arr(440, 565, 640, 565, label='346', ly=-14), Arr(710, 450, 710, 515), Arr(780, 565, 1000, 565, label='14346', ly=-14),
     T(0, 'logical 346 + 14000 = physical [h:14346]', x=240, y=720, color='black'))
beat(p, '''Swapping means moving a whole process out of memory to the disk, and back in later.''',
     T(13, '[k:Swapping]: move a process memory <-> disk'))

p = page('Contiguous Allocation: First / Best / Worst Fit', 6)
beat(p, '''In contiguous allocation, each process gets one continuous block of memory. When a process arrives,
we choose a free hole using one of three strategies. First fit: the first hole that is big enough.
Best fit: the smallest hole that is big enough. Worst fit: the largest hole.''',
     N(0, 1, '[r:First fit] - first hole big enough'), N(1, 2, '[r:Best fit] - smallest hole big enough'),
     N(2, 3, '[r:Worst fit] - largest hole'))
pf = {k: place(k) for k in ('first', 'best', 'worst')}
def cell(r): return '-' if r[1] is None else f'{PARTS[r[1]]}'
beat(p, '''Classic example. Memory partitions of one hundred, five hundred, two hundred, three hundred, and six hundred K B.
Processes of two hundred twelve, four hundred seventeen, one hundred twelve, and four hundred twenty six K B arrive in order.''',
     T(4, 'Partitions: 100, 500, 200, 300, 600 KB', color='black'), T(5, 'Processes: 212, 417, 112, 426 KB', color='black'))
rows = [['Process', 'First fit', 'Best fit', 'Worst fit']]
for k, j in enumerate(JOBS):
    def c(kind):
        r = pf[kind][k]
        if r[1] is None: return 'waits'
        return f'{r[2]} block' if r[2] != PARTS[r[1]] else f'{PARTS[r[1]]}'
    rows.append([f'{j} KB', c('first'), c('best'), c('worst')])
beat(p, '''With first fit, two twelve goes into five hundred. Four seventeen goes into six hundred. One twelve goes into the
leftover two eighty eight of the five hundred block. And four twenty six has to wait. With best fit, all four fit perfectly.
With worst fit, four twenty six waits again. So in this example, best fit is the winner.''',
     Tab(180, 560, [220, 250, 250, 250], 54, rows, size=30, colors={(4, 1): 'red', (4, 3): 'red', (4, 2): 'green'}),
     T(0, 'Here [h:best fit] wins', x=1240, y=760, color='green', size=40))

p = page('Fragmentation', 6)
beat(p, '''Fragmentation means wasted memory. Internal fragmentation is waste inside an allocated block. For example,
a process needs eighteen K B but gets a twenty K B block. Two K B is wasted inside.''',
     T(0, '[r:Internal fragmentation] - waste [h:inside] an allocated block'), T(1, 'needs 18 KB, gets 20 KB => 2 KB wasted inside', x=230, color='green'),
     Box(1300, 250, 420, 150, None), HL(1300, 330, 420, 70, 'pink'), T(0, 'used 18 KB', x=1420, y=300, size=30, color='black'),
     T(0, 'wasted 2 KB', x=1410, y=375, size=30, color='red'))
beat(p, '''External fragmentation is when the total free memory is enough, but it is not continuous, so a process still cannot fit.
The fix is compaction, which moves processes together. Or use paging.''',
     T(3, '[r:External fragmentation] - enough total free memory,'), T(4, 'but [h:not contiguous]', x=230),
     T(5, 'Fix: [g:compaction] or [g:paging]', x=230))
beat(p, '''Quick rule: fixed partitions and paging cause internal fragmentation. Variable partitions and segmentation cause external fragmentation.''',
     Tab(180, 560, [440, 380], 54, [['Causes internal', 'Causes external'], ['fixed partitions', 'variable partitions'], ['paging', 'segmentation']], size=30),
     Stamp(1300, 620))

p = page('Paging', 6)
beat(p, '''Paging solves external fragmentation. Physical memory is divided into fixed size blocks called frames.
Logical memory is divided into blocks of the same size called pages.''',
     T(0, 'Physical memory -> [r:frames]   Logical memory -> [r:pages]  (same size)'))
beat(p, '''The logical address is split into a page number p and an offset d. The page number is looked up in the page table,
which gives the frame number f. The physical address is f joined with d.''',
     Box(200, 330, 230, 80, 'p  |  d', size=34, color='blue'), T(0, 'logical', x=250, y=310, size=26, color='green'),
     Box(620, 280, 220, 300, None), T(0, 'page table', x=640, y=260, size=26, color='green'),
     Box(620, 400, 220, 60, 'f', size=30, color='red'),
     Box(1050, 330, 230, 80, 'f  |  d', size=34, color='red'), T(0, 'physical', x=1100, y=310, size=26, color='green'),
     Arr(300, 410, 620, 430, label='p', ly=30), Arr(840, 430, 1050, 380), Arr(400, 330, 1100, 330, curve=-60, label='d', ly=-12))
beat(p, '''If the page size is four K B, which is two to the power twelve, then the offset needs twelve bits.
Paging has no external fragmentation, but a little internal fragmentation in the last page.''',
     T(9, 'page size 4 KB = 2^12  =>  offset d = [h:12 bits]', color='black'),
     T(10, '[g:No external fragmentation], small internal (last page)'), Stamp(1450, 760))

p = page('TLB & Effective Access Time', 6)
beat(p, '''The page table is in memory, so every access needs two memory reads. To speed this up, we use a T L B,
the translation lookaside buffer. It is a small, fast cache of page table entries.''',
     T(0, '[h:TLB] = Translation Lookaside Buffer = fast cache of page table'),
     T(1, '[g:TLB hit]: frame found fast    [r:TLB miss]: go to page table in memory'))
beat(p, '''Effective access time. E A T equals hit ratio times T L B time plus memory time, plus one minus hit ratio,
times T L B time plus two memory times. Because on a miss, we access memory twice.''',
     T(3, '[h:EAT = h(t + m) + (1 - h)(t + 2m)]', size=44, color='red'), T(4, 'h = hit ratio, t = TLB time, m = memory time', size=32, color='black'))
beat(p, '''Example. T L B takes twenty nanoseconds, memory takes one hundred, and the hit ratio is eighty percent.
E A T equals point eight times one twenty, plus point two times two twenty. That is ninety six plus forty four,
which is one hundred forty nanoseconds.''',
     T(6, 'Ex: t = 20 ns, m = 100 ns, h = 0.8', color='black'), T(7, 'EAT = 0.8 x 120 + 0.2 x 220'),
     T(8, '= 96 + 44 = [h:140 ns]', size=44), Stamp(1400, 600, 'NUMERICAL'))

p = page('Segmentation', 6)
beat(p, '''Segmentation divides memory the way the user sees a program. Main function, other functions, stack, arrays.
Each segment can have a different size.''',
     T(0, 'Memory divided by [h:logical units]: main(), functions, stack, arrays'), T(1, 'segments have [r:variable size]'))
beat(p, '''The logical address is a segment number and an offset. The segment table stores a base and a limit for each segment.
If the offset is less than the limit, physical address equals base plus offset. Otherwise it is an error, a trap.''',
     T(2, 'address = (segment no. s, offset d)'), T(3, 'segment table: [k:base] & [k:limit]'),
     T(4, 'if d < limit: physical = [h:base + d]   else => [r:trap (error)]'))
beat(p, '''Paging versus segmentation. Paging uses fixed size pages and has internal fragmentation. It is invisible to the user.
Segmentation uses variable sizes, has external fragmentation, and matches the user's view.''',
     Tab(180, 560, [360, 360, 400], 54, [['', 'Paging', 'Segmentation'], ['size', 'fixed', 'variable'],
         ['fragmentation', 'internal', 'external'], ['user view', 'no', 'yes (logical units)']], size=30), Stamp(1500, 660))

# ===================================================================================== CH 7
p = chapter(7)
beat(p, 'Chapter seven. Virtual memory. Page replacement numericals are asked every single year.')

p = page('Virtual Memory & Demand Paging', 7)
beat(p, '''Virtual memory lets us run programs that are bigger than the RAM. Only the pages that are needed are loaded into memory.
This is called demand paging. A valid invalid bit in the page table tells if a page is in memory.''',
     T(0, '[h:Virtual memory] - run programs bigger than RAM'), T(1, '[r:Demand paging] - load a page only when needed'),
     T(2, 'valid / invalid bit tells if the page is in memory'))
beat(p, '''If a process uses a page that is not in memory, a page fault happens. The steps are.
One, the reference hits an invalid bit, and a trap goes to the OS. Two, the OS finds a free frame.
Three, it reads the page from the disk. Four, it updates the page table. Five, the instruction is restarted.''',
     S(4, 'Page fault - steps', color='black'), N(5, 1, 'reference -> invalid -> [r:trap] to OS'), N(6, 2, 'find a free frame'),
     N(7, 3, 'read the page from disk'), N(8, 4, 'update the page table'), N(9, 5, 'restart the instruction'), Stamp(1400, 520))
beat(p, '''If there is no free frame, we must remove a page. That is page replacement. Let's solve the classic example.''',
     T(11, 'No free frame? => [h:page replacement]', color='green'))

def pr_page(kind, title, say1, say2, say3):
    hist, faults = replace(REF, 3, kind)
    p = page(title, 7)
    rows = [['ref'] + [str(x) for x in REF]] + [[f'F{k + 1}'] + [('' if h[k] is None else str(h[k])) for h in hist] for k in range(3)]
    rows.append([''] + ['F' if f else 'H' for f in faults])
    colors = {(4, c + 1): ('red' if f else 'green') for c, f in enumerate(faults)}
    for c in range(len(REF)):
        if faults[c]:
            for k in range(3):
                if hist[c][k] == REF[c]: colors[(k + 1, c + 1)] = 'red'
    beat(p, say1, T(0, 'Reference string (3 frames):', color='black'), T(1, ', '.join(map(str, REF)), color='blue'))
    beat(p, say2, Tab(180, 330, [100] + [80] * 20, 54, rows, size=28, order='col', colors=colors))
    beat(p, say3, T(0, f'Page faults = [h:{sum(faults)}]   Hits = {len(REF) - sum(faults)}', x=180, y=680, size=46, color='red'),
         T(0, 'F = fault,  H = hit', x=1300, y=680, size=30, color='black'))
    return p, sum(faults)

pr_page('fifo', 'Page Replacement - FIFO',
    '''FIFO. First in, first out. When we need space, we remove the page that came in earliest. Here's the reference string with three frames.''',
    '''Seven, zero, one fill the empty frames. Three faults. Two comes, and seven is the oldest, so seven goes out. Zero is already there, that's a hit.
Three replaces zero, the oldest now. And we continue the same way, always removing the oldest page.''',
    '''Count them. FIFO gives fifteen page faults and five hits.''')
pr_page('opt', 'Page Replacement - Optimal',
    '''Optimal. Remove the page that will not be used for the longest time in the future. It gives the fewest faults,
but it cannot be built in real life, because we cannot see the future. It is used to compare other algorithms.''',
    '''At two, look ahead. Zero is used next, then one is used much later, and seven is used last of all. So replace seven.
Keep doing this, always looking into the future.''',
    '''Optimal gives only nine page faults. That's the minimum possible.''')
pr_page('lru', 'Page Replacement - LRU',
    '''L R U. Least recently used. Remove the page that has not been used for the longest time in the past.
It is like optimal, but looking backwards. This is the one used in practice.''',
    '''At two, seven was used longest ago, so seven goes. At three, look back. One was used longest ago, so one is replaced.
Continue the same way.''',
    '''LRU gives twelve page faults. So the order is: optimal nine, LRU twelve, FIFO fifteen.''')

p = page("Belady's Anomaly & Thrashing", 7)
b3 = sum(replace([1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5], 3, 'fifo')[1]); b4 = sum(replace([1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5], 4, 'fifo')[1])
beat(p, f'''Belady's anomaly. Normally, more frames means fewer page faults. But with FIFO, sometimes more frames give more faults.
For the string one two three four one two five one two three four five, three frames give {b3} faults, but four frames give {b4}.
L R U and optimal never have this problem.''',
     T(0, "[h:Belady's anomaly]: more frames => [r:more] faults (FIFO only)"), T(1, '1,2,3,4,1,2,5,1,2,3,4,5', color='black'),
     T(2, f'3 frames = [r:{b3}] faults,   4 frames = [r:{b4}] faults'), T(3, 'LRU & Optimal never suffer (stack algorithms)', color='green'),
     Stamp(1500, 320))
beat(p, '''Thrashing. When there are too many processes and too few frames, the system spends all its time swapping pages
in and out, instead of doing real work. CPU utilization suddenly drops.''',
     T(5, '[h:Thrashing] = too busy swapping pages, no real work'), T(6, 'CPU utilisation drops suddenly', color='red'),
     Ln([(1180, 990), (1180, 640)], 'black', 4), Ln([(1180, 990), (1800, 990)], 'black', 4),
     Ln([(1190, 960), (1300, 860), (1420, 760), (1520, 720), (1580, 730), (1640, 820), (1720, 960)], 'red', 5),
     T(0, 'CPU use', x=1060, y=630, size=26, color='black'), T(0, 'degree of multiprogramming', x=1300, y=1035, size=26, color='black'),
     T(0, 'thrashing', x=1650, y=820, size=28, color='red'))
beat(p, '''To fix it, use the working set model, control the page fault frequency, or reduce the degree of multiprogramming.''',
     T(8, 'Fix: [g:working set model], [g:page-fault frequency],'), T(9, 'reduce degree of multiprogramming', x=100 + 130, color='green'))

# ===================================================================================== CH 8
p = chapter(8)
beat(p, 'Chapter eight. File systems.')

p = page('Files & Access Methods', 8)
beat(p, '''A file is a named collection of related data, stored on secondary storage. Every file has attributes like name, type,
size, location, protection, and time. And operations like create, open, read, write, seek, and delete.''',
     T(0, '[h:File] = named collection of related data on disk'), T(1, 'Attributes: name, type, size, location, protection, time'),
     T(2, 'Operations: create, open, read, write, seek, delete, truncate'))
beat(p, '''Three access methods. Sequential access reads records one after another, like a tape.
Direct, or random access, can jump to any block directly. And indexed access first looks up an index, then goes to the block.''',
     S(4, 'Access methods', color='black'), N(5, 1, '[r:Sequential] - one after another (like a tape)'),
     N(6, 2, '[r:Direct / random] - jump to any block n'), N(7, 3, '[r:Indexed] - index first, then the block'))

p = page('Directory Structures', 8)
beat(p, '''Directory structures. Single level: all files in one directory, so names can clash.
Two level: a separate directory for each user.''',
     N(0, 1, '[r:Single-level] - all files in one directory (name clash)'), N(1, 2, '[r:Two-level] - separate directory per user'))
beat(p, '''Tree structured: directories inside directories, like folders on your computer. This is the most common.
Acyclic graph: like a tree, but a file can be shared through links. And general graph allows cycles, which need extra care.''',
     N(2, 3, '[r:Tree-structured] - folders in folders ([h:most common])'), N(3, 4, '[r:Acyclic graph] - sharing via links'),
     N(4, 5, '[r:General graph] - cycles allowed (needs garbage collection)'),
     Box(1000, 620, 160, 70, 'root', size=28), Box(760, 760, 160, 70, 'home', size=28), Box(1240, 760, 160, 70, 'bin', size=28),
     Box(640, 900, 160, 70, 'a.txt', size=26, color='blue'), Box(880, 900, 160, 70, 'b.c', size=26, color='blue'),
     Arr(1040, 690, 860, 760), Arr(1120, 690, 1300, 760), Arr(820, 830, 730, 900), Arr(860, 830, 950, 900))

p = page('File Allocation Methods', 8)
beat(p, '''How are file blocks placed on the disk? Three methods, very important. First, contiguous allocation.
The file uses blocks next to each other. Reading is fast, and direct access is easy.
But it causes external fragmentation, and the file is hard to grow.''',
     Stamp(1600, 140), S(0, '1) Contiguous', color='red', size=38), T(1, 'blocks next to each other. [g:fast, direct access]'),
     T(2, '[r:external fragmentation, hard to grow]'),
     *[Box(1150 + 80 * k, 250, 80, 70, str(k + 4), size=26, color='blue') for k in range(5)])
beat(p, '''Second, linked allocation. Each block holds a pointer to the next block. No external fragmentation,
and the file can grow easily. But random access is slow, and pointers use space. The FAT system is a version of this.''',
     S(4, '2) Linked', color='red', size=38), T(5, 'each block points to the next. [g:no ext. fragmentation]'),
     T(6, '[r:slow random access, pointer overhead]   (FAT = variant)'),
     Box(1150, 470, 90, 70, '9', size=26, color='blue'), Box(1330, 470, 90, 70, '16', size=26, color='blue'),
     Box(1510, 470, 90, 70, '1', size=26, color='blue'), Box(1690, 470, 90, 70, '25', size=26, color='blue'),
     Arr(1240, 505, 1330, 505), Arr(1420, 505, 1510, 505), Arr(1600, 505, 1690, 505))
beat(p, '''Third, indexed allocation. One index block keeps all the pointers to the file's blocks.
It supports direct access and has no external fragmentation, but the index block is extra overhead.''',
     S(8, '3) Indexed', color='red', size=38), T(9, 'index block keeps all pointers. [g:direct access]'),
     T(10, '[r:index block overhead]'),
     Box(1150, 760, 150, 160, '19\n9\n16\n1', size=26, color='red'), T(0, 'index', x=1180, y=950, size=26, color='green'),
     Box(1420, 700, 90, 60, '9', size=24, color='blue'), Box(1420, 790, 90, 60, '16', size=24, color='blue'), Box(1420, 880, 90, 60, '1', size=24, color='blue'),
     Arr(1300, 790, 1420, 730), Arr(1300, 830, 1420, 820), Arr(1300, 870, 1420, 905))

p = page('Free Space Management', 8)
beat(p, '''The OS must also track which disk blocks are free. First, the bit vector, or bitmap. One bit per block.
Zero means free, one means allocated, or the opposite, depending on the book. It is simple and fast.''',
     N(0, 1, '[r:Bit vector / bitmap] - 1 bit per block'), T(1, 'e.g. 0 0 1 1 1 1 0 0 1 1 ...  (simple, fast)', x=230, color='black'))
beat(p, '''Second, a linked list, where each free block points to the next free block. Third, grouping,
where one free block stores addresses of many free blocks. And fourth, counting, which stores the first free block,
and how many free blocks follow it.''',
     N(3, 2, '[r:Linked list] - free blocks point to next free block'), N(4, 3, '[r:Grouping] - one block stores many free addresses'),
     N(5, 4, '[r:Counting] - (first free block, count)'))

# ===================================================================================== CH 9
p = chapter(9)
beat(p, 'Chapter nine. Disk scheduling. Another sure shot numerical.')

p = page('Disk Structure & Access Time', 9)
beat(p, '''A hard disk has platters. Each platter has circular tracks, and each track is divided into sectors.
The same track on all platters forms a cylinder. The read write head moves across tracks.''',
     T(0, 'platter -> [r:tracks] -> [r:sectors];  same track on all = [r:cylinder]'),
     Ell(1300, 380, 420, 420, None, color='black'), Ell(1380, 460, 260, 260, None, color='blue'), Ell(1460, 540, 100, 100, None, color='black'),
     Ln([(1510, 380), (1510, 540)], 'red', 3), T(0, 'track', x=1720, y=470, size=28, color='blue'), T(0, 'sector', x=1540, y=450, size=28, color='red'))
beat(p, '''Disk access time equals seek time, plus rotational latency, plus transfer time. Seek time is the time to move the head
to the right track. It's the biggest part, so disk scheduling tries to reduce head movement.''',
     T(2, '[h:Access time = Seek + Rotational latency + Transfer]', color='red', size=40),
     T(3, 'Seek time = move head to the track ([r:biggest part])'),
     T(4, 'Disk scheduling goal: [g:minimise head movement]'))

def head_plot(path, x0, y0, w, h, color='red'):
    els = [Ln([(x0, y0), (x0 + w, y0)], 'black', 3)]
    for c in (0, 50, 100, 150, 199):
        els.append(T(0, str(c), x=x0 + int(w * c / 199) - 14, y=y0 - 14, size=22, color='black'))
    pts = [(x0 + int(w * c / 199), y0 + 30 + int(k * (h - 40) / (len(path) - 1))) for k, c in enumerate(path)]
    els.append(Ln(pts, color, 4))
    return els

p = page('Disk Scheduling: FCFS & SSTF', 9)
beat(p, f'''Classic example. The disk has cylinders zero to one ninety nine. The request queue is ninety eight, one eighty three,
thirty seven, one twenty two, fourteen, one twenty four, sixty five, sixty seven. And the head starts at fifty three.''',
     T(0, 'Queue: ' + ', '.join(map(str, QUEUE)), color='black'), T(1, 'Head = 53,   cylinders 0 - 199', color='black'))
pf_ = d_fcfs(); ps_ = d_sstf()
beat(p, f'''FCFS. Just go in the given order. Fifty three to ninety eight, to one eighty three, and so on.
Add up all the jumps. The total head movement is {total(pf_)} cylinders.''',
     S(3, 'FCFS', color='red', size=38), T(4, ' -> '.join(map(str, pf_)), size=30),
     T(5, f'Total head movement = [h:{total(pf_)}]', color='black'))
beat(p, f'''S S T F. Shortest seek time first. Always go to the nearest request. From fifty three, the nearest is sixty five,
then sixty seven, then thirty seven, fourteen, ninety eight, one twenty two, one twenty four, and one eighty three.
Total head movement is only {total(ps_)}. But requests far away may starve.''',
     S(7, 'SSTF (nearest first)', color='red', size=38), T(8, ' -> '.join(map(str, ps_)), size=30),
     T(9, f'Total head movement = [h:{total(ps_)}]   ([r:may starve far requests])', color='black'),
     *head_plot(ps_, 1150, 600, 680, 400))

p = page('SCAN, C-SCAN, LOOK, C-LOOK', 9)
sc, lk, cs, cl = d_scan_down(), d_look_down(), d_cscan_up(), d_clook_up()
beat(p, f'''SCAN, also called the elevator algorithm. The head moves in one direction to the end of the disk, serving requests,
then turns back. Moving towards zero first: fifty three, thirty seven, fourteen, zero, then sixty five up to one eighty three.
Total is {total(sc)}.''',
     S(0, 'SCAN (elevator), towards 0', color='red', size=36), T(1, ' -> '.join(map(str, sc)), size=30),
     T(2, f'Total = [h:{total(sc)}]', color='black'))
beat(p, f'''LOOK is the same, but the head only goes as far as the last request, not to the end. So it turns at fourteen.
Total is {total(lk)}.''',
     S(4, 'LOOK (turn at last request)', color='red', size=36), T(5, ' -> '.join(map(str, lk)), size=30),
     T(6, f'Total = [h:{total(lk)}]', color='black'))
beat(p, f'''C SCAN, or circular SCAN, moves in only one direction. Going up: sixty five to one eighty three, to the end, one ninety nine.
Then it jumps back to zero and continues up to fourteen and thirty seven. Counting the return jump, the total is {total(cs)}.
C LOOK does the same but turns at the last request: total {total(cl)}. Some books do not count the return jump, so follow your textbook.''',
     S(8, 'C-SCAN (one direction, jump back), going up', color='red', size=36), T(9, ' -> '.join(map(str, cs)), size=28),
     T(10, f'Total = [h:{total(cs)}] (with return jump)', color='black'),
     S(12, 'C-LOOK', color='red', size=36), T(13, ' -> '.join(map(str, cl)) + f'   Total = [h:{total(cl)}]', size=28))

p = page('RAID Levels', 9)
beat(p, '''Finally, RAID. Redundant array of independent disks. Many disks used together for speed or safety.
RAID zero is striping. Data is split across disks. Very fast, but no safety. If one disk fails, data is lost.''',
     T(0, '[h:RAID] = Redundant Array of Independent Disks'), N(1, 0, '[r:Striping] - fast, [r:no redundancy]'))
beat(p, '''RAID one is mirroring. The same data is copied on two disks. Very safe, but you lose half the space.
RAID five is striping with distributed parity. It balances speed and safety, and survives one disk failure.''',
     N(2, 1, '[r:Mirroring] - copy on 2 disks, safe, 50% space'), N(3, 5, '[r:Striping + distributed parity] - survives 1 disk failure'),
     T(5, 'Others: RAID 6 (double parity), RAID 10 (mirror + stripe)', color='green'))

# ===================================================================================== CH 10
p = chapter(10)
beat(p, "Chapter ten. Exam revision. If you're short on time, revise these first.")

p = page('Most Asked Exam Questions', 10)
qs = ['Process state diagram + PCB', 'Scheduling numericals: FCFS, SJF, RR (Gantt chart)', 'Critical section: 3 requirements, Peterson, semaphores',
      'Producer-consumer / dining philosophers', "Deadlock: 4 conditions + Banker's algorithm", 'Paging, TLB & effective access time',
      "Page replacement: FIFO, Optimal, LRU + Belady's anomaly", 'Thrashing', 'File allocation methods', 'Disk scheduling numericals']
beat(p, '''Here are the most asked questions across universities. One, the process state diagram and P C B.
Two, scheduling numericals with Gantt charts. Three, the critical section requirements, Peterson's solution, and semaphores.''',
     *[T(k, f'{k + 1}. {q}', x=200) for k, q in enumerate(qs[:3])])
beat(p, '''Four, producer consumer and dining philosophers. Five, deadlock conditions and Banker's algorithm.
Six, paging, T L B, and effective access time.''', *[T(k, f'{k + 1}. {q}', x=200) for k, q in enumerate(qs[:6]) if k >= 3])
beat(p, '''Seven, page replacement with FIFO, optimal and LRU, plus Belady's anomaly. Eight, thrashing.
Nine, file allocation methods. And ten, disk scheduling numericals.''', *[T(k, f'{k + 1}. {q}', x=200) for k, q in enumerate(qs) if k >= 6])
beat(p, '''Exam tip. In numericals, always draw the Gantt chart or the table neatly, write the formula first, and then the answer.
You get step marks even if the final answer is wrong.''',
     T(11, 'Tip: draw the table / Gantt chart, [h:write the formula first] => step marks!', color='red'))

p = page('All the Best!', 10, kind='outro')
beat(p, '''That's the complete operating system subject. If this helped you, share it with your friends who have the exam,
and subscribe to TechVibe24 for more one shot videos. Tell me in the comments which subject you want next. All the best for your exam!''')

if __name__ == '__main__':
    json.dump({'pages': PAGES, 'chapters': CHAPTERS}, open('os_script.json', 'w'), indent=1, ensure_ascii=False)
    nb = sum(len(p['beats']) for p in PAGES); nw = sum(len(b['say'].split()) for p in PAGES for b in p['beats'])
    print('pages', len(PAGES), 'beats', nb, 'words', nw, 'est minutes', round(nw / 150, 1))
