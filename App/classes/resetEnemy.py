import os
import random
import pygame
import math
from classes.enemyClass import *
from classes.bossEnemy import *
from classes.levelClass import *
from classes.gameMapClass import *
from classes.playerClass import *

def reset_map(game_map):
    #functia care reseteaza viata inamicilor
    #apelata cand se iese/reintra pe un level deja completat/ in care ai murit
    if game_map.bosss:
        game_map.bosss[0].exit()
    for i in range(len(game_map.inamic)):
        game_map.inamic[i].exit()