from flask import Flask, render_template, request, redirect, url_for
import os
from utils.predictor import load_model_and_scaler, predict_disorder

app = Flask(__name__)

# Load model and scaler once at startup
model, scaler, max_len = load_model_and_scaler()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    sequence = request.form.get('sequence', '').strip().upper()
    valid_aas = set('ACDEFGHIKLMNPQRSTVWY')
    if not sequence or not all(aa in valid_aas for aa in sequence):
        return render_template('error.html', message="Invalid sequence. Please use only valid amino acid letters (A, C, D, E, F, G, H, I, K, L, M, N, P, Q, R, S, T, V, W, Y).")
    try:
        binary_pred, raw_probs = predict_disorder(sequence, model, scaler, max_len)
        # Convert binary_pred string to list of ints/strs
        binary_pred_list = list(binary_pred)
        # Zip the results for the template
        results = list(zip(sequence, binary_pred_list, raw_probs))
        return render_template('result.html', sequence=sequence, results=results)
    except Exception as e:
        return render_template('error.html', message=str(e))

if __name__ == '__main__':
    app.run(debug=True)