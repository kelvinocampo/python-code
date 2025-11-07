from utils import player_symbols, machine_choices, coord
import random

def select_cell_machine(cells):
    machine_selected = False
    while not machine_selected:
        machine_input = random.choice(machine_choices)
        x, y = coord(machine_input)

        if not cells[x][y] in [player_symbols["player"], player_symbols["machine"]]:
            machine_selected = True
    cells[x][y] = player_symbols["machine"]
    return cells