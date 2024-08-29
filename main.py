from src.video_analytics import VideoAnalytics
from src.anomaly_detection import AnomalyDetection

if __name__ == "__main__":
    video_analytics = VideoAnalytics(video_source=0)
    anomaly_detection = AnomalyDetection()

    data_sample = [0.6, 0.7, 0.5]

    video_analytics.process_video()
