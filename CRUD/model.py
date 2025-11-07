from typing import Optional
import uuid
from helpers import *


class Model:
    _last_rows = []
    _rows_data = []
    affectedRows = []
    keys = []
    _model_name = ""

    def __init__(self):
        model_name = input_value("Ingresa el nombre del modelo: ")
        keys = input_value(
            "Ingresa los campos del modelo (separados por coma): "
        ).split(",")

        if "id" in keys:
            keys.remove("id")

        self._model_name = model_name

        keys = set(list(keys))
        self.keys = list(keys)
        self.keys.append("id")

    @property
    def _rows(self):
        return self._rows_data

    @_rows.setter
    def _rows(self, rows):
        self._rows_data = rows
        self._last_rows = rows

    def validate_cols(self, keys: list[str]):
        for key in keys:
            if not key in self.keys:
                raise ValueError(
                    f"Campo no válido: '{key}' no es parte de la definición del modelo '{self._model_name}'."
                )

    def valid_row(self, row: dict, where: dict):
        for key, value in where.items():
            if row[key] == value:
                return True
        return False

    def create(self, row: dict):
        row["id"] = str(uuid.uuid4())

        keys = row.keys()
        self.validate_cols(keys)

        self._rows.append(row)

    def read(self, where: Optional[dict] = None):
        rows = self._rows
        if where:
            rows = [row for row in self._rows if self.valid_row(row, where)]
        self.print_data(where)
        return rows

    def print_data(self, where: Optional[dict] = None):
        rows = self._rows
        if where:
            rows = [row for row in self._rows if self.valid_row(row, where)]

        if not rows:
            print(f"\n📭 No hay registros en el modelo '{self._model_name}'.\n")
            return

        # Obtener encabezados (columnas)
        headers = list(rows[0].keys())

        # Calcular el ancho máximo de cada columna
        col_widths = {
            header: max(len(header), *(len(str(row[header])) for row in rows))
            for header in headers
        }

        # Dibujar encabezado decorado
        print(f"\n📋 TABLA: {self._model_name.upper()}")
        print("=" * (sum(col_widths.values()) + len(headers) * 3 + 1))

        # Encabezados
        header_row = " | ".join(header.ljust(col_widths[header]) for header in headers)
        print(f"| {header_row} |")
        print("-" * (sum(col_widths.values()) + len(headers) * 3 + 1))

        # Filas de datos
        for row in rows:
            row_str = " | ".join(
                str(row[header]).ljust(col_widths[header]) for header in headers
            )
            print(f"| {row_str} |")

        print("=" * (sum(col_widths.values()) + len(headers) * 3 + 1))
        print()

    def delete(self, where: Optional[dict] = None):
        if not where and not self._rows:
            self._rows = []
            self.affectedRows = len(self._rows)
            return

        keys = where.keys()
        self.validate_cols(keys)

        affected_rows = len(self._rows)
        self._rows = [row for row in self._rows if not self.valid_row(row, where)]
        self.affectedRows = affected_rows - len(self._rows)

    def update(self, set: dict, where: Optional[dict] = None):
        keys = where.keys()
        self.validate_cols(keys)

        keys = set.keys()
        if "id" in keys:
            raise ValueError(
                f"El campo 'id' no es modificable en el modelo '{self._model_name}'."
            )
        self.validate_cols(keys)

        rows = self._rows
        if where:
            rows = [row for row in self._rows if self.valid_row(row, where)]

        affected_rows = 0
        for row in rows:
            for key, value in set.items():
                row[key] = value
            affected_rows += 1
        self.affectedRows = affected_rows
