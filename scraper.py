from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd 

YAHOO_FINANCE_URL = 'https://finance.yahoo.com/trending-tickers'

def get_driver():
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  chrome_options.add_argument('--headless')
  driver = webdriver.Chrome(options=chrome_options)
  return driver
  
def get_table(driver):
    TABLE_CLASS = "W(100%)"  
    driver.get(YAHOO_FINANCE_URL)
    tablerows = len(driver.find_elements(By.XPATH, value="//table[@class= '{}']/tbody/tr".format(TABLE_CLASS)))
    return tablerows
  
def parse_table(rownum, table_driver):
  Symbol = table_driver.find_element(By.XPATH, value="//tr[{}]/td[1]".format(rownum)).text
  Name = table_driver.find_element(By.XPATH, value="//tr[{}]/td[2]".format(rownum)).text
  LastPrice = table_driver.find_element(By.XPATH, value="//tr[{}]/td[3]".format(rownum)).text
  MarketTime = table_driver.find_element(By.XPATH, value="//tr[{}]/td[4]".format(rownum)).text
  Change = table_driver.find_element(By.XPATH, value="//tr[{}]/td[5]".format(rownum)).text
  PercentChange = table_driver.find_element(By.XPATH, value="//tr[{}]/td[6]".format(rownum)).text	
  Volume = table_driver.find_element(By.XPATH, value="//tr[{}]/td[7]".format(rownum)).text
  MarketCap = table_driver.find_element(By.XPATH, value="//tr[{}]/td[8]".format(rownum)).text	

  return {
  'Symbol': Symbol,
  'Name': Name,
  'LastPrice': LastPrice,
  'MarketTime': MarketTime,
  'Change': Change,
  'PercentChange': PercentChange,
  'Volume': Volume,
  'MarketCap': MarketCap
  }
    
if __name__ == "__main__" :
  print('Creating driver')
  driver = get_driver()
  
  print('Fetching the page')
  table_rows = get_table(driver)

  print(f'Found {table_rows} Tickers')
  
  print('Parsing Trending tickers videos')
  ticker_data = [parse_table(i, driver) for i in range (1, table_rows + 1)]

  print('Save the data to a CSV')
  videos_df = pd.DataFrame(ticker_data)
  print(videos_df)
  videos_df.to_csv('trending.csv', index=None)

print("Processing Done")
