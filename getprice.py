import requests

startAppInput = input('Do you want to start the app? (y/n) ')

if startAppInput == "y":
    request = requests.get("https://bitpay.com/api/rates/usd")
    request = request.json()

    print(f'Current price of one Bitcoin is at: {request["rate"]:.2f}$')
else:
    exit(0)
