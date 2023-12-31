import pygame

class Bird:
    def __init__(self, position, jump_speed, gravity, initial_speed, scale_factor=2.0):
        # Load bird animation frames
        self.frames = [
            pygame.image.load("yellowbird-downflap.png").convert_alpha(),
            pygame.image.load("yellowbird-midflap.png").convert_alpha(),
            pygame.image.load("yellowbird-upflap.png").convert_alpha()
        ]
        self.frame_index = 0  # Index of the current frame
        self.image = self.frames[self.frame_index]

        # Scale factor to adjust the size of the bird
        self.scale_factor = scale_factor

        # Adjust the width and height based on the scale factor
        self.rect = self.image.get_rect()
        self.rect.width = int(self.rect.width * scale_factor)
        self.rect.height = int(self.rect.height * scale_factor)

        self.rect.center = position
        self.jump_speed = jump_speed
        self.gravity = gravity
        self.y_speed = initial_speed
        self.on_ground = False
        self.on_top = False
        self.animation_timer = pygame.time.get_ticks()  # Timer to control animation

    def jump(self):
        self.y_speed = self.jump_speed

    def update(self):
        # Update animation frame every 100 milliseconds
        if pygame.time.get_ticks() - self.animation_timer > 100:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = pygame.transform.scale(self.frames[self.frame_index], (self.rect.width, self.rect.height))
            self.animation_timer = pygame.time.get_ticks()

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
