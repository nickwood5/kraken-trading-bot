import json


def coinPurchase(coin_in_position, position_volume, buy_price):
    with open("status.json", 'r') as f:
        status = json.load(f)

    status['coin_in_position'] = coin_in_position
    status['position_volume'] = position_volume
    status['buy_price'] = buy_price

    with open("status.json", 'w') as f:
        json.dump(status, f)


def coinSell():
    with open("status.json", 'r') as f:
        status = json.load(f)

    status['coin_in_position'] = 'None'

    with open("status.json", 'w') as f:
        json.dump(status, f)