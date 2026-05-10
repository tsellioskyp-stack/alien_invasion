import pygame
from settings import Settings


class Enemy:
    "A class to manage the enemy ships in the game."

    def __init__(self, ai_game):
        """Initialize the enemy and set its starting position."""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # Load the enemy image and get its rect.
        self.image = (pygame.image.load("images/enemy_transparent.png")).convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (ai_game.ship.rect.width, ai_game.ship.rect.height)
        )  # Scaling the image to fit the game surface size according to the original 1080p size, through the settings.py screen size attributes
        self.rect = self.image.get_rect()
        # Initialize the enemy's position at the top of the screen, with a horizontal position
        # that depends on the number of enemies already in the game.
        # This will create a row of enemies across the top of the screen,
        # with each new enemy positioned to the right of the last one.
        self.enemies_remaining = len(ai_game.enemies)
        self.rect.y = self.rect.height
        self.rect.x = self.rect.width + (self.rect.width * 2 * len(ai_game.enemies))
        if self.rect.right > self.screen_rect.right:
            self.rect.y += self.rect.height * (
                (self.rect.right // ai_game.settings.screen_width)
            )
            self.rect.x = self.rect.x % (self.screen_rect.right - self.rect.width)
        """for index, enemy in enumerate(ai_game.enemies):
            if enemy.rect.x > self.screen_rect.right - enemy.rect.width:
                enemy.rect.x = enemy.rect.width + enemy.rect.width * 2
                enemy.rect.y += self.rect.height * 2"""

    def update_y_down(self):
        """Motion pattern for the enemy ships, moving in a circular pattern"""
        self.rect.y += (
            self.settings.enemy_speed_y
        )  # Move the enemy down the screen by increasing its y coordinate by a value based on the enemy
        # speed setting in settings.py

    def update_x_right(self):
        self.rect.x += self.settings.enemy_speed_x

    def update_x_left(self):
        self.rect.x -= self.settings.enemy_speed_x

    def update_y_up(self):
        self.rect.y -= self.settings.enemy_speed_y

    def randomly_fire(self, upper_limit):
        """Randomly determine whether the enemy should fire a bullet."""
        import random

        # A script that randomly returns True or False to determine if the enemy should fire a bullet. Due to the game
        # running at 60 frames per second, this will create a random firing pattern for the enemies that is not too overwhelming for the player.
        return random.randint(
            0, upper_limit * 40
        )  # Randomly return a number between 0 and upper_limit * 40, and if the number is 0, the enemy will fire a bullet. This creates a 1 in 700 chance for each enemy to fire a bullet on each frame of the game.
        # This is to compensate for the fact that as enemies become fewer in number, the chance of each individual enemy firing a bullet
        # should increase to maintain a consistent level of challenge for the player.

    def blitme(self):
        """Draw the enemy to the screen."""
        self.screen.blit(self.image, self.rect)
