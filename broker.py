import pandas as pd

df_stocks = pd.read_csv('tracked_stocks.csv')

def datapreprocessing(data):
    data["date"] = pd.to_datetime(data["date_collection"], format="%Y-%m-%d")
    data.sort_values(by='date', inplace=True)
    data.reset_index(drop=True, inplace=True)

    data['mean_price'] = data[['open', 'low', 'high', 'close']].mean(axis=1)
    data['weekday'] = data['date'].dt.dayofweek
    data["price_change_1"] = data["mean_price"] / data["mean_price"].shift(1)
    data.fillna({'price_change_1': 1}, inplace=True)
    data["price_change_3"] = data["mean_price"] / data["mean_price"].shift(3)
    data.fillna({'price_change_1': 1}, inplace=True)
    data.fillna(0.0, inplace=True)

    preprocessing_information = pd.read_csv('normalizaton_stats.csv')
    features_list = preprocessing_information['Column Name'].tolist()
    data_features = data[features_list]
    
    data_features = data_features.reindex(sorted(data_features.columns), axis=1)
    #data_features.to_csv('data_features_from_model_broker.csv', index=False)
    return data_features
    
for index, row in df_stocks.iterrows():
    name = row['name']
    print(f'Running Simulation for {name}')
    path = 'Stocks/' + name + '/'

    #load model
    import joblib
    model = joblib.load('model_20240702_LR.pkl')
    #load new data
    data = pd.read_csv(path + 'data.csv')
    data = datapreprocessing(data)
    #predict
    prediction = model.predict(data)
    #save prediction
    data['prediction'] = prediction
    data.to_csv(path + 'prediction.csv', index=False)
