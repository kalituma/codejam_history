#from https://github.com/kamyu104/GoogleCodeJam-2019/blob/master/Round%201B/fair-fight2.py
# Copyright (c) 2019 kamyu. All rights reserved.
#
# Google Code Jam 2019 Round 1B - Problem C. Fair Fight
# https://codingcompetitions.withgoogle.com/codejam/round/0000000000051706/0000000000122838
#
# Time:  O(NlogN), pass in PyPy2 but Python2
# Space: O(NlogN)
#

import collections
import itertools

class RangeQuery(object):
    def __init__(self, items, fn):
        self.__fn = fn
        self.__pow = [1]
        self.__bit_length = [0]
        n, count = len(items), 1
        for i in xrange(1, n.bit_length()+1):
            self.__pow.append(self.__pow[-1] * 2)
            self.__bit_length.extend([i]*min(count, n+1-len(self.__bit_length)))
            count *= 2
        self.__rq = rq = [[0 for _ in xrange(n.bit_length())] for _ in xrange(n)]
        for i in xrange(n):
            self.__rq[i][0] = items[i]
        for step in xrange(1, n.bit_length()):  # Time: O(NlogN)
            for i in xrange(n+1-self.__pow[step]):
                self.__rq[i][step] = fn(self.__rq[i][step-1],
                                        self.__rq[i+self.__pow[step-1]][step-1])

    def query(self, start, stop):  # Time: O(1)
        j = self.__bit_length[stop-start]-1
        x = self.__rq[start][j]
        y = self.__rq[stop-self.__pow[j]][j]
        return self.__fn(x, y)

def lower_bound(left, right, check):
    while left <= right:
        mid = left + (right-left)//2
        if check(mid):
            right = mid-1
        else:
            left = mid+1
    return left

def upper_bound(left, right, check):
    while left <= right:
        mid = left + (right-left)//2
        if not check(mid):
            right = mid-1
        else:
            left = mid+1
    return left  # assert(right == left-1)

def fair_fight():
    N, K = map(int, raw_input().strip().split())
    C = map(int, raw_input().strip().split())
    D = map(int, raw_input().strip().split())

    C_RMQ, D_RMQ = RangeQuery(C, max), RangeQuery(D, max)
    result, next_to_last_seen = 0, collections.defaultdict(int)
    for i, (Ci, Di) in enumerate(itertools.izip(C, D)):
        if Di-Ci > K:  # skip impossible intervals to save time
            continue
        L_good = lower_bound(next_to_last_seen[Ci], i,
                             lambda x: C_RMQ.query(x, i+1) == Ci and D_RMQ.query(x, i+1)-Ci <= K)
        R_good = upper_bound(i, N-1,
                             lambda x: C_RMQ.query(i, x+1) == Ci and D_RMQ.query(i, x+1)-Ci <= K)-1
        L_bad = lower_bound(next_to_last_seen[Ci], i,
                            lambda x: C_RMQ.query(x, i+1) == Ci and D_RMQ.query(x, i+1)-Ci <= -K-1)
        R_bad = upper_bound(i, N-1,
                            lambda x: C_RMQ.query(i, x+1) == Ci and D_RMQ.query(i, x+1)-Ci <= -K-1)-1
        result += (i-L_good+1)*(R_good-i+1)-(i-L_bad+1)*(R_bad-i+1)
        next_to_last_seen[Ci] = i+1  # to avoid duplicated count

    return result

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, fair_fight())