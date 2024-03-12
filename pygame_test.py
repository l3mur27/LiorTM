import pygame 

#logo + nom du projet tout en haut de la fenêtre qui s'ouvre
icon = pygame.image.load("logo_top.jpeg")
pygame.display.set_icon(icon)
pygame.display.set_caption("Balistique 2D")

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init()


screen = pygame.display.set_mode(([1000, 300]))


running = True
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

