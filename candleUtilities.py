import time, requests, indicatorsFunctions, slackBot, config
from datetime import datetime


def getRawCoinData(coin, current_time, since):
    since = current_time - since
    url = 'https://api.kraken.com/0/public/OHLC?pair=' + coin + "&interval=5&since=" + str(int(since))
    data  = requests.get(url).json()
    result = data['result']
    keys = list(result.keys())
    pair_name = keys[0]
    candles = result[pair_name][:-1]

    return candles


def updateDatabase(coin, candle, database):
    c_timestamp = float(candle[0])
    c_open = float(candle[1])
    c_high = float(candle[2])
    c_low = float(candle[3])
    c_close = float(candle[4])
    c_volume = float(candle[6])
    database[coin]['timestamps'].append(c_timestamp)
    database[coin]['opens'].append(c_open)
    database[coin]['highs'].append(c_high)
    database[coin]['lows'].append(c_low)
    database[coin]['closes'].append(c_close)
    database[coin]['volumes'].append(c_volume)
    indicatorsFunctions.updateIndicators(database, coin)


def initializeCoinData(all_coins):
    database = {}
    current_time = time.time()
    for coin in all_coins:
        database[coin] = {'timestamps': [], 'opens': [], 'highs': [], 'lows': [], 'closes': [], 'rsi': [], 'stoch_k': [], 'stoch_d': [], 'ultosc': [], 'volumes': []}
        candles = getRawCoinData(coin, current_time, 43500)

        for candle in candles:
            updateDatabase(coin, candle, database)

    return database


def getLastCandle(coin):
    klines = getRawCoinData(coin, time.time(), 600)
    kline = klines[0]

    return kline


def printLatestCandle(coin, database):
    coin_data = database[coin]
    timestamp = datetime.fromtimestamp(int(coin_data['timestamps'][-1])-5*3600).strftime('%Y-%m-%d %H:%M:%S')
    close = coin_data['closes'][-1]
    last_rsi = coin_data['rsi'][-1]
    last_stoch_k = coin_data['stoch_k'][-1]
    last_stoch_d = coin_data['stoch_d'][-1]
    last_ultosc = coin_data['ultosc'][-1]
    last_volume = coin_data['volumes'][-1]

    status_message = "{}, {}: Candle closed at {}. RSI: {}. stoch_k: {}. stoch_d: {}. ultosc: {}. Volume: {}".format(timestamp, coin, close, round(last_rsi, 2), round(last_stoch_k, 2), round(last_stoch_d, 2), round(last_ultosc, 2), round(last_volume, 2))
    print(status_message)
    slackBot.post_message(status_message, config.SLACK_GENERAL)


def printLatestCandles(all_coins, database):
    status_message = ""
    for c in range (0, len(all_coins)):
        coin = all_coins[c]
        coin_data = database[coin]
        timestamp = datetime.fromtimestamp(int(coin_data['timestamps'][-1])-5*3600).strftime('%Y-%m-%d %H:%M:%S')
        close = coin_data['closes'][-1]
        last_rsi = coin_data['rsi'][-1]
        last_stoch_k = coin_data['stoch_k'][-1]
        last_stoch_d = coin_data['stoch_d'][-1]
        last_ultosc = coin_data['ultosc'][-1]
        last_volume = coin_data['volumes'][-1]

        status_message += "{}, {}: Candle closed at {}. RSI: {}. stoch_k: {}. stoch_d: {}. ultosc: {}. Volume: {}".format(timestamp, coin, close, round(last_rsi, 2), round(last_stoch_k, 2), round(last_stoch_d, 2), round(last_ultosc, 2), round(last_volume, 2))
        if c != len(all_coins)-1:
            status_message += '\n'
    
    print(status_message)
    slackBot.post_message(status_message, config.SLACK_GENERAL)