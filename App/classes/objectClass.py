import os
import random
import pygame
from os import listdir
from os.path import isfile, join

pygame.init()

class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name
        
    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        # Specificam folderul "Background" pentru blocuri
        block = get_block("beigeBrick.png", "Background", size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)
        self.x = x
        self.y = y

# clasa trap (tepi)
class Trap(Object):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "spike")
        # Specificam folderul "Tiles" pentru tepi
        trap = get_block("spikes.png", "Tiles", width)
        self.image.blit(trap, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

# fct get_block
def get_block(img_name, directory="Background", size=100, x_start_img=0, y_start_img=0):
    # construim calea folosind directorul specificat
    path = join("assets", directory, img_name)
    
    if not isfile(path):
        print(f"[EROARE] Nu am găsit imaginea: {path}")
        surface = pygame.Surface((size, size))
        surface.fill((255, 0, 0)) # patrat rosu for safety
        return surface

    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(x_start_img, y_start_img, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale(surface, (size, size))