import pygame
import os
from button import imageButton

class Shop(pygame.sprite.Sprite):
    def __init__(self, pos) :
        '''
        Args: pos
        Returns: none
        Creates the Shop
        '''
        super().__init__()
        #loads the image of the shop
        self.image = pygame.image.load(os.path.join('images', 'shop.png'))
        #uses the image as the rect and places it in the given position
        self.rect = self.image.get_rect(topleft = pos)
    
    def update(self, x_shift):
        '''
        Args: x_shift
        Returns: none
        Updates the shop's position
        '''
        self.rect.x += x_shift

class ShopItem(pygame.sprite.Sprite):
    def __init__(self, info) :
        '''
        Args: info
        Returns: None
        Creates a Shop Item
        This function is responsible for controlling the attributes of each shop item
        '''
        super().__init__()
        #the image of the item is the item icon
        self.image = pygame.image.load(os.path.join('images', 'shopIcons', f'{info[0]}.png'))
        #pulls the name, buff type, buff, cost, and position from the info list
        self.name = info[1]
        self.type = info[2]
        self.buff = info[3]
        self.cost = info[4]
        #Creates a Buy Button using the image which is then scaled down
        self.buyImage = pygame.image.load("images/buy.png")
        self.buyImage = pygame.transform.scale(self.buyImage, (78,34))
        #Creates a button with the buy button image on position 900, and the y value of the item icon (info[5][1])
        self.buyButton = imageButton(image=self.buyImage, pos=(900, info[5][1]))

        #the rect is determined by the image and placed on position in info[5]
        self.rect = self.image.get_rect(topleft = info[5])