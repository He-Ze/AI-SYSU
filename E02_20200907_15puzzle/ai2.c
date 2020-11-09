#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<math.h>
#include<time.h>

int move[4][2]={{-1,0},{0,-1},{0,1},{1,0}};
int map[4][4],map_og[4][4];
int map2[4*4]={0,5,15,14,7,9,6,13,1,2,12,10,8,11,4,3 };
//int map2[4*4]={11,3,1,7,4,6,8,2,15,9,10,13,14,12,5,0 };
//int map2[4*4]={2,10,3,4,1,9,6,7,13,5,11,8,0,14,15,12 };
int limit,path[100];
int flag,length;
int goal[16][2]= {{3,3},{0,0},{0,1}, {0,2},{0,3}, {1,0},{1,1}, {1,2}, {1,3},{2,0}, {2,1}, {2,2},{2,3},{3,0},{3,1},{3,2}};

void change(int*a,int*b){
    int tmp;
    tmp=*a;
    *a=*b;
    *b=tmp;
}

int h(int a[][4]){
    int i,j,cost=0;
    for(i=0;i<4;i++){
        for(j=0;j<4;j++){
            int w=map[i][j];
            cost+=abs(i-goal[w][0])+abs(j-goal[w][1]);
        }
    }
    return cost;
}

void ida_star(int sx,int sy,int len,int pre_move){
    int i,nx,ny;
	if(flag)
		return;
    int dv=h(map);
	if(len==limit){
		if(dv==0){
			flag=1;
			length=len;
			return;
		}
		else
			return;
	}
	else if(len<limit){
		if(dv==0){
			flag=1;
			length=len;
			return;
		}
	}
    for(i=0;i<4;i++){
		if(i+pre_move==3&&len>0)
			continue;
        nx=sx+move[i][0];
        ny=sy+move[i][1];
		if(0<=nx&&nx<4 && 0<=ny&&ny<4){
            change(&map[sx][sy],&map[nx][ny]);
            int p=h(map);
			if(p+len<=limit&&!flag){
                path[len]=i;
                ida_star(nx,ny,len+1,i);
				if(flag)
                    return;
            }
            change(&map[sx][sy],&map[nx][ny]);
        }
    }
}
int main(){
    int i=0,j,k,l,m,sx,sy,xx,yy;
    char c,g;
	clock_t start,end;
	flag=0,length=0;
	memset(path,-1,sizeof(path));
	for(i=0;i<16;i++){
		if(map2[i]==0){
			map[i/4][i%4]=0;
			map_og[i/4][i%4]=map[i/4][i%4];
			sx=i/4;sy=i%4;
			xx=i/4;yy=i%4;
		}
		else{
			map[i/4][i%4]=map2[i];
			map_og[i/4][i%4]=map[i/4][i%4];
		}
	}
	printf("原矩阵为:\n");
	for (i=0; i<4; i++) {
		for (int y=0; y<4; y++)
			printf("%d ",map[i][y]);
		printf("\n");
	}
	start=clock();
	limit=h(map);
	while(!flag&&length<=50){
		ida_star(sx,sy,0,0);
		if(!flag)
			limit++;
	}
	end=clock();
	printf("现矩阵为：\n");
	for (i=0; i<4; i++) {
		for (int y=0; y<4; y++)
			printf("%d ",map[i][y]);
		printf("\n");
	}
	printf("最短路径长度：%d\n",length);
	printf("最短路径需要调换顺序的数字为：\n");
	for (i=0; i<length; i++) {
		if(path[i]==0){
			printf("%d ",map_og[xx-1][yy]);
			change(&map_og[xx][yy],&map_og[xx-1][yy]);
			xx-=1;
		}
		else if(path[i]==1){
			printf("%d ",map_og[xx][yy-1]);
			change(&map_og[xx][yy],&map_og[xx][yy-1]);
			yy-=1;
		}
		else if(path[i]==2){
			printf("%d ",map_og[xx][yy+1]);
			change(&map_og[xx][yy],&map_og[xx][yy+1]);
			yy+=1;
		}
		else if(path[i]==3){
			printf("%d ",map_og[xx+1][yy]);
			change(&map_og[xx][yy],&map_og[xx+1][yy]);
			xx+=1;
		}
	}
	double endtime=(double)(end-start)/CLOCKS_PER_SEC;
	printf("\n总用时：%f s.\n",endtime);
    return 0;
}
