import eventlet
eventlet.sleep()
eventlet.monkey_patch()

import requests

from flask_socketio import Namespace, SocketIO, emit, disconnect
from flask import Flask, jsonify, render_template, request
from time import sleep
from threading import Thread, Event, Lock


# Variables

VERSION = "2.6.0"
CHANGELOG = VERSION + " - new: Showing the price in the title\n" \
                      + VERSION + " - new: Contribute button in the settings menu"

# PORT
PORT = 5000

async_mode = None

# You can use this if you are using Python 3.6 or newer.
# print(f'Current price of one Bitcoin is at: {request["rate"]:.2f}$')

# Creating the app

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret!"
socketio = SocketIO(app, async_mode=async_mode)

# API URL of the API used in this project
bitpay_url = "https://bitpay.com/api/rates"

# data[3] is EUR
# data[2] is USD

appstarted_bitpay_request = requests.get(bitpay_url)
appstarted_bitpay_data = appstarted_bitpay_request.json()

bitpay_EUR = appstarted_bitpay_data[3]
bitpay_USD = appstarted_bitpay_data[2]

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

        bitpay_EUR = bitpaydata[3]
        bitpay_USD = bitpaydata[2]

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

    bitpay_EUR = bitpaydata[3]
    bitpay_USD = bitpaydata[2]

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

    # URIs of the other exchanges
    bitfinex_url = "https://api.bitfinex.com/v1/pubticker/btcusd"
    coinmarketcap_url = "https://api.coinmarketcap.com/v1/ticker/bitcoin/"

    # Logging the start of the BitFinex request
    print("> Starting BitFinex Request")

    # Getting the price from BitFinex
    bitfinex_request = requests.get(bitfinex_url)
    bitfinex_data = bitfinex_request.json()
    bitfinex_price = "{0:.2f}".format(float(bitfinex_data["high"]))

    # Log if successful
    print("> BitFinex Request worked! ({0})\n".format(bitfinex_price))

    # Logging the start of the BitPay request
    print("> Starting BitPay Request")

    # Get the data from BitPay
    bitpay_request = requests.get(bitpay_url)
    bitpay_data = bitpay_request.json()

    # Creating variables for different currencies containing different data
    bitpay_EUR = bitpay_data[3]
    bitpay_USD = bitpay_data[2]

    # Log if successful
    print("> BitPay Request worked! \n")

    print("> Starting CoinMarketCap Request")
    coinmarketcap_request = requests.get(coinmarketcap_url)
    coinmarketcap_data = coinmarketcap_request.json()
    coinmarketcap_price = "{0:.2f}".format(float(coinmarketcap_data[0]["price_usd"]))
    # Log if successful
    print("> CoinMarketCap Request worked! ({0})\n\nAll requests worked fine!".format(coinmarketcap_price))

    # Creating a variable with the final results
    result = jsonify({
        "bitfinex": {
            "name": "BitFinex",
            "url": bitfinex_url,
            "currencyCode": "USD",
            "price": bitfinex_price
        },
        "bitpay": {
            "name": "BitPay",
            "url": bitpay_url,
            "USD": bitpay_USD,
            "EUR": bitpay_EUR
        },
        "coinmarketcap": {
            "name": "CoinMarketCap",
            "url": coinmarketcap_url,
            "currencyCode": "USD",
            "price": coinmarketcap_price
        }
    })

    # Returning the result
    return result


if __name__ == '__main__':
    socketio.run(app, port=PORT)
