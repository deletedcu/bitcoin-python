import requests

request = requests.get("https://bitpay.com/api/rates/usd")
request = request.json()

print(f'Current price of one Bitcoin is at: {request["rate"]:.2f}$')
