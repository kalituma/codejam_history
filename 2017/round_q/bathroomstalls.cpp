
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
        // n은 stall의 갯수, 기본적으로 양 옆은 채워져있다고 가정
        // k는 총 입장인 수
        ll n, k;
        cin >> n;
        cin >> k;

        codejam_2017_q::bathroomstalls(n, tc, spaces, k);
    }
}