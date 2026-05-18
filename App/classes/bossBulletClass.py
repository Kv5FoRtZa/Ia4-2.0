import os
import random
import pygame
import math
from classes.overlapClass import *
from classes.bulletClass import *
from utils.backgroudFunc import *
import sys

class boss_bullet_class(object):
    #identic ca la gloantele normale
    def __init__(self,x,y,radius,color,facing,up):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.velx = 8 * facing
        self.vely = 8 * up
        self.xplayer = 0
        self.yplayer = 0
        self.up = up
    def draw(self,win):
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)
    def split(self,bullets):
        #impartirea in 4 gloante normale
        bullets.append(bullet_class(round(self.x), round(self.y), 8, (255,0,0), 1,1,0))
        bullets.append(bullet_class(round(self.x), round(self.y), 8, (255,0,0), -1,1,0))
        bullets.append(bullet_class(round(self.x), round(self.y), 8, (255,0,0), 0,1,-1))
        bullets.append(bullet_class(round(self.x), round(self.y), 8, (255,0,0), 0,1,1))