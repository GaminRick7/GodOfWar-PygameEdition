import pygame
from tile import Tile
from player import Player
from enemy import Enemy

class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.level_data = level_data

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
                    self.enemy = Enemy(col_index *48, row_index *48, 4, "enemy1")
                    self.enemy_list.add(self.enemy)
                    
    
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
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(self.player.rect):
                if self.player.direction.x > 0:
                    self.player.rect.right = sprite.rect.left
                if self.player.direction.x < 0:
                    self.player.rect.left = sprite.rect.right
    
    def vertical_movement_collision(self):
        self.player.apply_gravity()
        for sprite in self.tiles.sprites():
            if sprite.rect.bottom.colliderect(self.player.rect):
                self.player.rect.bottom = sprite.rect.top
                self.player.direction.y = 0
            if sprite.rect.top.colliderect(self.player.rect):
                self.player.rect.top = sprite.rect.bottom
                self.player.direction.y = 0


    def run(self):
        self.scroll_x()
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.player.update()
        self.player_list.draw(self.display_surface)
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.enemy_list.draw(self.display_surface)
        self.enemy.update()
