import pygame
import sys

# Initialize pygame
pygame.init()

# Set up the window
WIDTH, HEIGHT = 1280, 720
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Trash Doves")

# Create font
font = pygame.font.Font(None, 36)


# Load background image
background_image = pygame.image.load("background.png").convert()

# Load images
image_list = [pygame.image.load(f"f{i}.png") for i in range(4)]
current_frame = 0
frame_delay = 10  # Adjust this value to control the frame rate

# Transition variables
transition_time = 250  # Time in milliseconds for each transition phase
transition_alpha = 0  # Alpha value for screen fade (0 = fully transparent, 255 = fully opaque)
transition_phase = "FADE_IN"  # Initial transition phase

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    window.blit(text_surface, text_rect)

def menu():
    global current_frame, transition_alpha, transition_phase
    clock = pygame.time.Clock()

    play_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)

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

        # Draw the game name
        draw_text("Trash Doves", font, (255, 255, 255), WIDTH // 2, HEIGHT // 4)

        # Draw the play button
        pygame.draw.rect(window, (7, 94, 166), play_button_rect)  # Green play button
        draw_text("Play", font, (255, 255, 255), WIDTH // 2, HEIGHT // 2 + 25)

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