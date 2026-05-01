import os

from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np

app = Flask(__name__)

# Load model
model = joblib.load("model.pkl")

# Load encoders
encoders = joblib.load("encoders.pkl")


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():

    data = request.json

    try:

        # Extract brand name
        brand_name = data['brand'].split()[0]

        # Encode categorical values
        brand = encoders["brand"].transform([brand_name])[0]

        fuel = encoders["fuel"].transform(
            [data['fuel']]
        )[0]

        seller = encoders["seller_type"].transform(
            [data['seller_type']]
        )[0]

        trans = encoders["transmission"].transform(
            [data['transmission']]
        )[0]

        owner = encoders["owner"].transform(
            [data['owner']]
        )[0]

        # Input values
        car_age = int(data['car_age'])
        km_driven = int(data['km_driven'])

        # Feature order MUST match training
        features = np.array([[

            km_driven,
            fuel,
            seller,
            trans,
            owner,
            car_age,
            brand

        ]])

        # Prediction
        prediction = float(model.predict(features)[0])

        # =========================
        # SMART PRICE CORRECTIONS
        # =========================

        # Realistic bounds
        prediction = max(50000, prediction)
        prediction = min(prediction, 5000000)

        # Depreciation by age
        if car_age > 15:
            prediction *= 0.75

        elif car_age > 10:
            prediction *= 0.85

        # KM driven penalty
        if km_driven > 150000:
            prediction *= 0.80

        elif km_driven > 100000:
            prediction *= 0.90

        # Premium brand bonus
        premium_brands = [
            "BMW",
            "Mercedes-Benz",
            "Audi",
            "Jaguar",
            "Lexus",
            "Volvo"
        ]

        if brand_name in premium_brands:
            prediction *= 1.35

        # Final rounding
        prediction = round(prediction, 2)

        # Price range
        lower_price = round(prediction * 0.95)
        upper_price = round(prediction * 1.05)

        # Confidence
        confidence = 82

        return jsonify({

            "predicted_price": prediction,

            "lower_price": lower_price,

            "upper_price": upper_price,

            "confidence": confidence

        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        })


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )