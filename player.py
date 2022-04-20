import pygame
import sys
import os

ani = 4
ALPHA = (0, 255, 0) 

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.movex = 0
        self.movey = 0
        self.frame = 0
        self.is_jumping = True
        self.is_falling = False
        self.walk_images = []
        self.jump_images = []
        for i in range(0, 7):
            walk_image = pygame.image.load(os.path.join('images', f'walk00{str(i)}.png')).convert()
            walk_image.convert_alpha()  # optimise alpha
            walk_image.set_colorkey(ALPHA)  # set alpha
            self.walk_images.append(walk_image)
            self.image = self.walk_images[0]
            self.rect = self.image.get_rect()

        for i in range(0, 7):
            jump_image = pygame.image.load(os.path.join('images', 'jump', f'tile00{str(i)}.png')).convert()
            jump_image.convert_alpha()  # optimise alpha
            jump_image.set_colorkey(ALPHA)  # set alpha
            self.jump_images.append(jump_image)


    def control(self, x, y):
        """
        Args: self, x, y
        Returns: none
        control player movement
        """
        self.movex += x
        self.movey += y

    def update(self):
        """
        Update sprite position
        """

        self.rect.x = self.rect.x + self.movex
        self.rect.y = self.rect.y + self.movey

        # moving left
        if self.movex < 0:
            self.frame += 1
            if self.frame > 3*ani:
                self.frame = 0
            self.image = pygame.transform.flip(self.walk_images[self.frame // ani], True, False)

        # moving right
        if self.movex > 0:
            self.frame += 1
            if self.frame > 3*ani:
                self.frame = 0
            self.image = self.walk_images[self.frame//ani]

        if self.movey > 0:
            self.frame += 1
            if self.frame > 3*ani:
                self.frame = 0
            self.image = self.jump_images[self.frame//ani]
           
