import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    from arsenal import Arsenal

class Ship:
    """Stores functions for the Ship
    """
    
    def __init__(self, game: 'AlienInvasion', arsenal: 'Arsenal') -> None:
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.boundaries = self.screen.get_rect()
        
        #Image creation
        self.image = pygame.image.load(self.settings.ship_file)
        self.image = pygame.transform.scale(self.image,
            (self.settings.ship_w,self.settings.ship_h)
            )
        
        #Boundary and location creation
        self.rect = self.image.get_rect()
        self._center_ship()
        self.moving_right = False
        self.moving_left = False
        
        self.arsenal = arsenal

    def _center_ship(self):
        self.rect.midbottom = self.boundaries.midbottom
        self.x = int(self.rect.x)
        
    def update(self):
        """Runs update functions for the ship
        """
        # Update position of the ship
        self._update_ship_movement()
        self.arsenal.update_arsenal()

    def _update_ship_movement(self):
        """Changes the ships location based on key pressed
        """
        temp_speed = self.settings.ship_speed
        if self.moving_right and self.rect.right < self.boundaries.right: 
            self.x += temp_speed
        if self.moving_left and self.rect.left > self.boundaries.left:
            self.x -= temp_speed
            
        self.rect.x = self.x
    
    def draw(self):
        """Draws the ship on the screen
        """
        self.arsenal.draw()
        self.screen.blit(self.image,self.rect)
        
    def fire(self):
        """Shoots a bullet from the arsenal

        Returns:
            bool: If the bullet was shot or not. Used for sound effect
        """
        return self.arsenal.fire_bullet()
    
    def check_collisions(self, other_group):
        if pygame.sprite.spritecollideany(self, other_group):
            self._center_ship()
            return True
        return False