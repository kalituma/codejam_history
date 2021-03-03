"""
A spanning tree of an undirected graph with N nodes is a tree with N-1 edges that uses only edges from N and includes all nodes in N.

Please construct a graph with at least 2 nodes, and no more than 22 nodes, such that the graph has exactly K different spanning trees.
(Two spanning trees are considered different if and only if the sets of edges that they use are different.)
The graph must have at most one edge per pair of nodes, and must not contain a loop (an edge from a node to itself).

It is guaranteed that at least one such graph exists for every K within the limits below.

- Solving this problem

This problem has only 1 Small dataset and no Large dataset. You will be able to retry the dataset (with a time penalty).
"""

"""
The first line of the input gives the number of test cases, T. T test cases follow. Each consists of one line with an integer K: the desired number of spanning trees.
"""

"""
For each test case, first output one line containing Case #x: y, 
where x is the test case number (starting from 1), and y is the number of nodes in your graph. (y must be between 2 and 22, inclusive.) 
Then, output y more lines. The i-th of these lines represents the i-th node in the graph, and must contain exactly y characters. 
The j-th character on the i-th line should be 1 if the i-th node and the j-th node are connected with an edge, and 0 otherwise. 
Note that this matrix will be symmetric and it will have all 0s along its main diagonal.

If multiple answers are possible, you may output any of them. Note that we guarantee that at least one valid answer exists for every K within the limits below.
"""

"""
Time limit: 240 seconds per test set.
Memory limit: 1 GB.
1 ≤ T ≤ 300.
Small dataset (Test Set 1 - Visible)
3 ≤ K ≤ 10000.
"""

"""
Input
2
3
8
"""

"""
Output
Case #1: 3
011
101
110
Case #2: 4
0111
1001
1001
1110
"""

"""
In Case #1, the graph is a triangle, and removing any one edge creates a different spanning tree.

In Case #2, the available edges in our solution tree are 1-2, 1-3, 1-4, 2-4, and 3-4. The eight different spanning trees are defined by these sets of edges:

1-2, 1-3, 1-4
1-2, 1-3, 2-4
1-2, 1-3, 3-4
1-2, 1-4, 3-4
1-2, 2-4, 3-4
1-3, 1-4, 2-4
1-3, 2-4, 3-4
1-4, 2-4, 3-4
"""

# code from https://codingcompetitions.withgoogle.com/codejam/round/0000000000201909/000000000020187a
# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2017 Word Finals - Problem C. Spanning Planning
# https://codingcompetitions.withgoogle.com/codejam/round/0000000000201909/000000000020187a
#
# Time:  O(R * N^3), R is the times of random, which may be up to 2*10^5
# Space: O(N^2)    , N is the empirical number of nodes, which could be 13
#

from sys import float_info
from random import randint, seed
from operator import mul

def determinant(matrix):
    N = len(matrix)
    sign = 1
    for d in xrange(N):  # turn the matrix into upper triangle form by Gaussian elimination
        for i in xrange(d, N):
            if abs(matrix[i][d]) > float_info.epsilon:  # use double to approximate the determinant rather than Fraction which is too slow in Python2 / PyPy2
                break
        else:
            break
        if i != d:
            matrix[i], matrix[d] = matrix[d], matrix[i]
            sign *= -1  # interchange
        for i in xrange(d+1, N):
            scalar = 1.0*matrix[i][d]/matrix[d][d]
            for j in xrange(N):
                matrix[i][j] -= scalar*matrix[d][j]
    return int(round(sign*reduce(mul, (matrix[d][d] for d in xrange(N)))))

def minor(matrix, r, c):
    return determinant([[v for j, v in enumerate(row) if j+1 != c]
                        for i, row in enumerate(matrix) if i+1 != r])

def cofactor(matrix, r, c):
    return (-1)**((r+c)%2) * minor(matrix, r, c)

# https://www.geeksforgeeks.org/total-number-spanning-trees-graph/
def kirchhoff_matrix_tree_theorem(adj):
    N = len(adj)
    laplacian_matrix = [[0]*N for _ in xrange(N)]
    for i in xrange(N):
        for j in xrange(N):
            if not adj[i][j]:
                continue
            laplacian_matrix[i][i] += 1
            laplacian_matrix[i][j] -= adj[i][j]
        if laplacian_matrix[i][i] == 0:
            return 0
    return cofactor(laplacian_matrix, 1, 1)  # every cofactor i, j where 1 <= i <= N and 1 <= j <= N is the same

def spanning_planning():
    K = input()
    if K <= MAX_N:
        N = K
        adj = [[int(abs(i-j) in (1, N-1)) for j in xrange(N)] for i in xrange(N)]
    else:
        N = EXP_N
        adj = [[0]*N for _ in xrange(N)]
        while True:
            number_of_spanning_tree = kirchhoff_matrix_tree_theorem(adj)
            if number_of_spanning_tree > K:
                while True:
                    i, j = randint(0, N-1), randint(0, N-1)
                    if i != j and adj[i][j]:
                        adj[i][j] = adj[j][i] = 0
                        break
            elif number_of_spanning_tree < K:
                while True:
                    i, j = randint(0, N-1), randint(0, N-1)
                    if i != j and not adj[i][j]:
                        adj[i][j] = adj[j][i] = 1
                        break
            else:
                break
    return "%s\n%s" % (N, "\n".join("".join(map(str, row)) for row in adj))

seed(0)
MAX_N = 22
EXP_N = 13
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, spanning_planning())