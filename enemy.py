import pygame
import os
import time
from utility import screen
class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, numwalkimg, numattackimg, source):
        pygame.sprite.Sprite.__init__(self)
        #Health Variables
        self.health = 200
        self.maximumHealth = 200

        #Number of images for attack and walking animations
        self.numwalkimg = numwalkimg
        self.numattackimg = numattackimg

        #Frame counter for walking animation
        self.frame = 0

        #Frame counter for attacking animation
        self.counter = 1

        #Direction vector with x, y
        self.direction = pygame.math.Vector2(1,0)

        #Sets gravity variable
        self.gravity = 0.8

        #Iitially sets the boolean that checks if the enemy is attacking to False
        self.attacking = False

        #Attack direction is set to none
        self.attackdirection = "none"

        #List  of all walking animation
        self.walk_images = []

        #List of all attack images
        self.attack_images = []

        #Two for loops to add walking and attacking images to their respective lists
        for i in range(0, numwalkimg):
            #loads the image by using tilee00 and i as the number added to it (as it is saved in the file directory); then, the image is convertre to access the pygame image features
            walk_image = pygame.image.load(os.path.join('images', source, 'walk', f'tile00{i}.png')).convert()
            #uses convert_alpha() to remove bakground from the image
            walk_image.convert_alpha()
            #appends the image to walk_images
            self.walk_images.append(walk_image)

        for i in range(0, numattackimg):
            #loads the image by using tilee00 and i as the number added to it (as it is saved in the file directory); then, the image is convertre to access the pygame image features
            attack_image = pygame.image.load(os.path.join('images', source, 'attack', f'tile00{i}.png')).convert()
            #uses convert_alpha() to remove bakground from the image
            attack_image.convert_alpha()
            #appends the image to attack_images
            self.attack_images.append(attack_image)
    
        #Sets image of the enemy to the final image of the walk images as the default
        self.image = self.walk_images[-1]
        #sets the rect of the enemy to the imge
        self.rect = self.image.get_rect(topleft = pos)

    def apply_gravity(self):
        """
        Applies gravity to the enemy
        """
        #constantly adds gravity to the y direction of the enemy
        self.direction.y += self.gravity
        #updates the position of the enemy on the screen in accordance to the gravity added to direction.y
        self.rect.y  += self.direction.y


    def draw_health(self):
        """
        Draws a helath indicator above the enemy
        """
        #Draws the enemy health using a red bar ; the width of the bar is determined by its health/2 
        pygame.draw.rect(screen, (255,0,0), (self.rect.x - 30, self.rect.y - 20, self.health/2, 10))
        #Draws a white outline around the enemy health bar to indicate its maximum health capacity; the width of the bar is determined by its health/2 
        pygame.draw.rect(screen, (255,255,255), (self.rect.x- 30, self.rect.y -20, self.maximumHealth/2, 10), 2)


    def update(self, x_shift):
        """
        Args: x_shift
        Returns: none
        Calls all functions associated with the enemy and hecks for other conditions
        """
        #Draws the 
        self.draw_health()
        if self.health <= 0:
            self.kill()
        self.rect.x += x_shift
        if self.attacking == False:
            self.rect.x += self.direction.x
        self.apply_gravity()
        self.frame += 1
        self.counter += 1
        #attacking animation
        if self.attacking == True:
            if self.attackdirection == "right":
                if self.counter > (len(self.attack_images) - 1)*3:
                    self.counter = 0
                    self.attacking = False
                if self.counter %3 == 0:
                    self.image = self.attack_images[self.counter//3]
            if self.attackdirection == "left":
                if self.counter > (len(self.attack_images) - 1)*3:
                    self.counter = 0
                    self.attacking = False
                if self.counter %3 == 0:
                    self.image = pygame.transform.flip(self.attack_images[self.counter//3], True, False)
        #walking animation
        elif self.direction.x < 0:
            if self.frame > (self.numwalkimg - 1)*7:
                self.frame = 0
            if self.frame %7 == 0:
                self.image = pygame.transform.flip(self.walk_images[self.frame//7], True, False)
        elif self.direction.x > 0:
            if self.frame > (self.numwalkimg - 1)*3:
                self.frame = 0
            if self.frame %3 == 0:
                self.image = self.walk_images[self.frame//7]


