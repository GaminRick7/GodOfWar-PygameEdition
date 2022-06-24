"""
ICS3U
Raihaan Sandhu
This file is responsible for creating all the objects on the screen and checking for interactions between various objects
"""

import pygame
from tile import Tile, invisTile
from player import Player
from enemy import Enemy
import parallax
from math import inf
import os
from portal import Portal
from shop import Shop
from coin import Coin

class Level:
    def __init__(self, level_data, surface, bgfolder, bgnumber):
        #sets a surface to blit the sprites on
        self.display_surface = surface

        #level map
        self.level_data = level_data

        #sets scroll speed of the tiles to 0
        self.scroll_speed = 0

        #Uses the PyParallax module to create a parallax backround
        self.bg = parallax.ParallaxSurface((960, 480), pygame.RLEACCEL)

        # sets a counter i to 1
        i = 1

        #sets the speed of the parallax tile
        speed = 5.5
        self.bg.add(os.path.join('images', f'{bgfolder}',f'0{i}.png'), inf)
        for image in range(bgnumber-1):
            i+= 1
            speed -= 0.5
            self.bg.add(os.path.join('images', f'{bgfolder}',f'0{i}.png'), speed)
        
        #variable to keep track of how many times the player has jumped
        self.jumpCount = 0


    def setup_level(self, pmaxhealth, pmoney, pdamage):
        # Spawn Player #
        self.player = Player(pmaxhealth, pmoney, pdamage)  # spawn player
        self.player_list = pygame.sprite.Group()
        self.player_list.add(self.player)


        # Enemy #
        self.enemy_list = pygame.sprite.Group()


        #World Shift
        self.world_shift = 0

        #Setup Tile Map#

        #Sprite groups for tiles, portals, coins, and shops
        self.tiles = pygame.sprite.Group()
        self.invisTiles = pygame.sprite.Group()
        self.portal_list = pygame.sprite.Group()
        self.coin_list = pygame.sprite.Group()
        self.shop_list = pygame.sprite.Group()


        #two for loops that go through each row and column of the level map
        #uses enumaerate which adds counter to the iterable
        for row_index, row in enumerate(self.level_data):
            for col_index, cell in enumerate(row):
                #the x value and y value are multipled by 48 to account for tile size
                x = col_index *48
                y = row_index *48
                #creates a tile where there is an X on the level map
                if cell == "X":
                    tile = Tile((x, y), 48)
                    self.tiles.add(tile)
                #creates the player where there is an P on the level map
                if cell == "P":
                    self.player.rect.x = x
                    self.player.rect.bottom = y
                #creates an enemy where there is an E on the level map
                if cell == "E":
                    enemy = Enemy((x, y), 8, 8, "enemy1")
                    self.enemy_list.add(enemy)
                if cell == "G":
                    enemy = Enemy((x, y), 8, 8, "enemy2")
                    self.enemy_list.add(enemy)
                if cell == "K":
                    enemy = Enemy((x, y), 4, 8, "enemy3")
                    self.enemy_list.add(enemy)
                #creates an invisible tile where there is an I on the level map
                if cell == "I":
                    tile = invisTile((x, y), 48)
                    self.invisTiles.add(tile)
                #Creates the portal where there is an O on the map
                if cell == "O":
                    portal = Portal((x, y))
                    self.portal_list.add(portal)
                #Creates a coin where there is a C on the map
                if cell == "C":
                    coin = Coin((x+15, y+15))
                    self.coin_list.add(coin)
                #Creates a shop where there is an S on the map
                if cell == "S":
                    shop = Shop((x, y - 330))
                    self.shop_list.add(shop)

                    
        
    def scroll_x(self):
        
        if self.player.attacking == False:
            #if the player is at almost at its maximum possible right boundary of the screen (849) and is continuing to move right, world_shift is set to -4
            if self.player.rect.centerx == 849:
                if self.player.direction.x > 0:
                    self.world_shift = -4
            #if the player is at almost at its maximum possible right boundary of the screen (101) and is continuing to move right, world_shift is set to 4
            elif self.player.rect.centerx == 101:
                if self.player.direction.x < 0:
                    self.world_shift = 4
            else:
                self.world_shift = 0
            
    def horizontal_movement_collision(self):
        #Normal Tile Collision
        #For loop to cycle through every tile and check for collision
        for sprite in self.tiles.sprites():
            #checks for tile collision with player
            if sprite.rect.colliderect(self.player.rect):
                #if the player is moving right, the left of the tile is set to the right of the player
                if self.player.direction.x > 0:
                    self.player.rect.right = sprite.rect.left
                #if the player is moving left, the right of the tile is set to the left of the player
                if self.player.direction.x < 0:
                    self.player.rect.left = sprite.rect.right
            #for loop to cycle through each enemy sprite and check for tile collision
            for enemy in self.enemy_list.sprites():
                #checks for tile collision with enemy
                if sprite.rect.colliderect(enemy.rect):
                    # if the enemy is moving right, its right side is set 0.5 pixels away from the tile's left side, then its direction is switched to the opposite
                    if enemy.direction.x > 0:
                        enemy.rect.right = sprite.rect.left - 0.5
                        enemy.direction.x = -1
                    # if the enemy is moving left, its left side is set 0.5 pixels away from the tile's right side, then its direction is switched to the opposite
                    elif enemy.direction.x < 0:
                        enemy.rect.left = sprite.rect.right + 0.5
                        enemy.direction.x = 1
            ####################################
        #for loops to cycle through each enemy sprite and invisible tile to check for tile collision
        for sprite in self.invisTiles.sprites():
            for enemy in self.enemy_list.sprites():
                #checks for collision
                if sprite.rect.colliderect(enemy.rect):
                    # if the enemy is moving right, its right side is set 0.5 pixels away from the tile's left side, then its direction is switched to the opposite
                    if enemy.direction.x > 0:
                        enemy.rect.right = sprite.rect.left - 0.5
                        enemy.direction.x = -1
                    # if the enemy is moving left, its left side is set 0.5 pixels away from the tile's right side, then its direction is switched to the opposite
                    elif enemy.direction.x < 0:
                        enemy.rect.left = sprite.rect.right + 0.5
                        enemy.direction.x = 1
                
    
    
    def vertical_movement_collision(self):
        #applies gravity to the player/calls apply_gravity()
        self.player.apply_gravity()
        #a for loop to check player collision with each and every tile
        for sprite in self.tiles.sprites():
            #checks tile collision with player
            if sprite.rect.colliderect(self.player.rect):
                #resets the number of times the player has jumped
                self.jumpCount = 0
                #checks if the player is jumping
                if self.player.direction.y > 0:
                    #sets the bottom of the player as the top of the tile
                    self.player.rect.bottom = sprite.rect.top
                    #ends the jump
                    self.player.direction.y = 0
                #if the player is not jumping 
                if self.player.direction.y < 0:
                    #sets the top of the player as the bottom of the tile
                    self.player.rect.top = sprite.rect.bottom
                    self.player.direction.y = 0
            #a for loop to check player collision with each and every tile
            #uses the same logic as the player
            for enemy in self.enemy_list.sprites():
                if sprite.rect.colliderect(enemy.rect):
                    if enemy.direction.y > 0:
                        enemy.rect.bottom = sprite.rect.top
                        enemy.direction.y = 0
                    if enemy.direction.y < 0:
                        enemy.rect.top = sprite.rect.bottom
                        enemy.direction.y = 0


    def collisions(self):
        '''
        Args: self
        Returns: None
        This function is reponsible for all interactions between the player and the enemies
        '''
        for enemy in self.enemy_list.sprites():
            if self.player.attacking == True:
                #checks whether the player is within 40 px of the enemy on the x axis
                if enemy.rect.x - self.player.rect.x <= 40 and enemy.rect.x - self.player.rect.x >= -40:
                    #checks whether the player is with 10 px of the enemy on the y axis
                    if enemy.rect.y - self.player.rect.y <= 30 and enemy.rect.y - self.player.rect.y >= -30:
                        # checks if the enemy is on the right 
                        if self.player.rect.x - enemy.rect.x < 0:
                            #applies knockback effect of 50 px to the right
                            enemy.rect.x += 50
                        #checks if enemy is on the left
                        elif self.player.rect.x - enemy.rect.x > 0:
                            enemy.rect.x -= 50
                        #subtracts player's damage from the enemy's health
                        enemy.health -= self.player.damage
                            
                #Attacking animation
                #Uses player.counter as the index for the player attack_images
                self.player.counter += 1
                #if the counter is greater than 
                if self.player.counter > (len(self.player.attack_images) - 1):
                    self.player.counter = 0
                    #depending on whether the player is facing left or right, the player image is flipped and set to walk_images[0]
                    if self.player.leftorright == "right":
                        self.player.image = self.player.walk_images[0]
                    if self.player.leftorright == "left":
                        self.player.image = pygame.transform.flip(self.player.walk_images[0], True, False)
                    self.player.attacking = False
                #depending on whether the player is facing left or right, the player image is flipped and set to attack_images[counter//3]
                elif self.player.leftorright == "right":
                    if self.player.frame %3 == 0:
                        self.player.image = self.player.attack_images[self.player.counter//3]
                elif self.player.leftorright == "left":
                    if self.player.frame %3 == 0:
                        self.player.image = pygame.transform.flip(self.player.attack_images[self.player.counter // 3], True, False)
            
            #checks if the player collides with the enemy
            elif enemy.rect.colliderect(self.player.rect):
                #sets enemy.attacking to true which triggers the attack animation for the enemy
                enemy.attacking = True
                #checks if whether the player is on the right or the left of the enemy
                if enemy.rect.x - self.player.rect.x < 0:
                    enemy.attackdirection = "right"
                if enemy.rect.x - self.player.rect.x > 0:
                    enemy.attackdirection = "left"
                #if the animatin attacking animation is finished
                if enemy.counter == 0:
                    #if the player is still in contact with the enemy 25 hp is subtracted from the player
                    if enemy.rect.colliderect(self.player.rect):
                        self.player.health -= 25
                        #depending on whether the enemy is attacking left or right, a knockback effect is applied on the player
                    if enemy.attackdirection == "right":
                        self.player.rect.x += 20
                    else:
                        self.player.rect.x -= 20

        #for loop to cycle through every coin and check for player collision
        for coin in self.coin_list:
            #checks if the coin collided with the player
            if coin.rect.colliderect(self.player.rect):
                #removes the coin from the screen
                coin.kill()
                #adds 1 to the players balance
                self.player.money += 1

    def run(self):
        #World scroll
        self.scroll_x()

        #Tiles
        self.tiles.update(self.world_shift)
        self.invisTiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.invisTiles.draw(self.display_surface)

        #Shop
        self.shop_list.update(self.world_shift)
        self.shop_list.draw(self.display_surface)

        #Coins
        self.coin_list.update(self.world_shift)
        self.coin_list.draw(self.display_surface)

        #Player
        self.player.update()
        self.player_list.draw(self.display_surface)

        #Collisions
        self.vertical_movement_collision()
        self.horizontal_movement_collision()
        self.collisions()

        #Enemies
        self.enemy_list.draw(self.display_surface)
        self.enemy_list.update(self.world_shift)

        #Portal
        self.portal_list.update(self.world_shift)
        self.portal_list.draw(self.display_surface)
'''
coins
shop
'''