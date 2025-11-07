from model import Model
from InquirerPy import inquirer
from helpers import *


model = Model()
keys = list(model.keys)
keys.remove("id")

while True:
    choice = inquirer.select(
        message="Elige una opción:",
        choices=["Create", "Read", "Update", "Delete", "Exit"],
    ).execute()

    if choice == "Create":
        row = {}
        for key in keys:
            value = input_value(f"Ingresa el valor para el campo '{key}': ")
            row[key] = value
        model.create(row)
        print("Registro(s) creado exitosamente.\n")
        continue
    elif choice == "Read":
        where_input = multi_input(
            "Ingresa los filtros a aplicar (campo=valor)(separados por coma) o dejalo vacio para conseguirlos todos: "
        )
        if where_input:
            model.print_data(where_input)
        else:
            model.print_data()
        continue
    elif choice == "Delete":
        where_input = multi_input(
            "Ingresa los filtros a aplicar (campo=valor)(separados por coma) o dejalo vacio para borrar todos: "
        )
        if where_input:
            model.delete(where_input)
        else:
            model.delete()
        print(f"{model.affectedRows} registro(s) eliminado(s) exitosamente.\n")
        continue
    elif choice == "Update":
        where_input = multi_input(
            "Ingresa los filtros a aplicar (campo=valor)(separados por coma) o dejalo vacio para actualizar todos todos: "
        )
        set_input = multi_input(
            "Ingresa los cambios (campo=valor)(separados por coma): "
        )
        if where_input:
            model.update(set_input, where_input)
        else:
            model.update(set_input)
        print(f"{model.affectedRows} registro(s) editados exitosamente.\n")
        continue
    elif choice == "Exit":
        print("Saliendo del programa.")
        break
