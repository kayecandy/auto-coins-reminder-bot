import requests
import logging
import time
import hmac
import hashlib
import numpy as np
import os
from time import time
from urllib.parse import urlencode
from src.binance.consts import BINANCE
from src.telegram.telegram import tg_message


####################
# HELPER FUNCTIONS
####################
def get_signature(query):

    queryString = bytes(urlencode(query), 'latin-1')
    secret = bytes(BINANCE.API_SECRET, 'latin-1')

    return hmac.new(secret, queryString, digestmod=hashlib.sha256).hexdigest()


def env_candle_intervals():
    return list(map(
        lambda interval: getattr(BINANCE, interval),
        os.getenv('GRAPH_CANDLE_INTERVAL').split(',')
    ))

####################
# REQUEST FUNCTIONS
####################
def request_margin_trade(
    stockCode, 
    orderSide, 
    amount, 
    price='', 
    orderType=BINANCE.ORDER_TYPE_MARKET, 
    isIsolated=BINANCE.IS_ISOLATED_TRUE, 
    timeInForce=BINANCE.TIME_IN_FORCE_GTC,
    responseType=BINANCE.ORDER_RESPONSE_RESULT
):
    ts = int(time() * 1000)

    query = {
        'symbol'            : stockCode,
        'isIsolated'        : isIsolated,
        'side'              : orderSide,
        'type'              : orderType,
        'quantity'          : amount,
        'timeInForce'       : timeInForce,
        'newOrderRespType'  : responseType,
        'timestamp'         : ts
    }

    if orderType == BINANCE.ORDER_TYPE_LIMIT:
        query['price'] = price

    signature = get_signature(query)
    query['signature'] = signature

    return requests.post(BINANCE.API_ORDER_MARGIN, data=query, headers=BINANCE.HEADER_AUTH)



def request_margin_amount(stockCode):
    query = {
        'symbols': stockCode,
        'timestamp': int(time() * 1000)
    }

    signature = get_signature(query)
    query['signature'] = signature

    return requests.get(BINANCE.API_GET_MARGIN_ACCOUNT, query, headers=BINANCE.HEADER_AUTH).json()

def request_moving_averages(stockCode, limit, limitBase, interval):
    trades = requests.get(BINANCE.API_GET_SYMBOL_KLINES, {
        'symbol'        : stockCode,
        'limit'         : limitBase,
        'interval'      : interval
    }).json()

    tradesAverages = list(map(lambda trade: float(trade[BINANCE.KLINE_CLOSE]), trades))


    ma25 = np.average(tradesAverages)
    ma7 = np.average(tradesAverages[-limit:])

    return {
        'MA7'       : ma7,
        'MA25'      : ma25
    }

####################
# MAIN FUNCTIONS
####################

def price_check(
    stockCode = os.getenv('GRAPH_STOCK', 'UNIBTC'), 
    limit = int(os.getenv('GRAPH_MA_7', 7)), 
    limitBase = int(os.getenv('GRAPH_MA_25', 25)), 
    intervals = env_candle_intervals()
):

    delta = float(os.getenv('GRAPH_DELTA_CHECK', 0.00001))

    for interval in intervals:
        averages = request_moving_averages(stockCode, limit, limitBase, interval)

        logging.warning((interval, 'MA7 ' + str(averages['MA7']), 'MA25 ' + str(averages['MA25']), delta))

        if averages['MA7'] + delta >= averages['MA25'] and averages['MA7'] - delta <= averages['MA25']:
            tg_message(
                '*_MA Intersect_*\n'
                + 'Interval: ' + interval + '\n'
                + 'MA7: ' + str(averages['MA7']).replace('.', '\\.') + '\n'
                + 'MA25: ' + str(averages['MA25']).replace('.', '\\.')
            )



def get_slope(stockCode, limit = 7, limitBase = 25, interval = BINANCE.INTERVAL_MIN1):
    

    trades = requests.get(BINANCE.API_GET_SYMBOL_KLINES, {
        'symbol'        : stockCode,
        'limit'         : limitBase + 1,
        'interval'      : interval
    }).json()

    currPrice = float(requests.get(BINANCE.API_GET_PRICE, {
        'symbol'        : stockCode
    }).json()['price'])

    tradesAverages = list(map(lambda trade: (float(trade[BINANCE.KLINE_HIGH]) + float(trade[BINANCE.KLINE_HIGH])) / 2, trades))
    

    numTrades = trades[-1][8]
    ma25 = np.average(tradesAverages[1:])
    pMA25 = np.average(tradesAverages[:limitBase])
    movingAverage = np.average(tradesAverages[-limit:])
    pMovingAverage = np.average(tradesAverages[-limit - 1:-1])
    

    marginAccount = request_margin_amount(stockCode)



    newPosition = ''
    amount = 0

    if movingAverage > pMovingAverage:
        if ma25 > pMA25:
            newPosition = 'BUY'
            amount = int(float(marginAccount['assets'][0]['quoteAsset']['free']) / currPrice)
    elif movingAverage < pMovingAverage:
        newPosition = 'SELL'
        amount = int(float(marginAccount['assets'][0]['baseAsset']['free']))

    logging.warning((newPosition, 'MA ' + str(movingAverage), 'Prev MA ' + str(pMovingAverage), 'volume ' + str(numTrades), 'BTC ' + marginAccount['assets'][0]['quoteAsset']['free'], 'UNI ' + marginAccount['assets'][0]['baseAsset']['free']))

    logging.warning(('MA25 ' + str(ma25), 'Prev MA25 ' + str(pMA25)))

    # TODO: Cleanup


    if (newPosition != '' and BINANCE.position != newPosition and amount > 0):
        logging.warning(('TRANSACTION!!! ', newPosition, movingAverage))
        request_margin_trade(stockCode, newPosition, amount)
        tg_message(newPosition + ' ' + str(amount) + ' UNI at ' + str(currPrice) + ' BTC')
        BINANCE.position = newPosition






