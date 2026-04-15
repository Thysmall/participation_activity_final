import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Alien(Sprite):
    """Stores functions about aliens

    Args:
        Sprite (class): Used for collisions 
    """
    def __init__(self, game: 'AlienInvasion', x: int, y: int) -> None:
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.boundaries = game.screen.get_rect()
        self.settings = game.settings
        
        #Image creation
        self.image = pygame.image.load(self.settings.alien_file)
        self.image = pygame.transform.scale(self.image,
            (self.settings.alien_w,self.settings.alien_h)
            )
        
        #Boundaries and Location creation
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = int(self.rect.x)
        self.y = int(self.rect.y)
        
    def update(self):
        """Moves the alien
        """
        temp_speed = self.settings.fleet_speed
        
        if self.check_edges():
            self.settings.fleet_direction *= -1
        self.x += temp_speed * self.settings.fleet_direction
        self.rect.x = self.x
        
    def check_edges(self):
        return (self.rect.right > self.boundaries.right or self.rect.left <= self.boundaries.left)
        
    def draw_alien(self):
        """Draws the alien
        """
        self.screen.blit(self.image,self.rect)