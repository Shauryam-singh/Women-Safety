import pyaudio
import numpy as np
import os
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

def train_model():
    X = np.array([
        np.random.rand(13) for _ in range(100)
    ])
    y = np.random.randint(0, 2, size=(100,))

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = RandomForestClassifier()
    model.fit(X_scaled, y)
    
    with open('model\model.pkl', 'wb') as f:
        pickle.dump(model, f)
    with open('model\scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    
    print("Model trained and saved.")

def detect_distress(audio_signal, model, scaler, sample_rate=16000):
    features = extract_features(audio_signal, sample_rate)
    features_scaled = scaler.transform([features])
    prediction = model.predict(features_scaled)
    return prediction[0] == 1

def alert_if_distress(audio_signal, model, scaler):
    if detect_distress(audio_signal, model, scaler):
        print("Distress detected! Triggering alert...")
    else:
        print("No distress detected.")