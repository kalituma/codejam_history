//
// Created by khw on 21. 3. 3..
//
/*
 * You created a new roller coaster that is about to open.
 * Its train consists of a single row of N seats numbered 1 through N from front to back.
 * Of course, seats closer to the front are more valuable.
 * Customers have already purchased opening-day tickets.
 * Each ticket allows a specific customer to take one ride on the coaster in a particular seat.
 * Some customers may have bought more than one ticket, and they expect to go on one ride for each ticket.
 *
 * You need to decide how many roller coaster rides there will be on opening day.
 * On each ride, one customer can sit in each seat; some seats on a ride might be left empty.
 * You cannot assign a customer to more than one seat in the same ride, nor can you put two customers on the same seat in any given ride.
 *
 * You wish to minimize the number of rides required to honor all tickets,
 * to reduce operational costs. To reduce the required number of rides, you can promote any number of tickets.
 * Promoting a ticket means taking a customer's ticket and giving
 * that customer a new ticket for a seat closer to the front of the train (that is, a seat with a lower number).
 * You would prefer to promote as few tickets as possible,
 * since too many promotions might cause customers to get greedy and ask for more promotions in the future.
 *
 * Given the positions and buyers of all the tickets that have been sold,
 * what is the minimum number of rides needed to honor all tickets,
 * using as many promotions as needed and scheduling the rides optimally?
 * And what is the minimum number of ticket promotions necessary to attain that number of rides?
 * Note that promoting a given customer on a given ride from seat 4 to seat 2, for example, counts as only one promotion, not two separate ones.
 */

/*
 * The first line of the input gives the number of test cases, T.
 * T test cases follow. Each test case starts with a single line with three integers N,
 * the number of seats in the roller coaster, C, the number of potential customers, and M,
 * the number of tickets sold. The customers are identified with numbers between 1 and C.
 * Then, M lines follow, each containing two integers: Pi,
 * the position in the roller coaster assigned to the i-th ticket, and Bi, the identifier of the buyer of that ticket.
 */

/*
 * For each test case, output one line containing Case #x: y z,
 * where x is the test case number (starting from 1),
 * y is the minimum number of rides you need to honor all tickets if you use the promotions and schedule the rides optimally,
 * and z is the minimum number of promotions you need to make be able to honor all tickets with y rides.
 */

/*
 * For each test case, output one line containing Case #x: y z,
 * where x is the test case number (starting from 1),
 * y is the minimum number of rides you need to honor all tickets if you use the promotions and schedule the rides optimally,
 * and z is the minimum number of promotions you need to make be able to honor all tickets with y rides.
 *
 * Limits
 * Time limit: 20 seconds per test set.
 * Memory limit: 1 GB.
 * 1 ≤ T ≤ 100.
 * 2 ≤ N ≤ 1000.
 * 1 ≤ M ≤ 1000.
 * 1 ≤ Pi ≤ N.
 * 1 ≤ Bi ≤ C.
 * Small dataset (Test Set 1 - Visible)
 * C = 2.
 * Large dataset (Test Set 2 - Hidden)
 * 2 ≤ C ≤ 1000.
*/

/*
 * Input
    5
    2 2 2
    2 1
    2 2
    2 2 2
    1 1
    1 2
    2 2 2
    1 1
    2 1
    1000 1000 4
    3 2
    2 1
    3 3
    3 1
    3 3 5
    3 1
    2 2
    3 3
    2 2
    3 1
*/
/*
 * Output
    Case #1: 1 1
    Case #2: 2 0
    Case #3: 2 0
    Case #4: 2 1
    Case #5: 2 1
*/

/*
 * Note that the last two sample cases would not appear in the Small dataset.
 *
 * In Case #1, both customers purchased a ticket for position 2.
 * It is impossible to honor both tickets with a single ride,
 * but promoting either ticket to position 1 allows you to accommodate both tickets on the same round.
 *
 * Case #2 is a similar story, except both tickets are for position 1.
 * Since you cannot promote those tickets or exchange them for inferior tickets, you are forced to run 2 separate rides, one per customer.
 *
 * Case #3 features the same customer purchasing both positions.
 * Since you are forced to have 2 rides for that customer, there is no reason to give out any promotions.
 *
 * In Case #4, notice that there may be both customers and positions with no tickets assigned.
 * In this case, there are three tickets sold for position three.
 * If you promote customer 2 to position 2, for instance, you can have one ride with customer 1 sitting in position 2 and customer 3 sitting in position 3,
 * and a second ride with customer 2 in position 2 and customer 1 in position 3.
 * Additional promotions will not allow you to decrease the number of rides,
 * because customer 1 has two tickets and you need to honor those in different rides, regardless of position.
 *
 * In Case #5, one optimal solution is to promote one of the 3 1 tickets to 1 1. 
 */

/*
 * code from https://github.com/ruippeixotog/google-code-jam-2017/blob/master/round2/roller-coaster-scheduling.cpp
 */
#include <algorithm>
#include <cstdio>
#include <cstring>
#include <iostream>
#include <map>
#include <queue>
#include <set>
#include <string>
#include <utility>
#include <vector>

#define MAXN 1000
#define INF 0x3f3f3f3f

using namespace std;

typedef long long ll;
typedef long double ld;

int hist[2][MAXN];

int main() {
    int t; scanf("%d\n", &t);
    for(int tc = 1; tc <= t; tc++) {
        int n, c, m; scanf("%d %d %d\n", &n, &c, &m);

        memset(hist, 0, sizeof(hist));
        for(int i = 0; i < m; i++) {
            int p, b; scanf("%d %d\n", &p, &b);
            hist[--b][--p]++;
        }

        vector<int> conflicts;
        for(int i = 0; i < n; i++) {
            if(hist[0][i] > 0 || hist[1][i] > 0) cerr << "elems " << hist[0][i] << " " << hist[1][i] << " " << endl;

            if(hist[0][i] > 0 && hist[1][i] > 0) {
//        cerr << "conf at " << (i + 1) << " " << endl;
                conflicts.push_back(i);
            }
        }

        int rides = 0, upgrades = 0;
        for(int i = 0; i < conflicts.size(); i++) {
            int ci = conflicts[i];

            int confs = min(hist[0][ci], hist[1][ci]);
            hist[0][ci] -= confs;
            hist[1][ci] -= confs;

            cerr << "confs pos " << (ci + 1) << " " << confs << endl;

            for(int j = i + 1; confs > 0 && j < conflicts.size(); j++) {
                int cj = conflicts[j];
                int rd = min(confs, min(hist[0][cj], hist[1][cj])) * 2;
                if(rd > 0) cerr << "conf*conf rides: " << rd << endl;
                rides += rd;
                confs -= rd / 2;
                hist[0][cj] -= rd / 2;
                hist[1][cj] -= rd / 2;
            }
            if(hist[1][ci] <= hist[0][ci]) {
                for(int j = 0; confs > 0 && j < n; j++) {
                    if(j == ci) continue;
                    int rd = min(confs, hist[0][j]);
                    if(rd > 0) cerr << "conf*r0 rides: " << rd << endl;
                    rides += rd;
                    confs -= rd;
                    hist[0][j] -= rd;
                    hist[0][ci] += rd;
                }
            }
            if(hist[0][ci] <= hist[1][ci]) {
                for (int j = 0; confs > 0 && j < n; j++) {
                    if (j == ci) continue;
                    int rd = min(confs, hist[1][j]);
                    if (rd > 0) cerr << "conf*r1 rides: " << rd << endl;
                    rides += rd;
                    confs -= rd;
                    hist[1][j] -= rd;
                    hist[1][ci] += rd;
                }
            }
            if(confs > 0) {
                cerr << "left conf rides: " << (confs * 2) << endl;
                if(ci == 0) rides += confs * 2;
                else { rides += confs; upgrades += confs; }
            }
        }
        int free1 = 0, free2 = 0;
        for(int i = 0; i < n; i++) {
            free1 += hist[0][i];
            free2 += hist[1][i];
        }
        cerr << free1 << " " << free2 << endl;
        rides += max(free1, free2);

        printf("Case #%d: %d %d\n", tc, rides, upgrades);
    }
    return 0;
}