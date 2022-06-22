import pygame
import sys
import os
from shop import ShopItem
from tile import Tile
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
' C    I E I                    ',
' XX    XXX                      CCCC',
' XX                             XXXXXX',
'                              I ECCCIXX ',
'      I  E CC IX       I CCCC IXXXXXXXXI      ICCO',
'       XXXXXXXXX  O     XXXXXXXXXXXXXXXXXX     XXXXXX ',
'    P      CCCCCCCCCC           CCCCCCCCCC',
'    XXXXXXXXXXXXXXXXXXXXX     X CCCCCCCCCC       CCCC',
'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX']

level_map2 = [
'      E                      ',
'    I   I                     ',
'     XXX                     I  ECCC I',
'                              XXXXXXX  O',
'             X          I E  CCCCI   XX ',
'                         XXXXXXXX ',
'                          ',
'    I   P   CCCCC  CCCCCC I',
'I    XXXXXXXXXXXXXXXXXXXXXI  E   IXI CCE    I',
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
'CCCCCCCCCCCS                O          ',
'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX ']

################ MAIN ###################
############### VARIOUS SCREENS ###############
def main_menu(): #Main Menu Screen that includes the play button and options button
    '''
    Args: None
    Returns: None
    Main Menu of the game
    '''
    #list of animations for main menu background
    mainMenuImages = []
    #Frame counter for background
    imageNumber = 0
    #for loop to load background frames
    for i in range(0, 7):
        #loads the frames of the background
        image = pygame.image.load(os.path.join('images', 'menuback', f'frame_{i}_delay-0.1s.gif')).convert()
        #scales it to fit the full screen
        image = pygame.transform.scale(image, (960,480))
        #appends to mainMenuImages
        mainMenuImages.append(image)
    #
    while True:
        #checks that the frame counter does not exceed 139 as that would result in a list index out of range
        if imageNumber > 139:
            imageNumber = 0
        #blits the background frame based on imageNumber
        screen.blit(mainMenuImages[imageNumber//20], (0,0))
        #increases the frame counter
        imageNumber += 1

        mousepos = pygame.mouse.get_pos()
        menuText = get_font(70).render("GOD OF WAR", True, "White")
        menuRect = menuText.get_rect(center=(480, 100))
        #Creates a Quit Button and a Play Button
        playButton = imageButton(image=pygame.transform.scale(pygame.image.load("images/Start.png"), (200, 65.28)), pos=(480, 200))
        quitButton = imageButton(image=pygame.transform.scale(pygame.image.load("images/Quit.png"), (200, 65.28)), pos=(480, 300))

        #displays text on the screen
        screen.blit(menuText, menuRect)

        #Updates all buttons
        for button in [playButton, quitButton]:
            button.update(screen)
        
        
        for event in pygame.event.get():
            #checks if mouse button is pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                #if play button is pressed, the game begins
                if playButton.checkForInput(mousepos):
                    game_loop()
                #if quit button is pressed, the game ends
                if quitButton.checkForInput(mousepos):
                    pygame.quit()
                    sys.exit()
        #updates the screen
        pygame.display.update()

def gameOver():
    '''
    Args: None
    Returns: None
    Creates Game Over screen
    '''
    #Creates black background
    screen.fill("black")

    #Creates Game Over text
    gameOverText = get_font(70).render("Game Over", True, "White")
    gameOverRect = gameOverText.get_rect(center=(480, 100))
    #Displays the text
    screen.blit(gameOverText, gameOverRect)
    #Creates Replay Button
    replayButton = imageButton(image=pygame.transform.scale(pygame.image.load("images/replay.png"), (200,53.2)), pos=(480, 400))
    #Displays Replay Button
    replayButton.update(screen)

    #mouse position to check for input
    mousepos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        #checks if mouse button is pressed
        if event.type == pygame.MOUSEBUTTONDOWN:
            #checks if the replay button is clicked, if so, the game begins
            if replayButton.checkForInput(mousepos):
                game_loop()
            
################# SHOP VARIABLES##########################
#A 2d list with all the image name, item name, buff type, buff, cost, and position for each item
shopInventory = [["armour1", "Loki's Armour", "health", 15, 85, (35, 155)], ["book1", "Odin's Blessing", "health", 25, 115, (35, 205)], ["mask1", "Balder's Curse", "damage", 15, 75, (35, 255)]]
# A list of items already purchased
bought = []
##############################################
################# MAIN GAME ##################
def game_loop(): #Main Game Loop
    mousepos = pygame.mouse.get_pos()
    shop = Level(level_map3, screen, "shopBackground", 7) 
    level = Level(level_map1, screen, "background", 7) 
    level2 = Level(level_map2, screen, "background2", 7)
    level3 = Level(level_map2, screen, "background3", 9)
    level4 = Level(level_map1, screen, "background", 7)
    level5 = Level(level_map2, screen, "background2", 7)
    level6 = Level(level_map2, screen, "background3", 9)

    #The current level is default set to 1
    currentLevel = 1
    #The scroll_speed of the background is set to 0
    scroll_speed = 0

    #The players initial attributes are stored as the following vriables
    pmaxhealth = 200
    pmoney = 1000
    pdamage = 50

    level.setup_level(pmaxhealth, pmoney, pdamage)
    LevelText = get_font(15).render("Level 1: Forests of Valheim", True, "White")
    controlsDisabled = False
    inShop = False
    ###################################
    
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
            gameOver()
        elif level.player.health <= 0:
            level.player.kill()
            gameOver()


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
        #http://pixelartmaker.com/art/bb84d0211d6dd52 buy button
        if inShop:
            items = pygame.sprite.Group()
            screen.fill("black")
            for individual in shopInventory:
                item = ShopItem(individual)
                items.add(item)
            items.draw(screen)
            for item in items:
                if item.name not in bought:
                    item.buyButton.update(screen)
                else:
                    ownedText = get_font(15).render("OWNED", True, "White")
                    ownedRect = itemText.get_rect(center=(960, item.rect.y))
                    screen.blit(ownedText, ownedRect)
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
            level.player.draw_damage()
            level.player.draw_health()
            shopName = get_font(20).render("Brok's Warehouse of Madness (Shop)", True, "White")
            shopNameRect = itemText.get_rect(center=(250, 78))
            screen.blit(shopName, shopNameRect)

            itemHeader = get_font(15).render("Item", True, "White")
            itemHeaderRect = itemText.get_rect(center=(230, 118))
            screen.blit(itemHeader, itemHeaderRect)

            typeHeader = get_font(15).render("Type", True, "White")
            typeHeaderRect = itemText.get_rect(center=(470, 118))
            screen.blit(typeHeader, typeHeaderRect)

            buffHeader = get_font(15).render("Buff", True, "White")
            buffHeaderRect = itemText.get_rect(center=(640, 118))
            screen.blit(buffHeader, buffHeaderRect)

            costHeader = get_font(15).render("Cost", True, "White")
            costHeaderRect = itemText.get_rect(center=(800, 118))
            screen.blit(costHeader, costHeaderRect)
            exitButton = imageButton(image=pygame.image.load("images/exitShop.png"), pos=(480, 400))
            exitButton.update(screen)

            for item in items:
                mousepos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN and item.name not in bought:
                    if item.buyButton.checkForInput(mousepos):
                        if level.player.money >= item.cost:
                            level.player.money -= item.cost
                            if item.type == "health":
                                level.player.maximumHealth += item.buff
                                level.player.health = level.player.maximumHealth
                            elif item.type == "damage":
                                level.player.damage += item.buff
                            bought.append(item.name)
                            inShop = False
                            controlsDisabled = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mousepos = pygame.mouse.get_pos()
                if exitButton.checkForInput(mousepos):
                    print("yeah")
                    inShop = False
                    controlsDisabled = False
        
        for portal in level.portal_list:
            prevDirection = level.player.direction.x
            if level.player.rect.colliderect(portal.rect):
                pmaxhealth = level.player.maximumHealth
                pmoney = level.player.money
                pdamage = level.player.damage
                currentLevel += 0.5
                if currentLevel % 1 != 0:
                    level = shop
                    LevelText = get_font(15).render("The World Between Worlds", True, "White")
                if currentLevel == 2:
                    level = level2
                    LevelText = get_font(15).render("Level 2: Valleys of Jotunheim", True, "White")
                if currentLevel == 3:
                    level = level3
                    LevelText = get_font(15).render("Level 3: Valleys of Alfheim", True, "White")
                if currentLevel == 4:
                    level = level4
                    LevelText = get_font(15).render("Unknown", True, "White")
                level.setup_level(pmaxhealth, pmoney, pdamage)
                level.player.control(prevDirection)
        pygame.display.flip()
main_menu()