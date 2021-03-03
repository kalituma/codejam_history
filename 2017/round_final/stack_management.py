"""
You are playing a solitaire game in which there are N stacks of face-up cards, each of which initially has C cards.
Each card has a value and a suit, and no two cards in the game have the same value/suit combination.

In one move, you can do one of the following things:

1. If there are two or more cards with the same suit that are on top of different stacks,
you may remove the one of those cards with the smallest value from the game. (Whenever you remove the last card from a stack, the stack is still there — it just becomes empty.)
2. If there is an empty stack, you may take a card from the top of any one of the non-empty stacks and place it on top of (i.e., as the only card in) that empty stack.
You win the game if you can make a sequence of moves such that eventually,
each stack contains at most one card. Given a starting arrangement, determine whether it is possible to win the game.
"""

"""
The first line of the input gives the number P of premade stacks that will be used in the test cases. 
Then, P lines follow. The i-th of those lines begins with an integer Ci, 
the number of cards in the i-th of those premade stacks, and continues with Ci ordered pairs of integers. 
The j-th of these ordered pairs has two integers Vij and Sij, representing the value and suit of the j-th card from the top in the i-th premade stack.

Then, there is another line with one integer T, the number of test cases. T test cases follow. 
Each case begins with one line with two integers N and C: the number of stacks, and the number of cards in each of those stacks. 
Then, there is one line with N integers Pi, representing the indexes (starting from 0) of the test case's set of premade stacks.
"""

"""
For each test case, output one line containing Case #x: y, 
where x is the test case number (starting from 1) and y is POSSIBLE if it is possible to win the game, or IMPOSSIBLE otherwise.
"""

"""
Time limit: 20 seconds per test set.
Memory limit: 1 GB.
1 ≤ T ≤ 100.
2 ≤ P ≤ 60000.
0 ≤ Pi < P, for all i.
The Pi-th premade stack has exactly C cards.
No two cards in a test case have the same value/suit combination.
Small dataset (Test Set 1 - Visible)
2 ≤ N ≤ 4.
2 ≤ Ci ≤ 13, for all i.
2 ≤ C ≤ 13.
1 ≤ Vij ≤ 13, for all i and j.
1 ≤ Sij ≤ 4, for all i and j.
Large dataset (Test Set 2 - Hidden)
2 ≤ N ≤ 50000.
2 ≤ Ci ≤ 50000, for all i.
2 ≤ C ≤ 50000.
4 ≤ N × C ≤ 105.
1 ≤ Vij ≤ 50000, for all i and j.
1 ≤ Sij ≤ 50000, for all i and j.
"""

"""
Input
5
2 7 2 7 1
2 6 4 7 4
2 3 2 6 2
2 4 2 10 2
2 5 4 7 3
2
2 2
0 2
3 2
4 1 3
"""

"""
Output
Case #1: POSSIBLE
Case #2: IMPOSSIBLE
"""

"""
In sample case #1, there are two stacks, each of which has two cards. 
The first stack has a 7 of suit 2 on top and a 7 of suit 1 below that. The second stack has a 3 of suit 2 on top and a 6 of suit 2 below that.

It is possible to win the game as follows:

Remove the 3 of suit 2 from the second stack.
Remove the 6 of suit 2 from the second stack. This makes the second stack empty.
Move the 7 of suit 2 to the second stack. Then the win condition is satisfied: all stacks have at most one card.
In sample case #2, there are three stacks, each of which has two cards. 
It is not possible to win the game in this case; the only possible move is to remove the 5 of suit 4 on top of the third stack, and this does not open up any new moves.
"""
# code from https://github.com/kamyu104/GoogleCodeJam-2017/blob/master/World%20Finals/stack_management.py

# Copyright (c) 2020 kamyu. All rights reserved.
#
# Google Code Jam 2017 Word Finals - Problem E. Stack Management
# https://codingcompetitions.withgoogle.com/codejam/round/0000000000201909/00000000002017fd
#
# Time:  O((N * C) * logN)
# Space: O(N * C)
#

from collections import defaultdict
from heapq import heappush, heappop

def preprocess(piles):  # Time: O((N * C) * logN), Space: O(N)
    min_heaps, stk = defaultdict(list), []
    for i, pile in enumerate(piles):
        value, suite = pile[-1]
        heappush(min_heaps[suite], (value, i))
        if len(min_heaps[suite]) > 1:
            stk.append(suite)
    while stk:
        suite = stk.pop()
        _, i = heappop(min_heaps[suite])
        piles[i].pop()
        if not piles[i]:
            continue
        value, suite = piles[i][-1]
        heappush(min_heaps[suite], (value, i))
        if len(min_heaps[suite]) > 1:
            stk.append(suite)

def dfs(adj, source, targets):  # Time: O(N), Space: O(N)
    stk, lookup = [source], set([source])
    while stk:
        u = stk.pop()
        if u in targets:
            return True
        if u not in adj:
            continue
        for v in adj[u]:
            if v in lookup:
                continue
            lookup.add(v)
            stk.append(v)
    return False

def stack_management():
    N, C = map(int, raw_input().strip().split())
    piles = map(lambda x: PILES[x][:], map(int, raw_input().strip().split()))
    preprocess(piles)  # remove all cards if possible
    for pile in piles:
        if len(pile) > 1:
            break
    else:
        return "POSSIBLE"
    suite_to_max_two_values = defaultdict(list)
    for i, pile in enumerate(piles):  # Time: O((N * C) * log2), Space: O(N)
        for idx, (value, suite) in enumerate(pile):
            heappush(suite_to_max_two_values[suite], value)
            if len(suite_to_max_two_values[suite]) == 3:
                heappop(suite_to_max_two_values[suite])
            elif len(suite_to_max_two_values) > len(piles):
                return "IMPOSSIBLE"  # early return
    if len(suite_to_max_two_values) < len(piles):
        return "POSSIBLE"
    for pile in piles:
        if not pile:
            break
    else:
        return "IMPOSSIBLE"  # no empty stack

    vertices = {pile[0][1] for pile in piles if pile and pile[0][0] == suite_to_max_two_values[pile[0][1]][-1]}  # Time: O(N)
    sources, targets, adj = [], set(), defaultdict(list)
    for i, pile in enumerate(piles):  # Time: O(N * C)
        if not pile:
            continue
        ace_value, ace_suite = pile[0]
        if ace_value != suite_to_max_two_values[ace_suite][-1]:
            continue
        if len(suite_to_max_two_values[ace_suite]) == 1:
            sources.append(ace_suite)
        for value, suite in pile:
            if suite == ace_suite:
                continue
            if value == suite_to_max_two_values[suite][-1]:
                targets.add(ace_suite)
            elif suite in vertices and len(suite_to_max_two_values[suite]) == 2 and value == suite_to_max_two_values[suite][-2]:
                adj[ace_suite].append(suite)
    for source in sources:  # total - Time: O(N), Space: O(N)
        if dfs(adj, source, targets):
            break
    else:
        return "IMPOSSIBLE"
    return "POSSIBLE"

P = input()
PILES = []
for _ in xrange(P):
    V_S = map(int, raw_input().strip().split())
    PILES.append([(V_S[2*i+1], V_S[2*i+2]) for i in reversed(xrange((len(V_S)-1)//2))])
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, stack_management())