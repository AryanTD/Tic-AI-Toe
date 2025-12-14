from agents.random_agent import RandomAgent
from agents.heuristic_agent import HeuristicAgent
from agents.minimax_agent import MinimaxAgent
from agents.qlearning_agent import QLearningAgent
from agents.mcts_agent import MCTSAgent
from tournament.matchup import Matchup
import time

class Tournament:
    """
    Runs a round-robin tournament with all agents.
    """
    
    def __init__(self, games_per_side=100):
        """
        Args:
            games_per_side (int): Games per agent per side (X and O)
        """
        self.games_per_side = games_per_side
        self.agents = {}
        self.results = {}
        self.standings = {}
        
    def setup_agents(self):
        """Initialize all agents."""
        print("Setting up agents...")
        
        # Random
        self.agents['Random'] = RandomAgent(player=1)
        
        # Heuristic
        self.agents['Heuristic'] = HeuristicAgent(player=1)
        
        # Minimax
        self.agents['Minimax'] = MinimaxAgent(player=1)
        
        # Q-Learning (load trained model)
        qlearning = QLearningAgent(player=1)
        qlearning.load_q_table("q_table.pkl")
        qlearning.epsilon = 0  # No exploration
        self.agents['Q-Learning'] = qlearning
        
        # MCTS
        self.agents['MCTS'] = MCTSAgent(player=1, num_simulations=1000)
        
        print(f"✓ Loaded {len(self.agents)} agents")
        
        # Initialize standings
        for name in self.agents:
            self.standings[name] = {
                'points': 0,
                'wins': 0,
                'draws': 0,
                'losses': 0,
                'games': 0
            }
    
    def run(self):
        """
        Run complete round-robin tournament.
        """
        agent_names = list(self.agents.keys())
        total_matchups = 0
        for i in range(len(agent_names)):
            for j in range(len(agent_names)):
                if i != j:  # <-- Only count when agents are different
                    total_matchups += 1
        
        print(f"\n{'='*60}")
        print(f"STARTING TOURNAMENT")
        print(f"{'='*60}")
        print(f"Format: Round-robin (everyone vs everyone)")
        print(f"Games per matchup: {self.games_per_side * 2}")
        print(f"Total matchups: {total_matchups}")
        print(f"Total games: {total_matchups * self.games_per_side * 2}")
        print(f"{'='*60}\n")
        
        matchup_count = 0
        start_time = time.time()
        
        # Play each agent against each other (including self)
        for i, name1 in enumerate(agent_names):
            for j, name2 in enumerate(agent_names):

                if name1 == name2:
                    continue  # Skip self-matchups

                matchup_count += 1
                
                print(f"[{matchup_count}/{total_matchups}] {name1} vs {name2}...", end=" ", flush=True)
                
                matchup_start = time.time()
                
                # Create matchup
                matchup = Matchup(
                    self.agents[name1],
                    self.agents[name2],
                    name1,
                    name2,
                    self.games_per_side
                )
                
                # Run matchup
                results = matchup.run()
                
                matchup_time = time.time() - matchup_start
                
                # Store detailed results
                self.results[f"{name1}_vs_{name2}"] = {
                    'matchup': matchup,
                    'results': results
                }
                
                # Update standings
                total_games = self.games_per_side * 2
                
                # Agent 1 points: 2 per win, 1 per draw
                agent1_points = results['agent1_wins'] * 2 + results['draws'] * 1
                agent2_points = results['agent2_wins'] * 2 + results['draws'] * 1
                
                self.standings[name1]['points'] += agent1_points
                self.standings[name1]['wins'] += results['agent1_wins']
                self.standings[name1]['draws'] += results['draws']
                self.standings[name1]['losses'] += results['agent2_wins']
                self.standings[name1]['games'] += total_games
                
                self.standings[name2]['points'] += agent2_points
                self.standings[name2]['wins'] += results['agent2_wins']
                self.standings[name2]['draws'] += results['draws']
                self.standings[name2]['losses'] += results['agent1_wins']
                self.standings[name2]['games'] += total_games
                
                print(f"Done ({matchup_time:.2f}s)")
        
        elapsed = time.time() - start_time
        print(f"\n{'='*60}")
        print(f"TOURNAMENT COMPLETE!")
        print(f"Total time: {elapsed:.1f}s ({elapsed/60:.1f} minutes)")
        print(f"{'='*60}\n")
    
    def print_standings(self):
        """Print final standings table."""
        # Sort by losses (ascending), then by wins (descending) as tiebreaker
        sorted_standings = sorted(
            self.standings.items(),
            key=lambda x: (x[1]['losses'], -x[1]['wins'])
        )
        
        print("\n" + "="*80)
        print("FINAL STANDINGS".center(80))
        print("="*80)
        print(f"{'Rank':<6}{'Agent':<15}{'Points':<10}{'W':<8}{'D':<8}{'L':<8}{'Games':<8}{'Win%':<8}")
        print("-"*80)
        
        for rank, (name, stats) in enumerate(sorted_standings, 1):
            win_pct = stats['wins'] / stats['games'] * 100 if stats['games'] > 0 else 0
            max_points = stats['games'] * 2
            
            print(f"{rank:<6}{name:<15}{stats['points']}/{max_points:<8}{stats['wins']:<8}"
                f"{stats['draws']:<8}{stats['losses']:<8}{stats['games']:<8}{win_pct:>6.1f}%")
        
        print("="*80)
        print("Scoring: Win = 2 points, Draw = 1 point, Loss = 0 points")
        print("="*80 + "\n")
    
    def print_head_to_head_matrix(self):
        """Print head-to-head win rate matrix."""
        agent_names = list(self.agents.keys())
        
        print("\n" + "="*80)
        print("HEAD-TO-HEAD WIN RATES (%)".center(80))
        print("="*80)
        
        # Header
        header = f"{'':15}"
        for name in agent_names:
            header += f"{name[:10]:>12}"
        print(header)
        print("-"*80)
        
        # Each row
        for name1 in agent_names:
            row = f"{name1:<15}"
            for name2 in agent_names:
                if name1 == name2:  # <-- ADD THIS CHECK
                    row += f"{'---':>12}"
                    continue  # <-- SKIP to next agent
                key = f"{name1}_vs_{name2}"
                results = self.results[key]['results']
                total = self.games_per_side * 2
                win_rate = results['agent1_wins'] / total * 100
                
                if name1 == name2:
                    row += f"{'---':>12}"
                else:
                    row += f"{win_rate:>11.1f}%"
            print(row)
        
        print("="*80 + "\n")
    
    def save_detailed_results(self, filename="tournament_results.txt"):
        """Save all detailed matchup results to file."""
        with open(filename, 'w') as f:
            f.write("="*80 + "\n")
            f.write("TIC-TAC-TOE AI TOURNAMENT - DETAILED RESULTS\n")
            f.write("="*80 + "\n\n")
            
            for key, data in self.results.items():
                f.write(data['matchup'].get_summary())
                f.write("\n")
        
        print(f"✓ Detailed results saved to {filename}")