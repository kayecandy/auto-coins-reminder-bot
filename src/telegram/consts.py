import os
import src.env
import logging

class TELEGRAM:

    API_BASE = os.getenv('TELEGRAM_URL_BASE') + os.getenv('TELEGRAM_SECRET')

    API_SEND_MESSAGE = API_BASE + '/sendMessage'


    IDS = [
        504017547      # ME
        # 695610152,      # Kuya
        # 563219073       # Ely

    ]

    PARSE_MODE_MARKDOWN_V2 = 'MarkdownV2'
    PARSE_MODE_HTML = 'HTML'