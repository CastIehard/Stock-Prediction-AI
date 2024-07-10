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

    trade_cost = 1
    #reload data because we removed the last day
    data = pd.read_csv(path + 'data.csv')

    price_change = data["close"].iloc[-1] / data["close"].iloc[-2]
    print(f"Price Change is: {price_change}")

    #create a file called depot.csv if it does not exist
    try:
        depot = pd.read_csv(path + 'depot.csv')
        old_data = True
        cash = depot['cash'].iloc[-1]
        stock = depot['stock'].iloc[-1]*price_change
        holding = depot['holding'].iloc[-1]*price_change
    except:
        cash = 500
        stock = 500
        holding = 1000
        old_data = False

    date = data['date_collection'].iloc[-1]
    price = data['close'].iloc[-1]

    if action == 'Buy':
        cash, stock = my_lib.buy_stock(cash, stock,trade_cost)
    elif action == 'Sell':
        cash, stock = my_lib.sell_stock(cash, stock,trade_cost)

    depot_value = cash + stock
    #add variables to one df rntry at the last row
        # Create a new dataframe entry
    new_entry = pd.DataFrame({
        'date': [date],
        'cash': [cash],
        'stock': [stock],
        'depot_value': [depot_value],
        'holding' : [holding],
        'flag': [action]
    })

    if old_data:
        depot = pd.concat([depot, new_entry], ignore_index=True)
    else:
        depot = new_entry



    depot.to_csv(path + 'depot.csv', index=False)

    print(f"Updated depot for {name} on {date} with cash: {cash}, stock: {stock}, depot value: {depot_value}")

    #plot
    my_lib.plot_depot(depot, name, path)

print("Depot simulation completed.")


    



