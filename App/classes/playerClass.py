import os
import random
import pygame
import math
from os import listdir
from os.path import isfile,join
from utils.global_variables import x_perete,y_perete,matrice_fundal,WIDTH,HEIGHT,FPS,LIGHT_BLUE,PLAYER_VELOCITY
pygame.init()
pygame.display.set_caption("game")
window = pygame.display.set_mode((WIDTH,HEIGHT))

#ia pozele cu animatia si le face sa fie spre stanga ca ele sunt spre dreapta default
def flip(sprites):
    return [pygame.transform.flip(sprite,True,False) for sprite in sprites]


#loads images
# SPRITE == imagine pe frames 
def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    # dir1 - director_for_characters
    # dir2 - director_for_pink man in this situation 
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        # .convert_alpha() says they are transparent 
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites

#player
class Player(pygame.sprite.Sprite):

    COLOR=LIGHT_BLUE
    ANIMATION_DELAY=5
    SPRITES=load_sprite_sheets("MainCharacters","PinkMan",25,25,True)
    def __init__(self,x,y,width,height):
        super().__init__()
        self.rect = pygame.Rect(x,y,width,height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.max_hp = 100
        self.hp = 100
        self.update_sprite() 
        self.update_mask()
    def move(self, dx, dy, objects):
            # miscare pe axa X
            self.rect.x += dx
            self.update_mask()
            for obj in objects:
                if pygame.sprite.collide_mask(self, obj):
                    # Mergem DREAPTA -> Lovim un perete aflat in dreapta noastra
                    if dx > 0 and obj.rect.left >= self.rect.left:
                        self.rect.x -= dx
                
                    # Mergem STANGA -> Lovim un perete aflat in stânga noastra
                    elif dx < 0 and obj.rect.right <= self.rect.right:
                        self.rect.x -= dx
                
                    self.update_mask()

            # Miscare pe axa Y
            self.rect.y += dy
            self.update_mask()
            for obj in objects:
                if pygame.sprite.collide_mask(self, obj):
                    # Mergem JOS -> Lovim un perete aflat SUB noi
                    if dy > 0 and obj.rect.top >= self.rect.top:
                        self.rect.y -= dy

                    # Mergem SUS -> Lovim un perete aflat DEASUPRA noastra
                    elif dy < 0 and obj.rect.bottom <= self.rect.bottom:
                        self.rect.y -= dy

                    self.update_mask()
    
    def move_left(self,vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self,vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0
    def move_up(self,vel):
        self.y_vel = -vel

    def move_down(self,vel):
        self.y_vel = vel

    #muta caracterul frame by frame
    def loop(self, fps, walls,traps):
        self.update_sprite()
        # Ne asiguram că avem o masca valida imediat dupa schimbarea sprite-ului
        self.update_mask()
        self.move(self.x_vel, self.y_vel, walls)
        self.check_traps(traps)


    # updateaza animatia frame by frame
    def update_sprite(self):
        sprite_sheet = "idle"
        if self.x_vel!=0:
            sprite_sheet = "run"
        if self.y_vel!=0:
            sprite_sheet = "run"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = self.animation_count//self.ANIMATION_DELAY % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count +=1
    def update_mask(self):
        # Creeaza o masca din imaginea curenta a sprite-ului
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self,window):
        window.blit(self.sprite,(self.rect.x,self.rect.y))
    def take_damage(self, amount):
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0
        print(f"Ai luat damage! HP rămas: {self.hp}")
    def check_traps(self, traps):
        for trap in traps:
            if pygame.sprite.collide_mask(self, trap):
                self.take_damage(1)
    
def handle_move(player):
    keys = pygame.key.get_pressed()
    player.x_vel=0
    player.y_vel=0
    #merge pe sageti si pe wasd
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]):
        player.move_left(PLAYER_VELOCITY)
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
        player.move_right(PLAYER_VELOCITY) 
    if (keys[pygame.K_UP] or keys[pygame.K_w]):
        player.move_up(PLAYER_VELOCITY)
    if (keys[pygame.K_DOWN] or keys[pygame.K_s]):
        player.move_down(PLAYER_VELOCITY)
