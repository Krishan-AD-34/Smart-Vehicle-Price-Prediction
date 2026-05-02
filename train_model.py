import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import r2_score, mean_absolute_error

from xgboost import XGBRegressor

# ==========================================
# LOAD DATASET
# ==========================================

df = pd.read_csv("cardekho_dataset.csv")

print("\nDataset Loaded Successfully!\n")
print(df.head())

# ==========================================
# BASIC CLEANING
# ==========================================

df.dropna(inplace=True)

# Remove duplicates
df.drop_duplicates(inplace=True)

# ==========================================
# REMOVE OUTLIERS
# ==========================================

# Remove extremely cheap cars
df = df[df["selling_price"] > 100000]

# Remove extremely expensive cars
df = df[df["selling_price"] < 50000000]

# Remove unrealistic kms
df = df[df["km_driven"] < 300000]

# Remove very old cars
df = df[df["vehicle_age"] < 18]

# ==========================================
# CLEAN NUMERIC COLUMNS
# ==========================================

numeric_columns = [
    "vehicle_age",
    "km_driven",
    "mileage",
    "engine",
    "max_power",
    "seats",
    "selling_price"
]

for col in numeric_columns:

    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )

# Fill missing numeric values
for col in numeric_columns:

    df[col].fillna(
        df[col].median(),
        inplace=True
    )

# ==========================================
# CLEAN STRING COLUMNS
# ==========================================

string_columns = [
    "brand",
    "car_name",
    "seller_type",
    "fuel_type",
    "transmission_type"
]

for col in string_columns:

    df[col] = (
        df[col]
        .astype(str)
        .str.strip()
    )



# ==========================================
# FINAL FEATURES
# ==========================================

final_features = [
    "brand",
    "car_name",
    "vehicle_age",
    "km_driven",
    "seller_type",
    "fuel_type",
    "transmission_type",
    "mileage",
    "engine",
    "max_power",
    "seats",
]

X = df[final_features]

# ==========================================
# LOG TRANSFORM TARGET
# ==========================================

y = np.log1p(df["selling_price"])

# ==========================================
# CATEGORICAL FEATURES
# ==========================================

categorical_features = [
    "brand",
    "car_name",
    "seller_type",
    "fuel_type",
    "transmission_type"
]

# ==========================================
# PREPROCESSOR
# ==========================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "cat",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        )
    ],
    remainder="passthrough"
)

# ==========================================
# MODEL
# ==========================================

xgb_model = XGBRegressor(

    n_estimators=1200,
    learning_rate=0.02,
    max_depth=10,

    min_child_weight=3,

    subsample=0.9,
    colsample_bytree=0.9,

    gamma=0.1,

    reg_alpha=0.1,
    reg_lambda=1,

    random_state=42,

    objective="reg:squarederror",

    n_jobs=-1
)

# ==========================================
# PIPELINE
# ==========================================

model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("regressor", xgb_model)
    ]
)

# ==========================================
# TRAIN TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# ==========================================
# TRAIN MODEL
# ==========================================

print("\nTraining Started...\n")

model.fit(X_train, y_train)

print("\nTraining Completed!\n")

# ==========================================
# PREDICTION
# ==========================================

pred_log = model.predict(X_test)

# Reverse log transform
pred = np.expm1(pred_log)

actual = np.expm1(y_test)

# ==========================================
# EVALUATION
# ==========================================

r2 = r2_score(actual, pred)

mae = mean_absolute_error(actual, pred)

print(f"\nR2 Score : {r2:.4f}")

print(f"MAE      : ₹ {mae:,.0f}")

# ==========================================
# SAVE MODEL
# ==========================================

joblib.dump(model, "model.pkl")

# ==========================================
# BRAND -> MODELS MAPPING
# ==========================================

brand_model_map = {}

for brand in sorted(df["brand"].unique()):

    models = sorted(

        df[df["brand"] == brand]["car_name"]
        .unique()
        .tolist()
    )

    brand_model_map[brand] = models

joblib.dump(
    brand_model_map,
    "brand_model_map.pkl"
)

# ==========================================
# SAVE FEATURES
# ==========================================

joblib.dump(
    final_features,
    "features.pkl"
)

# ==========================================
# SAVE BRANDS
# ==========================================

brands = sorted(
    df["brand"]
    .unique()
    .tolist()
)

joblib.dump(
    brands,
    "brands.pkl"
)

# ==========================================
# DONE
# ==========================================

print("\n===================================")

print("Model saved successfully!")

print("brand_model_map.pkl saved!")

print("features.pkl saved!")

print("brands.pkl saved!")

print("===================================")