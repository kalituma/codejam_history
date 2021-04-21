//
// Created by khw on 21. 3. 2..
//

/*
 * A certain bathroom has N + 2 stalls in a single row; the stalls on the left and right ends are permanently occupied by the bathroom guards. The other N stalls are for users.
 * Whenever someone enters the bathroom, they try to choose a stall that is as far from other people as possible.
 * To avoid confusion, they follow deterministic rules: For each empty stall S,
 * they compute two values LS and RS, each of which is the number of empty stalls between S and the closest occupied stall to the left or right, respectively.
 * Then they consider the set of stalls with the farthest closest neighbor, that is, those S for which min(LS, RS) is maximal.
 * If there is only one such stall, they choose it; otherwise, they choose the one among those where max(LS, RS) is maximal.
 * If there are still multiple tied stalls, they choose the leftmost stall among those.

 * K people are about to enter the bathroom; each one will choose their stall before the next arrives. Nobody will ever leave.
 *
 * When the last person chooses their stall S, what will the values of max(LS, RS) and min(LS, RS) be?
 */

/*
 * The first line of the input gives the number of test cases, T. T lines follow. Each line describes a test case with two integers N and K, as described above.
 */

/*
 * For each test case, output one line containing Case #x: y z, where x is the test case number (starting from 1),
 * y is max(LS, RS), and z is min(LS, RS) as calculated by the last person to enter the bathroom for their chosen stall S.
 */

/*
 * 1 ≤ T ≤ 100.
 * 1 ≤ K ≤ N.
 * Time limit: 60 seconds per test set.
 * Memory limit: 1GB.
 * Small Dataset 1 (Test set 1 - Visible)
 * 1 ≤ N ≤ 1000.
 * Small Dataset 2 (Test set 2 - Visible)
 * 1 ≤ N ≤ 106.
 * Large Dataset (Test set 3 - Hidden)
 * 1 ≤ N ≤ 1018.
 */


#include <cstdio>
#include <map>
#include <iostream>

using namespace std;
typedef long long ll;

namespace codejam_2017_q {
    void bathroomstalls( const int n, const int tc, map<ll, ll>& spaces, int k){
        spaces.clear();
        spaces[n]++;

        ll ls = -1, rs = -1;
        while(k > 0) {
            auto it = prev(spaces.end());
            ll size = it->first, count = it->second;
            spaces.erase(it);

            ls = (size - 1) / 2;
            rs = size / 2;
            spaces[ls] += count;
            spaces[rs] += count;
            k -= count;
        }
        printf("Case #%d: %lld %lld\n", tc, max(ls, rs), min(ls, rs));
    }
}

void run_bathroomstalls() {
    map<ll, ll> spaces;

    int t;
    cin >> t;
    for(int tc = 1; tc <= t; tc++) {
        ll n, k;
        cin >> n;
        cin >> k;

        codejam_2017_q::bathroomstalls(n, tc, spaces, k);
    }
}