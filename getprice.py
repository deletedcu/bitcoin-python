import requests
from flask import Flask

app = Flask(__name__)

startAppInput = input('Do you want to start the app? (y/n) ')

API_url = "https://bitpay.com/api/rates/usd"

if startAppInput == "y":
    request = requests.get(API_url)
    request = request.json()

    price = request["rate"]

    # This line will be executed to provide support for older Python 3 versions
    print("\nConsole output: \nCurrent price of one Bitcoin is at: {0:.2f}$".format(price))
    print("API URL: {0}\n".format(API_url))
    print("Flask Output:")

    @app.route("/")
    def runningapp():
        return "Current price of one Bitcoin (1 BTC) is {0:.2f}$".format(price)

    # You can use this if you are using Python 3.6 or newer.
    # print(f'Current price of one Bitcoin is at: {request["rate"]:.2f}$')
else:
    exit(0)

if __name__ == '__main__':
    app.run()
