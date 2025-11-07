from utils import MENU, cells, print_game, player_symbols, coord, check_winner
from machine import select_cell_machine

game = True
win = False
print_game(cells)

while game:
    user_input = input(MENU)

    if user_input == "exit":
        game = False
        break

    # User
    x, y = coord(user_input)
    if cells[x][y] in [player_symbols["player"], player_symbols["machine"]]:
        print("Esta celda ya ha sido marcada.")
        continue
    cells[x][y] = player_symbols["player"]

    # Machine
    cells = select_cell_machine(cells)

    # Print Cells
    print_game(cells)

    # Check Winner
    if check_winner(cells) == player_symbols['player']:
        win = True
        break
    elif check_winner(cells) == player_symbols['machine']:
        win = False
        break

# End
if not game:
    print("Juego Finalizado.")
else:
    print("Has ganado." if win else "Has perdido.")
