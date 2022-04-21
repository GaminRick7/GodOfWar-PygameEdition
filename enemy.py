import pygame
import os
import time
ani = 4
ALPHA = (0, 255, 0) 

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, numimg, source):
        pygame.sprite.Sprite.__init__(self)
        self.frame = 0
        self.idle_images = []
        for i in range(0, numimg -1):
            idle_image = pygame.image.load(os.path.join('images', source,f'tile00{str(i)}.png')).convert()
            idle_image.convert_alpha()  # optimise alpha
            self.idle_images.append(idle_image)

            self.image = self.idle_images[0]
            self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    
    def update(self):
        self.frame += 1
        if self.frame > 14:
            self.frame = 0
        if self.frame %7 == 0:
            self.image = pygame.transform.flip(self.idle_images[self.frame//7], True, False)
