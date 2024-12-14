import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.image = pygame.image.load(r"C:\Users\sahel\Python_Crash_Course\Pygame_Alien_Invasion\Images\DurrrSpaceShip.png")
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        self.right = False
        self.left = False
        self.settings = game.settings
        self.x = float(self.rect.x)

    def update_position(self):
        previous_screen_width = self.screen_rect.width
        self.screen_rect = self.screen.get_rect()

        if previous_screen_width > 0:
            self.x = (self.x / previous_screen_width) * self.screen_rect.width
        self.rect.midbottom = self.screen_rect.midbottom
        self.rect.x = self.x
    
    def update(self):
        if self.right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        self.rect.x = self.x

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        
    def blitShip(self):
        self.screen.blit(self.image, self.rect)