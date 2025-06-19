import requests
from bs4 import BeautifulSoup

import internal

url = 'https://api.coingecko.com/api/v3/simple/price'

params = {
    'ids': 'bitcoin',
    'vs_currencies': 'usd',
}

API_KEY = internal.get_internal()
headers = { 'x-cg-demo-api-key': API_KEY }

response = requests.get(url, params = params)

if response.status_code == 200:
    data = response.json()
    Bitcoin_price = data['bitcoin']['usd']
    print(f'The price of Bitcoin in USD is ${Bitcoin_price}')
else:
    print('Failed to retrieve data from the API')