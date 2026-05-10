import pygame
import random


class Settings:
    """A class to store all settings for Alien Invasion"""

    def __init__(self):
        """Initialize the game's settings"""
        # Screen settings
        self.screen_width = 1280
        self.screen_height = 720
        self.bg_color = (0, 0, 0)  # Set the background color to black (RGB value)
        self.bg = pygame.transform.scale(
            pygame.image.load("images/starfield.png"),
            (self.screen_width, self.screen_height),
        )
        self.ship_speed = 5
        self.enemies = 20  # Randomly generate a number of enemies between 20 and 30 for each new game
        self.enemy_speed_y = 1  # integer
        self.enemy_speed_x = 1
