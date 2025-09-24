# Placeholder ML module.
# This module contains a simple scaffold for training/predicting.
# If you have labeled data, implement train() to build a LightGBM or sklearn model.

import os
import pickle

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.pkl')

def train(X, y):
    # X: pandas DataFrame or feature matrix
    # y: labels
    # Implement model training here (LightGBM / sklearn). For now, we save a trivial stub.
    model = {'type': 'stub', 'classes': sorted(set(y))}
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(model, f)
    return model

def load_model():
    if os.path.exists(MODEL_PATH):
        import pickle
        with open(MODEL_PATH, 'rb') as f:
            return pickle.load(f)
    return None

def predict(model, X):
    # For each row return (predicted_class, confidence, explanation)
    # This stub returns 'OTHERS' with low confidence.
    out = []
    for _ in range(len(X)):
        out.append(('OTHERS', 0.6, 'Model stub - no trained model available'))
    return out
