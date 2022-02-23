import requests
from bs4 import BeautifulSoup

YAHOO_FINANCE_URL = 'https://finance.yahoo.com/trending-tickers'


response = requests.get(YAHOO_FINANCE_URL)

print('Status Code ', response.status_code)

with open('trending-tickers.html','w') as f:
  f.write(response.text)

doc = BeautifulSoup(response.text, 'html.parser')
print('Page title : ', doc.title.text)

ticker_div = doc.find_all('div', id = 'list-res-table')

ticker_table  = doc.find_all('table', class_ = "W(100%)")
#print(ticker_table)
table_rows = ticker_table.find('tr', class_ = "simpTblRow Bgc($hoverBgColor):h BdB Bdbc($seperatorColor) Bdbc($tableBorderBlue):h H(32px) Bgc($lv2BgColor) ")

print(f'Found {len(table_rows)} tickers')

