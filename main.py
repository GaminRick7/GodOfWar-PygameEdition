import pygame
import sys
import os
import time
from shop import ShopItem
from tile import Tile
from spritesheet import Spritesheet
from level import Level
from button import Button, imageButton
from utility import get_font, screen, fps


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

level_map3 = [
'',
'',
'',
'',
'',
'',
'',
'',
'CCCCCCCCCCC  S',
'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX ']

################ MAIN ###################

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



shopInventory = [["armour1", "Loki's Armour", "health", 15, 85, (35, 125)], ["book1", "Odin's Blessing", "health", 25, 115, (35, 175)], ["mask1", "Balder's Curse", "damage", 15, 75, (35, 225)]]

def shop():
    while True:
        level = Level(level_map3, screen, "background", 7) 
        LevelText = get_font(15).render("unknown", True, "White")
        LevelRect = LevelText.get_rect(center=(480, 50))
        screen.blit(LevelText, LevelRect)
def game_loop(): #Main Game Loop
    mousepos = pygame.mouse.get_pos()
    level = Level(level_map3, screen, "shopBackground", 7) 
    #level = Level(level_map1, screen, "background", 7) 
    level2 = Level(level_map2, screen, "background2", 7)
    level3 = Level(level_map2, screen, "background3", 9)
    level4 = Level(level_map1, screen, "background", 7)
    level5 = Level(level_map2, screen, "background2", 7)
    level6 = Level(level_map2, screen, "background3", 9)

    currentLevel = 1
    scroll_speed = 0
    level.setup_level()
    LevelText = get_font(15).render("Level 1: Forests of Valheim", True, "White")
    controlsDisabled = False
    inShop = False
    while True:
        screen.fill((0,0,0))
        LevelRect = LevelText.get_rect(center=(480, 50))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and controlsDisabled == False:
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
        #########
        

        ######
        screen.blit(LevelText, LevelRect)
        if level.player.rect.y >= 960:
            level.player.kill()
        elif level.player.health <= 0:
            level.player.kill()


        for shop in level.shop_list:
            if level.player.rect.colliderect(shop.rect):
                enterShop = Button(image=pygame.image.load("images/Play Rect.png"), pos=(480, 200), 
                            text_input="Enter Shop?", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
                mousepos = pygame.mouse.get_pos()
                enterShop.changeColor(mousepos)
                enterShop.update(screen)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if enterShop.checkForInput(mousepos):
                        inShop = True
                        controlsDisabled = True
        
        if inShop:
            items = pygame.sprite.Group()
            screen.fill("black")
            for individual in shopInventory:
                item = ShopItem(individual)
                items.add(item)
            items.draw(screen)
            for item in items:
                itemText = get_font(15).render(item.name, True, "White")
                itemRect = itemText.get_rect(topleft=(item.rect.x + 25, item.rect.y))
                screen.blit(itemText, itemRect)

                typeText = get_font(15).render(item.type, True, "White")
                typeRect = itemText.get_rect(topleft=(350, item.rect.y))
                screen.blit(typeText, typeRect)

                buffText = get_font(15).render(str(item.buff), True, "White")
                buffRect = itemText.get_rect(topleft=(560, item.rect.y))
                screen.blit(buffText, buffRect)

                costText = get_font(15).render(str(item.cost), True, "White")
                costRect = itemText.get_rect(topleft=(720, item.rect.y))
                screen.blit(costText, costRect)
            level.player.draw_balance()
            shopName = get_font(20).render("Brok's Warehouse of Madness (Shop)", True, "White")
            shopNameRect = itemText.get_rect(center=(250, 35))
            screen.blit(shopName, shopNameRect)

            itemHeader = get_font(15).render("Item", True, "White")
            itemHeaderRect = itemText.get_rect(center=(230, 80))
            screen.blit(itemHeader, itemHeaderRect)

            typeHeader = get_font(15).render("Type", True, "White")
            typeHeaderRect = itemText.get_rect(center=(470, 80))
            screen.blit(typeHeader, typeHeaderRect)

            buffHeader = get_font(15).render("Buff", True, "White")
            buffHeaderRect = itemText.get_rect(center=(640, 80))
            screen.blit(buffHeader, buffHeaderRect)

            costHeader = get_font(15).render("Cost", True, "White")
            costHeaderRect = itemText.get_rect(center=(800, 80))
            screen.blit(costHeader, costHeaderRect)
            exitButton = imageButton(image=pygame.image.load("images/exitShop.png"), pos=(480, 400))
            exitButton.update(screen)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousepos = pygame.mouse.get_pos()
                if exitButton.checkForInput(mousepos):
                    print("yeah")
                    inShop = False
                    controlsDisabled = False
        
        for portal in level.portal_list:
            prevDirection = level.player.direction.x
            if level.player.rect.colliderect(portal.rect):
                if currentLevel == 1:
                    level = level2
                    LevelText = get_font(15).render("Level 2: Valleys of Jotunheim", True, "White")
                if currentLevel == 2:
                    level = level3
                    LevelText = get_font(15).render("Level 3: Valleys of Alfheim", True, "White")
                if currentLevel == 3:
                    level = level4
                    LevelText = get_font(15).render("Unknown", True, "White")
                currentLevel += 1
                level.setup_level()
                level.player.control(prevDirection)
        pygame.display.flip()
main_menu()