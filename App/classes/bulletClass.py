import os
import random
import pygame
import math
class bullet_class(object):
    def __init__(self,x,y,radius,color,facing,nr_inamic,up):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing
        self.nr_inamic = nr_inamic
        self.up = up
        self.velx = 8 * facing
        self.vely = 8 * up
        self.startx = x
        self.starty = y
    def draw(self,win):
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)