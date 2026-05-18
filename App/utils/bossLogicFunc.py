import pygame
from classes.overlapClass import *
from classes.bulletClass import bullet_class
from utils.backgroudFunc import *
import sys
from classes.bossBulletClass import *

def hanle_boss_shooting(boss_bullets, cnt_tras, rand_X,boss,player):
    #trage catre directia player-ului
        if (cnt_tras) % int(rand_X) == 0:
            if  abs(boss.x - player.rect.x) < 40:
                #trage direct in fata/spate
                if boss.y < player.rect.y:
                    boss_bullets.append(boss_bullet_class(round(boss.x + 90), round(boss.y + 90), 10, (255,0,0), 0,1))
                else:
                    boss_bullets.append(boss_bullet_class(round(boss.x + 90), round(boss.y + 90), 10, (255,0,0), 0,-1))
            elif abs(boss.y - player.rect.y) < 40:
                #trage in sus/ jos
                if boss.x < player.rect.x:
                    boss_bullets.append(boss_bullet_class(round(boss.x + 90), round(boss.y + 90), 10, (255,0,0), 1,0))
                else:
                    boss_bullets.append(boss_bullet_class(round(boss.x + 90), round(boss.y + 90), 10, (255,0,0), -1,0))
            else:
                #diagonala(oricare dintre cele 4 diagonale)
                #in functie de pozitia playerului fata de boss
                if boss.x < player.rect.x and boss.y < player.rect.y:
                    boss_bullets.append(boss_bullet_class(round(boss.x + 90), round(boss.y + 90), 10, (255,0,0), 1,1))
                if boss.x > player.rect.x and boss.y < player.rect.y:
                    boss_bullets.append(boss_bullet_class(round(boss.x + 90), round(boss.y + 90), 10, (255,0,0), -1,1))
                if boss.x < player.rect.x and boss.y > player.rect.y:
                    boss_bullets.append(boss_bullet_class(round(boss.x + 90), round(boss.y + 90), 10, (255,0,0), 1,-1))
                if boss.x > player.rect.x and boss.y > player.rect.y:
                    boss_bullets.append(boss_bullet_class(round(boss.x + 90), round(boss.y + 90), 10, (255,0,0), -1,-1))

def handle_boss_bullets_logic(boss_bullets, player, rd,game_map,normal_bullets):
    #gloantele trase merg putin si apoi se impart in 4
    for bullet in boss_bullets:
            #if bullet.facing == 1 or bullet.facing == -1:
            #se iau 2 nr random, pt ca gloantele sa se sparga semi random, sa nu poti lovi boss-ul dintr-o pozitie anume
            #sau sa nu poti sta safe undeva anume
            r1 = random.randint(120, 180)
            r2 = random.randint(120, 180)
            if (abs(bullet.x - rd.x) < r1 and abs(bullet.y - rd.y) < r2):
                bullet.x += 2 * bullet.velx
                bullet.y += 2 * bullet.vely
            else:
                #se sparg in 4 gloante care merg sus jos stanga dreapta
                normal_bullets.append(bullet_class(round(bullet.x), round(bullet.y), 8, (255,0,0), 1,1,0))
                normal_bullets.append(bullet_class(round(bullet.x), round(bullet.y), 8, (255,0,0), -1,1,0))
                normal_bullets.append(bullet_class(round(bullet.x), round(bullet.y), 8, (255,0,0), 0,1,-1))
                normal_bullets.append(bullet_class(round(bullet.x), round(bullet.y), 8, (255,0,0), 0,1,1))
                boss_bullets.pop(boss_bullets.index(bullet))
            if overlap(player.rect.x + 16,player.rect.y + 16,31,bullet.x,bullet.y,bullet.radius):
                boss_bullets.pop(boss_bullets.index(bullet))
                player.take_damage(34)
            else:
                #se mai sparg si daca lovesc un zid, pt ca dc sa nu se sparga
                #face mai greu jocul
                for i in range(len(game_map.walls)):
                    if overlap(game_map.walls[i].x + 25,game_map.walls[i].y + 25,50,bullet.x,bullet.y,bullet.radius):
                        normal_bullets.append(bullet_class(round(bullet.x), round(bullet.y), 8, (255,0,0), 1,1,0))
                        normal_bullets.append(bullet_class(round(bullet.x), round(bullet.y), 8, (255,0,0), -1,1,0))
                        normal_bullets.append(bullet_class(round(bullet.x), round(bullet.y), 8, (255,0,0), 0,1,-1))
                        normal_bullets.append(bullet_class(round(bullet.x), round(bullet.y), 8, (255,0,0), 0,1,1))
                        boss_bullets.pop(boss_bullets.index(bullet))
                        break

def handle_split_bullets_logic(split_bullets, player,game_map):
    #gloantele impartite sunt asemanatoare cu gloantele normale, doar ca dau mai mult damage
    for bullet in split_bullets:
            vf = 0
            #de notat ca acestea merg si pe verticala, nu doar pe orizontala precum cele normale
            if bullet.velx != 0:
                if abs(bullet.x - bullet.startx) < 1000:
                    bullet.x += 2 * bullet.velx
                else:
                    vf = 1
                    split_bullets.pop(split_bullets.index(bullet))
            if bullet.vely != 0:
                if abs(bullet.y - bullet.starty) < 1000:
                    bullet.y += 2 * bullet.vely
                else:
                    vf = 0
                    split_bullets.pop(split_bullets.index(bullet))
            #aici chestiile basic
            #dau damage si se opresc in ziduri
            if overlap(player.rect.x + 16,player.rect.y + 16,32,bullet.x,bullet.y,bullet.radius) and vf == 0:
                split_bullets.pop(split_bullets.index(bullet))
                player.take_damage(25)
            else:
                for i in range(len(game_map.walls)):
                    if overlap(game_map.walls[i].x + 25,game_map.walls[i].y + 25,50,bullet.x,bullet.y,bullet.radius) and vf == 0:
                        split_bullets.pop(split_bullets.index(bullet))
                        break
