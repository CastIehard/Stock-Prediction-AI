import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import joblib
from preprocessing_utils import *
# Load and preprocess the data
print("Loading data...")
data = pd.read_csv("training_dataset_adobe_191_days.csv")


data = preprocess_data(data)

target = (data["mean_price"].shift(-1) / data["mean_price"] - 1) * 100
target.fillna(0, inplace=True)

# Select features
print("Selecting features...")
data_selected = select_features(data)
print(f"Selected features:\n{data_selected.head()}")

# Save normalization statistics
print("Saving normalization statistics...")
save_statistics(data_selected)

# Normalize the data
print("Normalizing data...")
data_normalized = normalize(data_selected)
print(f"Normalized data sample:\n{data_normalized.head()}")

# Sort columns alphabetically
print("Sorting columns alphabetically...")
data_normalized = data_normalized.reindex(sorted(data_normalized.columns), axis=1)
print(f"Sorted normalized data sample:\n{data_normalized.head()}")

# Split the data
print("Splitting data into train and test sets...")
X_train, X_test, y_train, y_test = train_test_split(data_normalized, target, test_size=0.1, random_state=42)
print(f"Training data sample:\n{X_train.head()}")
print(f"Training target sample:\n{y_train.head()}")
print(f"Test data sample:\n{X_test.head()}")
print(f"Test target sample:\n{y_test.head()}")

# Define the model pipeline
print("Defining the model pipeline...")
model_pipeline = Pipeline(steps=[
    ('normalize', FunctionTransformer(normalize, validate=False)),
    ('regressor', LinearRegression())
])

# Fit the model pipeline
print("Fitting the model pipeline...")
model_pipeline.fit(X_train, y_train)
print("Model training completed.")

# Save the model
today = pd.Timestamp.now().strftime("%Y%m%d")
model_name = f"model_{today}_LR.pkl"
joblib.dump(model_pipeline, model_name)
print(f"Model saved as {model_name}")
