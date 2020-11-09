#include<iostream>
#include<algorithm>
#include<cstring>
#include <ctime>
using namespace std;
#define size 9
int nodes=0;
double node_time;

struct item {
	int val;
	int row, col;
	int l, r, u, d;
	bool domain[size];
	bool assigned;
};

struct futoshiki {
	item board[size][size];
	int domain_count(item* m);
	bool row_check(futoshiki* board, item* m);
	bool col_check(futoshiki* board, item* m);
	bool check(futoshiki* board, item* m);
	bool is_finished(futoshiki* board);
	bool fc_check(futoshiki* board, int c, item* m);
	item* heuristicpick(futoshiki* board);
	void propagete(futoshiki* board, item* m);
};

int domain_count(item* m) {
	int a = 0;
	for (int i = 0;i<size;i++)
		a += m->domain[i];
	return a;
}

bool row_check(futoshiki* board, item* m) {
	int row[size];
	for(int i = 0;i<size;i++)
		row[i] = board->board[m->row][i].val;
	sort(row, row + size);
	for(int i = 0;i<size-1;i++) {
		if (!row[i])
			continue;
		if (row[i] == row[i+1])
			return false;
	}
	return true;
}

bool col_check(futoshiki* board, item* m) {
	int col[size];
	for(int i = 0;i<size;i++)
		col[i] = board->board[i][m->col].val;
	sort(col, col + size);
	for(int i = 0;i<size-1;i++) {
		if (!col[i])
			continue;
		if (col[i] == col[i+1])
			return false;
	}
	return true;
}

bool check(futoshiki* board, item* m) {
	int v = m->val;
	if (m->u && board->board[m->row - 1][m->col].assigned) {
		if (m->u == -1 && v > board->board[m->row - 1][m->col].val)
			return false;
		else if (m->u == 1 && v < board->board[m->row - 1][m->col].val)
			return false;
	}
	if (m->d && board->board[m->row + 1][m->col].assigned) {
		if (m->d == -1 && v > board->board[m->row + 1][m->col].val)
			return false;
		else if (m->d == 1 && v < board->board[m->row + 1][m->col].val)
			return false;
	}
	if (m->l && board->board[m->row - 1][m->col].assigned) {
		if (m->l == -1 && v > board->board[m->row][m->col - 1].val)
			return false;
		else if (m->l == 1 && v < board->board[m->row][m->col - 1].val)
			return false;
	}
	if (m->r && board->board[m->row - 1][m->col].assigned) {
		if (m->r == -1 && v > board->board[m->row][m->col + 1].val)
			return false;
		else if (m->r == 1 && v < board->board[m->row][m->col + 1].val)
			return false;
	}
	return true;
}

bool assign_check(futoshiki* board, int c, item* m) {
	int R = m->row, C = m->col, s = 0;
	if (c == 0) {
		for (int i = 0;i<size;i++)
			s += board->board[R][i].assigned;
		return (s == size-1);
	}
	else if (c == 1) {
		for (int i = 0;i<size;i++)
			s += board->board[i][C].assigned;
		return (s == size-1);
	}
	else if (c == 2) {
		s += (R == 0) ? 1 : board->board[R - 1][C].assigned;
		s += (R == size-1) ? 1 : board->board[R + 1][C].assigned;
		s += (C == 0) ? 1 : board->board[R][C - 1].assigned;
		s += (C == size-1) ? 1 : board->board[R][C + 1].assigned;
		return (s == size-1);
	}
	return false;
}

bool fc_check(futoshiki* board, int c, item* m) {
	nodes++;
	clock_t clock1=clock();
	if (c == 0)
		for (int i = 0;i<size;i++) {
			if (!m->domain[i]) {
				m->domain[i] = 1;
				if(row_check(board, m))
					m->domain[i] = 0;
			}
		}
	else if (c == 1)
		for (int i = 0;i<size;i++) {
			if (!m->domain[i]) {
				m->domain[i] = 1;
				if(col_check(board, m))
					m->domain[i] = 0;
			}
		}
	else if (c == 2)
		for (int i = 0;i<size;i++) {
			if (!m->domain[i]) {
				m->domain[i] = 1;
				if(check(board, m))
					m->domain[i] = 0;
			}
		}
	clock_t clock2=clock();
	double time_per_node=(double)(clock2-clock1)/CLOCKS_PER_SEC;
	node_time+=time_per_node;
	if (domain_count(m) == size)
		return false;
	else
		return true;
}

item* heuristicpick(futoshiki* board) {
	// MRV
	item* maxi = &board->board[0][0];
	for (int i = 0;i<size;i++) {
		for (int j = 0;j<size;j++) {
			if(board->board[i][j].assigned)
				continue;
			if(domain_count(maxi) < domain_count(&board->board[i][j]) || maxi->assigned) {
				maxi = &board->board[i][j];
				if (domain_count(maxi) == size-1)
					return maxi;
			}
		}
	}
	return maxi;
}

void propagate(futoshiki* board, item* m) {
	for (int i = 0;i<size;i++) {
		board->board[m->row][i].domain[m->val-1] = 1;
		board->board[i][m->col].domain[m->val-1] = 1;
	}
	if (m->r == -1) {
		for (int i = 0;i<m->val - 1;i++) {
			board->board[m->row][m->col + 1].domain[i] = 1;
		}
	}
	else if (m->r == 1) {
		for (int i = m->val;i<size;i++) {
			board->board[m->row][m->col + 1].domain[i] = 1;
		}
	}
	if (m->u == -1) {
		for (int i = 0;i<m->val - 1;i++) {
			board->board[m->row - 1][m->col].domain[i] = 1;
		}
	}
	else if (m->u == 1) {
		for (int i = m->val;i<size;i++) {
			board->board[m->row - 1][m->col].domain[i] = 1;
		}
	}
	if (m->l == -1) {
		for (int i = 0;i<m->val - 1;i++) {
			board->board[m->row][m->col - 1].domain[i] = 1;
		}
	}
	else if (m->l == 1) {
		for (int i = m->val;i<size;i++) {
			board->board[m->row][m->col - 1].domain[i] = 1;
		}
	}
	if (m->d == -1) {
		for (int i = 0;i<m->val - 1;i++) {
			board->board[m->row + 1][m->col].domain[i] = 1;
		}
	}
	else if (m->d == 1) {
		for (int i = m->val;i<size;i++) {
			board->board[m->row + 1][m->col].domain[i] = 1;
		}
	}
}

void print(futoshiki* board) {
	for (int i = 0;i<size;i++) {
		cout << "\t";
		for (int j = 0;j<size;j++) {
			if (board->board[i][j].r == 1) cout << " " << board->board[i][j].val << " >";
			else if (board->board[i][j].r == -1) cout << " " << board->board[i][j].val << " <";
			else cout << " " << board->board[i][j].val << "  ";
		}
		cout << endl << "\t";
		if (i!=size-1) {
			for (int j = 0;j<size;j++) {
				if (board->board[i+1][j].u == 1)
					cout << " ^  ";
				else if (board->board[i+1][j].u == -1)
					cout << " v  ";
				else cout << "    ";
			}
		}
		cout << endl;
	}
}

bool is_finished(futoshiki* board) {
	for (int i = 0;i<size;i++)
		for (int j = 0;j<size;j++)
			if (!board->board[i][j].assigned)
				return false;
	return true;
}

bool FC(futoshiki* board, int level) {
	if (is_finished(board)) {
		cout<<"完成后矩阵："<<endl;
		print(board);
		return true;
	}
	item* v = heuristicpick(board); // Pick with MRV
	v->assigned = true;
	bool dwo = false;
	int pos = 0;
	for (int i = 0;i<size;i++)
		if (!v->domain[i]) {
			futoshiki boardcopy;
			memcpy(&boardcopy, board, sizeof(futoshiki));
			v->val = i+1;
			propagate(board, v);
			dwo = false;
			if (!dwo && assign_check(board, 0, v)) {
				for (int i = 0;i<size;i++)
					if (!board->board[v->row][i].assigned)
						dwo = !fc_check(board, 0, &board->board[v->row][i]);
			}
			if (!dwo && assign_check(board, 1, v)) {
				for (int i = 0;i<size;i++)
					if (!board->board[i][v->col].assigned)
						dwo = !fc_check(board, 1, &board->board[i][v->col]);
			}
			if (!dwo && assign_check(board, 2, v)) {
				if (v->row && board->board[v->row - 1][v->col].assigned)
					dwo = !fc_check(board, 2, &board->board[v->row - 1][v->col]);
				else if (v->row!=size-1 && board->board[v->row + 1][v->col].assigned)
					dwo = !fc_check(board, 2, &board->board[v->row + 1][v->col]);
				else if (v->col && board->board[v->row][v->col - 1].assigned)
					dwo = !fc_check(board, 2, &board->board[v->row][v->col - 1]);
				else if (v->col!=size-1 && board->board[v->row][v->col + 1].assigned)
					dwo = !fc_check(board, 2, &board->board[v->row][v->col + 1]);
			}
			if(!dwo && FC(board, level + 1))
				return true;
			memcpy(board, &boardcopy, sizeof(futoshiki));
		}
	v->assigned = false;
	return false;
}

int main() {
	futoshiki f;
	futoshiki* ptr = &f;
	for (int i = 0;i<size;i++) {
		for (int j = 0;j<size;j++) {
			f.board[i][j].val = 0;
			f.board[i][j].row = i;
			f.board[i][j].col = j;
			f.board[i][j].u = 0;
			f.board[i][j].d = 0;
			f.board[i][j].l = 0;
			f.board[i][j].r = 0;
			f.board[i][j].assigned = 0;
			memset(f.board[i][j].domain, 0, sizeof(f.board[i][j].domain));
		}
	}
	cout << "请输入大小关系（以0 0 0 0 0结束）：" << endl;
	while(1) {
		char c; 
		int aa,bb,dd,ee;       
		cin >> aa >> bb >> c >> dd >> ee;
		if (c!='<' && c!='>') 
			break;
		if(aa==dd){
			if(c=='<'){
				if(bb<ee){
					f.board[aa-1][bb-1].r=-1;
					f.board[dd-1][ee-1].l=1;
				}
				else{
					f.board[aa-1][bb-1].l=-1;
					f.board[dd-1][ee-1].r=1;
				}
			}
			if(c=='>'){
				if(bb<ee){
					f.board[aa-1][bb-1].r=1;
					f.board[dd-1][ee-1].l=-1;
				}
				else{
					f.board[aa-1][bb-1].l=1;
					f.board[dd-1][ee-1].r=-1;
				}
			}
		}
		if(bb==ee){
			if(c=='<'){
				if(aa<dd){
					f.board[aa-1][bb-1].d=-1;
					f.board[dd-1][ee-1].u=1;
				}
				else{
					f.board[aa-1][bb-1].u=-1;
					f.board[dd-1][ee-1].d=1;
				}
			}
			if(c=='>'){
				if(aa<dd){
					f.board[aa-1][bb-1].d=1;
					f.board[dd-1][ee-1].u=-1;
				}
				else{
					f.board[aa-1][bb-1].u=1;
					f.board[dd-1][ee-1].d=-1;
				}

			}
		}
	}
	cout << "请输入某些元素初始值（以0 0 0结束）：" << endl;
	while(1) {
		int a, b, v;
		cin >> a >> b >> v;
		if (a+b+v == 0)
			break;
		f.board[a-1][b-1].val = v; 
		f.board[a-1][b-1].assigned = 1; 
		propagate(ptr, &f.board[a-1][b-1]);
	}


//	f.board[0][0].r=1 ; f.board[0][1].l=-1 ;	f.board[1][0].u=1 ; f.board[0][0].d=-1 ;
//	f.board[1][1].r=-1 ; f.board[1][2].l=1 ;	f.board[1][2].r=-1 ; f.board[1][3].l=1 ;
//	f.board[1][3].r=-1 ; f.board[1][4].l=1 ;	f.board[2][1].r=-1 ; f.board[2][2].l=1 ;
//	f.board[4][0].r=1 ; f.board[0][1].l=-1 ;
//	f.board[4][4].val = 4; f.board[0][3].assigned = 1; propagate(ptr, &f.board[0][3]);
	
	
//	f.board[0][0].r=1 ; f.board[0][1].l=-1 ;	f.board[1][3].r=1 ; f.board[1][4].l=-1 ;
//	f.board[2][0].r=-1 ; f.board[2][1].l=1 ;	f.board[3][2].r=1 ; f.board[3][3].l=-1 ;
//	f.board[3][3].r=1 ; f.board[3][4].l=-1 ;	f.board[5][3].r=-1 ; f.board[5][4].l=1 ;
//	f.board[5][4].r=-1 ; f.board[5][5].l=1 ;	f.board[1][1].d=1 ; f.board[2][1].u=-1 ;
//	f.board[1][5].d=-1 ; f.board[2][5].u=1 ;
//	f.board[0][4].val = 2; f.board[0][4].assigned = 1; propagate(ptr, &f.board[0][4]);
//	f.board[0][5].val = 6; f.board[0][5].assigned = 1; propagate(ptr, &f.board[0][5]);
//	f.board[1][5].val = 3; f.board[1][5].assigned = 1; propagate(ptr, &f.board[1][5]);
//	f.board[2][0].val = 3; f.board[2][0].assigned = 1; propagate(ptr, &f.board[2][0]);
//	f.board[3][2].val = 4; f.board[3][2].assigned = 1; propagate(ptr, &f.board[3][2]);
	
	



//	f.board[0][0].r=-1 ; f.board[0][1].l=1 ;	f.board[0][2].r=1 ; f.board[0][3].l=-1 ;
//	f.board[1][3].r=-1 ; f.board[1][4].l=1 ;	f.board[1][6].r=-1 ; f.board[1][7].l=1 ;
//	f.board[1][6].d=1 ; f.board[2][6].u=-1 ;	f.board[2][0].r=1 ; f.board[2][1].l=-1 ;
//	f.board[2][2].r=-1 ; f.board[2][3].l=1 ;	f.board[2][3].d=-1 ; f.board[3][3].u=1 ;
//	f.board[3][2].r=1 ; f.board[3][3].l=-1 ;	f.board[3][4].r=1 ; f.board[3][5].l=-1 ;
//	f.board[3][5].r=-1 ; f.board[3][6].l=1 ;	f.board[3][7].r=1 ; f.board[3][size-1].l=-1 ;
//	f.board[4][0].r=-1 ; f.board[4][1].l=1 ;	f.board[5][1].r=-1 ; f.board[5][2].l=1 ;
//	f.board[5][4].r=-1 ; f.board[5][5].l=1 ;	f.board[5][6].r=1 ; f.board[5][7].l=-1 ;
//	f.board[6][3].r=-1 ; f.board[6][4].l=1 ;	f.board[size-1][5].r=-1 ; f.board[size-1][6].l=1 ;
//	f.board[3][1].d=1 ; f.board[4][1].u=-1 ;	f.board[3][5].d=1 ; f.board[4][5].u=-1 ;
//	f.board[4][4].d=1 ; f.board[5][4].u=-1 ;	f.board[4][size-1].d=1 ; f.board[5][size-1].u=-1 ;
//	f.board[5][1].d=-1 ; f.board[6][1].u=1 ;	f.board[5][6].d=1 ; f.board[6][6].u=-1 ;
//	f.board[5][size-1].d=1 ; f.board[6][size-1].u=-1 ;	f.board[6][7].d=1 ; f.board[7][7].u=-1 ;
//	f.board[7][1].d=-1 ; f.board[size-1][1].u=1 ;	f.board[7][2].d=1 ; f.board[size-1][2].u=-1 ;
//	f.board[7][5].d=-1 ; f.board[size-1][5].u=1 ;	f.board[7][size-1].d=1 ; f.board[size-1][size-1].u=-1 ;
//	f.board[0][3].val = 7; f.board[0][3].assigned = 1; propagate(ptr, &f.board[0][3]);
//	f.board[0][4].val = 3; f.board[0][4].assigned = 1; propagate(ptr, &f.board[0][4]);
//	f.board[0][5].val = size-1; f.board[0][5].assigned = 1; propagate(ptr, &f.board[0][5]);
//	f.board[0][7].val = 5; f.board[0][7].assigned = 1; propagate(ptr, &f.board[0][7]);
//	f.board[1][2].val = 7; f.board[1][2].assigned = 1; propagate(ptr, &f.board[1][2]);
//	f.board[1][5].val = 2; f.board[1][5].assigned = 1; propagate(ptr, &f.board[1][5]);
//	f.board[2][5].val = size; f.board[2][5].assigned = 1; propagate(ptr, &f.board[2][5]);
//	f.board[3][3].val = 4; f.board[3][3].assigned = 1; propagate(ptr, &f.board[3][3]);
//	f.board[4][2].val = 1; f.board[4][2].assigned = 1; propagate(ptr, &f.board[4][2]);
//	f.board[4][6].val = 6; f.board[4][6].assigned = 1; propagate(ptr, &f.board[4][6]);
//	f.board[4][7].val = 4; f.board[4][7].assigned = 1; propagate(ptr, &f.board[4][7]);
//	f.board[5][6].val = 2; f.board[5][6].assigned = 1; propagate(ptr, &f.board[5][6]);
//	f.board[size-1][size-1].val = 6; f.board[size-1][size-1].assigned = 1; propagate(ptr, &f.board[size-1][size-1]);
	cout<<"原矩阵："<<endl;
	print(ptr);
	clock_t start,end;
	start=clock();
	FC(ptr, 0);
	end=clock();
	double endtime=(double)(end-start)/CLOCKS_PER_SEC;
	cout<<"计算已完成，用时："<<endtime*1000<<"ms."<<endl;
	cout << "搜索的节点数：" << nodes << "次" << endl;
	cout << "每个节点平均GAC时间：" << (double)(node_time*1000.00/(nodes)) << "ms" << endl;
	return 0;
}
