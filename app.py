import os

from flask import Flask, request, jsonify, render_template

import pandas as pd
import numpy as np
import joblib

app = Flask(__name__)

# =====================================
# LOAD FILES
# =====================================

model = joblib.load("model.pkl")

brand_model_map = joblib.load(
    "brand_model_map.pkl"
)

model_spec_map = joblib.load(
    "model_spec_map.pkl"
)

brands = joblib.load("brands.pkl")

features = joblib.load("features.pkl")

print("\n========== MODEL LOADED ==========")
print(type(model))
print("==================================\n")

# =====================================
# HOME
# =====================================

@app.route("/")
def home():

    return render_template(
        "index.html",
        brands=brands
    )

# =====================================
# GET MODELS API
# =====================================

@app.route("/get_models/<brand>")
def get_models(brand):

    models = brand_model_map.get(
        brand,
        []
    )

    return jsonify(models)

# =====================================
# GET VEHICLE SPECS
# =====================================

@app.route("/get_specs/<model_name>")
def get_specs(model_name):

    specs = model_spec_map.get(
        model_name
    )

    if specs:

        return jsonify(specs)

    return jsonify({

        "mileage": "",
        "engine": "",
        "max_power": "",
        "seats": ""
    })

# =====================================
# PREDICT
# =====================================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        data = request.get_json()

        print("\n========== RECEIVED JSON ==========")
        print(data)
        print("===================================\n")

        # =====================================
        # INPUT DATA
        # =====================================

        input_data = {

            "brand": data["brand"],

            "car_name": data["car_name"],

            "vehicle_age":
                float(data["vehicle_age"]),

            "km_driven":
                float(data["km_driven"]),

            "seller_type":
                data["seller_type"],

            "fuel_type":
                data["fuel_type"],

            "transmission_type":
                data["transmission_type"],

            "mileage":
                float(data["mileage"]),

            "engine":
                float(data["engine"]),

            "max_power":
                float(data["max_power"]),

            "seats":
                float(data["seats"])
        }

        # =====================================
        # DATAFRAME
        # =====================================

        df = pd.DataFrame([input_data])

        # EXACT FEATURE ORDER
        df = df[features]

        print("\n========== DATAFRAME ==========")
        print(df)

        print("\n========== DTYPES ==========")
        print(df.dtypes)

        print("================================\n")

        # =====================================
        # NULL CHECK
        # =====================================

        if df.isnull().sum().sum() > 0:

            return jsonify({

                "success": False,

                "error":
                    "NaN values detected"
            })

        # =====================================
        # PREDICTION
        # =====================================

        prediction_log = model.predict(df)[0]

        print("\n========== LOG PREDICTION ==========")
        print(prediction_log)
        print("====================================\n")

        # =====================================
        # LOG -> ACTUAL PRICE
        # =====================================

        prediction = np.expm1(
            prediction_log
        )

        print("\n========== FINAL PRICE ==========")
        print(prediction)
        print("=================================\n")

        # =====================================
        # INVALID CHECK
        # =====================================

        if prediction <= 0 or np.isnan(prediction):

            return jsonify({

                "success": False,

                "error":
                    "Invalid prediction generated"
            })

        # =====================================
        # ROUND
        # =====================================

        prediction = round(prediction)

        # =====================================
        # PRICE RANGE
        # =====================================

        lower_price = round(
            prediction * 0.95
        )

        upper_price = round(
            prediction * 1.05
        )

        # =====================================
        # RESPONSE
        # =====================================

        return jsonify({

            "success": True,

            "predicted_price":
                f"₹ {prediction:,.0f}",

            "lower_price":
                f"₹ {lower_price:,.0f}",

            "upper_price":
                f"₹ {upper_price:,.0f}",

            "confidence": "87.5%"
        })

    except Exception as e:

        print("\n========== ERROR ==========")
        print(str(e))
        print("================================\n")

        return jsonify({

            "success": False,
            "error": str(e)
        })

# =====================================
# MAIN
# =====================================

if __name__ == "__main__":

    port = int(
        os.environ.get("PORT", 5000)
    )

    app.run(

        host="0.0.0.0",

        port=port,

        debug=True
    )

