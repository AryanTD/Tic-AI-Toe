class HeuristicAgent:
    """
    An agent that uses strategic rules (heuristics) to play.
    
    This encodes human knowledge about good tic-tac-toe strategy.
    It's much stronger than Random, but not perfect like Minimax.
    """

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

        self.winning_lines = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]              # diagonals
        ]

    def find_winning_move(self, board, player):
        for line in self.winning_lines:
            values = [board[line[0]], board[line[1]], board[line[2]]]
            player_count = values.count(player)
            empty_count = values.count(0)

            if player_count == 2 and empty_count == 1:
                for pos in line:
                    if board[pos] == 0:
                        return pos
                    
        return None
    
    def get_move(self, game):
        """
        Decide on the next move using heuristics.
        
        Args:
            game (TicTacToe): Current game state
            
        Returns:
            int: Chosen board position (0-8)
            
         Strategy Priority (check in order):
            1. Win if possible
            2. Block opponent's winning move
            3. Take center if available
            4. Take a corner if available
            5. Take any remaining position
        """

        board = game.board
        
        winning_move = self.find_winning_move(board, self.player)
        if winning_move is not None:
            return winning_move
        
        opponent = -self.player
        blocking_move = self.find_winning_move(board, opponent)
        if blocking_move is not None:
            return blocking_move
        
        if board[4] == 0:
            return 4
        
        corners = [0, 2, 6, 8]
        for corner in corners:
            if board[corner] == 0:
                return corner
            
        edges = [1, 3, 5, 7]
        for edge in edges:
            if board[edge] == 0:
                return edge
            
        return game.get_legal_moves()[0]