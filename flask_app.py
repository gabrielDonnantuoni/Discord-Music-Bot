from flask import Flask
from threading import Thread

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return 'App running on fire!'


def run():
    app.run('0.0.0.0', port=8080)


def go_live():
    thread = Thread(target=run)
    thread.start()
