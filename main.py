import pygame
import mediapipe as mp
import cv2
import numpy as np
import random
import time
import math
from bird import Bird
from virus import Virus
from bullet import Bullet  # Import the Bullet class
from face import FaceDetector


# Function to calculate the angle between two points
def calculate_angle(point1, point2):
    angle = math.degrees(math.atan2(point2[1] - point1[1], point2[0] - point1[0]))
    return angle


# Function to rotate an image
def rotate_image(image, angle, center):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(center=center).center)
    return rotated_image, new_rect


# initialize pygame
pygame.init()

clock = pygame.time.Clock()

# webcam settings
webcam = cv2.VideoCapture(0)
webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# creating game window
WIDTH, HEIGHT = 1280, 720
window = pygame.display.set_mode((WIDTH, HEIGHT))

# Create an instance of the FaceDetector class
face_detector = FaceDetector()

# background music
pygame.mixer.music.load("bg-music.wav")
pygame.mixer.music.play(-1, 0, 0)
destroying_virus = pygame.mixer.Sound("collect.wav")

# adding main characters and virus
hand_left = pygame.image.load("hand_right.png")
hand_right = pygame.image.load("hand_left.png")
hand_coordinates = [hand_left.get_rect(), hand_right.get_rect()]  # Two hands for each hand

# hand model
hand_model = mp.solutions.hands

# Initialize rotated_image and new_rect for both hands
rotated_image_left, new_rect_left = None, None
rotated_image_right, new_rect_right = None, None

# Create a sprite group for viruses
viruses = pygame.sprite.Group()
# Define a variable to store the time when the last virus was added
last_virus_time = time.time()

# Creating the bird
main_bird = Bird(position=(WIDTH // 2, HEIGHT // 2), jump_speed=-10, gravity=1, initial_speed=0)
# Create default font
default_font = pygame.font.Font(pygame.font.get_default_font(), 36)

# Create a surface for the camera feed
camera_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

# Load background image
background_image = pygame.image.load("background.png").convert()

# Set opacity (alpha) value for the camera feed and background
camera_alpha = 255  # 50% opacity (0-255)
background_alpha = 0  # 20% opacity (0-255)

# Create a sprite group for bullets
bullets = pygame.sprite.Group()
# Timer for bullet creation
bullet_timer = time.time()
bullet_interval = 1  # Time interval to create a new bullet in seconds
bullet_timer2 = time.time()
bullet_interval2 = 1  # Time interval to create a new bullet in seconds

# score variable
SCORE = 0

prev_hand_left = hand_coordinates[0].center
prev_hand_right = hand_coordinates[1].center

# Set the height trigger for bird jump
height_trigger_bird_jump = 5  # Adjust this value based on your preference
# Variables to track center_point over time
center_point_before = None
center_point_time_before = None


# gameloop
working = True
with hand_model.Hands(min_tracking_confidence=0.2, min_detection_confidence=0.2, max_num_hands=2) as hand:
    while working:
        current_time = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            # Check for spacebar press
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                main_bird.jump()

        # Clear the camera surface
        camera_surface.fill((0, 0, 0, 0))

        # ------------------------ Bird Update
        # Update the bird
        main_bird.update()

        # Add new virus after a certain amount of time
        current_time = time.time()
        time_threshold = 2  # Adjust this threshold as needed in seconds
        if current_time - last_virus_time > time_threshold:
            new_virus = Virus(WIDTH, HEIGHT)
            viruses.add(new_virus)
            last_virus_time = current_time
        # Update viruses and check for reset and creation
        viruses.update()
        # ------------------------

        # OPENCV OPERATION
        control, frame = webcam.read()
        # Use the FaceDetector to detect and draw landmarks
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_detector.detect_face(frame_rgb)
        left_eye_landmark, right_eye_landmark = face_detector.draw_face_landmarks(frame, results)

        # Draw lines in the main loop
        if left_eye_landmark and right_eye_landmark:
            # Draw the line between the left and right eye landmarks
            cv2.line(frame, left_eye_landmark, right_eye_landmark, (0, 255, 0), 2)

            # Calculate and draw the center point
            center_point = ((left_eye_landmark[0] + right_eye_landmark[0]) // 2,
                            (left_eye_landmark[1] + right_eye_landmark[1]) // 2)
            cv2.circle(frame, center_point, 5, (0, 0, 255), -1)

            # Check for bird jump trigger
            if center_point_before is not None and center_point_time_before is not None:
                vertical_change = center_point[1] - center_point_before[1]
                time_difference = current_time - center_point_time_before
                #average_speed = vertical_change / time_difference

                # Check if the vertical change within the time threshold exceeds the height trigger
                if(vertical_change<0):
                    if time_difference <= 0.5 and abs(vertical_change) >= height_trigger_bird_jump:
                        main_bird.jump()

            # Update center_point variables
            center_point_before = center_point
            center_point_time_before = current_time



        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hand.process(rgb)

        if result.multi_hand_landmarks:
            for i, handLandmark in enumerate(result.multi_hand_landmarks):
                index_finger_coordinate = handLandmark.landmark[8]
                thumb_finger_coordinate = handLandmark.landmark[5]

                x = int(WIDTH - index_finger_coordinate.x * WIDTH)
                y = int(index_finger_coordinate.y * HEIGHT)

                if result.multi_handedness[i].classification[0].label == "Right":
                    # Right Hand
                    x2 = WIDTH / 2 - 60
                    hand_coordinates[1].center = (x2, main_bird.rect.centery)

                    angle = calculate_angle(
                        (thumb_finger_coordinate.x * WIDTH, thumb_finger_coordinate.y * HEIGHT),
                        (index_finger_coordinate.x * WIDTH, index_finger_coordinate.y * HEIGHT)
                    )

                    if 90 < angle <= 180:
                        angle = 90
                    if -180 < angle < -90:
                        angle = -90

                    rotation_threshold = 5
                    if abs(angle) > rotation_threshold:
                        rotated_image_right, new_rect_right = rotate_image(hand_right, angle,
                                                                           hand_coordinates[1].center)
                        hand_coordinates[1] = new_rect_right
                        if current_time - bullet_timer > bullet_interval:
                            bullet = Bullet("bulletleft.png", hand_coordinates[1].center, angle, 20)
                            bullets.add(bullet)
                            bullet_timer = current_time
                else:
                    # Left Hand
                    x1 = WIDTH / 2 + 60
                    hand_coordinates[0].center = (x1, main_bird.rect.centery)

                    angle2 = calculate_angle(
                        (thumb_finger_coordinate.x * WIDTH, thumb_finger_coordinate.y * HEIGHT),
                        (index_finger_coordinate.x * WIDTH, index_finger_coordinate.y * HEIGHT)
                    )

                    if -90 < angle2 <= 0:
                        angle2 = -90
                    if 0 < angle2 < 90:
                        angle2 = 90
                    rotation_threshold = 5
                    if abs(angle2) > rotation_threshold:
                        rotated_image_left, new_rect_left = rotate_image(hand_left, angle2, hand_coordinates[0].center)
                        hand_coordinates[0] = new_rect_left
                        if current_time - bullet_timer2 > bullet_interval2:
                            bullet = Bullet("bulletleft.png", hand_coordinates[0].center, angle2, 20)
                            bullets.add(bullet)
                            bullet_timer2 = current_time
        else:
            # If no hand is detected, use the previous hand positions
            hand_coordinates[0].center = prev_hand_left
            hand_coordinates[1].center = prev_hand_right

        # Draw camera feed onto the camera surface with 20% opacity
        rgb = np.rot90(rgb)
        frame_surface = pygame.surfarray.make_surface(rgb).convert_alpha()
        frame_surface.set_alpha(camera_alpha)
        camera_surface.blit(frame_surface, (0, 0))

        # Draw everything onto the main window
        window.fill((255, 255, 255))

        # Draw background image onto the main window with 20% opacity
        background_image.set_alpha(background_alpha)
        window.blit(background_image, (0, 0))

        # Draw camera feed on top of the main window
        window.blit(camera_surface, (0, 0))

        # Draw rotated hand images for both hands
        if rotated_image_left is not None:
            window.blit(rotated_image_left, new_rect_left)
        if rotated_image_right is not None:
            window.blit(rotated_image_right, new_rect_right)

        # Draw the bird
        main_bird.draw(window)

        # Draw viruses
        viruses.draw(window)

        # Update viruses and check for reset and creation
        viruses.update()
        # Update bullets
        bullets.update()
        # Draw bullets
        bullets.draw(window)

        # Check for collisions between bullets and viruses
        bullet_hits = pygame.sprite.groupcollide(bullets, viruses, True, True)
        # Increment score for each virus hit
        SCORE += len(bullet_hits)
        # Add new viruses when the score reaches a certain threshold

        # Draw score and line
        TEXT = default_font.render("Score: " + str(SCORE), True, (0, 0, 0))
        TEXT_COORDINATE = TEXT.get_rect()
        TEXT_COORDINATE.topleft = (20, 20)
        window.blit(TEXT, TEXT_COORDINATE)
        pygame.draw.line(window, (0, 255, 0), (0, 121), (1280, 121), 5)

        pygame.display.update()

pygame.quit()
