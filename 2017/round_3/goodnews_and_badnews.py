"""
You would like to get your F friends to share some news.
You know your friends well, so you know which of your friends can talk to which of your other friends.
There are P such one-way relationships, each of which is an ordered pair (Ai, Bi) that means that friend Ai can talk to friend Bi.
It does not imply that friend Bi can talk to friend Ai; however, another of the ordered pairs might make that true.

For every such existing ordered pair (Ai, Bi), you want friend Ai to deliver some news to friend Bi.
In each case, this news will be represented by an integer value;
the magnitude of the news is given by the absolute value, and the type of news (good or bad) is given by the sign.
The integer cannot be 0 (or else there would be no news!), and its absolute value cannot be larger than F2 (or else the news would be just too exciting!).
These integer values may be different for different ordered pairs.

Because you are considerate of your friends' feelings, for each friend,
the sum of the values of all news given by that friend must equal the sum of values of all news given to that friend.
If no news is given by a friend, that sum is considered to be 0; if no news is given to a friend, that sum is considered to be 0.

Can you find a set of news values for your friends to communicate such that these rules are obeyed, or determine that it is impossible?
"""

"""
The first line of the input gives the number of test cases, T. 
T test cases follow. Each begins with one line with two integers F and P: the number of friends, and the number of different ordered pairs of friends. 
Then, P more lines follow; the i-th of these lines has two different integers Ai and Bi representing that friend Ai can talk to friend Bi. Friends are numbered from 1 to F.
"""

"""
For each test case, output one line containing Case #x: y, 
where x is the test case number (starting from 1) and y is either IMPOSSIBLE if there is no arrangement satisfying the rules above, or, 
if there is such an arrangement, P integers, each of which is nonzero and lies inside [-F2, F2]. 
The i-th of those integers corresponds to the i-th ordered pair from the input, 
and represents the news value that the first friend in the ordered pair will communicate to the second. 
The full set of values must satisfy the conditions in the problem statement.

If there are multiple possible answers, you may output any of them.
"""

"""
Memory limit: 1 GB.
1 ≤ T ≤ 100.
1 ≤ Ai ≤ F, for all i.
1 ≤ Bi ≤ F, for all i.
Ai ≠ Bi, for all i. (A friend does not self-communicate.)
(Ai, Bi) ≠ (Aj, Bj), for all i ≠ j. (No pair of friends is repeated within a test case in the same order.)
Small dataset (Test Set 1 - Visible)
Time limit: 20 seconds.
2 ≤ F ≤ 4.
1 ≤ P ≤ 12.
Large dataset (Test Set 2 - Hidden)
Time limit: 40 seconds.
2 ≤ F ≤ 1000.
1 ≤ P ≤ 2000.
"""

"""
Input
5
2 2
1 2
2 1
2 1
1 2
4 3
1 2
2 3
3 1
3 4
1 2
2 3
3 1
2 1
3 3
1 3
2 3
1 2
"""

"""
Output
Case #1: 1 1
Case #2: IMPOSSIBLE
Case #3: -1 -1 -1
Case #4: 4 -4 -4 8
Case #5: -1 1 1
"""

"""
The sample output shows one possible set of valid answers. Other valid answers are possible.

In Sample Case #1, one acceptable arrangement is to have friend 1 deliver news with value 1 to friend 2, and vice versa.

In Sample Case #2, whatever value of news friend 1 gives to friend 2, it must be nonzero. 
So, the sum of news values given to friend 2 is not equal to zero. However, friend 2 cannot give any news and so that value is 0. 
Therefore, the sums of given and received news for friend 2 cannot match, and the case is IMPOSSIBLE.

In Sample Case #3, each of friends 1, 2, and 3 can deliver news with value -1 to the one other friend they can talk to — an unfortunate circle of bad news! 
Note that there is a friend 4 who does not give or receive any news; this still obeys the rules.

In Sample Case #4, note that -5 5 5 -10 would not have been an acceptable answer, because there are 3 friends, and |-10| > 32.

In Sample Case #5, note that the case cannot be solved without using at least one negative value.
"""

# code from https://github.com/kamyu104/GoogleCodeJam-2017/blob/master/Round%203/good_news_and_bad_news.py

# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2017 Round 3 - Problem B. Good News and Bad News
# https://codingcompetitions.withgoogle.com/codejam/round/0000000000201902/0000000000201846
#
# Time:  O(P^2)
# Space: O(P)
#

from sys import setrecursionlimit
from collections import defaultdict
from itertools import imap

def dfs(G, prev_id, u, stk, lookup, result):
    for i, v in G[u]:
        if ~i == prev_id:
            continue
        if v not in lookup:
            lookup[v] = len(lookup)+1
            stk.append((i, v))
            dfs(G, i, v, stk, lookup, result)
            stk.pop()
            continue
        if lookup[v] >= lookup[u]:
            continue
        result[i if i >= 0 else ~i] += 1 if i >= 0 else -1
        for j, t in reversed(stk):
            if t == v:
                break
            result[j if j >= 0 else ~j] += 1 if j >= 0 else -1

def good_news_and_bad_news():
    F, P = map(int, raw_input().strip().split())
    G = defaultdict(list)
    for i in xrange(P):
        A, B = map(int, raw_input().strip().split())
        G[A].append((i, B))
        G[B].append((~i, A))
    result, lookup, stk = [0]*P, {}, []
    for u in G.iterkeys():
        if u in lookup:
            continue
        lookup[u] = len(lookup)+1
        stk.append((None, u))
        dfs(G, None, u, stk, lookup, result)
        stk.pop()
    return " ".join(imap(str, result)) if all(x for x in result) else "IMPOSSIBLE"

BASE = 3
MAX_F = 1000
setrecursionlimit(BASE+(1+MAX_F))
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, good_news_and_bad_news())