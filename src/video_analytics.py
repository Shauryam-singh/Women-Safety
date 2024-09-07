import cv2
import numpy as np
import mediapipe as mp

class VideoAnalytics:
    def __init__(self, video_source, output_path=None):
        self.video_source = video_source
        self.cap = cv2.VideoCapture(video_source)
        self.output_path = output_path
        self.frame_count = 0

        self.fall_detected_flag = False
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose()
        self.mp_draw = mp.solutions.drawing_utils

        # Load DNN face detector
        self.net = cv2.dnn.readNetFromCaffe(r'model\deploy.prototxt', r'model\res10_300x300_ssd_iter_140000.caffemodel')

        # Initialize background subtractor for motion detection
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2()

        # Initialize video writer if output path is specified
        if output_path:
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            self.out = cv2.VideoWriter(output_path, fourcc, 20.0, (int(self.cap.get(3)), int(self.cap.get(4))))

        # Initialize tracking attributes
        self.trackers = []

        # Set window size
        self.window_width = 800
        self.window_height = 600

        # Initialize fall detection attributes
        self.activity_log = []

    def is_valid_bbox(self, bbox, frame_shape):
        x, y, w, h = bbox
        frame_height, frame_width = frame_shape[:2]
        return (0 <= x < frame_width) and (0 <= y < frame_height) and (0 < x + w <= frame_width) and (0 < y + h <= frame_height)

    def detect_faces(self, frame):
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
        self.net.setInput(blob)
        detections = self.net.forward()
        faces = []
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                faces.append((startX, startY, endX - startX, endY - startY))
        return faces

    def detect_fall(self, frame):
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        fg_mask = self.bg_subtractor.apply(gray_frame)
        contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        fall_detected = False

        # Pose estimation
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(frame_rgb)

        if results.pose_landmarks:
            self.mp_draw.draw_landmarks(frame, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
            # Analyze pose landmarks for fall detection

        for contour in contours:
            if cv2.contourArea(contour) > 500:  # Adjust this threshold as needed
                (x, y, w, h) = cv2.boundingRect(contour)
                fall_detected = True

        # Check if the fall detection state has changed
        if fall_detected and not self.fall_detected_flag:
            print("Fall detected!")
            self.fall_detected_flag = True
        elif not fall_detected:
            self.fall_detected_flag = False

    def process_video(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()

            if not ret:
                break

            frame = cv2.resize(frame, (self.window_width, self.window_height))

            # Detect faces
            faces = self.detect_faces(frame)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Detect falls
            self.detect_fall(frame)

            # Update object tracking
            if self.trackers:
                for tracker in self.trackers:
                    success, bbox = tracker.update(frame)
                    if success:
                        (x, y, w, h) = [int(v) for v in bbox]
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    else:
                        self.trackers.remove(tracker)

            # Display the frame
            cv2.imshow('Video Analytics', frame)

            # Save the frame if output path is specified
            if self.output_path:
                self.out.write(frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            self.frame_count += 1

        self.cap.release()
        if self.output_path:
            self.out.release()
        cv2.destroyAllWindows()

        # Print or save activity logs
        print("Activity Log:", self.activity_log)

if __name__ == "__main__":
    video_source = r"video\input\fall.mp4"
    output_path = r"video\output\output_video.mp4"
    video_analytics = VideoAnalytics(video_source, output_path)
    video_analytics.process_video()
