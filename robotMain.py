import candleUtilities, timeFunctions, time, indicatorsFunctions, slackBot, tradingFunctions, statusManager, json, config

# Specify amount to trade (USD)
trade_amount = 100

# Choose what coins to trade
all_coins = ["ATOMUSD", "ALGOUSD", "EOSUSD", "XMRUSD", "XLMUSD", "LINKUSD", "LTCUSD", "TRXUSD", "UNIUSD",
"SOLUSD", "BCHUSD", "AAVEUSD", "FILUSD", "BTCUSD", "MATICUSD", "DOTUSD", "DOGEUSD", "XRPUSD"]


def log(string):
    print(string)
    slackBot.post_message(string, config.SLACK_GENERAL)


def notify(string):
    print(string)
    slackBot.post_message(string, config.SLACK_IMPORTANT)


# Initialize status
with open("status.json", 'r') as f:
    status = json.load(f)
if status['coin_in_position'] == 'None':
    notify("Bot initializing for trade amount {}, not in position...".format(trade_amount))
    in_position = False
else:
    in_position = True
    coin_in_position = status['coin_in_position']
    position_volume = status['position_volume']
    buy_price = status['buy_price']
    current_price = tradingFunctions.getCurrentPrice(coin_in_position)
    notify("Bot initializing for trade amount {}, in position for {} {} at entrance price {}, current price {}.".format(trade_amount, position_volume, coin_in_position, buy_price, current_price))

    txid = tradingFunctions.stopLossOrder(coin_in_position, buy_price*0.99, position_volume)
    take_profit = False

start_time = timeFunctions.startTime()
trading = True
reset = True

while trading:
    if not in_position:
        if reset:
            timeFunctions.wait(start_time)
            database = candleUtilities.initializeCoinData(all_coins)
            notify("Initializing coin database...")
            reset = False
            timeFunctions.wait(start_time)

        for coin in all_coins:

            candle = candleUtilities.getLastCandle(coin)
            candleUtilities.updateDatabase(coin, candle, database)

            if not in_position:
                # Check if bot should buy this coin
                enter_position = indicatorsFunctions.detect_entrance(database[coin])

                if enter_position:
                    notify("buy for {}".format(coin))
                    position_volume, trade_id = tradingFunctions.marketBuyOrder(coin, trade_amount)

                    coin_in_position = coin
                    in_position = True

                    # Check if order has been closed before getting buy price
                    order_status = 'open'
                    while order_status == 'open':
                        try:
                            order_status = tradingFunctions.getOrderStatus(trade_id)
                        except:
                            notify("Waiting for market order to be filled...")
                            time.sleep(1)

                    notify("Market ordered filled.")

                    buy_price = tradingFunctions.getOrderBuyPrice(trade_id)
                    statusManager.coinPurchase(coin_in_position, position_volume, buy_price)

                    take_profit = False
                
        candleUtilities.printLatestCandles(all_coins, database)

    else:
        # Bot is in position 
        candle = candleUtilities.getLastCandle(coin_in_position)
        candleUtilities.updateDatabase(coin_in_position, candle, database)
        candleUtilities.printLatestCandle(coin_in_position, database)

        exit_position = indicatorsFunctions.detect_exit(database[coin_in_position])

        if exit_position:
            notify("Create sell order for {} {}".format(position_volume, position_volume))
            tradingFunctions.marketSellOrder(coin_in_position, position_volume)
            statusManager.coinSell()
            reset = True

    timeFunctions.wait(start_time)



