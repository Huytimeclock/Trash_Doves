import pygame
import sys

# Initialize pygame
pygame.init()

# Load the OTF font
otf_font = "Simon Lovely.otf"  # Replace with the path to your OTF font file
font_size = 72
custom_font = pygame.font.Font(otf_font, font_size)

# Set up the window
WIDTH, HEIGHT = 1280, 720
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Trash Doves")

# Create font
font = pygame.font.Font(None, 36)

# Load background image
background_image = pygame.image.load("background.png").convert()
# Resize the background image to match the screen dimensions
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Load background music
pygame.mixer.music.load("bgm.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Load images
image_list = [pygame.image.load(f"f{i}.png") for i in range(4)]
current_frame = 0
frame_delay = 10  # Adjust this value to control the frame rate

# Transition variables
transition_time = 250  # Time in milliseconds for each transition phase
transition_alpha = 0  # Alpha value for screen fade (0 = fully transparent, 255 = fully opaque)
transition_phase = "FADE_IN"  # Initial transition phase

# Modify the bird size
bird_size = 2  # Double the size
bird_image = pygame.image.load("bird.png")  # Replace with your bird image
bird_image = pygame.transform.scale(bird_image, (bird_image.get_width() * bird_size, bird_image.get_height() * bird_size))
bird_rect = bird_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    window.blit(text_surface, text_rect)

def fancy_button(surface, rect, color, text, font, text_color):
    pygame.draw.rect(surface, color, rect)
    pygame.draw.rect(surface, (255, 255, 255), rect, 5)  # White border
    draw_text(text, font, text_color, rect.centerx, rect.centery)

def menu():
    global current_frame, transition_alpha, transition_phase
    clock = pygame.time.Clock()

    play_button_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 100, 300, 100)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(pygame.mouse.get_pos()):
                    # Start the transition to the game
                    transition_phase = "FADE_OUT"

        # Fill the window with the background color/image
        window.blit(background_image, (0, 0))

        # Render text using the OTF font
        text = custom_font.render("Trash Doves", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        window.blit(text, text_rect)

        # Draw the double-sized bird
        window.blit(bird_image, bird_rect)

        # Draw the fancy play button
        fancy_button(window, play_button_rect, (14, 36, 71), "Play", custom_font, (255, 255, 255))

        # Draw the current frame image above the play button
        current_image = image_list[current_frame]
        image_rect = current_image.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        window.blit(current_image, image_rect)

        # Update the frame counter
        current_frame = (current_frame + 1) % len(image_list)

        # Handle transitions
        if transition_phase == "FADE_IN":
            transition_alpha = max(0, transition_alpha - 255 / (transition_time / frame_delay))
            if transition_alpha == 0:
                transition_phase = None  # Stop fading in
        elif transition_phase == "FADE_OUT":
            transition_alpha = min(255, transition_alpha + 255 / (transition_time / frame_delay))
            if transition_alpha == 255:
                # Start the game or transition to another screen
                # For now, we'll just print a message
                print("Transition to Game!")
                return  # Exit the menu loop

        # Draw the transition overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, int(transition_alpha)))
        window.blit(overlay, (0, 0))

        pygame.display.flip()
        clock.tick(frame_delay)

# Run the menu loop
menu()
