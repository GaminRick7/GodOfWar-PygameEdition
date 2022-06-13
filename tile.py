import pygame
import sys
import os

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size) :
        super().__init__()
        self.image = pygame.Surface((size, size))
        tile = pygame.image.load(os.path.join('images', 'tileset2.png')).convert()
        tile = pygame.transform.scale(tile, (48, 48))
        self.image = tile
        self.rect = self.image.get_rect(topleft = pos)
    
    def update(self, x_shift):
        self.rect.x += x_shift

class invisTile(pygame.sprite.Sprite):
    def __init__(self, pos, size) :
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.set_alpha(0)
        self.rect = self.image.get_rect(topleft = pos)
    
    def update(self, x_shift):
        self.rect.x += x_shift