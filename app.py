from flask import Flask, render_template, request
import json
import os

app = Flask(__name__, static_folder='static')

# Load JSON safely from the same folder as app.py
json_path = os.path.join(os.path.dirname(__file__), 'symptom_data.json')
with open(json_path) as f:
    symptom_map = json.load(f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check_symptoms():
    raw_input = request.form['symptoms']
    mode = request.form['mode']

    symptoms = [s.strip().lower() for s in raw_input.split(',') if s.strip()]
    result = "Unknown – please consult a doctor"
    urgency = None

    for entry in symptom_map.get(mode, []):
        entry_symptoms = [s.lower() for s in entry["symptoms"]]
        if any(symptom in entry_symptoms for symptom in symptoms):
            result = entry["condition"]
            urgency = entry["urgency"]
            break

    return render_template('index.html', result=result, urgency=urgency)

if __name__ == '__main__':
    app.run(debug=True)