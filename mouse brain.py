#mouse brain 
'''prioratize derections . west>north>east>south'''
import pickle
import time
import numpy as np
import turtle
#t=turtle.Pen()

index = 3
# load data in
Hwalls = []
pickle_in = open(f'design/H{index}.csv','rb')
Hwalls = pickle.load(pickle_in)

Vwalls = []
pickle_in = open(f'design/V{index}.csv','rb')
Vwalls = pickle.load(pickle_in)

'''
Hwalls=np.zeros(210, dtype=int).reshape(15,14)
Hwalls[0,:]=1
Hwalls[14,:]=1
#below here you can add walls horizontally (sides of the robot)
Hwalls[6][6]=1
Hwalls[8][6]=1
Hwalls[8][7]=1

Vwalls=np.zeros(210, dtype=int).reshape(14,15)
Vwalls[:,0]=1
Vwalls[:,14]=1
#below here you can add walls vertically(front and back of the robot)
Vwalls[6][6]=1
Vwalls[7][6]=1
'''
dir=0
x=13
y=0


vwall_senosr=np.zeros(210, dtype=int).reshape(14,15)
vwall_senosr[:,0]=-1
vwall_senosr[:,14]=-1

hwall_senosr=np.zeros(210, dtype=int).reshape(15,14)
hwall_senosr[0,:]=-1
hwall_senosr[14,:]=-1

def checkindex(i,j):
    if 0 <= i <= 13 and 0 <= j <= 13:
        return True
    else:
        return False

def run_floodfill():
    global ffill
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

        if checkindex(x,y-1) and ffill[x][y-1]==-1 and vwall_senosr[x][y]==0: #left
            ffill[x][y-1]=mother_value+1 
            queue.append([x,y-1])

        if checkindex(x-1,y) and ffill[x-1][y]==-1 and hwall_senosr[x][y]==0 : #up
            ffill[x-1][y]=mother_value+1 
            queue.append([x-1,y])

        if checkindex(x,y+1) and ffill[x][y+1]==-1 and vwall_senosr[x][y+1]==0: #right 
            ffill[x][y+1]=mother_value+1 
            queue.append([x,y+1])
    
        if checkindex(x+1,y) and ffill[x+1][y]==-1 and hwall_senosr[x+1][y]==0: #down
            ffill[x+1][y]=mother_value+1 
            queue.append([x+1,y])
    
    #print(ffill)

def run_floodfill_reverse():
    global ffill
    ffill=np.zeros(196 , dtype=int).reshape(14,14)
    ffill[:,:]=-1
    ffill[13,0]=0  #finish position

    queue=[[13,0]]
    while True:

        if not queue:
            break

        x=queue[0][0]
        y=queue[0][1]
        del queue[0]

        mother_value=ffill[x][y]  #mothercell , up,down,left,right of this cell will be changed

        if checkindex(x,y-1) and ffill[x][y-1]==-1 and vwall_senosr[x][y]==0: #left
            ffill[x][y-1]=mother_value+1 
            queue.append([x,y-1])

        if checkindex(x-1,y) and ffill[x-1][y]==-1 and hwall_senosr[x][y]==0 : #up
            ffill[x-1][y]=mother_value+1 
            queue.append([x-1,y])

        if checkindex(x,y+1) and ffill[x][y+1]==-1 and vwall_senosr[x][y+1]==0: #right 
            ffill[x][y+1]=mother_value+1 
            queue.append([x,y+1])
    
        if checkindex(x+1,y) and ffill[x+1][y]==-1 and hwall_senosr[x+1][y]==0: #down
            ffill[x+1][y]=mother_value+1 
            queue.append([x+1,y])

def predict_move():
    global turns
    global next_move_x
    global next_move_y
    #below next move is not accepted. its just checking. after the checking if there is no wall detected to obstruct the parth,
    #move will be accepted\
    mother_value=ffill[x][y]

    if checkindex(x,y-1) and ffill[x][y-1]!=-1 and vwall_senosr[x][y]==0 and mother_value>ffill[x][y-1]: #west
        next_move_x=x
        next_move_y=y-1
        print('turn west')
        turns=3

    elif checkindex(x-1,y) and ffill[x-1][y]!=-1 and hwall_senosr[x][y]==0 and mother_value>ffill[x-1][y] : #north
        next_move_x=x-1
        next_move_y=y
        print('move north')
        turns=0
    elif checkindex(x,y+1) and ffill[x][y+1]!=-1 and vwall_senosr[x][y+1]==0 and mother_value>ffill[x][y+1] : #East 
        next_move_x=x
        next_move_y=y+1
        print('turn east')
        turns=1

    elif checkindex(x+1,y) and ffill[x+1][y]!=-1 and hwall_senosr[x+1][y]==0 and mother_value>ffill[x+1][y]: #South
        next_move_x=x+1
        next_move_y=y
        print('move south')
        turns=2

def wall_detection():
    if dir==0:
        vwall_senosr[x][y]=Vwalls[x][y]
        hwall_senosr[x][y]=Hwalls[x][y]
        vwall_senosr[x][y+1]=Vwalls[x][y+1]
    elif dir==1:
        hwall_senosr[x][y]=Hwalls[x][y]
        vwall_senosr[x][y+1]=Vwalls[x][y+1]
        hwall_senosr[x+1][y]=Hwalls[x+1][y]
    elif dir==2:
        vwall_senosr[x][y+1]=Vwalls[x][y+1]
        hwall_senosr[x+1][y]=Hwalls[x+1][y]
        vwall_senosr[x][y]=Vwalls[x][y]
    elif dir==3:
        hwall_senosr[x+1][y]=Hwalls[x+1][y]
        vwall_senosr[x][y]=Vwalls[x][y]
        hwall_senosr[x][y]=Hwalls[x][y]

def move_acception():
    if turns==0 and hwall_senosr[x][y]==0 :
        print('move accepted')      
    elif turns==1 and vwall_senosr[x][y+1]==0:
        print('move accepted')
    elif turns==2 and hwall_senosr[x+1][y]==0:
        print('move accepted')
    elif turns==3 and vwall_senosr[x][y]==0:
        print('move accepted')
    else:
        print('move declined')
        print(ffill)
        run_floodfill()
        print('new floodfill:')
        print(ffill)
        predict_move()
        move_acception()
   
def move_acception_reverse():

    if turns==0 and hwall_senosr[x][y]==0 :
        print('move accepted')      
    elif turns==1 and vwall_senosr[x][y+1]==0:
        print('move accepted')
    elif turns==2 and hwall_senosr[x+1][y]==0:
        print('move accepted')
    elif turns==3 and vwall_senosr[x][y]==0:
        print('move accepted')
    else:
        print('move declined')
        print(ffill)
        run_floodfill_reverse()
        print('new floodfill reverse:')
        print(ffill)
        predict_move()
        move_acception_reverse() 

def draw_path():
    t.pencolor(0,0,0)
    t.right(90*(turns-dir))
    t.fd(25)
    t.pencolor(1,1,1)
    t.fd(10)

def draw_path_reverse():
    t.pencolor(1,0,0)
    t.right(90*(turns-dir))
    t.fd(25)
    t.pencolor(1,1,1)
    t.fd(10)

def draw_path_final():
    t.pencolor(0,1,0)
    t.right(90*(turns-dir))
    t.fd(25)
    t.pencolor(1,1,1)
    t.fd(10)

def turtle_placement():
    t.pencolor(1,1,1)
    t.right(-180)
    t.fd(300)
    t.left(90)
    t.fd(220)
    t.right(180)

turtle_placement()
for i in range(3):    
    run_floodfill()
    while ffill[x][y]!=0:
        predict_move()
        wall_detection()
        move_acception()
        x=next_move_x
        y=next_move_y
        draw_path()
        dir=turns
    
    print(ffill)
    print('Congratz , You have reached the center')
    t.pencolor('red')

    run_floodfill_reverse()
    while ffill[x][y]!=0:
        predict_move()
        wall_detection()
        move_acception_reverse()
        x=next_move_x
        y=next_move_y
        draw_path_reverse()
        dir=turns
    
    print(ffill)
    print('Congratz , You have reached the Start point')
    time.sleep(1)
t.pencolor('red')
time.sleep(1)

print('Final run is about start in 2s')
time.sleep(2)
run_floodfill()
while ffill[x][y]!=0:
    predict_move()
    wall_detection()
    move_acception()
    x=next_move_x
    y=next_move_y
    draw_path_final()
    dir=turns
    
print(ffill)
print('Congratz , You have reached the center')
time.sleep(5)




