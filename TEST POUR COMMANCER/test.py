import sys
import pygame
import math
import dearpygui.dearpygui as dpg

pygame.init()

# Parameters of the display
width = 960
height = 540

angle = 0.0  # Initialize as float
speed = 0.0  # Initialize as float
x_start = 0.0
y_start = 0.0
gravity = 9.81

# Background
gif_path = 'background/background_start.gif'
gif = pygame.image.load(gif_path)

main_background_day_path = 'background/1.png'
main_background_day = pygame.image.load(main_background_day_path)

# Sprite images
red_ball = pygame.image.load("character/red_ball_2.png")
ball_size = (30, 30)  # Set the size of the ball (width, height)
red_ball = pygame.transform.scale(red_ball, ball_size)
ball = red_ball.get_rect()
ball.center = (width // 2, height // 2)

# Class for the projectile
class Projectile(pygame.sprite.Sprite):
    def __init__(self, ball_image, width, height, angle, speed):
        super().__init__()
        self.image = ball_image
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height // 2)
        self.start_time = pygame.time.get_ticks() / 1000

        ppx_par_metre = 100

        self.pos = [ball_size[1] + x_start * ppx_par_metre, (height - y_start * ppx_par_metre) - ball_size[1]]
        self.vit = [speed * math.cos(math.radians(angle)) * ppx_par_metre, -(speed) * math.sin(math.radians(angle)) * ppx_par_metre]
        self.acc = [0, gravity * ppx_par_metre]

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

        if self.pos[1] >= height - ball_size[1]:
            self.pos[1] = height - ball_size[1]  
            self.vit = [0, 0] 

    def calculate_landing_position(self):
        # Calculate time of flight
        time_of_flight = (2 * speed * math.sin(math.radians(angle))) / gravity

        # Calculate horizontal distance
        horizontal_distance = x_start + speed * math.cos(math.radians(angle)) * time_of_flight

        print(f"The projectile will land at x: {horizontal_distance:.3f} meters, y: 0.0 meters, and the fly time is: {time_of_flight:.3f} seconds")

# Create a group for the sprite
all_sprites = pygame.sprite.Group()

# Pygame variables
fps = 60
clock = pygame.time.Clock()

def main_window():
    global angle, speed, width, height, main_background_day, red_ball

    # Set up Pygame display
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    pygame.display.set_caption("Ballistique 2D")

    main_background_day = pygame.transform.scale(main_background_day, (width, height))
    all_sprites.empty()
    ball = Projectile(red_ball, width, height, angle, speed)
    all_sprites.add(ball)
    ball.calculate_landing_position()


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update
        all_sprites.update()

        # Draw
        screen.fill("black")
        screen.blit(main_background_day, (0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()

        # Frames update
        clock.tick(fps)

def start_simulation(sender, app_data):
    global angle, speed, x_start, y_start
    try:
        angle = float(dpg.get_value("Angle Input"))
        speed = float(dpg.get_value("Speed Input"))
        x_start = float(dpg.get_value("x start input"))
        y_start = float(dpg.get_value("y start input"))
        dpg.set_value("Error Message", "")
        dpg.hide_item("Projectile Fly Information")
        pygame.display.quit()  # Ensure previous Pygame display is closed
        main_window()
    except ValueError:
        dpg.set_value("Error Message", "Invalid input. Please enter numeric values.")

dpg.create_context()

with dpg.window(label="Projectile Fly Information", tag="Projectile Fly Information"):
    dpg.add_text("Enter the initial conditions for the projectile:")
    dpg.add_input_text(label="Angle (degrees)", tag="Angle Input", default_value="0.0") 
    dpg.add_input_text(label="Speed (m/s)", tag="Speed Input", default_value="0.0")
    dpg.add_input_text(label="Starting position axis X (m)", tag="x start input", default_value="0.0")
    dpg.add_input_text(label="Starting position axis Y (m)", tag="y start input", default_value="0.0")
    dpg.add_button(label="Start Simulation", callback=start_simulation)
    dpg.add_text("", tag="Error Message", color=[255, 0, 0])

dpg.create_viewport(title='Ballistique 2D Control', width=width, height=height)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
