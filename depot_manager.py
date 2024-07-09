import pandas as pd
from my_lib import *

trade_cost = 1
df_stocks = pd.read_csv('tracked_stocks.csv')

for index, row in df_stocks.iterrows():
    name = row['name']
    print(f'Running Depot Simulation for {name}')
    path = 'Stocks/' + name + '/'

    with open(path+'flag.txt', 'r') as file:
    # Read the content of the file
        flag = int(file.read())

    data = pd.read_csv(path + 'data.csv')

    price_change = data["close"].iloc[-1] / data["close"].iloc[-2]
    print(f"Price Change is: {price_change}")

    #create a file called depot.csv if it does not exist
    try:
        depot = pd.read_csv(path + 'depot.csv')
        old_data = True
        cash = depot['cash'].iloc[-1]
        stock = depot['stock'].iloc[-1]*price_change
    except:
        cash = 500
        stock = 500
        old_data = False

    date = data['date_collection'].iloc[-1]
    price = data['close'].iloc[-1]

    if flag == 1:
        cash, stock = buy_stock(cash, stock,trade_cost)
    elif flag == -1:
        cash, stock = sell_stock(cash, stock,trade_cost)

    depot_value = cash + stock
    #add variables to one df rntry at the last row
        # Create a new dataframe entry
    new_entry = pd.DataFrame({
        'date': [date],
        'cash': [cash],
        'stock': [stock],
        'depot_value': [depot_value],
        'flag': [flag]
    })

    if old_data:
        depot = pd.concat([depot, new_entry], ignore_index=True)
    else:
        depot = new_entry



    depot.to_csv(path + 'depot.csv', index=False)

    print(f"Updated depot for {name} on {date} with cash: {cash}, stock: {stock}, depot value: {depot_value}")

print("Depot simulation completed.")

    



