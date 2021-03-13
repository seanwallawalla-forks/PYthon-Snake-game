# this was one of the first things I made in python.  I'm going to update it and use it to train my ML model for my senior project at fullsail.
import math
import random as rnd
import pygame as pyg
import tkinter as tk
from tkinter import messagebox as msg
 
class cube(object):
    
    rows = 20
    w = 500
    def __init__(self,start,dirnx=1,dirny=0,color=(255, 171, 42)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color
        
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)
 
    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]
 
        pyg.draw.rect(surface, self.color, (i*dis+1,j*dis+1, dis-2, dis-2))
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pyg.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pyg.draw.circle(surface, (0,0,0), circleMiddle2, radius)
       
class snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1
 
    def move(self):
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                pyg.quit()
 
            keys = pyg.key.get_pressed()
 
            for key in keys:
                if keys[pyg.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
 
                elif keys[pyg.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
 
                elif keys[pyg.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
 
                elif keys[pyg.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
 
        for i, c in enumerate(self.body):
            p = c.pos[:] # where is my body
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0],turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0,c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0],c.rows-1)
                else: c.move(c.dirnx,c.dirny)
       
 
    def reset(self, pos):
        start.play()
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1
 
 
    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny
 
        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))
 
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy
       
 
    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i ==0:
                c.draw(surface, True)
            else:
                c.draw(surface)
 
 
def drawGrid(w, rows, surface):
    sizeBtwn = w // rows
 
    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn
 
        pyg.draw.line(surface, (244, 82, 255), (x,0),(x,w))
        pyg.draw.line(surface, (244, 82, 255), (0,y),(w,y))
       
 
def redrawWindow(surface):
    global rows, width, s, snack
    surface.fill((0,0,0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width,rows, surface)
    pyg.display.update()
 
 
def randomSnack(rows, item):
 
    positions = item.body
 
    while True:
        x = rnd.randrange(rows)
        y = rnd.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break
       
    return (x,y)
 # seperated my initialization stuff.  this could be cleaner
def initialize():
    global width, rows, s, snack, bell, dead, start, flag, win, clock
    pyg.mixer.init()
    start = pyg.mixer.Sound("Start.wav")
    width = 500
    rows = 20
    win = pyg.display.set_mode((width, width))
    s = snake((255, 171, 42), (10,10))
    snack = cube(randomSnack(rows, s), color=(83, 228, 174))
    flag = True
    bell = pyg.mixer.Sound("Token.wav")
    dead = pyg.mixer.Sound("Dead.wav")
    clock = pyg.time.Clock()
    pass

def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    msg.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass
 
 # still need to work this main function but at least its in normal python format now
if __name__ == "__main__":
    initialize()
    start.play()
    while flag:
        pyg.time.delay(50)
        clock.tick(10)
        s.move()
        if s.body[0].pos == snack.pos:
            s.addCube()
            bell.play()
            snack = cube(randomSnack(rows, s), color=(83, 228, 174))
 
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                dead.play()
                print("Score: ", len(s.body))
                message_box("You Lost!", "Play again...")
                s.reset((10,10))
                break
        
        pyg.display.update()  
        redrawWindow(win)
 