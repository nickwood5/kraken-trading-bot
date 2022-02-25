import krakenCommands, time, config, requests


def getCurrentPrice(coin):
    resp = requests.get('https://api.kraken.com/0/public/Ticker?pair=' + coin)
    data = resp.json()
    kraken_coin_name = list(data['result'].keys())[0]
    current_price = float(data['result'][kraken_coin_name]['a'][0])
    return current_price


def marketBuyOrder(coin, trade_amount):
    current_price = getCurrentPrice(coin)
    volume = trade_amount/current_price
    print(volume)

    resp = krakenCommands.kraken_request('/0/private/AddOrder', {
    "nonce": str(int(1000*time.time())),
    "ordertype": "market",
    "type": "buy",
    "volume": volume,
    "pair": coin
    }, config.API_KEY, config.API_SECRET)

    print(resp.json())
    data = resp.json()
    result = data['result']

    order_description = result['descr']['order']
    volume_purchased = float(order_description.split()[1])
    txid = result['txid'][0]

    return volume_purchased, txid


def marketSellOrder(coin, volume):
    current_price = getCurrentPrice(coin)

    resp = krakenCommands.kraken_request('/0/private/AddOrder', {
    "nonce": str(int(1000*time.time())),
    "ordertype": "market",
    "type": "sell",
    "volume": volume,
    "pair": coin
    }, config.API_KEY, config.API_SECRET)

    print(resp.json())
    data = resp.json()
    result = data['result']

    order_description = result['descr']['order']
    volume_purchased = float(order_description.split()[1])
    txid = result['txid'][0]

    return volume_purchased, txid


def limitSellOrder(coin, sell_price, volume):
    kraken_coin_decimals = {'ATOMUSD': 4, 'ALGOUSD': 5, 'EOSUSD': 4, 'XMRUSD': 2, 'XLMUSD': 6, 'LINKUSD': 5, 'LTCUSD': 2, 'TRXUSD': 6, 'UNIUSD': 3, 'SOLUSD': 2, 'BCHUSD': 2, 'AAVEUSD': 2, 'FILUSD': 3, 'BTCUSD': 1, 'MATICUSD': 4, 'DOTUSD': 4, 'DOGEUSD': 7, 'XRPUSD': 5}
    rounding = kraken_coin_decimals[coin]
    print(rounding)
    rounded_sell_price = round(sell_price, rounding)

    resp = krakenCommands.kraken_request('/0/private/AddOrder', {
    "nonce": str(int(1000*time.time())),
    "ordertype": "limit",
    "type": "sell",
    "volume": volume,
    "pair": coin,
    "price": rounded_sell_price
    }, config.API_KEY, config.API_SECRET)

    print(resp.json())
    data = resp.json()
    result = data['result']
    txid = result['txid'][0]
    return txid
    

def stopLossOrder(coin, sell_price, volume):
    kraken_coin_decimals = {'ATOMUSD': 4, 'ALGOUSD': 5, 'EOSUSD': 4, 'XMRUSD': 2, 'XLMUSD': 6, 'LINKUSD': 5, 'LTCUSD': 2, 'TRXUSD': 6, 'UNIUSD': 3, 'SOLUSD': 2, 'BCHUSD': 2, 'AAVEUSD': 2, 'FILUSD': 3, 'BTCUSD': 1, 'MATICUSD': 4, 'DOTUSD': 4, 'DOGEUSD': 7, 'XRPUSD': 5}
    rounding = kraken_coin_decimals[coin]
    print(rounding)
    rounded_price = round(sell_price, rounding)

    resp = krakenCommands.kraken_request('/0/private/AddOrder', {
    "nonce": str(int(1000*time.time())),
    "ordertype": "stop-loss",
    "type": "sell",
    "volume": volume,
    "pair": coin,
    "price": rounded_price
    }, config.API_KEY, config.API_SECRET)

    print(resp.json())
    data = resp.json()
    result = data['result']
    txid = result['txid'][0]
    return txid


def cancelAllOrders():
    resp = krakenCommands.kraken_request('/0/private/CancelAll', {
    "nonce": str(int(1000*time.time()))
    }, config.API_KEY, config.API_SECRET)


def getOrderBuyPrice(txid):
    resp = krakenCommands.kraken_request('/0/private/QueryOrders', {
    "nonce": str(int(1000*time.time())),
    "txid": txid,
    "trades": True
    }, config.API_KEY, config.API_SECRET)
    data = resp.json()
    print(data)
    buy_price = float(data['result'][txid]['price'])
    print(buy_price)

    return buy_price

def getOrderStatus(txid):
    resp = krakenCommands.kraken_request('/0/private/QueryOrders', {
    "nonce": str(int(1000*time.time())),
    "txid": txid,
    "trades": True
    }, config.API_KEY, config.API_SECRET)
    data = resp.json()
    status = data['result'][txid]['status']

    return status
    
