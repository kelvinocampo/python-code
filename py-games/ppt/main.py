import random

combination = ["Roca", "Tijeras", "Papel"]

points_machine = 0
points_user = 0

win_combos = {"Roca": "Tijeras", "Tijeras": "Papel", "Papel": "Roca"}

while True:
    user = input("\nSelecciona una opcion: 1 - Roca, 2 - Tijeras, 3 - Papel, 4 - Salir: ")
    if user == '4':
        break

    machine_select = random.choice(combination)

    if user == '1':
        user_choice = "Roca"
    elif user == '2':
        user_choice = "Tijeras"
    elif user == '3':
        user_choice = "Papel"
    else:
        print("Opcion no valida. \n")
        continue

    print(f"\nTu elegiste: {user_choice}")
    print(f"La maquina eligio: {machine_select}\n")

    if win_combos[user_choice] == machine_select:
        machine = True
    else:
        machine = False

    if user_choice == machine_select:
        print("Empate. \n")
    elif machine:
        print("Ganaste. \n")
        points_user += 1
    else:
        print("Perdiste. \n")
        points_machine += 1

    print(f"Puntaje: \nMaquina: {points_machine} - Usuario: {points_user}")
    

print(f"Juego Terminado \nPuntaje Final: \nMaquina: {points_machine} - Usuario: {points_user}")
