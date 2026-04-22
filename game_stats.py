from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class GameStats():
    """Contains volatile stats
    """
    def __init__(self, game: 'AlienInvasion'):
        self.game = game
        self.settings = game.settings
        self.max_score = 0
        self.reset_stats()

    def reset_stats(self):
        self.ships_left = self.settings.starting_ship_count
        self.score = 0
        self.level = 1
        
    def update(self, collisions):
        # update score
        self._update_score(collisions)
        
        # update max_score
        self._update_max_score()
        
        # update hi_score

    def _update_max_score(self):
        if self.score > self.max_score:
            self.max_score = self.score
        # print(f'Max: {self.max_score}')

    def _update_score(self, collisions):
        for alien in collisions.values():
            self.score += self.settings.alien_points
        # print(f'Score: {self.score}')
        
    def update_level(self):
        self.level += 1
        print(self.level)
    
        
        