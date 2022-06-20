import pygame
import os

class Shop(pygame.sprite.Sprite):
    def __init__(self, pos, size) :
        super().__init__()
        shopImage = pygame.image.load(os.path.join('images', 'shop.png'))
        self.image = shopImage
        self.rect = self.image.get_rect(topleft = pos)
    
    def update(self, x_shift):
        self.rect.x += x_shift

class ShopItem(pygame.sprite.Sprite):
    def __init__(self, info) :
        super().__init__()
        self.image = pygame.image.load(os.path.join('images', 'shopIcons', f'{info[0]}.png'))
        self.name = info[1]
        self.type = info[2]
        self.buff = info[3]
        self.cost = info[4]
        self.rect = self.image.get_rect(topleft = info[5])