import pygame


class Bird:
    def __init__(self, position, jump_speed, gravity, initial_speed):
        self.image = pygame.image.load("bird.png")
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.jump_speed = jump_speed
        self.gravity = gravity
        self.y_speed = initial_speed
        self.on_ground = False
        self.on_top = False

    def jump(self):
            self.y_speed = self.jump_speed

    def update(self):
        self.rect.y += self.y_speed
        self.y_speed += self.gravity

        # Check if bird is on top
        if self.rect.y <= 0:
            self.rect.y = 0
            self.on_top = True
        else:
            self.on_top = False

        # Check if the bird is on the ground
        if self.rect.y >= pygame.display.get_surface().get_height() - self.rect.height:
            self.rect.y = pygame.display.get_surface().get_height() - self.rect.height
            self.y_speed = 0
            self.on_ground = True
        else:
            self.on_ground = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)
