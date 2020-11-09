//
// Created by GreenArrow on 2020/9/14.
//

#include <iostream>
#include <vector>

using namespace std;

class FutoshikiPuzzle {
public:
    vector<vector<int>> maps;
    vector<pair<pair<int, int>, pair<int, int>>> less_constraints;
    int nRow, nColumn;
    //表示第x行中某个数字是否存在
    int Count_RowNumbers[9][10];
    //表示第y列某个数字是否存在
    int Count_ColumnNumbers[9][10];

    void initial() {



        //初始地图
        maps = {{0, 0, 0, 7, 3, 8, 0, 5, 0},
                {0, 0, 7, 0, 0, 2, 0, 0, 0},
                {0, 0, 0, 0, 0, 9, 0, 0, 0},
                {0, 0, 0, 4, 0, 0, 0, 0, 0},
                {0, 0, 1, 0, 0, 0, 6, 4, 0},
                {0, 0, 0, 0, 0, 0, 2, 0, 0},
                {0, 0, 0, 0, 0, 0, 0, 0, 0},
                {0, 0, 0, 0, 0, 0, 0, 0, 0},
                {0, 0, 0, 0, 0, 0, 0, 0, 6}};
        nRow = maps.size();
        nColumn = maps[0].size();


        for (int i = 0; i < 9; i++) {
            for (int j = 0; j < 9; j++) {
                if (maps[i][j] != 0) {
                    Count_RowNumbers[i][maps[i][j]]++;
                    Count_ColumnNumbers[j][maps[i][j]]++;
                }
            }
        }
        //添加限制
        addConstraints(0, 0, 0, 1);
        addConstraints(0, 3, 0, 2);
        addConstraints(1, 3, 1, 4);
        addConstraints(1, 6, 1, 7);
        addConstraints(2, 6, 1, 6);
        addConstraints(2, 1, 2, 0);
        addConstraints(2, 2, 2, 3);
        addConstraints(2, 3, 3, 3);
        addConstraints(3, 3, 3, 2);
        addConstraints(3, 5, 3, 4);
        addConstraints(3, 5, 3, 6);
        addConstraints(3, 8, 3, 7);
        addConstraints(4, 1, 3, 1);
        addConstraints(4, 5, 3, 5);
        addConstraints(4, 0, 4, 1);
        addConstraints(5, 4, 4, 4);
        addConstraints(5, 8, 4, 8);
        addConstraints(5, 1, 5, 2);
        addConstraints(5, 4, 5, 5);
        addConstraints(5, 7, 5, 6);
        addConstraints(5, 1, 6, 1);
        addConstraints(6, 6, 5, 6);
        addConstraints(6, 8, 5, 8);
        addConstraints(6, 3, 6, 4);
        addConstraints(7, 7, 6, 7);
        addConstraints(7, 1, 8, 1);
        addConstraints(8, 2, 7, 2);
        addConstraints(7, 5, 8, 5);
        addConstraints(8, 8, 7, 8);
        addConstraints(8, 5, 8, 6);

    }

    void addConstraints(int x, int y, int x1, int y1) {
        less_constraints.push_back({{x,  y},
                                    {x1, y1}});
    }

    //检查当前位置是否可行
    bool check(int x, int y) {
        for (int i = 1; i < 10; i++) {
            if (Count_RowNumbers[x][i] > 1 || Count_ColumnNumbers[y][i] > 1) {
                return false;
            }
        }

        for (auto &less_constraint : less_constraints) {
            if (less_constraint.first.first == x && less_constraint.first.second == y) {
                if (maps[x][y] == 9) {
                    return false;
                }
                if (maps[less_constraint.second.first][less_constraint.second.second] > 0 &&
                    maps[less_constraint.second.first][less_constraint.second.second] <= maps[x][y]) {

                    return false;
                }
            }
        }

        for (auto &less_constraint : less_constraints) {
            if (less_constraint.second.first == x && less_constraint.second.second == y) {
                if (maps[x][y] == 1) {

                    return false;
                }
                if (maps[less_constraint.first.first][less_constraint.first.second] > 0 &&
                    maps[less_constraint.first.first][less_constraint.first.second] >= maps[x][y]) {

                    return false;
                }
            }
        }
        return true;
    }

    //显示图片
    void show() {
        for (int i = 0; i < nRow; i++) {
            for (int j = 0; j < nColumn; j++) {
                cout << maps[i][j] << " ";
            }
            cout << endl;
        }
        cout << "======================" << endl;
    }

    bool search(int x, int y) {

        if (maps[x][y] == 0) {
            for (int i = 1; i < 10; i++) {
                maps[x][y] = i;
                Count_RowNumbers[x][i]++;
                Count_ColumnNumbers[y][i]++;
                if (check(x, y)) {
                    if (x == 8 && y == 8) {
                        return true;
                    }
                    int next_x, next_y;
                    if (y != 8) {
                        next_x = x;
                        next_y = y + 1;
                    } else {
                        next_x = x + 1;
                        next_y = 0;
                    }


                    if (search(next_x, next_y)) {
                        return true;
                    }
                }
                maps[x][y] = 0;
                Count_RowNumbers[x][i]--;
                Count_ColumnNumbers[y][i]--;
            }
        } else {
            if (x == 8 && y == 8) {
                return true;
            }
            int next_x, next_y;
            if (y != 8) {
                next_x = x;
                next_y = y + 1;
            } else {
                next_x = x + 1;
                next_y = 0;
            }


            if (search(next_x, next_y)) {
                return true;
            }
        }
        return false;
    }
};

int main() {
    FutoshikiPuzzle *futoshikiPuzzle = new FutoshikiPuzzle();
    futoshikiPuzzle->initial();
    futoshikiPuzzle->show();
    futoshikiPuzzle->search(0, 0);
    futoshikiPuzzle->show();
	return 0;
}
