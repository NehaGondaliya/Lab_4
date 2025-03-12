from flask import Flask, request, render_template
import joblib
import numpy as np

# Load model and preprocessors
model = joblib.load("fish_weight_model.pkl")
scaler = joblib.load("scaler.pkl")
label_encoder = joblib.load("label_encoder.pkl")

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get user input
        species = request.form["species"]
        length1 = float(request.form["length1"])
        length2 = float(request.form["length2"])
        length3 = float(request.form["length3"])
        height = float(request.form["height"])
        width = float(request.form["width"])

        # Encode species
        species_encoded = label_encoder.transform([species])[0]

        # Prepare input for model
        input_data = np.array([[species_encoded, length1, length2, length3, height, width]])
        input_data_scaled = scaler.transform(input_data)

        # Predict weight
        predicted_weight = model.predict(input_data_scaled)[0]

        return render_template("index.html", prediction=f"Predicted Fish Weight: {predicted_weight:.2f} grams")

    except Exception as e:
        return render_template("index.html", prediction=f"Error: {str(e)}")

if __name__ == "__main__":
    app.run(debug=True)
