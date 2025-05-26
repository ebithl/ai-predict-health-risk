import time
import json
import random

def generate_random_vitals():
    return {
        "temp": round(random.uniform(96.5, 104.0), 1),
        "pulse": random.randint(50, 130),
        "spo2": random.randint(88, 100),
        "rr": random.randint(10, 30),
        "bp": f"{random.randint(90, 160)}/{random.randint(60, 100)}"
    }

while True:
    # Load patients.json
    with open('patients.json', 'r') as f:
        patients = json.load(f)

    # Update vitals
    for patient in patients:
        patient["vitals"].append(generate_random_vitals())
        if len(patient["vitals"]) > 20:
            patient["vitals"].pop(0)

    # Save
    with open('patients.json', 'w') as f:
        json.dump(patients, f, indent=2)

    time.sleep(10)  # Update every 10 seconds
