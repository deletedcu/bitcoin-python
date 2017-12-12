import requests
from flask import Flask, jsonify
from flask import render_template

# Variables
# Version of the app
# <major>.<minor>.<patch>-<total commits>
version = "1.1.0-21"

# API URL of the API used in this project
API_url = "https://bitpay.com/api/rates/usd"

# Accessing JSON data
data = requests.get(API_url)
data = data.json()

# Price in a single variable
price = data["rate"]
price = "{0:.2f}".format(price)

# This line will be executed to provide support for older Python 3 versions
print("\nConsole output: \nCurrent price of one Bitcoin is at: {0}$".format(price))
print("API URL: {0}\n".format(API_url))
print("Flask Output:")

# You can use this if you are using Python 3.6 or newer.
# print(f'Current price of one Bitcoin is at: {request["rate"]:.2f}$')

# Creating the app


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def home():
        return render_template('index.html', version=version, price=price, api=API_url)

    @app.route("/ping")
    def ping():
        return jsonify(ping='pong')

    @app.route("/raw")
    def rawoutput():
        return jsonify(api=API_url, currency=data['name'], currencycode=data['code'], price=price, version=version)

    @app.route("/raw_exchanges_rates")
    def rawexchangeoutput():
        return requestingexchanges()

    return app


def requestingexchanges():
    bitfinex_url = "https://api.bitfinex.com/v1/pubticker/btcusd"
    coinmarketcap_url = "https://api.coinmarketcap.com/v1/ticker/bitcoin/"

    print("> Starting BitFinex Request")
    bitfinex_request = requests.get(bitfinex_url)
    bitfinex_data = bitfinex_request.json()
    bitfinex_price = "{0:.2f}".format(float(bitfinex_data["high"]))
    print("> BitFinex Request worked! ({0})\n".format(bitfinex_price))

    print("> Starting BitPay Request")
    bitpay_price = price
    print("> BitPay Request worked! ({0})\n".format(price))

    print("> Starting CoinMarketCap Request")
    coinmarketcap_request = requests.get(coinmarketcap_url)
    coinmarketcap_data = coinmarketcap_request.json()
    coinmarketcap_price = "{0:.2f}".format(float(coinmarketcap_data[0]["price_usd"]))
    print("> CoinMarketCap Request worked! ({0})\n\nAll requests worked fine!".format(coinmarketcap_price))

    return jsonify(_code="USD",
                   version=version,
                   bitfinex=bitfinex_price,
                   bitpay=bitpay_price,
                   coinmarketcap=coinmarketcap_price)


if __name__ == '__main__':
    app = create_app()
    app.run(port=5000)
