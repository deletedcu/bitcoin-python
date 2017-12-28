import eventlet
eventlet.monkey_patch()

import requests

from flask_socketio import Namespace, SocketIO, emit, disconnect
from flask import Flask, jsonify, render_template, request
from time import sleep
from threading import Thread, Event, Lock


# Variables

VERSION = "2.4.4"
CHANGELOG = VERSION + " - fix: requests issue with eventlet and monkey_patch"

async_mode = None

# You can use this if you are using Python 3.6 or newer.
# print(f'Current price of one Bitcoin is at: {request["rate"]:.2f}$')

# Creating the app

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret!"
socketio = SocketIO(app, async_mode=async_mode)

# API URL of the API used in this project
bitpay_url = "https://bitpay.com/api/rates"

# data[2] is EUR
# data[1] is USD

appstarted_bitpay_request = requests.get(bitpay_url)
appstarted_bitpay_data = appstarted_bitpay_request.json()

bitpay_EUR = appstarted_bitpay_data[2]
bitpay_USD = appstarted_bitpay_data[1]

appstarted_bitpay_price = "{0:.2f} {1}".format(bitpay_EUR["rate"], bitpay_EUR["code"])

# Price thread
thread = None
thread_lock = Lock()


def background_thread():
    print("Socket -> Requesting price from BitPay")
    while True:
        socketio.sleep(60)
        bitpaydata = requests.get(bitpay_url)
        bitpaydata = bitpaydata.json()

        bitpay_EUR = bitpaydata[2]
        bitpay_USD = bitpaydata[1]

        bitpayprice = "{0:.2f} {1}".format(bitpay_EUR["rate"], bitpay_EUR["code"])

        print("Socket -> Bitpay request -> BitPay price: " + bitpayprice)
        socketio.emit('price_message', {'price': bitpayprice}, namespace='/price')
        socketio.emit('server_message', {'data': 'Price response sent to client!'}, namespace='/price')

        global appstarted_bitpay_price
        appstarted_bitpay_price = "{0:.2f} {1}".format(bitpay_EUR["rate"], bitpay_EUR["code"])


@app.route("/")
def home():
    return render_template('index.html',
                           api=bitpay_url,
                           version=VERSION,
                           price=appstarted_bitpay_price)


@app.route("/ping")
def ping():
    return jsonify(ping='pong')


@app.route("/raw")
def rawoutput():
    bitpaydata = requests.get(bitpay_url)
    bitpaydata = bitpaydata.json()

    bitpay_EUR = bitpaydata[2]
    bitpay_USD = bitpaydata[1]

    bitpayprice = "{0:.2f} {1}".format(bitpay_EUR["rate"], bitpay_EUR["code"])

    return jsonify(api=bitpay_url,
                   currency=bitpay_EUR['name'],
                   currencycode=bitpay_EUR,
                   price=bitpayprice,
                   version=VERSION)


@app.route("/raw_exchanges_rates")
def rawexchangeoutput():
    return requestingexchanges()


@socketio.on('connect', namespace='/price')
def test_connect():
    global thread
    print('Client connected', request.sid)
    emit('server_message', {'data': "Socket works! You are connected!"})
    emit('server_message', {'data': "You will get now a price update every minute!"})
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)
            print('Thread started!')
            emit('server_message', {'data': 'Background task started!'})


@socketio.on('disconnect', namespace='/price')
def test_disconnect():
    print('Client disconnected', request.sid)


@socketio.on('client_message', namespace='/price')
def handle_client_message(message):
    print("Message from the client " + request.sid + ": " + message['data'])


@socketio.on_error()  # Handles the default namespace
def error_handler_default(e):
    print("Default error handler")
    print(e)
    pass


@socketio.on_error('/price')  # handles the '/price' namespace
def error_handler_price(e):
    print("/price error handler")
    print(e)
    pass


def requestingexchanges():
    bitfinex_url = "https://api.bitfinex.com/v1/pubticker/btcusd"
    coinmarketcap_url = "https://api.coinmarketcap.com/v1/ticker/bitcoin/"

    print("> Starting BitFinex Request")
    bitfinex_request = requests.get(bitfinex_url)
    bitfinex_data = bitfinex_request.json()
    bitfinex_price = "{0:.2f}".format(float(bitfinex_data["high"]))
    print("> BitFinex Request worked! ({0})\n".format(bitfinex_price))

    print("> Starting BitPay Request")
    bitpay_request = requests.get(bitpay_url)
    bitpay_data = bitpay_request.json()

    bitpay_EUR = bitpay_data[2]
    bitpay_USD = bitpay_data[1]

    bitpay_price = "{0:.2f}".format(bitpay_EUR["rate"])
    print("> BitPay Request worked! ({0})\n".format(bitpay_price))

    print("> Starting CoinMarketCap Request")
    coinmarketcap_request = requests.get(coinmarketcap_url)
    coinmarketcap_data = coinmarketcap_request.json()
    coinmarketcap_price = "{0:.2f}".format(float(coinmarketcap_data[0]["price_usd"]))
    print("> CoinMarketCap Request worked! ({0})\n\nAll requests worked fine!".format(coinmarketcap_price))

    return jsonify(_code="USD",
                   version=VERSION,
                   bitfinex=bitfinex_price,
                   bitpay=bitpay_price,
                   coinmarketcap=coinmarketcap_price)


if __name__ == '__main__':
    socketio.run(app, port=5000)
