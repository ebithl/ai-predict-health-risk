from flask import Flask, request, jsonify
import joblib
import numpy as np
import os

app = Flask(__name__)

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
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 6000)), debug=True)
