import sys
import pygame
import pygame_gui
import imageio
import math

pygame.init()

# paramètres du display
width = 1000
height = 500
screen = pygame.display.set_mode((width, height))
pygame.display.setCaption("Ballistique 2D")

angle = ""

# background
gif_path = 'background/background_start.gif'
gif = pygame.image.load(gif_path)
full_screen_gif = pygame.transform.scale(gif, (width, height))

# sprites images
red_ball = pygame.image.load("character/red_ball_2.png")
ball_size = (100, 100)  # Set the size of the ball (width, height)
red_ball = pygame.transform.scale(red_ball, ball_size)
ball = red_ball.get_rect()
ball.center = (width // 2, height // 2)

# class pour le projectile
class Projectile(pygame.sprite.Sprite):
    def __init__(self, ball_image, width, height, angle):
        super().__init__()
        self.image = ball_image
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height // 2)
        self.start_time = pygame.time.get_ticks() / 1000

        #00
        ppx_par_metre = 100  # Conversion des pixels en mètres

        # Position initiale au centre de l'écran
        self.pos = [width // 2, height // 2]

        # Calcul de la vitesse initiale en utilisant l'angle donné par l'utilisateur
        # L'angle est converti en radians pour les fonctions trigonométriques
        # La composante x de la vitesse (vit[0]) est calculée en multipliant 10 par le cosinus de l'angle
        # La composante y de la vitesse (vit[1]) est calculée en multipliant 10 par le sinus de l'angle et en inversant le signe pour le mouvement vers le haut
        self.vit = [10 * math.cos(math.radians(angle)) * ppx_par_metre, -10 * math.sin(math.radians(angle)) * ppx_par_metre]

        # Accélération due à la gravité
        self.acc = [0, 9.81 * ppx_par_metre]
        #00

    def update(self):
        dt = 1 / 60  # deltaT est égale à 1 FPS
        self.movement(dt)

        # on affiche la balle au nouvel emplacement
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def movement(self, dt):
        # Mise à jour de la vitesse
        # v = v0 + a * t
        self.vit[0] += self.acc[0] * dt  # mise à jour de la vitesse en X
        self.vit[1] += self.acc[1] * dt  # mise à jour de la vitesse en Y

        # Mise à jour de la position
        # x = x0 + v * t + 0.5 * a * t^2
        # Note: La contribution de 0.5 * a * t^2 est généralement petite pour des petits dt et est souvent omise dans les simulations basiques
        self.pos[0] += self.vit[0] * dt  # mise à jour de la position en X
        self.pos[1] += self.vit[1] * dt  # mise à jour de la position en Y

# Créé un groupe pour le sprite
all_sprites = pygame.sprite.Group()

# variable de pygame_gui
fps = 60
clock = pygame.time.Clock()
manager = pygame_gui.UIManager((width, height))

# user's inputs

# angle
angle_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((350, 275), (200, 50)), manager=manager, object_id="user_angle")

# vitesse
# speed_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((0, 275), (200, 50)), manager=manager, object_id="user_speed")

def main_window(angle):
    all_sprites.empty()  # Vide le groupe de sprites
    ball = Projectile(red_ball, width, height, angle)  # Crée une nouvelle instance de Projectile avec l'angle donné
    all_sprites.add(ball)  # Ajoute le projectile au groupe de sprites

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

        # frames update
        clock.tick(fps)

def user_fly_info():
    global angle
    while True:
        UI_REFRESH_RATE = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "user_angle":
                angle = float(event.text)  # Convertit l'angle donné par l'utilisateur en float
                main_window(angle)  # Appelle la fonction main_window avec l'angle donné

            manager.process_events(event)

        manager.update(UI_REFRESH_RATE)

        screen.blit(full_screen_gif, (0, 0))

        manager.draw_ui(screen)

        pygame.display.update()

user_fly_info()
