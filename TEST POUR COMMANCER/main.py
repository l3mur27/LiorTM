import pygame

# Initialize Pygame
pygame.init()

# Set up display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Draw Red Line Behind Falling Object")

# Define colors
red = (255, 0, 0)
blue = (0, 0, 255)
white = (255, 255, 255)

# Set up the object (a blue rectangle in this case)
rect_width = 100
rect_height = 50
rect_x = (screen_width - rect_width) // 2
rect_y = 0  # Start from the top of the screen
rect_speed_y = 5  # Falling speed

# Main loop
running = True
previous_pos = (rect_x + rect_width // 2, rect_y + rect_height // 2)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the rectangle's position
    rect_y += rect_speed_y

    # Calculate the current position of the rectangle's center
    current_pos = (rect_x + rect_width // 2, rect_y + rect_height // 2)

    # Draw the red line segment
    pygame.draw.line(screen, red, previous_pos, current_pos, 5)

    # Update the previous position to the current position
    previous_pos = current_pos

    # Draw the blue rectangle
    pygame.draw.rect(screen, blue, (rect_x, rect_y, rect_width, rect_height))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate to 60 frames per second
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
