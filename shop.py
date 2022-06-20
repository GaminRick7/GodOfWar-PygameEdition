import pygame
import os
from button import imageButton

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
        self.buyImage = pygame.image.load("images/buy.png")
        self.buyImage = pygame.transform.scale(self.buyImage, (78,34))
        self.buyButton = imageButton(image=self.buyImage, pos=(900, info[5][1]))

        self.rect = self.image.get_rect(topleft = info[5])