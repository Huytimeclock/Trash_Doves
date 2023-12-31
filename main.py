import pygame
import mediapipe as mp
import cv2
import numpy as np
import random
import time
import pygame.gfxdraw
import math
from bird import Bird
from virus import Virus
from bullet import Bullet  # Import the Bullet class
from face import FaceDetector
from hand import calculate_angle, rotate_image, redefine_angle  # Import hand-related functions
from pipe import Pipe

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
deathsound=pygame.mixer.Sound("death.wav")

# adding main characters and virus
hand_left = pygame.image.load("hand_right.png")
hand_right = pygame.image.load("hand_left.png")
hand_coordinates = [hand_left.get_rect(), hand_right.get_rect()]  # Two hands for each hand

# hand model
hand_model = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Initialize rotated_image and new_rect for both hands
rotated_image_left, new_rect_left = None, None
rotated_image_right, new_rect_right = None, None

# Create a sprite group for viruses
viruses = pygame.sprite.Group()
# Define a variable to store the time when the last virus was added
last_virus_time = time.time()
last_pipe_time=time.time()
# Creating the bird
main_bird = Bird(position=(WIDTH // 2, HEIGHT // 2), jump_speed=-10, gravity=1, initial_speed=0)

# Create default font
default_font = pygame.font.Font(pygame.font.get_default_font(), 36)
# Load a different font for prettier text
button_font = pygame.font.Font("Poppins-Light.ttf", 30)


# Create a surface for the camera feed
camera_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

# Load background image
background_image = pygame.image.load("background.png").convert()

# Set opacity (alpha) value for the camera feed and background
camera_alpha = 255  # 50% opacity (0-255)
background_alpha = 0  # 20% opacity (0-255)

# Create a sprite group for bullets
bullets = pygame.sprite.Group()
bullet_timer = time.time()
bullet_interval = 1  # Time interval to create a new bullet in seconds
bullet_timer2 = time.time()
bullet_interval2 = 1  # Time interval to create a new bullet in seconds

# score variable
SCORE = 0

prev_hand_left = hand_coordinates[0].center
prev_hand_right = hand_coordinates[1].center
rotation_threshold = 5  # check hand angle

# Set the height trigger for bird jump
height_trigger_bird_jump = 5
center_point_before = None
center_point_time_before = None

pipes = pygame.sprite.Group()

# Initialize a Pipe instance
pipe_speed = 8  # Adjust speed as needed
max_top_y_pipe=-950
min_top_y_pipe=-1350

# Define a game over flag
game_over = False
# Initialize the game over screen variables
game_over_bg = None
game_over_sound_played = False
game_over_start_time = None
# gameloop-------------------------------------------------------------------------------------------------------------
working = True
with hand_model.Hands(min_tracking_confidence=0.2, min_detection_confidence=0.2, max_num_hands=2) as hand:
    while working and not game_over:
        current_time = time.time()
        virus_spawn_time = 2  # Virus spawn
        pipe_spawn_time = 8
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False

        # Clear the window
        window.fill((255, 255, 255))

        # Clear the camera surface
        camera_surface.fill((0, 0, 0, 0))

        if current_time - last_virus_time > virus_spawn_time:
            new_virus = Virus(WIDTH, HEIGHT)
            viruses.add(new_virus)
            last_virus_time = current_time

        # Create new pipes
        pipe_top_y_value=random.randint(min_top_y_pipe,max_top_y_pipe)
        lr_value=random.randint(1,2)
        if current_time - last_pipe_time > pipe_spawn_time:
            new_pipe = Pipe(WIDTH, HEIGHT, pipe_speed,1,pipe_top_y_value,lr_value)
            pipes.add(new_pipe)
            new_pipe = Pipe(WIDTH, HEIGHT, pipe_speed, 2,pipe_top_y_value+1000,lr_value)
            pipes.add(new_pipe)
            print(pipe_top_y_value)
            last_pipe_time = current_time

        main_bird.update()
        viruses.update()
        pipes.update()




        # ------------------------ OPENCV OPERATION
        control, frame = webcam.read()
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faceresult = face_detector.detect_face(frame_rgb)
        handresult = hand.process(frame_rgb)
        x2 = WIDTH / 2 - 60
        x1 = WIDTH / 2 + 60
        if handresult.multi_hand_landmarks:
            for i, handLandmark in enumerate(handresult.multi_hand_landmarks):
                for j in range(len(handLandmark.landmark)):
                    # Extract the coordinates of the current landmark
                    landmark_coordinate = handLandmark.landmark[j]

                    # Calculate the pixel coordinates
                    x3 = int(landmark_coordinate.x * WIDTH)
                    y3 = int(landmark_coordinate.y * HEIGHT)
                    print(x3, " ", y3)

                    # Draw a circle for each landmark
                    cv2.circle(frame, (x3, y3), 5, (0, 255, 0), -1)

                index_finger_coordinate = handLandmark.landmark[8]
                thumb_finger_coordinate = handLandmark.landmark[5]

                x = int(WIDTH - index_finger_coordinate.x * WIDTH)
                y = int(index_finger_coordinate.y * HEIGHT)

                if handresult.multi_handedness[i].classification[0].label == "Right":
                    # Right Hand

                    hand_coordinates[0].center = (x1, main_bird.rect.centery)  # prev_hand_left
                    hand_coordinates[1].center = (x2, main_bird.rect.centery)

                    angle = redefine_angle(calculate_angle(
                        (thumb_finger_coordinate.x * WIDTH, thumb_finger_coordinate.y * HEIGHT),
                        (index_finger_coordinate.x * WIDTH, index_finger_coordinate.y * HEIGHT)
                    ), 1)

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
                    hand_coordinates[1].center = (x2, main_bird.rect.centery)  # prev_hand_right
                    hand_coordinates[0].center = (x1, main_bird.rect.centery)

                    angle2 = redefine_angle(calculate_angle(
                        (thumb_finger_coordinate.x * WIDTH, thumb_finger_coordinate.y * HEIGHT),
                        (index_finger_coordinate.x * WIDTH, index_finger_coordinate.y * HEIGHT)
                    ), 2)

                    if abs(angle2) > rotation_threshold:
                        rotated_image_left, new_rect_left = rotate_image(hand_left, angle2, hand_coordinates[0].center)
                        hand_coordinates[0] = new_rect_left
                        if current_time - bullet_timer2 > bullet_interval2:
                            bullet = Bullet("bulletleft.png", hand_coordinates[0].center, angle2, 20)
                            bullets.add(bullet)
                            bullet_timer2 = current_time

        else:
            # If no hand is detected, use the previous hand positions
            hand_coordinates[0].center = (x1, main_bird.rect.centery)  # prev_hand_left
            hand_coordinates[1].center = (x2, main_bird.rect.centery)  # prev_hand_right

        left_eye_landmark, right_eye_landmark = face_detector.draw_face_landmarks(frame_rgb,
                                                                                  faceresult)  # return point of left_eye and righteye
        if left_eye_landmark and right_eye_landmark:
            cv2.line(frame, left_eye_landmark, right_eye_landmark, (0, 255, 0), 2)
            center_point = ((left_eye_landmark[0] + right_eye_landmark[0]) // 2,
                            (left_eye_landmark[1] + right_eye_landmark[1]) // 2)
            cv2.circle(frame, center_point, 5, (0, 0, 255), -1)

            # Check for bird jump trigger
            if center_point_before is not None and center_point_time_before is not None:
                vertical_change = center_point[1] - center_point_before[1]
                time_difference = current_time - center_point_time_before
                if (vertical_change < 0):
                    if time_difference <= 0.5 and abs(vertical_change) >= height_trigger_bird_jump:
                        main_bird.jump()

            # Update center_point variables
            center_point_before = center_point
            center_point_time_before = current_time

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # dontknowwhatthis is
        rgb = np.rot90(rgb)
        frame_surface = pygame.surfarray.make_surface(rgb).convert_alpha()
        frame_surface.set_alpha(camera_alpha)
        camera_surface.blit(frame_surface, (0, 0))

        # Draw camera feed on top of the main window
        window.blit(camera_surface, (0, 0))

        # Draw rotated hand images for both hands
        if rotated_image_left is not None:
            window.blit(rotated_image_left, new_rect_left)
        if rotated_image_right is not None:
            window.blit(rotated_image_right, new_rect_right)

        main_bird.draw(window)        # Draw the bird
        viruses.draw(window)        # Draw viruses
        pipes.draw(window)        # Draw pipes
        bullets.draw(window)  # Draw bullets

        viruses.update()        # Update viruses and check for reset and creation
        bullets.update()        # Update bullets

        # Check for collisions between bullets and viruses
        bullet_hits = pygame.sprite.groupcollide(bullets, viruses, True, True)
        SCORE += len(bullet_hits)

        # Check for collisions between bird and pipes
        if pygame.sprite.spritecollide(main_bird, pipes, False):
            game_over = True

        # Check for collisions between bird and viruses
        if pygame.sprite.spritecollide(main_bird, viruses, False):
            game_over = True

        # Draw score and line
        TEXT = default_font.render("Score: " + str(SCORE), True, (0, 0, 0))
        TEXT_COORDINATE = TEXT.get_rect()
        TEXT_COORDINATE.topleft = (20, 20)
        window.blit(TEXT, TEXT_COORDINATE)
        pygame.draw.line(window, (0, 255, 0), (0, 121), (1280, 121), 5)
        pygame.display.update()

    # Game over logic
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = False
                working = False  # Added to handle quitting the game correctly

        # Play the game over sound only once
        if not game_over_sound_played:
            deathsound.play()
            game_over_sound_played = True
            game_over_start_time = current_time

        # Drawing Rectangle
        pygame.draw.rect(window, (255,255,255), pygame.Rect(WIDTH // 3 * 2-150, HEIGHT // 2-150, 300, 400))

        # Display game over text with a different font
        game_over_text = button_font.render("Game Over", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=(WIDTH // 3 * 2, HEIGHT // 2 - 50))
        window.blit(game_over_text, text_rect)

        # Display the score
        score_text = button_font.render("Score: " + str(SCORE), True, (0, 0, 0))
        score_rect = score_text.get_rect(center=(WIDTH // 3 * 2, HEIGHT // 2))
        window.blit(score_text, score_rect)

        # Display buttons with anti-aliased shapes
        button_color = (100, 100, 100)
        play_again_rect = pygame.Rect(WIDTH // 3 * 2 - 75, HEIGHT // 2 + 25, 150, 40)
        pygame.gfxdraw.aapolygon(window, [(play_again_rect.left, play_again_rect.top),
                                          (play_again_rect.right, play_again_rect.top),
                                          (play_again_rect.right, play_again_rect.bottom),
                                          (play_again_rect.left, play_again_rect.bottom)], button_color)
        pygame.gfxdraw.filled_polygon(window, [(play_again_rect.left, play_again_rect.top),
                                               (play_again_rect.right, play_again_rect.top),
                                               (play_again_rect.right, play_again_rect.bottom),
                                               (play_again_rect.left, play_again_rect.bottom)], button_color)
        play_again_text = button_font.render("Play Again", True, (255, 255, 255))
        text_rect = play_again_text.get_rect(center=play_again_rect.center)
        window.blit(play_again_text, text_rect)

        back_to_menu_rect = pygame.Rect(WIDTH // 3 * 2 - 75, HEIGHT // 2 + 75, 150, 40)
        pygame.gfxdraw.aapolygon(window, [(back_to_menu_rect.left, back_to_menu_rect.top),
                                          (back_to_menu_rect.right, back_to_menu_rect.top),
                                          (back_to_menu_rect.right, back_to_menu_rect.bottom),
                                          (back_to_menu_rect.left, back_to_menu_rect.bottom)], button_color)
        pygame.gfxdraw.filled_polygon(window, [(back_to_menu_rect.left, back_to_menu_rect.top),
                                               (back_to_menu_rect.right, back_to_menu_rect.top),
                                               (back_to_menu_rect.right, back_to_menu_rect.bottom),
                                               (back_to_menu_rect.left, back_to_menu_rect.bottom)], button_color)
        back_to_menu_text = button_font.render("Back to Menu", True, (255, 255, 255))
        text_rect = back_to_menu_text.get_rect(center=back_to_menu_rect.center)
        window.blit(back_to_menu_text, text_rect)

        quit_rect = pygame.Rect(WIDTH // 3 * 2 - 75, HEIGHT // 2 + 125, 150, 40)
        pygame.gfxdraw.aapolygon(window, [(quit_rect.left, quit_rect.top),
                                          (quit_rect.right, quit_rect.top),
                                          (quit_rect.right, quit_rect.bottom),
                                          (quit_rect.left, quit_rect.bottom)], button_color)
        pygame.gfxdraw.filled_polygon(window, [(quit_rect.left, quit_rect.top),
                                               (quit_rect.right, quit_rect.top),
                                               (quit_rect.right, quit_rect.bottom),
                                               (quit_rect.left, quit_rect.bottom)], button_color)
        quit_text = button_font.render("Quit", True, (255, 255, 255))
        text_rect = quit_text.get_rect(center=quit_rect.center)
        window.blit(quit_text, text_rect)

        pygame.display.update()

        # Check for button clicks
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        if play_again_rect.collidepoint(mouse_x, mouse_y) and mouse_click[0] == 1:
            # Reset game state
            main_bird.rect.center = (WIDTH // 2, HEIGHT // 2)
            main_bird.y_speed = 0
            viruses.empty()
            bullets.empty()
            SCORE = 0
            game_over = False
            game_over_sound_played = False
            game_over_start_time = None

        elif back_to_menu_rect.collidepoint(mouse_x, mouse_y) and mouse_click[0] == 1:
            pass  # Implement logic for going back to the menu

        elif quit_rect.collidepoint(mouse_x, mouse_y) and mouse_click[0] == 1:
            game_over = False
            working = False

pygame.quit()
