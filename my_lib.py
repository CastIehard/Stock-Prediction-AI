import os
import requests
from transformers import BertTokenizer, BertForSequenceClassification, pipeline
import pandas as pd
import matplotlib.pyplot as plt

def plot_depot(depot, name,path):
    plt.cla()
    plt.clf()
    plt.close()
    plt.figure(figsize=(10, 6))

    plt.plot(depot['date'], depot["holding"], label='Holding', marker='o', color='blue')
    plt.plot(depot['date'], depot["depot_value"], label='Using SPAI', marker='x', color='purple')

    buy_label_added = False
    sell_label_added = False

    for index, row in depot.iterrows():
        if row['flag'] == 'Buy':
            if not buy_label_added:
                plt.bar(row['date'], height=0.1, bottom=row["holding"] - 0.05, color='green', width=1, alpha=0.5, label ="buy")
                buy_label_added = True
            else:
                plt.bar(row['date'], height=0.1, bottom=row["holding"] - 0.05, color='green', width=1, alpha=0.5)
        elif row['flag'] == 'Sell':
            if not sell_label_added:
                plt.bar(row['date'], height=0.1, bottom=row["holding"] - 0.05, color='red', width=1, alpha=0.5, label = "sell")
                sell_label_added = True
            else:
                plt.bar(row['date'], height=0.1, bottom=row["holding"] - 0.05, color='red', width=1, alpha=0.5)
    plt.title(name)
    plt.xlabel('Datum')
    plt.ylabel('Depotwert nach Start bei 1000 €')
    plt.legend()
    plt.xticks(depot['date'][::10], rotation=45)
    plt.tight_layout()
    plt.savefig(path + 'depot.png')
    print(f"Depot plot saved to {path + 'depot.png'}")



def buy_stock(cash,stocks,trade_cost):
    if cash > 0:
        cash -= trade_cost
        stocks += cash
        cash = 0
    return cash, stocks

def sell_stock(cash,stocks,trade_cost):
    if stocks > 0:
        cash += stocks
        cash -= trade_cost
        stocks = 0
    return cash, stocks

    
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
                    try:
                        extracted_data = extractor(data)
                        combined_data.update(extracted_data)
                        print(f'{key} data extracted')
                    except:
                        print(f'Error extracting {key} data')
                        print(f'From url: {url}')
                        return pd.DataFrame({'API rate limit reached': [99999]})

    df = pd.DataFrame([combined_data])
    return df
# preprocessing_utils.py
import pandas as pd

def normalize(df):
    mean = df.mean(axis=0)
    max_min_diff = df.max(axis=0) - df.min(axis=0)
    return (df - mean) / max_min_diff

def preprocess_data(data):
    ###
    # Convert date to datetime format
    # Try different date formats
    # Sort data by date
    # Calculate mean price
    # Calculate target
    # Calculate weekday
    # Calculate price change 1
    # Calculate price change 3
    # Drop any date-related columns
    # Sort columns alphabetically
    # Drop any columns that are not numeric
    # Drop any columns with less than 2 unique values
    # Fill NaN values with 0
    ###

    for fmt in ('%Y-%m-%d', '%Y%m%d'):
        try:
            data["date"] = pd.to_datetime(data['date_collection'], format=fmt)
        except ValueError:
            continue
        
    data.sort_values(by='date', inplace=True)
    data.reset_index(drop=True, inplace=True)

    data['mean_price'] = data[['open', 'low', 'high', 'close']].mean(axis=1)

    target = (data["mean_price"].shift(-1) / data["mean_price"] - 1) * 100
    target.fillna(0, inplace=True)

    data['weekday'] = data['date'].dt.dayofweek

    data["price_change_1"] = data["mean_price"] / data["mean_price"].shift(1)
    data.fillna({'price_change_1': 1}, inplace=True)

    data["price_change_3"] = data["mean_price"] / data["mean_price"].shift(3)
    data.fillna({'price_change_3': 1}, inplace=True)

    data.fillna(0.0, inplace=True)
        
    # Sort columns alphabetically
    data = data.reindex(sorted(data.columns), axis=1)
    data.fillna(0.0, inplace=True)
    # Drop any date-related columns explicitly
    data.drop(columns=data.filter(like='date').columns, inplace=True)

    features = []
    needed_unique = 2
    for column in data.columns[1:]:
        if pd.to_numeric(data[column], errors='coerce').notnull().all():
            data[column] = pd.to_numeric(data[column])
            if data[column].nunique() >= needed_unique:
                features.append(column)
    return data[features]


def select_features(df):
    features = []
    needed_unique = 5
    for column in df.columns[1:]:
        if pd.to_numeric(df[column], errors='coerce').notnull().all():
            df[column] = pd.to_numeric(df[column])
            if df[column].nunique() >= needed_unique:
                features.append(column)
    return df[features]

def save_statistics(df, output_csv_path='normalizaton_stats.csv'):
    statistics = {
        'Column Name': df.columns,
        'Mean': df.mean(),
        'Max': df.max(),
        'Min': df.min()
    }

    statistics_df = pd.DataFrame(statistics)
    statistics_df.to_csv(output_csv_path, index=False)
    print(f"Normalization statistics saved to {output_csv_path}")
    print(statistics_df)
def extract_global_quote(data):
    return {
        'date_global_quote': data["Global Quote"]["07. latest trading day"],
        'open': data["Global Quote"]["02. open"],
        'high': data["Global Quote"]["03. high"],
        'low': data["Global Quote"]["04. low"],
        'close': data["Global Quote"]["05. price"],
        'volume': data["Global Quote"]["06. volume"]
    }

def extract_news_sentiment(data):
    if "feed" in data:
        news_scores = [item["overall_sentiment_score"] for item in data["feed"]]
        mean_score = sum(news_scores) / len(news_scores) if len(news_scores) > 0 else 0
        return {
            'alpha_news_amount': len(news_scores),
            'news_sentiment_mean': mean_score
        }
    return {'alpha_news_amount': 0, 'news_sentiment_mean': 0}

def extract_currency_exchange_rate(data):
    return {
        'currency_exchange_rate': data["Realtime Currency Exchange Rate"]["5. Exchange Rate"]
    }

def extract_retail_sales(data):
    return {
        'date_retail_sales': data["data"][0]["date"],
        'retail_sales': data["data"][0]["value"]
    }

def extract_cpi(data):
    return {
        'date_cpi': data["data"][0]["date"],
        'cpi': data["data"][0]["value"]
    }

def extract_unemployment(data):
    return {
        'date_unemployment': data["data"][0]["date"],
        'unemployment': data["data"][0]["value"]
    }

def extract_overview(data):
    return {
    'market_capitalization': data["MarketCapitalization"],
    'ebitda': data["EBITDA"],
    'pe_ratio': data["PERatio"],
    'peg_ratio': data["PEGRatio"],
    'book_value': data["BookValue"],
    'dividend_per_share': data["DividendPerShare"],
    'dividend_yield': data["DividendYield"],
    'eps': data["EPS"],
    'revenue_per_share_ttm': data["RevenuePerShareTTM"],
    'profit_margin': data["ProfitMargin"],
    'operating_margin_ttm': data["OperatingMarginTTM"],
    'return_on_assets_ttm': data["ReturnOnAssetsTTM"],
    'return_on_equity_ttm': data["ReturnOnEquityTTM"],
    'revenue_ttm': data["RevenueTTM"],
    'gross_profit_ttm': data["GrossProfitTTM"],
    'diluted_eps_ttm': data["DilutedEPSTTM"],
    'quarterly_earnings_growth_yoy': data["QuarterlyEarningsGrowthYOY"],
    'quarterly_revenue_growth_yoy': data["QuarterlyRevenueGrowthYOY"],
    'analyst_target_price': data["AnalystTargetPrice"],
    'trailing_pe': data["TrailingPE"],
    'forward_pe': data["ForwardPE"],
    'price_to_sales_ratio_ttm': data["PriceToSalesRatioTTM"],
    'price_to_book_ratio': data["PriceToBookRatio"],
    'ev_to_revenue': data["EVToRevenue"],
    'ev_to_ebitda': data["EVToEBITDA"],
    'beta': data["Beta"],
    'week_high_52': data["52WeekHigh"],
    'week_low_52': data["52WeekLow"],
    'day_moving_average_50': data["50DayMovingAverage"],
    'day_moving_average_200': data["200DayMovingAverage"],
    'shares_outstanding': data["SharesOutstanding"]
}

def extract_income_statement(data):
    return {
    'fiscal_date_ending': data["quarterlyReports"][0]["fiscalDateEnding"],
    'reported_currency': data["quarterlyReports"][0]["reportedCurrency"],
    'gross_profit': data["quarterlyReports"][0]["grossProfit"],
    'total_revenue': data["quarterlyReports"][0]["totalRevenue"],
    'cost_of_revenue': data["quarterlyReports"][0]["costOfRevenue"],
    'cost_of_goods_and_services_sold': data["quarterlyReports"][0]["costofGoodsAndServicesSold"],
    'operating_income': data["quarterlyReports"][0]["operatingIncome"],
    'selling_general_and_administrative': data["quarterlyReports"][0]["sellingGeneralAndAdministrative"],
    'research_and_development': data["quarterlyReports"][0]["researchAndDevelopment"],
    'operating_expenses': data["quarterlyReports"][0]["operatingExpenses"],
    'investment_income_net': data["quarterlyReports"][0]["investmentIncomeNet"],
    'net_interest_income': data["quarterlyReports"][0]["netInterestIncome"],
    'interest_income': data["quarterlyReports"][0]["interestIncome"],
    'interest_expense': data["quarterlyReports"][0]["interestExpense"],
    'non_interest_income': data["quarterlyReports"][0]["nonInterestIncome"],
    'other_non_operating_income': data["quarterlyReports"][0]["otherNonOperatingIncome"],
    'depreciation': data["quarterlyReports"][0]["depreciation"],
    'depreciation_and_amortization': data["quarterlyReports"][0]["depreciationAndAmortization"],
    'income_before_tax': data["quarterlyReports"][0]["incomeBeforeTax"],
    'income_tax_expense': data["quarterlyReports"][0]["incomeTaxExpense"],
    'interest_and_debt_expense': data["quarterlyReports"][0]["interestAndDebtExpense"],
    'net_income_from_continuing_operations': data["quarterlyReports"][0]["netIncomeFromContinuingOperations"],
    'comprehensive_income_net_of_tax': data["quarterlyReports"][0]["comprehensiveIncomeNetOfTax"],
    'ebit': data["quarterlyReports"][0]["ebit"],
    'ebitda': data["quarterlyReports"][0]["ebitda"],
    'net_income': data["quarterlyReports"][0]["netIncome"]
}


def extract_balance_sheet(data):
    return {
    'fiscal_date_ending': data["quarterlyReports"][0]["fiscalDateEnding"],
    'reported_currency': data["quarterlyReports"][0]["reportedCurrency"],
    'total_assets': data["quarterlyReports"][0]["totalAssets"],
    'total_current_assets': data["quarterlyReports"][0]["totalCurrentAssets"],
    'cash_and_cash_equivalents': data["quarterlyReports"][0]["cashAndCashEquivalentsAtCarryingValue"],
    'cash_and_short_term_investments': data["quarterlyReports"][0]["cashAndShortTermInvestments"],
    'inventory': data["quarterlyReports"][0]["inventory"],
    'current_net_receivables': data["quarterlyReports"][0]["currentNetReceivables"],
    'total_non_current_assets': data["quarterlyReports"][0]["totalNonCurrentAssets"],
    'property_plant_equipment': data["quarterlyReports"][0]["propertyPlantEquipment"],
    'accumulated_depreciation_amortization_ppe': data["quarterlyReports"][0]["accumulatedDepreciationAmortizationPPE"],
    'intangible_assets': data["quarterlyReports"][0]["intangibleAssets"],
    'intangible_assets_excluding_goodwill': data["quarterlyReports"][0]["intangibleAssetsExcludingGoodwill"],
    'goodwill': data["quarterlyReports"][0]["goodwill"],
    'investments': data["quarterlyReports"][0]["investments"],
    'long_term_investments': data["quarterlyReports"][0]["longTermInvestments"],
    'short_term_investments': data["quarterlyReports"][0]["shortTermInvestments"],
    'other_current_assets': data["quarterlyReports"][0]["otherCurrentAssets"],
    'other_non_current_assets': data["quarterlyReports"][0]["otherNonCurrentAssets"],
    'total_liabilities': data["quarterlyReports"][0]["totalLiabilities"],
    'total_current_liabilities': data["quarterlyReports"][0]["totalCurrentLiabilities"],
    'current_accounts_payable': data["quarterlyReports"][0]["currentAccountsPayable"],
    'deferred_revenue': data["quarterlyReports"][0]["deferredRevenue"],
    'current_debt': data["quarterlyReports"][0]["currentDebt"],
    'short_term_debt': data["quarterlyReports"][0]["shortTermDebt"],
    'total_non_current_liabilities': data["quarterlyReports"][0]["totalNonCurrentLiabilities"],
    'capital_lease_obligations': data["quarterlyReports"][0]["capitalLeaseObligations"],
    'long_term_debt': data["quarterlyReports"][0]["longTermDebt"],
    'current_long_term_debt': data["quarterlyReports"][0]["currentLongTermDebt"],
    'long_term_debt_noncurrent': data["quarterlyReports"][0]["longTermDebtNoncurrent"],
    'short_long_term_debt_total': data["quarterlyReports"][0]["shortLongTermDebtTotal"],
    'other_current_liabilities': data["quarterlyReports"][0]["otherCurrentLiabilities"],
    'other_non_current_liabilities': data["quarterlyReports"][0]["otherNonCurrentLiabilities"],
    'total_shareholder_equity': data["quarterlyReports"][0]["totalShareholderEquity"],
    'treasury_stock': data["quarterlyReports"][0]["treasuryStock"],
    'retained_earnings': data["quarterlyReports"][0]["retainedEarnings"],
    'common_stock': data["quarterlyReports"][0]["commonStock"],
    'common_stock_shares_outstanding': data["quarterlyReports"][0]["commonStockSharesOutstanding"]
}


def extract_federal_funds_rate(data):
    return {
        'date_federal_funds_rate': data["data"][0]["date"],
        'federal_funds_rate': data["data"][0]["value"]
    }

def extract_real_gdp(data):
    return {
        'date_gdp': data["data"][0]["date"],
        'real_gdp': data["data"][0]["value"]
    }

def extract_inflation(data):
    return {
        'date_inflation': data["data"][0]["date"],
        'inflation': data["data"][0]["value"]
    }