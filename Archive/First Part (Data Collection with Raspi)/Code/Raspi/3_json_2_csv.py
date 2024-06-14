#make this true for cmd output
import os
import pandas as pd
import json
from my_config import output_bool

def get_need_to_do_list(already_done_list, directory):
    folder_list = [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))]
    # Convert all elements of both lists to strings
    folder_list = [str(name) for name in folder_list]
    already_done_list = [str(item) for item in already_done_list]

    # Convert both lists to sets
    set_folder_list = set(folder_list)
    set_already_done_list = set(already_done_list)

    # Subtract the sets
    need_to_do_list = list(set_folder_list - set_already_done_list)

    return need_to_do_list

# Get the current working directory
cwd = os.path.dirname(os.path.abspath(__file__))
# Set the 'directory' variable to the new path
directory = os.path.join(cwd, "Collected_Data")

data_path = os.path.join(cwd, "3.1_data_raw.csv")
#delete file because we cant fix bug and otherwise it wont work
if os.path.exists(data_path):
    os.remove(data_path)


try:
    
    old_data = pd.read_csv(data_path)
    already_done_list = old_data['folder'].tolist()
except:
    already_done_list = []

need_to_do_list = get_need_to_do_list(already_done_list, directory)

if output_bool:
    print("--> Need to do list: ", need_to_do_list)

# Initialize an empty list to store data
data_list = []

# Iterate through folders
for folder in need_to_do_list:
    folder_path = os.path.join(directory, folder)

########News_org News Sentiment Company#####################################################################################
    json_file_path = os.path.join(folder_path, 'adobe_inc.json')
    with open(json_file_path) as file:
        data = json.load(file)
    # Extract relevant data
    com_news_amount = data["totalResults"]
    if com_news_amount > 0:
        com_text_list = []
        for i in range(int(com_news_amount)):
            title = data["articles"][i]["title"]
            com_text_list.append(title)
            description = data["articles"][i]["description"]
            com_text_list.append(description)         
    else: com_text_list = 0

########News_org News Sentiment CEO#####################################################################################
    json_file_path = os.path.join(folder_path, 'shantanu_narayen.json')
    with open(json_file_path) as file:
        data = json.load(file)
    # Extract relevant data
    ceo_news_amount = data["totalResults"]
    if ceo_news_amount > 0:
        ceo_text_list = []
        for i in range(int(ceo_news_amount)):
            title = data["articles"][i]["title"]
            ceo_text_list.append(title)
            description = data["articles"][i]["description"]
            ceo_text_list.append(description)         
    else: ceo_text_list = 0

########Alpha News Sentiment#####################################################################################
    json_file_path = os.path.join(folder_path, 'news_sentiment.json')
    with open(json_file_path) as file:
        data = json.load(file)
    # Extract relevant data
    alpha_news_amount = int(data["items"])
    if alpha_news_amount > 0:
        news_score_list = []
        for i in range(int(alpha_news_amount)):
            score = data["feed"][i]["overall_sentiment_score"]
            news_score_list.append(score)
        alpha_news_sentiment_mean = sum(news_score_list)/len(news_score_list)
    else: alpha_news_sentiment_mean = 0
    
########GLOBAL QUOTE#####################################################################################
    json_file_path = os.path.join(folder_path, 'global_quote.json')
    with open(json_file_path) as file:
        data = json.load(file)
    # Extract relevant data
    date_global_quote           = data["Global Quote"]["07. latest trading day"]
    open_price                  = data["Global Quote"]["02. open"]
    high_price                  = data["Global Quote"]["03. high"]
    low_price                   = data["Global Quote"]["04. low"]
    closing_price               = data["Global Quote"]["05. price"]
    volume                      = data["Global Quote"]["06. volume"]
    
########Federal Fund Rate#################################################################################
    json_file_path = os.path.join(folder_path, 'federal_funds_rate.json')
    with open(json_file_path) as file:
        data = json.load(file)
    # Extract relevant data
    date_federal_funds_rate     = data["data"][0]["date"]
    federal_funds_rate          = data["data"][0]["value"]
    
########Exchange Rate#####################################################################################
    json_file_path = os.path.join(folder_path, 'currency_exchange_rate.json')
    with open(json_file_path) as file:
        data = json.load(file)
    # Extract relevant data
    date_currency_exchange_rate = data["Realtime Currency Exchange Rate"]["6. Last Refreshed"]
    currency_exchange_rate      = data["Realtime Currency Exchange Rate"]["5. Exchange Rate"]

########Consumer Price Index################################################################################
    json_file_path = os.path.join(folder_path, 'cpi.json')
    with open(json_file_path) as file:
        data = json.load(file)
    # Extract relevant data
    date_cpi                    = data["data"][0]["date"]
    cpi                         = data["data"][0]["value"]
    
########Inflation###########################################################################################
    json_file_path = os.path.join(folder_path, 'inflation.json')
    with open(json_file_path) as file:
        data = json.load(file)
    # Extract relevant data
    date_inflation                = data["data"][0]["date"]
    inflation                     = data["data"][0]["value"]

########Unemployment Rate####################################################################################
    json_file_path = os.path.join(folder_path, 'unemployment.json')
    with open(json_file_path) as file:
        data = json.load(file)
    # Extract relevant data
    date_unenployment            = data["data"][0]["date"]
    unemployment                 = data["data"][0]["value"]

########Earnings per Share#####################################################################################
    json_file_path = os.path.join(folder_path, 'earnings.json')
    with open(json_file_path) as file:
        data = json.load(file)
    # Extract relevant data
    date_eps                      = data["annualEarnings"][0]["fiscalDateEnding"]
    eps                           = data["annualEarnings"][0]["reportedEPS"]

########Real Gross Domestic Product############################################################################
    json_file_path = os.path.join(folder_path, 'real_gdp.json')
    with open(json_file_path) as file:
        data = json.load(file)
    # Extract relevant data
    date_gdp            = data["data"][0]["date"]
    gdp                 = data["data"][0]["value"]

########Advance Retail Sales####################################################################################
    json_file_path = os.path.join(folder_path, 'retail_sales.json')
    with open(json_file_path) as file:
        data = json.load(file)
    # Extract relevant data
    date_retail_sales            = data["data"][0]["date"]
    retail_sales                 = data["data"][0]["value"]

########Overview################################################################################################
    json_file_path = os.path.join(folder_path, 'overview.json')
    with open(json_file_path) as file:
        data = json.load(file)
    # Extract relevant data
    date_overview = folder #no date give so assumed that its current
    market_capitalization = data["MarketCapitalization"]
    ebitda = data["EBITDA"]
    pe_ratio = data["PERatio"]
    peg_ratio = data["PEGRatio"]
    book_value = data["BookValue"]
    dividend_per_share = data["DividendPerShare"]
    dividend_yield = data["DividendYield"]
    eps_2 = data["EPS"]
    revenue_per_share_ttm = data["RevenuePerShareTTM"]
    profit_margin = data["ProfitMargin"]
    operating_margin_ttm = data["OperatingMarginTTM"]
    return_on_assets_ttm = data["ReturnOnAssetsTTM"]
    return_on_equity_ttm = data["ReturnOnEquityTTM"]
    revenue_ttm = data["RevenueTTM"]
    gross_profit_ttm = data["GrossProfitTTM"]
    diluted_eps_ttm = data["DilutedEPSTTM"]
    quarterly_earnings_growth_yoy = data["QuarterlyEarningsGrowthYOY"]
    quarterly_revenue_growth_yoy = data["QuarterlyRevenueGrowthYOY"]
    analyst_target_price = data["AnalystTargetPrice"]
    trailing_pe = data["TrailingPE"]
    forward_pe = data["ForwardPE"]
    price_to_sales_ratio_ttm = data["PriceToSalesRatioTTM"]
    price_to_book_ratio = data["PriceToBookRatio"]
    ev_to_revenue = data["EVToRevenue"]
    ev_to_ebitda = data["EVToEBITDA"]
    beta = data["Beta"]
    week_high_52 = data["52WeekHigh"]
    week_low_52 = data["52WeekLow"]
    day_moving_average_50 = data["50DayMovingAverage"]
    day_moving_average_200 = data["200DayMovingAverage"]
    shares_outstanding = data["SharesOutstanding"]

########Balance Sheet####################################################################################
    json_file_path = os.path.join(folder_path, 'balance_sheet.json')
    with open(json_file_path) as file:
        data = json.load(file)
    # Extract relevant data
    fiscalDateEnding = data["quarterlyReports"][0]["fiscalDateEnding"]
    reportedCurrency = data["quarterlyReports"][0]["reportedCurrency"]
    totalAssets = data["quarterlyReports"][0]["totalAssets"]
    totalCurrentAssets = data["quarterlyReports"][0]["totalCurrentAssets"]
    cashAndCashEquivalentsAtCarryingValue = data["quarterlyReports"][0]["cashAndCashEquivalentsAtCarryingValue"]
    cashAndShortTermInvestments = data["quarterlyReports"][0]["cashAndShortTermInvestments"]
    inventory = data["quarterlyReports"][0]["inventory"]
    currentNetReceivables = data["quarterlyReports"][0]["currentNetReceivables"]
    totalNonCurrentAssets = data["quarterlyReports"][0]["totalNonCurrentAssets"]
    propertyPlantEquipment = data["quarterlyReports"][0]["propertyPlantEquipment"]
    accumulatedDepreciationAmortizationPPE = data["quarterlyReports"][0]["accumulatedDepreciationAmortizationPPE"]
    intangibleAssets = data["quarterlyReports"][0]["intangibleAssets"]
    intangibleAssetsExcludingGoodwill = data["quarterlyReports"][0]["intangibleAssetsExcludingGoodwill"]
    goodwill = data["quarterlyReports"][0]["goodwill"]
    investments = data["quarterlyReports"][0]["investments"]
    longTermInvestments = data["quarterlyReports"][0]["longTermInvestments"]
    shortTermInvestments = data["quarterlyReports"][0]["shortTermInvestments"]
    otherCurrentAssets = data["quarterlyReports"][0]["otherCurrentAssets"]
    otherNonCurrentAssets = data["quarterlyReports"][0]["otherNonCurrentAssets"]
    totalLiabilities = data["quarterlyReports"][0]["totalLiabilities"]
    totalCurrentLiabilities = data["quarterlyReports"][0]["totalCurrentLiabilities"]
    currentAccountsPayable = data["quarterlyReports"][0]["currentAccountsPayable"]
    deferredRevenue = data["quarterlyReports"][0]["deferredRevenue"]
    currentDebt = data["quarterlyReports"][0]["currentDebt"]
    shortTermDebt = data["quarterlyReports"][0]["shortTermDebt"]
    totalNonCurrentLiabilities = data["quarterlyReports"][0]["totalNonCurrentLiabilities"]
    capitalLeaseObligations = data["quarterlyReports"][0]["capitalLeaseObligations"]
    longTermDebt = data["quarterlyReports"][0]["longTermDebt"]
    currentLongTermDebt = data["quarterlyReports"][0]["currentLongTermDebt"]
    longTermDebtNoncurrent = data["quarterlyReports"][0]["longTermDebtNoncurrent"]
    shortLongTermDebtTotal = data["quarterlyReports"][0]["shortLongTermDebtTotal"]
    otherCurrentLiabilities = data["quarterlyReports"][0]["otherCurrentLiabilities"]
    otherNonCurrentLiabilities = data["quarterlyReports"][0]["otherNonCurrentLiabilities"]
    totalShareholderEquity = data["quarterlyReports"][0]["totalShareholderEquity"]
    treasuryStock = data["quarterlyReports"][0]["treasuryStock"]
    retainedEarnings = data["quarterlyReports"][0]["retainedEarnings"]
    commonStock = data["quarterlyReports"][0]["commonStock"]
    commonStockSharesOutstanding = data["quarterlyReports"][0]["commonStockSharesOutstanding"]

########Income Statement####################################################################################
    json_file_path = os.path.join(folder_path, 'income_statement.json')
    with open(json_file_path) as file:
        data = json.load(file)
    # Extract relevant data
    fiscalDateEnding = data["quarterlyReports"][0]["fiscalDateEnding"]
    reportedCurrency = data["quarterlyReports"][0]["reportedCurrency"]
    grossProfit = data["quarterlyReports"][0]["grossProfit"]
    totalRevenue = data["quarterlyReports"][0]["totalRevenue"]
    costOfRevenue = data["quarterlyReports"][0]["costOfRevenue"]
    costofGoodsAndServicesSold = data["quarterlyReports"][0]["costofGoodsAndServicesSold"]
    operatingIncome = data["quarterlyReports"][0]["operatingIncome"]
    sellingGeneralAndAdministrative = data["quarterlyReports"][0]["sellingGeneralAndAdministrative"]
    researchAndDevelopment = data["quarterlyReports"][0]["researchAndDevelopment"]
    operatingExpenses = data["quarterlyReports"][0]["operatingExpenses"]
    investmentIncomeNet = data["quarterlyReports"][0]["investmentIncomeNet"]
    netInterestIncome = data["quarterlyReports"][0]["netInterestIncome"]
    interestIncome = data["quarterlyReports"][0]["interestIncome"]
    interestExpense = data["quarterlyReports"][0]["interestExpense"]
    nonInterestIncome = data["quarterlyReports"][0]["nonInterestIncome"]
    otherNonOperatingIncome = data["quarterlyReports"][0]["otherNonOperatingIncome"]
    depreciation = data["quarterlyReports"][0]["depreciation"]
    depreciationAndAmortization = data["quarterlyReports"][0]["depreciationAndAmortization"]
    incomeBeforeTax = data["quarterlyReports"][0]["incomeBeforeTax"]
    incomeTaxExpense = data["quarterlyReports"][0]["incomeTaxExpense"]
    interestAndDebtExpense = data["quarterlyReports"][0]["interestAndDebtExpense"]
    netIncomeFromContinuingOperations = data["quarterlyReports"][0]["netIncomeFromContinuingOperations"]
    comprehensiveIncomeNetOfTax = data["quarterlyReports"][0]["comprehensiveIncomeNetOfTax"]
    ebit = data["quarterlyReports"][0]["ebit"]
    ebitda = data["quarterlyReports"][0]["ebitda"]
    netIncome = data["quarterlyReports"][0]["netIncome"]


#######put all the data from one folder to datalist##########################################################       
    data_list.append([
                folder,
                com_news_amount,
                com_text_list,
                ceo_news_amount,
                ceo_text_list,
                alpha_news_amount,
                alpha_news_sentiment_mean,
                date_global_quote,
                open_price,
                high_price,
                low_price,
                closing_price,
                volume,
                date_federal_funds_rate,
                federal_funds_rate,
                date_currency_exchange_rate,
                currency_exchange_rate,
                date_cpi,
                cpi,
                date_inflation,
                inflation,
                date_unenployment,
                unemployment,
                date_eps,
                eps,
                date_gdp,
                gdp,
                date_retail_sales,
                retail_sales,
                market_capitalization,
                ebitda,
                pe_ratio,
                peg_ratio,
                book_value,
                dividend_per_share,
                dividend_yield,
                eps,
                revenue_per_share_ttm,
                profit_margin,
                operating_margin_ttm,
                return_on_assets_ttm,
                return_on_equity_ttm,
                revenue_ttm,
                gross_profit_ttm,
                diluted_eps_ttm,
                quarterly_earnings_growth_yoy,
                quarterly_revenue_growth_yoy,
                analyst_target_price,
                trailing_pe,
                forward_pe,
                price_to_sales_ratio_ttm,
                price_to_book_ratio,
                ev_to_revenue,
                ev_to_ebitda,
                beta,
                week_high_52,
                week_low_52,
                day_moving_average_50,
                day_moving_average_200,
                shares_outstanding,
                fiscalDateEnding,
                reportedCurrency,
                totalAssets,
                totalCurrentAssets,
                cashAndCashEquivalentsAtCarryingValue,
                cashAndShortTermInvestments,
                inventory,
                currentNetReceivables,
                totalNonCurrentAssets,
                propertyPlantEquipment,
                accumulatedDepreciationAmortizationPPE,
                intangibleAssets,
                intangibleAssetsExcludingGoodwill,
                goodwill,
                investments,
                longTermInvestments,
                shortTermInvestments,
                otherCurrentAssets,
                otherNonCurrentAssets,
                totalLiabilities,
                totalCurrentLiabilities,
                currentAccountsPayable,
                deferredRevenue,
                currentDebt,
                shortTermDebt,
                totalNonCurrentLiabilities,
                capitalLeaseObligations,
                longTermDebt,
                currentLongTermDebt,
                longTermDebtNoncurrent,
                shortLongTermDebtTotal,
                otherCurrentLiabilities,
                otherNonCurrentLiabilities,
                totalShareholderEquity,
                treasuryStock,
                retainedEarnings,
                commonStock,
                commonStockSharesOutstanding,
                fiscalDateEnding,
                reportedCurrency,
                grossProfit,
                totalRevenue,
                costOfRevenue,
                costofGoodsAndServicesSold,
                operatingIncome,
                sellingGeneralAndAdministrative,
                researchAndDevelopment,
                operatingExpenses,
                investmentIncomeNet,
                netInterestIncome,
                interestIncome,
                interestExpense,
                nonInterestIncome,
                otherNonOperatingIncome,
                depreciation,
                depreciationAndAmortization,
                incomeBeforeTax,
                incomeTaxExpense,
                interestAndDebtExpense,
                netIncomeFromContinuingOperations,
                comprehensiveIncomeNetOfTax,
                ebit,
                ebitda,
                netIncome
            ])
    if output_bool:
        print("--> " + folder + " was added to data_list")

column_names = [
            'folder',
            'com_news_amount',
            'com_title_list',
            'ceo_news_amount',
            'ceo_title_list',
            'alpha_news_amount',
            'alpha_news_sentiment_mean',
            'date_global_quote',
            'open_price',
            'high_price',
            'low_price',
            'closing_price',
            'volume',
            'date_federal_funds_rate',
            'federal_funds_rate',
            'date_currency_exchange_rate',
            'currency_exchange_rate',
            'date_cpi',
            'cpi',
            'date_inflation',
            'inflation',
            'date_unenployment',
            'unemployment',
            'date_eps',
            'eps',
            'date_gdp',
            'gdp',
            'date_retail_sales',
            'retail_sales',
            'market_capitalization',
            'ebitda',
            'pe_ratio',
            'peg_ratio',
            'book_value',
            'dividend_per_share',
            'dividend_yield',
            'eps',
            'revenue_per_share_ttm',
            'profit_margin',
            'operating_margin_ttm',
            'return_on_assets_ttm',
            'return_on_equity_ttm',
            'revenue_ttm',
            'gross_profit_ttm',
            'diluted_eps_ttm',
            'quarterly_earnings_growth_yoy',
            'quarterly_revenue_growth_yoy',
            'analyst_target_price',
            'trailing_pe',
            'forward_pe',
            'price_to_sales_ratio_ttm',
            'price_to_book_ratio',
            'ev_to_revenue',
            'ev_to_ebitda',
            'beta',
            'week_high_52',
            'week_low_52',
            'day_moving_average_50',
            'day_moving_average_200',
            'shares_outstanding',
            'fiscalDateEnding',
            'reportedCurrency',
            'totalAssets',
            'totalCurrentAssets',
            'cashAndCashEquivalentsAtCarryingValue',
            'cashAndShortTermInvestments',
            'inventory',
            'currentNetReceivables',
            'totalNonCurrentAssets',
            'propertyPlantEquipment',
            'accumulatedDepreciationAmortizationPPE',
            'intangibleAssets',
            'intangibleAssetsExcludingGoodwill',
            'goodwill',
            'investments',
            'longTermInvestments',
            'shortTermInvestments',
            'otherCurrentAssets',
            'otherNonCurrentAssets',
            'totalLiabilities',
            'totalCurrentLiabilities',
            'currentAccountsPayable',
            'deferredRevenue',
            'currentDebt',
            'shortTermDebt',
            'totalNonCurrentLiabilities',
            'capitalLeaseObligations',
            'longTermDebt',
            'currentLongTermDebt',
            'longTermDebtNoncurrent',
            'shortLongTermDebtTotal',
            'otherCurrentLiabilities',
            'otherNonCurrentLiabilities',
            'totalShareholderEquity',
            'treasuryStock',
            'retainedEarnings',
            'commonStock',
            'commonStockSharesOutstanding',
            'fiscalDateEnding',
            'reportedCurrency',
            'grossProfit',
            'totalRevenue',
            'costOfRevenue',
            'costofGoodsAndServicesSold',
            'operatingIncome',
            'sellingGeneralAndAdministrative',
            'researchAndDevelopment',
            'operatingExpenses',
            'investmentIncomeNet',
            'netInterestIncome',
            'interestIncome',
            'interestExpense',
            'nonInterestIncome',
            'otherNonOperatingIncome',
            'depreciation',
            'depreciationAndAmortization',
            'incomeBeforeTax',
            'incomeTaxExpense',
            'interestAndDebtExpense',
            'netIncomeFromContinuingOperations',
            'comprehensiveIncomeNetOfTax',
            'ebit',
            'ebitda',
            'netIncome'
        ]


new_data = pd.DataFrame(data_list, columns=column_names)            

try:
    combined_data = pd.concat([old_data, new_data], ignore_index=True)
except Exception as e:
    combined_data = new_data
    if output_bool:
        print("--> No old data found. New data was created.")
        print("--> Exception from combining the data: ", e)

combined_data.sort_values(by=['folder'], inplace=False)        

# Write the combined data to a new CSV file
combined_data.to_csv(data_path, index=False)

if output_bool:
    print("--> All json data was put to -3.1_data_raw.csv-")
