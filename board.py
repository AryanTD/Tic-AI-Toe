class TicTacToe:
    """
    Tic-tac-toe game engine using 1D board representation.
    
    Board positions:
    0 | 1 | 2
    ---------
    3 | 4 | 5
    ---------
    6 | 7 | 8
    """

    def __init__(self):
        """
        Initialize a new game.
        
        Why we need each attribute:
        - board: The actual game state (9 positions)
        - current_player: Whose turn is it? (1 for X, -1 for O)
        """
        self.board = [0] * 9  # 0 for empty, 1 for X, -1 for O
        self.current_player = 1  # X starts first


    def make_move(self, position):
        """
        Place the current player's mark at the given position.
        
        Args:
            position (int): Board index (0-8)
            
        Returns:
            bool: True if move was legal and made, False otherwise
            
        Why this returns bool:
        - AI agents need to know if their move was valid
        - Prevents illegal moves from breaking game state
        """

        #Check if move is legal
        if position < 0 or position > 8:
            return False
        
        #Check if position is already taken
        if self.board[position] != 0:
            return False
        
        #Make the move
        self.board[position] = self.current_player
        self.current_player *= -1  # Switch player

        return True
    
    def check_winner(self):
        """
        Check if there's a winner.
        
        Returns:
            int: 1 if X wins, -1 if O wins, 0 if no winner yet
        """

        winning_lines = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]

        for line in winning_lines:
            line_sum = self.board[line[0]] + self.board[line[1]] + self.board[line[2]]
            if line_sum == 3:
                return 1  # X wins
            elif line_sum == -3:
                return -1  # O wins
            
        return 0  # No winner yet
    
    def is_game_over(self):
        """
        Check if the game is over (win or draw).
        
        Returns:
            bool: True if game is over, False otherwise
        """

        if self.check_winner() != 0:
            return True
        
        if 0 not in self.board:
            return True  # Draw
        
        return False
    
    def get_legal_moves(self):
        """
        Get a list of legal moves.
        
        Returns:
            list: List of indices (0-8) that are empty
        """

        return [i for i in range(9) if self.board[i] == 0]
    
    def copy(self):
        """
        Create a copy of the current game state.
        
        Returns:
            TicTacToe: A new instance with the same state
        """

        new_game = TicTacToe()
        new_game.board = self.board.copy()
        new_game.current_player = self.current_player
        return new_game
    
    def display(self):
        """
        Print the current board state.
        """

        symbols = {1: 'X', -1: 'O', 0: ' '}
        print("\n")
        for row in range(3):
            start = row * 3
            cells = []
            for i in range(3):
                position = start + i
                value = self.board[position]
                cells.append(symbols[value])
            print(f"{cells[0]} | {cells[1]} | {cells[2]}")
            if row < 2:
                print("---------")
        print("\n")
