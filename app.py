from flask import Flask, request, jsonify
import joblib
import numpy as np
import os
import threading
import time
import json
import random

app = Flask(__name__)

def generate_random_vitals():
    return {
        "temp": round(random.uniform(96.5, 104.0), 1),
        "pulse": random.randint(50, 130),
        "spo2": random.randint(88, 100),
        "rr": random.randint(10, 30),
        "bp": f"{random.randint(90, 160)}/{random.randint(60, 100)}"
    }

def run_simulator():
    while True:
        try:
            with open('patients.json', 'r') as f:
                patients = json.load(f)

            for patient in patients:
                patient["vitals"].append(generate_random_vitals())
                if len(patient["vitals"]) > 20:
                    patient["vitals"].pop(0)

            with open('patients.json', 'w') as f:
                json.dump(patients, f, indent=2)

            time.sleep(10)
        except Exception as e:
            print("Simulator error:", e)

if not os.path.exists('patients.json'):
    with open('patients.json', 'w') as f:
        json.dump([], f)



# Load the trained model
model = joblib.load('risk_model.pkl')  # Make sure this path is correct

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    # Extract vitals
    try:
        temp = float(data['temp'])
        pulse = float(data['pulse'])
        spo2 = float(data['spo2'])
        rr = float(data['rr'])
        sysdia = (data['bp']).split("/");
        bp = float(sysdia[0])
    except (KeyError, ValueError) as e:
        return jsonify({'error': 'Invalid or missing input data'}), 400

    # Prepare input for the model
    input_features = np.array([[temp, pulse, spo2, rr, bp]])

    # Make prediction
    prediction = model.predict(input_features)[0]

    return jsonify({
        'risk_level': int(prediction)  # Ensures JSON-safe response
    })

if __name__ == '__main__':
    # Start simulator in background
    threading.Thread(target=run_simulator, daemon=True).start()
    # Start predict web service
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 6000)), debug=True)
