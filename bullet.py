import pygame
import math

class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, position, angle, speed):
        super().__init__()
        original_image = pygame.image.load(image)
        self.image = pygame.transform.rotate(original_image, angle)  # Rotate the original image
        self.rect = self.image.get_rect(center=position)
        self.angle = angle
        self.speed = speed
        self.dx = self.speed * math.cos(math.radians(self.angle))
        self.dy = self.speed * math.sin(math.radians(self.angle))

    def update(self):
        self.rect.x -= self.dx
        self.rect.y += self.dy

        # Remove the bullet when it goes off-screen
        if self.rect.x > 1280 or self.rect.y > 720 or self.rect.y < 0:
            self.kill()
