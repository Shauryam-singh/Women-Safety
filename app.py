from flask import Flask, request, render_template, redirect, url_for, jsonify
from src.Geofencing import check_geofence
from src.Route_finder import create_route
from src.Speech_analyse import analyze_speech
from src.alert_system import AlertSystem
from src.anomaly_detection import detect_anomalies
from src.gesture_recognition import GestureRecognition
from src.video_analytics import VideoAnalytics
from src.gesture_recognition import GestureRecognition
import os
import numpy as np
import cv2

app = Flask(__name__)

ALERT_RECIPIENT_PHONE = "+916307257097"

if not os.path.exists('temp'):
    os.makedirs('temp')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/geofencing', methods=['GET', 'POST'])
def geofencing():
    if request.method == 'POST':
        try:
            latitude = float(request.form.get('latitude'))
            longitude = float(request.form.get('longitude'))
            result = check_geofence(latitude, longitude)
            return render_template('geofencing.html', result=result)
        except ValueError as e:
            return render_template('geofencing.html', error=f"Invalid input: {e}")
    return render_template('geofencing.html')

@app.route('/route_finder', methods=['GET', 'POST'])
def route_finder():
    if request.method == 'POST':
        try:
            start_location = request.form.get('start_location')
            end_location = request.form.get('end_location')
            route_info = create_route(start_location, end_location)
            return render_template('route_finder.html', route_info=route_info)
        except Exception as e:
            return render_template('route_finder.html', error=str(e))
    return render_template('route_finder.html')

@app.route('/analyze_speech', methods=['POST'])
def speech_analysis():
    try:
        duration = int(request.form.get('duration', 5)) 
        analyze_speech(duration)
        return render_template('analyze_speech.html')
    except Exception as e:
        return str(e)

@app.route('/gesture_recognition_page')
def gesture_recognition_page():
    return render_template('gesture_recognition.html')

@app.route('/recognize_gesture', methods=['POST'])
def recognize_gesture():
    if 'video_frame' not in request.files:
        return jsonify({'error': 'No video frame found'}), 400

    video_frame = request.files['video_frame'].read()
    np_img = np.frombuffer(video_frame, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    gesture_name = GestureRecognition.recognize_gesture(img)

    return jsonify({'gesture': gesture_name})

@app.route('/video_analytics', methods=['GET', 'POST'])
def video_analytics():
    if request.method == 'POST' and 'video_file' in request.files:
        video_file = request.files['video_file']
        video_path = os.path.join('temp', video_file.filename)
        video_file.save(video_path)
        
        try:
            video_analytics = VideoAnalytics(video_path)
            video_analytics.process_video()
            result = "Video processed successfully!"
        except Exception as e:
            result = f"Error: {e}"
        finally:
            os.remove(video_path)
        
        return render_template('video_analytics.html', result=result)
    return render_template('video_analytics.html')

if __name__ == "__main__":
    app.run(debug=True)
