#1
import requests
from bs4 import BeautifulSoup
import pandas as pd

#2
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

#3
import re
import json
from io import StringIO
from IPython.display import display

BASE_URL = 'https://finance.yahoo.com' #Global Variable 

#1
def get_page(url):
    """Download a webpage and return a beautiful soup doc"""
    response = requests.get(url)
    if not response.ok:
        print('Status code:', response.status_code)
        raise Exception('Failed to load page {}'.format(url))
    doc = BeautifulSoup(response.text, 'html.parser')
    return doc

def get_news_tags(doc):
    """Get the list of tags containing news information"""
    news_class = "Ov(h) Pend(44px) Pstart(25px)" ## class name of div tag 
    news_list  = doc.find_all('div', {'class': news_class})
    return news_list

def parse_news(news_tag):
    """Get the news data point and return dictionary"""
    news_source = news_tag.find('div').text #source
    news_headline = news_tag.find('a').text #heading
    news_url = news_tag.find('a')['href'] #link
    news_content = news_tag.find('p').text #content
    news_image = news_tag.findParent().find('img')['src'] #thumb image
    return { 'source' : news_source,
            'headline' : news_headline,
            'url' : BASE_URL + news_url,
            'content' : news_content,
            'image' : news_image
           }

def scrape_yahoo_news(url, path=None):
    """Get the yahoo finance market news and write them to CSV file """
    if path is None:
        path = 'stock-market-news.csv'
        
    print('Requesting html page')
    doc = get_page(url)
    print('Extracting news tags')
    news_list = get_news_tags(doc)
    print('Parsing news tags')
    news_data = [parse_news(news_tag) for news_tag in news_list]
    print('Save the data to a CSV')
    news_df = pd.DataFrame(news_data)
    news_df.to_csv(path, index=None)
    #This return statement is optional, we are doing this just analyze the final output 
    display(news_df.head())
    return news_df 

#2
def get_driver(url):
    """Return web driver"""
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--headless')
    #serv = Service(ChromeDriverManager().install())
    serv = Service(os.getcwd()+'/chromedriver')
    driver = webdriver.Chrome(options=chrome_options, service=serv)
    driver.get(url)
    return driver

def get_table_header(driver):
    """Return Table columns in list form """
    header = driver.find_elements(By.TAG_NAME, value= 'th')
    header_list = [item.text for index, item in enumerate(header) if index < 10]
    return header_list

def get_table_rows(driver):
    """Get number of rows available on the page """
    tablerows = len(driver.find_elements(By.XPATH, value='//*[@id="scr-res-table"]/div[1]/table/tbody/tr'))
    return tablerows    

def parse_table_rows(rownum, driver, header_list):
    """get the data for one row at a time and return column value in the form of dictionary"""
    row_dictionary = {}
    #time.sleep(1/3)
    for index , item in enumerate(header_list):
        time.sleep(1/20)
        column_xpath = '//*[@id="scr-res-table"]/div[1]/table/tbody/tr[{}]/td[{}]'.format(rownum, index+1)
        row_dictionary[item] = driver.find_element(By.XPATH, value=column_xpath).text
    return row_dictionary

def parse_multiple_pages(driver, total_crypto):
    """Loop through each row, perform Next button click at the end of page 
    return total_crypto numbers of rows 
    """
    table_data = []
    page_num = 1
    is_scraping = True
    header_list = get_table_header(driver)

    while is_scraping:
        table_rows = get_table_rows(driver)
        print('Found {} rows on Page : {}'.format(table_rows, page_num))
        print('Parsing Page : {}'.format(page_num))
        table_data += [parse_table_rows(i, driver, header_list) for i in range (1, table_rows + 1)]
        total_count = len(table_data)
        print('Total rows scraped : {}'.format(total_count))
        if total_count >= total_crypto:
            print('Done Parsing..')
            is_scraping = False
        else:    
            print('Clicking Next Button')
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="scr-res-table"]/div[2]/button[3]')))
            element.click() 
            page_num += 1
    return table_data

def scrape_yahoo_crypto(url, total_crypto, path=None):
    """Get the list of yahoo finance crypto-currencies and write them to CSV file """
    if path is None:
        path = 'crypto-currencies.csv'
    print('Creating driver')
    driver = get_driver(url)    
    table_data = parse_multiple_pages(driver, total_crypto)
    driver.close()
    print('Save the data to a CSV')
    table_df = pd.DataFrame(table_data)
    #print(table_df)
    table_df.to_csv(path, index=None)
    #This return statement is optional, we are doing this just analyze the final output 
    display(table_df.head())
    return table_df 

#3
def get_event_page(scraper_url):
    """Download a webpage and return a beautiful soup doc"""
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                  "(KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
    }
    response = requests.get(scraper_url, headers=headers)
    if not response.ok:
        print('Status code:', response.status_code)
        raise Exception('Failed to fetch web page ' + scraper_url)
    # Construct a beautiful soup document
    doc = BeautifulSoup(response.text, 'html.parser')
    return doc

def get_json_dictionary(doc):
    """Get Json formated data in the form of Python Dictionary"""
    pattern = re.compile(r'\s--\sData\s--\s')
    script_data = doc.find('script', text=pattern).text
    script_data = doc.find('script', text=pattern).contents[0]
    
    start  = script_data.find('context')-2
    json_text  = script_data[start:-12]
    
    parsed_dictionary = json.loads(json_text)
    return parsed_dictionary    

def get_total_rows(parsed_dictionary):
    '''Get the Total Rows for the search criteria & Columns detail''' 
    total_rows = parsed_dictionary['context']['dispatcher']['stores']['ScreenerResultsStore']['results']['total']
    return total_rows

def get_page_rows(parsed_dictionary):
    """Get the Content current page"""    
    data_dictionary = parsed_dictionary['context']['dispatcher']['stores']['ScreenerResultsStore']['results']['rows']
    return data_dictionary

def scrape_all_pages(event_type, date):
    """Loop through each row and return lists of data dictiionary"""
    YAHOO_CAL_URL = BASE_URL+'/calendar/{}?day={}&offset={}&size={}'
    max_rows_per_page = '100' # this indicates max rows per page 
    page_number = 1
    final_data_dictionary = []
    
    while page_number > 0:
        print("Processing page # {}".format(page_number))
        page_url = str((page_number - 1 ) * int(max_rows_per_page))
        scrape_url = YAHOO_CAL_URL.format(event_type, date, page_url, max_rows_per_page)
        print("Scrape url for page {} is {}".format(page_number,scrape_url))
        page_doc = get_event_page(scrape_url)
        parse_dict = get_json_dictionary(page_doc)
        if page_number == 1:
            total_rows = get_total_rows(parse_dict)        
        final_data_dictionary += get_page_rows(parse_dict)
        if len(final_data_dictionary) >= total_rows:
            page_number = 0
            return final_data_dictionary
        page_number += 1

def scrape_yahoo_calendar(event_types, date_param):
    """Get the list of yahoo finance calendar and write them to CSV file """
    for event in event_types:
        data_dict = {}
        print('Web Scraping for ', event  )
        data_dict = scrape_all_pages(event, date_param)
        if len(data_dict) > 0:
            scraped_df = pd.DataFrame(data_dict)
            scraped_df.to_csv(event+'_'+date_param+'.csv',index=False)
            print("checking few rows.. for event : {} & date : {}".format(event, date_param))
            display(scraped_df.head())
        else:
            print("No data found for event : {} & date : {}".format(event, date_param))

def send_email(body):
  try:
    server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server_ssl.ehlo()   

    SENDER_EMAIL = 'sendsometrends@gmail.com'
    RECEIVER_EMAIL = 'sendsometrends@gmail.com'
    SENDER_PASSWORD = os.environ['GMAIL_PASSWORD']
    
    subject = 'YouTube Trending Videos'

    email_text = f"""
    From: {SENDER_EMAIL}
    To: {RECEIVER_EMAIL}
    Subject: {subject}
    {body}
    """

    server_ssl.login(SENDER_EMAIL, SENDER_PASSWORD)
    server_ssl.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, email_text)
    server_ssl.close()

  except:
      print('Something went wrong...')

if __name__ == "__main__" :

    YAHOO_NEWS_URL = BASE_URL+'/topic/stock-market-news/'
    news_df = scrape_yahoo_news(YAHOO_NEWS_URL)

    YAHOO_FINANCE_URL = BASE_URL+'/cryptocurrencies'
    TOTAL_CRYPTO = 50
    crypto_df = scrape_yahoo_crypto(YAHOO_FINANCE_URL, TOTAL_CRYPTO,'crypto-currencies.csv')

    #date_param = '2022-03-18' # no data condition
    date_param = '2022-02-28'
    event_types = ['splits','economic','ipo','earnings']
    scrape_yahoo_calendar(event_types, date_param)

print("Processing Done")
