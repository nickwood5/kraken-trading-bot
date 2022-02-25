import talib, numpy


def detect_entrance(coin_data):
    # Process the coin candlestick data from the last 12 hours and determine if bot should buy
    # Return True if the bot should buy, otherwise return False
    return False


def detect_exit(coin_data):
    # Process the coin candlestick data from the last 12 hours and determine if bot should sell
    # Return True if the bot should sell, otherwise return False
    return False


def updateIndicators(database, coin):
    coin_data = database[coin]
    highs = coin_data['highs']
    lows = coin_data['lows']
    closes = coin_data['closes']

    np_closes = numpy.array(closes)
    np_highs = numpy.array(highs)
    np_lows = numpy.array(lows)

    stoch_k, stoch_d = talib.STOCH(np_highs, np_lows, np_closes, fastk_period=14, slowk_period=3, slowd_period=3)
    ultosc = talib.ULTOSC(np_highs, np_lows, np_closes, timeperiod1=7, timeperiod2=14, timeperiod3=28)
    rsi = talib.RSI(np_closes, 14)

    p_rsi_14 = numpy.ndarray.tolist(rsi)
    p_stoch_k = numpy.ndarray.tolist(stoch_k)
    p_stoch_d = numpy.ndarray.tolist(stoch_d)
    p_ultosc = numpy.ndarray.tolist(ultosc)

    coin_data['rsi'].append(p_rsi_14[-1])
    coin_data['stoch_k'].append(p_stoch_k[-1])
    coin_data['stoch_d'].append(p_stoch_d[-1])
    coin_data['ultosc'].append(p_ultosc[-1])

