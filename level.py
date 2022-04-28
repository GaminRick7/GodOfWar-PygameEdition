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
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x
        
        if player_x < 200:
            self.world_shift = 8
            player.speed = 0

    def run(self):
        self.player.update()
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
