"""
A short, short time into the future, in a nearby galaxy,
you find yourself wanting to take a little trip and get away from the responsibilities of being Planet Thundera's only manufacturer of yarn.
You decide to travel to Planet Care-a-Lot, the most relaxing planet there is. To travel, you are going to use the network of interstellar teleporters.

A teleporter is a small machine floating around somewhere in space.
You can use it remotely from any point in space, but, due to the conservation of teleportation distance principle,
it can teleport you to any other point in space at exactly the same L1 distance from the teleporter as your L1 distance to it before the teleportation.
The L1 distance between two points at coordinates (x0, y0, z0) and (x1, y1, z1) is given by |x0 - x1| + |y0 - y1| + |z0 - z1|.
Unfortunately, your space jetpack is broken, so you cannot move around on your own; to travel, you can only use the teleporters.
You start at Planet Thundera. You can use a teleporter to travel from Planet Thundera to a point p1, then use another to get from p1 to p2, and so on.
The last teleportation must take you exactly to Planet Care-a-Lot.

Given the locations in 3-dimensional space of both planets and all the available teleporters,
find out if it is possible for you to make the trip using only teleporters.
If the trip can be made, what is the minimum number of teleportations needed to get to your destination?
(Even if two teleportations use the same teleporter, they still count as separate teleportations.)

The input is given as points with coordinates that are all integers that fall within a certain range.
However, you are allowed to teleport to intermediate points with integer or non-integer coordinates, and there are no range restrictions on the points you can visit.
"""

"""
The first line of the input gives the number of test cases, T. 
T test cases follow. Each test case starts with a single line with a single integer N, the number of teleporters available. 
Then, N+2 lines follow, each containing three integers Xi, Yi, and Zi. The first of these lines represents the coordinates of your home planet, Thundera. 
The second of these lines represents the coordinates of your destination planet, Care-A-Lot. Each of the remaining N lines represents the coordinates of one of the teleporters.
"""

"""
For each test case, output one line containing Case #x: y, 
where x is the test case number (starting from 1) and y is IMPOSSIBLE if it is not possible to get from Thundera to Care-A-Lot using only the available teleporters, 
or, if it is possible, an integer representing the minimum number of teleportations needed.
"""

"""
Memory limit: 1 GB.
1 ≤ T ≤ 100.
(Xi, Yi, Zi) ≠ (Xj, Yj, Zj) for all i ≠ j. (No two described objects have the same coordinates.)

Small dataset (Test Set 1 - Visible)
Time limit: 180 seconds.
1 ≤ N ≤ 100.
-10^3 ≤ Xi ≤ 10^3, for all i.
-10^3 ≤ Yi ≤ 10^3, for all i.
-10^3 ≤ Zi ≤ 10^3, for all i.
Large dataset (Test Set 2 - Hidden)
Time limit: 360 seconds.
1 ≤ N ≤ 150.
-10^12 ≤ Xi ≤ 10^12, for all i.
-10^12 ≤ Yi ≤ 10^12, for all i.
-10^12 ≤ Zi ≤ 10^12, for all i.
"""

"""
Input
3
1
0 0 0
0 4 0
0 3 0
2
0 0 1
0 0 11
0 0 3
0 0 0
3
0 0 0
6 2 0
6 0 0
3 0 0
6 1 0
"""

"""
Output
Case #1: IMPOSSIBLE
Case #2: 3
Case #3: 2
"""

"""
In Sample Case #1, the only teleporter is exactly 3 units away from Thundera, 
and we can only use it to go to another position that is exactly 3 units away from the teleporter. 
From that position, we can still only reach other positions that are exactly 3 units away from the teleporter. 
Since Care-a-Lot is 1 unit away from the teleporter, we can never reach it.

In Sample Case #2, the optimal strategy is to first use the teleporter at (0, 0, 3) to travel to (0, 0, 5). 
Then, from there, use the teleporter at (0, 0, 0) to travel to (0, 0, -5). 
Finally, from there, use the teleporter at (0, 0, 3) again to travel to (0, 0, 11). 
Note that the two uses of the teleporter at (0, 0, 3) cause us to travel different distances, 
because we are at different distances from the teleporter each time. Also note that the two uses of that teleporter count as two separate teleportations.

In Sample Case #3, the optimal strategy is to first use the teleporter at (3, 0, 0) to travel to (6, 0, 0). 
Then, from there, use the teleporter at (6, 1, 0) to travel to (6, 2, 0). 
Note that even though there was a teleporter at (6, 0, 0), merely occupying the same point as a teleporter does not count as using it.
"""

# code from https://github.com/kamyu104/GoogleCodeJam-2017/blob/master/World%20Finals/teleporters.py
# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2017 Word Finals - Problem F. Teleporters
# https://codingcompetitions.withgoogle.com/codejam/round/0000000000201909/000000000020184b
#
# Time:  O(N^3 * logM), pass in PyPy2 but Python2
# Space: O(N^2 * logM)
#

from itertools import izip, islice

def dist(a, b):
    return abs(a[0]-b[0])+abs(a[1]-b[1])+abs(a[2]-b[2])

def vector_mult(A, B):  # Time: O(N^2), A is a N-d vector, B is a N x N symmetric matrix
    result = [0]*len(B[0])
    B_T = B
    for i, B_T_i in enumerate(B_T):
        for j, (A_j, B_T_i_j) in enumerate(izip(A, B_T_i)):
            dist = A_j + B_T_i_j
            if dist > result[i]:
                result[i] = dist
    return result

def matrix_mult(A, B):  # Time: O(N^3), A, B are both N x N symmetric matrixs
    result = [[0]*len(B[0]) for _ in xrange(len(A))]
    B_T = B
    for i, (result_i, A_i) in enumerate(izip(result, A)):
        for j, (result_j, B_T_j) in enumerate(islice(izip(result, B_T), i, len(result)), i):
            for A_i_k, B_T_j_k in izip(A_i, B_T_j):
                dist = A_i_k + B_T_j_k
                if dist > result_i[j]:
                    result_i[j] = result_j[i] = dist  # result is also a symmetric matrix
    return result

def binary_search(left, right, check_fn, update_fn):  # find min x in (left, right) s.t. check(x) = true
    while right-left >= 2:
        mid = left + (right-left)//2
        found, new_U_vector = check_fn(mid-left)  # Time: O(N^2), Space: O(N)
        if found:
            right = mid
        else:
            left = mid
            update_fn(new_U_vector)  # Time: O(N), Space: O(N)
    return right

def teleporters():
    def check_fn(x):
        new_U_vector = vector_mult(U_vector, matrix_pow[log2[x]])  # Time: O(N^2), Space: O(N)
        return any(dist_Q[i] <= U for i, U in enumerate(new_U_vector)), new_U_vector

    def update_fn(new_U_vector):
        U_vector[:] = new_U_vector

    N = input()
    P, Q = [map(int, raw_input().strip().split()) for _ in xrange(2)]
    teleporters = [map(int, raw_input().strip().split()) for _ in xrange(N)]
    dist_P, dist_Q = [[dist(x, t) for t in teleporters] for x in (P, Q)]
    if any(dist_P_t == dist_Q_t for dist_P_t, dist_Q_t in izip(dist_P, dist_Q)):
        return 1
    if N == 1:
        return "IMPOSSIBLE"
    if all(dist_P_t < dist_Q_t for dist_P_t, dist_Q_t in izip(dist_P, dist_Q)):
        pass  # P is the closer point
    elif all(dist_P_t > dist_Q_t for dist_P_t, dist_Q_t in izip(dist_P, dist_Q)):
        P, Q = Q, P
        dist_P, dist_Q = dist_Q, dist_P
    else:
        return 2

    MAX_STEP_NUM = max(dist_Q)  # the farest reachable distance strictly increase at least 1 per step
    ceil_log2_MAX_STEP_NUM = (MAX_STEP_NUM-1).bit_length()
    left = 2-1  # extend binary search range from [2, MAX_STEP_NUM] to (1, 1+2**ceil_log2_MAX_STEP_NUM)
    right = left+2**ceil_log2_MAX_STEP_NUM
    U_vector = dist_P[:]  # N-d vector
    matrix_pow = [[[dist(t, u) for u in teleporters] for t in teleporters]]
    log2, base = {1:0}, 2
    for i in xrange(1, ceil_log2_MAX_STEP_NUM):  # Time: O(N^3 * logM)
        matrix_pow.append(matrix_mult(matrix_pow[-1], matrix_pow[-1]))
        log2[base] = i
        base <<= 1
    return binary_search(left, right, check_fn, update_fn)

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, teleporters())