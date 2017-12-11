import requests
from flask import Flask, jsonify
from flask import render_template

# Variables
# Version of the app
version = "1.0.0-12"

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

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(port=5000)
