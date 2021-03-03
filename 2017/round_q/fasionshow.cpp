//
// Created by khw on 21. 3. 2..
//

/*
 * You are about to host a fashion show to show off three new styles of clothing.
 * The show will be held on a stage which is in the most fashionable of all shapes: an N-by-N grid of cells.
 *
 * Each cell in the grid can be empty (which we represent with a . character) or can contain one fashion model.
 * The models come in three types, depending on the clothing style they are wearing: +, x, and the super-trendy o.
 * A cell with a + or x model in it adds 1 style point to the show. A cell with an o model in it adds 2 style points. Empty cells add no style points.
 * To achieve the maximum artistic effect, there are rules on how models can be placed relative to each other.
 * Whenever any two models share a row or column, at least one of the two must be a +.
 * Whenever any two models share a diagonal of the grid, at least one of the two must be an x.
 * Formally, a model located in row i0 and column j0 and a model located in row i1 and column j1 share a row if and only if i0 = i1,
 * they share a column if and only if j0 = j1, and they share a diagonal if and only if i0 + j0 = i1 + j1 or i0 - j0 = i1 - j1.
 * For example, the following grid is not legal:
 *
 * ...
 * x+o
 * .+.
 *
 * The middle row has a pair of models (x and o) that does not include a +.
 * The diagonal starting at the + in the bottom row and running up to the o in the middle row has two models, and neither of them is an x.
 * However, the following grid is legal. No row, column, or diagonal violates the rules.
 *
 * +.x
 * +x+
 * o..
 *
 * Your artistic advisor has already placed M models in certain cells, following these rules.
 * You are free to place any number (including zero) of additional models of whichever types you like.
 * You may not remove existing models, but you may upgrade as many existing + and x models into o models as you wish, as long as the above rules are not violated.
 *
 * Your task is to find a legal way of placing and/or upgrading models that earns the maximum possible number of style points.
 */


#include <cstdio>
#include <cstring>
#include <vector>

#define MAXN 100

using namespace std;

int n;
bool row[MAXN], col[MAXN], diag1[MAXN * 2 - 1], diag2[MAXN * 2 - 1];

int crossSol[MAXN][MAXN], plusSol[MAXN][MAXN];

void placeCrosses() {
    for(int i = 0; i < n; i++) {
        if(row[i]) continue;
        for(int j = 0; j < n; j++) {
            if(col[j]) continue;

            crossSol[i][j] = 1;
            col[j] = true;
            break;
        }
    }
}

int placePluses() {
    vector<int> ds;
    for(int i = 0; i < n - 1; i++) {
        ds.push_back(i);
        ds.push_back(n * 2 - i - 2);
    }
    ds.push_back(n - 1);

    int points = 0;
    for(int d: ds) {
        if(diag1[d]) { points++; continue; }
        int i = d < n ? d : n - 1;
        int j = d < n ? 0 : d - n + 1;

        for(; i >= 0 && j < n; i--, j++) {
            if(diag2[i - j + n - 1]) continue;

            plusSol[i][j] = 1;
            diag2[i - j + n - 1] = true;
            points++;
            break;
        }
    }
    return points;
}

int main() {
    int t; scanf("%d\n", &t);
    for(int tc = 1; tc <= t; tc++) {
        int m; scanf("%d %d\n", &n, &m);

        memset(row, 0, sizeof(row));
        memset(col, 0, sizeof(col));
        memset(diag1, 0, sizeof(diag1));
        memset(diag2, 0, sizeof(diag2));
        memset(crossSol, 0, sizeof(crossSol));
        memset(plusSol, 0, sizeof(plusSol));

        for(int i = 0; i < m; i++) {
            char ch; int r, c; scanf("%c %d %d\n", &ch, &r, &c);
            r--; c--;
            if(ch != '+') {
                crossSol[r][c] = -1;
                row[r] = col[c] = true;
            }
            if(ch != 'x') {
                plusSol[r][c] = -1;
                diag1[r + c] = diag2[r - c + n - 1] = true;
            }
        }

        placeCrosses();
        int plusPoints = placePluses();

        int pieces = 0;
        for(int i = 0; i < n; i++) {
            for(int j = 0; j < n; j++) {
                if(crossSol[i][j] > 0 || plusSol[i][j] > 0) pieces++;
            }
        }

        printf("Case #%d: %d %d\n", tc, n + plusPoints, pieces);
        for(int i = 0; i < n; i++) {
            for(int j = 0; j < n; j++) {
                if(crossSol[i][j] > 0 || plusSol[i][j] > 0) {
                    char ch = crossSol[i][j] ? (plusSol[i][j] ? 'o' : 'x') : '+';
                    printf("%c %d %d\n", ch, i + 1, j + 1);
                }
            }
        }
    }
    return 0;
}