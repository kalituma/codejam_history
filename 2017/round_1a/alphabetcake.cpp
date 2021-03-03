//
// Created by khw on 21. 3. 3..
//

/*
 * You are catering a party for some children, and you are serving them a cake in the shape of a grid with R rows and C columns.
 * Your assistant has started to decorate the cake by writing every child's initial in icing on exactly one cell of the cake.
 * Each cell contains at most one initial, and since no two children share the same initial, no initial appears more than once on the cake.

 * Each child wants a single rectangular (grid-aligned) piece of cake that has their initial and no other child's initial(s).
 * Can you find a way to assign every blank cell of the cake to one child, such that this goal is accomplished?
 * It is guaranteed that this is always possible.
 * There is no need to split the cake evenly among the children, and one or more of them may even get a 1-by-1 piece; this will be a valuable life lesson about unfairness.
 */

/*
 * The first line of the input gives the number of test cases, T.
 * T test cases follow. Each begins with one line with two integers R and C.
 * Then, there are R more lines of C characters each, representing the cake.
 * Each character is either an uppercase English letter (which means that your assistant has already added that letter to that cell) or ? (which means that that cell is blank).
 */

/*
 * For each test case, output one line containing Case #x: and nothing else.
 * Then output R more lines of C characters each.
 * Your output grid must be identical to the input grid, but with every ?
 * replaced with an uppercase English letter, representing that that cell appears in the slice for the child who has that initial.
 * You may not add letters that did not originally appear in the input.
 * In your grid, for each letter, the region formed by all the cells containing that letter must be a single grid-aligned rectangle.
 *
 * If there are multiple possible answers, you may output any of them.
 */

/*
 * Time limit: 20 seconds per test set.
 * Memory limit: 1 GB.
 * 1 ≤ T ≤ 100.
 * There is at least one letter in the input grid.
 * No letter appears in more than one cell in the input grid.
 * It is guaranteed that at least one answer exists for each test case.
 * Small dataset (Test Set 1 - Visible)
 * 1 ≤ R ≤ 12.
 * 1 ≤ C ≤ 12.
 * R × C ≤ 12.
 * Large dataset (Test Set 2 - Hidden)
 * 1 ≤ R ≤ 25.
 * 1 ≤ C ≤ 25.
 */

/*
Sample
    Input
    3
    3 3
    G??
    ?C?
    ??J
    3 4
    CODE
    ????
    ?JAM
    2 2
    CA
    KE
*/
/*
Output

 Case #1:
    GGJ
    CCJ
    CCJ

 Case #2:
    CODE
    COAE
    JJAM

 Case #3:
    CA
    KE
 */

/*
 * code from https://github.com/ruippeixotog/google-code-jam-2017/blob/master/round1a/alphabet-cake.cpp
 */
#include <cstdio>
#include <cstring>

#define MAXN 25

using namespace std;

char grid[MAXN][MAXN];

char start[MAXN];

int main() {
    int t; scanf("%d\n", &t);
    for(int tc = 1; tc <= t; tc++) {
        int r, c; scanf("%d %d\n", &r, &c);

        memset(start, 0, sizeof(start));
        for(int i = 0; i < r; i++) {
            for(int j = 0; j < c; j++) {
                scanf("%c", &grid[i][j]);
                if(!start[i] && grid[i][j] != '?') start[i] = grid[i][j];
            }
            scanf("\n");
        }

        int lastRow = 0;
        for(int i = 0; i < r; i++) {
            char curr = start[i];
            if(!curr) continue;

            lastRow = i;
            for(int j = 0; j < c; j++) {
                if(grid[i][j] == '?') grid[i][j] = curr;
                else curr = grid[i][j];
            }
            for(int i2 = i - 1; i2 >= 0 && !start[i2]; i2--) {
                memcpy(grid[i2], grid[i], sizeof(grid[i]));
            }
        }
        for(int i = lastRow + 1; i < r; i++) {
            memcpy(grid[i], grid[lastRow], sizeof(grid[lastRow]));
        }

        printf("Case #%d:\n", tc);
        for(int i = 0; i < r; i++) {
            for(int j = 0; j < c; j++) {
                printf("%c", grid[i][j]);
            }
            printf("\n");
        }
    }
    return 0;
}