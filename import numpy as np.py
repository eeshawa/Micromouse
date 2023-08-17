import numpy as np
import pickle
# import miocromouse_maze_designer as ds
maze = []
#initialize mach settings
index = 0


# load data in
Hwalls = []
pickle_in = open(f'design/H{index}.csv','rb')
Hwalls = pickle.load(pickle_in)

Vwalls = []
pickle_in = open(f'design/V{index}.csv','rb')
Vwalls = pickle.load(pickle_in)

H_walls = np.array(Hwalls)
V_walls = np.array(Vwalls)

length = len(Vwalls)

#create maze matries
maze = -1 * np.ones(length**2).reshape(length, length)
# V_walls = np.zeros(length**2 + length).reshape(length, length + 1)#[cell][wall]
# H_walls = np.zeros(length**2 + length).reshape(length + 1, length)#[wall][cell]

#make destination to 0
if length % 2 == 1:
    maze[length // 2, length // 2] = 0
elif length % 2 == 0:
    maze[length // 2, length // 2] = 0
    maze[length // 2, length // 2 - 1] = 0
    maze[length // 2 - 1, length // 2] = 0
    maze[length // 2 - 1, length // 2 - 1] = 0


def Get_maze_wall():
    return H_walls, V_walls

def FludFill(maze, V_walls, H_walls):
    for value in range(200):
            #read indexes
            # indexes = []

            # print('checking for', value)

            for i in range(maze.shape[0]):
                for j in range(maze.shape[1]):
                    if maze[i][j] == value:
                        # indexes.append((i, j))
                        try:
                            #check vertical walls
                            if V_walls[i, j + 1] != -1 and maze[i, j + 1] == -1:
                                maze[i, j + 1] = value + 1
                        except:
                            pass

                        try:
                            if V_walls[i, j] != -1 and maze[i, j - 1] == -1:
                                maze[i, j - 1] = value + 1
                        except:
                            pass 
                        try: 
                            #check Horizontal walls
                            if H_walls[i + 1, j] != -1 and maze[i + 1, j] == -1:
                                maze[i + 1, j] = value + 1
                        except:
                            pass
                        try:
                            if H_walls[i, j] != -1 and maze[i - 1, j] == -1:
                                maze[i - 1, j] = value + 1
                        except:
                            pass
            # print(maze)
    return maze


if __name__ == "__main__":
    
    print(FludFill(maze, V_walls, H_walls))