import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from xgboost import XGBRegressor
from sklearn.preprocessing import LabelEncoder

# Load dataset
df = pd.read_csv("CAR DETAILS FROM CAR DEKHO.csv")

# Create car age
current_year = 2025
df["car_age"] = current_year - df["year"]

# Extract brand
df["brand"] = df["name"].apply(lambda x: x.split()[0])

# Remove outliers
df = df[
    (df["selling_price"] > 50000) &
    (df["selling_price"] < 3000000)
]

# Drop unnecessary columns
df.drop(["name", "year"], axis=1, inplace=True)

# Encode categorical columns
label_encoders = {}

categorical_cols = [
    "brand",
    "fuel",
    "seller_type",
    "transmission",
    "owner"
]

for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Features and target
X = df.drop("selling_price", axis=1)
y = df["selling_price"]

# Train test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# XGBoost Model
model = XGBRegressor(
    n_estimators=500,
    learning_rate=0.05,
    max_depth=8,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

# Train model
model.fit(X_train, y_train)

# Prediction
pred = model.predict(X_test)

# Accuracy
score = r2_score(y_test, pred)

print(f"Accuracy Score: {score}")

# Save model
pickle.dump(model, open("model.pkl", "wb"))

# Save encoders
pickle.dump(label_encoders, open("encoders.pkl", "wb"))

print("Model trained successfully!")