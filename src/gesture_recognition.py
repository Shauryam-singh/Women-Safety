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
            gesture_detected = self.detect_gestures(results.pose_landmarks)
            if gesture_detected:
                print(f"Gesture detected: {gesture_detected}")
                return gesture_detected

        return None

    def detect_gestures(self, landmarks):
        # Customize gesture detection logic here
        if self.detect_sos_signal(landmarks):
            return "SOS"
        elif self.detect_help_signal(landmarks):
            return "Help"
        elif self.detect_call_for_help(landmarks):
            return "Call for Help"
        elif self.detect_stop_signal(landmarks):
            return "Stop"
        elif self.detect_no_signal(landmarks):
            return "No"
        elif self.detect_danger_signal(landmarks):
            return "Danger"
        else:
            return None

    def detect_sos_signal(self, landmarks):
        # Example logic for SOS gesture
        left_hand_up = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_WRIST].y < landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_SHOULDER].y
        right_hand_up = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_WRIST].y < landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_SHOULDER].y
        return left_hand_up and right_hand_up

    def detect_help_signal(self, landmarks):
        # Example logic for Help gesture
        left_hand_open = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_WRIST].y < landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_SHOULDER].y
        right_hand_open = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_WRIST].y < landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_SHOULDER].y
        return left_hand_open and right_hand_open

    def detect_call_for_help(self, landmarks):
        # Example logic for Call for Help gesture
        right_hand_on_ear = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_WRIST].x > landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_SHOULDER].x
        return right_hand_on_ear

    def detect_stop_signal(self, landmarks):
        # Example logic for Stop gesture (open palm facing camera)
        left_hand_open = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_WRIST].y < landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_SHOULDER].y
        return left_hand_open

    def detect_no_signal(self, landmarks):
        # Example logic for No gesture (shaking head or hand)
        head_tilted = landmarks.landmark[self.mp_pose.PoseLandmark.NOSE].y < landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_EAR].y
        return head_tilted

    def detect_danger_signal(self, landmarks):
        # Example logic for Danger gesture
        hand_near_throat = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_WRIST].x < landmarks.landmark[self.mp_pose.PoseLandmark.NOSE].x
        return hand_near_throat
