import pygame
import random
import math

class Virus(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        # Initialize virus attributes
        self.image = pygame.image.load("virus.png")
        self.rect = self.image.get_rect()
        self.width = width
        self.height = height
        self.speed = random.randint(3, 5)  # Random speed
        self.direction = random.choice(['left', 'right'])  # Added direction attribute
        self.randomize_position()
        self.define_angle()
        self.destroyed = False  # Added destroyed attribute

    def randomize_position(self):
        # Randomize virus position and set direction
        if self.direction == 'left':
            self.rect.x = -self.rect.width
        else:
            self.rect.x = self.width
        self.rect.y = random.randint(0, self.height - self.rect.height)
        # Mark self.positionY based on self.rect.y
        if 0 <= self.rect.y <= self.height / 3:
            self.positionY = "high"
        elif self.height / 3 < self.rect.y <= 2 * self.height / 3:
            self.positionY = "center"
        else:
            self.positionY = "low"

    def define_angle(self):
        if self.positionY == "high":
            self.angle = random.randint(25, 35)
        elif self.positionY == "center":
            self.angle = random.randint(-25, 25)
        elif self.positionY == "low":
            self.angle = random.randint(-35, -25)  # Corrected the range for "high"


    def update(self):
        # Move the virus based on its direction
        if not self.destroyed:
            if self.direction == 'left':
                delta_x = self.speed * math.cos(math.radians(self.angle))
            else:
                delta_x = -self.speed * math.cos(math.radians(self.angle))
            delta_y = self.speed * math.sin(math.radians(self.angle))
            self.rect.x += delta_x
            self.rect.y += delta_y


            # Check if it's time to disappear
            if self.direction == 'left':
                if self.rect.x >= self.width / 2:
                    self.destroyed = True  # Set destroyed to True when the virus reaches the center
                    self.kill()  # Remove the virus from the sprite group
                    self.game_over = True  # Set game_over to True when the virus is destroyed
                    self.gameover()
                    print("lose")
            else:
                if self.rect.x <= self.width / 2:
                    self.destroyed = True  # Set destroyed to True when the virus reaches the center
                    self.kill()  # Remove the virus from the sprite group
                    self.game_over = True  # Set game_over to True when the virus is destroyed
                    self.gameover()
                    print("lose")

    def gameover(self):
        # Add your game over logic here
        pass
