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
  
def get_table(driver):
    TABLE_CLASS = "W(100%)"  
    driver.get(YAHOO_FINANCE_URL)
    tablerows = len(driver.find_elements(By.XPATH, value="//table[@class= '{}']/tbody/tr".format(TABLE_CLASS)))
    return tablerows
  
def parse_table(table_driver):
  Symbol = table_driver.find_element(By.XPATH, value="//tr[{}]/td[1]".format(i)).text
  Name = table_driver.find_element(By.XPATH, value="//tr[{}]/td[2]".format(i)).text
  LastPrice = table_driver.find_element(By.XPATH, value="//tr[{}]/td[3]".format(i)).text
  MarketTime = table_driver.find_element(By.XPATH, value="//tr[{}]/td[4]".format(i)).text
  Change = table_driver.find_element(By.XPATH, value="//tr[{}]/td[5]".format(i)).text
  PercentChange = table_driver.find_element(By.XPATH, value="//tr[{}]/td[6]".format(i)).text	
  Volume = table_driver.find_element(By.XPATH, value="//tr[{}]/td[7]".format(i)).text
  MarketCap = table_driver.find_element(By.XPATH, value="//tr[{}]/td[8]".format(i)).text	

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
  
  #VALUE_EXPRESSION='//table[@class="W(100%)"]//tr' for row count
  TABLE_CLASS = "W(100%)"
  
  # to identify the table rows
  r = driver.find_elements(By.XPATH, value="//table[@class= '{}']/tbody/tr".format(TABLE_CLASS))
  # to identify table columns
  #c = driver.find_elements(By.XPATH, value="//*[@class= '{}']/tbody/tr[1]/td".format(TABLE_CLASS))
  # to get row count with len method
  rc = len (r)
  print('rc ', rc)
  
  # to get column count with len method
  #cc = len (c)
  #print('c ', cc)
  
  # to traverse through the table rows excluding headers
  for i in range (2, table_rows + 1) :
    print(i)
    # to traverse through the table column
    """    
    for j in range (1, cc + 1) :
    # to get all the cell data with text method
      d = driver.find_element(By.XPATH, value="//tr["+str(i)+"]/td["+str(j)+"]").text
      print(i, j)
      print (d)
    """



print("End")
