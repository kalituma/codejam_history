//
// Created by khw on 21. 3. 2..
//

#include <iostream>
#include <vector>

using namespace std;

/*
 * Tatiana likes to keep things tidy. Her toys are sorted from smallest to largest,
 * her pencils are sorted from shortest to longest and her computers from oldest to newest.
 * One day, when practicing her counting skills, she noticed that some integers, when written in base 10 with no leading zeroes,
 * have their digits sorted in non-decreasing order. Some examples of this are 8, 123, 555, and 224488. She decided to call these numbers tidy.
 * Numbers that do not have this property, like 20, 321, 495 and 999990, are not tidy.
 * She just finished counting all positive integers in ascending order from 1 to N. What was the last tidy number she counted?
 */

/*
 * The first line of the input gives the number of test cases, T. T lines follow. Each line describes a test case with a single integer N, the last number counted by Tatiana.
 */

/*
 * For each test case, output one line containing Case #x: y, where x is the test case number (starting from 1) and y is the last tidy number counted by Tatiana.
 */

/*
 * Time limit: 20 seconds per test set.
 * Memory limit: 1 GB.
 * 1 ≤ T ≤ 100.
 * Small dataset (Test Set 1 - Visible)
 * 1 ≤ N ≤ 1000.
 * Large dataset (Test Set 2 - Hidden)
 * 1 ≤ N ≤ 1018.
 */

namespace codejam_2017_q{
    long long tidynumbers(vector<int>& vec){
        int cipher = vec.size();
        if (cipher != 1) {
            for (int a = cipher - 1; a > 0; a--) {
                for (int b = cipher - 1; b > 0; b--) {
                    if (vec[b] > vec[b - 1]) {
                        vec[b] -= 1;
                        while (b != 0) {
                            vec[b - 1] = 9;
                            b--;
                        }
                        break;
                    }
                }
            }
        }

        long long num = 0;
        for (int a = cipher - 1; a >= 0; a--) {
            num = num * 10 + vec[a];
        }

        return num;
    }
}
int call_tidynumbers() {
    int testCount;
    cin >> testCount;

    for (int i = 0; i < testCount; i++) {
        long long N;
        vector <int>vec;
        cin >> N;

        int c = 0;
        while (N) {
            vec.push_back(N % 10);
            N = N / 10;
        }

        long long num = codejam_2017_q::tidynumbers(vec);
        cout << "Case #" << i + 1 << ": " << num << endl;
    }

    return 0;
}

