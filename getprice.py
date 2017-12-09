import requests
from flask import Flask

app = Flask(__name__)

API_url = "https://bitpay.com/api/rates/usd"

data = requests.get(API_url)
data = data.json()

price = data["rate"]

# This line will be executed to provide support for older Python 3 versions
print("\nConsole output: \nCurrent price of one Bitcoin is at: {0:.2f}$".format(price))
print("API URL: {0}\n".format(API_url))
print("Flask Output:")

# You can use this if you are using Python 3.6 or newer.
# print(f'Current price of one Bitcoin is at: {request["rate"]:.2f}$')


@app.route("/")
def runningapp():
    return "Current price of one Bitcoin (1 BTC) is {0:.2f}$".format(price)


if __name__ == '__main__':
    app.run(port=5000)
