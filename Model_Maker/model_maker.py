import pandas as pd

data = pd.read_csv("Model_Maker/data_raw.csv")
data["date"] = pd.to_datetime(data[data.columns[0]], format="%Y%m%d")
data.drop(data.columns[0], axis=1, inplace=True)
data.sort_values(by='date', inplace=True)
data.reset_index(drop=True, inplace=True)

data['mean_price'] = data[['open_price', 'low_price', 'high_price', 'closing_price']].mean(axis=1)

target = (data["mean_price"].shift(-1) / data["mean_price"] - 1)*100
target.fillna(0, inplace=True)

data['weekday'] = data['date'].dt.dayofweek

data["price_change_1"] = data["mean_price"] / data["mean_price"].shift(1)
data.fillna({'price_change_1': 1}, inplace=True)

data["price_change_3"] = data["mean_price"] / data["mean_price"].shift(3)
data.fillna({'price_change_1': 1}, inplace=True)

data.fillna(0.0, inplace=True)
data.drop(columns=data.filter(like='date').columns)
features = []
needed_unique = 5


for column in data.columns[1:]:
    if pd.to_numeric(data[column], errors='coerce').notnull().all():
        data[column] = pd.to_numeric(data[column])
        if data[column].nunique() >= needed_unique:  
            features.append(column)

data_features = data[features]

data_normalized = data_features.sub(data_features.mean(axis=0), axis=1).div((data_features.max(axis=0)-data_features.min(axis=0)), axis=1)

def create_statistics_csv(original_df, output_csv_path):
    statistics = {
        'Column Name': [],
        'Mean': [],
        'Max': [],
        'Min': []
    }

    for column in original_df.columns:
        statistics['Column Name'].append(column)
        statistics['Mean'].append(original_df[column].mean())
        statistics['Max'].append(original_df[column].max())
        statistics['Min'].append(original_df[column].min())

    statistics_df = pd.DataFrame(statistics)
    statistics_df.to_csv(output_csv_path, index=False)
create_statistics_csv(data_features, 'Model_Maker/normalizaton_stats.csv')

from sklearn.model_selection import train_test_split
features = data_features
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.1, random_state=42)

from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X_train, y_train)

import joblib
today = pd.Timestamp.now().strftime("%Y%m%d")
model_name = f"model_{today}_LR.pkl"
joblib.dump(model, f'Model_Maker/{model_name}')

