import pandas as pd
import joblib
from preprocessing_utils import *

# Load preprocessing information
preprocessing_information = pd.read_csv('normalizaton_stats.csv')
features_list = preprocessing_information['Column Name'].tolist()

# Load tracked stocks information
df_stocks = pd.read_csv('tracked_stocks.csv')

buy_threshold = 0.5
sell_threshold = -0.5

for index, row in df_stocks.iterrows():
    name = row['name']
    print(f'Generating Signal using pretrained Model for {name}')
    path = 'Stocks/' + name + '/'

    # Load model
    try:
        model = joblib.load('model_20240703_LR.pkl')
    except AttributeError as e:
        print(f"Error loading model for {name}: {e}")
        continue

    # Load new data
    data = pd.read_csv(path + 'data.csv')

    # Use last 3 days
    data = data.iloc[-3:]

    # Preprocess the data
    data_preprocessed = preprocess_data(data)
    data_normalized = select_and_normalize_with_stats(data_preprocessed, features_list, preprocessing_information)

    # Predict using the last preprocessed row
    prediction = model.predict(data_preprocessed)

    # Assign predictions to the original data
    data['prediction'] = prediction

    # Generate buy/sell signals
    data['buy_or_sell'] = [1 if x >= buy_threshold else -1 if x <= sell_threshold else 0 for x in data['prediction']]

    print(f'Predictions and signals for {name}:')
    print(data[['date_collection', 'prediction', 'buy_or_sell']])
