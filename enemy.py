import pygame
import os
import time
ani = 4
ALPHA = (0, 255, 0) 

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, numimg, source):
        pygame.sprite.Sprite.__init__(self)
        self.numimg = numimg
        self.frame = 0
        self.direction = pygame.math.Vector2(0.001,0)
        self.gravity = 0.8
        self.idle_images = []
        for i in range(0, numimg):
            idle_image = pygame.image.load(os.path.join('images', source,f'tile00{i}.png')).convert()
            idle_image.convert_alpha()  # optimise alpha
            self.idle_images.append(idle_image)

            self.image = self.idle_images[-1]
            self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y  += self.direction.y

    def update(self, x_shift):
        self.rect.x += self.direction.x
        self.apply_gravity()
        self.rect.x += x_shift
        self.frame += 1
        if self.frame > (self.numimg - 2)*7:
            self.frame = 0
        if self.frame %7 == 0:
            self.image = pygame.transform.flip(self.idle_images[self.frame//7], True, False)
