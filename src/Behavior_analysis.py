import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import pickle

# Load and preprocess data
def load_and_preprocess_data(file_path):
    # Load data (e.g., from a CSV file)
    data = pd.read_csv(file_path)
    
    # Preprocess data (e.g., normalization)
    features = data[['feature1', 'feature2', 'feature3']]  # Replace with your feature columns
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)
    
    return features_scaled, scaler

# Train anomaly detection model
def train_model(features):
    model = IsolationForest(contamination=0.1)  # Adjust contamination rate as needed
    model.fit(features)
    
    # Save the model
    with open('anomaly_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    print("Model trained and saved.")

# Detect anomalies
def detect_anomalies(features, model):
    predictions = model.predict(features)
    return predictions  # -1 for anomaly, 1 for normal

# Main function
def main():
    # Load and preprocess data
    features, scaler = load_and_preprocess_data('behavior_data.csv')
    
    # Train the model
    train_model(features)
    
    # Load the model
    with open('anomaly_model.pkl', 'rb') as f:
        model = pickle.load(f)
    
    # Detect anomalies on new data
    new_data = pd.read_csv('new_behavior_data.csv')
    new_features = scaler.transform(new_data[['feature1', 'feature2', 'feature3']])
    anomalies = detect_anomalies(new_features, model)
    
    print("Anomalies detected:", np.sum(anomalies == -1))

if __name__ == "__main__":
    main()
