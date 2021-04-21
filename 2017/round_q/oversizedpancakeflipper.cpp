//
// Created by khw on 21. 3. 2..
//

#include<iostream>
#include<string.h>
#include <bits/stdc++.h>
using namespace std;

/*
 * Problem
 * Last year, the Infinite House of Pancakes introduced a new kind of pancake.
 * It has a happy face made of chocolate chips on one side (the "happy side"), and nothing on the other side (the "blank side").
 * You are the head cook on duty. The pancakes are cooked in a single row over a hot surface.
 * As part of its infinite efforts to maximize efficiency, the House has recently given you an oversized pancake flipper that flips exactly K consecutive pancakes.
 * That is, in that range of K pancakes, it changes every happy-side pancake to a blank-side pancake, and vice versa; it does not change the left-to-right order of those pancakes.
 * You cannot flip fewer than K pancakes at a time with the flipper, even at the ends of the row (since there are raised borders on both sides of the cooking surface).
 * For example, you can flip the first K pancakes, but not the first K - 1 pancakes.
 * Your apprentice cook, who is still learning the job, just used the old-fashioned single-pancake flipper to flip some individual pancakes and then ran to the restroom with it,
 * right before the time when customers come to visit the kitchen. You only have the oversized pancake flipper left,
 * and you need to use it quickly to leave all the cooking pancakes happy side up, so that the customers leave feeling happy with their visit.
 * Given the current state of the pancakes, calculate the minimum number of uses of the oversized pancake flipper needed to leave all pancakes happy side up,
 * or state that there is no way to do it.
 */

/* Input
 * The first line of the input gives the number of test cases, T.
 * T test cases follow. Each consists of one line with a string S and an integer K.
 * S represents the row of pancakes: each of its characters is either + (which represents a pancake that is initially happy side up)
 * or - (which represents a pancake that is initially blank side up).
 */

/* Output
 * For each test case, output one line containing Case #x: y, where x is the test case number (starting from 1)
 * and y is either IMPOSSIBLE if there is no way to get all the pancakes happy side up,
 * or an integer representing the the minimum number of times you will need to use the oversized pancake flipper to do it.
 */

/* Limit
 * Time limit: 20 seconds per test set.
 * Memory limit: 1 GB.
 * 1 ≤ T ≤ 100.
 * Every character in S is either + or -.
 * 2 ≤ K ≤ length of S.
 * Small dataset (Test Set 1 - Visible)
 * 2 ≤ length of S ≤ 10.
 * Large dataset (Test Set 2 - Hidden)
 * 2 ≤ length of S ≤ 1000.
 */

// solution
namespace codejam_2017_q {
    void oversized_pancake_flipper(int no_of_trial, string& pancake, int k){
        for(int Trial= 1;Trial<=no_of_trial;Trial++)
        {
            // Number of pancakes in current trial
            int n = pancake.size();

            //Final solution
            int Number_Of_Flips = 0;

            for(int i=0;i+k <= n;i++)
            {
                if(pancake[i] == '-')
                {
                    for(int j=i;j< i+k;j++)
                    {
                        pancake[j] = (pancake[j] == '+') ? '-' : '+'; //Flip the pancake
                    }
                    Number_Of_Flips++;
                }
            }
            //Now we have flipped pancakes. Check which trials are full of happy faces;
            //if all are happy faces, then print the number of flips as solution
            //otherwise print "IMPOSSIBLE"

            bool All_Happyside = true;
            for (int i = 0; i < n; i++)
            {
                All_Happyside = (pancake[i] == '+');
                if(!All_Happyside)
                    break;
            }
            printf("Case #%d: ", Trial);
            if (All_Happyside)
                printf("%d\n", Number_Of_Flips);
            else
                printf("IMPOSSIBLE\n");
        }
    }
}
void call_oversized_pancake()
{
    int no_of_trial, k;
    string pancake;

    //Get the pancake positions
    cin >> no_of_trial;
    cin >> pancake;

    //Get the Pancake Flipper's capacity
    cin >> k;

    codejam_2017_q::oversized_pancake_flipper(no_of_trial, pancake, k);
}

