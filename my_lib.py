import os
import requests
from transformers import BertTokenizer, BertForSequenceClassification, pipeline
from my_api_extractors import *
import pandas as pd

def get_news(topic: str, date: str,api_key:str):
    """
    Get news articles based on a given topic and date.

    Parameters:
    - topic (str): The topic of the news articles.
    - date (str): The date from which to retrieve the news articles. %Y-%m-%d format.
    - api_key (str): The API key for accessing the news API. Get it at https://newsapi.org/

    Returns:
    - news_list (list): A list of news article titles related to the given topic and date.
    - amount (int): The number of news articles found.
    """
    url = f'https://newsapi.org/v2/everything?q={topic}&from={date}&sortBy=publishedAt&apiKey={api_key}'  

    request = requests.get(url)
    data = request.json()
    if check_api_error(data):
        print("Something went wrong with the API request of Newsapi.org")
        return [], 0
    else:
        amount = int(data["totalResults"])

        if amount > 0:
            if amount > 99: amount = 99
            news_list = []
            for i in range(amount):
                title = data["articles"][i]["title"]
                news_list.append(title)
                description = data["articles"][i]["description"]
                news_list.append(description)         
        else:
            news_list = []
            amount = 0
        print(f'Found {amount} news articles for {topic} on {date}')
        return news_list, amount

def download_finbert(path:str):
    """
    If in the provided path folder the Finbert model and tokenizer are not available, download them from the Hugging Face model hub.
    """
    if not os.path.exists(path):
        finbert = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone',num_labels=3)
        finbert.save_pretrained(path + 'Finbert_Offline')

        tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')
        tokenizer.save_pretrained(path + 'Tokenizer_Offline')

        print("Transfomers successfully downloaded")
    else:
        print("Transfomers already downloaded")

def list_finbert(string_list: list, path: str):
    """
    Get the sentiment of a list of news articles using the Finbert model.

    Parameters:
    - news_list (list): A list of news article titles.
    - path (str): The path to the Finbert model and tokenizer.

    Returns:
    - sentiment (int): A number representing the sentiment of the news articles.
    """

    finbert = BertForSequenceClassification.from_pretrained(path + 'Finbert_Offline',num_labels=3)
    tokenizer = BertTokenizer.from_pretrained(path + 'Tokenizer_Offline')
    nlp = pipeline("sentiment-analysis", model=finbert, tokenizer=tokenizer)
    # Return 0 immediately if input is "0"
    if string_list == "0":
        print(f'Topic list: {string_list} -> Sentiment: 0')
        return 0
    else:
        scores = []
        for text in string_list:
            # Truncate text to fit tokenization limit
            if text is None:
                #skip to the next text
                continue
            while len(tokenizer.tokenize(text)) > 500:
                text = text[:-1]

            # Analyze text with finbert
            results = nlp(text)
            for item in results:
                score = item['score']
                label = item['label']
                # Convert label to numerical value and multiply by score
                if label == "Neutral":
                    scores.append(0)
                elif label == "Negative":
                    scores.append(-1 * score)
                elif label == "Positive":
                    scores.append(1 * score)
        try:
            score = sum(scores) / len(scores)
            print(f'Topic list: {string_list} -> Sentiment: {score}')
            return score
        except ZeroDivisionError:
            score = 0
            print(f'Topic list: {string_list} -> Sentiment: {score}')
            return score
        
def check_api_error(json_response):
    if "Information" in json_response and "rate limit" in json_response["Information"]:
        return True
    if json_response.get('status') == 'error':
        return True
    return False

def get_stock_info(ticker: str, api_key: str, date: str):
    """
    Get stock information from the Alpha Vantage API.
    Input:
    - ticker (str): The stock ticker symbol.
    - api_key (str): The API key for accessing the Alpha Vantage API.
    - date (str): The date for which to retrieve the stock information. %Y%m%d format.
    """
    url_list = [
        f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={api_key}',
        f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker}&limit=1000&time_from={date}T0001&time_to={date}T2359&apikey={api_key}',
        f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=USD&to_currency=JPY&apikey={api_key}',
        f'https://www.alphavantage.co/query?function=RETAIL_SALES&apikey={api_key}',
        f'https://www.alphavantage.co/query?function=CPI&interval=monthly&apikey={api_key}',
        f'https://www.alphavantage.co/query?function=UNEMPLOYMENT&apikey={api_key}',
        f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={api_key}',
        f'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={ticker}&apikey={api_key}',
        f'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={ticker}&apikey={api_key}',
        f'https://www.alphavantage.co/query?function=FEDERAL_FUNDS_RATE&interval=daily&apikey={api_key}',
        f'https://www.alphavantage.co/query?function=REAL_GDP&interval=quarterly&apikey={api_key}',
        f'https://www.alphavantage.co/query?function=INFLATION&apikey={api_key}'
    ]

    data_extractors = {
        'GLOBAL_QUOTE': extract_global_quote,
        'NEWS_SENTIMENT': extract_news_sentiment,
        'CURRENCY_EXCHANGE_RATE': extract_currency_exchange_rate,
        'RETAIL_SALES': extract_retail_sales,
        'CPI': extract_cpi,
        'UNEMPLOYMENT': extract_unemployment,
        'OVERVIEW': extract_overview,
        'INCOME_STATEMENT': extract_income_statement,
        'BALANCE_SHEET': extract_balance_sheet,
        'FEDERAL_FUNDS_RATE': extract_federal_funds_rate,
        'REAL_GDP': extract_real_gdp,
        'INFLATION': extract_inflation
    }

    combined_data = {}

    for url in url_list:
        r = requests.get(url)
        data = r.json()

        if check_api_error(data):
            print("API rate limit reached")
            return pd.DataFrame({'API rate limit reached': [99999]})
        else:
            for key, extractor in data_extractors.items():
                if key in url:
                    extracted_data = extractor(data)
                    combined_data.update(extracted_data)
                    print(f'{key} data extracted')

    df = pd.DataFrame([combined_data])
    return df