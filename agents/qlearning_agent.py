import random
import pickle

class QLearningAgent:
    """
    An agent that learns through self-play using Q-Learning.
    
    Q-Learning is a reinforcement learning algorithm where the agent:
    1. Maintains a Q-table: Q(state, action) = expected future reward
    2. Updates Q-values based on outcomes (wins/losses/draws)
    3. Improves through experience (trial and error)
    """

    def __init__(self, player, learning_rate=0.1, discount_factor=0.9, epsilon=0.1):
        self.player = player
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon

        self.q_table = {}  # Key: (state, action), Value: Q-value
        self.history = []  # To store state-action pairs for learning



    def get_move(self, game, training=False):
        """
        Choose a move using epsilon-greedy strategy.
        
        Args:
            game (TicTacToe): Current game state
            training (bool): If True, uses epsilon for exploration
            
        Returns:
            int: Position to play (0-8)
            
        Strategy:
        - During training: ε% random (explore), (1-ε)% best Q-value (exploit)
        - During play: Always pick best Q-value (pure exploitation)
        """

        state = self.transform_state(game.board)
        legal_moves = game.get_legal_moves()


        # Exploration vs Exploitation
        if training and random.random() < self.epsilon:
            move = random.choice(legal_moves)
        else:
            move = self.get_best_move(state, legal_moves)

        if training:
            self.history.append((state, move))

        return move
    
    def get_best_move(self, state, legal_moves):
        """
        Get the best move based on current Q-values.
        
        Args:
            state (tuple): Current board state
            legal_moves (list): List of legal moves 
        Returns:
            int: Best move based on Q-values
        """

        if state not in self.q_table:
            return random.choice(legal_moves)
        
        best_value = float('-inf')
        best_moves = []

        for move in legal_moves:
            q_value = self.q_table[state].get(move, 0)

            if q_value > best_value:
                best_value = q_value
                best_moves = [move]
            elif q_value == best_value:
                best_moves.append(move)

        return random.choice(best_moves)
    
    def learn(self, reward):
        """
        Update Q-values for all moves made during the game.
        
        Args:
            reward (int): Final reward (+1 win, -1 loss, 0 draw)
            
        How it works:
        1. Start from the last move (most recent)
        2. Update its Q-value based on immediate reward
        3. Work backwards, each move gets credit for future value
        4. This is called "temporal difference learning"
        """

        for i in range(len(self.history)-1, -1, -1):
            state, action = self.history[i]

            if state not in self.q_table:
                self.q_table[state] = {}
            if action not in self.q_table[state]:
                self.q_table[state][action] = 0

            current_q = self.q_table[state][action]

            if i == len(self.history) - 1:
                target = reward
            else:
                next_state, next_action = self.history[i + 1]
                
                if next_state in self.q_table and next_action in self.q_table[next_state]:
                    next_q = self.q_table[next_state][next_action]
                else:
                    next_q = 0

                target = reward + self.discount_factor * next_q

            self.q_table[state][action] = current_q + self.learning_rate * (target - current_q)

            reward = 0  # Only the final move gets the actual reward
        self.history = []  # Clear history after learning

    def reset_history(self):
        """Clear the history of state-action pairs."""
        self.history = []

    def save_q_table(self, filename):
        """Save the Q-table to a file."""
        with open(filename, 'wb') as f:
            pickle.dump(self.q_table, f)
        print(f"Q-table saved to {filename}")


    def load_q_table(self, filename):
        """Load the Q-table from a file."""
        with open(filename, 'rb') as f:
            self.q_table = pickle.load(f)
        print(f"Q-table loaded from {filename}")
        print(f"Q-table has {len(self.q_table)} states.")

    def transform_state(self, board):
        """
        Transform board to agent's perspective.
        
        Agent always sees:
        - Its own pieces as +1
        - Opponent's pieces as -1
        - Empty as 0
        
        This allows a single Q-table to work for both X and O.
        """
        if self.player == 1:
            # Playing as X - board is already in correct perspective
            return tuple(board)
        else:
            # Playing as O - flip the perspective
            # Swap 1 and -1
            transformed = [-cell if cell != 0 else 0 for cell in board]
            return tuple(transformed)