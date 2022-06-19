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

worldx = 960
worldy = 480

screen = pygame.display.set_mode((worldx, worldy))
fps = 40  # frame rate

############### INITIAL SETUP #############

clock = pygame.time.Clock()
pygame.init()
steps = 2

########## LEVEL MAPS ###############

level_map1 = [
'                            ',
'      I E I                    ',
' XX    XXX                ',
' XX                             XXXXXX',
'                             I E   IXX ',
'      I  E    IX       I      IXXXXXXXXI      I  O',
'       XXXXXXXXX       XXXXXXXXXXXXXXXXXX     XXXXXX ',
'    P               ',
'    XXXXXXXXXXXXXXXXXXXXX     X',
'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX']

level_map2 = [
'      E                      ',
'    I   I                     ',
'     XXX                     I  E    I',
'                              XXXXXXX  O',
'             X          I E      I   XX ',
'                         XXXXXXXX ',
'                          ',
'    I   P                 I',
'I    XXXXXXXXXXXXXXXXXXXXXI  E   IXI   E    I',
' XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX ']

################ MAIN ####################
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def main_menu(): #Main Menu Screen that includes the play button and options button
    menuimg = pygame.image.load("images/8OWVccL.gif")
    logo = pygame.image.load("images/pngwing.com.png")
    menuimg = pygame.transform.scale(menuimg, (960, 480))
    while True:
        screen.blit(menuimg, (0,0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = get_font(70).render("GOD OF WAR", True, "#ab0000")
        MENU_RECT = MENU_TEXT.get_rect(center=(480, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("images/Play Rect.png"), pos=(480, 200), 
                            text_input="PLAY", font=get_font(35), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("images/Options Rect.png"), pos=(480, 300), 
                            text_input="OPTIONS", font=get_font(35), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("images/Quit Rect.png"), pos=(480, 400), 
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

def game_loop(): #Main Game Loop
    level = Level(level_map1, screen, "background", 7) 
    level2 = Level(level_map2, screen, "background2", 7)
    level3 = Level(level_map2, screen, "background3", 9)
    level4 = Level(level_map1, screen, "background", 7)
    level5 = Level(level_map2, screen, "background2", 7)
    level6 = Level(level_map2, screen, "background3", 9)

    currentLevel = 1
    scroll_speed = 0
    level.setup_level(level_map1)
    LevelText = get_font(15).render("Level 1: Forests of Valheim", True, "White")

    while True:
        screen.fill((0,0,0))
        LevelRect = LevelText.get_rect(center=(480, 50))
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
                    level.player.control(-steps)
                    scroll_speed -= 2
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    level.player.control(steps)
                    scroll_speed +=2
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == ord('w'):
                    level.player.jump()
                if event.key == ord('e'):
                    level.player.attacking = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    level.player.control(steps)
                    scroll_speed = 0
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    level.player.control(-steps)
                    scroll_speed = 0
        level.bg.scroll(scroll_speed)
        clock.tick(fps)
        level.bg.draw(screen)
        level.run()
        screen.blit(LevelText, LevelRect)
        if level.player.rect.y >= 960:
            level.player.kill()
        elif level.player.health <= 0:
            level.player.kill()
        for portal in level.portal_list:
            prevDirection = level.player.direction.x
            if level.player.rect.colliderect(portal.rect):
                if currentLevel == 1:
                    level = level2
                    LevelText = get_font(15).render("Level 2: Valleys of Jotunheim", True, "White")
                if currentLevel == 2:
                    level = level3
                    LevelText = get_font(15).render("Level 3: Valleys of Alfheim", True, "White")
                currentLevel += 1
                level.setup_level(level_map2)
                level.player.control(prevDirection)
        pygame.display.flip()
main_menu()