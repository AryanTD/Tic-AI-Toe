from board import TicTacToe
from agents.random_agent import RandomAgent

game = TicTacToe()

player_x = RandomAgent(player = 1)   # X player
player_o = RandomAgent(player =-1)  # O player

print("Two Random Agents playing Tic-Tac-Toe:\n")

move_count = 0

while not game.is_game_over():
    move_count += 1

    if game.current_player == 1:
        move = player_x.get_move(game)
        print(f"Move {move_count}: Player X chooses position {move}")
    else:
        move = player_o.get_move(game)
        print(f"Move {move_count}: Player O chooses position {move}")

    game.make_move(move)
    game.display()

winner = game.check_winner()
if winner == 1:
    print("Player X wins!")
elif winner == -1:
    print("Player O wins!")
else:
    print("The game is a draw!")

x_wins = 0
o_wins = 0
draws = 0

for i in range(100):
    game = TicTacToe()
    player_x = RandomAgent(player=1)
    player_o = RandomAgent(player=-1)
    
    while not game.is_game_over():
        if game.current_player == 1:
            move = player_x.get_move(game)
        else:
            move = player_o.get_move(game)
        game.make_move(move)
    
    winner = game.check_winner()
    if winner == 1:
        x_wins += 1
    elif winner == -1:
        o_wins += 1
    else:
        draws += 1

print(f"Results after 100 games:")
print(f"X wins: {x_wins}%")
print(f"O wins: {o_wins}%")
print(f"Draws: {draws}%")