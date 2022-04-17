import pygame
import sys
import os

from spritesheet import Spritesheet

############## VARIABLES ###############
#

worldx = 960
worldy = 720
fps = 40  # frame rate
ani = 4   # animation cycles
main = True

BLUE = (25, 25, 200)
BLACK = (23, 23, 23)
WHITE = (254, 254, 254)
ALPHA = (0, 255, 0)

############### OBJECTS ##################

# put Python classes and functions here

class Player(pygame.sprite.Sprite):
    """
    Spawn a player
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.LEFT_KEY, self.RIGHT_KEY, self.FACING_LEFT = False, False, False



############### INITIAL SETUP #############

clock = pygame.time.Clock()
pygame.init()
world = pygame.display.set_mode([worldx, worldy])
backdrop = pygame.image.load(os.path.join('images', 'mountain.png'))
backdropbox = world.get_rect()


################ MAIN ####################

while main:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            try:
                sys.exit()
            finally:
                main = False

        if event.type == pygame.KEYDOWN:
            if event.key == ord('q'):
                pygame.quit()
            try:
                sys.exit()
            finally:
                main = False
    world.blit(backdrop, backdropbox)
    pygame.display.flip()
    clock.tick(fps)