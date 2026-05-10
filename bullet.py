import pygame


class Bullet:
    """A class to manage bullets fired from the ship."""

    def __init__(self, ai_game):
        """Create a bullet object at the ship's current position."""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.image = pygame.image.load("images/laser.png").convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (ai_game.ship.rect.width, ai_game.ship.rect.height)
        )  # Scale the bullet image to be smaller than the ship, using the ship's rect dimensions as a reference
        self.rect = self.image.get_rect()
        # Initialize the bullets position right after being fired, which is at the top center of the ship's rect
        self.rect.y = (
            ai_game.ship.rect.y - ai_game.ship.rect.height
        )  # Set the bullet's y coordinate to be just above the ship's rect, so it appears
        self.rect.centerx = ai_game.ship.rect.centerx
        self.speed = (
            2 * ai_game.settings.ship_speed
        )  # Set the speed of the bullet based on the ship's speed setting in settings.py

    def update(self):
        """Move the bullet up the screen."""
        self.rect.y -= self.settings.ship_speed * 2
        # Move the bullet up the screen by decreasing its y coordinate by a value based on the ship's speed setting (multiplied by 2 to make the bullet move faster than the ship)

    def blitme(self):
        """Draw the bullet to the screen."""
        self.screen.blit(self.image, self.rect)
