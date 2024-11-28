import sys
import pygame
import math
import tkinter as tk

pygame.init()

# Parameters of the display
width = 960
height = 540

"""
Main variables 
#1 - are initialized as a float so that we don't have to convert it later
#2 - are initialized as integer for example because the are not "," in pixels
#3 - constant
"""
angle = 0.0  #1
speed = 0.0  #1
x_start = 0.0 #1
y_start = 0.0 #1
gravity = 9.81 #3
land_pos = []
ppx_par_metre = 30 #2
screen_width = 0   #2
screen_height = 0  #2
rescale = []
max_high = 0.0     #1  

# Colors 

red = (255, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)
gray = (50, 50, 50)
dark_gray = (169, 169, 169)

button_state = {False: gray, True: "lightgray"} # Button state (slider state)

# Initialize Fonts 
pygame.font.init()
FONT = pygame.font.Font(None, 24)

# Background
main_background_day_path = 'background/1.png'
main_background_day = pygame.image.load(main_background_day_path)

# Sprite image (Ball)
red_ball = pygame.image.load("character/red_ball_2.png")
ball_size = (13, 13)    
# The size of the ball (width, height)
red_ball = pygame.transform.scale(red_ball, ball_size)
ball = red_ball.get_rect()

# Sprite images (Stickman)
stickman = pygame.image.load("character/stickman.png")
stickman_size = (19, 54)
stickman = pygame.transform.scale(stickman, stickman_size)  
stickman_original = stickman   

# Sprite images (House)
house = pygame.image.load("character/house.png")
house_size = (150, 150)
house = pygame.transform.scale(house, house_size)  
house_original = house   

class Slider:
    """Slider class"""
    def __init__(self, pos: tuple, size: tuple, initial_val: float, min_val: int, max_val: int) -> None:
        self.pos = pos
        self.size = size
        self.hovered = False # Initialize as False 
        self.grabbed = False # Initialize as False 

        self.slider_left_pos = self.pos[0] - (size[0] // 2)
        self.slider_right_pos = self.pos[0] + (size[0] // 2)
        self.slider_top_pos = self.pos[1] - (size[1] // 2)

        self.min = min_val # Sliders min value
        self.max = max_val # Sliders max value
        self.initial_val = (self.slider_right_pos - self.slider_left_pos) * initial_val  

        self.container_rect = pygame.Rect(self.slider_left_pos, self.slider_top_pos, self.size[0], self.size[1])
        self.button_rect = pygame.Rect(self.slider_left_pos + self.initial_val - 5, self.slider_top_pos, 10, self.size[1])

    def move_slider(self, mouse_pos):
        """The function to make the slider button move"""
        pos = mouse_pos[0]
        if pos < self.slider_left_pos:
            pos = self.slider_left_pos
        elif pos > self.slider_right_pos:
            pos = self.slider_right_pos
        self.button_rect.centerx = pos

    def hover(self, mouse_pos):
        """The function to change from False to True or the opposite when the button is hovered"""
        if self.button_rect.collidepoint(mouse_pos):
            self.hovered = True
        else:
            self.hovered = False

    def grab(self, mouse_pos):
        """The function to check if the button was grabed"""
        if self.button_rect.collidepoint(mouse_pos):
            self.grabbed = True

    def release(self):
        """The function to to check if the button is realesed """
        self.grabbed = False

    def render(self, screen):
        """The function that makes appear the slider """
        pygame.draw.rect(screen, dark_gray, self.container_rect)
        pygame.draw.rect(screen, button_state[self.hovered], self.button_rect)

    def get_value(self):
        """The function that calculates the position of the slider to get a value on top of it """
        val_range = self.slider_right_pos - self.slider_left_pos - 1
        button_val = self.button_rect.centerx - self.slider_left_pos
        return (button_val / val_range) * (self.max - self.min) + self.min

    def update_distance_and_time(self, screen):
        """The function that calculates and displays  the time and the distance associated with the slider value """

        current_value = self.get_value() # Get current slider value


        # Calculate distance and time 
        distance = current_value
        angle_rad = math.radians(angle)
        speed_x = speed * math.cos(angle_rad)
        time_to_reach_x = distance / speed_x if speed_x != 0 else float("inf")

        # Render distance and time
        distance_text = FONT.render(f"Distance: {distance:.2f} m", True, white)
        time_text = FONT.render(f"Time: {time_to_reach_x:.2f} s", True, white)

        screen.blit(distance_text, (self.pos[0] - distance_text.get_width() // 2, self.slider_top_pos - 70))
        screen.blit(time_text, (self.pos[0] - time_text.get_width() // 2, self.slider_top_pos - 50))




class Projectile(pygame.sprite.Sprite):
    """ Class for the projectile """
    def __init__(self, ball_image, width, height, angle, speed):
        super().__init__()
        self.original_image = ball_image  # Store the original image
        self.image = self.original_image
        self.rect = self.original_image.get_rect()
        self.rect.center = (width // 2, height // 2)
        self.start_time = pygame.time.get_ticks() / 1000
        self.positions = []

    def pos_vit_acc(self):
        """Update the initial position based on the rescaled ball size """
        global x_start

        x_start = 8 # Modifies the ball initial starting position so that the stickman and the house are beside 

        self.pos = [ball_size[1] + x_start * ppx_par_metre * rescale[0], (height - y_start * ppx_par_metre * rescale[0]) - ball_size[1]]
        self.vit = [speed * math.cos(math.radians(angle)) * ppx_par_metre * rescale[0], -(speed) * math.sin(math.radians(angle)) * ppx_par_metre * rescale[0]]
        self.acc = [0, gravity * ppx_par_metre * rescale[0]]

    def update(self):
        """Update the ball's position"""
        dt = 1 / 60  # deltaT is equal to 1 FPS
        self.movement(dt)
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def movement(self, dt):
        """Updates the velocity and the position"""

        # Update the velocity after rescale
        self.vit[0] += self.acc[0] * dt  # Update velocity in X
        self.vit[1] += self.acc[1] * dt  # Update velocity in Y

        # Update the position
        self.pos[0] += self.vit[0] * dt  # Update position in X
        self.pos[1] += self.vit[1] * dt  # Update position in Y

        # Append the new position, adjusted for the center of the ball 
        self.positions.append((self.pos[0] + (self.rect.width / 2), self.pos[1] + (self.rect.height / 2)))

        if self.pos[1] >= height - ball_size[1]:
            self.pos[1] = height - ball_size[1]
            self.vit = [0, 0]

    def calculate_landing_position(self):
        """Function calculates the time of the flight and the distance that the ball overcame """

        #Calculate time of flight

        v0y = speed * math.sin(math.radians(angle))

        a = -0.5 * gravity
        b = v0y
        c = y_start

        delta = b**2 - 4*a*c

        if delta < 0:
            print("There are no solution, the ball won't touch the ground.")
        else:
            x1 = (-b + math.sqrt(delta)) / (2 * a)
            x2 = (-b - math.sqrt(delta)) / (2 * a)

        time_of_flight = max(x1, x2) # Takes the positif time between x1 and x2
        
        # Calculate horizontal distance
        horizontal_distance = x_start + speed * math.cos(math.radians(angle)) * time_of_flight
        land_pos.append(horizontal_distance)

        self.highest_point()

        print(f"The projectile will land at x: {horizontal_distance:.3f} meters, y: 0.0 meters, and the fly time is: {time_of_flight:.3f} seconds")
        print(f"The highest point reached is: {max_high:.3f} meters")
        
        self.rescale()  # Call rescale after calculating the landing position

    def rescale(self):
        global screen_width, rescale, ball_size, screen_height, stickman, house, stickman_size, house_size

        # Gets the users screen width 
        if screen_width == 0:
            screen_width = pygame.display.get_surface().get_width()
            screen_height = pygame.display.get_surface().get_height()

        # Convert the landing and highest positions from meters to pixels 
        landing_position_in_pixels = land_pos[0] * ppx_par_metre
        highest_position_in_pixels = max_high * ppx_par_metre

        # Print the users screen size 
        print(f"Screen Width: {screen_width} pixels")
        print(f"Screen Width: {screen_height} pixels")
        
        # Check if the landing position is outside of the users default screen size 
        if landing_position_in_pixels >= screen_width and highest_position_in_pixels >= screen_height:
            print("out horizontal and vertical")
            rescale_factor = min((screen_height - 220) / highest_position_in_pixels, (screen_width - 220) / landing_position_in_pixels)
            rescale.append(rescale_factor)
            print("Rescale factor", rescale[0])

        elif x_start * ppx_par_metre >= screen_width:
            print("initially out horizontal")
            rescale.append((screen_width - 220) / landing_position_in_pixels)
            print("Rescale factor", rescale[0])

        elif landing_position_in_pixels >= screen_width:
            print("out horizontal")
            rescale.append((screen_width - 220) / landing_position_in_pixels)
            print("Rescale factor", rescale[0])
        
        elif highest_position_in_pixels >= screen_height:
            print("out vertical")
            rescale.append((screen_height - 220) / highest_position_in_pixels)
            print("Rescale factor", rescale[0])

        else:
            print("in")
            rescale.append(1)
            print("Rescale factor", rescale[0])

        if rescale:
            # Adjust the ball size based on the rescale factor
            
            ball_size = (int(13 * rescale[0]), int(13 * rescale[0]))
            

            # Rescale the ball image based on the new ball size 
            self.image = pygame.transform.scale(self.original_image, ball_size)
            self.rect = self.image.get_rect(center=self.rect.center)

            # Scale the stickman and house images based on the original images 
            stickman_size = (int(19 * rescale[0]), int(54 * rescale[0]))
            house_size = (int(150 * rescale[0]), int(150 * rescale[0]))

            stickman = pygame.transform.scale(stickman_original, stickman_size)  
            house = pygame.transform.scale(house_original, house_size)  


            # Recalculate position, velocity, and acceleration with the new scale 
            self.pos_vit_acc()

    def time_at_x_position(self, x_pos):
        """Time at a given position"""

        # Horizontal velocity (MRU) 
        v_x = speed * math.cos(math.radians(angle))

        # Calculate time at x position
        time_at_x = (x_pos - x_start) / v_x if v_x != 0 else float('None')  # Prevent division by zero

        return time_at_x
    
    def highest_point(self):
        """Highest position that a ball can reach"""
        global max_high, speed, angle, gravity, y_start
    
        vertical_speed = speed * math.sin(math.radians(angle))
    
        max_high = y_start + (vertical_speed ** 2) / (2 * gravity)
        return max_high

    def draw_a_red_line(self, screen):
        """Draws a red line behind the ball"""
        if len(self.positions) > 1:
            for i in range(len(self.positions) - 1):
                pygame.draw.line(screen, red, self.positions[i], self.positions[i+1], 2)

# Create a group for the sprite
all_sprites = pygame.sprite.Group()


# Pygame variables to set 60 frames per second 
fps = 60
clock = pygame.time.Clock()

# Menu state(Open or Closed)
menu_active = False
menu_rects = (None, None)

 
def draw_menu(screen):
    """Draws a esc menu """
    global menu_rects

    # Menu size 
    menu_width = 300
    menu_height = 200
    menu_x = (width - menu_width) // 2
    menu_y = (height - menu_height) // 2

    # Draw menu background 
    pygame.draw.rect(screen, gray, (menu_x, menu_y, menu_width, menu_height))
    
    # Button size 
    button_width = 100
    button_height = 50
    button_x = menu_x + (menu_width - button_width) // 2

    # Exit button 
    exit_button_y = menu_y + (menu_height - button_height) // 2 - 30  # Positioned a bit higher
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
    """ Function that launches the simulation """
    global angle, speed, x_start, y_start, land_pos, screen_width, rescale, menu_active

    # Reset variables 
    angle = 0.0
    speed = 0.0
    x_start = 0.0
    y_start = 0.0
    land_pos.clear()
    rescale.clear()
    menu_active = False

    # Try if the numeric values are entered correctly 
    try:
        angle = float(angle_entry.get())
        speed = float(speed_entry.get())
        y_start = float(y_start_entry.get())

        # Validate angle: It should be between -90 and 90 degrees 
        if not (-90 <= angle <= 90):
            error_label.config(text="Invalid input. Angle must be between -90° and 90°.")
            return  # Stop execution and show error
        
        """ Validate speed: It should not be equal to 0. """
        if speed <= 0:
            error_label.config(text="Invalid input. Speed should not be equal to 0.")
            return  # Stop execution and show error

        

        error_label.config(text="")  # Clear the error if inputs are valid
        root.destroy()  # Close the Tkinter menu
        pygame.display.quit()  # Closes the previous pygame display
        main_window()  # Launches the main window

    except ValueError:
        error_label.config(text="Invalid input. Please enter numeric values.")  # Show this in case of entering a wrong numeric value


def open_menu():
    """Open the Tkinter menu to enter values in it"""
    global root, angle_entry, speed_entry, y_start_entry, error_label

    root = tk.Tk()
    root.title("Projectile Simulation Menu")

    tk.Label(root, text="Enter the initial conditions for the projectile:").pack()

    # Angle input
    tk.Label(root, text="Angle (degrees)").pack()
    angle_entry = tk.Entry(root)
    angle_entry.insert(0, "0.0")
    angle_entry.pack()

    # Speed input
    tk.Label(root, text="Speed (m/s)").pack()
    speed_entry = tk.Entry(root)
    speed_entry.insert(0, "1.0")
    speed_entry.pack()

    # Y pos input 
    tk.Label(root, text="Starting position axis Y (m)").pack()
    y_start_entry = tk.Entry(root)
    y_start_entry.insert(0, "0.0")
    y_start_entry.pack()

    tk.Button(root, text="Start Simulation", command=start_simulation).pack(pady=10) # when the button pressed go to start_simulation 

    error_label = tk.Label(root, text="", fg="red")
    error_label.pack(pady=10)

    root.mainloop() # starts the Tkinter event loop

def main_window():
    """Loads the main window"""
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

    # land_pos correct value 
    if land_pos:
        max_value = land_pos[0]  # Set the max value 
    else:
        max_value = 100  # Default value if no landing position 

    # Makes the slider appear 
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

        # Draw the stickman and the house at a fixed position 
        stickman_rect = stickman.get_rect(center=(20 * rescale[0], height - (25 * rescale[0])))  
        screen.blit(stickman, stickman_rect)
        house_rect = house.get_rect(center=(120 * rescale[0], height - (75 * rescale[0]) ))  
        screen.blit(house, house_rect)

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

