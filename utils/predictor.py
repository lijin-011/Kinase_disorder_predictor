import numpy as np
import pickle

# Hydrophobicity, disorder propensity, etc. (same as your notebook)
hydrophobicity_scale = {
    'A': 1.8, 'C': 2.5, 'D': -3.5, 'E': -3.5, 'F': 2.8, 'G': -0.4,
    'H': -3.2, 'I': 4.5, 'K': -3.9, 'L': 3.8, 'M': 1.9, 'N': -3.5,
    'P': -1.6, 'Q': -3.5, 'R': -4.5, 'S': -0.8, 'T': -0.7, 'V': 4.2,
    'W': -0.9, 'Y': -1.3
}
pKa_values = {'N_term': 9.0, 'C_term': 2.0, 'D': 3.9, 'E': 4.3, 'H': 6.0, 'K': 10.5, 'R': 12.5}
disorder_promoting_residues = {'K', 'Q', 'S', 'E', 'P', 'A', 'G', 'D'}
order_promoting_residues = {'C', 'W', 'I', 'Y', 'F', 'L', 'H', 'V', 'N', 'M'}
disorder_propensity = {
    'A': 0.06, 'C': 0.02, 'D': 0.192, 'E': 0.736, 'F': -0.697, 'G': 0.166,
    'H': 0.303, 'I': -0.486, 'K': 0.586, 'L': -0.326, 'M': -0.397, 'N': 0.007,
    'P': 0.5, 'Q': 0.318, 'R': 0.180, 'S': 0.341, 'T': 0.5, 'V': -0.121,
    'W': -0.884, 'Y': -0.510
}

def henderson_hasselbalch(pKa, pH):
    return 10**(pKa - pH) / (1 + 10**(pKa - pH))

def calculate_net_charge(sequence, pH=7.4):
    charge = 0.0
    charge += henderson_hasselbalch(pKa_values['N_term'], pH)
    charge -= henderson_hasselbalch(pKa_values['C_term'], pH)
    for aa in sequence:
        if aa in pKa_values:
            if aa in ['D', 'E']:
                charge -= 1 / (1 + 10**(pKa_values[aa] - pH))
            elif aa in ['H', 'K', 'R']:
                charge += 1 / (1 + 10**(pH - pKa_values[aa]))
    return charge

def extract_features(sequence, pH=7.0):
    features = []
    for aa in sequence:
        aa_features = [
            hydrophobicity_scale.get(aa, 0),
            disorder_propensity.get(aa, 0),
            calculate_net_charge(aa, pH),
            1 if aa in disorder_promoting_residues else 0,
            1 if aa in order_promoting_residues else 0
        ]
        features.append(aa_features)
    return np.array(features)

def load_model_and_scaler():
    with open('model/disorder_prediction_model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('model/scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    with open('model/processed_data.pkl', 'rb') as f:
        data = pickle.load(f)
    max_len = data['X_train'].shape[1]
    return model, scaler, max_len

def predict_disorder(sequence, model, scaler, max_len, threshold=0.25):
    features = extract_features(sequence)
    features_padded = np.pad(features, ((0, max_len - len(features)), (0, 0)), 'constant')
    features_scaled = scaler.transform(features_padded.reshape(-1, features_padded.shape[-1])).reshape(1, *features_padded.shape)
    prediction = model.predict(features_scaled)[0]
    binary_prediction = (prediction > threshold).astype(int).flatten()
    binary_prediction = binary_prediction[:len(sequence)]
    raw_probs = prediction[:len(sequence)].flatten()
    return ''.join(map(str, binary_prediction)), raw_probs