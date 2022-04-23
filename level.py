import pygame
from tile import Tile

class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.level_data = level_data

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                if cell == "X":
                    x = col_index *48
                    y = row_index *48
                    tile = Tile((x, y), 48)
                    self.tiles.add(tile)
    
    def run(self):
        self.tiles.update(-4)
        self.tiles.draw(self.display_surface)
