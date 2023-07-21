import turtle
import time
dir=0
turns=0

t=turtle.Pen()
t.right(90*(turns-dir-1))
t.fd(10)
t.pencolor(1,1,1)
t.fd(10)
t.pencolor(0,0,0)
t.fd(30)
time.sleep(2)