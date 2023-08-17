import fludfill as ff
import numpy as np
import time

#game variables

direct = {  'UP'      : 0,
            'RIGHT'   : 1,
            'DOWN'    : 2,
            'LEFT'    : 3,
            }
X_direction = 1
Y_direction = 1


H_walls, V_walls = ff.Get_maze_wall()
step = 1
length = len(V_walls)

#create empty wall lists
#maze matrix
MAZE = -1 * np.ones(length**2).reshape(length, length)

MV_walls = np.zeros(length**2 + length).reshape(length, length + 1)#[cell][wall]
MH_walls = np.zeros(length**2 + length).reshape(length + 1, length)#[wall][cell]
mouse = np.zeros(length**2).reshape(length, length)
mouse_row = 5
mouse_col = 4
#make destination to 0
if length % 2 == 1:
    MAZE[length // 2, length // 2] = 0
elif length % 2 == 0:
    MAZE[length // 2, length // 2] = 0
    MAZE[length // 2, length // 2 - 1] = 0
    MAZE[length // 2 - 1, length // 2] = 0
    MAZE[length // 2 - 1, length // 2 - 1] = 0
EMPTY_MAZE = MAZE
def Print_grid(mouse_row, mouse_col):
    # mouse = np.zeros(length**2).reshape(length, length)
    for i, path in enumerate(mouse):
        for j, road in enumerate(path):
            if road == 888:
                mouse[i][j] = step
    mouse[mouse_row, mouse_col] = 888
    
    print(mouse, '\n')
    # print(MAZE, '\n')

def UpdateWalls():
    #get walls inputs according to the muse possition
    for xdirect in (1, -1):
        if V_walls[mouse_row][mouse_col + (1 + xdirect)//2] == -1:
            MV_walls[mouse_row][mouse_col + (1 + xdirect)//2] = -1

    for ydirect in (1, -1):
        if H_walls[mouse_row + (1 + ydirect)//2][mouse_col] == -1:
            MH_walls[mouse_row + (1 + ydirect)//2][mouse_col] = -1           

def move(MAZE, mouse_row, mouse_col, run, MV_walls, MH_walls):
    # print("hi")
    #check X direction
    if len(X_direction) == 1:
        mouse_col += 1 * X_direction[0]
        # print('1')
    elif len(X_direction) > 1:
        mouse_col += 1 * X_direction[1]#can select any
        # print('2')
    elif len(Y_direction) == 1:
        mouse_row += 1 * Y_direction[0]
        # print('3')
    elif len(Y_direction) > 1:
        mouse_row += 1 * Y_direction[1]#can select any
        # print('4')
    elif MAZE[mouse_row, mouse_col] == 0:
        run = False
    elif len(X_direction) == 0 and len(Y_direction) == 0:
        MAZE = ff.FludFill(np.array(EMPTY_MAZE), np.array(MV_walls), np.array(MH_walls))
        print(MV_walls,'\n', MH_walls)
        # print('here')
    
    return MAZE, mouse_row, mouse_col, run


def CheckDirection(MAZE, mouse_row, mouse_col, MH_walls, MV_walls):
    xdirections = []
    for xdirect in (1, -1):
        if MAZE[mouse_row][mouse_col] == MAZE[mouse_row][(mouse_col + 1 * xdirect)%length] + 1 and MV_walls[mouse_row][mouse_col + (1 + xdirect)//2] != -1:
            xdirections.append(xdirect)

    ydirections = []
    for ydirect in (1, -1):
        if MAZE[mouse_row][mouse_col] == MAZE[(mouse_row + 1 * ydirect)%length][mouse_col] + 1 and MH_walls[mouse_row + (1 + ydirect)//2][mouse_col] != -1:
            ydirections.append(ydirect)
    
    return xdirections, ydirections
MAZE = ff.FludFill(np.array(EMPTY_MAZE), np.array(MV_walls), np.array(MH_walls))
Print_grid(mouse_row, mouse_col)

run = True
while run:
    # print(mouse, '\n')
    UpdateWalls()
    X_direction, Y_direction = CheckDirection(MAZE, mouse_row, mouse_col, MH_walls, MV_walls)
    
    MAZE, mouse_row, mouse_col, run = move(MAZE, mouse_row, mouse_col, run, MV_walls, MH_walls)
    Print_grid(mouse_row, mouse_col)
    step += 1
    time.sleep(3)
    # if mouse_col <= length -1:
    #     mouse_row, mouse_col = move(maze, mouse_row, mouse_col)
    # else:
    #     run= False


# print(ff.FludFill(maze, V_walls, H_walls))