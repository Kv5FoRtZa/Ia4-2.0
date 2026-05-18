import os
import random
import pygame
import math
import time
from os import listdir
from os.path import isfile,join
from classes.bulletClass import *
from classes.overlapClass import *

class enemy(object):
    walk = [pygame.image.load(join("assets","MainCharacters","RD","RD.png"))]
    
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.path = [x, end]
        self.walkCount = 0
        self.vel = 3
        self.hp = 2
        self.initialx = x
        self.initialy = y
    def draw(self, win,game_map):
        self.move(game_map)
        win.blit((self.walk[0]), (self.x,self.y))
    def move(self,game_map):
        #in principiu merge pana loveste ceva/ atinge maximul
        #apoi se intoarce
        if self.vel > 0:
            if self.x < self.path[1] + self.vel:
                vf = 0
                for i in range(len(game_map.walls)):
                     if square_square_overlap(game_map.walls[i].x + 25,game_map.walls[i].y + 25,50,self.x +25,self.y + 25,49):
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
                for i in range(len(game_map.walls)):
                     if square_square_overlap(game_map.walls[i].x + 25,game_map.walls[i].y + 25,50,self.x + 25,self.y + 25,49):
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
    def fire(self,facing):
        # trage 
        bullets = []
        if len(bullets) < 4:
             bullets.append(bullet_class(round(self.x + 25), round(self.y + 25), 6, (255,0,0), facing,0)) 
    def damage(self):
        #are 2 hp, si moare in 2 hits
        self.hp -= 1
        if self.hp == 0:
            self.x = -1000
            self.y = -1000
    def exit(self):
        #se respawneaza cand se rejoaca
        self.hp = 2
        self.x = self.initialx
        self.y = self.initialy