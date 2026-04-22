import pygame.font
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Button:
    """Button class used to create new clickable buttons on the screen
    """
    
    def __init__(self, game: 'AlienInvasion', msg) -> None:
        self.game = game
        self.screen = game.screen
        self.boundaries = game.screen.get_rect()
        self.settings = game.settings
        self.font = pygame.font.Font(self.settings.font_file, 
            self.settings.button_font_size)
        self.rect = pygame.Rect(0,0, self.settings.button_w, self.settings.button_h)
        self.rect.center = self.boundaries.center
        self._prep_msg(msg)
        
    def _prep_msg(self,msg):
        """Prepares a message to be displayed

        Args:
            msg (str): The message to be displayed on the button
        """
        self.msg_image = self.font.render(msg, True, self.settings.text_color, None)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
        
    def draw(self):
        """Draws the button to the screen with the specified message
        """
        self.screen.fill(self.settings.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
        
    def check_clicked(self, mouse_pos):
        """Returns a boolean on if the mouse clicked the button or not

        Args:
            mouse_pos (Tuple[int,int]): The current position of the mouse

        Returns:
            bool: True if the mouse clicked within the button
        """
        return self.rect.collidepoint(mouse_pos)
        