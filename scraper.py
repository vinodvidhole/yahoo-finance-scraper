import requests

YAHOO_FINANCE_URL = 'https://finance.yahoo.com/trending-tickers'

response = requests.get(YAHOO_FINANCE_URL)

print('Status Code ', response.status_code)

with open('trending-tickers.html','w') as f:
  f.write(response.text)
  