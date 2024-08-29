import cv2
import mediapipe as mp
from src.alert_system import AlertSystem

class VideoAnalytics:
    def __init__(self, video_source=0):
        self.video_source = video_source
        self.cap = cv2.VideoCapture(video_source)
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.mp_drawing = mp.solutions.drawing_utils

        # Define gestures with more precise landmark positions
        self.gestures = {
            "Thumbs Up": [4, 8, 12, 16, 20],  # Thumb extended, others folded
            "Peace": [8, 12],  # Index and middle fingers extended
        }

        self.last_gesture = None

    def process_video(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            self.analyze_frame(frame)

            cv2.imshow('Video Analytics', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

    def analyze_frame(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame to detect hand landmarks.
        results = self.hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw hand landmarks on the frame.
                self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

                # Analyze the landmarks to recognize gestures.
                gesture_name = self.recognize_gesture(hand_landmarks)
                if gesture_name and gesture_name != self.last_gesture:
                    self.last_gesture = gesture_name
                    print(f"Gesture Detected: {gesture_name}")

    def recognize_gesture(self, hand_landmarks):
        # Extract landmark positions
        landmarks = [(lm.x, lm.y, lm.z) for lm in hand_landmarks.landmark]
        
        # Define landmarks for gesture recognition
        thumb_tip = landmarks[4]
        index_finger_tip = landmarks[8]
        middle_finger_tip = landmarks[12]
        ring_finger_tip = landmarks[16]
        pinky_tip = landmarks[20]

        if self.is_thumbs_up(thumb_tip, index_finger_tip, middle_finger_tip, ring_finger_tip, pinky_tip):
            return "Thumbs Up"

        if self.is_peace(index_finger_tip, middle_finger_tip, thumb_tip):
            alert_system = AlertSystem(recipient_phone="+916307257097")
            alert_system.send_alert("This is a test alert message.")
            return "Peace"

        return None

    def is_thumbs_up(self, thumb_tip, index_finger_tip, middle_finger_tip, ring_finger_tip, pinky_tip):
        return (
            thumb_tip[1] < index_finger_tip[1] and
            index_finger_tip[1] > middle_finger_tip[1] and
            middle_finger_tip[1] > ring_finger_tip[1] and
            ring_finger_tip[1] > pinky_tip[1]
        )

    def is_peace(self, index_finger_tip, middle_finger_tip, thumb_tip):
        return (
            index_finger_tip[1] < thumb_tip[1] and
            middle_finger_tip[1] < thumb_tip[1]
        )
