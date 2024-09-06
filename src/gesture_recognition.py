import cv2
import mediapipe as mp
import numpy as np
from alert_system import AlertSystem  # Replace with the actual module name

class GestureRecognition:
    def __init__(self, recipient_phone):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.8, min_tracking_confidence=0.8)
        self.mp_draw = mp.solutions.drawing_utils
        self.smoothing_buffer = []
        
        # Initialize the alert system with recipient phone
        self.alert_system = AlertSystem(recipient_phone)

    def recognize_gesture(self, frame):
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(img_rgb)

        gesture_name = None
        if results.pose_landmarks:
            self.mp_draw.draw_landmarks(frame, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
            gesture_detected = self.detect_gestures(results.pose_landmarks)
            if gesture_detected:
                self.update_smoothing_buffer(gesture_detected)
                if self.is_gesture_stable():
                    gesture_name = gesture_detected
                    self.trigger_alert(gesture_name)

        if gesture_name:
            self.display_gesture_name(frame, gesture_name)

        return gesture_name

    def update_smoothing_buffer(self, gesture_name):
        if len(self.smoothing_buffer) >= 5:
            self.smoothing_buffer.pop(0)
        self.smoothing_buffer.append(gesture_name)

    def is_gesture_stable(self):
        return len(self.smoothing_buffer) > 0 and all(g == self.smoothing_buffer[0] for g in self.smoothing_buffer)

    def detect_gestures(self, landmarks):
        # Check gestures in order of confidence
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
        elif self.detect_yell_signal(landmarks):  # New gesture example
            return "Yell"
        elif self.detect_come_here_signal(landmarks):  # New gesture example
            return "Come Here"
        else:
            return None

    def detect_sos_signal(self, landmarks):
        # Example logic for SOS gesture: Both hands raised and open
        left_hand_up = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_WRIST].y < landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_SHOULDER].y
        right_hand_up = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_WRIST].y < landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_SHOULDER].y
        left_hand_open = self.is_hand_open(landmarks, self.mp_pose.PoseLandmark.LEFT_WRIST)
        right_hand_open = self.is_hand_open(landmarks, self.mp_pose.PoseLandmark.RIGHT_WRIST)
        return left_hand_up and right_hand_up and left_hand_open and right_hand_open

    def detect_help_signal(self, landmarks):
        # Example logic for Help gesture: Hands open and facing camera
        left_hand_open = self.is_hand_open(landmarks, self.mp_pose.PoseLandmark.LEFT_WRIST)
        right_hand_open = self.is_hand_open(landmarks, self.mp_pose.PoseLandmark.RIGHT_WRIST)
        return left_hand_open and right_hand_open

    def detect_call_for_help(self, landmarks):
        # Example logic for Call for Help gesture: Right hand touching the ear
        right_hand_on_ear = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_WRIST].x < landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_SHOULDER].x and \
                            landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_WRIST].y < landmarks.landmark[self.mp_pose.PoseLandmark.NOSE].y
        return right_hand_on_ear

    def detect_stop_signal(self, landmarks):
        # Example logic for Stop gesture: Open palm facing camera
        left_hand_open = self.is_hand_open(landmarks, self.mp_pose.PoseLandmark.LEFT_WRIST)
        return left_hand_open

    def detect_no_signal(self, landmarks):
        # Example logic for No gesture: Head tilted side-to-side
        head_tilted = landmarks.landmark[self.mp_pose.PoseLandmark.NOSE].y < landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_EAR].y
        return head_tilted

    def detect_danger_signal(self, landmarks):
        # Example logic for Danger gesture: Hand near throat
        hand_near_throat = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_WRIST].x < landmarks.landmark[self.mp_pose.PoseLandmark.NOSE].x and \
                           landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_WRIST].y < landmarks.landmark[self.mp_pose.PoseLandmark.NOSE].y
        return hand_near_throat

    def detect_yell_signal(self, landmarks):
        # Example logic for Yell gesture: Hand raised to mouth
        hand_near_mouth = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_WRIST].x < landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_ELBOW].x and \
                          landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_WRIST].y < landmarks.landmark[self.mp_pose.PoseLandmark.NOSE].y
        return hand_near_mouth

    def detect_come_here_signal(self, landmarks):
        # Example logic for Come Here gesture: Hand waved toward body
        hand_waved = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_WRIST].x < landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_SHOULDER].x and \
                     landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_WRIST].y > landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_SHOULDER].y
        return hand_waved

    def is_hand_open(self, landmarks, wrist_landmark):
        # Check if hand is open based on wrist position relative to shoulder
        wrist_y = landmarks.landmark[wrist_landmark].y
        shoulder_y = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_SHOULDER if wrist_landmark == self.mp_pose.PoseLandmark.LEFT_WRIST else self.mp_pose.PoseLandmark.RIGHT_SHOULDER].y
        return wrist_y < shoulder_y

    def display_gesture_name(self, frame, gesture_name):
        # Display the gesture name on the frame
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, f"Gesture: {gesture_name}", (10, 50), font, 1, (0, 255, 0), 2, cv2.LINE_AA)

    def trigger_alert(self, gesture_name):
        # Trigger the alert system based on detected gesture
        if gesture_name in ["SOS", "Help", "Call for Help", "Danger"]:
            self.alert_system.send_alert(gesture_name)

if __name__ == "__main__":
    recipient_phone = "+916307257097"
    cap = cv2.VideoCapture(0)
    gesture_recognition = GestureRecognition(recipient_phone)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        gesture_recognition.recognize_gesture(frame)

        cv2.imshow('Gesture Recognition', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
