import random
import math

class MCTSNode:
    """A node in the MCTS search tree."""
    
    def __init__(self, game, parent=None, move=None):
        self.game = game.copy()
        self.parent = parent
        self.move = move
        self.visits = 0
        self.wins = 0  # Wins for the PLAYER WHO JUST MOVED to create this node
        self.children = []
        self.untried_moves = game.get_legal_moves()
    
    def is_fully_expanded(self):
        return len(self.untried_moves) == 0
    
    def is_terminal(self):
        return self.game.is_game_over()
    
    def best_child(self, exploration_weight=1.414):
        """
        Select child with highest UCB1.
        IMPORTANT: We want children where OPPONENT did poorly (we did well).
        """
        choices_weights = []
        for child in self.children:
            # Child.wins is from opponent's perspective
            # We want LOW child wins (opponent lost = we won)
            # So we use (visits - wins) to get OUR wins
            our_wins = child.visits - child.wins
            exploitation = our_wins / child.visits
            exploration = exploration_weight * math.sqrt(
                math.log(self.visits) / child.visits
            )
            ucb1_score = exploitation + exploration
            choices_weights.append(ucb1_score)
        return self.children[choices_weights.index(max(choices_weights))]
    
    def expand(self):
        move = self.untried_moves.pop()
        child_game = self.game.copy()
        child_game.make_move(move)
        child_node = MCTSNode(child_game, parent=self, move=move)
        self.children.append(child_node)
        return child_node
    
    def simulate(self):
        """
        Simulate random game.
        Returns 1 if CURRENT player wins, 0 for draw, -1 if current player loses.
        """
        simulation_game = self.game.copy()
        current_player = simulation_game.current_player
        
        while not simulation_game.is_game_over():
            legal_moves = simulation_game.get_legal_moves()
            move = random.choice(legal_moves)
            simulation_game.make_move(move)
        
        winner = simulation_game.check_winner()
        
        if winner == current_player:
            return 1
        elif winner == -current_player:
            return -1
        else:
            return 0
    
    def backpropagate(self, result):
        """
        Update tree with result.
        Result is from the perspective of the player at the CHILD node.
        """
        self.visits += 1
        
        # Positive result means the player who moved here won
        if result == 1:
            self.wins += 1
        elif result == 0:
            self.wins += 0.5
        
        # Propagate to parent with FLIPPED result
        # (parent's opponent won = parent lost)
        if self.parent:
            self.parent.backpropagate(-result)


class MCTSAgent:
    """Agent that uses Monte Carlo Tree Search."""
    
    def __init__(self, player, num_simulations=1000):
        self.player = player
        self.num_simulations = num_simulations
    
    def get_move(self, game):
        legal_moves = game.get_legal_moves()
        
        if len(legal_moves) == 1:
            return legal_moves[0]
        
        if game.is_game_over():
            return legal_moves[0] if legal_moves else 0
        
        root = MCTSNode(game)
        
        for _ in range(self.num_simulations):
            node = root
            
            # Selection
            while not node.is_terminal() and node.is_fully_expanded():
                node = node.best_child()
            
            # Expansion
            if not node.is_terminal() and not node.is_fully_expanded():
                node = node.expand()
            
            # Simulation
            result = node.simulate()
            
            # Backpropagation
            node.backpropagate(result)
        
        if not root.children:
            return random.choice(legal_moves)
        
        # Pick most visited child
        best_child = max(root.children, key=lambda c: c.visits)
        return best_child.move