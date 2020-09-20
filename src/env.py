import os
import logging


if os.getenv('BINANCE_KEY') == None:
    from dotenv import load_dotenv
    load_dotenv(override=True)

DEBUG = os.getenv('DEBUG') == 'True'