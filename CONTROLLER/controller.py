import cv2
import mediapipe as mp
import pyautogui
import math
from screen_brightness_control import set_brightness
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np
import win32con

class HandDetector:
    def __init__(self, 
                 max_hands=1, 
                 detection_confidence=0.3, 
                 tracking_confidence=0.5):
        
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=max_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )
        self.screen_width, self.screen_height = pyautogui.size()
        self.prev_index_x, self.prev_index_y = None, None
        
        # Initialize audio controller
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume_controller = cast(interface, POINTER(IAudioEndpointVolume))
        self.current_volume = self.volume_controller.GetMasterVolumeLevelScalar()
        
        # Gesture states
        self.prev_gesture = None
        self.gesture_cooldown = 0
        self.gesture_threshold = 10
        
    def get_fingers_up(self, hand_landmarks):
        fingers = []
        # Thumb
        if hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP].x < \
           hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_IP].x:
            fingers.append(1)
        else:
            fingers.append(0)
            
        # Other fingers
        tips = [8, 12, 16, 20]  # Index, Middle, Ring, Pinky
        for tip in tips:
            if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers

    def detect(self, frame):
        frame = cv2.flip(frame, 1)
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image)
        
        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            fingers = self.get_fingers_up(hand_landmarks)
            
            # Get key landmarks
            index_pos = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
            thumb_pos = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
            middle_pos = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            ring_pos = hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_TIP]
            
            index_x, index_y = int(index_pos.x * self.screen_width), int(index_pos.y * self.screen_height)
            thumb_x, thumb_y = int(thumb_pos.x * self.screen_width), int(thumb_pos.y * self.screen_height)
            
            # Basic mouse control
            if sum(fingers) == 1 and fingers[1] == 1:  # Only index finger up
                if self.prev_index_x is None:
                    self.prev_index_x, self.prev_index_y = index_x, index_y
                else:
                    factor = 0.5
                    new_x = (1 - factor) * self.prev_index_x + factor * index_x
                    new_y = (1 - factor) * self.prev_index_y + factor * index_y
                    pyautogui.moveTo(new_x, new_y)
                    self.prev_index_x, self.prev_index_y = new_x, new_y
            
            # Click gesture
            thumb_index_distance = math.sqrt((index_x - thumb_x)**2 + (index_y - thumb_y)**2)
            if thumb_index_distance < 70 and self.gesture_cooldown == 0:
                pyautogui.click()
                self.gesture_cooldown = self.gesture_threshold
            
            # Volume Up - Index, Middle, Ring fingers up
            if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and sum(fingers) == 3:
                self.current_volume = min(1.0, self.current_volume + 0.02)
                self.volume_controller.SetMasterVolumeLevelScalar(self.current_volume, None)
                
            # Volume Down - Index and Ring fingers up
            if fingers[1] == 1 and fingers[3] == 1 and sum(fingers) == 2:
                self.current_volume = max(0.0, self.current_volume - 0.02)
                self.volume_controller.SetMasterVolumeLevelScalar(self.current_volume, None)
            
            # Brightness control (spread gesture with horizontal movement)
            if sum(fingers) == 5:  # All fingers up
                x_pos = index_pos.x
                brightness = int(np.interp(x_pos, [0.2, 0.8], [0, 100]))
                set_brightness(brightness)
            
            # Windows search (peace sign gesture)
            if fingers[1] == 1 and fingers[2] == 1 and sum(fingers) == 2 and self.gesture_cooldown == 0:
                pyautogui.hotkey('win', 's')
                self.gesture_cooldown = self.gesture_threshold * 2
            
            self.draw_lines(frame, hand_landmarks)
            
            # Update gesture cooldown
            if self.gesture_cooldown > 0:
                self.gesture_cooldown -= 1
        
        return frame

    def draw_lines(self, frame, hand_landmarks):
        image_height, image_width, _ = frame.shape
        color = (41, 98, 255)
        
        # Draw hand landmarks
        for i in range(len(hand_landmarks.landmark) - 1):
            start = (
                int(hand_landmarks.landmark[i].x * image_width),
                int(hand_landmarks.landmark[i].y * image_height)
            )
            end = (
                int(hand_landmarks.landmark[i+1].x * image_width),
                int(hand_landmarks.landmark[i+1].y * image_height)
            )
            cv2.line(frame, start, end, color, thickness=2)
        
        # Draw gesture labels
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, "Volume Up: Index + Middle + Ring", (10, 30), font, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, "Volume Down: Index + Ring", (10, 60), font, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, "Brightness: All fingers", (10, 90), font, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, "Search: Peace sign", (10, 120), font, 0.7, (255, 255, 255), 2)

class GestureInterfaceController:
    def __init__(self, webcam_id=0, frame_width=640, frame_height=480, target_fps=30):
        self.webcam_id = webcam_id
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.target_fps = target_fps
        self.delay = int(1000 / target_fps)
        self.frame_counter = 0
        self.frame_skip = 2
        self.cap = None
        self.detector = None

    def initialize(self):
        self.cap = cv2.VideoCapture(self.webcam_id)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_height)
        self.detector = HandDetector()

    def run(self):
        self.initialize()
        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    break

                self.frame_counter += 1
                if self.frame_counter % self.frame_skip == 0:
                    frame = self.detector.detect(frame)
                    cv2.imshow('Gesture Interface', frame)

                if cv2.waitKey(self.delay) & 0xFF == 27:  # ESC to exit
                    break
        finally:
            self.cleanup()

    def cleanup(self):
        if self.cap is not None:
            self.cap.release()
        cv2.destroyAllWindows()

# Usage
if __name__ == "__main__":
    controller = GestureInterfaceController()
    controller.run()