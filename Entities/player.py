import pygame

from sys import exit
from pygame.locals import *
from BuildFunctions.sounds import Sounds
from BuildFunctions.directory import Directory
from BuildFunctions.variables import Variables
from .entities import Entity

sounds = Sounds()


class Player(Entity):
    def __init__(self, x, y):
        """The player class handles all actions of the user. It is the C in level loading."""
        Entity.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.dead = False
        self.direction = 'right'
        self.on_ground = True
        self.canDie = True
        self.coin_count = 0
        self.deaths = 0
        self.levelDeaths = 0
        self.up = False
        self.right = False
        self.left = False
        self.image = pygame.transform.scale(
            pygame.image.load(Directory().get_directory() + "/images/Thief.png"), (40, 40)
        )
        self.image.convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = Rect(x, y, 32, 40)
        self.canPressKey = True

    def update(self, up, left, right, platforms):
        """Handle the directions of the character and change the image based on left or right."""
        if up:
            # only jump if on the ground
            if self.on_ground:
                self.yvel -= 10
        if left and not self.dead:
            self.direction = 'left'
            self.image = pygame.transform.scale(pygame.image.load(Directory().get_directory() + "/images/Thief2.png"), (40, 40))
            self.image.convert_alpha()
            self.mask = pygame.mask.from_surface(self.image)
            self.xvel = -8
        if right and not self.dead:
            self.direction = 'right'
            self.image = pygame.transform.scale(pygame.image.load(Directory().get_directory() + "/images/Thief.png"), (40, 40))
            self.image.convert_alpha()
            self.mask = pygame.mask.from_surface(self.image)
            self.xvel = 8
        if not self.on_ground:
            # only accelerate with gravity if in the air
            self.yvel += 0.95
            # max falling speed
            if self.yvel > 100: 
                self.yvel = 100
        if not(left or right):
            self.xvel = 0

        # increment in x direction
        self.rect.left += self.xvel

        # do x-axis collisions
        self.collide(self.xvel, 0, platforms)

        # increment in y direction
        self.rect.top += self.yvel

        # assuming we're in the air
        self.on_ground = False;

        # do y-axis collisions
        self.collide(0, self.yvel, platforms)

    def collide(self, xvel, yvel, platforms):
        """Handles collisions with platforms."""
        for p in platforms:
            if self.rect.colliderect(p):
                if xvel > 0:
                    self.rect.right = p.rect.left
                if xvel < 0:
                    self.rect.left = p.rect.right
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.on_ground = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.yvel = 0

    def get_key_press(self):
        for e in pygame.event.get():
            if e.type == QUIT: 
                exit()
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                exit()
            if e.type == KEYDOWN and e.key == K_SPACE:
                self.on_ground = False
                self.up = True
            if e.type == KEYDOWN and e.key == K_UP:
                self.on_ground = False
                self.up = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                self.direction = 'left'
                self.left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                self.direction = 'right'
                self.right = True
            if e.type == KEYDOWN and e.key == K_w:
                self.on_ground = False
                self.up = True
            if e.type == KEYDOWN and e.key == K_a:
                self.direction = 'left'
                self.left = True
            if e.type == KEYDOWN and e.key == K_d:
                self.direction = 'right'
                self.right = True
            if e.type == KEYDOWN and e.key == K_RETURN:
                self.dead = True
            if e.type == KEYDOWN and e.key == K_LSHIFT:
                if self.canDie:
                    self.canDie = False
                    break
                if not self.canDie:
                    self.canDie = True
                    break
            if e.type == KEYDOWN and e.key == K_c:
                self.set_coins()
                print("new coin count: " + str(self.coin_count))
            if e.type == KEYDOWN and e.key == K_e:
                self.yvel -= 20
            if e.type == KEYDOWN and e.key == K_m:
                if Variables.volume > 0.0 and Variables.muted == False:
                    Variables.old_volume = Variables.volume
                    Variables.volume = 0.0
                    print("oldVolume: " + str(Variables.old_volume) + "; current: " + str(Variables.volume))
                    Variables.muted = True
                    break
                if Variables.volume == 0.0 and Variables.muted:
                    Variables.volume = Variables.old_volume
                    Variables.old_volume = 0.0
                    print("oldVolume: " + str(Variables.old_volume) + "; current: " + str(Variables.volume))
                    Variables.muted = False
                    break

            if e.type == KEYUP and e.key == K_SPACE:
                self.on_ground = True
                self.up = False
            if e.type == KEYUP and e.key == K_UP:
                self.on_ground = True
                self.up = False
            if e.type == KEYUP and e.key == K_RIGHT:
                self.direction = 'right'
                self.right = False
            if e.type == KEYUP and e.key == K_LEFT:
                self.direction = 'left'
                self.left = False
            if e.type == KEYUP and e.key == K_w:
                self.on_ground = True
                self.up = False
            if e.type == KEYUP and e.key == K_d:
                self.direction = 'right'
                self.right = False
            if e.type == KEYUP and e.key == K_a:
                self.direction = 'left'
                self.left = False

    def get_status(self):
        return self.dead

    def get_coins(self):
        return self.coin_count

    def set_coins(self):
        self.coin_count += 4

    def add_coin(self):
        self.coin_count += 1
        
    def reset_coins(self):
        self.coin_count = 0

    def is_player__air(self):
        return self.on_ground
