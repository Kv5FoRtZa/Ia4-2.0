import pygame
import time
import sys
from classes.levelClass import *
from utils.global_variables import WIDTH, HEIGHT, LIGHT_BLUE, WHITE, BLACK, DARK_GRAY, GRAY, RED, FPS

# de facut o clasa levels:
    # starea_nivelului : locked / unlocked
    # harta nivelului
    # exista constructori in python ?
    # metode pt get si pt update/set

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Levels:")

def get_font(size):
    return pygame.font.SysFont("comicsans", size)

# COORDONATELE IN PYGAME : 
    # (x, y) ==> x orizontala (partea de sus ; st la dr), y verticala (partea din st ; sus in jos)

def draw_button(window, level, text, x, y, width, height):
    # draw the shadow
    shadow_rect = pygame.Rect(x + 5, y + 5, width, height)
    pygame.draw.rect(window, DARK_GRAY, shadow_rect, border_radius=12)

    # draw the button
    button_rect = pygame.Rect(x, y, width, height)

    # nivel care e unlocked si poate fi jucat
    if(level.getWinStatus() == 0 and level.getState() == "unlocked"):
        pygame.draw.rect(window, WHITE, button_rect, border_radius=12)

    # nivel care e locked (de pus un lacat peste ??)
    if(level.getState() == "locked"):
        pygame.draw.rect(window, GRAY, button_rect, border_radius=12)

    # de adaugat o poza cu o coroana idk -- level care a fost deja jucat si castigat
    if(level.getWinStatus() == 1):
        pygame.draw.rect(window, (252, 215, 30), button_rect, border_radius=12)
    
    pygame.draw.rect(window, BLACK, button_rect, 3, border_radius=12)

    # add the text
    text_font = get_font(40)
    text_surface = text_font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center = button_rect.center)
    window.blit(text_surface, text_rect)

    return button_rect

def draw_level_locked_message(window, level):
    name = level.getName()
    
    # facem cu overlay ca nu imi place cum arata ce am mai incercat
    msg_width, msg_height = 400, 150
    overlay = pygame.Surface((msg_width, msg_height), pygame.SRCALPHA)
    
    # dreptunghi transparent
    pygame.draw.rect(overlay, (0, 0, 0, 200), (0, 0, msg_width, msg_height), border_radius=20)
    
    # contur
    pygame.draw.rect(overlay, (255, 0, 0), (0, 0, msg_width, msg_height), 3, border_radius=20)

    # font
    font_big = get_font(40)
    font_small = get_font(25)
    
    # text surface
    title_surf = font_big.render("LEVEL LOCKED", True, RED)
    text_surf = font_small.render(f"Complete previous levels to play {name}", True, WHITE)
    
    # text rect
    title_rect = title_surf.get_rect(center=(msg_width // 2, 50))
    text_rect = text_surf.get_rect(center=(msg_width // 2, 100))
    
    # desenam le overlay pe centru
    overlay.blit(title_surf, title_rect)
    overlay.blit(text_surf, text_rect)
    
    screen_rect = overlay.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    window.blit(overlay, screen_rect)

def levels_menu(window, levels):
    run = True
    clock = pygame.time.Clock()

    level_with_locked_message = None
    show_message_until = 0

    while run:
        clock.tick(FPS)
        window.fill(LIGHT_BLUE)

        # title
        title_levels_font = get_font(75)
        title_levels_text = title_levels_font.render("Choose a level: ", True, (0, 0, 0))
        title_levels_rect = title_levels_text.get_rect(center=(WIDTH / 2, 250))
        window.blit(title_levels_text, title_levels_rect)

        # get the buttons
        button1 = draw_button(window, levels[0], levels[0].getName(), WIDTH / 2 - 100, 320, 200, 60)
        button2 = draw_button(window, levels[1], "Level 2", WIDTH / 2 - 100, 420, 200, 60)
        button3 = draw_button(window, levels[2], "Level 3", WIDTH / 2 - 100, 520, 200, 60)
        button4 = draw_button(window, levels[3], "Level 4", WIDTH / 2 - 100, 620, 200, 60)
        button5 = draw_button(window, levels[4], "Bo$$ Level", WIDTH / 2 - 100, 720, 200, 60)

        # draws the locked message until said time
        current_time = pygame.time.get_ticks()
        if level_with_locked_message and current_time < show_message_until:
            draw_level_locked_message(window, level_with_locked_message)
        else:
            level_with_locked_message = None


        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if button1.collidepoint(mouse_pos):
                    if (levels[0].getState() == "locked"):
                        level_with_locked_message = levels[0]
                        show_message_until = pygame.time.get_ticks() + 2000
                    else:
                        chosen_level = levels[0]
                        run = False

                    # apelat din main si se opreste si intra in harta aia
                    # ar trebui apelata functia de harta cand se scrie clasa de levels
                elif button2.collidepoint(mouse_pos):
                    if (levels[1].getState() == "locked"):
                        level_with_locked_message = levels[1]
                        show_message_until = pygame.time.get_ticks() + 2000
                    else:
                        chosen_level = levels[1]
                        run = False

                elif button3.collidepoint(mouse_pos):
                    if (levels[2].getState() == "locked"):
                        level_with_locked_message = levels[2]
                        show_message_until = pygame.time.get_ticks() + 2000
                    else:
                        chosen_level = levels[2]
                        run = False

                elif button4.collidepoint(mouse_pos):
                    if (levels[3].getState() == "locked"):
                        level_with_locked_message = levels[3]
                        show_message_until = pygame.time.get_ticks() + 2000
                    else:
                        chosen_level = levels[3]
                        run = False

                elif button5.collidepoint(mouse_pos):
                    if (levels[4].getState() == "locked"):
                        level_with_locked_message = levels[4]
                        show_message_until = pygame.time.get_ticks() + 2000
                    else:
                        chosen_level = levels[4]
                        run = False
    return chosen_level

if __name__ == "__main__":
    levels = [Level("unlocked", 1), Level("locked", 2), Level("locked", 3), Level("locked", 4)]
    levels_menu(window, levels)
    