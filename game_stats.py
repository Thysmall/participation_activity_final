import json
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
        self.init_saved_scores()
        self.reset_stats()
        
    def init_saved_scores(self):
        """Either creates a blank score sheet or loads an existing one
        """
        self.path = self.settings.scores_file
        if self.path.exists() and self.path.stat.__sizeof__() > 20:
            contents = self.path.read_text()
            scores = json.loads(contents)
            self.hi_score = scores.get('hi_score', 0)
        else:
            self.hi_score = 0
            self.save_scores()
            
    def save_scores(self):
        """Saves the current hi score to a score sheet
        """
        scores = {
            'hi_score': self.hi_score
        }
        contents = json.dumps(scores, indent = 4)
        try:
            self.path.write_text(contents)
        except FileNotFoundError as e:
            print(f'File Not Found: {e}')

    def reset_stats(self):
        """Resets the current stats like score, level, and number of lives
        """
        self.ships_left = self.settings.starting_ship_count
        self.score = 0
        self.level = 1
        
    def update(self, collisions):
        """Runs update functions for each score type

        Args:
            collisions (Dict[Unknown, List[Unknown]]): A list of collissions
        """
        # update score
        self._update_score(collisions)
        
        # update max_score
        self._update_max_score()
        
        # update hi_score
        self._update_hi_score()

    def _update_max_score(self):
        """Sets the max score to the current score if the score is higher
        """
        if self.score > self.max_score:
            self.max_score = self.score
        # print(f'Max: {self.max_score}')
        
    def _update_hi_score(self):
        """Updates the hi score to the score if the score is higher
        """
        if self.score > self.hi_score:
            self.hi_score = self.score
        # print(f'Max: {self.hi_score}')

    def _update_score(self, collisions):
        """Updates the score according to the number of collisions passed in

        Args:
            collisions (Dict[Unknown, List[Unknown]]): A list of collissions
        """
        for alien in collisions.values():
            self.score += self.settings.alien_points
        # print(f'Score: {self.score}')
        
    def update_level(self):
        self.level += 1
        # print(self.level)
    
        
        