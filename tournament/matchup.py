from game.board import TicTacToe

class Matchup:
    """Handles a series of games between two agents."""
    
    def __init__(self, agent1, agent2, agent1_name, agent2_name, games_per_side=100):
        self.agent1 = agent1
        self.agent2 = agent2
        self.agent1_name = agent1_name
        self.agent2_name = agent2_name
        self.games_per_side = games_per_side
        
        self.results = {
            'agent1_wins': 0,
            'agent2_wins': 0,
            'draws': 0,
            'agent1_as_x_wins': 0,
            'agent1_as_o_wins': 0,
            'agent2_as_x_wins': 0,
            'agent2_as_o_wins': 0,
            'draws_as_x': 0,
            'draws_as_o': 0
        }
    
    def play_game(self, x_agent, o_agent):
        """Play a single game with proper player assignment."""
        game = TicTacToe()
        
        # CRITICAL: Set player attributes
        x_agent.player = 1
        o_agent.player = -1
        
        while not game.is_game_over():
            if game.current_player == 1:
                move = x_agent.get_move(game)
            else:
                move = o_agent.get_move(game)
            game.make_move(move)
        
        return game.check_winner()
    
    def run(self):
        """Run complete matchup."""
        # Agent 1 as X, Agent 2 as O
        for _ in range(self.games_per_side):
            winner = self.play_game(self.agent1, self.agent2)
            
            if winner == 1:
                self.results['agent1_wins'] += 1
                self.results['agent1_as_x_wins'] += 1
            elif winner == -1:
                self.results['agent2_wins'] += 1
                self.results['agent2_as_o_wins'] += 1
            else:
                self.results['draws'] += 1
                self.results['draws_as_x'] += 1
        
        # Agent 2 as X, Agent 1 as O
        for _ in range(self.games_per_side):
            winner = self.play_game(self.agent2, self.agent1)
            
            if winner == 1:
                self.results['agent2_wins'] += 1
                self.results['agent2_as_x_wins'] += 1
            elif winner == -1:
                self.results['agent1_wins'] += 1
                self.results['agent1_as_o_wins'] += 1
            else:
                self.results['draws'] += 1
                self.results['draws_as_o'] += 1
        
        return self.results
    
    def get_summary(self):
        """Get human-readable summary."""
        total_games = self.games_per_side * 2
        
        summary = f"\n{'='*60}\n"
        summary += f"MATCHUP: {self.agent1_name} vs {self.agent2_name}\n"
        summary += f"{'='*60}\n"
        summary += f"\nOverall ({total_games} games):\n"
        summary += f"  {self.agent1_name} wins: {self.results['agent1_wins']:3d} ({self.results['agent1_wins']/total_games*100:5.1f}%)\n"
        summary += f"  {self.agent2_name} wins: {self.results['agent2_wins']:3d} ({self.results['agent2_wins']/total_games*100:5.1f}%)\n"
        summary += f"  Draws:           {self.results['draws']:3d} ({self.results['draws']/total_games*100:5.1f}%)\n"
        
        return summary