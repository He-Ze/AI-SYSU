def DFS(map, x, y, used):
    global res
    if len(res) and len(used) > len(res):
        return
    if x == -1 or y == -1 or x == len(map) or y == len(map[0]) or map[x][y] == '1' or (x, y) in used:
        return
    elif map[x][y] == 'E':
        print('\033[1;30;46m %d \033[0m' % (len(used) + 1), end="")
        if len(used) + 1 < len(res) or len(res) == 0:
            res = used
            res.append((x, y))
        return
    else:
        used.append((x, y))
        DFS(map, x + 1, y, used[:])
        DFS(map, x - 1, y, used[:])
        DFS(map, x, y + 1, used[:])
        DFS(map, x, y - 1, used[:])
        used.remove(used[-1])


def print_result(map, path):
    print(' ')
    print('\033[1;30;46m                   最短路径长度： %d                   \033[0m' % len(path))
    print('图示：')
    for i in range(len(map)):
        for j in range(len(map[i])):
            if (i, j) in path[1:-1]:
                print('\033[1;32;43m  \033[0m', end="")
            elif map[i][j] == "1":
                print('\033[1;33;44m  \033[0m', end="")
            elif map[i][j] == "S":
                print('\033[1;30;41mS \033[0m', end="")
            elif map[i][j] == "E":
                print('\033[1;30;45mE \033[0m', end="")
            else:
                print("  ", end="")
        print("")
    print("")


if __name__ == "__main__":
    print('\033[1;30;46m          何泽-18340052-人工智能实验一：Maze            \033[0m')
    print('\033[1;30;44m  蓝色是墙  \033[0m', end="")
    print('\033[1;30;41m  红色是起始点  \033[0m', end="")
    print('\033[1;30;45m  紫色是终点  \033[0m', end="")
    print('\033[1;30;43m  黄色是最短路径  \033[0m')
    print('\033[1;30;46m  历史路径长度：  \033[0m', end="")
    Maze = []
    res = []
    with open("./MazeData.txt", 'r') as Maze_og:
        for i in Maze_og.readlines():
            if i[0] == '1' or i[0] == '0':
                Maze.append(i[:-1])

    for i in range(len(Maze)):
        for j in range(len(Maze[i])):
            if Maze[i][j] == 'S':
                DFS(Maze, i, j, [])
                break

    print_result(Maze, res)