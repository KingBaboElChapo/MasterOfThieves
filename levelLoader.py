import pygame
from pygame.locals import *

from entities import Entity
from player import Player
from platform import Platform
from door import Door
from coins import Coins
from spike import Spike
from sounds import Sounds
from trophies import Trophy
from themes import Themes

class levelLoader(object):
	def __init__(self, level):
		self.level = level
		self.platforms = []

		self.doorsClosed = True

		self.entities = pygame.sprite.Group()
		self.coin = pygame.sprite.Group()
		self.spikes = pygame.sprite.Group()
		self.trophies = pygame.sprite.Group()
		self.x = 0
		self.y = 0
	def buildLevel(self):
		level = open('levels/level' + str(self.level) + '.txt', 'r')
		for row in level:
		    for col in row:
		        if col == "P":
		            p = Platform(self.x, self.y) # Place a platform at the given x,y
		            self.platforms.insert(0, p) # Insert it into the platforms list
		            self.entities.add(p) # Add to entities so it appears on screen
		        if col == "C":
					#print "Character found!"
					self.charX = self.x # The character x found from file loading
					self.charY = self.y # The character y found from file loading
					self.player = Player(self.charX, self.charY) # Set the player along with the x,y of the starting position
					#print "yes, player!"
		        if col == "A":
		            spike = Spike(self.x, self.y, 1) # Load a spike at the x,y found 
		            self.entities.add(spike) # Add the spike to the entities
		            self.spikes.add(spike) # Add the spike to the spike sprite group for collison purposes
		        if col == "V":
		            spike = Spike(self.x, self.y, 2) # Load a spike at the x,y found 
		            self.entities.add(spike) # Add the spike to the entities
		            self.spikes.add(spike) # Add the spike to the spike sprite group for collison purposes
		        if col == ">":
		            spike = Spike(self.x, self.y, 3) # Load a spike at the x,y found 
		            self.entities.add(spike) # Add the spike to the entities
		            self.spikes.add(spike) # Add the spike to the spike sprite group for collison purposes
		        if col == "<":
		            spike = Spike(self.x, self.y, 4) # Load a spike at the x,y found 
		            self.entities.add(spike) # Add the spike to the entities
		            self.spikes.add(spike) # Add the spike to the spike sprite group for collison purposes
		        if col == "1":
		            c1 = Coins(self.x, self.y) # Load a coin image at the given x,y
		            self.entities.add(c1) # Coin 1 to the entities
		            self.coin.add(c1) # add coin 1 to the coinA sprite group
		        if col == "2":
		            c2 = Coins(self.x, self.y) # Load a coin image at the given x,y
		            self.entities.add(c2) # Coin 2 to the entities
		            self.coin.add(c2) # add coin 2 to the coinB sprite group
		        if col == "3":
		            c3 = Coins(self.x, self.y) # Load a coin image at the given x,y
		            self.entities.add(c3) # Coin 3 to the entities
		            self.coin.add(c3) # add coin 3 to the coinC sprite group
		        if col == "4":
		            c4 = Coins(self.x, self.y) # Load a coin image at the given x,y
		            self.entities.add(c4) # Coin 4 to the entities
		            self.coin.add(c4) # add coin 4 to the coinD sprite group
		        if col == "X":
		            win_object = Trophy(self.x, self.y, self.level) # Load the proper trophy by passing the level to the trophy class and load at the given x,y from file loading
		            self.entities.add(win_object) # Add the trophy to the entities so it appears
		            self.trophies.add(win_object) # Also make it a trophy sprite for collision detection purposes
		        if col == "T":
		            self.doorA = Door(self.x, self.y)
		            self.platforms.append(self.doorA) # Make the door top a platform so the player cannot walk through it
		            self.entities.add(self.doorA) # Add the door bottom to the entities
		        if col == "B":
		            self.doorB = Door(self.x, self.y)
		            self.platforms.append(self.doorB) # Make the door bottom a platform so the player cannot walk through it
		            self.entities.add(self.doorB) # Add the door bottom to entities
		        self.x += 32
		    self.y += 32
		    self.x = 0

		# Try loading in the level image and theme; if it fails, use level 0 theme and background
		try:
		    self.theme = (Themes(self.level))
		    self.background = pygame.image.load('images/backgrounds/background' + str(self.level) + '.png').convert_alpha()
		    self.background_rect = self.background.get_rect()
		except:
		    self.theme = (Themes(0)) # Instead of passing level we explicity pass level 0 as we know it exists (unless the user deletes it)
		    self.background = pygame.image.load('images/backgrounds/background0.png').convert_alpha()
		    self.background_rect = self.background.get_rect()

	def getPlayer(self):
		return self.player

	def getPlatforms(self):
		return self.platforms

	def getEntities(self):
		return self.entities

	def getCoins(self):
		return self.coin

	def getTrophy(self):
		return self.trophies

	def getSpikes(self):
		return self.spikes

	def getBGWidth(self):
		return self.background_rect.w

	def getBGHeight(self):
		return self.background_rect.h

	def getBackground(self):
		return self.background

	def delPlatforms(self):
		del self.platforms[-1]

	def delDoors(self):
		self.doorsClosed = False
		self.doorA.kill()
		self.doorB.kill()

	def rebuildDoors(self):
		self.doorsClosed = True

	def doorStatus(self):
		return self.doorsClosed

	def clearScreen(self):
		self.player.onGround = True
		self.x = 0
		self.y = 0
		level = self.level
		self.platforms = None
		self.doorA.kill()
		self.doorB.kill()
		self.entities.empty()
		self.trophies.empty()
		self.spikes.empty()
		self.coin.empty()

	def rebuildObjects(self, level):
		self.level = level
		self.platforms = []
		self.doorsClosed = True
		self.player = Player(self.charX, self.charY)
		self.entities = pygame.sprite.Group()
		self.coin = pygame.sprite.Group()
		self.spikes = pygame.sprite.Group()
		self.trophies = pygame.sprite.Group()
		self.x = 0
		self.y = 0
		self.player.dead = False