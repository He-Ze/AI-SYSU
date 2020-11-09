#include<iostream>
#include<cstring>
#include<vector>
#include<time.h>
using namespace std;

const int max_size = 9;
int size;
static int nodes = 0;
clock_t start_time,end_time;
double node_time;

struct item {
    int val;
    Position pos;
    int curdom[max_size+1];
    bool assigned;
    vector<Relation> relation;
    item() {}
};

struct futoshiki {
    item board[max_size+1][max_size+1];
    vector<MultiRelation> multirelation; 
    futoshiki() {}
};

struct Position{
    int row, col;
    Position() {}
    Position(int a, int b): row(a), col(b) {}
};

struct Relation {
    Position p;
    int r;    // 1 : >, -1 : <
    Relation() {}
    Relation(Position a, int re): p(a), r(re) {}
};

struct MultiRelation {
    Position x, y;
    int r;
    MultiRelation() {}
    MultiRelation(Position a, Position b, int re): x(a), y(b), r(re) {}
};

int CDcount(item* m);
bool RowCheck(futoshiki* f, item* m);
bool ColCheck(futoshiki* f, item* m);
bool neighbour_check(futoshiki* f);
item* heuristicpick(futoshiki* f);
void GAC(futoshiki* f);
bool GAC_Enforce(futoshiki* f, item* v);
bool finish(futoshiki* f);
void Copyboard(futoshiki* dest, const futoshiki* src);
void display(futoshiki* f);

int main() {
    cout << "请输入维数：";
    cin >> size;
    futoshiki f;
    futoshiki* ptr = &f;
    for (int i = 1;i<=size;i++) {
        for (int j = 1;j<=size;j++) {
            ptr->board[i][j].val = 0;
            ptr->board[i][j].pos.row = i;
            ptr->board[i][j].pos.col = j;
            ptr->board[i][j].assigned = 0;
            memset(ptr->board[i][j].curdom, 0, sizeof(ptr->board[i][j].curdom));
        }
    }
    cout << "请输入大小关系（以0 0 0 0 0结束）：" << endl;
    while(1) {
        Position x, y;
        char c;        
        cin >> x.row >> x.col >> c >> y.row >> y.col;
        if (c!='<' && c!='>') 
            break;
        Relation tmp1(y, ((c == '>') ? 1 : -1));
        Relation tmp2(x, ((c == '>') ? -1 : 1));
        MultiRelation tmp(x, y, ((c == '>') ? 1 : -1));
        ptr->multirelation.push_back(tmp);
        ptr->board[x.row][x.col].relation.push_back(tmp1);
        ptr->board[y.row][y.col].relation.push_back(tmp2);
    }
    cout << "请输入某些元素初始值（以0 0 0结束）：" << endl;
    while(1) {
        int a, b, v;
        cin >> a >> b >> v;
        if (a+b+v == 0)
            break;
        ptr->board[a][b].val = v;
        ptr->board[a][b].assigned = 1;
        GAC_Enforce(ptr, &ptr->board[a][b]);
    }
    cout << "初始Futoshiki：" << endl;
    display(ptr);
    start_time=clock();
    GAC(ptr);
    return 0;
}

bool RowCheck(futoshiki* f, item* m) {
    int row = m->pos.row;
    int val = m->val;
    for(int i = 1;i<=size;i++) {
        item* current_item = &f->board[row][i];        
        if (current_item->assigned)
            continue;
        if (!current_item->curdom[val]) {
            current_item->curdom[val] = 1;
            current_item->curdom[0] = CDcount(&f->board[row][i]);
        }
        if(current_item->curdom[0] == size) 
            return false;
    }
    return true;
}

bool ColCheck(futoshiki* f, item* m) {
    int col = m->pos.col;
    int val = m->val;
    for(int i = 1;i<=size;i++) {
        item* current_item = &f->board[i][col];
        if (current_item->assigned) 
            continue;
        if (!current_item->curdom[val]) {
            current_item->curdom[val] = 1;
            current_item->curdom[0] = CDcount(&f->board[i][col]);
        }
        if(current_item->curdom[0] == size) 
            return false;
    }
    return true;
}

bool neighbour_check(futoshiki* f) {
    bool flag = true;
    for (size_t m = 0;m<f->multirelation.size();m++) {
        int x_row = f->multirelation[m].x.row;
        int x_col = f->multirelation[m].x.col;
        int y_row = f->multirelation[m].y.row;
        int y_col = f->multirelation[m].y.col;
        item* X = &f->board[x_row][x_col];
        item* Y = &f->board[y_row][y_col];
        int re = f->multirelation[m].r;
        
        if (X->assigned && Y->assigned) 
            continue;
        else if (X->assigned) {
            int v = X->val;
            if (re == 1) {
                for (int j = v;j<=size;j++) {
                    if (!Y->curdom[j]) {
                        Y->curdom[j] = 1;
                        Y->curdom[0] = CDcount(Y);
                    }
                }
                if(Y->curdom[0] == size) 
                    flag = false;
            }
            else if (re == -1)  {
                for (int j = v;j>0;j--){ 
                    if (!Y->curdom[j]) {
                        Y->curdom[j] = 1;
                        Y->curdom[0] = CDcount(Y);
                    }
                }
                if(Y->curdom[0] == size) 
                    flag = false;
            }
        }
        else if (Y->assigned) {
            int v = Y->val;
            if (re == 1) {
                for (int j = v;j>0;j--) {
                    if (!X->curdom[j]) {
                        X->curdom[j] = 1;
                        X->curdom[0] = CDcount(X);
                    }
                }
                if(X->curdom[0] == size) 
                    flag = false;
            }
            else if (re == -1)  {
                for (int j = v;j<=size;j++){
                    if (!X->curdom[j]) {
                        X->curdom[j] = 1;
                        X->curdom[0] = CDcount(X);
                    }
                }
                if(X->curdom[0] == size) 
                    flag = false;
            }            
        }
        else {
            if (re == 1) {
                for (int j = 1;j<=size;j++){
                    if (!X->curdom[j]) {
                        int t = 1;
                        while (Y->curdom[t++]) {
                            if(t == j) {
                                X->curdom[j] = 1;
                                X->curdom[0] = CDcount(X);
                            }
                        }
                    }
                    if(X->curdom[0] == size) 
                        flag = false;
                }
                for (int j = 1;j<=size;j++){
                    if (!Y->curdom[j]) {
                        int t = j + 1;
                        while (X->curdom[t++]) {
                            if(t == size + 1) {
                                Y->curdom[j] = 1;
                                Y->curdom[0] = CDcount(Y);
                            }
                        }
                        if(Y->curdom[0] == size) 
                            flag = false;
                    }
                }
            }
            else if (re == -1)  {
                for (int j = 1;j<=size;j++){
                    if (!X->curdom[j]) {
                        int t = j + 1;
                        while (Y->curdom[t++]) {
                            if(t == size + 1) {
                                X->curdom[j] = 1;
                                X->curdom[0] = CDcount(X);
                            }
                        }
                        if(X->curdom[0] == size) 
                            flag = false;
                    }
                }
                for (int j = 1;j<=size;j++) {
                    if (!Y->curdom[j]) {
                        int t = 1;
                        while (X->curdom[t++]) {
                            if(t == j) {
                                Y->curdom[j] = 1;
                                Y->curdom[0] = CDcount(Y);
                            }
                        }
                        if(Y->curdom[0] == size) 
                            flag = false;
                    }
                }
            }
        }
    }
    return flag;
}

bool finish(futoshiki* f) {
    for (int i = 1;i<=size;i++) {
        for (int j = 1;j<=size;j++) {
            if (!f->board[i][j].assigned)
                return false;
        }
    }
    return true;
}

item* heuristicpick(futoshiki* f) {
    // MRV
    item* maxi = &f->board[1][1];
    for (int i = 1;i<=size;i++) {
        for (int j = 1;j<=size;j++) {
            if(f->board[i][j].assigned) 
                continue;
            if(maxi->curdom[0] < f->board[i][j].curdom[0] || maxi->assigned) {
                maxi = &f->board[i][j];
                if (maxi->curdom[0] == size-1) 
                    return maxi;
            }
        }
    }
    return maxi;
}

void Copyboard(futoshiki* dest, const futoshiki* src) {
    memset(dest->board, 0, sizeof(dest->board));
    dest->multirelation.clear();
    for (int i =1;i<=size;i++) {
        for (int j =1;j<=size;j++) {
            dest->board[i][j].val = src->board[i][j].val;
            dest->board[i][j].pos.row = src->board[i][j].pos.row;
            dest->board[i][j].pos.col = src->board[i][j].pos.col;
            memcpy(dest->board[i][j].curdom, src->board[i][j].curdom, sizeof(dest->board[i][j].curdom));
            dest->board[i][j].assigned = src->board[i][j].assigned;
            dest->board[i][j].relation = src->board[i][j].relation;
        }
    }
    dest->multirelation = src->multirelation;
}

bool GAC_Enforce(futoshiki* f, item* v) {
    bool flag_row = 0, flag_col = 0, flag_compare = 0;
    flag_row = RowCheck(f, v);
    flag_col = ColCheck(f, v);
    flag_compare = neighbour_check(f);
    return (flag_row && flag_col && flag_compare);
}

void GAC(futoshiki* f) {
    clock_t clock1=clock();
    nodes++;
    if (finish(f)) {
        end_time=clock();
        double time=(double)(end_time-start_time)/CLOCKS_PER_SEC;
        cout << "结果Futoshiki：" << endl; 
        display(f);
        cout << "运行总时间：" << time*1000 << " ms" << endl;
        cout << "搜索的节点数：" << nodes << "次" << endl;
        cout << "每个节点平均GAC时间：" << (double)(node_time*1000.00/(nodes-1)) << "ms" << endl;
        exit(0);
    }
    item* v = heuristicpick(f);
    v->assigned = true;
    for (int i = 1;i<=size;i++){
        if (!v->curdom[i]) {
            v->val = i;
            futoshiki boardcopy;
            Copyboard(&boardcopy, f);
            for (int j = 1;j<=size;j++){
                if (j != i && !v->curdom[j]) { 
                    v->curdom[j] = 1;
                    v->curdom[0] = CDcount(v);
                }
            }
            if (GAC_Enforce(f, v) != false) {
                GAC(f);
            }
            Copyboard(f, &boardcopy);
        }
    }
    v->assigned = false;
    clock_t clock2=clock();
    double time_per_node=(double)(clock2-clock1)/CLOCKS_PER_SEC;
    node_time+=time_per_node;
}

int CDcount(item* m) {
    int res = 0;
    for (int i = 1;i<=size;i++) {
        res += m->curdom[i];
    }
    return res;
}

string lrarrow(futoshiki* f, item* m) {
    if (!f->board[m->pos.row][m->pos.col].relation.size()) 
        return "  ";
    else {
        for(size_t i = 0;i<f->board[m->pos.row][m->pos.col].relation.size();i++) {
            int col = f->board[m->pos.row][m->pos.col].relation[i].p.col;
            int r = f->board[m->pos.row][m->pos.col].relation[i].r;
            if (col == m->pos.col+1) 
                return (r == -1) ? " <" : " >";
        }
    }
    return "  ";
}
string udarrow(futoshiki* f, item* m) {
    if (!f->board[m->pos.row][m->pos.col].relation.size()) 
        return "    ";
    else{
        for(size_t i = 0;i<f->board[m->pos.row][m->pos.col].relation.size();i++) {
            int row = f->board[m->pos.row][m->pos.col].relation[i].p.row;
            int r = f->board[m->pos.row][m->pos.col].relation[i].r;
            if (row == m->pos.row+1) 
                return (r == -1) ? " ^  " : " v  ";
        }
    }
    return "    ";
}
void display(futoshiki* f) {
    for (int i = 1;i<=size;i++) {
        cout << "\t";
        for (int j = 1;j<=size;j++) {
            cout << " " << f->board[i][j].val << lrarrow(f, &f->board[i][j]);
        }
        cout << endl << "\t";
        for (int j = 1;j<=size;j++) if (i!=size) {
            cout << udarrow(f, &f->board[i][j]);
        }
        cout << endl;
    }
}