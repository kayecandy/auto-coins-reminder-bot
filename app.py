from flask import Flask, render_template
import threading
import logging
import os
import atexit
import src.env
from src.binance.consts import BINANCE


from src.binance.binance import get_slope



logging.basicConfig(level=logging.DEBUG if src.env.DEBUG else logging.WARNING)


priceCheckerThread = threading.Thread()

def init_app():
    app = Flask(__name__)

    def interrupt():
        global priceCheckerThread
        logging.warning('CANCEL')
        priceCheckerThread.cancel()

    def price_check():
        global priceCheckerThread

        logging.warning('CALL THREAD!!')
        get_slope(
            os.getenv('GRAPH_STOCK'),
            limit=int(os.getenv('GRAPH_MA_7')),
            limitBase=int(os.getenv('GRAPH_MA_25')),
            interval=getattr(BINANCE, os.getenv('GRAPH_CANDLE_INTERVAL'))
        )

        priceCheckerThread = threading.Timer(int(os.getenv('GRAPH_REQUEST_INTERVAL')), price_check)
        priceCheckerThread.start()

    def init():
        global priceCheckerThread


        price_check()



    init()
    atexit.register(interrupt)
    return app



app = init_app()

if __name__ == '__main__':
    app.run(debug=src.env.DEBUG)

# Routes
import routes


