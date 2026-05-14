print ("APP STARTED SUCCESSFULLY!")

from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

print("LOADING DATASET...")

# -----------------------------------
# LOAD DATASET
# -----------------------------------

df = pd.read_csv(
    "electricity.csv",
    na_values='?',
    low_memory=False,
    nrows=50000
)

print("DATASET LOADED!")

# -----------------------------------
# REMOVE MISSING VALUES
# -----------------------------------

df = df.dropna()

# -----------------------------------
# CONVERT COLUMNS TO NUMERIC
# -----------------------------------

columns = [
    'Voltage',
    'Global_intensity',
    'Sub_metering_1',
    'Sub_metering_2',
    'Sub_metering_3',
    'Global_active_power'
]

for col in columns:
    df[col] = pd.to_numeric(df[col])

# -----------------------------------
# FEATURES & TARGET
# -----------------------------------

X = df[[
    'Voltage',
    'Global_intensity',
    'Sub_metering_1',
    'Sub_metering_2',
    'Sub_metering_3'
]]

y = df['Global_active_power']

# -----------------------------------
# TRAIN TEST SPLIT
# -----------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# -----------------------------------
# TRAIN MODEL
# -----------------------------------

print("TRAINING MODEL...")

model = LinearRegression()

model.fit(X_train, y_train)

print("MODEL TRAINED SUCCESSFULLY!")

# -----------------------------------
# CREATE FLASK APP
# -----------------------------------

app = Flask(__name__)

# -----------------------------------
# HOME ROUTE
# -----------------------------------

@app.route("/")
def home():
    return render_template("index.html")

# -----------------------------------
# PREDICTION ROUTE
# -----------------------------------

@app.route("/predict", methods=["POST"])
def predict():

    try:

        data = request.get_json()

        voltage = float(data["voltage"])
        intensity = float(data["intensity"])
        sub1 = float(data["sub_metering_1"])
        sub2 = float(data["sub_metering_2"])
        sub3 = float(data["sub_metering_3"])

        features = np.array([
            [voltage, intensity, sub1, sub2, sub3]
        ])

        prediction = model.predict(features)

        return jsonify({
            "status": "success",
            "predicted_consumption": round(float(prediction[0]), 3)
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        })

# -----------------------------------
# RUN SERVER
# -----------------------------------

import os

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )
