import cv2
import mediapipe as mp

class GestureRecognition:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose()
        self.mp_draw = mp.solutions.drawing_utils

    def recognize_gesture(self, frame):
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(img_rgb)

        if results.pose_landmarks:
            self.mp_draw.draw_landmarks(frame, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
            if self.detect_sos_signal(results.pose_landmarks):
                print("SOS signal detected!")
                return True

        return False

    def detect_sos_signal(self, landmarks):
        # Simple example logic for detecting a specific gesture
        # Customize with specific detection logic based on landmarks
        left_hand_up = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_WRIST].y < landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_SHOULDER].y
        right_hand_up = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_WRIST].y < landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_SHOULDER].y
        return left_hand_up and right_hand_up
