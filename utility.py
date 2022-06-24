"""
ICS3U
Raihaan Sandhu
This file is to store important values that are used across a variety of files
"""

import pygame
screen = pygame.display.set_mode((960, 480))
fps = 40  # frame rate
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)