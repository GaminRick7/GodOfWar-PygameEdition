import pygame
import sys
import os
import time
from player import Player
from enemy import Enemy
from tile import Tile
from spritesheet import Spritesheet
from level import Level
from button import Button


############## VARIABLES ###############
#

worldx = 960
worldy = 480
LOWER_MARGIN = 100
SIDE_MARGIN = 300

screen = pygame.display.set_mode((worldx, worldy))
fps = 40  # frame rate
ani = 4   # animation cycles
main = True

BLUE = (25, 25, 200)
BLACK = (23, 23, 23)
WHITE = (254, 254, 254)
ALPHA = (0, 255, 0)

############### INITIAL SETUP #############

clock = pygame.time.Clock()
pygame.init()
world = pygame.display.set_mode([worldx, worldy])
backdrop = pygame.image.load(os.path.join('images', 'mountain.png'))
backdrop = pygame.transform.scale(backdrop, (960, 480))
backdropbox = world.get_rect()


steps = 2




########## LEVEL MAPS ###############


level_map1 = [
'                            ',
'       E                     ',
' XX    XXX                ',
' XXP                             XXXXXX',
'                                 XX ',
'            XX             XXXXXXXX ',
'       XXXXXXXXX       XXXXXXXXXXXXXXXXXXXXXXXX ',
'                   ',
'    XXXXXXXXXXXXXXXXXXXXX     X',
'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX ']

level_map2 = [
'                            ',
'       E                     ',
'     XXX                ',
'                              XXXXXX',
'             X                    XX ',
'                         XXXXXXXX ',
'                          ',
'                   ',
'    XXXXXXXXXXXXXXXXXXXXX     X',
'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX ']
level = Level(level_map2, screen, "background", 7)
scroll_speed =0
################ MAIN ####################
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def main_menu():
    menuimg = pygame.image.load("images/8OWVccL.gif")
    logo = pygame.image.load("images/pngwing.com.png")
    menuimg = pygame.transform.scale(menuimg, (960, 480))
    while True:
        screen.blit(menuimg, (0,0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()
        screen.blit(logo, (480,100))
        MENU_TEXT = get_font(70).render("GOD OF WAR", True, "#ab0000")
        MENU_RECT = MENU_TEXT.get_rect(center=(480, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("images/Play Rect.png"), pos=(480, 240), 
                            text_input="PLAY", font=get_font(35), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("images/Options Rect.png"), pos=(480, 400), 
                            text_input="OPTIONS", font=get_font(35), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("images/Quit Rect.png"), pos=(480, 550), 
                            text_input="QUIT", font=get_font(35), base_color="#d7fcd4", hovering_color="White")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    game_loop()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    print("options")
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def game_loop():
    level.setup_level(level_map2)
    scroll_speed = 0
    while True:
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == ord('q'):
                    pygame.quit()
                    try:
                        sys.exit()
                    finally:
                        main = False
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    level.player.control(-steps, 0)
                    scroll_speed -= 2
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    level.player.control(steps, 0)
                    scroll_speed +=2
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == ord('w'):
                    level.player.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    level.player.control(steps, 0)
                    scroll_speed = 0
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    level.player.control(-steps, 0)
                    scroll_speed = 0
        level.bg.scroll(scroll_speed)
        clock.tick(fps)
        level.bg.draw(screen)
        level.run()
        pygame.display.flip()
main_menu()
#game_loop()