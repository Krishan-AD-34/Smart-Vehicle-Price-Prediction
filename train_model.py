import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBRegressor
import joblib

# Load dataset
df = pd.read_csv("CAR DETAILS FROM CAR DEKHO.csv")

# Remove missing values
df = df.dropna()

# Rename columns
df = df.rename(columns={
    "name": "brand",
    "year": "year",
    "selling_price": "price",
    "km_driven": "km_driven",
    "fuel": "fuel",
    "seller_type": "seller_type",
    "transmission": "transmission",
    "owner": "owner"
})

# Keep only first word of car name
df["brand"] = df["brand"].apply(lambda x: x.split()[0])

# Select useful columns
df = df[[
    "brand",
    "year",
    "fuel",
    "seller_type",
    "transmission",
    "owner",
    "km_driven",
    "price"
]]

# Extra features
df["mileage"] = 20
df["engine"] = 1200
df["car_age"] = 2026 - df["year"]

# Label encoders
le_brand = LabelEncoder()
le_fuel = LabelEncoder()
le_seller = LabelEncoder()
le_trans = LabelEncoder()
le_owner = LabelEncoder()

# Encode categorical data
df["brand"] = le_brand.fit_transform(df["brand"])
df["fuel"] = le_fuel.fit_transform(df["fuel"])
df["seller_type"] = le_seller.fit_transform(df["seller_type"])
df["transmission"] = le_trans.fit_transform(df["transmission"])
df["owner"] = le_owner.fit_transform(df["owner"])

# Features and target
X = df[[
    "brand",
    "year",
    "fuel",
    "seller_type",
    "transmission",
    "owner",
    "km_driven",
    "mileage",
    "engine",
    "car_age"
]]

y = df["price"]

# Train test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Model
model = XGBRegressor(
    n_estimators=300,
    max_depth=7,
    learning_rate=0.08
)

# Train model
model.fit(X_train, y_train)

# Save model and encoders
joblib.dump(model, "model.pkl")

joblib.dump(le_brand, "brand_encoder.pkl")
joblib.dump(le_fuel, "fuel_encoder.pkl")
joblib.dump(le_seller, "seller_encoder.pkl")
joblib.dump(le_trans, "trans_encoder.pkl")
joblib.dump(le_owner, "owner_encoder.pkl")

print("Advanced model trained successfully ✅")