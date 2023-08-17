import pygame
import numpy as np
import pickle

pygame.init()
length = 6
#game window

SIZE = int(input('Enter window size(50 to 100): '))
SCREEN_WIDTH = int(8 * SIZE // 1)
SCREEN_HEIGHT = int(6.4 * SIZE // 1)
SIDE_MARGINE = int(3 * SIZE // 1)
Hight = int(5.6 * SIZE)
Width = int(5.6 * SIZE)
wall_length = Hight // length

font = pygame.font.SysFont('Futura', int(0.3 * SIZE // 1))

#define colours
GREEN = (144, 201, 120)
WHITE = (180, 180, 200)
RED = (200, 25, 25)
BLACK = (0, 0, 0)

draw = True
index = 0

#maze matrix
V_walls = np.zeros(length**2 + length , dtype=int ).reshape(length, length + 1)#[cell][wall]
H_walls = np.zeros(length**2 + length , dtype=int).reshape(length + 1, length)#[wall][cell]

white_v = -1 * np.ones(length**2 + length , dtype=int ).reshape(length, length + 1)#[cell][wall]
white_h = -1 * np.ones(length**2 + length, dtype=int).reshape(length + 1, length)#[wall][cell] 

def Change_matrix():
    global  white_h, white_v, V_walls, H_walls
    #maze matrix
    V_walls = np.zeros(length**2 + length, dtype=int).reshape(length, length + 1)#[cell][wall]
    H_walls = np.zeros(length**2 + length, dtype=int).reshape(length + 1, length)#[wall][cell]

    white_v = -1 * np.ones(length**2 + length, dtype=int).reshape(length, length + 1)#[cell][wall]
    white_h = -1 * np.ones(length**2 + length, dtype=int).reshape(length + 1, length)#[wall][cell] 

screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGINE, SCREEN_HEIGHT))
pygame.display.set_caption('maze designer')

def Change_length():
    global length, wall_length
    length = int(input("enter the number of cells: "))
    wall_length = Hight // length

def Save():
    H = []
    for rows in H_walls:
        r =[]
        for walls in rows:
            r.append(walls)
        H.append(r)

    V = []
    for walls in V_walls:
        w = []
        for rows in walls:
            w.append(rows)
        V.append(w)

    #save level data in txt
    with open(f'design_txt/H{index}.txt', 'w') as fp:
        h=str(H)
        for i in h:
            if i=='[':
                fp.write('\n')
                fp.write('{')
            elif i==']':
                fp.write('}')
            else:
                fp.write(i)
    
    with open(f'design_txt/V{index}.txt', 'w') as fp:
        v=str(V)
        for i in v:
            if i=='[':
                fp.write('\n')
                fp.write('{')

            elif i==']':
                fp.write('}')
            else:
                fp.write(i)


    #save level data in csv
    pickle_out = open(f'design/H{index}.csv', 'wb')
    pickle.dump(H, pickle_out)
    pickle_out.close()

    pickle_out = open(f'design/V{index}.csv', 'wb')
    pickle.dump(V, pickle_out)
    pickle_out.close()


    # file = open(f'design/{index}.txt', 'w')
    # text = f"{H} \n{V}"
    # file.write(text)
    # file.close()

def draw_bg():
    '''draw the background colour and the working area'''
    screen.fill(GREEN)
    #draw area
    pygame.draw.rect(screen, RED, (((SCREEN_WIDTH - Width) // 2), ((SCREEN_HEIGHT - Hight) // 2), Width, Hight))

def Vertical_wall(x, y, colour):
    '''draw the vertical walls according to the given matrix'''
    pygame.draw.line(screen, colour, (x, y), (x, y + wall_length), 2)

def Horizontal_wall(x, y, colour):
    '''draw the horizontal walls according to the given matrix'''
    pygame.draw.line(screen, colour, (x, y), (x + wall_length, y), 2)

def draw_text(text, font, text_col, x, y):
    img =  font.render(text, True, text_col)
    screen.blit(img, (x, y))

run = True
while run:

    draw_bg()

    #draw text
    #draw current maze details
    draw_text(f'CURRENT MAZE {index}', font, RED, SCREEN_WIDTH, 80)
    draw_text(f'CURRENT MAZE SIZE {length}', font, RED, SCREEN_WIDTH, 120)
    #draw instructions
    draw_text('Press 1 to draw', font, BLACK, SCREEN_WIDTH, 160)
    draw_text('(left click for Horizontal wall)', font, BLACK, SCREEN_WIDTH, 180)
    draw_text('(right click for Vertical wall)', font, BLACK, SCREEN_WIDTH, 200)
    draw_text('Press 2 to erase', font, BLACK, SCREEN_WIDTH, 240)
    draw_text('Press 3 to save', font, BLACK, SCREEN_WIDTH, 280)
    draw_text('Press UP or DOWN', font, BLACK, SCREEN_WIDTH, 320)
    draw_text('to change the current maze', font, BLACK, SCREEN_WIDTH, 340)
    draw_text('Press SPACE to change size', font, BLACK, SCREEN_WIDTH, 380)

    
    #draw the maze using matrix
    #draw grid
    for y,  wall in enumerate(white_h):
        for x, col in enumerate(wall):
            if white_h[y][x] == -1:
                Horizontal_wall(((SCREEN_WIDTH - Width) // 2) + x*wall_length, ((SCREEN_HEIGHT - Hight) // 2) + y*wall_length, WHITE)
    #vertical walls
    for y,  row in enumerate(white_v):
        for x, wall in enumerate(row):
            if white_v[y][x] == -1:
                Vertical_wall(((SCREEN_WIDTH - Width) // 2) + x*wall_length, ((SCREEN_HEIGHT - Hight) // 2) + y*wall_length, WHITE)

    #horizontal walls
    for y,  wall in enumerate(H_walls):
        for x, col in enumerate(wall):
            if H_walls[y][x] == -1:
                Horizontal_wall(((SCREEN_WIDTH - Width) // 2) + x*wall_length, ((SCREEN_HEIGHT - Hight) // 2) + y*wall_length, BLACK)
    #vertical walls
    for y,  row in enumerate(V_walls):
        for x, wall in enumerate(row):
            if V_walls[y][x] == -1:
                Vertical_wall(((SCREEN_WIDTH - Width) // 2) + x*wall_length, ((SCREEN_HEIGHT - Hight) // 2) + y*wall_length, BLACK)

    #get mouse position
    pos = pygame.mouse.get_pos()
    x_pos = (pos[0] - ((SCREEN_WIDTH - Width) // 2)) // wall_length
    y_pos = (pos[1] - ((SCREEN_HEIGHT - Hight) // 2)) // wall_length
    # print(x_pos, y_pos)
    if pygame.mouse.get_pressed()[0] == 1 and 0 <= x_pos < length and 0 <= y_pos <= length:#right mouse
        if draw:
            H_walls[y_pos][x_pos] = -1
        else:
            H_walls[y_pos][x_pos] = 0

    if pygame.mouse.get_pressed()[2] == 1 and 0 <= x_pos <= length and 0 <= y_pos < length:#left mouse
        if draw:
            V_walls[y_pos][x_pos] = -1
        else:
            V_walls[y_pos][x_pos] = 0

    #event handler

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        #keyboard press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                draw = True
            if event.key == pygame.K_2:
                draw = False
            if event.key == pygame.K_UP:
                index += 1
            if event.key == pygame.K_DOWN:
                if index > 0:
                    index -= 1
            if event.key == pygame.K_3:
                Save()
            if event.key == pygame.K_SPACE:
                Change_length()
                Change_matrix()

    pygame.display.update()

pygame.quit()
