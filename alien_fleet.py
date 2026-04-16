import pygame
from typing import TYPE_CHECKING
from alien import Alien

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    
    
class AlienFleet:
    """Manages the entire fleet of Alien sprites
    """
    def __init__(self, game: 'AlienInvasion'):
        self.game = game
        self.settings = game.settings
        self.fleet = pygame.sprite.Group()
        self.fleet_direction = self.settings.fleet_direction
        self.fleet_drop_speed = self.settings.fleet_drop_speed
        
        self.create_fleet()
        
    def create_fleet(self):
        """Creates the fleet of aliens using smaller functions
        """
        alien_w = self.settings.alien_w
        alien_h = self.settings.alien_h
        screen_w = self.settings.screen_w
        screen_h = self.settings.screen_h
        
        # calculate the fleet size and offset needed to center it
        fleet_w, fleet_h = self.calculate_fleet_size(alien_w, screen_w, alien_h, screen_h)
        x_offset, y_offset = self.calculate_offsets(alien_w, alien_h, screen_w, fleet_w, fleet_h)
        
        # generate the fleet
        self._create_rectangle_fleet(alien_w, alien_h, fleet_w, fleet_h, x_offset, y_offset)

    def _create_rectangle_fleet(self, alien_w, alien_h, fleet_w, fleet_h, x_offset, y_offset):
        """Generates the fleet

        Args:
            alien_w (int): Width of each alien
            alien_h (int): Height of each alien
            fleet_w (int): Width of the fleet
            fleet_h (int): Height of the fleet
            x_offset (int): Offset between aliens side to side
            y_offset (int): Offset between aliens up and down
        """
        for row in range(fleet_h):
            for col in range(fleet_w):
                current_x = alien_w * col + x_offset
                current_y = alien_h * row + y_offset
                if col % 2 == 0 or row %2 == 0:
                    continue
                
                self._create_alien(current_x, current_y)

    def calculate_offsets(self, alien_w, alien_h, screen_w, fleet_w, fleet_h):
        """Calculates the offsets used when generating the fleet

        Args:
            alien_w (int): Width of each alien
            alien_h (int): Height of each alien
            screen_w (int): Width of the screen
            fleet_w (int): Total number of aliens wide the fleet is
            fleet_h (int): Total number of aliens high the fleet is

        Returns:
            tuple(int): Both the x offset and y offset values
        """
        half_screen = self.settings.screen_h//2
        fleet_horizontal_space = fleet_w * alien_w
        fleet_vertical_space = fleet_h * alien_h
        x_offset = int((screen_w-fleet_horizontal_space)//2)
        y_offset = int((half_screen-fleet_vertical_space)//2)
        return x_offset,y_offset
            
    

    def calculate_fleet_size(self, alien_w, screen_w, alien_h, screen_h):
        """Calculates how many aliens can fit in the fleet

        Args:
            alien_w (int): Width of each alien
            screen_w (int): Width of the screen
            alien_h (int): Height of each alien
            screen_h (int): Height of the screen

        Returns:
            tuple(int): Both the width and the height in number of aliens
        """
        fleet_w = (screen_w//alien_w)
        fleet_h = ((screen_h / 2)// alien_h)
        
        if fleet_w % 2 == 0:
            fleet_w -= 1
        else:
            fleet_w -= 2
            
        if fleet_h % 2 == 0:
            fleet_h -= 1
        else:
            fleet_h -= 2
            
        return int(fleet_w), int(fleet_h)
            
    def _create_alien(self, current_x: int, current_y: int):
        """Creates an alien into the group

        Args:
            current_x (int): x value to place alien
            current_y (int): y value to place alien
        """
        new_alien = Alien(self, current_x, current_y)
        self.fleet.add(new_alien)
        
    def _check_fleet_edges(self):
        """Change direction of the fleet if an alien hits a wall
        """
        alien: Alien
        for alien in self.fleet:
            if alien.check_edges():
                self._drop_alien_fleet()
                self.fleet_direction *= -1
                break
            
    def _drop_alien_fleet(self):
        """Moves the fleet closer. Run when the fleet hits a wall.
        """
        for alien in self.fleet:
            alien.y += self.fleet_drop_speed
        
    def update_fleet(self):
        """Check if the fleet needs to change direction and moves the fleet
        """
        self._check_fleet_edges()
        self.fleet.update()
        
    def draw(self):
        """Draws the entire fleet by running each aliens draw function
        """
        alien: 'Alien'
        for alien in self.fleet:
            alien.draw_alien()
            
    def check_collisions(self, other_group):
        """Checks collisions between the fleet and a passed in group

        Args:
            other_group (Group): Passed in group to check against

        Returns:
            dict: Dictionary of what sprites did collide if any
        """
        return pygame.sprite.groupcollide(self.fleet, other_group, True, True)
            
    def check_fleet_bottom(self):
        """Checks if the fleet hits the bottom of the screen

        Returns:
            bool: True if an alien in the fleet hit the bottom, else False
        """
        alien: Alien
        for alien in self.fleet:
            if alien.rect.bottom >= self.settings.screen_h:
                return True
        return False
    
    def check_destroyed_status(self):
        """Checks if each alien was destroyed in the fleet

        Returns:
            bool: True if the fleet is empty, else False
        """
        return not self.fleet