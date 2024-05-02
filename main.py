import sys
import pygame
import pygame_gui
import imageio
import math

pygame.init()

#paramètres du display
width = 1000
height = 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ballistique 2D")


#background

gif_path = 'background/background_start.gif' 
gif = pygame.image.load(gif_path)

full_screen_gif = pygame.transform.scale(gif, (width, height))

#sprites images

red_ball = pygame.image.load("character/red_ball_2.png")
ball_size = (100, 100)  # Set the size of the ball (width, height)
red_ball = pygame.transform.scale(red_ball, ball_size)
ball = red_ball.get_rect()
ball.center = ((width //2 , height // 2))

#class pour le projectile

class Projectile(pygame.sprite.Sprite):
    def __init__(self, ball_image, width, height):
        super().__init__()
        self.image = ball_image
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height // 2)
        self.start_time = pygame.time.get_ticks() / 1000

    # une fonction qui fait bouger l'objet grace à l'équation horraire

    def update(self):

        time = pygame.time.get_ticks() / 1000
        fly_time = time - self.start_time

        self.rect.y = (0.5 * gravity * (fly_time ** 2))

        #self.rect.y = (- 0.5 * gravity * (fly_time ** 2) + (math.sin(math.degrees(30) * 30 * fly_time )))
        #self.rect.x = ( math.cos(math.degrees(30)) * 30 * fly_time ) 
        


# Créé un groupe pour le sprite

all_sprites = pygame.sprite.Group()
ball = Projectile(red_ball, width, height)
all_sprites.add(ball)


#les variables pour le vol du projectile

speed = ""
angle = ""
x_start = ""
y_start = ""

#constante de gravité

gravity = 9.81

#variable de pygame_gui

fps = 60
clock = pygame.time.Clock()
manager = pygame_gui.UIManager((width, height))

#text input

text_input_test = pygame_gui.elements.UITextEntryLine(relative_rect= pygame.Rect((350, 275), (200, 50)), manager=manager, object_id = "main_text")

def main_window():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update
        all_sprites.update()

        # Dessine
        screen.fill("black")
        all_sprites.draw(screen)
        pygame.display.flip()

        #framaes update
        clock.tick(fps)



def user_fly_info():
    while True:
        UI_REFRESH_RATE = clock.tick(60)/1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "main_text":
                main_window()

            manager.process_events(event)

        manager.update(UI_REFRESH_RATE) 

        screen.blit(full_screen_gif, (0, 0))

        manager.draw_ui(screen)

        pygame.display.update()

user_fly_info()

