import pygame
import os

class Portal(pygame.sprite.Sprite):
    def __init__(self, pos, size) :
        super().__init__()
        self.ani_images = []
        self.counter = 0
        for i in range(7):
            ani_image = pygame.image.load(os.path.join('images', 'portal', f'tile00{i}.png'))
            self.ani_images.append(ani_image)
        self.image = self.ani_images[2]
        self.rect = self.image.get_rect(topleft = pos)
    
    def update(self, x_shift):
        self.rect.x += x_shift
        self.counter += 1
        if self.counter > 26:
            self.counter = 0
        if self.counter%4 == 0:
            self.image = self.ani_images[self.counter//4]
    
