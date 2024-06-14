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
        return {
            'alpha_news_amount': len(news_scores),
            'news_sentiment_mean': sum(news_scores) / len(news_scores)
        }
    return {'alpha_news_amount': 0, 'news_sentiment_mean': 0}

def extract_currency_exchange_rate(data):
    return {
        'date_currency_exchange_rate': data["Realtime Currency Exchange Rate"]["6. Last Refreshed"],
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