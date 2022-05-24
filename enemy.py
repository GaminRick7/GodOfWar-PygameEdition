import pygame
import os
import time
ani = 4
ALPHA = (0, 255, 0) 

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, numwalkimg, numattackimg, source):
        pygame.sprite.Sprite.__init__(self)
        self.numwalkimg = numwalkimg
        self.numattackimg = numattackimg
        self.frame = 0
        self.counter = 0
        self.direction = pygame.math.Vector2(1,0)
        self.gravity = 0.8
        self.attacking = False
        self.idle_images = []
        self.attack_images = []
        for i in range(0, numwalkimg):
            idle_image = pygame.image.load(os.path.join('images', source,f'tile00{i}.png')).convert()
            idle_image.convert_alpha()  # optimise alpha
            self.idle_images.append(idle_image)

        for i in range(0, numattackimg - 1):
            attack_image = pygame.image.load(os.path.join('images', source, 'attack', f'tile00{i}.png')).convert()
            attack_image.convert_alpha()  # optimise alpha
            self.attack_images.append(attack_image)
    

        self.image = self.idle_images[-1]
        self.rect = self.image.get_rect(topleft = pos)

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y  += self.direction.y

    def update(self, x_shift):
        self.rect.x += x_shift
        self.rect.x += self.direction.x
        self.apply_gravity()
        self.frame += 1
        if self.direction.x < 0:
            if self.frame > (self.numwalkimg - 1)*7:
                self.frame = 0
            if self.frame %7 == 0:
                self.image = pygame.transform.flip(self.idle_images[self.frame//7], True, False)
        if self.direction.x > 0:
            if self.frame > (self.numwalkimg - 1)*3:
                self.frame = 0
            if self.frame %3 == 0:
                self.image = self.idle_images[self.frame//7]
        if self.attacking == True:
            if self.counter > (self.numattackimg - 1)*3:
                self.counter = 0
            if self.counter %3 == 0:
                self.image = self.attack_images[self.counter//7]

