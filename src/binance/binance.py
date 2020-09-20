import requests
import logging
import time
import hmac
import hashlib
import numpy as np
from time import time
from urllib.parse import urlencode
from src.binance.consts import BINANCE
from src.telegram.telegram import tg_message


def get_signature(query):

    queryString = bytes(urlencode(query), 'latin-1')
    secret = bytes(BINANCE.API_SECRET, 'latin-1')

    return hmac.new(secret, queryString, digestmod=hashlib.sha256).hexdigest()


def margin_trade(stockCode, orderSide, amount, price='', orderType=BINANCE.ORDER_TYPE_MARKET, isIsolated=BINANCE.IS_ISOLATED_TRUE, timeInForce=BINANCE.TIME_IN_FORCE_GTC, responseType=BINANCE.ORDER_RESPONSE_RESULT):
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



def get_margin_amount(stockCode):
    query = {
        'symbols': stockCode,
        'timestamp': int(time() * 1000)
    }

    signature = get_signature(query)
    query['signature'] = signature

    return requests.get(BINANCE.API_GET_MARGIN_ACCOUNT, query, headers=BINANCE.HEADER_AUTH).json()


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
    

    marginAccount = get_margin_amount(stockCode)



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
        margin_trade(stockCode, newPosition, amount)
        tg_message(newPosition + ' ' + str(amount) + ' UNI at ' + str(currPrice) + ' BTC')
        BINANCE.position = newPosition






