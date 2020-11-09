<h1 align=center>E03 Othello Game (α − β pruning)</h1>

| 姓名 |   学号   |    日期    |
| :--: | :------: | :--------: |
| 何泽 | 18340052 | 2020.09.20 |

<h2 align=center>目录</h2>

[TOC]

## 1 Othello

> Othello (or Reversi) is a strategy board game for two players, played on an 8 × 8 uncheckered board. There are sixty-four identical game pieces called disks (often spelled ”discs”), which are light on one side and dark on the other. Please see figure 1.
>
> Players take turns placing disks on the board with their assigned color facing up. During a play, any disks of the opponent’s color that are in a straight line and bounded by the disk just placed and another disk of the current player’s color are turned over to the current player’s color.
>
> The object of the game is to have the majority of disks turned to display your color when the last playable empty square is filled.
>
> You can refer to http://www.tothello.com/html/guideline_of_reversed_othello.html for more information of guideline, meanwhile, you can download the software to have a try from http://www.tothello.com/html/download.html. The game installer tothello trial setup.exe can also be found in the current folder.
>
> <img src="/Users/heze/Library/Application Support/typora-user-images/image-20200915083717983.png" alt="image-20200915083717983" style="zoom:50%;" />

## 2 Tasks

> 1. In order to reduce the complexity of the game, we think the board is 6 × 6.
>
> 2. There are several evaluation functions that involve many aspects, you can turn to http://www.cs.cornell.edu/~yuli/othello/othello.html for help. In order to reduce the difficulty of the task, I have gaven you some hints of evaluation function in the file Heuristic Function for Reversi (Othello).cpp.
>
> 3. Please choose an appropriate evaluation function and use min-max and α − β prunning to implement the Othello game. The framework file you can refer to is Othello.cpp. Of course, I wish your program can beat the computer.
>
> 4. Write the related codes and take a screenshot of the running results in the file named E03_StudentNumber.pdf, and send it to ai2020@foxmail.com, the deadline is 2020.09.20 23:59:59.

## 3 Codes

- 我是保留了原来的评价函数，然后在提供的新的评价函数基础上重写了一个新的评价函数，然后让这两种评价函数进行PK

- 对于min-max 和 α − β 剪枝算法，我使用的就是提供的代码

  ```c++
  if (num == 0) {   /* 无处落子 */
          if (board->Rule(board, (enum Option) - player)){    /* 对方可以落子,让对方下.*/
              Othello tempBoard;
              Do nextChoice;
              Do *pNextChoice = &nextChoice;
              board->Copy(&tempBoard, board);
              pNextChoice = Find(&tempBoard, (enum Option) - player, step - 1, -max, -min, pNextChoice,who_judge);
              choice->score = -pNextChoice->score;
              choice->pos.first = -1;
              choice->pos.second = -1;
              return choice;
          }
          else{    /* 对方也无处落子,游戏结束. */
              int value = WHITE*(board->whiteNum) + BLACK*(board->blackNum);
              if (player*value>0)
                  choice->score = MAX - 1;
              else if (player*value<0)
                  choice->score = -MAX + 1;
              else
                  choice->score = 0;
              return choice;
          }
      }
  	
      if (step <= 0){
  		if (who_judge)
  			choice->score = board->MyJudge(board, player);
  		else
  			choice->score = board->Judge(board, player);
  		return choice;
  	}
  
      allChoices = (Do *)malloc(sizeof(Do)*num);
      k = 0;
      for (i = 0; i<6; i++){
          for (j = 0; j<6; j++){
              if (i == 0 || i == 5 || j == 0 || j == 5){
                  if (board->cell[i][j].color == SPACE && board->cell[i][j].stable){
                      allChoices[k].score = -MAX;
                      allChoices[k].pos.first = i;
                      allChoices[k].pos.second = j;
                      k++;
                  }
              }
          }
      }
      for (i = 0; i<6; i++){
          for (j = 0; j<6; j++){
              if ((i == 2 || i == 3 || j == 2 || j == 3) && (i >= 2 && i <= 3 && j >= 2 && j <= 3)){
                  if (board->cell[i][j].color == SPACE && board->cell[i][j].stable){
                      allChoices[k].score = -MAX;
                      allChoices[k].pos.first = i;
                      allChoices[k].pos.second = j;
                      k++;
                  }
              }
          }
      }
      for (i = 0; i<6; i++){
          for (j = 0; j<6; j++){
              if ((i == 1 || i == 4 || j == 1 || j == 4) && (i >= 1 && i <= 4 && j >= 1 && j <= 4)){
                  if (board->cell[i][j].color == SPACE && board->cell[i][j].stable){
                      allChoices[k].score = -MAX;
                      allChoices[k].pos.first = i;
                      allChoices[k].pos.second = j;
                      k++;
                  }
              }
          }
      }
      for (k = 0; k<num; k++){
          Othello tempBoard;
          Do thisChoice, nextChoice;
          Do *pNextChoice = &nextChoice;
          thisChoice = allChoices[k];
          board->Copy(&tempBoard, board);
          board->Action(&tempBoard, &thisChoice, player);
          pNextChoice = Find(&tempBoard, (enum Option) - player, step - 1, -max, -min, pNextChoice,who_judge);
          thisChoice.score = -pNextChoice->score;
  
          if (thisChoice.score>min && thisChoice.score<max){    /* 可以预计的更优值 */
              min = thisChoice.score;
              choice->score = thisChoice.score;
              choice->pos.first = thisChoice.pos.first;
              choice->pos.second = thisChoice.pos.second;
          }
          else if (thisChoice.score >= max) {   /* 好的超乎预计 */
              choice->score = thisChoice.score;
              choice->pos.first = thisChoice.pos.first;
              choice->pos.second = thisChoice.pos.second;
              break;
          }
          /* 不如已知最优值 */
      }
  ```

- 而评价函数我是在提供的基础上改的，将8x8改为了6x6，并去掉了最后的l

  ```c++
  double Othello::MyJudge(Othello *board, enum Option player)
  {
  	int my_tiles = 0, opp_tiles = 0, i, j, k, my_front_tiles = 0, opp_front_tiles = 0, x, y;
  	double p = 0, c = 0, l = 0, m = 0, f = 0, d = 0;
  	enum Option my_color = player;
  	enum Option opp_color = (enum Option) - player;
  
  	// eight directions
  	int X1[] = {-1, -1, 0, 1, 1, 1, 0, -1};
  	int Y1[] = {0, 1, 1, 1, 0, -1, -1, -1};
  	// aprior weights for each movement
  	int V[6][6]= {{20, -3, 11, 11, -3, 20},{-3, -7, -4, -4, -7, -3},{11, -4, 2, 2, -4, 11},{11, -4, 2, 2, -4, 11},{-3, -7, -4, -4, -7, -3},{20, -3, 11, 11, -3, 20}};
  	
  	// Piece difference
  	for (i = 0; i < 6; i++)
  		for (j = 0; j < 6; j++){
  			// count how many tiles are occupied
  			if (board->cell[i][j].color == my_color){
  				d += V[i][j];
  				my_tiles++;
  			}
  			else if (board->cell[i][j].color == opp_color){
  				d -= V[i][j];
  				opp_tiles++;
  			}
  			// find the difference in eight directions
  			if (board->cell[i][j].color != SPACE){
  				for (k = 0; k < 8; k++){
  					x = i + X1[k];
  					y = j + Y1[k];
  					if (x >= 0 && x < 6 && y >= 0 && y < 6 && board->cell[x][y].color == SPACE){
  						if (board->cell[i][j].color == my_color)
  							my_front_tiles++;
  						else
  							opp_front_tiles++;
  						break;
  					}
  				}
  			}
  		}
  	// calculate the proportions
  	if (my_tiles > opp_tiles)
  		p = (100.0 * my_tiles) / (my_tiles + opp_tiles);
  	else if (my_tiles < opp_tiles)
  		p = -(100.0 * opp_tiles) / (my_tiles + opp_tiles);
  	else
  		p = 0;
  
  	if (my_front_tiles > opp_front_tiles)
  		f = -(100.0 * my_front_tiles) / (my_front_tiles + opp_front_tiles);
  	else if (my_front_tiles < opp_front_tiles)
  		f = (100.0 * opp_front_tiles) / (my_front_tiles + opp_front_tiles);
  	else
  		f = 0;
  
  	// Corner occupancy
  	my_tiles = opp_tiles = 0;
  	if (board->cell[0][0].color == my_color)
  		my_tiles++;
  	else if (board->cell[0][0].color == opp_color)
  		opp_tiles++;
  	if (board->cell[0][5].color == my_color)
  		my_tiles++;
  	else if (board->cell[0][5].color == opp_color)
  		opp_tiles++;
  	if (board->cell[5][0].color == my_color)
  		my_tiles++;
  	else if (board->cell[5][0].color == opp_color)
  		opp_tiles++;
  	if (board->cell[5][5].color == my_color)
  		my_tiles++;
  	else if (board->cell[5][5].color == opp_color)
  		opp_tiles++;
  	c = 25 * (my_tiles - opp_tiles);
  	
  	// Mobility
  	// The more tiles can be moved on, the better
  	my_tiles = Rule(board, my_color);
  	opp_tiles = Rule(board, opp_color);
  	if (my_tiles > opp_tiles)
  		m = (100.0 * my_tiles) / (my_tiles + opp_tiles);
  	else if (my_tiles < opp_tiles)
  		m = -(100.0 * opp_tiles) / (my_tiles + opp_tiles);
  	else
  		m = 0;
  	
  	// final weighted score (magic numbers!)
  	double score = (10 * p) + (801.724 * c) +  (78.922 * m) + (74.396 * f) + (10 * d);
  	return score;
  }
  ```

## 4 Results

> 使用两种算法进行PK，可以看到在新的评价函数下的算法打败了原来的，下面记录了每次的过程，我为我的算法选了白棋，原来的是黑棋

<img src="/Users/heze/Library/Mobile Documents/com~apple~CloudDocs/大三上/人工智能实验/E03_20190911_Othello/截图/截屏2020-09-15 14.46.38.png" alt="截屏2020-09-15 14.46.38" style="zoom: 50%;" />

<img src="/Users/heze/Library/Mobile Documents/com~apple~CloudDocs/大三上/人工智能实验/E03_20190911_Othello/截图/截屏2020-09-15 14.47.07.png" alt="截屏2020-09-15 14.47.07" style="zoom:50%;" />

<img src="/Users/heze/Library/Mobile Documents/com~apple~CloudDocs/大三上/人工智能实验/E03_20190911_Othello/截图/截屏2020-09-15 14.47.29.png" alt="截屏2020-09-15 14.47.29" style="zoom:50%;" />

<img src="/Users/heze/Library/Mobile Documents/com~apple~CloudDocs/大三上/人工智能实验/E03_20190911_Othello/截图/截屏2020-09-15 14.47.48.png" alt="截屏2020-09-15 14.47.48" style="zoom:50%;" />

<img src="/Users/heze/Library/Mobile Documents/com~apple~CloudDocs/大三上/人工智能实验/E03_20190911_Othello/截图/截屏2020-09-15 14.48.05.png" alt="截屏2020-09-15 14.48.05" style="zoom:50%;" />

<img src="/Users/heze/Library/Mobile Documents/com~apple~CloudDocs/大三上/人工智能实验/E03_20190911_Othello/截图/截屏2020-09-15 14.48.22.png" alt="截屏2020-09-15 14.48.22" style="zoom:50%;" />

<img src="/Users/heze/Library/Mobile Documents/com~apple~CloudDocs/大三上/人工智能实验/E03_20190911_Othello/截图/截屏2020-09-15 14.48.42.png" alt="截屏2020-09-15 14.48.42" style="zoom:50%;" />

<img src="/Users/heze/Library/Mobile Documents/com~apple~CloudDocs/大三上/人工智能实验/E03_20190911_Othello/截图/截屏2020-09-15 14.48.58.png" alt="截屏2020-09-15 14.48.58" style="zoom:50%;" />

<img src="/Users/heze/Library/Mobile Documents/com~apple~CloudDocs/大三上/人工智能实验/E03_20190911_Othello/截图/截屏2020-09-15 14.49.14.png" alt="截屏2020-09-15 14.49.14" style="zoom:50%;" />

<img src="/Users/heze/Library/Mobile Documents/com~apple~CloudDocs/大三上/人工智能实验/E03_20190911_Othello/截图/截屏2020-09-15 14.49.32.png" alt="截屏2020-09-15 14.49.32" style="zoom:50%;" />

<img src="/Users/heze/Library/Mobile Documents/com~apple~CloudDocs/大三上/人工智能实验/E03_20190911_Othello/截图/截屏2020-09-15 14.49.46.png" alt="截屏2020-09-15 14.49.46" style="zoom:50%;" />

<img src="/Users/heze/Library/Mobile Documents/com~apple~CloudDocs/大三上/人工智能实验/E03_20190911_Othello/截图/截屏2020-09-15 14.50.01.png" alt="截屏2020-09-15 14.50.01" style="zoom:50%;" />

<img src="/Users/heze/Library/Mobile Documents/com~apple~CloudDocs/大三上/人工智能实验/E03_20190911_Othello/截图/截屏2020-09-15 14.50.17.png" alt="截屏2020-09-15 14.50.17" style="zoom:50%;" />

<img src="/Users/heze/Library/Mobile Documents/com~apple~CloudDocs/大三上/人工智能实验/E03_20190911_Othello/截图/截屏2020-09-15 14.50.33.png" alt="截屏2020-09-15 14.50.33" style="zoom:50%;" />

<img src="/Users/heze/Library/Mobile Documents/com~apple~CloudDocs/大三上/人工智能实验/E03_20190911_Othello/截图/截屏2020-09-15 14.50.48.png" alt="截屏2020-09-15 14.50.48" style="zoom:50%;" />

<img src="/Users/heze/Library/Mobile Documents/com~apple~CloudDocs/大三上/人工智能实验/E03_20190911_Othello/截图/截屏2020-09-15 14.51.04.png" alt="截屏2020-09-15 14.51.04" style="zoom:50%;" />

<img src="/Users/heze/Library/Mobile Documents/com~apple~CloudDocs/大三上/人工智能实验/E03_20190911_Othello/截图/截屏2020-09-15 14.51.17.png" alt="截屏2020-09-15 14.51.17" style="zoom:50%;" />

程序结束，白棋胜