"""
ICS3U
Raihaan Sandhu
This file is responsible for all the different screens of the game (main menu, introduction, main game, end, shop)
It is also responsible for taking in different inputs and calling functions in level.py in accordance to the inputs.
"""

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
'                             ',
'  C    I E I                    ',
'  XX    XXX                      CCCC',
'  XX                             XXXXXX',
'                               I GCCCIXX ',
'       I  K CC IX       I CCCC IXXXXXXXXI      ICCO',
'        XXXXXXXXX       XXXXXXXXXXXXXXXXXX     XXXXXX ',
'     P      CCCCCCCCCC           CCCCCCCCCC',
'     XXXXXXXXXXXXXXXXXXXXX     X CCCCCCCCCC       CCCC',
'OXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX']

level_map2 = [
'       E                      ',
'     I   I                     ',
'      XXX                     I  ECCC I',
'                               XXXXXXX  O',
'              X          I E  CCCCI   XX ',
'                          XXXXXXXX ',
'                           ',
'     I   P   CCCCC  CCCCCC I',
' I    XXXXXXXXXXXXXXXXXXXXXI  E   IXI CCE    I',
'OXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX ']

level_map3 = [
'                             ',
'  C    I E I                    ',
'  XX    XXX                      CCCC',
'  XX                             XXXXXX',
'                             X I GCCCIXX ',
'              I CCGC IXE  IKXXXIXXXXXXXXXX ICCO',
'        XXXXXXXXXXXXXXXXXXXXXXXXX     XXXXXX ',
'     CCPCCCCC           ',
'     XXXXXXXXXXXI  G  IXXXXXXXXXXXI  K      I',
'OXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX']
level_map4 = [
'                             ',
'  C    I E I                    ',
'  XX    XXX                      CCCC',
'  XX                             XXXXXX',
'                               I GCCCIXX ',
'       I  K CC IX       I CCGC IXXXXXXXXI      ICCO',
'        XXXXXXXXX       XXXXXXXXXXXXXXXXXX     XXXXXX ',
'    IP   E   CCCKCCCCCC   I       CCCCCCCCCC',
'     XXXXXXXXXXXXXXXXXXXXX     X CCCKCCCC       CCCC',
'OXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX']
level_map5 = [
'       E                      ',
'     ICCCI                     ',
'      XXX                     I  KCCC I',
'             I  G I            XXXXXXX  O',
'              XXXX       I G  CCCCI   XX ',
'                          XXXXXXXX ',
'                           ',
'     I   P   CCCCCK CCCCCC I',
' I    XXXXXXXXXXXXXXXXXXXXXI  K   IXI CCE    I',
'OXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX ']

level_map_shop = [
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
def main_menu(): 
    '''
    Args: None
    Returns: None
    Main Menu Screen that includes the play button and quit button
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
        
        #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #checks if mouse button is pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                #if play button is pressed, the game begins
                if playButton.checkForInput(mousepos):
                    intro()
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
        if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        #checks if mouse button is pressed
        if event.type == pygame.MOUSEBUTTONDOWN:
            #checks if the replay button is clicked, if so, the game begins
            if replayButton.checkForInput(mousepos):
                game_loop()
        
def intro():
    '''
    Args: None
    Returns: None
    Creates an introduction screen screen
    '''
    while True:
        #Creates black background
        screen.blit(pygame.image.load("images/intro.png"), (0,0))
        #Creates Replay Button
        playButton = imageButton(image=pygame.transform.scale(pygame.image.load("images/start.png"), (100,32.5)), pos=(800, 400))
        #Displays Replay Button
        playButton.update(screen)

        #mouse position to check for input
        mousepos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            #checks if mouse button is pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                #checks if the replay button is clicked, if so, the game begins
                if playButton.checkForInput(mousepos):
                    game_loop()
        pygame.display.update()

def end():
    '''
    Args: None
    Returns: None
    Creates an ending screen screen with a thank you message
    '''
    while True:
        #Creates black background
        screen.blit(pygame.image.load("images/end.png"), (0,0))
        #Creates Replay Button
        playButton = imageButton(image=pygame.transform.scale(pygame.image.load("images/quit.png"), (100,32.5)), pos=(480, 400))
        #Displays Replay Button
        playButton.update(screen)

        #mouse position to check for input
        mousepos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            #checks if mouse button is pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                #checks if the replay button is clicked, if so, the game begins
                if playButton.checkForInput(mousepos):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()
##############################################
################# MAIN GAME ##################
################# SHOP VARIABLES##########################
#A 2d list with all the image name, item name, buff type, buff, cost, and position for each item
shopInventory = [["armour1", "Loki's Armour", "health", 15, 85, (35, 155)], ["book1", "Odin's Blessing", "health", 25, 115, (35, 205)], ["mask1", "Balder's Curse", "damage", 15, 75, (35, 255)]]
# A list of items already purchased
bought = []
def game_loop(): #Main Game Loop
    '''
    Args: none
    Returns: none
    Main game loop that controls all game actions
    '''
    mousepos = pygame.mouse.get_pos()
    shopLevel = Level(level_map_shop, screen, "shopBackground", 7) 
    level = Level(level_map1, screen, "background", 7) 
    level2 = Level(level_map2, screen, "background2", 7)
    level3 = Level(level_map3, screen, "background3", 9)
    level4 = Level(level_map4, screen, "background4", 5)
    level5 = Level(level_map5, screen, "background5", 6)
    level6 = Level(level_map4, screen, "background6", 2)

    #The current level is default set to 1
    currentLevel = 1
    #The scroll_speed of the background is set to 0
    scroll_speed = 0

    #The players initial attributes are stored as the following vriables
    pmaxhealth = 200
    pmoney = 1000
    pdamage = 50

    #Creates the level using the player attributes
    level.setup_level(pmaxhealth, pmoney, pdamage)
    #The default Level 1 heading; this variable changes based on the level
    LevelText = get_font(15).render("Level 1: Forests of Valheim", True, "White")
    #Controls are not disabled
    controlsDisabled = False
    #By default, the player is not in the shop
    inShop = False

    ###################################
    #while loop for the game to run in
    while True:
        #Creates a rect of the Level Header based on Level Tect
        LevelRect = LevelText.get_rect(center=(480, 50))

        for event in pygame.event.get():
            #closes the game if the window is closed
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #checks if a key is pressed and if the controls are disabled
            if event.type == pygame.KEYDOWN and controlsDisabled == False:
                if event.key == ord('q'):
                    pygame.quit()
                    try:
                        sys.exit()
                    finally:
                        main = False
                #if the player presses "a"
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    #uses player.control() to move -2 pixels
                    level.player.control(-2)
                    #moves the parallax background by a factor of 2
                    scroll_speed -= 2
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    #uses player.control() to move -2 pixels
                    level.player.control(2)
                    #moves the parallax background by a factor of 2
                    scroll_speed +=2
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == ord('w'):
                    #ensures that the player can only jump twice (double jump)
                    if level.jumpCount <= 1:
                        #increases jump count everytime the player jumps
                        level.jumpCount += 1
                        level.player.jump()
                if event.key == ord('e'):
                    level.player.attacking = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    #counteracts the player moving -2 pixels by moving the player 2 pixels
                    level.player.control(2)
                    #stops parallax background from moving
                    scroll_speed = 0
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    #counteracts the player moving -2 pixels by moving the player 2 pixels
                    level.player.control(-2)
                    #stops parallax background from moving
                    scroll_speed = 0
        #based on the scroll speed the parallax background moves
        level.bg.scroll(scroll_speed)
        #creates a clock tick
        clock.tick(fps)
        #draws the background onto the screen
        level.bg.draw(screen)
        #calls level.run()
        level.run()
        #########
        

        ######
        #blits the level heading onto the screen
        screen.blit(LevelText, LevelRect)

        #if the player is dead (fallen off the edge or health is less than 0), its sprite is killed and the game over screen is called
        if level.player.rect.y >= 960:
            level.player.kill()
            gameOver()
        elif level.player.health <= 0:
            level.player.kill()
            gameOver()

        
        for shop in level.shop_list:
            #checks if the player is colliding with the shop
            if level.player.rect.colliderect(shop.rect):
                #creates an enter shop button onto the middle of the screen
                enterShop = Button(image=pygame.image.load("images/Play Rect.png"), pos=(480, 200), 
                            text_input="Enter Shop?", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
                #gets the position of the mouse
                mousepos = pygame.mouse.get_pos()

                #updates the button based on hover, and places it on the screen
                enterShop.changeColor(mousepos)
                enterShop.update(screen)

                #if the enter shop button is clicked
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if enterShop.checkForInput(mousepos):
                        #the player is now in the shop
                        inShop = True
                        #player can no longer move
                        controlsDisabled = True
        #The shop
        if inShop:
            #creates a sprite group of items
            items = pygame.sprite.Group()
            #creates a black screen
            screen.fill("black")
            #a for loop that that goes through all available shop items
            for individual in shopInventory:
                #uses the ShopItem class to create an item based of the given attributes in its list
                item = ShopItem(individual)
                #adds the item to the sprite group
                items.add(item)
            #draws the item icons onto the screen
            items.draw(screen)
            #goes through each of the items 
            for item in items:
                #if the item has not been purchased, the buy button is place on the screen
                if item.name not in bought:
                    item.buyButton.update(screen)
                #if the player has already purchased an item , "owned" appears in place of the button
                else:
                    ownedText = get_font(15).render("OWNED", True, "White")
                    ownedRect = itemText.get_rect(center=(960, item.rect.y))
                    screen.blit(ownedText, ownedRect)


                ############ ITEM TABLE ###############
                # HEADERS

                #Creates the title of the shop at the top of the screen
                shopName = get_font(20).render("Brok's Warehouse of Madness (Shop)", True, "White")
                shopNameRect = shopName.get_rect(center=(250, 78))
                screen.blit(shopName, shopNameRect)

                #Creates a Table Header called Item
                itemHeader = get_font(15).render("Item", True, "White")
                itemHeaderRect = itemHeader.get_rect(center=(180, 118))
                screen.blit(itemHeader, itemHeaderRect)

                #Creates a Table Header called Item
                typeHeader = get_font(15).render("Type", True, "White")
                typeHeaderRect = typeHeader.get_rect(center=(400, 118))
                screen.blit(typeHeader, typeHeaderRect)

                #Creates a Table Header called Item
                buffHeader = get_font(15).render("Buff", True, "White")
                buffHeaderRect = buffHeader.get_rect(center=(560, 118))
                screen.blit(buffHeader, buffHeaderRect)

                #Creates a Table Header called Item
                costHeader = get_font(15).render("Cost", True, "White")
                costHeaderRect = costHeader.get_rect(center=(750, 118))
                screen.blit(costHeader, costHeaderRect)
                #A table of the items and its attributes is created next to the icon of the item
                #The item name is rendered under the item header
                itemText = get_font(15).render(item.name, True, "White")
                itemRect = itemText.get_rect(topleft=(item.rect.x + 25, item.rect.y))
                screen.blit(itemText, itemRect)

                #The type of buff is rendered under the type header
                typeText = get_font(15).render(item.type, True, "White")
                typeRect = itemText.get_rect(topleft=(350, item.rect.y))
                screen.blit(typeText, typeRect)

                #The buff is rendered under the buff header
                buffText = get_font(15).render(str(item.buff), True, "White")
                buffRect = itemText.get_rect(topleft=(560, item.rect.y))
                screen.blit(buffText, buffRect)

                #The cost of the item is rendered under the cost header
                costText = get_font(15).render(str(item.cost), True, "White")
                costRect = itemText.get_rect(topleft=(720, item.rect.y))
                screen.blit(costText, costRect)
            
            #draws the player attributes onto the screen so that the player can see how buying an item affects the attributes in real time
            level.player.draw_balance()
            level.player.draw_damage()
            level.player.draw_health()
            #Creates an exit button on the screen to leave the shop
            exitButton = imageButton(image=pygame.image.load("images/exitShop.png"), pos=(480, 400))
            exitButton.update(screen)

            for item in items:
                mousepos = pygame.mouse.get_pos()
                #checks if buy button is clicked and the item is not already bought
                if event.type == pygame.MOUSEBUTTONDOWN and item.name not in bought:
                    if item.buyButton.checkForInput(mousepos):
                        #checks that the player has enough money to buy the item
                        if level.player.money >= item.cost:
                            #removes the cost of the item from the player's balance
                            level.player.money -= item.cost
                            #if the buff type of the item is "health", the maximum health is incrased based on the buff
                            if item.type == "health":
                                level.player.maximumHealth += item.buff
                                level.player.health = level.player.maximumHealth
                            #if the buff type of the item is "damage", the player damage is increased based on the buff
                            elif item.type == "damage":
                                level.player.damage += item.buff
                            #adds the item name to the list of items already bought
                            bought.append(item.name)
                            #player is no longer in the shop
                            inShop = False
                            #controls are re-enabled
                            controlsDisabled = False


            #Checks if the player clicked the exit button
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousepos = pygame.mouse.get_pos()
                if exitButton.checkForInput(mousepos):
                    #player is no longer in the shop
                    inShop = False
                    #controls are re-enabled
                    controlsDisabled = False
        
        #for loop to go through all the portals in a level
        for portal in level.portal_list:
            #checks if the player is touching a portal
            if level.player.rect.colliderect(portal.rect):
                #saves the player direction as prevDirection before changing the level
                prevDirection = level.player.direction.x
                #the players attributes are saved before changing th elevel
                pmaxhealth = level.player.maximumHealth
                pmoney = level.player.money
                pdamage = level.player.damage
                #currentLevel is increased in increments of 0.5 because every time currentLevel is not a whole number, the level will be set to the shop level
                #As a result, between each "real" level, the player has an opportunity to visit the shop
                currentLevel += 0.5
                if currentLevel == 6.5:
                    end()
                #if currentLevel is not a whole number, the level is set to the shop
                elif currentLevel % 1 != 0:
                    level = shopLevel
                    #Level Header changed
                    LevelText = get_font(15).render("The World Between Worlds", True, "White")
                #The code below changes the level and the level header based on the updated currentLevel when it's a whole number
                elif currentLevel == 2:
                    level = level2
                    LevelText = get_font(15).render("Level 2: Valleys of Jotunheim", True, "White")
                elif currentLevel == 3:
                    level = level3
                    LevelText = get_font(15).render("Level 3: Valleys of Valhalla", True, "White")
                elif currentLevel == 4:
                    level = level4
                    LevelText = get_font(15).render("Level 4: Grounds of Vanheim", True, "White")
                elif currentLevel == 5:
                    level = level5
                    LevelText = get_font(15).render("Level 5: Gardens of Alfheim", True, "White")
                elif currentLevel == 6:
                    level = level6
                    LevelText = get_font(15).render("Level 6: Caves of Nilfheim", True, "White")
                
                #sets up the level with the player attributes stored earlier
                level.setup_level(pmaxhealth, pmoney, pdamage)
                #moves the player in the direction it entered in the portal to stop it from moving
                level.player.control(prevDirection)
        #updates the screen
        pygame.display.flip()

#calls the main menu to start the game as a whole
main_menu()