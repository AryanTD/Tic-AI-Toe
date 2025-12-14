from game.board import TicTacToe
from agents.qlearning_agent import QLearningAgent
from agents.random_agent import RandomAgent
from agents.heuristic_agent import HeuristicAgent
from agents.minimax_agent import MinimaxAgent

# Load the trained agent
print("Loading trained Q-Learning agent...")
agent = QLearningAgent(player=1)
agent.load_q_table("q_table.pkl")
agent.epsilon = 0  # No exploration during testing!

print(f"Loaded Q-table with {len(agent.q_table):,} states\n")

# Test 1: Q-Learning vs Random
print("=" * 50)
print("Q-Learning (X) vs Random (O) - 100 games")
print("=" * 50)
wins = 0
losses = 0
draws = 0

for i in range(100):
    game = TicTacToe()
    random_agent = RandomAgent(player=-1)
    
    while not game.is_game_over():
        if game.current_player == 1:
            move = agent.get_move(game, training=False)
        else:
            move = random_agent.get_move(game)
        game.make_move(move)
    
    winner = game.check_winner()
    if winner == 1:
        wins += 1
    elif winner == -1:
        losses += 1
    else:
        draws += 1

print(f"Q-Learning wins: {wins}%")
print(f"Random wins: {losses}%")
print(f"Draws: {draws}%")

# Test 2: Q-Learning vs Heuristic
print("\n" + "=" * 50)
print("Q-Learning (X) vs Heuristic (O) - 100 games")
print("=" * 50)
wins = 0
losses = 0
draws = 0

for i in range(100):
    game = TicTacToe()
    heuristic = HeuristicAgent(player=-1)
    
    while not game.is_game_over():
        if game.current_player == 1:
            move = agent.get_move(game, training=False)
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

print(f"Q-Learning wins: {wins}%")
print(f"Heuristic wins: {losses}%")
print(f"Draws: {draws}%")

# Test 3: Q-Learning vs Minimax
print("\n" + "=" * 50)
print("Q-Learning (X) vs Minimax (O) - 20 games")
print("=" * 50)
wins = 0
losses = 0
draws = 0

for i in range(20):
    game = TicTacToe()
    minimax = MinimaxAgent(player=-1)
    
    while not game.is_game_over():
        if game.current_player == 1:
            move = agent.get_move(game, training=False)
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

print(f"Q-Learning wins: {wins} ({wins*5}%)")
print(f"Minimax wins: {losses} ({losses*5}%)")
print(f"Draws: {draws} ({draws*5}%)")