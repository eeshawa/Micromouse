import pickle
import numpy as np
index = 0 
# load data in

Hwalls = []
pickle_in = open(f'design/H{index}.csv','rb')
Hwalls = pickle.load(pickle_in)

Vwalls = []
pickle_in = open(f'design/V{index}.csv','rb')
Vwalls = pickle.load(pickle_in)

def checkindex(i,j):
    if 0 <= i <= 13 and 0 <= j <= 13:
        return True
    else:
        return False




def run_floodfill():
    ffill=np.zeros(196 , dtype=int).reshape(14,14)
    ffill[:,:]=-1
    ffill[6:8,6:8]=0  #finish position

    queue=[[6,6],[6,7],[7,6],[7,7]]
    while True:

        if not queue:
            break

        x=queue[0][0]
        y=queue[0][1]
        del queue[0]

        mother_value=ffill[x][y]  #mothercell , up,down,left,right of this cell will be changed

        if checkindex(x,y-1) and ffill[x][y-1]==-1 and Vwalls[x][y]==0: #left
            ffill[x][y-1]=mother_value+1 
            queue.append([x,y-1])

        if checkindex(x-1,y) and ffill[x-1][y]==-1 and Hwalls[x][y]==0 : #up
            ffill[x-1][y]=mother_value+1 
            queue.append([x-1,y])

        if checkindex(x,y+1) and ffill[x][y+1]==-1 and Vwalls[x][y+1]==0: #right 
            ffill[x][y+1]=mother_value+1 
            queue.append([x,y+1])
    
        if checkindex(x+1,y) and ffill[x+1][y]==-1 and Hwalls[x+1][y]==0: #down
            ffill[x+1][y]=mother_value+1 
            queue.append([x+1,y])
    
    print(ffill)

if __name__=='__main__':
    run_floodfill()
