//
// Created by khw on 21. 3. 3..
//


/*
 * Cameron and Jamie are longtime life partners and have recently become parents!
 * Being in charge of a baby, exciting as it is, is not without challenges.
 * Given that both parents have a scientific mind, they have decided to take a scientific approach to baby care.
 *
 * Cameron and Jamie are establishing a daily routine and need to decide who will be the main person in charge of the baby at each given time.
 * They have been equal partners their whole relationship, and they do not want to stop now,
 * so they decided that each of them will be in charge for exactly 12 hours (720 minutes) per day.
 *
 * Cameron and Jamie have other activities that they either need or want to do on their own.
 * Cameron has AC of these and Jamie has AJ. These activities always take place at the same times each day.
 * None of Cameron's activities overlap with Jamie's activities, so at least one of the parents will always be free to take care of the baby.
 *
 * Cameron and Jamie want to come up with a daily baby care schedule such that:
 *
 * Scheduled baby time must not interfere with a scheduled activity. That is, during Cameron's activities, Jamie has to be in charge of the baby, and vice versa.
 * Each of Cameron and Jamie must have exactly 720 minutes assigned to them.
 * The number of exchanges — that is, the number of times the person in charge of the baby changes from one partner to the other — must be as small as possible.
 * For example, suppose that Jamie and Cameron have a single activity each: Jamie has a morning activity from 9 am to 10 am,
 * and Cameron has an afternoon activity from 2 pm to 3 pm.
 * One possible but suboptimal schedule would be for Jamie to take care of the baby from midnight to 6 am and from noon to 6 pm,
 * and for Cameron to take care of the baby from 6 am to noon and 6 pm to midnight. That fulfills the first two conditions,
 * and requires a total of 4 exchanges, which happen at midnight, 6 am, noon and 6 pm. If there is an exchange happening at midnight,
 * it is counted exactly once, not zero or two times.
 *
 * A better option would be for Cameron to take care of the baby from midnight to noon,
 * and Jamie to take care of the baby from noon to midnight. This schedule also fulfills the first two conditions,
 * but it uses only 2 exchanges, which is the minimum possible.
 *
 * Given Cameron's and Jamie's lists of activities, and the restrictions above, what is the minimum possible number of exchanges in a daily schedule?
 */

/*
 * The first line of the input gives the number of test cases, T.
 * T test cases follow. Each test case starts with a line containing two integers AC and AJ,
 * the number of activities that Cameron and Jamie have, respectively. Then, AC + AJ lines follow.
 * The first AC of these lines contain two integers Ci and Di each.
 * The i-th of Cameron's activities starts exactly Ci minutes after the start of the day at midnight
 * and ends exactly Di minutes after the start of the day at midnight (taking exactly Di - Ci minutes).
 * The last AJ of these lines contain two integers Ji and Ki each, representing the starting and ending time of one of Jamie's activities,
 * in minutes counting from the start of the day at midnight (same format as Cameron's).
 * No activity spans two days, and no two activities overlap (except that one might end exactly as another starts, but an exchange can still occur at that time).
 */

/*
 * For each test case, output one line containing Case #x: y,
 * where x is the test case number (starting from 1) and y the minimum possible number of exchanges, as described in the statement.
 */

/*
 * Time limit: 20 seconds per test set.
 * Memory limit: 1 GB.
 * 1 ≤ T ≤ 100.
 * 0 ≤ Ci < Di ≤ 24 × 60, for all i.
 * 0 ≤ Ji < Ki ≤ 24 × 60, for all i.
 *
 * Any two of the intervals of {[Ci, Di) for all i} union {[Ji, Ki) for all i} have an empty intersection.
 * (The intervals are closed on the left and open on the right, which ensures that two exactly consecutive intervals have nothing in between but do not overlap.)
 * sum of {Di - Ci for all i} ≤ 720.
 * sum of {Ki - Ji for all i} ≤ 720.
 * Small dataset (Test Set 1 - Visible)
 * 0 ≤ AC ≤ 2.
 * 0 ≤ AJ ≤ 2.
 * 1 ≤ AC + AJ ≤ 2.
 * Large dataset (Test Set 2 - Hidden)
 * 0 ≤ AC ≤ 100.
 * 0 ≤ AJ ≤ 100.
 * 1 ≤ AC + AJ ≤ 200.
 */

/*
 * Input
    5
    1 1
    540 600
    840 900
    2 0
    900 1260
    180 540
    1 1
    1439 1440
    0 1
    2 2
    0 1
    1439 1440
    1438 1439
    1 2
    3 4
    0 10
    1420 1440
    90 100
    550 600
    900 950
    100 150
    1050 1400
 */

/*
 * Output
    Case #1: 2
    Case #2: 4
    Case #3: 2
    Case #4: 4
    Case #5: 6
 */

/*
 * Note that Cases #4 and #5 would not appear in the Small dataset.
 *
 * Case #1 is the one described in the problem statement.
 *
 * In Case #2, Jamie must cover for all of Cameron's activity time, and then Cameron must cover all the remaining time. This schedule entails four exchanges.
 *
 * In Case #3, there is an exchange at midnight, from Cameron to Jamie.
 * No matter how the parents divide up the remaining 1438 non-activity minutes of the day,
 * there must be at least one exchange from Jamie to Cameron, and there is no reason to add more exchanges than that.
 *
 * In Case #4, note that back-to-back activities can exist for the same partner or different partners.
 * There is no exchange at midnight because Cameron has activities both right before and right after that time.
 * However, the schedule needs to add some time for Cameron in between Jamie's activities,
 * requiring a total of 4 exchanges. Notice that it is optimal to add a single interval for Cameron of length 718 somewhere between minutes 2 and 1438,
 * but the exact position of that added interval does not impact the number of exchanges, so there are multiple optimal schedules.
 *
 * In Case #5, a possible optimal schedule is to assign Cameron to the intervals (in minutes) 100-200, 500-620, and 900-1400.
 */
/*
 * code from https://github.com/ruippeixotog/google-code-jam-2017/blob/master/round1c/parenting-partnering.cpp
 */
#include <algorithm>
#include <cstdio>
#include <cstring>
#include <tuple>

#define MAXAC 100
#define MAXAJ 100

using namespace std;

tuple<int, int, int> act[MAXAC + MAXAJ + 2];

int dp[MAXAC + MAXAJ + 2][2][721];

int main() {
    int t; scanf("%d\n", &t);
    for(int tc = 1; tc <= t; tc++) {
        int ac, aj; scanf("%d %d\n", &ac, &aj);
        for(int i = 0; i < ac; i++) {
            get<2>(act[i]) = 0;
            scanf("%d %d\n", &get<0>(act[i]), &get<1>(act[i]));
        }
        for(int i = 0; i < aj; i++) {
            get<2>(act[ac + i]) = 1;
            scanf("%d %d\n", &get<0>(act[ac + i]), &get<1>(act[ac + i]));
        }

        act[ac + aj] = {0, 0, -1};
        act[ac + aj + 1] = {1440, 1440, -1};
        sort(act, act + ac + aj + 2);

        memset(dp, 0x3f, sizeof(dp));
        dp[0][0][0] = dp[0][1][0] = 0;

        for(int i = 1; i < ac + aj + 2; i++) {
            for(int st = 0; st < 2; st++) {
                int c0, d0, c1, d1, isJ0, isJ1;
                tie(c0, d0, isJ0) = act[i - 1];
                tie(c1, d1, isJ1) = act[i];
                if(isJ0 == -1) isJ0 = st;
                if(isJ1 == -1) isJ1 = st;

                int task = isJ1 ? d1 - c1 : 0;
                for(int mc = 0; mc <= 720; mc++) {
                    for(int mc1 = 0; mc1 <= c1 - d0 && mc + mc1 + task <= 720; mc1++) {
                        int exchanges = isJ0 != isJ1 ? 1 :
                                        isJ0 && isJ1 ? (mc1 == c1 - d0 ? 0 : 2) :
                                        mc1 == 0 ? 0 : 2;

                        dp[i][st][mc + mc1 + task] = min(
                                dp[i][st][mc + mc1 + task], dp[i - 1][st][mc] + exchanges);
                    }
                }
            }
        }

        int res = min(dp[ac + aj + 1][0][720], dp[ac + aj + 1][1][720]);
        printf("Case #%d: %d\n", tc, res);
    }
    return 0;
}