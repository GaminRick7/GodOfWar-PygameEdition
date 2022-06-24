"""
ICS3U
Raihaan Sandhu
This file is responsible for the player, its attributes, and its animations
"""

import pygame
import sys
import os
from utility import get_font, screen

class Player(pygame.sprite.Sprite):
    def __init__(self, maximumHealth, money, damage):
        '''
        Args: maximumHealth, money, damage
        Returns: None
        Creates the player, its image, its attributes, and its animations
        '''
        pygame.sprite.Sprite.__init__(self)
        
        #PLAYER ATTRIBUTES (maximum health, health, money, damage points)
        #When the level changes, the player attributes tended to reset
        #Thus, to counteract this, any attributes are saved as variables in main.py every time the level switches and are used as arguments when creating the player again to save the attributes across levels
        self.maximumHealth = maximumHealth
        self.health = maximumHealth
        self.money = money
        self.damage = damage


        #Movement and attacking variables
        self.attacking = False
        self.direction = pygame.math.Vector2(0,0)
        self.leftorright = "right"
        self.gravity = 0.8
        self.jump_speed = -11
        self.speed = 2

        #Animation Variables
        self.frame = 0 #frame tracker for walking animation
        self.counter = 0 #frame tracker
        self.walk_images = []
        self.jump_images = []
        self.attack_images = []

        #uses a for loop to load all the walking images
        for i in range(0, 7):
            #each image is loaded, made transparent where need be, and appended to walk_images
            walk_image = pygame.image.load(os.path.join('images', f'walk00{i}.png')).convert()
            walk_image.convert_alpha() 
            self.walk_images.append(walk_image)
            self.image = self.walk_images[0]
            #the rect of the player is based on the size of the image
            self.rect = self.image.get_rect()


        #each image is loaded, made transparent where need be, and appended to attack_images
        for i in range(0, 29):
            attack_image = pygame.image.load(os.path.join('images', 'attack', f'tile00{str(i)}.png')).convert()
            attack_image.convert_alpha() 
            self.attack_images.append(attack_image)
        
    def apply_gravity(self):
        '''
        Args: None
        Returns: None
        Updates y-position of the player based on gravity
        '''
        #constantly adds gravity to the y direction of the enemy
        self.direction.y += self.gravity
        #updates the position of the enemy on the screen in accordance to the gravity added to direction.y
        self.rect.y  += self.direction.y
    
    def jump(self):
        '''
        Args: None
        Returns: None
        Updates player's y-direction based on the player jumping
        '''
        self.direction.y = self.jump_speed
    
    def control(self, x):
        """
        Args: self, x, y
        Returns: none
        control player movement
        """
        #adds to the x direction of the player based on keyboard input
        self.direction.x += x
    
    def draw_health(self):
        '''
        Args: None
        Returns: None
        Draws health bar
        '''
        #draws the of the player in red
        pygame.draw.rect(screen, (255,0,0), (20, 10, self.health, 25))
        #draws a maximum health outline in white
        pygame.draw.rect(screen, (255,255,255), (20,10, self.maximumHealth, 25), 4)
        #displays a heart next to the health bar
        heart = pygame.image.load(os.path.join('images', 'heart.png'))
        screen.blit(heart, (5,6))

    def draw_balance(self):
        '''
        Args: None
        Returns: None
        Draws coin balance
        '''
        #displays a coin next to the player's balance
        coin = pygame.image.load(os.path.join('images', 'coins', 'tile000.png'))
        coin = pygame.transform.scale(coin, (32, 32))
        screen.blit(coin, (820,6))
        #displays the player's balance
        coinText = get_font(22).render(str(self.money), True, "White")
        coinRect = coinText.get_rect(topleft=(860, 12))
        screen.blit(coinText, coinRect)

    def draw_damage(self):
        '''
        Args: None
        Returns: None
        Draws player's damage
        '''
        #displays a sword next to the player's balance
        damage = pygame.image.load(os.path.join('images', 'sword.png'))
        damage = pygame.transform.scale(damage, (32, 32))
        screen.blit(damage, (700,6))
         #displays the player's damage
        damageText = get_font(22).render(str(self.damage), True, "White")
        damageRect = damageText.get_rect(topleft=(750, 12))
        screen.blit(damageText, damageRect)

    def update(self):
        """
        Args: none
        Returns: none
        Updates sprite position
        """
        #Drawing functions
        self.draw_health()
        self.draw_balance()
        self.draw_damage()

        #Limits the player from ever going past 100 px and 850 px
        if self.attacking != True:
            #While the player is within the confines of 100px and 850 px
            if self.rect.centerx > 100 and self.rect.centerx < 850:
                #updates the player rect on the x-axis based on the direction multiplied by the speed
                self.speed = 2
                self.rect.x = self.rect.x + self.direction.x * self.speed
                #updates the player rect on the y-axis based on the direction
                self.rect.y = self.rect.y + self.direction.y
            #if the player is at either 100 or 850 px:
            # - speed is set to 1
            # - the player is moved slightly away from the confines
            elif self.rect.centerx <= 100:
                self.speed = 1
                self.rect.centerx = 101
            elif self.rect.centerx >= 850:
                self.speed = 1
                self.rect.centerx = 849.9

        #increases the frame for the player walking
        self.frame += 1

        # checks that the player is not attacking
        if self.attacking == False:
            #if the player frame is greater than 0, it resets the frame to 0
            if self.frame > 12:
                self.frame = 0
            #moving left animation that flips the image and uses frame as the index for walk_images
            if self.direction.x < 0:
                self.image = pygame.transform.flip(self.walk_images[self.frame // 4], True, False)

            # moving right animation that uses frame as the index for walk_images
            elif self.direction.x > 0:
                self.image = self.walk_images[self.frame//4]

        #based on the player's direction, the leftorright variable is set to "left" or "right"
        if self.direction.x < 0:
            self.leftorright = "left"
        elif self.direction.x > 0:
            self.leftorright = "right"