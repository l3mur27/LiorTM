import pygame
import sys 

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

#créé un dsplay 
screen = pygame.display.set_mode(([1000, 1000]))

# une classe pour créé un objet en ayant comme paramètre le liens vers le png 
#et ça taille en pourcentage (en se basant sur ça taille initiale) 
class Sprite(pygame.sprite.Sprite):
    def __init__(self, image_path, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_path).convert_alpha()
        original_width, original_height = self.image.get_size()
        self.new_width = int(original_width * x)
        self.new_height = int(original_height * x)
        self.image = pygame.transform.scale(self.image, (self.new_width, self.new_height))
        self.rect = self.image.get_rect()

#def move(x, y):
    


#créé la balle de golf et diminue sa taille de 30%
Golf_ball = Sprite("golf_ball.png", 0.9)

#permet de fermer le programme en appuyant sur la touche "esc"
running = True
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

    #donne une couleur au display
    screen.fill((0, 0, 0))

    # Blit le sprite de la balle de golf sur l'écran
    screen.blit(Golf_ball.image, Golf_ball.rect)
    
    # met à jour le display
    pygame.display.flip()

