#from https://github.com/kamyu104/GoogleCodeJam-2019/blob/master/Round%203/napkin-folding.py
# Copyright (c) 2019 kamyu. All rights reserved.
#
# Google Code Jam 2019 Round C - Problem D. Napkin Folding
# https://codingcompetitions.withgoogle.com/codejam/round/0000000000051707/0000000000159170
#
# Time:  O(N^2 * K^2), much better than official analysis
# Space: O(N * K^2)
#

def gcd(a, b):  # Time: O((logn)^2)
    while b:
        a, b = b, a % b
    return a

def advance_polygon_area(p1, p2):
    return p1[0]*p2[1]-p1[1]*p2[0]

def delta_area(a, b, c):
    return advance_polygon_area(a, b) + \
           advance_polygon_area(b, c) - \
           advance_polygon_area(a, c)

def polygon_area(polygon):
    area = 0
    for i in xrange(len(polygon)):
        area += advance_polygon_area(polygon[i-1], polygon[i])
    return area  # in this problem, we don't divide the area by 2 and keep it a signed area

def reflect(P, A, B):  # return Q which is the reflection of P over line (A, B)
    a, b, c = A[1]-B[1], -(A[0]-B[0]), (A[1]-B[1])*(-A[0])-(A[0]-B[0])*(-A[1])
    if -2 * a * (a * P[0] + b * P[1] + c) % (a * a + b * b) or \
            -2 * b * (a * P[0] + b * P[1] + c) % (a * a + b * b):
        return None  # in this problem, Q should be integers too, otherwise it won't be on polygon
    return (-2 * a * (a * P[0] + b * P[1] + c) // (a * a + b * b) + P[0],
            -2 * b * (a * P[0] + b * P[1] + c) // (a * a + b * b) + P[1])

def find_candidates(K, lcm):
    fractions_set = set()
    # 1. a folding point with rational coordinates only has 1 or 3 folding segments (see appendix in official analysis),
    #    there must be a vertical folding segment, so folding points on an edge would equaully split the edge
    # 2. there may be 1 ~ K-1 non-vertex folding points on an edge
    for y in xrange(2, K+1):
        for x in xrange(1, y):
            common = gcd(x, y)
            fractions_set.add((x//common, y//common))
    candidates = list(fractions_set)
    candidates.sort(key=lambda x : lcm*x[0]//x[1])  # applying binary search should be sorted (full search doesn't matter)
    return candidates

def split(A, B, candidates):
    endpoints = []
    for c in candidates:
        endpoints.append((A[0]+(B[0]-A[0])*c[0]//c[1],
                          A[1]+(B[1]-A[1])*c[0]//c[1]))
    return endpoints

def find_possible_endpoints(polygon, candidates):
    endpoints = []
    endpoints.append(polygon[0])
    for i in xrange(1, len(polygon)):
        endpoints.extend(split(polygon[i-1], polygon[i], candidates))
        endpoints.append(polygon[i])
    endpoints.extend(split(polygon[-1], polygon[0], candidates))
    return endpoints

def edge_num(begin, end, length, C):
    if end < begin:
        end += length
    begin = begin//C
    end = (end-1)//C+1
    return (end-begin)+1

def binary_search(begin, end, C, K, endpoints, total_area, area):
    left, right = end+1, end//C*C+C
    while left <= right:
        mid = left + (right-left)//2
        curr_area = area + delta_area(endpoints[end], endpoints[mid%len(endpoints)], endpoints[begin])
        if total_area == K * curr_area:
            return mid%len(endpoints)
        elif total_area > K * curr_area:
            right = mid-1
        else:
            left = mid+1
    return -1

def find_possible_segments(polygon, K, endpoints):
    C = len(endpoints)//len(polygon)  # count of polygon and non-polygon vertex on an edge
    total_area = polygon_area(polygon)

    begin, end = 0, 0
    area = 0
    while K*edge_num(begin, end, len(endpoints), C) < len(polygon) + 2*(K-1):
        # at most N/K + 2 times becuase a valid pattern forms at least N + 2*(K-1) endpoints
        end = (end+C)%len(endpoints)
        area += delta_area(endpoints[(end-C)%len(endpoints)], endpoints[end], endpoints[begin])

    # use sliding window to find the target area
    for begin in xrange(len(endpoints)):  # O(N*K^2) times
        while K*edge_num(begin, end, len(endpoints), C) >= len(polygon) + 2*(K-1):
            # at most 3 times (1 invalid + 2 candidate edges) to restore possible end
            prev_end = end//C*C if end%C != 0 else (end-C)%len(endpoints)
            area -= delta_area(endpoints[prev_end], endpoints[end], endpoints[begin])
            end = prev_end
        while K*(edge_num(begin, (end+1)%len(endpoints), len(endpoints), C)) <= len(polygon) + 2*2*(K-1):
            # at most 3 times (1 invalid + 2 candidate edges)
            # to check because a valid pattern forms at most N + 2*2*(K-1) endpoints
            next_end = binary_search(begin, end, C, K, endpoints, total_area, area)  # O(log(K^2))
            if next_end == -1:
                next_end = (end//C*C+C)%len(endpoints)
            area += delta_area(endpoints[end], endpoints[next_end], endpoints[begin])
            end = next_end
            if K*area == total_area:  # found a candidate end endpoint on the same edge
                yield (begin, end)
                break  # each endpoint has at most one ordered pair to create a line segment,
                # and the nearest one is always the only candidate.
                # because if this pair is invalid, all other pairs with same begin
                # and end with at most one more endpoints are all invalid either.
                # this "break" is an optional optimization (doesn't change time complexity).
        area -= delta_area(endpoints[end], endpoints[begin], endpoints[(begin+1)%len(endpoints)])

def find_pattern(begin, end, length, C):
    pattern = [begin]
    if end < begin:
        end += length
    curr = begin//C*C + C
    while end-curr > 0:
        pattern.append(curr%length)
        curr += C
    pattern.append(end%length)
    return pattern

def normalize(a, b):
    return (a, b) if a <= b else (b, a)

def is_on_polygon_edge(a, b, length, C):
    if a%C == b%C == 0:
        return abs(a-b) in (C, length-C)
    if a%C == 0:
        return a in (b//C*C, (b//C+1)*C%length)
    if b%C == 0:
        return b in (a//C*C, (a//C+1)*C%length)
    return a//C == b//C

def find_valid_segments(polygon, K, endpoints, endpoints_idx, segment):
    C = len(endpoints)//len(polygon)  # count of polygon and non-polygon vertex on an edge

    pattern = find_pattern(segment[0], segment[1], len(endpoints), C)  # Time:  O(N)
    segments = set()
    stk = [(segment, pattern)]  # using queue is also fine (BFS), here we use stack (DFS)
    segments.add(normalize(segment[0], segment[1]))
    while stk:  # Time: O(N + K)
        if len(segments) >= K:  # only invalid pattern makes more than K-1 segments, this check is not necessary
            return None
        segment, pattern = stk.pop()

        new_segments, new_pattern = [], []
        for i in xrange(-1, len(pattern)):
            p = reflect(endpoints[pattern[i]], endpoints[segment[0]], endpoints[segment[1]])
            if not p or p not in endpoints_idx:  # not on polygon
                return None
            p_idx = endpoints_idx[p]
            if new_pattern:
                if not is_on_polygon_edge(new_pattern[-1], p_idx, len(endpoints), C):  # not on polygon edge
                    new_segment = normalize(new_pattern[-1], p_idx)
                    if new_segment not in segments:
                        new_segments.append(new_segment)
            if len(new_pattern) != len(pattern):
                new_pattern.append(p_idx)

        for new_segment in new_segments:
            stk.append((new_segment, new_pattern))
            segments.add(normalize(new_segment[0], new_segment[1]))

    assert(len(segments) == K-1)  # only simple polygon pattern can reach here (no crossed polygon pattern),
    # and it must be the answer
    return segments

def to_fraction(p, lcm):
    common = gcd(p, lcm)
    return "{}/{}".format(p//common, lcm//common)  # restore the numbers

def to_str(p, lcm):
    return "{} {}".format(to_fraction(p[0], lcm), to_fraction(p[1], lcm))

def napkin_folding():
    N, K = map(int, raw_input().strip().split())
    lcm = 1
    for i in xrange(2, K+1):
        lcm = lcm * i // gcd(lcm, i)
    polygon = []
    for _ in xrange(N):  # scale the number by lcm to make sure candidates are also integers
        polygon.append(tuple(map(lambda x: int(x)*lcm, raw_input().strip().split())))

    candidates = find_candidates(K, lcm)  # Time: O(K^2 * logK)
    endpoints = find_possible_endpoints(polygon, candidates)  # Time: O(N * K^2)
    endpoints_idx = {v:k for k, v in enumerate(endpoints)}

    for segment in find_possible_segments(polygon, K, endpoints):  # Time: O(N * K^2 * logK)
        # number of possible segments is at most O(N * K^2)
        segments = find_valid_segments(polygon, K, endpoints, endpoints_idx, segment)  # Time: O(N + K)
        if not segments:
            continue
        result = ["POSSIBLE"]
        for a, b in segments:
            result.append("{} {}".format(to_str(endpoints[a], lcm), to_str(endpoints[b], lcm)))
        return "\n".join(result)
    return "IMPOSSIBLE"

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, napkin_folding())