import random
import time
from animation import animacion

# Posiciones posibles
positions = [1, 2, 3]
tries = 0
points = 0

# Juego
animacion(0)
game = True
while game:
    while True:
        continue_game = input(
            "\n- Ingrese exit para salir \n- Presion Enter para iniciar el juego: "
        )

        if continue_game.lower() == "exit":
            salir = True
            break
        salir = False

        if continue_game not in ["exit", ""]:
            print("Entrada inválida. Inténtalo de nuevo.")
            continue
        else:
            break
    
    if salir:
        break

    # Posición inicial de la pelota
    ball_position = random.choice(positions)

    # Número de movimientos
    moves = random.randint(4, 8)

    animacion(ball_position)
    time.sleep(1)
    animacion(0)

    for i in range(moves):
        ball_initial = ball_position

        # Si la pelota está en una esquina
        if ball_position == 1:
            # Puede moverse hacia el centro o hacia el lado contrario
            ball_position = random.choice([2, 3])
        elif ball_position == 3:
            # Puede moverse hacia el centro o hacia el lado contrario
            ball_position = random.choice([2, 1])
        else:
            # Si está en el centro, puede moverse hacia cualquiera de las esquinas
            ball_position = random.choice([1, 3])

        coords = str(ball_initial) + str(ball_position)

        animacion(int(coords))
        time.sleep(0.5)

    while True:
        user_input = input(
            "\n- Ingrese exit para salir \n- Ingrese la posicion de la pelota: "
        )

        if user_input.lower() == "exit":
            salir = True
            break
        salir = False

        if user_input not in ["1", "2", "3", "exit"]:
            print("Entrada inválida. Inténtalo de nuevo.")
            continue
        else:
            break

    if salir:
        break

    user_input = int(user_input)
    if ball_position == user_input:
        animacion(user_input)
        points += 1
        print("¡Has ganado!")
    else:
        animacion(user_input + 3)
        print("Has perdido. Inténtalo de nuevo.")

    tries += 1
    time.sleep(1)

print(f"\nJuego terminado. Has jugado {tries} veces y has ganado {points} veces.")
print(f"Porcentaje de aciertos: {points/tries*100 if tries > 0 else 0:.2f}%")
print("¡Gracias por jugar!")
