import sys
import pygame
from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from time import sleep
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:

    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height), pygame.RESIZABLE)
        pygame.display.set_caption("ALIEN INVASION")
        self.previous_screen_width = self.settings.screen_width
        self.previous_screen_height = self.settings.screen_height
        self.stats = GameStats(self)
        self.ship = Ship(self)
        self.clock = pygame.time.Clock()
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._alien_fleet()
        self.play_button = Button(self, 'PLAY')
        self.scoreboard = Scoreboard(self)

    def run_game(self):
        while True:
            self._update_screen()
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            pygame.display.flip()
            self.clock.tick(60)
    def _check_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.VIDEORESIZE:
                    self.settings.screen_width, self.settings.screen_height = event.w, event.h
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    self.ship.update_position()
                    self._update_alien_positions()
                    self.scoreboard.update_positions()
                    self.previous_screen_width = self.settings.screen_width
                    self.previous_screen_height = self.settings.screen_height
                elif event.type == pygame.KEYDOWN:
                    self._keydown_events(event)
                elif event.type == pygame.KEYUP:
                    self._keyup_events(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self._check_play_button(mouse_pos)
    
    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.scoreboard.prep_score()
            self.scoreboard.prep_level()
            self.scoreboard.prep_ships()
            self.aliens.empty()
            self.bullets.empty()
            self._alien_fleet()
            self.ship.center_ship()
            pygame.mouse.set_visible(True)

    def _keydown_events(self, event):
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.right = True
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
            sys.exit()
    
    def _keyup_events(self, event):
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.right = False
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.left = False
    
    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    
    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._alien_bullet_collision()
    
    def _alien_bullet_collision(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.scoreboard.prep_score()
            self.scoreboard.check_high_score()
        if not self.aliens:
            self.bullets.empty()
            self._alien_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.scoreboard.prep_level()
    
    def _create_alien(self, alien_index, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_index
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)
    
    def _alien_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        ship_height = self.ship.rect.height

        available_space_x = self.settings.screen_width - (2 * alien_width)
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)

        alien_index = available_space_x // (2 * alien_width)
        number_rows = available_space_y // (2 * alien_height)

        for row_number in range(number_rows):
            for alien in range(alien_index):
                self._create_alien(alien, row_number)
    
    
    def _update_alien_positions(self):
        for alien in self.aliens:
            alien.update_position(self.previous_screen_width, self.settings.screen_width)

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        self._aliens_ground()
    
    def _ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.scoreboard.prep_ships()
            self.aliens.empty()
            self.bullets.empty()

            self._alien_fleet()
            self.ship.center_ship()
        else:
            self.stats.game_active = False
            

        sleep(0.5)
    
    def _aliens_ground(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _update_screen(self):
        self.screen.fill(self.settings.background_color)
        self.ship.blitShip()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.scoreboard.show_score()
        if not self.stats.game_active:
            self.play_button.draw_button()

    

if __name__ == '__main__':
    game = AlienInvasion()
    game.run_game()