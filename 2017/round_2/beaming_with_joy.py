"""
Joy is about to go on a long vacation, so she has hired technicians to install a security system based on infrared laser beams.
The technicians have given her a diagram that represents her house as a grid of unit cells with R rows and C columns. Each cell in this grid contains one of the following:

/: A two-sided mirror that runs from the cell's lower left corner to its upper right corner.
\: A two-sided mirror that runs from the cell's upper left corner to its lower right corner.
-: A beam shooter that shoots horizontal beams out into the cells (if any) to the immediate left and right of this cell.
|: A beam shooter that shoots vertical beams out into the cells (if any) immediately above and below this cell.
#: A wall. (Note that the house is not necessarily surrounded by a border of walls; this is one reason why Joy needs a security system!)
.: Nothing; the cell is empty.

Beams travel in straight lines and continue on through empty cells.
When a beam hits a mirror, it bounces 90 degrees off the mirror's surface and continues.
When a beam traveling to the right hits a / mirror, it bounces off the mirror and starts traveling up;
beams traveling up, left, or down that hit a / mirror bounce off and travel right, down, or left, respectively.
The \ mirror behaves similarly: when a beam traveling right, up, left or down hits it,
it bounces off and starts traveling down, left, up or right, respectively. When a beam hits a wall or goes out of the bounds of the grid, it stops.
It is fine for beams to cross other beams, but if a beam hits any beam shooter
(including, perhaps, the beam shooter that originated the beam), that beam shooter will be destroyed!

Joy wants to make sure that every empty cell in the house has at least one beam passing through it,
and that no beam shooters are destroyed, since that would just be wasting money! Unfortunately,
the technicians have already installed the system, so the most Joy can do is rotate some of the existing beam shooters 90 degrees.
That is, for any number (including zero) of beam shooters, she can turn - into | or vice versa.

Can you find any way for Joy to achieve her goal, or determine that it is impossible?
Note that it is not required to minimize the number of rotations of beam shooters.
"""

"""
The first line of the input gives the number of test cases, T. 
T test cases follow. Each case begins with one line with two integers R and C: the number of rows and columns in the grid representing the house. 
Then, R lines of C characters each follow; each character is /, \, -, |, #, or ., as described in the statement.
"""

"""
For each test case, output one line containing Case #x: y, 
where x is the test case number (starting from 1) and y is IMPOSSIBLE if Joy cannot accomplish her goal, or POSSIBLE if she can. 
Then, if the case is possible, output the same R lines of C characters each from the input grid, with zero or more instances of - replaced by | or vice versa.

If there are multiple possible answers, you may output any of them.
"""

"""
Time limit: 20 seconds per test set.
Memory limit: 1 GB.
1 ≤ T ≤ 100.
1 ≤ C ≤ 50.
Each character in the grid is one of /, \, -, |, #, or ..
The number of - characters plus the number of | characters (that is, the number of beam shooters) in the grid is between 1 and 100, inclusive.
There is at least 1 . character (that is, empty space) in the grid.
Small dataset (Test Set 1 - Visible)
1 ≤ R ≤ 5.
There are no / or \ characters (that is, no mirrors) in the grid.
Large dataset (Test Set 2 - Hidden)
1 ≤ R ≤ 50.
"""

"""
    5
    1 3
    -.-
    3 4
    #.##
    #--#
    ####
    2 2
    -.
    #|
    4 3
    .|.
    -//
    .-.
    #\/
    3 3
    /|\
    \\/
    ./#
"""

"""
    Case #1: IMPOSSIBLE
    Case #2: POSSIBLE
    #.##
    #||#
    ####
    Case #3: POSSIBLE
    |.
    #|
    Case #4: POSSIBLE
    .-.
    |//
    .|.
    #\/
    Case #5: IMPOSSIBLE
"""

"""
Note that the last 2 sample cases would not appear in the Small dataset.

In Sample Case #1, if a beam shooter is positioned to shoot its beam into the empty cell, 
it will necessarily destroy the other beam shooter. So the case is IMPOSSIBLE.

In Sample Case #2, the leftmost beam shooter must be rotated to cover the empty cell. 
The rightmost beam shooter must also be rotated to avoid destroying the leftmost beam shooter.

In Sample Case #3, the existing beam shooters already cover all empty cells with their beams and do not destroy each other, 
so outputting the grid from the input would be acceptable. However, notice that the output that we have given is also correct.

In Sample Case #4, one acceptable solution is to rotate all three of the beam shooters. However, note that the following would also be acceptable:

.-.
|//
.-.
#\/

since it is not necessary for cells with mirrors to have a beam pass through them. (Who would steal giant diagonal mirrors, anyway?)

In Sample Case #5, the beam shooter would destroy itself no matter which orientation Joy chooses for it, so the case is IMPOSSIBLE.
"""

from collections import defaultdict, deque
import sys

sys.setrecursionlimit(200000)

class Graph:
    def __init__(self):
        self.v = set()
        self.e = defaultdict(list)
        self.r = defaultdict(list)
    def add(self, a, b):
        self.v.add(a)
        self.v.add(b)
        self.e[a].append(b)
        self.r[b].append(a)
    def components(self):
        L = deque()
        visited = set()
        def visit(u):
            if u not in visited:
                visited.add(u)
                for v in self.e[u]:
                    visit(v)
                L.appendleft(u)

        order = []
        assigned = set()
        cs = defaultdict(set)
        def assign(u, root):
            if u not in assigned:
                assigned.add(u)
                if root not in cs:
                    order.append(root)
                cs[root].add(u)
                for v in self.r[u]:
                    assign(v, root)

        for u in self.v:
            visit(u)
        for u in L:
            assign(u, u)

        return [cs[c] for c in order]

class TwoSat:
    def __init__(self):
        self.cs = None
    def is_satisfiable(self, clauses):
        g = Graph()
        for p, q in clauses:
            g.add(-p, q)
            g.add(-q, p)

        cs = g.components()
        for c in cs:
            for v in c:
                if -v in c:
                    return False

        self.cs = cs
        return True
    def assignment(self):
        if self.cs is None:
            raise Exception('No components')

        a = set()
        for c in reversed(self.cs):
            for v in c:
                if v not in a and -v not in a:
                    a.add(v)
        return a

class CNFEncoder:
    def __init__(self, solver):
        self.solver = solver
        self.forward_map = {}
        self.reverse_map = {}
        self.clauses = []
    def add(self, o1, v1, o2, v2):
        self.clauses.append((self._encode(o1) * self._sign(v1), self._encode(o2) * self._sign(v2)))
    def solve(self):
        if self.solver.is_satisfiable(self.clauses):
            return map(self._decode, self.solver.assignment())
    def _encode(self, obj):
        if obj not in self.forward_map:
            key = 1 + len(self.forward_map)
            self.forward_map[obj] = key
            self.reverse_map[key] = obj
        return self.forward_map[obj]
    def _decode(self, key):
        return self.reverse_map[abs(key)], key > 0
    def _sign(self, val):
        return {True: 1, False: -1}[val]


R, C = 0, 0


def _fire(M, i, j, di, dj, acc):
    ni, nj = i + di, j + dj
    if ni < 0 or ni >= R or nj < 0 or nj >= C:
        return acc
    if M[ni][nj] == '#':
        return acc
    if M[ni][nj] == '.':
        acc.append((ni, nj))
        return _fire(M, ni, nj, di, dj, acc)
    if M[ni][nj] in '-|':
        return None
    if M[ni][nj] == '/':
        return _fire(M, ni, nj, -dj, -di, acc)
    if M[ni][nj] == '\\':
        return _fire(M, ni, nj, dj, di, acc)
    raise Exception('Nani?')

def fire(M, i, j, d):
    if d == '-':
        pr = _fire(M, i, j, 0,  1, [])
        pl = _fire(M, i, j, 0, -1, [])
        return None if pr is None or pl is None else pr + pl
    else:
        pu = _fire(M, i, j, -1, 0, [])
        pd = _fire(M, i, j,  1, 0, [])
        return None if pu is None or pd is None else pu + pd

def negate(c):
    return '-' if c == '|' else '|'

def solve(M):
    blank = {}
    laser = {}
    for i, r in enumerate(M):
        for j, c in enumerate(r):
            if c == '.':
                blank[(i, j)] = []
            elif c in '-|':
                laser[(i, j)] = c

    solver = CNFEncoder(TwoSat())
    for l in laser:
        paths = [fire(M, *l, '-'), fire(M, *l, '|')]
        which = 0
        for i, (path, dir) in enumerate(zip(paths, '-|')):
            if path is not None:
                which |= i+1
                for dot in path:
                    blank[dot].append((l, dir))
        if which == 0:
            print ('Laser at {} will always hit a laser'.format(l), file=sys.stderr)
            return []
        if which == 1:
            solver.add(l, False, l, False)
        elif which == 2:
            solver.add(l, True, l, True)

    for dot, options in blank.items():
        if not options:
            print ('Dot at {} can not be covered'.format(dot), file=sys.stderr)
            return []
        if len(options) == 1:
            l, dir = options[0]
            solver.add(l, dir == '|', l, dir == '|')
        elif len(options) == 2:
            l0, d0 = options[0]
            l1, d1 = options[1]
            solver.add(l0, d0 == '|', l1, d1 == '|')
        else:
            print ('There are {} options for {}'.format(len(options), dot), file=sys.stderr)
            return []

    solution = solver.solve()
    if not solution:
        print ('Solver says no soup for you', file=sys.stderr)
        return []

    for (i, j), is_vertical in solution:
        M[i][j] = '|' if is_vertical else '-'

    return M


T = int(input())
for x in range(1, T+1):
    R, C = map(int, input().split())
    M = [list(input()) for _ in range(R)]
    R = solve(M)
    print ('Case #{}: {}'.format(x, 'POSSIBLE' if R else 'IMPOSSIBLE'))
    for m in R:
        print (''.join(m))