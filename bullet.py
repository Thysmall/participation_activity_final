import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Bullet(Sprite):
    """Stores functions about bullets

    Args:
        Sprite (class): Used for collisions 
    """
    def __init__(self, game: 'AlienInvasion') -> None:
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        
        #Image creation
        self.image = pygame.image.load(self.settings.bullet_file)
        self.image = pygame.transform.scale(self.image,
            (self.settings.bullet_w,self.settings.bullet_h)
            )
        
        #Boundaries and Location creation
        self.rect = self.image.get_rect()
        self.rect.midtop = game.ship.rect.midtop
        self.y = int(self.rect.y)
        
    def update(self):
        """Moves the bullet
        """
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y
        
    def draw_bullet(self):
        """Draws the bullet
        """
        self.screen.blit(self.image,self.rect)