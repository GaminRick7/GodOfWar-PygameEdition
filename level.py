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

        #
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
        self.tiles = pygame.sprite.Group()
        self.invisTiles = pygame.sprite.Group()
        self.portal_list = pygame.sprite.Group()
        self.coin_list = pygame.sprite.Group()
        self.shop_list = pygame.sprite.Group()
        for row_index, row in enumerate(self.level_data):
            for col_index, cell in enumerate(row):
                x = col_index *48
                y = row_index *48
                if cell == "X":
                    tile = Tile((x, y), 48)
                    self.tiles.add(tile)
                if cell == "P":
                    self.player.rect.x = x
                    self.player.rect.bottom = y
                if cell == "E":
                    enemy = Enemy((x, y), 8, 8, "enemy1")
                    self.enemy_list.add(enemy)
                if cell == "I":
                    tile = invisTile((x, y), 48)
                    self.invisTiles.add(tile)
                if cell == "O":
                    portal = Portal((x, y), 48)
                    self.portal_list.add(portal)
                if cell == "C":
                    coin = Coin((x+15, y+15), 48)
                    self.coin_list.add(coin)
                if cell == "S":
                    shop = Shop((x, y - 330), 48)
                    self.shop_list.add(shop)

                    
        
    def scroll_x(self):
        if self.player.attacking == False:
            if self.player.rect.centerx == 849:
                if self.player.direction.x > 0:
                    self.world_shift = -4
            elif self.player.rect.centerx == 101:
                if self.player.direction.x < 0:
                    self.world_shift = 4
            else:
                self.world_shift = 0
            
    def horizontal_movement_collision(self):
        #Normal Tile Collision
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(self.player.rect):
                if self.player.direction.x > 0:
                    self.player.rect.right = sprite.rect.left
                if self.player.direction.x < 0:
                    self.player.rect.left = sprite.rect.right
            ########## NOT WORKING#############
            for enemy in self.enemy_list.sprites():
                if sprite.rect.colliderect(enemy.rect):
                    if enemy.direction.x > 0:
                        enemy.rect.right = sprite.rect.left - 0.5
                        enemy.direction.x = -1
                    elif enemy.direction.x < 0:
                        enemy.rect.left = sprite.rect.right + 0.5
                        enemy.direction.x = 1
            ####################################
        for sprite in self.invisTiles.sprites():
            for enemy in self.enemy_list.sprites():
                if sprite.rect.colliderect(enemy.rect):
                    if enemy.direction.x > 0:
                        enemy.rect.right = sprite.rect.left - 0.5
                        enemy.direction.x = -1
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
                if enemy.rect.x - self.player.rect.x <= 40 and enemy.rect.x - self.player.rect.x >= -40:
                    if enemy.rect.y - self.player.rect.y <= 10 and enemy.rect.y - self.player.rect.y >= -10:
                        if self.player.rect.x - enemy.rect.x < 0:
                            enemy.rect.x += 50
                        if self.player.rect.x - enemy.rect.x > 0:
                            enemy.rect.x -= 50
                        enemy.health -= self.player.damage
                            
                #animation
                self.player.counter += 1
                if self.player.counter > (len(self.player.attack_images) - 1):
                    self.player.counter = 0
                    if self.player.leftorright == "right":
                        self.player.image = self.player.walk_images[0]
                    if self.player.leftorright == "left":
                        self.player.image = pygame.transform.flip(self.player.walk_images[0], True, False)
                    self.player.attacking = False
                elif self.player.leftorright == "right":
                    if self.player.counter > (len(self.player.attack_images) - 1):
                        self.player.counter = 0
                        self.player.image = self.player.walk_images[0]
                    elif self.player.frame %3 == 0:
                        self.player.image = self.player.attack_images[self.player.counter//3]
                elif self.player.leftorright == "left":
                    if self.player.frame %3 == 0:
                        self.player.image = pygame.transform.flip(self.player.attack_images[self.player.counter // 3], True, False)

            elif enemy.rect.colliderect(self.player.rect):
                enemy.attacking = True
                if enemy.rect.x - self.player.rect.x < 0:
                    enemy.attackdirection = "right"
                if enemy.rect.x - self.player.rect.x > 0:
                    enemy.attackdirection = "left"
                if enemy.counter == 0:
                    print("player moved")
                    if enemy.rect.colliderect(self.player.rect):
                        self.player.health -= 25
                    print(self.player.health)
                    if enemy.attackdirection == "right":
                        self.player.rect.x += 20
                    else:
                        self.player.rect.x -= 20

        for coin in self.coin_list:
            if coin.rect.colliderect(self.player.rect):
                coin.kill()
                self.player.money += 1
                print(self.player.money)

    def run(self):
        self.scroll_x()
        self.tiles.update(self.world_shift)
        self.invisTiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.invisTiles.draw(self.display_surface)
        self.shop_list.update(self.world_shift)
        self.shop_list.draw(self.display_surface)
        self.coin_list.update(self.world_shift)
        self.coin_list.draw(self.display_surface)
        self.player.update()
        self.player_list.draw(self.display_surface)
        self.vertical_movement_collision()
        self.horizontal_movement_collision()
        self.collisions()
        self.enemy_list.draw(self.display_surface)
        self.enemy_list.update(self.world_shift)
        self.portal_list.update(self.world_shift)
        self.portal_list.draw(self.display_surface)
'''
coins
shop
'''