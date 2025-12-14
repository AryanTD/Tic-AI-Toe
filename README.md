# Multi-Agent Tic-Tac-Toe Tournament

Comparing five AI algorithms through competitive gameplay to understand how different approaches to intelligence perform.

## Research Question

How do different AI agents compare in performance, learning efficiency, and computational cost when competing in a tournament of tic-tac-toe?

## What This Project Does

Five AI agents play tic-tac-toe against each other in a complete round-robin tournament:

- Random - Pure chance, no strategy (baseline)
- Heuristic - Rule-based, human-like decisions
- Minimax (Alpha-Beta) - Perfect play through exhaustive search
- Q-Learning - Learns strategy through 75,000 self-play games
- MCTS - Statistical sampling of possible futures

Each pair plays 200 games (100 as X, 100 as O) for fairness.
Total: 4,000 games

## Why Tic-Tac-Toe?

Although tic-tac-toe is a simple game, it's ideal for learning how different AI algorithms operate. It allows us to compare classical AI techniques (Minimax, Heuristic) with modern approaches (Q-Learning, MCTS) in a controlled environment.

## Quick Start

```bash
# Clone the repository
git clone https://github.com/AryanTD/Tic-AI-Toe.git
cd Tic-AI-TAC-Toe

# Run the tournament (requires Python 3.x and NumPy)
python run_tournament.py
```

## Key Findings

Finding #1: Perfect Play = Draws

- Minimax vs Heuristic: 100% draws
- When both agents play near-optimally, winning becomes impossible
- Intelligence doesn't result in more wins; it results in fewer losses

Finding #2: Simple Can Equal Smart

- Heuristic (basic rules) matched Minimax (exhaustive search) perfectly
- Heuristic ran 50x faster (0.001s vs 0.05s per move)
- Sometimes the simplest solution is the smartest solution

Finding #3: Learning Needs More Than Volume

- Q-Learning never beat Minimax, Heuristic, or MCTS
- 75,000 training games weren't enough without better reward shaping
- Learned effective defensive play (50% draw rate) but couldn't learn offensive plays

Finding #4: Three Performance Tiers Emerged

- Tier 1 (Minimax, Heuristic): ~35% win rate, nearly perfect (0-1 losses total)
- Tier 2 (MCTS): ~26% win rate, very strong (4 losses total)
- Tier 3 (Q-Learning): ~23% win rate, competent but flawed (434 losses)

Finding #5: MCTS vs Q-Learning

- MCTS achieved 99.8% unbeaten rate with 1000+ simulations per move
- MCTS won 29 games, Q-Learning won only 1
- Fresh thinking per move beats imperfect pre-trained patterns

Finding #6: Random's Lucky Win

- Random beat Heuristic 1 time out of 400 games
- Created a fork (two winning threats) by pure luck
- Minimax prevents forks through exhaustive search, so Random never won

## The Agents

# 1. Random Agent

Strategy: Pick any legal move randomly  
Intelligence: None  
Purpose: Baseline for comparison

# 2. Heuristic Agent

Strategy: Follow priority rules:

1. Win if possible
2. Block opponent's winning move
3. Take center if available
4. Take corner
5. Take any remaining position

Intelligence: Rule-based decision making  
Advantage: Fast, human-like, no planning ahead required

# 3. Minimax Agent (with Alpha-Beta Pruning)

Strategy: Explore every possible game outcome

- Recursively builds game tree
- Assumes opponent plays optimally
- Chooses move guaranteeing best outcome
- Alpha-Beta pruning eliminates ~96% of unnecessary branches

Intelligence: Mathematically optimal  
Result: Unbeatable in tic-tac-toe

# 4. Q-Learning Agent

Strategy: Learn through experience

- Played 75,000 games against itself
- Started with zero knowledge
- Built Q-table: state → action → expected value
- Balances exploration vs exploitation

Intelligence: Reinforcement learning  
Challenge: Needs better training structure

# 5. Monte Carlo Tree Search (MCTS) Agent

Strategy: Statistical sampling of possible futures

- Simulates 1000+ random games per move
- Tracks win/loss/draw rates
- Chooses move with highest success rate
- Uses UCB1 formula to balance exploration vs exploitation

Intelligence: Simulation-based decision making  
Trade-off: Most computationally expensive during gameplay

## Tournament Design

- Format: Round-robin (every agent plays every other agent)
- Games per matchup: 200 (100 as X, 100 as O)
- Why alternate positions? First player (X) has a slight advantage
- Total games: 4,000 across all matchups
- Metrics tracked: Wins, losses, draws, performance by position

## Project Structure

```
Tic-AI-Toe/
├── README.md
├── DOCUMENTATION.md
├── main.py
├── agents/          # All five AI implementations
├── game/            # Board and game logic
├── tournament/      # Tournament orchestration
├── results/         # Tournament data and visualizations
└── presentation/    # Project slides
```

## Technologies Used

- Python 3.14
- NumPy (for Q-Learning)
- Standard library (no heavy frameworks)

## Results

See `results/tournament_results.csv` for complete data.

## Authors

Built for CSCI-6660: Introduction to AI  
Aryan Tandon, Bipin Kumar Thollikonda

## License

MIT License - Feel free to use this for learning!
