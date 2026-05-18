import os
import random
import pygame
import math
import sys
from os import listdir
from os.path import isfile, join
from utils.global_variables import *
from utils.backgroudFunc import *
from classes.playerClass import *
from classes.objectClass import *
from level_menu import levels_menu
from classes.levelClass import *
from classes.gameMapClass import GameMap
from classes.bulletClass import *
from classes.enemyClass import *
from classes.overlapClass import *
from utils.enemyLogicFunc import *
from utils.bossLogicFunc import *
from utils.gameLogicFunc import *
from classes.resetEnemy import *

pygame.init()
pygame.font.init() # Inițializăm modulul de fonturi

pygame.display.set_caption("EVO HUNTER")
window = pygame.display.set_mode((WIDTH, HEIGHT)) 

# BIG TODO: de mutat toate metodele din main intr-un fisier ajutator

def get_font(size): 
    return pygame.font.SysFont("comicsans", size)

def draw_3d_box(window, rect, color):
    # desenam umbra
    shadow_rect = pygame.Rect(rect.x + 5, rect.y + 5, rect.width, rect.height)
    pygame.draw.rect(window, (40, 40, 40), shadow_rect, border_radius=15)

    # desenam cutia
    pygame.draw.rect(window, color, rect, border_radius=15)

    # adaugam contur
    pygame.draw.rect(window, (200, 200, 200), rect, 2, border_radius=15)

def main_menu(window):
    run = True
    clock = pygame.time.Clock()
    
    # colors used
    BG_COLOR = LIGHT_MUTED_BLUE
    TEXT_COLOR = LIGHT_GRAY
    TITLE_COLOR = WHITE
    BOX_COLOR = DARK_MUTED_BLUE

    while run:
        clock.tick(FPS)
        window.fill(BG_COLOR)
        
        # Titlul mare
        title_font = get_font(120)
        title_text = title_font.render("EVO HUNTER", True, TITLE_COLOR)
        title_rect = title_text.get_rect(center=(WIDTH/2, 200))
        window.blit(title_text, title_rect)

        # fontul pt poveste
        font = get_font(30)

        # textele
        text1 = font.render("Bine ai venit!", True, TEXT_COLOR)
        text2 = font.render("In acest joc trebuie sa vanezi goblini mov evil!", True, TEXT_COLOR)
        text3 = font.render("Esti singurul care ii poate opri!", True, TEXT_COLOR)

        # creat rect pt story box
        story_box = pygame.Rect(0, 0, 700, 150)
        story_box.center = (WIDTH/2, 360)

        # draw the box
        draw_3d_box(window, story_box, BOX_COLOR)

        # draw textele in cutie
        window.blit(text1, text1.get_rect(center=(WIDTH/2, 330)))
        window.blit(text2, text2.get_rect(center=(WIDTH/2, 360)))
        window.blit(text3, text3.get_rect(center=(WIDTH/2, 395)))

        # button de play 
        instruct_font = get_font(80)
        instruct_text = instruct_font.render("Click to Play", True, TITLE_COLOR)
        instruct_rect = instruct_text.get_rect(center=(WIDTH/2, 530))

        # efect de schimbare de culoare pt button de play 
        if instruct_rect.collidepoint(pygame.mouse.get_pos()):
            instruct_text = instruct_font.render("Click to Play", True, (255, 215, 0))
        
        # display the button
        window.blit(instruct_text, instruct_rect)

        # instructiuni - text
        font2 = get_font(55)
        inst_title = font2.render("Instructiuni:", True, TEXT_COLOR)
        i1 = font.render("Mers pe WASD sau pe sageti", True, TEXT_COLOR)
        i2 = font.render("Pentru a impusca apasa Click", True, TEXT_COLOR)

        # cutie pt instructiuni
        inst_box = pygame.Rect(0, 0, 600, 150)
        inst_box.center = (WIDTH/2, 700)
        
        # draw the box
        draw_3d_box(window, inst_box, BOX_COLOR)

        # put the text in the box
        window.blit(inst_title, inst_title.get_rect(center=(WIDTH/2, 660)))
        window.blit(i1, i1.get_rect(center=(WIDTH/2, 705)))
        window.blit(i2, i2.get_rect(center=(WIDTH/2, 740)))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() # Iese de tot din program
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if instruct_rect.collidepoint(mouse_pos):
                    run = False

def play_game(window, current_level):
    clock = pygame.time.Clock()
    # harta jocului curent
    game_map = current_level.getMap()
    #save = current_level.getMap()

    # Aici se declară toate tipurile de bg
    background_tiles, bg_image = get_background("beigeTile.png")
    player = Player(100, 100, 32, 32)

    # bullets rd-ei si helperi pt ele
    bullets = []
    enemy_bullets = []
    boss_bullets = []
    split_bullets = []
    nr_rd = 5
    rand_X = [10 for _ in range(len(game_map.inamic))]
    rnd = 10
    #rd = create_rd(rand_X, nr_rd,game_map)
    cnt_tras = 0

    run=True
    while run:
        cnt_tras += 1
        clock.tick(FPS)

        # handles the shooting logic
        handle_player_bullets_logic(bullets, player,game_map)
        handle_enemy_bullets_logic(enemy_bullets, player,game_map)
        handle_enemy_shooting(game_map,enemy_bullets, cnt_tras, rand_X)
        if game_map.bosss:
            hanle_boss_shooting(boss_bullets, cnt_tras,rnd,game_map.bosss[0],player)
            handle_boss_bullets_logic(boss_bullets,player,game_map.bosss[0],game_map,split_bullets)
        if len(split_bullets) != 0:
            handle_split_bullets_logic(split_bullets,player,game_map)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    player.take_damage(10) # Scade 10 HP la fiecare apăsare
            if event.type == pygame.MOUSEBUTTONUP:  # tragere de gloante ale player-ului
                if player.direction == 'left':
                    facing = -1
                else:
                    facing = 1
                if len(bullets) < 16:
                    bullets.append(bullet_class(round(player.rect.x + 25), round(player.rect.y + 25), 6, (0,0,0), facing,0,0)) 

        # rulam frumos playerul si sa se miste frumos
        player.loop(FPS, game_map.walls, game_map.traps)
        handle_move(player)

        # am facut o functie noua de draw in backgroundFunc
        draw(window, background_tiles, bg_image, player, current_level, bullets, enemy_bullets,game_map,boss_bullets,split_bullets)

        # desenam health bar
        draw_health_bar(window, player)
        if game_map.bosss:
            draw_boss_bar(window,game_map.bosss[0])

        pygame.display.update()

        # daca s a castigat -- marcam in nivel si ne intoarcem la meniu
        if check_win_condition(game_map) is True:
            draw(window, background_tiles, bg_image, player, current_level, bullets, enemy_bullets,game_map,boss_bullets,split_bullets)
            winning_message(window)
            # should help with the messages who are not always being displayed
            pygame.display.flip() 
            pygame.event.pump()

            current_level.setWinStatus(1)
            reset_map(game_map)
            pygame.time.delay(3000)
            run = False

        if check_loss_condition(player) is True:
            draw(window, background_tiles, bg_image, player, current_level, bullets, enemy_bullets,game_map,boss_bullets,split_bullets)
            losing_message(window)

            pygame.display.flip() 
            pygame.event.pump()

            reset_map(game_map)
            pygame.time.delay(3000)
            run = False

# main function -- rulam jocul
def main(window):
    clock = pygame.time.Clock()
    
    # rulam meniul
    main_menu(window)

    # Levels array and choosing a level
    levels = create_levels()
    run = True

    while run:
        # displaying the levels' menu and choosing to play a level
        current_level = levels_menu(window, levels)

        if current_level:
            play_game(window, current_level)
            if current_level.getWinStatus() == 1:
                unlock_next_level(current_level, levels)
        else:
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main(window)