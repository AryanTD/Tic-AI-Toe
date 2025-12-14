from game.board import TicTacToe
from agents.mcts_agent import MCTSAgent
from agents.random_agent import RandomAgent
from agents.heuristic_agent import HeuristicAgent
from agents.minimax_agent import MinimaxAgent
from agents.qlearning_agent import QLearningAgent

print("=" * 60)
print("MCTS AGENT COMPLETE EVALUATION")
print("=" * 60)

# Load trained Q-Learning agent
qlearning = QLearningAgent(player=-1)
qlearning.load_q_table("q_table.pkl")
qlearning.epsilon = 0

# Test MCTS (1000 sims) against all agents
mcts = MCTSAgent(player=1, num_simulations=1000)

# Test 1: vs Heuristic
print("\n" + "=" * 60)
print("MCTS (X) vs Heuristic (O) - 50 games")
print("=" * 60)
wins = losses = draws = 0

for i in range(50):
    game = TicTacToe()
    heuristic = HeuristicAgent(player=-1)
    
    while not game.is_game_over():
        if game.current_player == 1:
            move = mcts.get_move(game)
        else:
            move = heuristic.get_move(game)
        game.make_move(move)
    
    winner = game.check_winner()
    if winner == 1:
        wins += 1
    elif winner == -1:
        losses += 1
    else:
        draws += 1

print(f"MCTS wins: {wins} ({wins*2}%)")
print(f"Heuristic wins: {losses} ({losses*2}%)")
print(f"Draws: {draws} ({draws*2}%)")

# Test 2: vs Q-Learning
print("\n" + "=" * 60)
print("MCTS (X) vs Q-Learning (O) - 50 games")
print("=" * 60)
wins = losses = draws = 0

for i in range(50):
    game = TicTacToe()
    qlearning.player = -1
    
    while not game.is_game_over():
        if game.current_player == 1:
            move = mcts.get_move(game)
        else:
            move = qlearning.get_move(game, training=False)
        game.make_move(move)
    
    winner = game.check_winner()
    if winner == 1:
        wins += 1
    elif winner == -1:
        losses += 1
    else:
        draws += 1

print(f"MCTS wins: {wins} ({wins*2}%)")
print(f"Q-Learning wins: {losses} ({losses*2}%)")
print(f"Draws: {draws} ({draws*2}%)")

# Test 3: vs Minimax
print("\n" + "=" * 60)
print("MCTS (X) vs Minimax (O) - 20 games")
print("=" * 60)
wins = losses = draws = 0

for i in range(20):
    game = TicTacToe()
    minimax = MinimaxAgent(player=-1)
    
    while not game.is_game_over():
        if game.current_player == 1:
            move = mcts.get_move(game)
        else:
            move = minimax.get_move(game)
        game.make_move(move)
    
    winner = game.check_winner()
    if winner == 1:
        wins += 1
    elif winner == -1:
        losses += 1
    else:
        draws += 1

print(f"MCTS wins: {wins} ({wins*5}%)")
print(f"Minimax wins: {losses} ({losses*5}%)")
print(f"Draws: {draws} ({draws*5}%)")

print("\n" + "=" * 60)
print("EVALUATION COMPLETE!")
print("=" * 60)