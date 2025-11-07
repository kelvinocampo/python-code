MENU = """
Opciones:
Terminar juego = exit

Elige la casilla escribiendo las coordenadas (x, y) ejemplo (12):
"""

cells = [
    [" ", " ", " "],
    [" ", " ", " "],
    [" ", " ", " "],
]

machine_choices = [
    '11', '12', '13', 
    '21', '22', '23', 
    '31', '32', '33'
]

win_combinations = [
    [(0,0), (0,1), (0,2)],
    [(1,0), (1,1), (1,2)],
    [(2,0), (2,1), (2,2)],

    [(0,0), (1,0), (2,0)],
    [(0,1), (1,1), (2,1)],
    [(0,2), (1,2), (2,2)],

    [(0,0), (1,1), (2,2)],
    [(0,2), (1,1), (2,0)],
]

player_symbols = {"player": "M", "machine": "O"}

def print_game(cells):
    for col in cells: 
        print('', *col, sep=' | ', end=' | \n', )
        print()

def coord(input_text):
    x = int(input_text[:1]) - 1
    y = int(input_text[1:2]) - 1
    return x, y

def check_winner(cells):
    for combo in win_combinations:
        (r1, c1), (r2, c2), (r3, c3) = combo
        if (
            cells[r1][c1] == cells[r2][c2] == cells[r3][c3]
            and cells[r1][c1] != " "
        ):
            return cells[r1][c1]  # 'X' o 'O'
    return None
