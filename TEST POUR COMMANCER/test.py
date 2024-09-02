import sys
import pygame
import math
import tkinter as tk

pygame.init()

# Parameters of the display
width = 960
height = 540

angle = 0.0  # Initialize as float
speed = 0.0  # Initialize as float
x_start = 0.0
y_start = 0.0
gravity = 9.81
land_pos = []

# Colors
red = (255, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)
gray = (50, 50, 50)
dark_gray = (169, 169, 169)

# Button state (slider state)
button_state = {False: gray, True: "lightgray"}

# Initialize Fonts
pygame.font.init()
FONT = pygame.font.Font(None, 24)

# Background
gif_path = 'background/background_start.gif'
gif = pygame.image.load(gif_path)

main_background_day_path = 'background/1.png'
main_background_day = pygame.image.load(main_background_day_path)

# Sprite images
red_ball = pygame.image.load("character/red_ball_2.png")
ball_size = (10, 10)  # Set the size of the ball (width, height)
red_ball = pygame.transform.scale(red_ball, ball_size)
ball = red_ball.get_rect()
ball.center = (width // 2, height // 2)

class Slider:
    def __init__(self, pos: tuple, size: tuple, initial_val: float, min_val: int, max_val: int) -> None:
        self.pos = pos
        self.size = size
        self.hovered = False
        self.grabbed = False

        self.slider_left_pos = self.pos[0] - (size[0] // 2)
        self.slider_right_pos = self.pos[0] + (size[0] // 2)
        self.slider_top_pos = self.pos[1] - (size[1] // 2)

        self.min = min_val
        self.max = max_val
        self.initial_val = (self.slider_right_pos - self.slider_left_pos) * initial_val  # Initial value as percentage

        self.container_rect = pygame.Rect(self.slider_left_pos, self.slider_top_pos, self.size[0], self.size[1])
        self.button_rect = pygame.Rect(self.slider_left_pos + self.initial_val - 5, self.slider_top_pos, 10, self.size[1])

    def move_slider(self, mouse_pos):
        pos = mouse_pos[0]
        if pos < self.slider_left_pos:
            pos = self.slider_left_pos
        elif pos > self.slider_right_pos:
            pos = self.slider_right_pos
        self.button_rect.centerx = pos

    def hover(self, mouse_pos):
        if self.button_rect.collidepoint(mouse_pos):
            self.hovered = True
        else:
            self.hovered = False

    def grab(self, mouse_pos):
        if self.button_rect.collidepoint(mouse_pos):
            self.grabbed = True

    def release(self):
        self.grabbed = False

    def render(self, screen):
        pygame.draw.rect(screen, dark_gray, self.container_rect)
        pygame.draw.rect(screen, button_state[self.hovered], self.button_rect)

    def get_value(self):
        val_range = self.slider_right_pos - self.slider_left_pos - 1
        button_val = self.button_rect.centerx - self.slider_left_pos
        return (button_val / val_range) * (self.max - self.min) + self.min

    def update_distance_and_time(self, screen):
        # Get current slider value
        current_value = self.get_value()

        # Calculate distance and time
        distance = current_value
        angle_rad = math.radians(angle)
        speed_x = speed * math.cos(angle_rad)
        time_to_reach_x = distance / speed_x if speed_x != 0 else float('inf')

        # Render distance and time
        distance_text = FONT.render(f"Distance: {distance:.2f} m", True, white)
        time_text = FONT.render(f"Time: {time_to_reach_x:.2f} s", True, white)

        screen.blit(distance_text, (self.pos[0] - distance_text.get_width() // 2, self.slider_top_pos - 70))
        screen.blit(time_text, (self.pos[0] - time_text.get_width() // 2, self.slider_top_pos - 50))



# Class for the projectile
class Projectile(pygame.sprite.Sprite):
    def __init__(self, ball_image, width, height, angle, speed):
        super().__init__()
        self.image = ball_image
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height // 2)
        self.start_time = pygame.time.get_ticks() / 1000

        ppx_par_metre = 25

        self.pos = [ball_size[1] + x_start * ppx_par_metre, (height - y_start * ppx_par_metre) - ball_size[1]]
        self.vit = [speed * math.cos(math.radians(angle)) * ppx_par_metre, -(speed) * math.sin(math.radians(angle)) * ppx_par_metre]
        self.acc = [0, gravity * ppx_par_metre]

        self.positions = []

    def update(self):
        dt = 1 / 60  # deltaT is equal to 1 FPS
        self.movement(dt)

        # Update the ball's position
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def movement(self, dt):
        # Update the velocity
        self.vit[0] += self.acc[0] * dt  # Update velocity in X
        self.vit[1] += self.acc[1] * dt  # Update velocity in Y

        # Update the position
        self.pos[0] += self.vit[0] * dt  # Update position in X
        self.pos[1] += self.vit[1] * dt  # Update position in Y

        # Append(adds digits in matrice)
        self.positions.append((self.pos[0] + (ball_size[1] / 2), self.pos[1] + (ball_size[1] / 2)))

        if self.pos[1] >= height - ball_size[1]:
            self.pos[1] = height - ball_size[1]
            self.vit = [0, 0]

    def calculate_landing_position(self):
        # Calculate time of flight
        time_of_flight = (2 * speed * math.sin(math.radians(angle))) / gravity

        # Calculate horizontal distance
        horizontal_distance = x_start + speed * math.cos(math.radians(angle)) * time_of_flight
        land_pos.append(horizontal_distance)


    def time_at_x_position(self, x_pos):
        # Horizontal velocity
        v_x = speed * math.cos(math.radians(angle))

        # Calculate time at x position
        time_at_x = (x_pos - x_start) / v_x if v_x != 0 else float('inf')  # Prevent division by zero

        return time_at_x

        print(f"The projectile will land at x: {horizontal_distance:.3f} meters, y: 0.0 meters, and the fly time is: {time_of_flight:.3f} seconds")

    def draw_a_red_line(self, screen):
        if len(self.positions) > 1:
            for i in range(len(self.positions) - 1):
                pygame.draw.line(screen, red, self.positions[i], self.positions[i + 1], 2)

# Create a group for the sprite
all_sprites = pygame.sprite.Group()

# Pygame variables
fps = 60
clock = pygame.time.Clock()

# Menu state(Open or Closed)
menu_active = False
menu_rects = (None, None)

def draw_menu(screen):
    global menu_rects
    # Menu size
    menu_width = 300
    menu_height = 200
    menu_x = (width - menu_width) // 2
    menu_y = (height - menu_height) // 2

    # Draw menu background
    pygame.draw.rect(screen, gray, (menu_x, menu_y, menu_width, menu_height))
    
    # Button dimensions
    button_width = 100
    button_height = 50
    button_x = menu_x + (menu_width - button_width) // 2

    # Exit button
    exit_button_y = menu_y + (menu_height - button_height) // 2 - 30  # Positioned slightly higher
    pygame.draw.rect(screen, black, (button_x, exit_button_y, button_width, button_height))
    
    # Exit text
    font = pygame.font.Font(None, 36)
    exit_text = font.render("Exit", True, white)
    exit_rect = exit_text.get_rect(center=(button_x + button_width // 2, exit_button_y + button_height // 2))
    screen.blit(exit_text, exit_rect)

    # Restart button
    restart_button_y = menu_y + (menu_height - button_height) // 2 + 30  # Positioned slightly lower
    pygame.draw.rect(screen, black, (button_x, restart_button_y, button_width, button_height))

    # Restart text
    restart_text = font.render("Restart", True, white)
    restart_rect = restart_text.get_rect(center=(button_x + button_width // 2, restart_button_y + button_height // 2))
    screen.blit(restart_text, restart_rect)

    # Update menu_rects (Buttons)
    menu_rects = (exit_rect, restart_rect)

def start_simulation():
    global angle, speed, x_start, y_start
    try:
        angle = float(angle_entry.get())
        speed = float(speed_entry.get())
        x_start = float(x_start_entry.get())
        y_start = float(y_start_entry.get())
        error_label.config(text="")
        root.destroy()  # Close the Tkinter menu
        pygame.display.quit()  # closes the previous pygame display
        main_window()
    except ValueError:
        error_label.config(text="Invalid input. Please enter numeric values.")

def open_menu():
    global root, angle_entry, speed_entry, x_start_entry, y_start_entry, error_label

    root = tk.Tk()
    root.title("Projectile Simulation Menu")

    tk.Label(root, text="Enter the initial conditions for the projectile:").pack()

    tk.Label(root, text="Angle (degrees)").pack()
    angle_entry = tk.Entry(root)
    angle_entry.insert(0, "0.0")
    angle_entry.pack()

    tk.Label(root, text="Speed (m/s)").pack()
    speed_entry = tk.Entry(root)
    speed_entry.insert(0, "0.0")
    speed_entry.pack()

    tk.Label(root, text="Starting position axis X (m)").pack()
    x_start_entry = tk.Entry(root)
    x_start_entry.insert(0, "0.0")
    x_start_entry.pack()

    tk.Label(root, text="Starting position axis Y (m)").pack()
    y_start_entry = tk.Entry(root)
    y_start_entry.insert(0, "0.0")
    y_start_entry.pack()

    tk.Button(root, text="Start Simulation", command=start_simulation).pack(pady=10)

    error_label = tk.Label(root, text="", fg="red")
    error_label.pack(pady=10)

    root.mainloop()

def main_window():
    global angle, speed, width, height, main_background_day, red_ball, menu_active, menu_rects, land_pos

    # Pygame display in fullscreen mode
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    width, height = screen.get_size()
    pygame.display.set_caption("Ballistique 2D")

    main_background_day = pygame.transform.scale(main_background_day, (width, height))
    all_sprites.empty()
    ball = Projectile(red_ball, width, height, angle, speed)
    all_sprites.add(ball)
    ball.calculate_landing_position()
    
    # Ensure land_pos has the correct value
    if land_pos:
        max_value = land_pos[0]  # Set the max value to the calculated landing position
    else:
        max_value = 100  # Default value if no landing position is calculated yet

    # Move the slider lower by changing the y-coordinate
    slider = Slider(pos=(width // 2, 150), size=(300, 20), initial_val=0, min_val=0, max_val=max_value)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu_active = not menu_active  # Toggle the menu

            if not menu_active:  # Only handle events related to the game if the menu is not active
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        slider.grab(pygame.mouse.get_pos())
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:  # Left mouse button
                        slider.release()
                elif event.type == pygame.MOUSEMOTION:
                    if slider.grabbed:
                        slider.move_slider(pygame.mouse.get_pos())
                    slider.hover(pygame.mouse.get_pos())
            else:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if menu_rects[0].collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()
                    elif menu_rects[1].collidepoint(mouse_pos):
                        # Restart the simulation
                        menu_active = False
                        open_menu()

        # Update
        if not menu_active:  # Only update sprites if the menu is not active
            all_sprites.update()

        # Draw
        screen.fill(black)
        screen.blit(main_background_day, (0, 0))
        all_sprites.draw(screen)

        # Draw the red line
        for sprite in all_sprites:
            if isinstance(sprite, Projectile):
                sprite.draw_a_red_line(screen)

        # Draw the slider and its additional info
        if not menu_active:
            slider.render(screen)
            slider.update_distance_and_time(screen)  # Update and display distance and time

        # Draw the menu if active (opened)
        if menu_active:
            draw_menu(screen)

        pygame.display.flip()

        # Frames update
        clock.tick(fps)



open_menu()