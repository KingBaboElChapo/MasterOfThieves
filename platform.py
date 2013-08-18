import pygame
from pygame.locals import *
from entities import *
from directory import Directory

class Platform(Entity):
    def __init__(self, x, y):
    	"""Handles the creation and images of platforms; they are the P in level creation."""
        Entity.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(Directory().getDirectory() + "/images/brick.png"), (32, 32))
        self.rect = Rect(x, y, 23, 32)
        self.mask = pygame.mask.from_surface(self.image)