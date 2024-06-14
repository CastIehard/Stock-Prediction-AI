#make this true for cmd output
import requests
import json
from datetime import datetime,timedelta
import re
import os
from my_config import *

def get_folder_size(folder_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)
    return total_size
          
def check_api_error(json_response):
    if "Information" in json_response and "rate limit" in json_response["Information"]:
        return True
    return False
    
def extract_file_name(url):
    match = re.search(r'=(.*?)&', url)
    if match:
        file_name = match.group(1)
        file_name = re.sub(r'[^\w\s]', '', file_name)  # Remove special characters
        file_name = file_name.replace(' ', '_')         
        file_name = file_name.replace('20', '_')       # Empty space in URL is represented as '20'
        file_name = file_name.lower()
    else:
        file_name = 'unknown'
    return file_name
    
yesterday_raw = datetime.now() - timedelta(days=1)
yesterday = yesterday_raw.strftime('%Y%m%d')
yesterday_4_news_api = yesterday_raw.strftime('%Y-%m-%d')

error_counter = 0
#Some Outputs for User
if output_bool:
    print("\n________________________________________")
    print("Overall Information\n")
    print("Date of collection:  " + yesterday_4_news_api)
    print("Stock name:          " + company_name_4_news)
    print("Stock CEO:           " + company_ceo_4_news)
    print("Stock Symbol:        " + stock_symbol)
    print("________________________________________\n")

# Get the current working directory
cwd = os.path.dirname(os.path.abspath(__file__))
# Set the 'directory' variable to the new path
directory = os.path.join(cwd, "Collected_Data")

# Define the list of URLs
url_list = [
    #https://www.alphavantage.co/documentation/    
    #Daily:
    f'https://newsapi.org/v2/everything?q={company_name_4_news}&from={yesterday_4_news_api}&sortBy=publishedAt&apiKey={na_api_key}',  # Adobe news --> daily
    f'https://newsapi.org/v2/everything?q={company_ceo_4_news}&from={yesterday_4_news_api}&sortBy=publishedAt&apiKey={na_api_key}',  # CEO news --> daily    
    f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock_symbol}&apikey={av_api_key}',  # stock data: selected stock open close high low volume --> daily
    f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={stock_symbol}&limit=1000&time_from={yesterday}T0001&time_to={yesterday}T2359&apikey={av_api_key}',  # news sentiment with sentiment score from yesterday --> daily
    #only current rate  
    f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=USD&to_currency=JPY&apikey={av_api_key}',  # currency forex eur to jpy --> daily
    #Monthly
    f'https://www.alphavantage.co/query?function=RETAIL_SALES&apikey={av_api_key}',#retail sales --> monthly
    f'https://www.alphavantage.co/query?function=CPI&interval=monthly&apikey={av_api_key}',  # CPI USA --> monthly
    f'https://www.alphavantage.co/query?function=UNEMPLOYMENT&apikey={av_api_key}',  # unemployment rate --> monthly  
    #Quartely or more
    f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={stock_symbol}&apikey={av_api_key}',  # company overview with ratio, etc. --> quarterly
    f'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={stock_symbol}&apikey={av_api_key}',#-->income statement quartely
    f'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={stock_symbol}&apikey={av_api_key}',#-->balance sheet quartely
    f'https://www.alphavantage.co/query?function=EARNINGS&symbol={stock_symbol}&apikey={av_api_key}', #-->earnings quartely    
    f'https://www.alphavantage.co/query?function=FEDERAL_FUNDS_RATE&interval=daily&apikey={av_api_key}',  # federal funds rate --> 8 times a year
    f'https://www.alphavantage.co/query?function=REAL_GDP&interval=quarterly&apikey={av_api_key}',  # real GDP USA --> yearly
    f'https://www.alphavantage.co/query?function=INFLATION&apikey={av_api_key}'  # inflation USA --> yearly
]

#make yesterday folder    
if not os.path.exists(os.path.join(directory, yesterday)):
        os.makedirs(os.path.join(directory, yesterday))
        if output_bool:
            print("New Folder with name -" + yesterday +"- created.\n")

# Make API requests and save JSON data to files
for url in url_list:
    r = requests.get(url)
    data = r.json()
    file_name = extract_file_name(url)
        
    #test the json data for data limit message
    if check_api_error(data):
        if output_bool:
            print(f"API Error! No data about -{file_name}- collected! ->API Limit reached")
        file_name = f"fail_{file_name}"
        error_counter = error_counter + 1
           
    #get full file path with filename    
    file_path = os.path.join(directory, yesterday, f"{file_name}.json")

    #safe the json data into direction with filename
    with open(file_path, "w") as json_file:
        json.dump(data, json_file)
    if output_bool:    
        print("-> " + file_name + ".json saved")  
    
folder_path = os.path.join(directory, yesterday)
size = get_folder_size(folder_path)/1000000
# Get the current date and time
current_datetime = datetime.now()
# Format as a string
formatted_datetime = current_datetime.strftime("Date: %Y-%m-%d Time: %H:%M:%S")

body = f"""
Hello Luca,
from your Pi ;-);-)
"""

if output_bool:
    print("\nMail Content:")
    print("________________________________________")
    print(body)
    print("________________________________________")

directory_mail = os.path.join(cwd, "5.1_mail_body.txt")
with open(directory_mail, "w") as file:
    file.write(body)


