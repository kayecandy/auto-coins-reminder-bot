import os
import threading
import logging
from src.binance.binance import price_check
from src.telegram.telegram import tg_message
import src.env


logging.basicConfig(level=logging.DEBUG if src.env.DEBUG else logging.WARNING)

def price_check_continous():
    try:
        price_check()
    except Exception as e:
        logging.debug('TEST' + str(e))
        tg_message('API ERROR!! Check logs')
    finally:
        threading.Timer(int(os.getenv('GRAPH_REQUEST_INTERVAL')), price_check_continous).start()




price_check_continous()
