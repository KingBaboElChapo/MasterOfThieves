# Read about what each thing does in the respective class
# !!! WARNING !!! The game will break if the level does not contain the player ("C") within; the game may break if the door Top and Bottom is not found as well.

import pygame

from Entities.player import Player
from Entities.platform import Platform
from Entities.door import Door
from Entities.coins import Coins
from Entities.spike import Spike
from Entities.trophies import Trophy
from display.display import Display
from BuildFunctions.directory import Directory

Display = Display()
Directory = Directory()


class LevelLoader(object):
    """
    This class actually handles a lot of things; while also handling the level loading, it also must be used to call from another class in the game
    class itself.  For example, to use anything from the Player class, the user must have LevelLoader()getPlayer().functionHere.
    In all honesty, this class handles pretty much everything that has anything to do with levels.
    """
    def __init__(self):
        self.level = 0
        self.platforms = []

        self.doorsClosed = True

        self.entities = pygame.sprite.Group()
        self.coin = pygame.sprite.Group()
        self.spikes = pygame.sprite.Group()
        self.trophies = pygame.sprite.Group()
        self.x = 0
        self.y = 0

        self.levelCoins = 0
        self.loadedCoins = False

        self.showDebug = False

    def buildLevel(self):
        """
        KEY FOR LEVELS
        P = Platform
        C = player starting position
        A = Spike (Up)    - 1
        V = Spike (Down)  - 2
        > = Spike (Right) - 3
        < = Spike (Left)  - 4
        K = Key
        X = Trophy
        T = Door Top
        B = Door Bottom
        O = Coin
        """
        level = open(Directory.get_directory() + '/levels/level' + str(self.level) + '.txt', 'r')
        for row in level:
            for col in row:
                if col.isdigit() and self.loadedCoins == False:
                    if int(col) > 0:
                        self.loadedCoins = True
                        self.levelCoins = int(col)
                    else:
                        self.loadedCoins = True
                        self.levelCoins = 1
                if col == "P":
                    p = Platform(self.x, self.y) # Place a platform at the given x,y
                    self.platforms.insert(0, p) # Insert it into the platforms list
                    self.entities.add(p) # Add to Entities so it appears on screen
                if col == "C":
                    self.charX = self.x # The character x found from file loading
                    self.charY = self.y # The character y found from file loading
                    self.player = Player(self.charX, self.charY) # Set the player along with the x,y of the starting position
                if col == "A":
                    spike = Spike(self.x, self.y, 1) # Load a spike at the x,y found
                    self.entities.add(spike) # Add the spike to the Entities
                    self.spikes.add(spike) # Add the spike to the spike sprite group for collison purposes
                if col == "V":
                    spike = Spike(self.x, self.y, 2) # Load a spike at the x,y found
                    self.entities.add(spike) # Add the spike to the Entities
                    self.spikes.add(spike) # Add the spike to the spike sprite group for collison purposes
                if col == ">":
                    spike = Spike(self.x, self.y, 3) # Load a spike at the x,y found
                    self.entities.add(spike) # Add the spike to the Entities
                    self.spikes.add(spike) # Add the spike to the spike sprite group for collison purposes
                if col == "<":
                    spike = Spike(self.x, self.y, 4) # Load a spike at the x,y found
                    self.entities.add(spike) # Add the spike to the Entities
                    self.spikes.add(spike) # Add the spike to the spike sprite group for collison purposes
                if col == "O":
                    coin = Coins(self.x, self.y) # Load a coin image at the given x,y
                    self.entities.add(coin) # Coin 1 to the Entities
                    self.coin.add(coin) # add coin 1 to the coinA sprite group
                if col == "X":
                    try:
                        win_object = Trophy(self.x, self.y, self.level) # Load the proper trophy by passing the level to the trophy class and load at the given x,y from file loading
                        self.entities.add(win_object) # Add the trophy to the Entities so it appears
                        self.trophies.add(win_object) # Also make it a trophy sprite for collision detection purposes
                    except:
                        win_object = Trophy(self.x, self.y, 0)
                        self.entities.add(win_object) # Add the trophy to the Entities so it appears
                        self.trophies.add(win_object) # Also make it a trophy sprite for collision detection purposes
                if col == "T":
                    self.doorA = Door(self.x, self.y)
                    self.platforms.append(self.doorA) # Make the door top a platform so the player cannot walk through it
                    self.entities.add(self.doorA) # Add the door bottom to the Entities
                if col == "B":
                    self.doorB = Door(self.x, self.y)
                    self.platforms.append(self.doorB) # Make the door bottom a platform so the player cannot walk through it
                    self.entities.add(self.doorB) # Add the door bottom to Entities
                self.x += 32
            self.y += 32
            self.x = 0

        # Try loading in the level image and theme; if it fails, use level 0 theme and background
        try:
            self.background = pygame.image.load(Directory.get_directory() + '/images/backgrounds/background' + str(self.level) + '.png').convert_alpha()
            self.background_rect = self.background.get_rect()
        except:
            self.background = pygame.image.load(Directory.get_directory() + '/images/backgrounds/background0.png').convert_alpha()
            self.background_rect = self.background.get_rect()

    def getPlayer(self):
        return self.player

    def getPlatforms(self):
        return self.platforms

    def getEntities(self):
        return self.entities

    def get_coins(self):
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
        self.player.on_ground = True
        self.x = 0
        self.y = 0
        self.loadedCoins = False
        level = self.level
        self.platforms = None
        self.doorA.kill()
        self.doorB.kill()
        self.entities.empty()
        self.trophies.empty()
        self.spikes.empty()
        self.coin.empty()

    def rebuildObjects(self):
        self.level = self.level
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
        self.player.up = False
        self.player.right = False
        self.player.left = False
        self.player.running = False

    def add_level(self):
        self.level += 1

    def reset_level(self):
        self.level = 0

    def get_level(self):
        return self.level

    def loading_bar(self):
        return self.loading_bar

    def get_level_coins(self):
        return self.levelCoins

    def infoScreen(self):
        self.debug = Display.font.render("Information Window", True, (255,255,255))
        self.death_status = Display.font.render("player.canDie: " + str(self.getPlayer().canDie), True, (255,255,255))
        self.door_status = Display.font.render("door_closed: " + str(self.doorsClosed), True, (255,255,255))
        self.coin_debug = Display.font.render("coin_count: " + str(self.getPlayer().get_coins()), True, (255,255,255))
        Display.screen.blit(self.debug, (0,0))
        Display.screen.blit(self.death_status, (0,25))
        Display.screen.blit(self.door_status, (0,50))
        Display.screen.blit(self.coin_debug, (0,75))
