import os
import random
import pygame
import math
import time
from os import listdir
from os.path import isfile,join
from classes.bulletClass import *
from classes.overlapClass import *

class boss(object):
    walk = [pygame.image.load(join("assets","MainCharacters","RD","UPB2.png"))]
    
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.path = [x, end]
        self.walkCount = 0
        self.vel = 3
        self.hp = 20
        self.initialx = x
        self.initialy = y
    def draw(self, win,walls):
        self.move(walls)
        win.blit((self.walk[0]), (self.x,self.y))
    def move(self,walls):
        #se poate misca inainte si inapoi
        #pana loveste distanta maxima sau pana loveste un zid
        #apoi se intoarce
        if self.vel > 0:
            if self.x < self.path[1] + self.vel:
                vf = 0
                for i in range(len(walls)):
                     if square_square_overlap(walls[i].x + 25,walls[i].y + 25,50,self.x + self.height / 2,self.y + self.width / 2,self.height):
                         vf = 1
                         break
                if vf == 0:
                    self.x += self.vel
                else:
                    self.vel = self.vel * -1
                    self.x += self.vel
                    self.walkCount = 0
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0
        else:
            if self.x > self.path[0] - self.vel:
                vf = 0
                for i in range(len(walls)):
                     if square_square_overlap(walls[i].x + 25,walls[i].y + 25,50,self.x + self.height / 2,self.y + self.width / 2,self.height):
                         vf = 1
                         break
                if vf == 0:
                    self.x += self.vel
                else:
                    self.vel = self.vel * -1
                    self.x += self.vel
                    self.walkCount = 0
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0
    def damage(self):
        #isi ia damage si poate muri
        self.hp -= 1
        if self.hp == 0:
            self.x = -1000
            self.y = -1000
    def exit(self):
        #la iesirea din level si reintrare i se reface viata
        self.hp = 20
        self.x = self.initialx
        self.y = self.initialy