"""
You are on top of Mount Everest, and you want to enjoy all the nice hiking trails that are up there.
However, you know from past experience that climbing around on Mount Everest alone is bad — you might get lost in the dark!
So you want to go on hikes at pre-arranged times with tour guides.

There are C camps on the mountain (numbered 1 through C), and there are 2 × C one-way hiking tours (numbered 1 through 2 × C).
Each hiking tour starts at one camp and finishes at a different camp, and passes through no other camps in between.
Mount Everest is sparsely populated, and business is slow; there are exactly 2 hiking tours departing from each camp, and exactly 2 hiking tours arriving at each camp.

Each hiking tour runs daily. Tours 1 and 2 start at camp 1, tours 3 and 4 start at camp 2, and so on: in general, tour 2 × i - 1 and tour 2 × i start at camp i.
The i-th hiking tour ends at camp number Ei, leaves at hour Li, and has a duration of exactly Di hours.

It is currently hour 0; the hours in a day are numbered 0 through 23. You are at camp number 1,
and you want to do each of the hiking tours exactly once and end up back at camp number 1.
You cannot travel between camps except via hiking tours. While you are in a camp,
you may wait for any number of hours (including zero) before going on a hiking tour, but you can only start a hiking tour at the instant that it departs.

After looking at the tour schedules, you have determined that it is definitely possible to achieve your goal,
but you want to do it as fast as possible. If you plan your route optimally, how many hours will it take you to finish all of the tours?
"""

"""
The first line of the input gives the number of test cases, T.
T test cases follow. Each begins with one line with an integer C: the number of camps. Then, 2 × C more lines follow. 
The i-th of these lines (counting starting from 1) represents one hiking tour starting at camp number floor((i + 1) / 2), 
and contains three integers Ei, Li, and Di, as described above. Note that this format guarantees that exactly two tours start at each camp.
"""

"""
For each test case, output one line containing Case #x: y, where x is the test case number (starting from 1) 
and y is the minimum number of hours that it will take you to achieve your goal, as described above.
"""

"""
Time limit: 20 seconds per test set.
Memory limit: 1 GB.
1 ≤ T ≤ 100.
1 ≤ Ei ≤ C.
Ei ≠ ceiling(i / 2), for all i. (No hiking tour starts and ends at the same camp.)
size of {j : Ej = i} = 2, for all j. (Exactly two tours end at each camp.)
0 ≤ Li ≤ 23.
1 ≤ Di ≤ 1000.
There is at least one route that starts and ends at camp 1 and includes each hiking tour exactly once.
Small dataset (Test Set 1 - Visible)
2 ≤ C ≤ 15.
Large dataset (Test Set 2 - Hidden)
2 ≤ C ≤ 1000.
"""

"""
Input
2
2
2 1 5
2 0 3
1 4 4
1 6 3
4
3 0 24
2 0 24
4 0 24
4 0 24
2 0 24
1 0 24
3 0 24
1 0 24
"""

"""
output
Case #1: 32
Case #2: 192
"""

"""
In sample case #1, the optimal plan is as follows:

Wait at camp 1 for an hour, until it becomes hour 1.
Leave camp 1 at hour 1 to take the 5 hour hiking tour; arrive at camp 2 at hour 6.
Immediately leave camp 2 at hour 6 to take the 3 hour hiking tour; arrive at camp 1 at hour 9.
Wait at camp 1 for 15 hours, until it becomes hour 0 of the next day.
Leave camp 1 at hour 0 to take the 3 hour hiking tour; arrive at camp 2 at hour 3.
Wait at camp 2 for 1 hour, until it becomes hour 4.
Leave camp 2 at hour 4 to take the 4 hour hiking tour; arrive at camp 1 at hour 8.
This achieves the goal in 1 day and 8 hours, or 32 hours. Any other plan takes longer.

In sample case #2, all of the tours leave at the same time and are the same duration. 
After finishing any tour, you can immediately take another tour. If we number the tours from 1 to 8 in the order in which they appear in the test case, 
one optimal plan is: 1, 5, 4, 7, 6, 2, 3, 8.
"""

# code from https://github.com/kamyu104/GoogleCodeJam-2017/blob/master/Round%203/mountain_tour.py

# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2017 Round 3 - Problem C. Mountain Tour
# https://codingcompetitions.withgoogle.com/codejam/round/0000000000201902/0000000000201877
#
# Time:  O(C * log*(C))
# Space: O(C)
#

# Template:
# https://github.com/kamyu104/FacebookHackerCup-2019/blob/master/Final%20Round/temporal_revision.py
class UnionFind(object):  # Time: (N * log*(N)), Space: O(N)
    def __init__(self, n):
        self.set = range(n)

    def get_id(self):
        self.set.append(len(self.set))
        return len(self.set)-1

    def find_set(self, x):
        stk = []
        while self.set[x] != x:  # path compression.
            stk.append(x)
            x = self.set[x]
        while stk:
            self.set[stk.pop()] = x
        return x

    def union_set(self, x, y):
        x_root, y_root = map(self.find_set, (x, y))
        if x_root == y_root:
            return False
        self.set[min(x_root, y_root)] = max(x_root, y_root)
        return True

def time_to_arrive(a, b):
    return (a+b)%24

def time_to_leave(a, b):
    return (b-a)%24

def mountain_tour():
    C = input()
    tours = map(lambda x: (x[0]-1, x[1], x[2]), [map(int, raw_input().strip().split()) for _ in xrange(2*C)])
    prev_camps = [[] for _ in xrange(C)]
    for i, (E, _, _) in enumerate(tours):
        prev_camps[E].append(i)
    result = sum(D for _, _, D in tours)
    next_camps, costs = [0]*(2*C), [0]*C
    for i, (prev_a, prev_b) in enumerate(prev_camps):
        if not i:
            ta = min(time_to_leave(time_to_arrive(tours[prev_a][1], tours[prev_a][2]), tours[2*i][1]) + tours[2*i+1][1],
                     time_to_leave(time_to_arrive(tours[prev_b][1], tours[prev_b][2]), tours[2*i+1][1]) + tours[2*i][1])
            tb = min(time_to_leave(time_to_arrive(tours[prev_a][1], tours[prev_a][2]), tours[2*i+1][1]) + tours[2*i][1],
                     time_to_leave(time_to_arrive(tours[prev_b][1], tours[prev_b][2]), tours[2*i][1]) + tours[2*i+1][1])
        else:
            ta = time_to_leave(time_to_arrive(tours[prev_a][1], tours[prev_a][2]), tours[2*i][1]) + \
                 time_to_leave(time_to_arrive(tours[prev_b][1], tours[prev_b][2]), tours[2*i+1][1])
            tb = time_to_leave(time_to_arrive(tours[prev_a][1], tours[prev_a][2]), tours[2*i+1][1]) + \
                 time_to_leave(time_to_arrive(tours[prev_b][1], tours[prev_b][2]), tours[2*i][1])
            assert(abs(ta-tb) in (0, 24))
        if ta < tb:
            result += ta
            next_camps[prev_a], next_camps[prev_b] = 2*i, 2*i+1
            costs[i] = tb-ta
        else:
            result += tb
            next_camps[prev_a], next_camps[prev_b] = 2*i+1, 2*i
            costs[i] = ta-tb
    union_find = UnionFind(2*C)
    for i in xrange(2*C):
        union_find.union_set(i, next_camps[i])
    for i, c in enumerate(costs):
        if not c:  # firstly, union tours with 0 hr
            union_find.union_set(2*i, 2*i+1)
    # secondly, union tours of camp1 if they are in disjoint cycles, which has the smallest union costs in the rest of disjoint cycles
    # finally, union the rest of tours in disjoint cycles, which all have the same cost 24 hrs
    return result + sum(c for i, c in enumerate(costs) if union_find.union_set(2*i, 2*i+1))

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, mountain_tour())