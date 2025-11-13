import random

class RandomAgent:

    def __init__(self, player):
        """
        Initialize the RandomAgent

        
        """
        self.player = player

    def get_move(self, game):
        """
        Select a random legal move from the available options.
        
        Args:
            game: The current game state
        Returns:
            int: The chosen move position
        """
        legal_moves = game.get_legal_moves()
        return random.choice(legal_moves)