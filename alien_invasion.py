import sys
import pygame
from settings import Settings
from ship import Ship
from arsenal import Arsenal
from alien_fleet import AlienFleet
from game_stats import GameStats
from time import sleep

class AlienInvasion:
    """Main run file that manages the game and its functions
    """
    def __init__(self) -> None:
        pygame.init()
        self.settings = Settings()
        self.game_stats = GameStats(self.settings.starting_ship_count)
        
        #Create window
        self.screen = pygame.display.set_mode(
            (self.settings.screen_w,self.settings.screen_h)
            )
        pygame.display.set_caption(self.settings.name)
        
        #Create background
        self.bg = pygame.image.load(self.settings.bg_file)
        self.bg = pygame.transform.scale(self.bg,
            (self.settings.screen_w,self.settings.screen_h)
            )
        
        #Initialize running and running rate
        self.running = True
        self.clock = pygame.time.Clock()
        
        #Create sound effects
        pygame.mixer.init()
        self.laser_sound = pygame.mixer.Sound(self.settings.laser_sound)
        self.laser_sound.set_volume(0.7)
        self.impact_sound = pygame.mixer.Sound(self.settings.impact_sound)
        self.impact_sound.set_volume(0.7)
        
        #Create ship
        self.ship = Ship(self, Arsenal(self))
        self.alien_fleet = AlienFleet(self)
        self.alien_fleet.create_fleet()
        self.game_active = True
        
    def run_game(self):
        """Runs functions of game while playing
        """
        while self.running:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self.alien_fleet.update_fleet()
                self._check_collisions()
            self._update_screen()
            self.clock.tick(self.settings.FPS)

    def _check_collisions(self):
        """Runs different functions based on different collissions being checked
        """
        # check collisisons for ship
        if self.ship.check_collisions(self.alien_fleet.fleet):
            self._check_game_status()
            # subtract one life if possible
        
        # check collisisons for aliens and bottom of screen
        if self.alien_fleet.check_fleet_bottom():
            self._check_game_status()
        
        # check collisions of projectiles and aliens
        collissions = self.alien_fleet.check_collisions(self.ship.arsenal.arsenal)
        if collissions:
            self.impact_sound.play()
            self.impact_sound.fadeout(500)
        
        # check if fleet is destroyed
        if self.alien_fleet.check_destroyed_status():
            self._reset_level()     
            
    def _check_game_status(self):
        """Changes lives and resets or stops game when run
        """
        if self.game_stats.ships_left > 0:
            self.game_stats.ships_left -= 1
            self._reset_level()
            sleep(0.5)
        else:
            self.game_active = False
            
        
        
    def _reset_level(self):
        """Removes all sprites and creates a new fleet
        """
        self.ship.arsenal.arsenal.empty()
        self.alien_fleet.fleet.empty()
        self.alien_fleet.create_fleet()

    def _update_screen(self):
        """Draws background and other file draw functions then displays
        """
        self.screen.blit(self.bg,(0,0))
        self.ship.draw()
        self.alien_fleet.draw()
        pygame.display.flip()

    def _check_events(self):
        """Checks for events and runs event functions accordingly
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
    
    def _check_keyup_events(self,event):
        """Inputs keyup events and acts based on the key pressed

        Args:
            event (KEYUP): Used to get key that activated event
        """
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
    
    def _check_keydown_events(self,event):
        """Inputs KEYDOWN events and acts based on the key pressed

        Args:
            event (KEYDOWN): Used to get key that activated event
        """
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            if self.ship.fire():
                self.laser_sound.play()
                self.laser_sound.fadeout(250)
                
        elif event.key == pygame.K_q:
            self.running = False
            pygame.quit()
            sys.exit()

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
