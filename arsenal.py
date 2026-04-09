import pygame
from typing import TYPE_CHECKING
from bullet import Bullet

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    

class Arsenal:
    """Stores funcitons for managing the ammo supply
    """
    def __init__(self, game: 'AlienInvasion') -> None:
        self.game = game
        self.settings = game.settings
        self.arsenal = pygame.sprite.Group()
        
    def update_arsenal(self):
        """Runs update functions for the arsenal
        """
        self.arsenal.update()
        self._remove_bullets_offscreen()
        
    def _remove_bullets_offscreen(self):
        """Removes the bullets if they fly off screen
        """
        for bullet in self.arsenal.copy():
            if bullet.rect.bottom <= 0:
                self.arsenal.remove(bullet)
        
    def draw(self):
        """Draws each of the bullets to the screen
        """
        for bullet in self.arsenal:
            bullet.draw_bullet()
            
    def fire_bullet(self):
        """Shoots a bullet if there aren't more than the max on screen

        Returns:
            bool: True if bullet was fired. Else, False
        """
        if len(self.arsenal) < self.settings.bullet_ammount:
            new_bullet = Bullet(self.game)
            self.arsenal.add(new_bullet)
            return True
        return False