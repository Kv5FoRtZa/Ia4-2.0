import pygame
from classes.overlapClass import *
from classes.bulletClass import bullet_class
from utils.backgroudFunc import *
import sys
from classes.bossBulletClass import *

def handle_player_bullets_logic(bullets, player,game_map):
    #gloantele merg pana la o anumita distanta/ pana lovesc un inamic sau un perete
    for bullet in bullets:
            vf = 0
            if bullet.facing == 1 or bullet.facing == -1:
                if abs(bullet.x - player.rect.x) < 1000:
                    bullet.x += 2 * bullet.vel
                else:
                    vf = 1
                    bullets.pop(bullets.index(bullet))  
            #damage la inamici
            for i in range(len(game_map.inamic)):
                if overlap(game_map.inamic[i].x + 25,game_map.inamic[i].y + 25,50,bullet.x,bullet.y,bullet.radius) and vf == 0:
                    bullets.pop(bullets.index(bullet))
                    game_map.inamic[i].damage()
                    vf = 1
            if game_map.bosss:
                #damage la boss
                if overlap(game_map.bosss[0].x + 90,game_map.bosss[0].y + 90,180,bullet.x,bullet.y,bullet.radius) and vf == 0:
                    bullets.pop(bullets.index(bullet))
                    game_map.bosss[0].damage()
                    vf = 1
            #print(sys.getsizeof(game_map.walls))
            if vf == 0:
                for i in range(len(game_map.walls)):
                    if overlap(game_map.walls[i].x + 25,game_map.walls[i].y + 25,50,bullet.x,bullet.y,bullet.radius):
                        bullets.pop(bullets.index(bullet))
                        break

def handle_enemy_bullets_logic(enemy_bullets, player,game_map):
    #merg o distanta/ pana lovesc jucatorul sau un perete
    for bullet in enemy_bullets:
            vf = 0
            if bullet.facing == 1 or bullet.facing == -1:
                if abs(bullet.x - game_map.inamic[bullet.nr_inamic].x) < 1000:
                    bullet.x += 2 * bullet.vel
                else:
                    vf = 1
                    enemy_bullets.pop(enemy_bullets.index(bullet))
            if overlap(player.rect.x + 16,player.rect.y + 16,32,bullet.x,bullet.y,bullet.radius) and vf == 0:
                #se opreste in player
                #moare la 5 lovituri
                vf = 1
                enemy_bullets.pop(enemy_bullets.index(bullet))
                player.take_damage(20)
            else:
                for i in range(len(game_map.walls)):
                    #se orpeste in perete
                    if overlap(game_map.walls[i].x + 25,game_map.walls[i].y + 25,50,bullet.x,bullet.y,bullet.radius) and vf == 0:
                        vf = 1
                        enemy_bullets.pop(enemy_bullets.index(bullet))
                        break

def handle_enemy_shooting(game_map, enemy_bullets, cnt_tras, rand_X):
    #inamicii trag semi random
    #trag in directia in care merg
    for i in range(len(game_map.inamic)):
        if (cnt_tras) % int(rand_X[i]) == 0:
            if game_map.inamic[i].vel >= 0:
                enemy_bullets.append(bullet_class(round(game_map.inamic[i].x + 25), round(game_map.inamic[i].y + 25), 6, (255,0,0), 1,i,0))
            else:
                enemy_bullets.append(bullet_class(round(game_map.inamic[i].x + 25), round(game_map.inamic[i].y + 25), 6, (255,0,0), -1,i,0)) 
