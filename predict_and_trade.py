import pandas as pd
import my_lib
from datetime import datetime, timedelta
import os
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

training_amount = 50
buy_threshold = 0.5
sell_threshold = -0.5

df_stocks = pd.read_csv('tracked_stocks.csv')

for index, row in df_stocks.iterrows():
    name = row['name']
    ticker = row['ticker']
    ceo = row['ceo']
    print(f'Predict and trade {name}')

    path = 'Stocks/' + name + '/'

    data = pd.read_csv(path + 'data.csv')
    #get the last 50 entries
    if len(data) > training_amount:
        data = data.iloc[-training_amount:]
        
    #do data preprocessing
    data = my_lib.preprocess_data(data)
    #add target column
    target = (data["mean_price"].shift(-1) / data["mean_price"] - 1) * 100
    #standardize the data
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data)

    #remove last day because we want to predict it later
    todays_data = data_scaled[-1].reshape(1, -1)
    data_scaled = data_scaled[:-1]
    target = target[:-1]

    X_train, X_test, y_train, y_test = train_test_split(data_scaled, target, test_size=0.2, random_state=42)
    #train the model
    model = LinearRegression()
    model.fit(X_train, y_train)

    #predict the next day
    prediction = model.predict(todays_data)
    print(f"Prediction for {name}: {prediction[0]}")

    if prediction[0] > buy_threshold:
        action = 'Buy'
    elif prediction[0] < sell_threshold:
        action = 'Sell'
    else:
        action = 'Hold'
    
    print(f"Action for {name}: {action}")

    #write the action to the txt file with 1 for buy -1 for sell and 0 for hold
    with open(path + 'flag.csv', 'w') as f:
        if action == 'Buy':
            f.write('1')
        elif action == 'Sell':
            f.write('-1')
        else:
            f.write('0')
