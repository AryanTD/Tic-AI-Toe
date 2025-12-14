from game.board import TicTacToe

game = TicTacToe()
print("Starting game: ")
game.display()

moves = [4,0,1,3,7]

for move in moves:
    print(f"Player {'X' if game.current_player == 1 else 'O'} moves to position {move}")
    game.make_move(move)
    game.display()

    winner = game.check_winner()
    if winner != 0:
        print(f"Player {'X' if winner == 1 else 'O'} wins!")
        break

print(f"Legal moves remaining: {game.get_legal_moves()}")
print(f"Game Over: {game.is_game_over()}")