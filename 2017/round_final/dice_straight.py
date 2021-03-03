"""
You have a special set of N six-sided dice, each of which has six different positive integers on its faces. Different dice may have different numberings.

You want to arrange some or all of the dice in a row such that the faces on top form a straight (that is, they show consecutive integers).
For each die, you can choose which face is on top.

How long is the longest straight that can be formed in this way?
"""

"""
The first line of the input gives the number of test cases, T. 
T test cases follow. Each test case begins with one line with N, the number of dice. 
Then, N more lines follow; each of them has six positive integers Dij. The j-th number on the i-th of these lines gives the number on the j-th face of the i-th die.
"""

"""
For each test case, output one line containing Case #x: y, where x is the test case number (starting from 1) and y is the length of the longest straight that can be formed.
"""

"""
Memory limit: 1 GB.
1 ≤ T ≤ 100.
1 ≤ Dij ≤ 106 for all i, j.
Small dataset (Test Set 1 - Visible)
Time limit: 60 seconds.
1 ≤ N ≤ 100.
Large dataset (Test Set 2 - Hidden)
Time limit: 120 seconds.
1 ≤ N ≤ 50000.
The sum of N across all test cases ≤ 200000.
"""

"""
Input
3
4
4 8 15 16 23 42
8 6 7 5 30 9
1 2 3 4 55 6
2 10 18 36 54 86
2
1 2 3 4 5 6
60 50 40 30 20 10
3
1 2 3 4 5 6
1 2 3 4 5 6
1 4 2 6 5 3
"""

"""
Output
Case #1: 4
Case #2: 1
Case #3: 3
"""

"""
In sample case #1, a straight of length 4 can be formed by taking the 2 from the fourth die, the 3 from the third die, the 4 from the first die, and the 5 from the second die.

In sample case #2, there is no way to form a straight larger than the trivial straight of length 1.

In sample case #3, you can take a 1 from one die, a 2 from another, and a 3 from the remaining unused die. 
Notice that this case demonstrates that there can be multiple dice with the same set of values on their faces.
"""

# code from https://github.com/kamyu104/GoogleCodeJam-2017/blob/master/World%20Finals/dice_straight.py

# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2017 Word Finals - Problem A. Dice Straight
# https://codingcompetitions.withgoogle.com/codejam/round/0000000000201909/00000000002017fc
#
# Time:  O(N^2), pass in PyPy2 but Python2
# Space: O(N)
#

from collections import defaultdict

# Ford-Fulkerson Algorithm
# Time:  O(V * E)
# Space: O(V)
from functools import partial

class BipartiteMatching:
    def __init__(self, graph):
        self.graph = graph
        self.match = {}
        self.match_r = {}

    def augment(self, u):
        def divide(u):
            if u not in self.graph:
                return
            for v in self.graph[u]:
                if v not in self.match_r:  # early return
                    self.match[u] = v
                    self.match_r[v] = u
                    ret[0] = True
                    return
            stk.append(partial(conquer, u, iter(self.graph[u])))

        def conquer(u, it):
            for v in it:
                if v in lookup:
                    continue
                lookup.add(v)
                stk.append(partial(postprocess, u, v, it))
                stk.append(partial(divide, self.match_r[v]))
                return

        def postprocess(u, v, it):
            if not ret[0]:
                stk.append(partial(conquer, u, it))
                return
            self.match[u] = v
            self.match_r[v] = u

        ret, stk, lookup = [False], [], set()
        stk.append(partial(divide, u))
        while stk:
            stk.pop()()
        return ret[0]

def dice_straight():
    N = input()
    D = [map(int, raw_input().strip().split()) for _ in xrange(N)]
    graph = defaultdict(list)
    for i, dice in enumerate(D):
        for dij in dice:
            graph[dij].append(i)
    nums, bipartite_matching = sorted(graph.iterkeys()), BipartiteMatching(graph)
    result, right = 0, -1
    for left in xrange(len(nums)):
        if (len(nums)-1)-left+1 <= result:  # early return
            break
        while right+1 != len(nums) and (right+1 == left or nums[right]+1 == nums[right+1]) and \
                bipartite_matching.augment(nums[right+1]):
            right += 1
        result = max(result, right-left+1)
        bipartite_matching.match_r.pop(bipartite_matching.match.pop(nums[left]))
    return result

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, dice_straight())