# preprocessing_utils.py
import pandas as pd

def normalize(df):
    mean = df.mean(axis=0)
    max_min_diff = df.max(axis=0) - df.min(axis=0)
    return (df - mean) / max_min_diff

def preprocess_data(data):
    for fmt in ('%Y-%m-%d', '%Y%m%d'):
        try:
            data["date"] = pd.to_datetime(data['date_collection'], format=fmt)
        except ValueError:
            continue
        
    data.sort_values(by='date', inplace=True)
    data.reset_index(drop=True, inplace=True)

    data['mean_price'] = data[['open', 'low', 'high', 'close']].mean(axis=1)

    target = (data["mean_price"].shift(-1) / data["mean_price"] - 1) * 100
    target.fillna(0, inplace=True)

    data['weekday'] = data['date'].dt.dayofweek

    data["price_change_1"] = data["mean_price"] / data["mean_price"].shift(1)
    data.fillna({'price_change_1': 1}, inplace=True)

    data["price_change_3"] = data["mean_price"] / data["mean_price"].shift(3)
    data.fillna({'price_change_3': 1}, inplace=True)

    data.fillna(0.0, inplace=True)
        
    # Sort columns alphabetically
    data = data.reindex(sorted(data.columns), axis=1)
    data.fillna(0.0, inplace=True)
    # Drop any date-related columns explicitly
    data.drop(columns=data.filter(like='date').columns, inplace=True)
    return data

def normalize_with_stats(data_features,preprocessing_information):
    data_features = data_features.sub(preprocessing_information.set_index('Column Name')['Mean'], axis=1)
    data_features = data_features.div(preprocessing_information.set_index('Column Name')['Max'] - preprocessing_information.set_index('Column Name')['Min'], axis=1)
    return data_features

def select_features(df):
    features = []
    needed_unique = 5
    for column in df.columns[1:]:
        if pd.to_numeric(df[column], errors='coerce').notnull().all():
            df[column] = pd.to_numeric(df[column])
            if df[column].nunique() >= needed_unique:
                features.append(column)
    return df[features]

def save_statistics(df, output_csv_path='normalizaton_stats.csv'):
    statistics = {
        'Column Name': df.columns,
        'Mean': df.mean(),
        'Max': df.max(),
        'Min': df.min()
    }

    statistics_df = pd.DataFrame(statistics)
    statistics_df.to_csv(output_csv_path, index=False)
    print(f"Normalization statistics saved to {output_csv_path}")
    print(statistics_df)
