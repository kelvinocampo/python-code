def multi_input(message: str):
    while True:
        user_input = input(message).strip()

        # Si el usuario no ingresa nada, devolvemos None
        if user_input == "":
            return None

        where = {}

        for expression in user_input.split(","):
            # Validar que tenga un "="
            if "=" in expression:
                key, value = expression.split(
                    "=", 1
                )  # 1 = solo divide en el primer "="
                key, value = key.strip(), value.strip()

                if key and value:
                    where[key] = value  # válido
                else:
                    print("Formato inválido. Usa campo=valor\n")
            else:
                print("Debes usar el formato campo=valor\n")

        print(where)
        return where


def input_value(message: str, required: bool = True):
    while True:
        user_input = input(message).strip()

        if user_input == "" and required:
            print("Debes ingresar un valor valido.")
            continue

        return user_input
