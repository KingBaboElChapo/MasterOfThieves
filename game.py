#! /usr/bin/python

import pygame
import gc # garbage collector
import os
import time as pause
from pygame import *
from sys import exit

# Import all of our classes
from entities import Entity
from player import Player
from platform import Platform
from door import Door
from coins import Coins
from spike import Spike
from sounds import Sounds
from trophies import Trophy
from themes import Themes
from levelLoader import levelLoader

from camera import *

os.environ['SDL_VIDEO_CENTERED'] = '1' # Attempt to center the game window on the users screen; may not always work

# The below globals are used throughout; disliked them, but they wouldn't work any other way.
global coin_count, door_closed, current_level, deaths, deaths_total, volume
current_level = 3
deaths = 0
deaths_total = 0
coin_count = 0
door_closed = True
volume = 0.2 # Maximum volume

# Initialize PyGame
pygame.init()

# The menu music; ends when the first level begins
pygame.mixer.pre_init(44100, -16, 2, 2048)
sounds = Sounds()
levelLoader = levelLoader(current_level, volume)
theme = (Themes(-1)) # Themes(-1) is the theme name within the /sounds/themes folder
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(volume)

def main():
    """The main loop of the game.  It handles loading the levels, key strokes, playing music and sounds; relies heavily on multiple other classes to function correctly.
        These include the camera, coins, door, entities, platform, player, sounds, spike, themes, and trophies classes."""
    gc.enable() # Garbage collector
    global cameraX, cameraY, coin_count, door_closed, current_level, deaths, deaths_total, volume # Load in the global variables
    pygame.mixer.pre_init(44100, -16, 2, 2048) # Initilize the music
    screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH) # Set the screen information
    screen_rect = screen.get_rect()
    timer = pygame.time.Clock()

    show_debug = False

    # We don't want to see the normal mouse cursor while playing.
    pygame.mouse.set_visible(False)

    sounds = Sounds() # Allows us to call sounds by doing sounds.name

    font = pygame.font.SysFont("arial", 25) # Font for the game

    loading_bar = pygame.transform.scale(pygame.image.load("images/button.png"), (WIN_WIDTH, 35)) # Loading bar image (so that the "Loading Level (level)..." text is visible)

    up = down = left = right = running = False # Set all key strokes (directions) to False

    # Load in the first level by assigning sprites into groups and into the platforms and coin_list lists
    # Read about what each thing does in the respective class
    # !!! WARNING !!! The game will break if the level does not contain the player ("C") within; the game may break if the door Top and Bottom is not found as well.
    """KEY FOR LEVELS
        P = Platform
        C = player starting position
        A = Spike (Up) - 1
        V = Spike (Down) - 2
        > = Spike (Right) - 3
        < = Spike (Left) - 4
        K = Key
        X = Trophy
        T = Door Top
        B = Door Bottom"""

    levelLoader.buildLevel()
    try:
        theme = (Themes(current_level))
        pygame.mixer.music.play(-1, 0.0)
        pygame.mixer.music.set_volume(volume)
    except:
        theme = (Themes(0))
        pygame.mixer.music.play(-1, 0.0)
        pygame.mixer.music.set_volume(volume)

    total_level_width  = len('level'[0])*32
    total_level_height = len('level')*32
    camera = Camera(complex_camera, total_level_width, total_level_height)
    levelLoader.entities.add(levelLoader.getPlayer()) # Finally, add player to entities so it appears
        
    # The main loop of the game which runs it until we're done.    
    while 1:
        pygame.display.set_caption("Master of Thieves | Level: " +str(current_level) + " | Deaths (level): " + str(deaths) + " | Deaths (Total): " + str(deaths_total) + " | FPS: " + str(int(timer.get_fps())))
        asize = ((screen_rect.w // levelLoader.getBGWidth() + 1) * levelLoader.getBGWidth(), (screen_rect.h // levelLoader.getBGHeight() + 1) * levelLoader.getBGHeight())
        bg = pygame.Surface(asize)

        # Create the background
        for x in range(0, asize[0], levelLoader.getBGWidth()):
            for y in range(0, asize[1], levelLoader.getBGHeight()):
                screen.blit(levelLoader.getBackground(), (x, y))

        timer.tick(38) # The maximum framerate; the game is designed to run at an FPS of 30-40 (38 being best)

        # All the keystroke events; the game can run using the UP-RIGHT-LEFT arrow keys, Space Bar, and the AWD keys (down is never needed)
        #   ENTER will kill the player (used if the player glitch spawns outside the level or glitch out (reloads the level as if they died))
        for e in pygame.event.get():
            if e.type == QUIT: 
                exit()
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                exit()
            if e.type == KEYDOWN and e.key == K_SPACE:
                levelLoader.getPlayer().onGround = False
                up = True
            if e.type == KEYDOWN and e.key == K_UP:
                levelLoader.getPlayer().onGround = False
                up = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                levelLoader.getPlayer().direction = 'left'
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                levelLoader.getPlayer().direction = 'right'
                right = True
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                exit()
            if e.type == KEYDOWN and e.key == K_w:
                levelLoader.getPlayer().onGround = False
                up = True
            if e.type == KEYDOWN and e.key == K_a:
                levelLoader.getPlayer().direction = 'left'
                left = True
            if e.type == KEYDOWN and e.key == K_d:
                levelLoader.getPlayer().direction = 'right'
                right = True
            if e.type == KEYDOWN and e.key == K_RETURN:
                levelLoader.getPlayer().dead = True
            if e.type == KEYDOWN and e.key == K_LSHIFT:
                if levelLoader.getPlayer().canDie == True:
                    levelLoader.getPlayer().canDie = False
                    break
                if levelLoader.getPlayer().canDie == False:
                    levelLoader.getPlayer().canDie = True
                    break
            if e.type == KEYDOWN and e.key == K_i:
                if show_debug == False:
                    show_debug = True
                    break
                if show_debug == True:
                    show_debug = False
                    break
            if e.type == KEYDOWN and e.key == K_c:
                coin_count = 4
            if e.type == KEYDOWN and e.key == K_e:
                levelLoader.getPlayer().yvel -= 20

            if e.type == KEYUP and e.key == K_SPACE:
                levelLoader.getPlayer().onGround = True
                up = False
            if e.type == KEYUP and e.key == K_UP:
                levelLoader.getPlayer().onGround = True
                up = False
            if e.type == KEYUP and e.key == K_RIGHT:
                levelLoader.getPlayer().direction = 'right'
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                levelLoader.getPlayer().direction = 'left'
                left = False
            if e.type == KEYUP and e.key == K_w:
                levelLoader.getPlayer().onGround = True
                up = False
            if e.type == KEYUP and e.key == K_d:
                levelLoader.getPlayer().direction = 'right'
                right = False
            if e.type == KEYUP and e.key == K_a:
                levelLoader.getPlayer().direction = 'left'
                left = False

        # All of the coin collision detection; when it occurs, the coin is removed and a sound plays while adding one to the coin_count (4 opens the door)
        # the True in each IF statement means that when the collision occurs the coin is removed from it's group, thus removing it from appearing on screen
        if pygame.sprite.spritecollide(levelLoader.getPlayer(), levelLoader.getCoins(), True, pygame.sprite.collide_mask):
            sounds.coin_sound.play()
            sounds.coin_sound.set_volume(volume)
            #coin_list.remove(c1)
            coin_count += 1
        #if pygame.sprite.spritecollide(player, coinB, True, pygame.sprite.collide_mask):
        #    sounds.coin_sound.play()
        #    sounds.coin_sound.set_volume(volume)
        #    coin_list.remove(c2)
        #    coin_count += 1
        #if pygame.sprite.spritecollide(player, coinC, True, pygame.sprite.collide_mask):
        #    sounds.coin_sound.play()
        #    sounds.coin_sound.set_volume(volume)
        #    coin_list.remove(c3)
        #    coin_count += 1
        #if pygame.sprite.spritecollide(player, coinD, True, pygame.sprite.collide_mask):
        #    sounds.coin_sound.play()
        #    sounds.coin_sound.set_volume(volume)
        #    coin_list.remove(c4)
        #    coin_count += 1

        # If the player manages to reach the trophy, reset the level deaths, add one to the current_level, kill the theme (music), add the loading bar, print out loading level
        #       kill all key-presses (directions) empty all sprites and lists and load in the next level

        # INSERT RELOAD THANKS TO TROPHY HERE

        # Player collision with spike; if true, kill the player
        if pygame.sprite.spritecollide(levelLoader.getPlayer(), levelLoader.getSpikes(), False, pygame.sprite.collide_mask) and levelLoader.getPlayer().canDie == True:
            levelLoader.getPlayer().dead = True

        # If the player is dead, reset all key strokes to False, play the death sound, empty all groups and lists and reload the level, add one to both total and level deaths_total
        if levelLoader.getPlayer().dead == True:
            levelLoader.getPlayer().onGround = True
            up = False
            right = False
            left = False
            levelLoader.clearScreen()
            pygame.display.update()
            levelLoader.rebuildObjects(current_level, volume)
            levelLoader.buildLevel()
            levelLoader.entities.add(levelLoader.getPlayer()) # Finally, add player to entities so it appears
            try:
                theme = (Themes(current_level))
            except:
                theme = (Themes(0))


        # If the coin count is four, then set the door status to False, kill the door sprites and remove from the platforms list
        # When door_closed is True it means the door can be removed when the coins are all collected; False means it's been collected. This check was added to prevent it from continually playing the sounds.
        if coin_count >= 4 and door_closed == True:
            sounds.door.play()
            sounds.door.set_volume(volume)
            for x in xrange(2): # Since we ensure doors are added to the end of the list, we can just remove the last two items in the platforms list safely
                levelLoader.delPlatforms()
            door_closed = False # now the door status is False
            levelLoader.delDoors()

        camera.update(levelLoader.getPlayer())

        # Update the player and everything else
        levelLoader.getPlayer().update(up, down, left, right, running, levelLoader.getPlatforms())
        for e in levelLoader.getEntities():
            screen.blit(e.image, camera.apply(e))

        # Small debug window
        if show_debug == True:
            font = pygame.font.SysFont("arial", 25)
            debug = font.render("Information Window", True, (255,255,255))
            death_status = font.render("player.canDie: " + str(levelLoader.getPlayer().canDie), True, (255,255,255))
            door_status = font.render("door_closed: " + str(door_closed), True, (255,255,255))
            coin_debug = font.render("coin_count: " + str(coin_count), True, (255,255,255))
            screen.blit(debug, (0,0))
            screen.blit(death_status, (0,25))
            screen.blit(door_status, (0,50))
            screen.blit(coin_debug, (0,75))

        pygame.display.update() # Update the display

# Load the title screen to start the game        
main()