import pygame
import sys
import os
from utility import get_font, screen
worldx = 960
worldy = 480

screen = pygame.display.set_mode((worldx, worldy))
ani = 4
ALPHA = (0, 255, 0) 

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.frame = 0
        self.counter = 0
        self.attacking = False
        self.maximumHealth = 200
        self.health = 200
        self.money = 0

        self.direction = pygame.math.Vector2(0,0)
        self.leftorright = "right"
        self.gravity = 0.8
        self.jump_speed = -11
        self.speed = 2

        self.walk_images = []
        self.jump_images = []
        self.attack_images = []
        for i in range(0, 7):
            walk_image = pygame.image.load(os.path.join('images', f'walk00{i}.png')).convert()
            walk_image.convert_alpha()  # optimise alpha
            self.walk_images.append(walk_image)
            self.image = self.walk_images[0]
            self.rect = self.image.get_rect()

        for i in range(0, 7):
            jump_image = pygame.image.load(os.path.join('images', 'jump', f'tile00{str(i)}.png')).convert()
            jump_image.convert_alpha()  # optimise alpha
            jump_image.set_colorkey(ALPHA)  # set alpha
            self.jump_images.append(jump_image)
        
        for i in range(0, 29):
            attack_image = pygame.image.load(os.path.join('images', 'attack', f'tile00{str(i)}.png')).convert()
            attack_image.convert_alpha()  # optimise alpha
            self.attack_images.append(attack_image)
        
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y  += self.direction.y
    
    def jump(self):
        self.direction.y = self.jump_speed
    
    def control(self, x):
        """
        Args: self, x, y
        Returns: none
        control player movement
        """
        self.direction.x += x
    
    def draw_health(self):
        pygame.draw.rect(screen, (255,0,0), (20, 10, self.health, 25))
        pygame.draw.rect(screen, (255,255,255), (20,10, self.maximumHealth, 25), 4)
        heart = pygame.image.load(os.path.join('images', 'heart.png'))
        screen.blit(heart, (5,6))

    def draw_balance(self):
        coin = pygame.image.load(os.path.join('images', 'coins', 'tile000.png'))
        coin = pygame.transform.scale(coin, (32, 32))
        screen.blit(coin, (850,6))
        coinText = get_font(22).render(str(self.money), True, "White")
        coinRect = coinText.get_rect(topleft=(890, 12))
        screen.blit(coinText, coinRect)

    def update(self):
        """
        Args: none
        Returns: none
        Update sprite position
        """
        self.draw_health()
        self.draw_balance()
        if self.attacking != True:
            if self.rect.centerx > 100 and self.rect.centerx < 850:
                self.speed = 2
                self.rect.x = self.rect.x + self.direction.x * self.speed
                self.rect.y = self.rect.y + self.direction.y
            elif self.rect.centerx <= 100:
                self.speed = 1
                self.rect.centerx = 101
            elif self.rect.centerx >= 850:
                self.speed = 1
                self.rect.centerx = 849.9

        self.frame += 1


        if self.attacking == False:
            if self.direction.x < 0:
                if self.frame > 3*ani:
                    self.frame = 0
                self.image = pygame.transform.flip(self.walk_images[self.frame // ani], True, False)

            # moving right animation
            elif self.direction.x > 0:
                if self.frame > 3*ani:
                    self.frame = 0
                self.image = self.walk_images[self.frame//ani]
        
        if self.direction.x < 0:
            self.leftorright = "left"
        elif self.direction.x > 0:
            self.leftorright = "right"