//
// Created by khw on 21. 3. 3..
//

/*
 * Chemists work with periodic table elements, but here at Code Jam,
 * we have been using our advanced number smasher to study googlements.
 * A googlement is a substance that can be represented by a string of at most nine digits.
 * A googlement of length L must contain only decimal digits in the range 0 through L, inclusive,
 * and it must contain at least one digit greater than 0. Leading zeroes are allowed.
 * For example, 103 and 001 are valid googlements of length 3.
 * 400 (which contains a digit, 4, greater than the length of the googlement, 3) and 000 (which contains no digit greater than 0) are not.
 *
 * Any valid googlement can appear in the world at any time, but it will eventually decay into another googlement in a deterministic way,
 * as follows. For a googlement of length L, count the number of 1s in the googlement (which could be 0) and write down that value,
 * then count the number of 2s in the googlement (which could be 0) and write down that value to the right of the previous value,
 * and so on, until you finally count and write down the number of Ls.
 * The new string generated in this way represents the new googlement,
 * and it will also have length L. It is even possible for a googlement to decay into itself!
 *
 * For example, suppose that the googlement 0414 has just appeared.
 * This has one 1, zero 2s, zero 3s, and two 4s, so it will decay into the googlement 1002.
 * This has one 1, one 2, zero 3s, and zero 4s, so it will decay into 1100, which will decay into 2000,
 * which will decay into 0100, which will decay into 1000, which will continuously decay into itself.
 *
 * You have just observed a googlement G. This googlement might have just appeared in the world,
 * or it might be the result of one or more decay steps. What is the total number of possible googlements it could have been w
 * hen it originally appeared in the world?
 */

/*
 * The first line of the input gives the number of test cases, T.
 * T test cases follow. Each consists of one line with a string G, representing a googlement.
 */

/*
 * For each test case, output one line containing Case #x: y,
 * where x is the test case number (starting from 1)
 * and y is the number of different googlements that the observed googlement could have been when it first appeared in the world.
 */

/*
 * Memory limit: 1 GB.
 * 1 ≤ T ≤ 100.
 * Each digit in G is a decimal digit between 0 and the length of G, inclusive.
 * G contains at least one non-zero digit.
 * Small dataset (Test Set 1 - Visible)
 * Time limit: 20 seconds.
 * 1 ≤ the length of G ≤ 5.
 * Large dataset (Test Set 2 - Hidden)
 * Time limit: 60 seconds.
 * 1 ≤ the length of G ≤ 9.
 */

/*
 * Input
    3
    20
    1
    123
 */

/*
 * Output
    Case #1: 4
    Case #2: 1
    Case #3: 1
 */

/*
 * In sample case #1, the googlement could have originally been 20, or it could have decayed from 11, which could have itself decayed from 12 or 21. Neither of the latter two could have been a product of decay. So there are four possibilities in total.

In sample case #2, the googlement must have originally been 1, which is the only possible googlement of length 1.

In sample case #3, the googlement must have been 123; no other googlement could have decayed into it.
 */

#include <algorithm>
#include <cstdio>

#define MAXN 1000

using namespace std;

typedef long double ld;

pair<int, int> ks[MAXN];

ld ts[MAXN + 1];

int main() {
    int t; scanf("%d\n", &t);
    for(int tc = 1; tc <= t; tc++) {
        int d, n; scanf("%d %d\n", &d, &n);
        for(int i = 0; i < n; i++)
            scanf("%d %d\n", &ks[i].first, &ks[i].second);

        sort(ks, ks + n);
        ts[n] = 0.0;
        for(int i = n - 1; i >= 0; i--) {
            ts[i] = max((d - ks[i].first) / (ld) ks[i].second, ts[i + 1]);
        }
        printf("Case #%d: %.9Lf\n", tc, d / ts[0]);
    }
    return 0;
}