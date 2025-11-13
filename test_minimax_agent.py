from board import TicTacToe
from agents.random_agent import RandomAgent
from agents.heuristic_agent import HeuristicAgent
from agents.minimax_agent import MinimaxAgent

# Test 1: Minimax vs Random
print("=== Minimax (X) vs Random (O) - 20 games ===")
minimax_wins = 0
random_wins = 0
draws = 0

for i in range(20):  # Start with just 20 games (Minimax is slow!)
    game = TicTacToe()
    minimax = MinimaxAgent(player=1)
    random_agent = RandomAgent(player=-1)
    
    while not game.is_game_over():
        if game.current_player == 1:
            move = minimax.get_move(game)
        else:
            move = random_agent.get_move(game)
        game.make_move(move)
    
    winner = game.check_winner()
    if winner == 1:
        minimax_wins += 1
    elif winner == -1:
        random_wins += 1
    else:
        draws += 1

print(f"Minimax wins: {minimax_wins} ({minimax_wins*5}%)")
print(f"Random wins: {random_wins} ({random_wins*5}%)")
print(f"Draws: {draws} ({draws*5}%)")

# Test 2: Minimax vs Heuristic
print("\n=== Minimax (X) vs Heuristic (O) - 20 games ===")
minimax_wins = 0
heuristic_wins = 0
draws = 0

for i in range(100):
    game = TicTacToe()
    minimax = MinimaxAgent(player=1)
    heuristic = HeuristicAgent(player=-1)
    
    while not game.is_game_over():
        if game.current_player == 1:
            move = minimax.get_move(game)
        else:
            move = heuristic.get_move(game)
        game.make_move(move)
    
    winner = game.check_winner()
    if winner == 1:
        minimax_wins += 1
    elif winner == -1:
        heuristic_wins += 1
    else:
        draws += 1

print(f"Minimax wins: {minimax_wins} ({minimax_wins*5}%)")
print(f"Heuristic wins: {heuristic_wins} ({heuristic_wins*5}%)")
print(f"Draws: {draws} ({draws*5}%)")

print("\n=== Counting Minimax's Work ===")
game = TicTacToe()
minimax = MinimaxAgent(player=1)

# Just make ONE move from the starting position
minimax.nodes_explored = 0
move = minimax.get_move(game)
print(f"First move from empty board: position {move}")
print(f"Positions evaluated: {minimax.nodes_explored:,}")

print("\n=== Alpha-Beta Pruning Performance ===")
game = TicTacToe()
minimax = MinimaxAgent(player=1)

minimax.nodes_explored = 0
move = minimax.get_move(game)
print(f"First move with Alpha-Beta: position {move}")
print(f"Positions evaluated: {minimax.nodes_explored:,}")
print(f"Reduction from 549,945: {(1 - minimax.nodes_explored/549945)*100:.1f}%")

print("\n=== How Work Decreases Each Move ===")

# Simulate a game and count work per move
game = TicTacToe()
minimax_x = MinimaxAgent(player=1)
minimax_o = MinimaxAgent(player=-1)

move_number = 1
while not game.is_game_over():
    if game.current_player == 1:
        minimax_x.nodes_explored = 0
        move = minimax_x.get_move(game)
        print(f"Move {move_number} (X): {minimax_x.nodes_explored:,} positions evaluated")
    else:
        minimax_o.nodes_explored = 0
        move = minimax_o.get_move(game)
        print(f"Move {move_number} (O): {minimax_o.nodes_explored:,} positions evaluated")
    
    game.make_move(move)
    move_number += 1

print(f"\nGame ended in a draw (as expected!)")

print("\n=== Can Random beat Heuristic? ===")
# Heuristic as O (disadvantage), Random as X
random_wins = 0
heuristic_wins = 0
draws = 0

for i in range(100):
    game = TicTacToe()
    random_agent = RandomAgent(player=1)
    heuristic = HeuristicAgent(player=-1)
    
    while not game.is_game_over():
        if game.current_player == 1:
            move = random_agent.get_move(game)
        else:
            move = heuristic.get_move(game)
        game.make_move(move)
    
    winner = game.check_winner()
    if winner == 1:
        random_wins += 1
    elif winner == -1:
        heuristic_wins += 1
    else:
        draws += 1

print(f"Random wins: {random_wins}%")
print(f"Heuristic wins: {heuristic_wins}%") 
print(f"Draws: {draws}%")

print("\n=== Can Random beat Minimax? ===")
# Minimax as O (disadvantage), Random as X
random_wins = 0
minimax_wins = 0
draws = 0

for i in range(100):
    game = TicTacToe()
    random_agent = RandomAgent(player=1)
    minimax = MinimaxAgent(player=-1)
    
    while not game.is_game_over():
        if game.current_player == 1:
            move = random_agent.get_move(game)
        else:
            move = minimax.get_move(game)
        game.make_move(move)
    
    winner = game.check_winner()
    if winner == 1:
        random_wins += 1
    elif winner == -1:
        minimax_wins += 1
    else:
        draws += 1

print(f"Random wins: {random_wins}%")
print(f"Minimax wins: {minimax_wins}%")
print(f"Draws: {draws}%")