import pandas as pd
from utils import download_finbert, get_news, list_finbert, get_stock_info
from datetime import datetime,timedelta
import os

NEWS_API_KEY = os.environ.get('NEWS_API_KEY')
ALPHA_API_KEY = os.environ.get('ALPHA_API_KEY')

df_stocks = pd.read_csv('tracked_stocks.csv')

finbert_path  = '.venv/Transformer/'
download_finbert(finbert_path)

for index, row in df_stocks.iterrows():
    name = row['name']
    ticker = row['ticker']
    ceo = row['ceo']
    print(f'Collecting data for {name} and {ceo} with ticker {ticker}')

    path = 'Stocks/' + name + '/'

    os.makedirs(path, exist_ok=True)

    df_collected = pd.DataFrame()

    #get the news from yesterday 
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    df_collected['date_collection'] = [yesterday]

    #get News and sentiment about company
    news_list, amount = get_news(name, yesterday, NEWS_API_KEY)
    df_collected['amount_news_name'] = [amount]
    sentiment = list_finbert(news_list, finbert_path)
    df_collected['sentiment_name'] = [sentiment]
    
    #get News and sentiment about CEO
    news_list, amount = get_news(ceo, yesterday, NEWS_API_KEY)
    df_collected['amount_news_ceo'] = [amount]
    sentiment = list_finbert(news_list, finbert_path)
    df_collected['sentiment_ceo'] = [sentiment]

    #get the stock data
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
    df_stock_data = get_stock_info(ticker, ALPHA_API_KEY, yesterday)

    #check if api limit reached if df contains "API rate limit reached"
    if "API rate limit reached" in df_stock_data.columns:
        print("API rate limit reached no need to run the rest of the code.")
        exit()
    else:
        df_collected = pd.concat([df_collected, df_stock_data], axis=1)
        print("Data collected and news and stock data combined.")
    
        if os.path.isfile(path + 'data.csv'):
            try:
                df_old = pd.read_csv(path + 'data.csv')
                df_collected = pd.concat([df_old, df_collected], axis=0)
                print('Old data read and new data combined on bottom of it.')
            except:
                print('Error reading old data')
        
    df_collected.to_csv(path + 'data.csv',index=False)
    print(f'Data about {name} and {ceo} with ticker {ticker} saved.')
