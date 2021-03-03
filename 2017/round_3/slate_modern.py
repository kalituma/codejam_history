"""
The prestigious Slate Modern gallery specializes in the latest art craze:
grayscale paintings that follow very strict rules. Any painting in the gallery must be a grid with R rows and C columns.
Each cell in the grid is painted with a color of a certain positive integer brightness value;
to make sure the art is not too visually startling, the brightness values of any two cells that share an edge (not just a corner) must differ by no more than D units.

Your artist friend Cody-Jamal is working on a canvas for the gallery.
Last night, he became inspired and filled in N different particular cells with certain positive integer brightness values.
You just told him about the gallery's rules today,
and now he wants to know whether it is possible to fill in all of the remaining cells with positive integer brightness values
and complete the painting without breaking the gallery's rules. If this is possible,
he wants to make the sum of the brightness values as large as possible, to save his black paint.
Can you help him find this sum or determine that the task is impossible? Since the output can be a really big number,
we only ask you to output the remainder of dividing the result by the prime 109+7 (1000000007).
"""

"""
The first line of the input gives the number of test cases, T. 
T test cases follow. Each test case begins with one line with four integers: R, C, N, and D, as described above. 
Then, N lines follow; the i-th of these has three integers Ri, Ci, and Bi,
indicating that the cell in the Rith row and Cith column of the grid has brightness value Bi. The rows and columns of the grid are numbered starting from 1.
"""

"""
For each test case, output one line containing Case #x: y, 
where x is the test case number (starting from 1) and y is either IMPOSSIBLE if it is impossible to complete the picture, 
or else the value of the maximum possible sum of all brightness values modulo the prime 109+7 (1000000007).
"""

"""
Memory limit: 1 GB.

1 ≤ T ≤ 100.
1 ≤ N ≤ 200.
1 ≤ D ≤ 109.
1 ≤ Ri ≤ R, for all i. 1 ≤ Ci ≤ C, for all i. 1 ≤ Bi ≤ 109, for all i. 
(Note that the upper bound only applies to cells that Cody-Jamal already painted. You can assign brightness values larger than 109 to other cells.)
N < R × C. (There is at least one empty cell.)
Ri ≠ Rj and/or Ci ≠ Cj for all i ≠ j. (All of the given cells are different cells in the grid.)
Small dataset (Test Set 1 - Visible)
Time limit: 40 seconds.
1 ≤ R ≤ 200.
1 ≤ C ≤ 200.
Large dataset (Test Set 2 - Hidden)
Time limit: 80 seconds.
1 ≤ R ≤ 10^9.
1 ≤ C ≤ 10^9.
"""

"""
Input
4
2 3 2 2
2 1 4
1 2 7
1 2 1 1000000000
1 2 1000000000
3 1 2 100
1 1 1
3 1 202
2 2 2 2
2 1 1
2 2 4
"""

"""
Output
Case #1: 40
Case #2: 999999986
Case #3: IMPOSSIBLE
Case #4: IMPOSSIBLE
"""

"""
In Sample Case #1, the optimal way to finish the painting is:

6 7 9
4 6 8

and the sum is 40.

In Sample Case #2, the optimal way to finish the painting is:

2000000000 1000000000

and the sum is 3000000000; modulo 109+7, it is 999999986.

In Sample Case #3, the task is impossible. 
No matter what value you choose for the cell in row 2, it will be too different from at least one of the two neighboring filled-in cells.

In Sample Case #4, the two cells that Cody-Jamal filled in already have brightness values that are too far apart, so it is impossible to continue.
"""
# code from https://github.com/kamyu104/GoogleCodeJam-2017/blob/master/Round%203/slate_modern.py

# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2017 Round 3 - Problem D. Slate Modern
# https://codingcompetitions.withgoogle.com/codejam/round/0000000000201902/0000000000201903
#
# Time:  O(N^2)
# Space: O(N^2)
#

# divide submatrix into 4 parts, each part would be either a rectangle, triangle,
# ladder-shaped, or rectangle excluding triangle, generalized as follows:
#  +-------- c+1 --------+
#  |b...............b+D*c|
#  |.                   .|
#  |.            b+D*anti+
# r+1                  ./
#  |.          b+D*anti/
#  |.                ./
#  |b+D*r....b+D*anti/
#  +----------------+
def f(b, r, c, anti, D):
    def rectangle(b, r, c, D):
        return b*(r+1)*(c+1) + D*(r+c)*(r+1)*(c+1)//2

    def triangle(b, anti, D):
        return (b-D)*anti*(anti+1)//2 + D*anti*(anti+1)*(2*anti+1)//6

    r, c, anti = min(r, anti), min(c, anti), min(anti, r+c)
    return rectangle(b, r, c, D) - triangle(b+D*(r+c), (r+c)-anti, -D)

def coordinate_compression(R, C, D, fixeds):
    rows, cols = sorted(set([1, R+1]+[r for r, _, _ in fixeds])), sorted(set([1, C+1]+[c for _, c, _ in fixeds]))
    lookup_r, lookup_c = {x:i for i, x in enumerate(rows)}, {x:i for i, x in enumerate(cols)}
    dp = [[[float("inf")]*4 for _ in xrange(len(cols))] for _ in xrange(len(rows))]
    for r, c, b in fixeds:
        dp[lookup_r[r]][lookup_c[c]] = [b+D*(-r-c), b+D*(r-c), b+D*(-r+c), b+D*(r+c)]
    for d1, direction1 in enumerate(DIRECTIONS):
        for i in direction1(xrange(len(rows))):
            for d2, direction2 in enumerate(DIRECTIONS):
                for j in direction2(xrange(len(cols))):
                    if 0 <= i+2*d1-1 < len(rows):
                        dp[i][j][d2*2+d1] = min(dp[i][j][d2*2+d1], dp[i+2*d1-1][j][d2*2+d1])
                    if 0 <= j+2*d2-1 < len(cols):
                        dp[i][j][d2*2+d1] = min(dp[i][j][d2*2+d1], dp[i][j+2*d2-1][d2*2+d1])
    return rows, cols, [[[dp[i][j][0], dp[i+1][j][1], dp[i][j+1][2], dp[i+1][j+1][3]] for j in xrange(len(cols)-1)] for i in xrange(len(rows)-1)]

def slate_modern():
    R, C, N, D = map(int, raw_input().strip().split())
    fixeds = [map(int, raw_input().strip().split()) for i in xrange(N)]
    if any(abs(b1-b2) > D*(abs(r1-r2)+abs(c1-c2)) for r1, c1, b1 in fixeds for r2, c2, b2 in fixeds):
        return "IMPOSSIBLE"
    rows, cols, min_manhattan_dist_dp = coordinate_compression(R, C, D, fixeds)
    result = 0
    for i in xrange(len(rows)-1):
        for j in xrange(len(cols)-1):
            r0, c0, r1, c1 = rows[i], cols[j], rows[i+1], cols[j+1]
            m0, m1, m2, m3 = min_manhattan_dist_dp[i][j]  # tl, bl, tr, br
            min_r, max_r = r0, min(r1-1, (m1-m0)/(2*D))
            min_c, max_c = c0, min(c1-1, (m2-m0)/(2*D))
            min_anti, max_anti = r0+c0, min((r1-1)+(c1-1), (m3-m0)/(2*D))
            if (min_r <= max_r) and (min_c <= max_c) and (min_anti <= max_anti):
                # b0 = min(b + D*(r0-r + c0-c)) = min(b+D*(-r-c)) + D*(min_r+min_c)
                result = (result + f(m0+D*min_anti, max_r-min_r, max_c-min_c, max_anti-min_anti, D))%MOD
            min_r, max_r = max(r0, (m1-m0)/(2*D)+1), r1-1
            min_diag, max_diag = c0-(r1-1), min((c1-1)-r0, (m2-m1)/(2*D))
            min_c, max_c = c0, min(c1-1, (m3-m1)/(2*D))
            if (min_r <= max_r) and (min_c <= max_c) and (min_diag <= max_diag):
                # b1 = min(b + D*(r-(r1-1) + c0-c)) = min(b+D*(r-c)) + D*(-max_r+min_c)
                result = (result + f(m1+D*min_diag, max_r-min_r, max_c-min_c, max_diag-min_diag, D))%MOD
            min_c, max_c = max(c0, (m2-m0)/(2*D)+1), c1-1
            min_diag, max_diag = max(c0-(r1-1), (m2-m1)/(2*D)+1), (c1-1)-r0
            min_r, max_r = r0, min(r1-1, (m3-m2)/(2*D))
            if (min_r <= max_r) and (min_c <= max_c) and (min_diag <= max_diag):
                # b2 = min(b + D*(r0-r + c-(c1-1))) = min(b+D*(-r+c)) + D*(min_r-max_c)
                result = (result + f(m2+D*(-max_diag), max_r-min_r, max_c-min_c, max_diag-min_diag, D))%MOD
            min_anti, max_anti = max(r0+c0, (m3-m0)/(2*D)+1), (r1-1)+(c1-1)
            min_c, max_c = max(c0, (m3-m1)/(2*D)+1), c1-1
            min_r, max_r = max(r0, (m3-m2)/(2*D)+1), r1-1
            if (min_r <= max_r) and (min_c <= max_c) and (min_anti <= max_anti):
                # b3 = min(b + D*(r-(r1-1)+ c-(c1-1))) = min(b+D*(r+c)) + D*(-max_r-max_c)
                result = (result + f(m3+D*(-max_anti), max_r-min_r, max_c-min_c, max_anti-min_anti, D))%MOD
    return result

MOD = 10**9+7
DIRECTIONS = [lambda x: x, lambda x:reversed(x)]
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, slate_modern())