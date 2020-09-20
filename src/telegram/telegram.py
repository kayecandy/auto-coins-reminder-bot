import requests
from src.telegram.consts import TELEGRAM


def tg_message(msg):
    for userId in TELEGRAM.IDS:
        requests.get(TELEGRAM.API_SEND_MESSAGE, {
            'chat_id'   : userId,
            'text'      : msg
        })