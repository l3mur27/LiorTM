import sys
import pygame
import pygame_gui
import imageio

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


#les variables pour le vol du projectile

speed = ""
angle = ""
x_start = ""
y_start = ""

#constante de gravité

g = 9,81

#variable de pygame_gui

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

        screen.fill("lime")

        pygame.display.update()



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