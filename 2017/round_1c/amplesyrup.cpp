//
// Created by khw on 21. 3. 3..
//

/*
 * The kitchen at the Infinite House of Pancakes has just received an order for a stack of K pancakes!
 * The chef currently has N pancakes available, where N ≥ K. Each pancake is a cylinder, and different pancakes may have different radii and heights.
 *
 * As the sous-chef, you must choose K out of the N available pancakes,
 * discard the others, and arrange those K pancakes in a stack on a plate as follows.
 * First, take the pancake that has the largest radius, and lay it on the plate on one of its circular faces.
 * (If multiple pancakes have the same radius, you can use any of them.)
 * Then, take the remaining pancake with the next largest radius and lay it on top of that pancake, and so on,
 * until all K pancakes are in the stack and the centers of the circular faces are aligned in a line perpendicular to the plate, as illustrated by this example:
 *
 * You know that there is only one thing your diners love as much as they love pancakes: syrup!
 * It is best to maximize the total amount of exposed pancake surface area in the stack,
 * since more exposed pancake surface area means more places to pour on delicious syrup.
 * Any part of a pancake that is not touching part of another pancake or the plate is considered to be exposed.
 *
 * If you choose the K pancakes optimally, what is the largest total exposed pancake surface area you can achieve?
 */

/*
 * The first line of the input gives the number of test cases, T.
 * T test cases follow. Each begins with one line with two integers N and K:
 * the total number of available pancakes, and the size of the stack that the diner has ordered.
 * Then, N more lines follow. Each contains two integers Ri and Hi: the radius and height of the i-th pancake, in millimeters.
 */

/*
 * For each test case, output one line containing Case #x: y,
 * where x is the test case number (starting from 1) and y is the maximum possible total exposed pancake surface area,
 * in millimeters squared. y will be considered correct if it is within an absolute or relative error of 10-6 of the correct answer.
 * See the FAQ for an explanation of what that means, and what formats of real numbers we accept.
 */

/*
 * Time limit: 20 seconds per test set.
 * Memory limit: 1 GB.
 * 1 ≤ T ≤ 100.
 * 1 ≤ K ≤ N.
 * 1 ≤ Ri ≤ 10^6, for all i.
 * 1 ≤ Hi ≤ 10^6, for all i.
 * Small dataset (Test Set 1 - Visible)
 * 1 ≤ N ≤ 10.
 *
 * Large dataset (Test Set 2 - Hidden)
 * 1 ≤ N ≤ 1000.
 */

/*
 * Input
    4
    2 1
    100 20
    200 10
    2 2
    100 20
    200 10
    3 2
    100 10
    100 10
    100 10
    4 2
    9 3
    7 1
    10 1
    8 4
 */

/*
 * Output
    Case #1: 138230.076757951
    Case #2: 150796.447372310
    Case #3: 43982.297150257
    Case #4: 625.176938064
 */

/*
 * In sample case #1,
 * the "stack" consists only of one pancake.
 * A stack of just the first pancake would have an exposed area of π × R_0^2 + 2 × π * R_0 × H_0 = 14000π mm2.
 * A stack of just the second pancake would have an exposed area of 44000π mm2. So it is better to use the second pancake.
 *
 * In sample case #2, we can use both of the same pancakes from case #1.
 * The first pancake contributes its top area and its side, for a total of 14000π mm2.
 * The second pancake contributes some of its top area (the part not covered by the first pancake) and its side,
 * for a total of 34000π mm2. The combined exposed surface area is 48000π mm2.
 *
 * In sample case #3, all of the pancakes have radius 100 and height 10.
 * If we stack two of these together, we effectively have a single new cylinder of radius 100 and height 20.
 * The exposed surface area is 14000π mm2.
 *
 * In sample case #4, the optimal stack uses the pancakes with radii of 8 and 9.
 */

/*
 * code from https://github.com/ruippeixotog/google-code-jam-2017/blob/master/round1c/ample-syrup.cpp
 */

#include <algorithm>
#include <cmath>
#include <cstdio>
#include <cstring>
#include <functional>

#define MAXN 1000

using namespace std;

typedef long double ld;

pair<int, int> rh[MAXN];

ld dp[MAXN + 1][MAXN];

int main() {
    int t; scanf("%d\n", &t);
    for(int tc = 1; tc <= t; tc++) {
        int n, k; scanf("%d %d\n", &n, &k);
        for(int i = 0; i < n; i++)
            scanf("%d %d\n", &rh[i].first, &rh[i].second);

        sort(rh, rh + n, greater<pair<int, int>>());
        memset(dp, 0, sizeof(dp));

        for(int i = 0; i < n; i++) {
            memcpy(dp[i + 1], dp[i], sizeof(dp[i]));
            dp[i + 1][1] = max(
                    dp[i + 1][1],
                    M_PI * pow((ld) rh[i].first, 2) +
                    2 * M_PI * (ld) rh[i].first * rh[i].second);

            for(int j = 1; j < k; j++) {
                dp[i + 1][j + 1] = max(
                        dp[i + 1][j + 1],
                        dp[i][j] + 2 * M_PI * rh[i].first * rh[i].second);
            }
        }
        printf("Case #%d: %.9Lf\n", tc, dp[n][k]);
    }
    return 0;
}