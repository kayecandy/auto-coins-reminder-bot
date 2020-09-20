import os
import logging
import src.env


class BINANCE:

    previous = -1
    position = ''

    API_KEY = os.getenv('BINANCE_KEY')
    API_SECRET = os.getenv('BINANCE_SECRET')

    API_BASE = os.getenv('BINANCE_URL_BASE') + os.getenv('BINANCE_URL_PATH')
    API_BASE_MARGIN = os.getenv('BINANCE_URL_BASE') + os.getenv('BINANCE_URL_PATH_MARGIN')

    API_GET_SYMBOL_PRICES = str(API_BASE) + '/trades'
    API_GET_SYMBOL_KLINES = str(API_BASE) + '/klines'
    API_GET_PRICE = str(API_BASE) + '/ticker/price'

    API_ORDER_MARGIN = str(API_BASE_MARGIN) + '/margin/order'
    API_GET_MARGIN_ACCOUNT = str(API_BASE_MARGIN) + '/margin/isolated/account'

    HEADER_AUTH = {
        'Content-Type'  : 'application/x-www-form-urlencoded',
        'X-MBX-APIKEY'  : API_KEY
    }

    IS_ISOLATED_TRUE = 'TRUE'
    IS_ISOLATED_FALSE = 'FALSE'

    KLINE_OPEN = 1
    KLINE_HIGH = 2
    KLINE_LOW = 3
    KLINE_CLOSE = 4

    INTERVAL_MIN1 = '1m' 
    INTERVAL_MIN3 = '3m'
    INTERVAL_MIN5 = '5m'
    INTERVAL_MIN15 = '15m'
    INTERVAL_MIN30 = '30m'
    INTERVAL_HOUR1 = '1h'
    INTERVAL_HOUR2 = '2h'
    INTERVAL_HOUR4 = '4h'
    INTERVAL_HOUR6 = '6h'
    INTERVAL_HOUR8 = '8h'
    INTERVAL_HOUR12 = '12h'
    INTERVAL_DAY1 = '1d'
    INTERVAL_DAY3 = '3d'
    INTERVAL_WEEK1 = '1w'
    INTERVAL_MONTH1 = '1M'

    ORDER_TYPE_MARKET = 'MARKET'
    ORDER_TYPE_LIMIT = 'LIMIT'

    ORDER_RESPONSE_ACK = 'ACK'
    ORDER_RESPONSE_RESULT = 'RESULT'
    ORDER_RESPONSE_FULL = 'FULL'

    ORDER_SIDE_BUY = 'BUY'
    ORDER_SIDE_SELL = 'SELL'

    TIME_IN_FORCE_GTC = 'GTC'
    TIME_IN_FORCE_IOC = 'IOC'
    TIME_IN_FORCE_FOK = 'FOK'

    