from game.board import TicTacToe
from agents.heuristic_agent import HeuristicAgent
from agents.random_agent import RandomAgent

print("=== Heuristic (X) vs Random (O) ===")
heuristic_wins = 0
random_wins = 0
draws = 0


for i in range(100):
    game = TicTacToe()
    heuristic_agent = HeuristicAgent(player=-1)  # X
    random_agent = HeuristicAgent(player=1)       # O

    while not game.is_game_over():
        if game.current_player == 1:
            move = heuristic_agent.get_move(game)
        else:
            move = random_agent.get_move(game)
        
        game.make_move(move)
    
    winner = game.check_winner()
    if winner == 1:
        heuristic_wins += 1
    elif winner == -1:
        random_wins += 1
    else:
        draws += 1

print(f"Heuristic wins: {heuristic_wins}%")
print(f"Random wins: {random_wins}%")
print(f"Draws: {draws}%")