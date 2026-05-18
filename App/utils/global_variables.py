from os import environ

# it stops showing the pygame message 
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = ''

# importing the required libraries
import pygame
import sys
import time
from pygame.locals import *
x_perete = [0] * 90# salvez coltul stanga sus pt fiecare perete(sunt noob si nu stiu sa fac coliziune fara var globala)
y_perete = [0] * 90
matrice_fundal = [0] * 290 # aici o sa avem fundalul codat cu 0 = fundal basic, 1 = perete, -1 = tepi, etc
#momentan este 0 si se baga 1 din loc in loc pentru perete
#in get_background fac acesta initializare momentan, insa ea va trebui facuta de mana(pt a avea o harta care arata ok)
#de retinut ca fiecare poza trebuie trecuta prin get_background
#afisez poze diferite in draw, in functie de ce se afla in matrice momentan
WHITE=(255,255,255)
BLACK=(0,0,0)
LIGHT_BLUE   = (173, 216, 230)
BLUE_MUTED   = (70, 130, 180)   
LIGHT_PINK   = (255, 182, 193)  
DARK_GREEN   = (0, 100, 0)
GRAY = (150, 150, 150)
DARK_GRAY = (50, 50, 50)
LIGHT_GRAY = (200, 200, 200)
RED = (180, 40, 40)
LIGHT_MUTED_BLUE = (94, 129, 162)
DARK_MUTED_BLUE = (60, 90, 120)
WIDTH=1800
HEIGHT=1000
FPS=30
PLAYER_VELOCITY=6
