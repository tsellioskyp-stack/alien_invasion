import math
import sys
import pygame
from enemy_bullet import EnemyBullet
from enemy import Enemy
from bullet import Bullet
from settings import Settings
from ship import Ship
import time


class AlienInvasion:
    """Overall class to manage game assets and behaviour"""

    def __init__(self):
        """Attributes:  self.screen,
        self.settings,
        self.screen,
        self.ship,
        self.clock,
        self.bg_color
        self.fired_bullets
        self.enemies
        self.motion_counter
        self.fired_enemy_bullets
        self.which_enemy_fired
        self.healthbar
        """

        """Initialize the game, and create game resources"""
        pygame.init()
        self.clock = (
            pygame.time.Clock()
        )  # Create a clock object to control the frame rate
        self.settings = Settings()  # Create an instance of the Settings class
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Alien Invasion")
        self.bg_color = self.settings.bg_color  # Set the background color
        self.ship = Ship(
            self
        )  # Create an instance of the Ship class. The "self" argument is actually
        # the value for the "ai_game" parameter in the Ship class __init__ method, which allows the Ship instance
        # to access attributes of the AlienInvasion instance, such as the screen and settings.
        self.fired_bullets = (
            []
        )  # Create an empty list to store the bullets that have been fired from the ship
        self.enemies = (
            []
        )  # Create an empty list to store the enemy objects that will be created later in the game
        self.fired_enemy_bullets = (
            []
        )  # Create an empty list to store the bullets that have been fired from the enemies
        for _ in range(self.settings.enemies):
            new_enemy = Enemy(self)
            self.enemies.append(new_enemy)
        self.motion_counter = 0
        self.which_enemy_fired = 0
        self.healthbar = pygame.image.load("images/fullhealthbar.png").convert_alpha()
        self.healthbar = pygame.transform.scale(
            self.healthbar,
            (
                math.ceil(
                    (self.settings.screen_width / 1920)
                    * (self.healthbar.get_width())
                    / 20
                ),
                math.ceil(
                    (self.settings.screen_height / 1080)
                    * (self.healthbar.get_height())
                    / 20
                ),
            ),
        )

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()
            # This is a helper method to keep the run_game method clean and organized.
            # It will handle all the event checking for the game, such as keyboard and mouse events.
            self.ship.update()  # Update the ship's position based on the movement flags
            self.enemy_movement()  # Update the position of the enemies based on the motion pattern
            for bullet in self.fired_bullets:
                if bullet.rect.y < 0:
                    self.fired_bullets.remove(
                        bullet
                    )  # Remove the bullet from the list if it has moved
                    # off the top of the screen (y coordinate is less than 0). WIthout it, the list of fired bullets
                    # would continue to grow indefinitely as bullets are fired and move off the screen,
                    # which could eventually lead to performance issues or memory errors.
                    # By removing bullets that are no longer visible on the screen,
                    # we can keep the list of fired bullets manageable and prevent it from consuming unnecessary resources.
                    # If the fired_bullets list is empty, the for loop will simply be skipped
                    # and no bullets will be updated or drawn to the screen.
                else:
                    bullet.update()  # Update the position of each fired bullet
            self.check_collisions()  # Check for collisions between bullets and enemies and between enemy bullets and the ship, and remove them if they collide
            self.check_no_enemies()  # Check if there are no enemies left, and if so, add new enemies to the game
            self.randomly_fire_enemy_bullets()  # Check if any enemies should randomly fire bullets
            self.remove_off_screen_enemy_bullets()  # Remove any enemy bullets that have moved off the bottom of the screen
            self._update_screen()
            # This is another helper method to keep the run_game method clean and organized.
            # It will handle all the screen updating for the game, such as filling the background color,
            # drawing the ship, and flipping the display.
            self.clock.tick(60)  # Limit the frame rate to 60 frames per second

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        max_y = (
            self.screen.get_height() - self.ship.rect.height - 2 * self.ship.rect.height
        )  # Set a maximum y value for the ship to prevent it
        # from moving off the top of the screen (2 * ship height pixels is added as a buffer to prevent the ship from getting
        # too close to the top edge). This is calculated by taking the height of the screen
        # and subtracting the height of the ship, which gives us the maximum y coordinate that the ship can have
        # while still being fully visible on the screen. By using this max_y value in the event handling
        # for the up arrow key, we can ensure that the ship does not move off the top of the screen
        # when the player tries to move it upwards.
        max_x = self.screen.get_width() - self.ship.rect.width
        # The max_x variable is calculated by taking the width of the screen and subtracting the width of the ship.
        # This gives us the maximum x coordinate that the ship can have while still being fully visible on the screen.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    new_bullet = Bullet(self)
                    self.fired_bullets.append(new_bullet)
        keys = pygame.key.get_pressed()
        # The pygame.key.get_pressed() function returns a list of boolean values representing the state of each key on the keyboard.
        # If a key is pressed, the corresponding value in the list will be True, otherwise it will be False.
        # By using this function, we can check the state of multiple keys at once and respond
        # accordingly in our game loop.
        if keys[pygame.K_RIGHT] and self.ship.rect.x < max_x:
            self.ship.moving_right = True
        else:
            self.ship.moving_right = False
        if keys[pygame.K_LEFT] and self.ship.rect.x > 0:
            self.ship.moving_left = True
        else:
            self.ship.moving_left = False
        if keys[pygame.K_UP] and self.ship.rect.y > max_y:
            self.ship.moving_up = True
        else:
            self.ship.moving_up = False
        if (
            keys[pygame.K_DOWN]
            and self.ship.rect.y != self.screen.get_height() - self.ship.rect.height
        ):
            self.ship.moving_down = True
        else:
            self.ship.moving_down = False

            """elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and self.ship.rect.x < max_x:
                    self.ship.moving_right = True
                elif event.key == pygame.K_LEFT and self.ship.rect.x > 0:
                    self.ship.moving_left = True
                elif event.key == pygame.K_UP and self.ship.rect.y > max_y:
                    self.ship.moving_up = True
                elif (
                    event.key == pygame.K_DOWN
                    and self.ship.rect.y
                    != self.screen.get_height() - self.ship.rect.height
                ):
                    self.ship.moving_down = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = False
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = False
                elif event.key == pygame.K_UP:
                    self.ship.moving_up = False
                elif event.key == pygame.K_DOWN:
                    self.ship.moving_down = False
            # The above code checks for keydown events and moves the ship accordingly.
            # It also includes boundary checks to prevent the ship from moving off the screen.
            # The max_y variable is used to ensure that the ship does not move above a certain point on the screen,
            # while the check for the down arrow key ensures that the ship does not move below
            # the bottom edge of the screen."""

    def check_collisions(self):
        """Check for collisions between bullets and enemies, and remove them if they collide."""
        for bullet in self.fired_bullets:
            for enemy in self.enemies:
                if bullet.rect.colliderect(enemy.rect):
                    self.fired_bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    break  # Exit the inner loop after a collision is detected to prevent multiple collisions with the same bullet
        # The check_collisions method iterates through each bullet in the fired_bullets list and checks for collisions with each enemy in the enemies list using the colliderect method.
        # If a collision is detected, the bullet and enemy are removed from their respective lists.
        # The break statement is used to exit the inner loop after a collision is detected to prevent multiple collisions with the same bullet.
        """ Check collisions between enemy bullets and the ship, and remove them if they collide. """
        for bullet in self.fired_enemy_bullets:
            if bullet.rect.colliderect(self.ship.rect):
                self.fired_enemy_bullets.remove(bullet)
                self.ship.health -= 1  # Decrease the ship's health by 1
                print(f"Ship health: {self.ship.health}")
                if self.ship.health <= 0:
                    print("Game Over!")
                    sys.exit()  # Exit the game if the ship's health reaches 0
        match self.ship.health:
            case 3:
                self.healthbar = pygame.image.load(
                    "images/fullhealthbar.png"
                ).convert_alpha()
                self.healthbar = pygame.transform.scale(
                    self.healthbar,
                    (
                        math.ceil(
                            (self.settings.screen_width / 1920)
                            * (self.healthbar.get_width())
                            / 20
                        ),
                        math.ceil(
                            (self.settings.screen_height / 1080)
                            * (self.healthbar.get_height())
                            / 20
                        ),
                    ),
                )
            case 2:
                self.healthbar = pygame.image.load(
                    "images/mediumhealthbar.png"
                ).convert_alpha()
                self.healthbar = pygame.transform.scale(
                    self.healthbar,
                    (
                        math.ceil(
                            (self.settings.screen_width / 1920)
                            * (self.healthbar.get_width())
                            / 20
                        ),
                        math.ceil(
                            (self.settings.screen_height / 1080)
                            * (self.healthbar.get_height())
                            / 20
                        ),
                    ),
                )
            case 1:
                self.healthbar = pygame.image.load(
                    "images/lowhealthbar.png"
                ).convert_alpha()
                self.healthbar = pygame.transform.scale(
                    self.healthbar,
                    (
                        math.ceil(
                            (self.settings.screen_width / 1920)
                            * (self.healthbar.get_width())
                            / 20
                        ),
                        math.ceil(
                            (self.settings.screen_height / 1080)
                            * (self.healthbar.get_height())
                            / 20
                        ),
                    ),
                )

    def enemy_movement(self):
        """Update the position of the enemies based on a motion pattern."""
        for enemy in self.enemies:
            if self.motion_counter <= 4 * self.clock.get_fps():
                enemy.update_y_down()  # Update the position of each enemy in the enemies list
            elif (
                4 * self.clock.get_fps()
                < self.motion_counter
                <= 8 * self.clock.get_fps()
            ):
                enemy.update_x_right()
            elif (
                8 * self.clock.get_fps()
                < self.motion_counter
                <= 12 * self.clock.get_fps()
            ):
                enemy.update_y_up()
            elif (
                12 * self.clock.get_fps()
                < self.motion_counter
                <= 16 * self.clock.get_fps()
            ):
                enemy.update_x_left()
            self.motion_counter += 1
            if self.motion_counter > 16 * self.clock.get_fps():
                self.motion_counter = 0  # Reset the motion counter after completing a full cycle of movements (down, right, up, left)
        # The enemy_movement method updates the position of each enemy in the enemies list based on a motion pattern that cycles through moving down, right, up, and left.
        # The motion_counter variable is used to keep track of how long the enemies have been moving in their current direction, and it is reset after completing a full cycle of movements.

    def check_no_enemies(self):
        """Check if there are no enemies left, and if so, add new enemies to the game."""
        if not self.enemies:
            for _ in range(self.settings.enemies):
                new_enemy = Enemy(self)
                self.enemies.append(new_enemy)
        # The check_no_enemies method checks if the enemies list is empty (i.e., there are no enemies left on the screen).
        # If the list is empty, it creates new enemy objects and adds them to the enemies list using a for loop that iterates based on the number of enemies specified in the settings.

    def randomly_fire_enemy_bullets(self):
        """Check if any enemies should randomly fire bullets."""
        for index, enemy in enumerate(self.enemies):
            if enemy.randomly_fire(len(self.enemies)) == 0:
                new_bullet = EnemyBullet(self)
                self.which_enemy_fired = index
                print(f"Enemy {index} fired a bullet!")
                self.fired_enemy_bullets.append(new_bullet)
        # The randomly_fire_enemy_bullets method iterates through each enemy in the enemies list and calls the randomly_fire method to determine if the enemy should fire a bullet.
        # If the randomly_fire method returns 0, a new EnemyBullet object is created and added to the fired_enemy_bullets list.

    def remove_off_screen_enemy_bullets(self):
        """Remove any enemy bullets that have moved off the bottom of the screen."""
        for bullet in self.fired_enemy_bullets:
            if bullet.rect.y > self.screen.get_height():
                self.fired_enemy_bullets.remove(bullet)
            else:
                bullet.update()  # Update the position of each fired enemy bullet
        # The remove_off_screen_enemy_bullets method iterates through each bullet in the fired_enemy_bullets list and checks if its y coordinate is greater than the height of the screen (i.e., it has moved off the bottom of the screen).
        # If a bullet has moved off the screen, it is removed from the fired_enemy_bullets list to prevent it from consuming unnecessary resources and to keep the list manageable.

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        # self.screen.fill(self.bg_color)
        self.screen.blit(self.settings.bg, (0, 0))
        self.ship.blitme()
        self.screen.blit(
            self.healthbar,
            (
                self.ship.rect.centerx - self.healthbar.get_width() // 2,
                self.ship.rect.centery
                + self.ship.rect.height
                + self.healthbar.get_height() // 2,
            ),
        )  # Draw the health bar image at the top left corner of the screen
        for bullet in self.fired_bullets:
            bullet.blitme()  # Draw each fired bullet to the screen using its blitme method
        for bullet in self.fired_enemy_bullets:
            bullet.blitme()  # Draw each fired enemy bullet to the screen using its blitme method
        for enemy in self.enemies:
            enemy.blitme()  # Draw each enemy in the enemies list to the screen using its blitme method
        pygame.display.flip()


if __name__ == "__main__":
    # Make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()
