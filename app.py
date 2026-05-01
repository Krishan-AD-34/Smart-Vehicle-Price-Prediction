import os

from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np

app = Flask(__name__)

# Load model
model = joblib.load("model.pkl")

# Load encoders
le_brand = joblib.load("brand_encoder.pkl")
le_fuel = joblib.load("fuel_encoder.pkl")
le_seller = joblib.load("seller_encoder.pkl")
le_trans = joblib.load("trans_encoder.pkl")
le_owner = joblib.load("owner_encoder.pkl")


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():

    data = request.json

    try:

        # Encode categorical values
        brand_name = data['brand'].split()[0]

        brand = le_brand.transform([brand_name])[0]
        fuel = le_fuel.transform([data['fuel']])[0]
        seller = le_seller.transform([data['seller_type']])[0]
        trans = le_trans.transform([data['transmission']])[0]
        owner = le_owner.transform([data['owner']])[0]

        # Feature array
        car_age = data['car_age']
        year = 2026 - car_age

        features = np.array([[

        brand,
        year,
        fuel,
        seller,
        trans,
        owner,
        data['km_driven'],
        data['mileage'],
        data['engine'],
        car_age

    ]])

        # Prediction
        prediction = float(model.predict(features)[0])

        return jsonify({
            "predicted_price": round(prediction, 2)
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)