from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

# Load symptom data
with open("symptom_data.json") as f:
    symptom_data = json.load(f)

@app.route("/", methods=["GET", "POST"])
def index():
    diagnosis = None
    if request.method == "POST":
        symptoms = request.form.get("symptoms", "").lower().split(",")
        matched_conditions = []

        for condition in symptom_data:
            if any(symptom.strip() in condition["symptoms"] for symptom in symptoms):
                matched_conditions.append(condition)

        if matched_conditions:
            diagnosis = matched_conditions
        else:
            diagnosis = [{"condition": "No match found", "urgency": "Unknown"}]

    return render_template("index.html", diagnosis=diagnosis)

# ✅ This part ensures compatibility with Render or Replit
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)