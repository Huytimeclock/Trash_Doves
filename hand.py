# hand.py
import math
import pygame

def calculate_angle(point1, point2):
    angle = math.degrees(math.atan2(point2[1] - point1[1], point2[0] - point1[0]))
    return angle

def rotate_image(image, angle, center):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(center=center).center)
    return rotated_image, new_rect

def redefine_angle(angle, index):
    if index==1:
        if 90 < angle <= 180:
            angle = 90
        if -180 < angle < -90:
            angle = -90
    if index==2:
        if -90 < angle <= 0:
            angle = -90
        if 0 < angle < 90:
            angle = 90
    return angle