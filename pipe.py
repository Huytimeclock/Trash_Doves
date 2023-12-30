import pygame
import random


class Pipe(pygame.sprite.Sprite):
    def __init__(self, width, height, speed, index, y,lr):
        super().__init__()

        self.pipe_up = pygame.image.load("pipe_up.png").convert_alpha()
        self.pipe_down = pygame.image.load("pipe_down.png").convert_alpha()

        if index == 1:
            self.image = self.pipe_up
        elif index == 2:
            self.image = self.pipe_down

        self.rect = self.image.get_rect()

        self.width = width
        self.height = height
        self.speed = speed

        if(lr==1):
            self.direction = 'left'
        if(lr==2):
            self.direction = 'right'


        if self.direction == 'left':
            self.rect.x = self.width
        else:
            self.rect.x = -self.rect.width


        self.rect.y = self.rect.height + y

    def update(self):
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed


