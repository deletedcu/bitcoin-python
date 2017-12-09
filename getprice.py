import requests

startAppInput = input('Do you want to start the app? (y/n) ')

if startAppInput == "y":
    request = requests.get("https://bitpay.com/api/rates/usd")
    request = request.json()

    # This line will be executed to provide support for older Python 3 versions
    print("Current price of one Bitcoin is at: {0:.2f}$".format(request["rate"]))

    # You can use this if you are using Python 3.6 or newer.
    # print(f'Current price of one Bitcoin is at: {request["rate"]:.2f}$')
else:
    exit(0)
