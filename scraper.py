from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


YAHOO_FINANCE_URL = 'https://finance.yahoo.com/trending-tickers'

def get_driver():
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  chrome_options.add_argument('--headless')
  driver = webdriver.Chrome(options=chrome_options)
  return driver

if __name__ == "__main__":
  print('Creating Driver')
  driver = get_driver();

  print('Fetching the page')
  driver.get(YAHOO_FINANCE_URL)
  print('Page title:', driver.title)

  #TICKER_TABLE_CLASS = "W(100%)"
  
  #ticker_table  = driver.find_element_by_class_name(TICKER_TABLE_CLASS)
  #ticker_table = driver.find_element(By.CLASS_NAME, TICKER_TABLE_CLASS)

  for row in driver.find_elements(By.XPATH, value='//table[@class="W(100%)"]//tr'):
    #print(row.get_attribute('id'))
    print(row.text)
    
  #print(f'Found {len(ticker_table)} table')

print("End")