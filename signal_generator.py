import pandas as pd
import joblib
from my_lib import *

# Load preprocessing information
preprocessing_information = pd.read_csv('normalizaton_stats.csv')
features_list = preprocessing_information['Column Name'].tolist()
model = joblib.load('model_20240703_LR.pkl')

# Load tracked stocks information
df_stocks = pd.read_csv('tracked_stocks.csv')

buy_threshold = 0.5
sell_threshold = -0.5

for index, row in df_stocks.iterrows():
    name = row['name']
    path = 'Stocks/' + name + '/'
    data = pd.read_csv(path + 'data.csv')
    #only need last 3 days
    data = data.iloc[-3:]

    # Preprocess the data
    data_preprocessed = preprocess_data(data)
    data_selected = data_preprocessed[features_list] 
    data_normalized = normalize_with_stats(data_selected, preprocessing_information)

    # Predict using the last preprocessed row
    current_day = data_normalized.iloc[-1:]
    prediction = model.predict(current_day)
    print(f"Prediction for {name}: {prediction[0]}")

    