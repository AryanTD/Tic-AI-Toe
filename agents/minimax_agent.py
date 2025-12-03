class MinimaxAgent:
    
    def __init__(self, player):
        """
        Initialize the agent.
        
        Args:
            player (int): 1 for X, -1 for O
            
        Why we need player:
        - To know which side the agent is playing
        - Helps in evaluating board states
        """
        self.player = player    
        self.nodes_explored = 0


    def get_move(self, game):
        """
        Decide on the next move using the Minimax algorithm.
        
        Args:
            game (TicTacToe): Current game state
            
        Returns:
            int: Chosen board position (0-8)
            
        How it works:
        1. Try every legal move
        2. For each move, use minimax to calculate its score
        3. Pick the move with the highest score
        """

        best_score = float('-inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')


        for move in game.get_legal_moves():
            game_copy = game.copy()
            game_copy.make_move(move)

            score = self.minimax(game_copy, False, alpha, beta)

            if score > best_score:
                best_score = score
                best_move = move

            alpha = max(alpha, best_score)

        return best_move
    
    def minimax(self, game, is_maximizing, alpha, beta):
        """
        Minimax algorithm to evaluate board states.
        
        Args:
            game (TicTacToe): Current game state
            is_maximizing (bool): True if maximizing player, False if minimizing
            
        The algorithm:
        1. If game is over, return the score
        2. If maximizing: try all moves, return the MAX score
        3. If minimizing: try all moves, return the MIN score
        """
        self.nodes_explored += 1

        winner = game.check_winner()

        if winner == self.player:
            return 1  # Win
        elif winner == -self.player:
            return -1  # Loss
        elif game.is_game_over():
            return 0  # Draw
        
        if is_maximizing:
            max_score = float('-inf')
            for move in game.get_legal_moves():
                game_copy = game.copy()
                game_copy.make_move(move)
                score = self.minimax(game_copy, False, alpha, beta)
                max_score = max(max_score, score)

                alpha = max(alpha, max_score)
                if beta <= alpha:
                    break  # Beta cut-off
            return max_score
        else:
            min_score = float('inf')
            for move in game.get_legal_moves():
                game_copy = game.copy()
                game_copy.make_move(move)
                score = self.minimax(game_copy, True, alpha, beta)
                min_score = min(min_score, score)

                beta = min(beta, min_score)
                if beta <= alpha:
                    break  # Alpha cut-off
            return min_score