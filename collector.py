import pandas as pd
import my_lib
from datetime import datetime,timedelta
import os

NEWS_API_KEY = os.environ.get('NEWS_API_KEY')
ALPHA_API_KEY = os.environ.get('ALPHA_API_KEY')

df_stocks = pd.read_csv('tracked_stocks.csv')

finbert_path  = '.venv/Transformer/'
my_lib.download_finbert(finbert_path)

for index, row in df_stocks.iterrows():
    name = row['name']
    ticker = row['ticker']
    ceo = row['ceo']
    print(f'Collecting data for {name} and {ceo} with ticker {ticker}')

    path = 'Stocks/' + name + '/'

    my_lib.makefolder(path)

    df_collected = pd.DataFrame()

    #get the news from yesterday 
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    df_collected['date_collection'] = [yesterday]

    news_list, amount = my_lib.get_news(name, yesterday, NEWS_API_KEY)
    df_collected['amount_news_name'] = [amount]
    
    #convert the list to one single number that represents the the sentiment
    sentiment = my_lib.list_finbert(news_list, finbert_path)
    df_collected['sentiment_name'] = [sentiment]
    
    news_list, amount = my_lib.get_news(ceo, yesterday, NEWS_API_KEY)
    df_collected['amount_news_ceo'] = [amount]
    sentiment = my_lib.list_finbert(news_list, finbert_path)
    df_collected['sentiment_ceo'] = [sentiment]

    #get the stock data
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
    df_stock_data = my_lib.get_stock_info(ticker, ALPHA_API_KEY, yesterday)
    
    df = pd.concat([df_collected, df_stock_data], axis=1)
    print("Data collected and news and stock data combined.")
    if os.path.isfile(path + 'data.csv'):
        try:
            df_old = pd.read_csv(path + 'data.csv')
            df = pd.concat([df_old, df], axis=0)
            print('Old data read and new data combined.')
        except:
            print('Error reading old data')
        
    df.to_csv(path + 'data.csv',index=False)
    print(f'Data about {name} and {ceo} with ticker {ticker} saved.')
