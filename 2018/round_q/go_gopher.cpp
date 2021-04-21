// https://github.com/ruippeixotog/google-code-jam-2018/blob/master/qualification/go-gopher.cpp
/*
 *
 */
#include <cstdio>
#include <cstring>

#define MAXA 200

bool field[MAXA / 3 + 2][4];

int main() {
    int t; scanf("%d", &t);
    for(int tc = 1; tc <= t; tc++) {
        int a; scanf("%d", &a);

        int rowCount = (a + 2) / 3;
        memset(field, false, sizeof(field));

        int row = 2, fillCnt = 0;
        while(true) {
            while(row < rowCount - 1 && fillCnt == 3) {
                fillCnt = field[row][1] + field[row][2] + field[row][3];
                row++;
            }
            printf("%d 2\n", row); fflush(stdout);

            int il, jl; scanf("%d %d", &il, &jl);
            if(il == -1) return 0;
            if(il == 0) break;

            if(il == row - 1 && !field[il][jl]) fillCnt++;
            field[il][jl] = true;
        }
    }
    return 0;
}