"""
Intrepid globetrotter K, who may or may not be the author of this problem, has been traveling a lot lately.
On one of her recent trips, she traveled from San Francisco to Frankfurt to Johannesburg to Abu Dhabi to Singapore to Tokyo and back to San Francisco.
On this trip, she circumnavigated the Earth by traveling along a closed path that touches every meridian.
In other words, for every possible longitude, there is at least one point along this path at that longitude.

K is not sure that this trip qualifies as being super awesome,
however, since it would also be possible to circumnavigate the Earth by flying to the North Pole and then walking around it,
which does not seem to be particularly difficult (other than the part about flying to the North Pole).
So she has decided to come up with a more generalized definition of circumnavigation.
The new concept is called omnicircumnavigation — a closed path around the Earth (which we assume to be a sphere)
that is a circumnavigation regardless of where one places the poles.
In other words, an omnicircumnavigation is a closed path on the surface of a sphere that touches every possible hemisphere.
(Touching the edge of a hemisphere is sufficient.)
Equivalently, an omnicircumnavigation intersects every possible great circle — a circle of greatest possible diameter on the surface of a sphere.

You are given a sequence of N points on a sphere of radius 1.
You need to check whether a path connecting those points in order is an omnicircumnavigation.
The path is formed by connecting each pair of successive points along the shortest possible surface route,
and connecting the last point to the first one in the same way. No two successive points
(including the pair of the last point and the first point) are collinear with the origin.
(That is, they are not antipodes — polar opposites — and they do not represent the same point on the surface of the sphere.)
"""

"""
The first line of the input gives the number of test cases, T. 
T test cases follow. Each begins with one line containing N, the number of cities visited by K. 
The next N lines contain three integers Xi, Yi and Zi each. 
The i-th point in the list is given by the coordinates (Xi / sqrt(Xi^2 + Yi^2 + Zi^2), Yi / sqrt(Xi^2 + Yi^2 + Zi^2), Zi / sqrt(Xi^2 + Yi^2 + Zi^2)).
"""

"""
For each test case, output one line containing Case #x: y, 
where x is the case number and y is either YES or NO depending on whether the route is an omnicircumnavigation or not.
"""

"""
Memory limit: 1 GB.
1 ≤ T ≤ 200.
-10^6 ≤ Xi ≤ 10^6, for all i.
-10^6 ≤ Yi ≤ 10^6, for all i.
-10^6 ≤ Zi ≤ 10^6, for all i.
At least one of the values in (Xi, Yi, Zi) ≠ 0, for all i. For all i, j such that (i + 1 = j) or (i = N - 1 and j = 0), 
neither of (Xi, Yi, Zi) and (Xj, Yj, Zj) is an integer multiple of the other. 
(No two successive points, including the last and first, are antipodes or represent the same point on the sphere.)
Small dataset (Test Set 1 - Visible)
Time limit: 60 seconds.
3 ≤ N ≤ 50.
Large dataset (Test Set 2 - Hidden)
Time limit: 300 seconds.
3 ≤ N ≤ 5000.
"""

"""
Input
4
3
1 0 0
0 1 0
0 0 1
8
5 5 5
5 -5 5
-5 -5 5
-5 5 5
-5 5 -5
-5 -5 -5
5 -5 -5
5 5 -5
3
1 0 0
-1 1 0
-1 -1 0
5
1 0 0
-1 1 0
2 0 0
-2 2 0
-1 -1 0
"""

"""
Output
Case #1: NO
Case #2: YES
Case #3: YES
Case #4: YES
"""

"""
In Sample Case #1, the three points are the surface points of one octant of the sphere, and the path traces out that octant. 
There are many hemispheres that do not overlap that path at all.

In Sample Case #2, the eight points are the corners of a cube inscribed in the sphere; 
any hemisphere will contain at least some parts of that path. Note that dividing all values by 5 would produce an equivalent case (with the same set of points).

In Sample Case #3, the path is itself a great circle, and so every other great circle must intersect it somewhere.

Sample Case #4 uses the same three points as in Sample Case #3, except that the first two points are visited twice each. 
Note that a case may include multiple representations of the same point, and that a path may include the same points or connections more than once.
"""

# code from https://github.com/kamyu104/GoogleCodeJam-2017/blob/master/World%20Finals/omnicircumnavigation.py

# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2017 Word Finals - Problem D. Omnicircumnavigation
# https://codingcompetitions.withgoogle.com/codejam/round/0000000000201909/000000000020190a
#
# Time:  O(N^2), pass in PyPy2 but Python2
# Space: O(N)
#

def inner_product(a, b):
    return a[0]*b[0]+a[1]*b[1]+a[2]*b[2]

def outer_product(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])

def omnicircumnavigation():
    points = [tuple(map(int, raw_input().strip().split())) for _ in xrange(input())]
    p = []
    for i in xrange(len(points)):
        for j in xrange(i+1, len(points)):
            if outer_product(points[i], points[j]) == (0, 0, 0):  # colinear
                if inner_product(points[i], points[j]) < 0:  # angle between line [(0, 0), points[i]] and line [(0, 0), points[j]] is 180 degrees
                    return "YES"
                else:  # duplicated
                    break
        else:
            p.append(points[i])
    for i in xrange(len(p)):
        k = -1
        for j in xrange(len(p)):
            if j in (i, k):
                continue
            # rotate a plane with [(0, 0), p[i]] as the axis to cover each point,
            # if the points are inside the semi-sphere,
            # there should exist two plane boundaries and the angle between them is less than 180 degrees and all points are inside them
            if k == -1 or inner_product(outer_product(p[i], p[k]), p[j]) > 0:
                k = j  # find the leftmost point where the left plane boundary is
        for j in xrange(len(p)):
            if j in (i, k):
                continue
            coplanar = inner_product(outer_product(p[i], p[k]), p[j])
            if coplanar == 0:  # coplanar
                if inner_product(outer_product(p[i], p[k]), outer_product(p[i], p[j])) < 0:  # angle between plane [(0, 0), p[i], p[k]] and plane [(0, 0), p[i], p[k]] is 180 degrees
                    break
            elif coplanar > 0:  # the left plane boundary doesn't exist, thus the points are not inside the semisphere
                break
        else:
            return "NO"  # all points are inside the semisphere
    return "YES"

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, omnicircumnavigation())