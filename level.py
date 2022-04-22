import pygame
from tile import Tile

class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.level_data = level_data
