from src.video_analytics import VideoAnalytics
from src.anomaly_detection import AnomalyDetection
from src.alert_system import AlertSystem

if __name__ == "__main__":
    video_analytics = VideoAnalytics(video_source=0)
    anomaly_detection = AnomalyDetection()
    alert_system = AlertSystem("shauryamsingh9@gmail.com")  # No keyword argument here

    # Example data for anomaly detection
    data_sample = [0.6, 0.7, 0.5]  # Replace with real data from video analysis

    # Process the video and detect gestures
    video_analytics.process_video()

    # Anomaly detection
    if anomaly_detection.detect_anomaly(data_sample):
        alert_system.send_alert("An anomaly was detected during video analysis.")
