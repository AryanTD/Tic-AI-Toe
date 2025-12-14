# AI Tic-Tac-Toe Tournament - Technical Documentation

Complete guide to understanding and using this project.

---

## Table of Contents

1. [Agent Implementations](#agent-implementations)
2. [Tournament System](#tournament-system)
3. [Results & Analysis](#results--analysis)
4. [Usage Guide](#usage-guide)
5. [Implementation Details](#implementation-details)

---

## Agent Implementations

### 1. Random Agent

**Algorithm Type:** Baseline (No Intelligence)

**How It Works:**

- Gets list of all legal moves (empty positions on board)
- Randomly selects one using `random.choice()`
- No strategy, planning, or learning

**Code Concept:**

```python
available_moves = [i for i in range(9) if board[i] == 0]
return random.choice(available_moves)
```

**Performance:**

- Win Rate: ~10% (only against itself)
- Loses to all intelligent agents
- Serves as baseline to measure other agents against

**Why Include It?**
Shows the minimum performance level. Any AI algorithm should easily beat random play.

---

### 2. Heuristic Agent

**Algorithm Type:** Rule-Based AI

**How It Works:**
Follows a priority list of rules in order:

1. **Win if possible** - Check if you can win in one move
2. **Block opponent** - Check if opponent can win, block them
3. **Take center** - Position 4 is strategically valuable
4. **Take corner** - Positions 0, 2, 6, 8 create more winning opportunities
5. **Take any edge** - Positions 1, 3, 5, 7 as last resort

**Code Concept:**

```python
# Check for immediate win
if can_win(board, player):
    return winning_move

# Block opponent's win
if can_win(board, opponent):
    return blocking_move

# Take center
if board[4] == 0:
    return 4

# Take corner
corners = [0, 2, 6, 8]
for corner in corners:
    if board[corner] == 0:
        return corner

# Take any remaining move
return first_available_move
```

**Performance:**

- Win Rate: ~35%
- Never lost to Minimax (100% draw rate)
- Speed: 0.001s per move (50x faster than Minimax)

**Key Insight:**
Simple rules can match sophisticated algorithms. The heuristic captures human intuition about tic-tac-toe without any search or calculation.

---

### 3. Minimax Agent (with Alpha-Beta Pruning)

**Algorithm Type:** Exhaustive Search (Game Theory)

**How It Works:**

Minimax explores every possible game outcome:

1. **For each legal move**, recursively simulate the game to completion
2. **Assume opponent plays optimally** at every step
3. **Score terminal states:**
   - Win = +10
   - Loss = -10
   - Draw = 0
4. **Maximize your score, minimize opponent's score**
5. **Choose the move with the best guaranteed outcome**

**Alpha-Beta Pruning:**

- Eliminates branches that cannot affect the final decision
- Reduces ~96% of unnecessary calculations
- Makes Minimax practical for real-time play

**Code Concept:**

```python
def minimax(board, depth, is_maximizing, alpha, beta):
    # Base case: game over
    if game_over(board):
        return evaluate(board)

    if is_maximizing:
        max_eval = -infinity
        for move in legal_moves:
            eval = minimax(make_move(board, move), depth+1, False, alpha, beta)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Prune this branch
        return max_eval
    else:
        min_eval = +infinity
        for move in legal_moves:
            eval = minimax(make_move(board, move), depth+1, True, alpha, beta)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Prune this branch
        return min_eval
```

**Performance:**

- Win Rate: ~35%
- Losses: 0 (mathematically unbeatable)
- Speed: 0.05s per move
- Draw rate vs Heuristic: 100%

**Why It's Perfect:**
Minimax guarantees optimal play by considering every possible future. In tic-tac-toe, perfect play from both sides always results in a draw.

---

### 4. Q-Learning Agent

**Algorithm Type:** Reinforcement Learning

**How It Works:**

Q-Learning learns through experience by building a Q-table:

**Q(state, action) = expected future reward**

**Training Process (75,000 self-play games):**

1. **Start with empty Q-table** (no knowledge)
2. **Play a move** (either explore new moves or exploit known good moves)
3. **Observe the result** (win/loss/draw)
4. **Update Q-value** using the formula:

```
Q(s,a) ← Q(s,a) + α[reward + γ·max(Q(s',a')) - Q(s,a)]

Where:
- α (alpha) = learning rate (0.1)
- γ (gamma) = discount factor (0.9)
- reward = +1 for win, -1 for loss, 0 for draw
- s' = next state after action
```

5. **Repeat thousands of times** to refine the Q-table

**Exploration vs Exploitation:**

- **Exploration:** Try new moves to discover better strategies (ε = 0.1)
- **Exploitation:** Use known good moves from Q-table (1 - ε = 0.9)

**Code Concept:**

```python
# Training
for episode in range(75000):
    state = initial_state
    while not game_over:
        # Epsilon-greedy action selection
        if random() < epsilon:
            action = random_move()  # Explore
        else:
            action = best_q_value_move()  # Exploit

        next_state, reward = take_action(action)

        # Q-Learning update
        old_q = Q[state][action]
        future_q = max(Q[next_state])
        Q[state][action] = old_q + alpha * (reward + gamma * future_q - old_q)

        state = next_state

# Playing (after training)
def get_move(board):
    state = board_to_state(board)
    return action_with_max_q_value(state)
```

**Performance:**

- Win Rate: ~23%
- Never beat Minimax, Heuristic, or MCTS
- Learned defensive play (50% draw rate vs top agents)
- Couldn't learn offensive strategies

**Why It Struggled:**

- 75,000 games insufficient for complex strategy discovery
- Reward structure too simple (win/loss/draw only)
- No reward shaping for intermediate good moves
- Needed better training opponents (trained only against itself)

---

### 5. Monte Carlo Tree Search (MCTS) Agent

**Algorithm Type:** Simulation-Based Search

**How It Works:**

For each possible move, MCTS runs 1000+ random simulations:

**Four Phases per Simulation:**

1. **Selection** - Navigate down the tree using UCB1 formula
2. **Expansion** - Add a new node to the tree
3. **Simulation** - Play out a random game from that position
4. **Backpropagation** - Update statistics for all nodes visited

**UCB1 Formula (Balances Exploration vs Exploitation):**

```
UCB1 = (wins/visits) + C × √(ln(parent_visits)/visits)
         ↑                        ↑
    Exploitation            Exploration

Where C = exploration constant (√2)
```

**Code Concept:**

```python
def mcts_search(board, simulations=1000):
    root = Node(board)

    for _ in range(simulations):
        node = root

        # Selection: Navigate down tree using UCB1
        while node.is_fully_expanded():
            node = node.best_child_ucb1()

        # Expansion: Add new child node
        if not node.is_terminal():
            node = node.expand()

        # Simulation: Random playout
        result = simulate_random_game(node.state)

        # Backpropagation: Update statistics
        while node is not None:
            node.visits += 1
            node.wins += result
            node = node.parent

    # Return move with most visits
    return root.most_visited_child()
```

**Performance:**

- Win Rate: ~26%
- 99.8% unbeaten rate
- Crushed Q-Learning (29 wins vs 1 loss)
- 4 total losses in entire tournament

**Key Strength:**
Thinks fresh for every move. Doesn't rely on pre-trained knowledge. Adapts to opponent's strategy in real-time through simulations.

**Trade-off:**
Most computationally expensive during gameplay (1000+ simulations per move).

---

## Tournament System

### Design Principles

**Round-Robin Format:**

- Every agent plays every other agent
- Total matchups: 10 (5 agents × 4 opponents each ÷ 2)

**Games Per Matchup: 200**

- 100 games with Agent A as X (first player)
- 100 games with Agent A as O (second player)
- **Why?** First player has slight advantage; alternating ensures fairness

**Total Games: 4,000**

- 10 matchups × 200 games each × 2 positions

### Metrics Tracked

For each agent:

- **Total wins, losses, draws**
- **Win rate by position** (as X vs as O)
- **Performance against each opponent**
- **Draw rate vs top agents**

### Board Representation

**1D Array (Length 9):**

```
[0, 1, 2]     Positions:  [0][1][2]
[3, 4, 5]  →              [3][4][5]
[6, 7, 8]                 [6][7][8]

Values:
  0 = empty
  1 = X
 -1 = O
```

**Why 1D instead of 2D?**

- Simpler indexing for AI algorithms
- Easier state representation for Q-Learning
- Faster processing

---

## Results & Analysis

### Performance Tiers

**Tier 1: Nearly Perfect (Minimax, Heuristic)**

- Win Rate: ~35%
- Losses: 0-1 total
- Draw rate vs each other: 100%
- Strategy: Different paths to optimal play

**Tier 2: Very Strong (MCTS)**

- Win Rate: ~26%
- Losses: 4 total
- 99.8% unbeaten rate
- Strategy: Statistical approximation of optimal play

**Tier 3: Competent but Flawed (Q-Learning)**

- Win Rate: ~23%
- Losses: 434 total
- Good defense, weak offense
- Strategy: Pattern-based from incomplete learning

### Key Discoveries

**1. The Draw Wall**
When both agents play near-optimally, draws become inevitable:

- Minimax vs Heuristic: 200/200 draws
- MCTS vs Heuristic: 199/200 draws
- Minimax vs MCTS: 199/200 draws

**2. Simple ≠ Inferior**
Heuristic's five simple rules matched Minimax's exhaustive search while running 50x faster.

**3. Learning Quality > Learning Quantity**
Q-Learning's 75,000 training games weren't enough without:

- Diverse training opponents
- Better reward shaping
- Strategic exploration guidance

**4. Fresh Thinking Wins**
MCTS (no stored knowledge) beat Q-Learning (75,000 games of experience) because it adapts to each unique position.

**5. Random's Miracle**
Random beat Heuristic once by accidentally creating a fork (two simultaneous winning threats). Minimax prevents this through exhaustive search.

---

## Usage Guide

### Running the Tournament

```python
# Basic tournament
python main.py

# Results saved to: results/tournament_results.csv
```

### Customizing the Tournament

```python
# Modify number of games per matchup
tournament = Tournament(agents, games_per_matchup=100)

# Run specific matchup
matchup = Matchup(agent1, agent2, games=50)
matchup.play_series()
```

### Testing Individual Agents

```python
from agents.minimax_agent import MinimaxAgent
from agents.random_agent import RandomAgent
from game.game import Game

# Create agents
minimax = MinimaxAgent()
random = RandomAgent()

# Play single game
game = Game(minimax, random)
winner = game.play()
```

### Analyzing Results

```python
# Load tournament results
import pandas as pd
results = pd.read_csv('results/tournament_results.csv')

# Filter specific matchup
minimax_vs_heuristic = results[
    (results['agent1'] == 'Minimax') &
    (results['agent2'] == 'Heuristic')
]

# Calculate statistics
win_rate = results['wins'].sum() / results['total_games'].sum()
```

---

## Implementation Details

### Project Structure

```
Tic-AI-Toe/
├── main.py                  # Tournament entry point
├── agents/
│   ├── random_agent.py      # Baseline agent
│   ├── heuristic_agent.py   # Rule-based agent
│   ├── minimax_agent.py     # Game tree search
│   ├── qlearning_agent.py   # Reinforcement learning
│   └── mcts_agent.py        # Monte Carlo simulation
├── game/
│   ├── board.py             # Board state management
│   └── game.py              # Game logic and rules
├── tournament/
│   ├── tournament.py        # Tournament orchestration
│   └── matchup.py           # Head-to-head matchup manager
└── results/
    ├── tournament_results.csv
    └── qlearning_training_curve.png
```

### Dependencies

**Required:**

- Python 3.x
- NumPy (for Q-Learning arrays)

**Optional:**

- Matplotlib (for visualizations)
- Pandas (for data analysis)

### Algorithm Complexity

**Random:**

- Time: O(1)
- Space: O(1)

**Heuristic:**

- Time: O(n) where n = empty positions
- Space: O(1)

**Minimax with Alpha-Beta:**

- Time: O(b^d) where b = branching factor, d = depth
- With pruning: ~O(b^(d/2))
- Space: O(d) for recursion stack

**Q-Learning:**

- Training: O(episodes × moves_per_game)
- Playing: O(1) table lookup
- Space: O(states × actions) for Q-table

**MCTS:**

- Time: O(simulations × moves_per_simulation)
- Space: O(tree_nodes) = O(simulations)

---

## Future Improvements

**For Q-Learning:**

- Train against diverse opponents (not just self-play)
- Implement reward shaping for strategic moves
- Use deep Q-learning (neural network instead of table)

**For Tournament:**

- Add more agents (Deep Q-Learning, AlphaZero-style)
- Implement Elo rating system
- Track move-by-move decision patterns

**For Analysis:**

- Visualize decision trees
- Track computation time per move
- Analyze opening strategy effectiveness

---

## References

**Related Work:**

- Khushee Kapoor: "AI Agent Tic-Tac-Toe" (Kaggle)
- Sai Coumar: "Tic-Tac-Toe AI Tournament" (Medium)

---

## Contact

**Authors:** Aryan Tandon, Bipin Kumar Thollikonda  
**Course:** CSCI-6660: Introduction to AI  
**GitHub:** https://github.com/AryanTD/Tic-AI-Toe

---

## License

MIT License - Use this project for learning and education!
