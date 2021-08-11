# from https://github.com/kamyu104/GoogleCodeJam-2019/blob/master/Qualification%20Round/dat-bae.py
# Copyright (c) 2019 kamyu. All rights reserved.
#
# Google Code Jam 2019 Qualification Round - Problem D. Dat Bae
# https://codingcompetitions.withgoogle.com/codejam/round/0000000000051705/00000000000881de
#
# Time:  O(NlogB)
# Space: O(N)
#

import sys

def dat_bae():
    N, B, F = map(int, raw_input().strip().split())

    # find the smallest Q s.t. 2**Q > B
    # p.s. if 2**Q <= B, when the whole 2**Q block is missing,
    #      we cannot tell which block is lost
    Q = B.bit_length()  # floor(log2(B))+1
    assert(2**Q > B and Q <= F)

    idxs = [0]*(N-B)
    for j in xrange(Q):  # floor(log2(B)) + 1 times
        query = [((i%(2**Q))>>j)&1 for i in xrange(N)]
        print "".join(map(str, query))
        sys.stdout.flush()
        response = map(int, raw_input())
        for i in xrange(len(response)):
            idxs[i] |= (response[i])<<j

    result = []
    i, pow_Q_of_2 = 0, 2**Q
    for idx in xrange(N):
        if idxs[i] != (idx % pow_Q_of_2) :
            result.append(str(idx))
        elif i+1 < len(idxs):
            i += 1

    print " ".join(result)
    sys.stdout.flush()
    verdict = input()
    if verdict == -1:  # error
        exit()

for case in xrange(input()):
    dat_bae()