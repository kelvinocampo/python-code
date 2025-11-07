def calc_area(coords: list[str]):
    value = 0
    for coord in coords:
        lenght = len(coord)
        x, y = coord[1:lenght - 1 ].split()
        x = int(x)
        y = int(y)
        distance = x - y
        if distance != 0:
            if value:
                result = abs(value * distance)
                return result

            value = distance


coords = [
    "(1 1)",
    "(1 3)",
    "(3 1)",
    "(3 3)",
]
area = calc_area(coords)
print(area)
