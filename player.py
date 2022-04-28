import pygame
import sys
import os

ani = 4
ALPHA = (0, 255, 0) 

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.frame = 0
        self.is_jumping = True
        self.on_ground = False
        self.gravity = 0.35 
        self.acceleration = pygame.math.Vector2(0, self.gravity)
        self.velocity = pygame.math.Vector2(0,0)
        self.position = pygame.math.Vector2(0,0)
        self.direction = pygame.math.Vector2(0,0)
        self.walk_images = []
        self.jump_images = []
        self.attack_images = []
        for i in range(0, 7):
            walk_image = pygame.image.load(os.path.join('images', f'walk00{str(i)}.png')).convert()
            walk_image.convert_alpha()  # optimise alpha
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
        self.direction.x += x
        self.direction.y += y

    def update(self):
        """
        Args: none
        Returns: none
        Update sprite position
        """
        
        if self.rect.centerx > 100 and self.rect.centerx < 850:
            self.rect.x = self.rect.x + self.direction.x
            self.rect.y = self.rect.y + self.direction.y
        elif self.rect.centerx <= 100:
            self.rect.centerx = 101
        elif self.rect.centerx >= 850:
            self.rect.centerx = 849
        # moving left animation
        if self.direction.x < 0:
            self.frame += 1
            if self.frame > 3*ani:
                self.frame = 0
            self.image = pygame.transform.flip(self.walk_images[self.frame // ani], True, False)

        # moving right animation
        if self.direction.x > 0:
            self.frame += 1
            if self.frame > 3*ani:
                self.frame = 0
            self.image = self.walk_images[self.frame//ani]

        if self.direction.y > 0:
            self.frame += 1
            if self.frame > 3*ani:
                self.frame = 0
            self.image = self.jump_images[self.frame//ani]
           
def vertical_movement(self, dt):
    self.velocity.y += self.acceleration
    if self.velocity.y > 7:
        self.velocity.y = 7
    if self.postion.y > 128:
        self.on_ground= True
        self.velocity = 0
        self.position.y = 128
    self.rect.bottom = self.postion.y
