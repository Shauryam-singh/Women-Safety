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
            "SOS": [4, 8, 12, 16, 20],  # Specific gesture for SOS
            "Help": [4, 8, 12, 16],     # Open hand with thumb and index finger extended
            "Call for Help": [4, 8],    # Phone gesture
            "Stop": [4, 8, 12, 16, 20], # Open palm
            "No": [4, 8, 12, 16, 20],  # Shaking hand or specific gesture
            "Danger": [4, 8, 12, 16]    # Hand near throat or specific signal
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

                    # Trigger alert based on gesture
                    self.trigger_alert(gesture_name)

    def recognize_gesture(self, hand_landmarks):
        # Extract landmark positions
        landmarks = [(lm.x, lm.y, lm.z) for lm in hand_landmarks.landmark]
        
        # Define landmarks for gesture recognition
        thumb_tip = landmarks[4]
        index_finger_tip = landmarks[8]
        middle_finger_tip = landmarks[12]
        ring_finger_tip = landmarks[16]
        pinky_tip = landmarks[20]

        if self.is_sos(thumb_tip, index_finger_tip, middle_finger_tip, ring_finger_tip, pinky_tip):
            return "SOS"

        if self.is_help(thumb_tip, index_finger_tip, middle_finger_tip, ring_finger_tip):
            return "Help"

        if self.is_call_for_help(thumb_tip, index_finger_tip):
            return "Call for Help"

        if self.is_stop(thumb_tip, index_finger_tip, middle_finger_tip, ring_finger_tip, pinky_tip):
            return "Stop"

        if self.is_no(thumb_tip, index_finger_tip, middle_finger_tip, ring_finger_tip, pinky_tip):
            return "No"

        if self.is_danger(thumb_tip, index_finger_tip, middle_finger_tip, ring_finger_tip):
            return "Danger"

        return None

    def is_sos(self, thumb_tip, index_finger_tip, middle_finger_tip, ring_finger_tip, pinky_tip):
        # Check for SOS gesture
        return (
            thumb_tip[1] < index_finger_tip[1] and
            index_finger_tip[1] < middle_finger_tip[1] and
            middle_finger_tip[1] < ring_finger_tip[1] and
            ring_finger_tip[1] < pinky_tip[1]
        )

    def is_help(self, thumb_tip, index_finger_tip, middle_finger_tip, ring_finger_tip):
        # Check for Help gesture
        return (
            thumb_tip[1] < index_finger_tip[1] and
            index_finger_tip[1] < middle_finger_tip[1] and
            middle_finger_tip[1] < ring_finger_tip[1]
        )

    def is_call_for_help(self, thumb_tip, index_finger_tip):
        # Check for Call for Help gesture (holding phone)
        return (
            thumb_tip[1] < index_finger_tip[1]
        )

    def is_stop(self, thumb_tip, index_finger_tip, middle_finger_tip, ring_finger_tip, pinky_tip):
        # Check for Stop gesture (open palm)
        return (
            thumb_tip[1] < index_finger_tip[1] and
            index_finger_tip[1] < middle_finger_tip[1] and
            middle_finger_tip[1] < ring_finger_tip[1] and
            ring_finger_tip[1] < pinky_tip[1]
        )

    def is_no(self, thumb_tip, index_finger_tip, middle_finger_tip, ring_finger_tip, pinky_tip):
        # Check for No gesture
        return (
            thumb_tip[1] > index_finger_tip[1] and
            index_finger_tip[1] > middle_finger_tip[1] and
            middle_finger_tip[1] > ring_finger_tip[1] and
            ring_finger_tip[1] > pinky_tip[1]
        )

    def is_danger(self, thumb_tip, index_finger_tip, middle_finger_tip, ring_finger_tip):
        # Check for Danger gesture (hand near throat or other specific signal)
        return (
            thumb_tip[1] < index_finger_tip[1] and
            index_finger_tip[1] < middle_finger_tip[1] and
            middle_finger_tip[1] < ring_finger_tip[1]
        )

    def trigger_alert(self, gesture_name):
        alert_system = AlertSystem(recipient_phone="+916307257097")
        if gesture_name == "SOS":
            alert_system.send_alert("SOS gesture detected! Immediate help needed.")
        elif gesture_name == "Help":
            alert_system.send_alert("Help gesture detected! Immediate assistance needed.")
        elif gesture_name == "Call for Help":
            alert_system.send_alert("Call for Help gesture detected! Please call for help.")
        elif gesture_name == "Danger":
            alert_system.send_alert("Danger gesture detected! Potential threat.")
        else:
            alert_system.send_alert(f"{gesture_name} gesture detected.")
