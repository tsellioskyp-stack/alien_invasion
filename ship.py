import pygame
import math
from settings import Settings


class Ship:
    """A class to manage the ship."""

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.health = 3  # Initialize the ship's health to 3

        # Load the ship image and get its rect.
        self.image = (
            pygame.image.load("images/player_transparent.png")
        ).convert_alpha()
        self.image = pygame.transform.scale(
            self.image,
            (
                math.ceil(
                    (self.settings.screen_width / 1920) * (self.image.get_width()) / 5
                ),
                math.ceil(
                    (self.settings.screen_height / 1080) * (self.image.get_height()) / 5
                ),
            ),
        )  # SCaling the image to fit the game surface size according to the original 1080p size, through the settings.py screen size attributes
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Update the ship's position based on the movement flag."""
        if self.moving_right:
            self.rect.x += 1 * self.settings.ship_speed
        if self.moving_left:
            self.rect.x -= 1 * self.settings.ship_speed
        if self.moving_up:
            self.rect.y -= 1 * self.settings.ship_speed
        if self.moving_down:
            self.rect.y += 1 * self.settings.ship_speed
