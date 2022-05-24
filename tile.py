import pygame
import sys

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size) :
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill('grey')
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