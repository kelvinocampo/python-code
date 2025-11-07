PRICES = [1, 5, 10, 25, 50]


def bill_to_coin(bill: int):
    PRICES.sort()
    coins = []
    i = 0
    while True:
        max_price = PRICES[(len(PRICES) - 1) - i]

        if max_price > bill:
            i += 1
            continue
        elif max_price <= bill:
            bill -= max_price
            coins.append(max_price)

        if bill == 0:
            return coins


coins = bill_to_coin(253)
print(coins)
