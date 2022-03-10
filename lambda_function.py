try:
    import json
    from selenium.webdriver import Chrome
    from selenium.webdriver.chrome.options import Options
    import os
    import shutil
    import uuid
    import boto3
    from datetime import datetime
    import datetime
    from selenium.webdriver.common.by import By
    import smtplib
    import time


    print("All Modules are ok ...")

except Exception as e:

    print("Error in Imports ")


YAHOO_FINANCE_URL = "https://finance.yahoo.com/trending-tickers"

class WebDriver(object):

    def __init__(self):
        self.options = Options()

        self.options.binary_location = '/opt/headless-chromium'
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--start-maximized')
        self.options.add_argument('--start-fullscreen')
        self.options.add_argument('--single-process')
        self.options.add_argument('--disable-dev-shm-usage')

    def get(self):
        driver = Chrome('/opt/chromedriver', options=self.options)
        return driver

def parse_ticker(rownum, table_driver):
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

def get_tickers(driver):
    TABLE_CLASS = "W(100%)"  
    tablerows = len(driver.find_elements(By.XPATH, value="//table[@class= '{}']/tbody/tr".format(TABLE_CLASS)))
    return tablerows

def send_email(body):
    try:
        server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server_ssl.ehlo()   
    
        SENDER_EMAIL = os.environ['SENDER_EMAIL'] 
        RECEIVER_EMAIL = os.environ['RECEIVER_EMAIL']
        SENDER_PASSWORD = os.environ['PASSWORD']
        
        subject = 'Yahoo! Finance web scraping'
    
        email_text = f"""
        From: {SENDER_EMAIL}
        To: {RECEIVER_EMAIL}
        Subject: {subject}
        {body}
        """
    
        server_ssl.login(SENDER_EMAIL, os.environ['PASSWORD'])
        server_ssl.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, email_text)
        server_ssl.close()
        
    except:
        print('Something went wrong...')


def lambda_handler(event, context):
    #table_rows = 0
    #table_data = 'Hi'
    
    instance_ = WebDriver()
    driver = instance_.get()
    driver.get("https://finance.yahoo.com/trending-tickers")
  
    table_data = driver.title
    print('Fetching the page')
    table_rows = get_tickers(driver)
    print(f'Found {table_rows} Tickers')
    print('Parsing Trending tickers')
    table_data = [parse_ticker(i, driver) for i in range (1, table_rows + 1)]
    
    driver.close()
    driver.quit()
    
    email_body = json.dumps(table_data)

    send_email(email_body)

    response = {
        "statusCode": 200,
        "Rows": table_rows,
        "body": table_data
    }

    return response
    
if __name__ == "__main__":
    lambda_handler(None, None)