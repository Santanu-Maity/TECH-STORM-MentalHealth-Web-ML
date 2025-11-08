from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
from flask_cors import CORS

# ------------------------------
# 1️⃣ Initialize Flask App
# ------------------------------
app = Flask(__name__)
CORS(app)  # Allow requests from frontend

# ------------------------------
# 2️⃣ Load Trained Model
# ------------------------------
model = pickle.load(open("model.pkl", "rb"))

# ------------------------------
# 3️⃣ Define Routes
# ------------------------------

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        # Extract all inputs safely
        sleep_hours = float(data.get("sleep_hours", 0))
        work_stress = float(data.get("work_stress", 0))
        screen_time = float(data.get("screen_time", 0))
        exercise_hours = float(data.get("exercise_hours", 0))
        food_quality = float(data.get("food_quality", 0))
        financial_stress = float(data.get("financial_stress", 0))
        introvert_extrovert = data.get("introvert_extrovert", "introvert")

        # Convert introvert/extrovert to numeric value
        introvert_extrovert_num = 0 if introvert_extrovert.lower() == "introvert" else 1

        # Prepare features in the same order as training
        features = np.array([[sleep_hours, work_stress, screen_time,
                              exercise_hours, food_quality, financial_stress,
                              introvert_extrovert_num]])

        # Make prediction
        prediction = model.predict(features)[0]

        # Map model output to readable labels
        label_map = {0: "anxious", 1: "depressed", 2: "happy", 3: "stable", 4: "stressed"}
        result = label_map.get(prediction, "unknown")

        return jsonify({"mental_state": result})

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500


# ------------------------------
# 4️⃣ Run App
# ------------------------------
if __name__ == "__main__":
    app.run(debug=True)
