import os
import random
import pygame
import math
from os import listdir
from os.path import isfile,join
from utils.global_variables import x_perete,y_perete,matrice_fundal,WIDTH,HEIGHT,FPS,LIGHT_BLUE,PLAYER_VELOCITY
from classes.gameMapClass import GameMap
from classes.levelClass import Level
from utils.global_variables import WIDTH, HEIGHT

pygame.init()
pygame.display.set_caption("game")


#function for getting a tile and positon vector for background
def get_background(fundal):
    image = pygame.image.load(join("assets","Background",fundal))

    _, _, width, height = image.get_rect() #gaseste marimea imaginii
    tiles=[]
    #vor fi eliminate cand facem matricile si layoutul fundalului de mana
    for i in range (WIDTH // width + 1):
        for j in range (HEIGHT // height + 1):
            pos = (i * width,j* height) #tiles position 
            tiles.append(pos)
    return tiles,image

def draw(window, background_tiles, bg_image, player, current_level, bullets, enemy_b,game_map,boss_b,split_bullets):
    # punem background 
    for tile in background_tiles:
        window.blit(bg_image, tile)

    # desenam walls si traps conform layoutului
    game_map = current_level.getMap() 
    if game_map:
        game_map.draw(window)

    # desenam rd-ei si bullets 
    for bullet in bullets:
        bullet.draw(window)
    for bullet in enemy_b:
        bullet.draw(window)
    for bullet in boss_b:
        bullet.draw(window)
    for bullet in split_bullets:
        bullet.draw(window)
    for i in range(len(game_map.inamic)):
        if (game_map.inamic[i].hp > 0):
            game_map.inamic[i].draw(window,game_map)

    # desenam playerul
    player.draw(window)

def draw_health_bar(window, player):
    # configurare bara
    bar_width = 200
    bar_height = 20
    x_pos = 20  # distanta de la stanga ecranului
    y_pos = 20  # Distanta de sus
    
    # calc cat din bara trebuie sa fie verde (procentaj)
    # Formula: (HP curent / HP maxim) * latime totala
    ratio = player.hp / player.max_hp
    fill_width = ratio * bar_width
    
    # Dreptunghiul de fundal (Rosu - arata cat damage ai luat)
    border_rect = pygame.Rect(x_pos, y_pos, bar_width, bar_height)
    
    # Dreptunghiul de viata (Verde - arata cata viata mai ai)
    fill_rect = pygame.Rect(x_pos, y_pos, fill_width, bar_height)
    
    # Desenam dreptunghiurile
    pygame.draw.rect(window, (255, 0, 0), border_rect) # Fundal Roșu
    pygame.draw.rect(window, (0, 255, 0), fill_rect)   # Viata Verde
    
    # contur alb
    pygame.draw.rect(window, (255, 255, 255), border_rect, 2)

def draw_boss_bar(window, boss):
    #bara de hp pt boss
    #apare doar la levelul cu boss-ul
    #este rosie cu alb
    font = pygame.font.SysFont('Comic Sans MS', 30)
    text = font.render("The evil Rectorat's hp", False, (0, 0, 0))
    window.blit(text, (WIDTH // 2 - 100,70))
    bar_width = WIDTH // 3
    bar_height = 15
    x_pos = WIDTH // 3
    y_pos = 55
    
    ratio = boss.hp / 20
    fill_width = ratio * bar_width
    
    border_rect = pygame.Rect(x_pos, y_pos, bar_width, bar_height)
    
    fill_rect = pygame.Rect(x_pos, y_pos, fill_width, bar_height)
    
    pygame.draw.rect(window, (255, 0, 0), border_rect)
    pygame.draw.rect(window, (255, 255, 255), fill_rect)
    
    pygame.draw.rect(window, (0, 0, 0), border_rect, 2)