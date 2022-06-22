import pygame
import os

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size) :
        '''
        Args: pos, size
        Returns: none
        Creates a tile based on the tile image, position and size
        '''
        super().__init__()
        #loads image
        tile = pygame.image.load(os.path.join('images', 'tileset2.png')).convert()
        #scales to 48x48
        tile = pygame.transform.scale(tile, (48, 48))
        #image of the tile is set to the loaded image
        self.image = tile
        #given position, the rect of the image is at pos
        self.rect = self.image.get_rect(topleft = pos)
    
    def update(self, x_shift):
        '''
        Args: x_shift
        Returns: none
        Updates the tile's position
        '''
        self.rect.x += x_shift

class invisTile(pygame.sprite.Sprite):
    def __init__(self, pos, size) :
        super().__init__()
        #a transparent surface is created
        self.image = pygame.Surface((size, size))
        self.image.set_alpha(0)
        #given position, the rect of the image is at pos
        self.rect = self.image.get_rect(topleft = pos)
    
    def update(self, x_shift):
        '''
        Args: x_shift
        Returns: none
        Updates the tile's position
        '''
        self.rect.x += x_shift