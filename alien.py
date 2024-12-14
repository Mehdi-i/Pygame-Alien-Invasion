

import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.image = pygame.image.load(r"C:\Users\sahel\Python_Crash_Course\Pygame_Alien_Invasion\Images\Alien.png")
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.settings = game.settings

    def update_position(self, old_screen_width, new_screen_width):
        scale_ratio = new_screen_width / old_screen_width
        self.x *= scale_ratio
        self.rect.x = int(self.x)

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
    
    def update(self):
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

