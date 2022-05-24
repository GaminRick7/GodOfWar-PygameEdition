import pygame
from tile import Tile, invisTile
from player import Player
from enemy import Enemy
import parallax
from math import inf
import os

class Level:
    def __init__(self, level_data, surface, bgfolder, bgnumber):
        self.display_surface = surface
        self.level_data = level_data
        self.scroll_speed = 0
        self.bg = parallax.ParallaxSurface((960, 480), pygame.RLEACCEL)
        # clouds should not move at all
        i = 1
        speed = 3.5
        self.bg.add(os.path.join('images', f'{bgfolder}',f'0{i}.png'), inf)
        for image in range(bgnumber-1):
            i+= 1
            speed -= 0.5
            self.bg.add(os.path.join('images', f'{bgfolder}',f'0{i}.png'), speed)

    def setup_level(self, layout):
        # Spawn Player #
        self.player = Player()  # spawn player
        self.player_list = pygame.sprite.Group()
        self.player_list.add(self.player)

        # Enemy #
        self.enemy_list = pygame.sprite.Group()


        #World Shift
        self.world_shift = 0

        #Setup Tile Map#
        self.tiles = pygame.sprite.Group()
        self.invisTiles = pygame.sprite.Group()
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                if cell == "X":
                    x = col_index *48
                    y = row_index *48
                    tile = Tile((x, y), 48)
                    self.tiles.add(tile)
                if cell == "P":
                    self.player.rect.x = col_index *48
                    self.player.rect.bottom = row_index *48
                if cell == "E":
                    print(col_index *48, row_index *48)
                    enemy = Enemy((col_index *48, row_index *48), 4, 9, "enemy1")
                    self.enemy_list.add(enemy)
                if cell == "I":
                    x = col_index *48
                    y = row_index *48
                    tile = invisTile((x, y), 48)
                    self.invisTiles.add(tile)
                    
        
    def scroll_x(self):
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
            for enemy in self.enemy_list.sprites():
                if sprite.rect.colliderect(enemy.rect):
                    if enemy.direction.x > 0:
                        enemy.rect.right = sprite.rect.left
                    if enemy.direction.x < 0:
                        enemy.rect.left = sprite.rect.right
        for sprite in self.invisTiles.sprites():
            for enemy in self.enemy_list.sprites():
                if sprite.rect.colliderect(enemy.rect):
                    if enemy.direction.x > 0:
                        enemy.rect.right = sprite.rect.left - 0.5
                        enemy.direction.x = -1
                        print(enemy.direction.x)
                    elif enemy.direction.x < 0:
                        enemy.rect.left = sprite.rect.right + 0.5
                        enemy.direction.x = 1
                        print(enemy.direction.x)
                
    
    
    def vertical_movement_collision(self):
        self.player.apply_gravity()
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(self.player.rect):
                if self.player.direction.y > 0:
                    self.player.rect.bottom = sprite.rect.top
                    self.player.direction.y = 0
                if self.player.direction.y < 0:
                    self.player.rect.top = sprite.rect.bottom
                    self.player.direction.y = 0
            for enemy in self.enemy_list.sprites():
                if sprite.rect.colliderect(enemy.rect):
                    if enemy.direction.y > 0:
                        enemy.rect.bottom = sprite.rect.top
                        enemy.direction.y = 0
                    if enemy.direction.y < 0:
                        enemy.rect.top = sprite.rect.bottom
                        enemy.direction.y = 0


    def epcollision(self):
        for enemy in self.enemy_list.sprites():
            if enemy.rect.colliderect(self.player.rect):
                enemy.attacking = True

    def run(self):
        self.scroll_x()
        self.tiles.update(self.world_shift)
        self.invisTiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.invisTiles.draw(self.display_surface)
        self.player.update()
        self.player_list.draw(self.display_surface)
        self.vertical_movement_collision()
        self.horizontal_movement_collision()
        self.epcollision()
        self.enemy_list.draw(self.display_surface)
        self.enemy_list.update(self.world_shift)
