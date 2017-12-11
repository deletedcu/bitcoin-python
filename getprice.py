import requests
from flask import Flask, jsonify
from flask import render_template

version = "1.0.0"

API_url = "https://bitpay.com/api/rates/usd"

data = requests.get(API_url)
data = data.json()

price = data["rate"]
price = "{0:.2f}".format(price)
# This line will be executed to provide support for older Python 3 versions
print("\nConsole output: \nCurrent price of one Bitcoin is at: {0}$".format(price))
print("API URL: {0}\n".format(API_url))
print("Flask Output:")

# You can use this if you are using Python 3.6 or newer.
# print(f'Current price of one Bitcoin is at: {request["rate"]:.2f}$')


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def runningapp():
        with app.app_context():
            return render_template('index.html', version=version, price=price, api=API_url)

    @app.route("/ping")
    def ping():
        return jsonify(ping='pong')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(port=5000)
