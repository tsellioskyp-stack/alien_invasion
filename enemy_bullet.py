from bullet import Bullet
import pygame
from enemy import Enemy


class EnemyBullet(Bullet):
    """A class to manage bullets fired by the enemies."""

    def __init__(self, ai_game):
        """Create a bullet object at the enemy's current position."""
        super().__init__(ai_game)
        self.color = (255, 0, 0)  # Set the color of the enemy bullet to red
        self.speed = 2 * ai_game.settings.ship_speed
        self.image = pygame.image.load("images/laser.png").convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (ai_game.ship.rect.width, ai_game.ship.rect.height)
        )  # Scale the bullet image to be smaller than the ship, using the ship's rect dimensions as a reference
        self.rect = self.image.get_rect()
        try:  # because the enemy that fired the bullet may have been destroyed by the time the bullet is created, we need to use a try-except block to handle the potential IndexError that could occur when trying to access the rect of an enemy that no longer exists in the enemies list.
            self.rect.y = (
                ai_game.enemies[ai_game.which_enemy_fired].rect.y
                + ai_game.enemies[ai_game.which_enemy_fired].rect.height
            )  # Set the bullet's y coordinate to be just below the enemy's rect, so it appears to be fired from the enemy
            self.rect.centerx = ai_game.enemies[
                ai_game.which_enemy_fired
            ].rect.centerx  # Set the bullet's x coordinate to be at the center of the enemy's rect
        except IndexError:
            # We will initialize this bullet outside of the screen, so it will be removed immediately in the next step of the game loop when we check for off-screen bullets. This is a simple way to handle the case where an enemy fires a bullet but is destroyed before the bullet is created, without causing any errors or issues in the game.
            self.rect.y = (
                ai_game.screen.get_height() + 100
            )  # Set the bullet's y coordinate to be below the bottom of the screen
            self.rect.centerx = 0  # Set the bullet's x coordinate to be at the left edge of the screen (it won't be visible since it's off-screen, but it needs to be initialized to some value)
        """self.rect.y = (
            ai_game.enemies[ai_game.which_enemy_fired].rect.y
            + ai_game.enemies[ai_game.which_enemy_fired].rect.height
        )  # Set the bullet's y coordinate to be just below the enemy's rect, so it appears to be fired from the enemy
        self.rect.centerx = ai_game.enemies[
            ai_game.which_enemy_fired
        ].rect.centerx  # Set the bullet's x coordinate to be at the center of the enemy's rect"""

    def update(self):
        """Move the bullet down the screen."""
        self.rect.y += self.speed
        # Move the bullet down the screen by increasing its y coordinate by a value based on the enemy bullet's speed setting (which is based on the ship's speed setting in settings.py)
