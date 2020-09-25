from flask import Flask
import logging
import src.env





logging.basicConfig(level=logging.DEBUG if src.env.DEBUG else logging.WARNING)


app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=src.env.DEBUG)


# Routes
import routes


