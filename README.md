# Disorder Prediction Flask App

A web application for predicting intrinsically disordered regions in human kinome protein sequences using a deep learning model.

## Features

- Paste a protein sequence and get disorder predictions.
- Responsive, animated UI.
- Hover and scroll effects.
- Error handling for invalid input.

## Usage

1. Place your trained model files (`disorder_prediction_model.pkl`, `scaler.pkl`, `processed_data.pkl`) in the `model/` folder.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the app:
   ```
   python app.py
   ```
4. Open [http://localhost:5000](http://localhost:5000) in your browser.

## File Structure

See the included code for details.