import pandas as pd

df_stocks = pd.read_csv('tracked_stocks.csv')

for index, row in df_stocks.iterrows():
    name = row['name']
    print(f'Running Depot Simulation for {name}')
    path = 'Stocks/' + name + '/'

    #get todays data
    data = pd.read_csv(path + 'prediction.csv')
    #get current day
    current_day = data['buy_or_sell'].tail(1).values[0]
    #print that stock needs to be bought or sold
    if current_day == 1:
        info = (f'{name} needs to be bought')
    elif current_day == -1:
        info = (f'{name} needs to be sold')
    else:
        info = (f'{name} is on hold')

    #save infomation to textfile
    today = pd.to_datetime('today').strftime('%Y-%m-%d')
    with open('buy_or_sell_info.txt', 'a') as f:
        f.write(today + ' : ' +info + '\n')
