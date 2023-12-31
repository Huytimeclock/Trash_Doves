import pygame
import random
import math

class Virus(pygame.sprite.Sprite):
    def __init__(self, width, height, scale_factor=4.0):
        super().__init__()
        # Initialize virus attributes
        original_frames = [pygame.image.load(f"BatMove{i}.png") for i in range(1, 7)]

        # Scale each frame based on the provided scale_factor
        self.frames = [pygame.transform.scale(frame, (int(frame.get_width() * scale_factor),
                                                     int(frame.get_height() * scale_factor)))
                       for frame in original_frames]

        self.image = self.frames[0]  # Start with the first frame

        self.rect = self.image.get_rect()

        self.width = width
        self.height = height
        self.speed = random.randint(3, 5)  # Random speed
        self.direction = random.choice(['left', 'right'])  # Added direction attribute
        self.frame_index = 0  # Index to keep track of the current frame
        self.frame_counter = 0  # Counter to control frame switching
        self.randomize_position()
        self.define_angle()
        self.destroyed = False  # Added destroyed attribute
        self.lose_flag = False  # Added lose_flag attribute

    def randomize_position(self):
        # Randomize virus position and set direction
        if self.direction == 'left':
            self.rect.x = -self.rect.width
        else:
            self.rect.x = 1080
        self.rect.y = random.randint(0, 720 - self.rect.height)
        # Mark self.positionY based on self.rect.y
        if 0 <= self.rect.y <= 240:
            self.positionY = "high"
        elif 240 < self.rect.y <= 480:
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
                self.image = pygame.transform.flip(self.frames[self.frame_index], True, False)
            else:
                delta_x = -self.speed * math.cos(math.radians(self.angle))
                self.image = self.frames[self.frame_index]
            delta_y = self.speed * math.sin(math.radians(self.angle))
            self.rect.x += delta_x
            self.rect.y += delta_y

            # Check if it's time to switch to the next frame
            self.frame_counter += 1
            if self.frame_counter >= 5:  # Adjust this value for the desired animation speed
                self.frame_index = (self.frame_index + 1) % len(self.frames)
                if self.direction == 'left':
                    self.image = pygame.transform.flip(self.frames[self.frame_index], True, False)
                else:
                    self.image = self.frames[self.frame_index]
                self.frame_counter = 0

            # Check if it's time to disappear
            if self.direction == 'left':
                if self.rect.x >= 590:
                    self.destroyed = True  # Set destroyed to True when the virus reaches the center
                    self.lose_flag = True  # Set lose_flag to True when the virus is destroyed

            else:
                if self.rect.x <= 630:
                    self.destroyed = True  # Set destroyed to True when the virus reaches the center
                    self.lose_flag = True  # Set lose_flag to True when the virus is destroyed

