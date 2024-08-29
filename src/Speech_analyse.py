import pyaudio
import numpy as np
import librosa
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pickle

def record_audio(duration=5, sample_rate=16000):
    chunk = 1024
    format = pyaudio.paInt16
    channels = 1

    audio = pyaudio.PyAudio()
    stream = audio.open(format=format, channels=channels, rate=sample_rate, input=True, frames_per_buffer=chunk)
    
    print("Recording...")
    frames = []

    for _ in range(0, int(sample_rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(np.frombuffer(data, dtype=np.int16))

    print("Finished recording.")
    stream.stop_stream()
    stream.close()
    audio.terminate()

    return np.concatenate(frames)

def extract_features(audio_signal, sample_rate=16000):
    mfccs = librosa.feature.mfcc(y=audio_signal, sr=sample_rate, n_mfcc=13)
    return np.mean(mfccs.T, axis=0)

# Dummy model training function
def train_model():
    # Simulated training data
    # In practice, replace this with your dataset
    X = np.array([
        # Example features (MFCCs)
        np.random.rand(13) for _ in range(100)
    ])
    y = np.random.randint(0, 2, size=(100,))  # 0 = non-distress, 1 = distress

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = RandomForestClassifier()
    model.fit(X_scaled, y)
    
    # Save the model and scaler to files
    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)
    with open('scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    
    print("Model trained and saved.")

def detect_distress(audio_signal, model, scaler, sample_rate=16000):
    features = extract_features(audio_signal, sample_rate)
    features_scaled = scaler.transform([features])
    prediction = model.predict(features_scaled)
    return prediction[0] == 1  # True if distress detected

# Function to alert if distress is detected
def alert_if_distress(audio_signal, model, scaler):
    if detect_distress(audio_signal, model, scaler):
        print("Distress detected! Triggering alert...")
        # Implement your alert logic here
    else:
        print("No distress detected.")

def main():
    # Uncomment the line below if you need to train the model
    # train_model()

    # Load the model and scaler
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    
    # Record audio and detect distress
    audio_signal = record_audio()
    alert_if_distress(audio_signal, model, scaler)

if __name__ == "__main__":
    main()
