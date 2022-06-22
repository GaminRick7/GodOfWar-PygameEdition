import pygame
import os

class Coin(pygame.sprite.Sprite):
    def __init__(self, pos) :
        '''
        Args: pos
        Returns: none
        Creates a coin
        '''
        super().__init__()
        # list of coin animation images 
        self.ani_images = []
        #counter for index of the animation images
        self.counter = 0
        #for loop to append coin images from the file directrory
        for i in range(8):
            ani_image = pygame.image.load(os.path.join('images', 'coins', f'tile00{i}.png'))
            self.ani_images.append(ani_image)
        #sets starting image to the third image in the list
        self.image = self.ani_images[2]
        #finds rect based on the image and puts its position on the screen based on the pos argument
        self.rect = self.image.get_rect(topleft = pos)
    
    def update(self, x_shift):
        """
        Args: x_shift
        Returns: none
        Updates animation of the coin and its position
        """
        #updates position based on the world shift (x_shift)
        self.rect.x += x_shift
        #increases the counter for the frame of the enimation
        self.counter += 1
        #if the counter exceeds 26, it would result in ani_images to be out of rage, thus it sets counter back to 0
        if self.counter > 31:
            self.counter = 0
        #for every 4 times the screen updates the portal image updates
        if self.counter%4 == 0:
            self.image = self.ani_images[self.counter//4]