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
    
  #VALUE_EXPRESSION='//table[@class="W(100%)"]//tr' for row count
  TABLE_CLASS = "W(100%)"
  ROW = 3
  EXPRESSION_ROWCOUNT = "//table[@class= '{}']/tbody/tr".format(TABLE_CLASS)
  EXPRESSION_COLUMN = "//*[@class= '{}']/tbody/tr[{}]/td".format(TABLE_CLASS,ROW)
  #VALUE_EXPRESSION = "//*[@class= '{}']/tbody/tr[1]/th".format(TABLE_CLASS,ROW)
   
  # to identify the table rows
  r = driver.find_elements(By.XPATH, value="//table[@class= '{}']/tbody/tr".format(TABLE_CLASS))
  # to identify table columns
  c = driver.find_elements(By.XPATH, value="//*[@class= '{}']/tbody/tr[1]/td".format(TABLE_CLASS))
  # to get row count with len method
  rc = len (r)
  print('rc ', rc)
  
  # to get column count with len method
  cc = len (c)
  print('c ', cc)
  
  # to traverse through the table rows excluding headers
  for i in range (2, rc + 1) :
    # to traverse through the table column
    for j in range (1, cc + 1) :
    # to get all the cell data with text method
      d = driver.find_element(By.XPATH, value="//tr["+str(i)+"]/td["+str(j)+"]").text
      print(j)
      print (d)

print("End")