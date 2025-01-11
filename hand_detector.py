import cv2
import mediapipe as mp
import pyautogui
import math
from collections import deque
import time

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
        
        # Gesture tracking
        self.position_history = deque(maxlen=10)
        self.last_gesture_time = 0
        self.gesture_cooldown = 1.0
        
        # Movement thresholds
        self.swipe_threshold = 100
        self.vertical_threshold = 100  # Minimum vertical movement for swipe detection
        self.horizontal_tolerance = 50  # Maximum horizontal movement during vertical swipe

    def detect_swipe_gesture(self, hand_landmarks):
        """Detect both horizontal and vertical swipe gestures."""
        palm_center = hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]
        current_x = palm_center.x * self.screen_width
        current_y = palm_center.y * self.screen_height
        
        self.position_history.append((current_x, current_y))
        
        if len(self.position_history) < 10:
            return None
            
        # Calculate movement
        start_x, start_y = self.position_history[0]
        end_x, end_y = self.position_history[-1]
        dx = end_x - start_x
        dy = end_y - start_y
        
        current_time = time.time()
        if current_time - self.last_gesture_time < self.gesture_cooldown:
            return None
            
        # Check for horizontal swipe
        if abs(dx) > self.swipe_threshold and abs(dy) < self.horizontal_tolerance:
            self.last_gesture_time = current_time
            self.position_history.clear()
            
            if dx < 0:
                return "left_swipe"
            elif dx > 0:
                return "right_swipe"
        
        # Check for vertical swipe (up)
        elif abs(dy) > self.vertical_threshold and abs(dx) < self.horizontal_tolerance:
            self.last_gesture_time = current_time
            self.position_history.clear()
            
            if dy < 0:  # Moving upward
                return "up_swipe"
                
        return None

    def detect(self, frame):
        frame = cv2.flip(frame, 1)
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image)
        
        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            
            # Detect gestures
            gesture = self.detect_swipe_gesture(hand_landmarks)
            if gesture == "left_swipe":
                pyautogui.hotkey('alt', 'tab')
                pyautogui.sleep(0.1)
            elif gesture == "right_swipe":
                pyautogui.hotkey('alt', 'shift', 'tab')
                pyautogui.sleep(0.1)
            elif gesture == "up_swipe":
                pyautogui.hotkey('winleft', 'tab')  # Windows Task View shortcut
                pyautogui.sleep(0.1)
            
            # Process regular cursor movement and clicks
            index_pos = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
            thumb_pos = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]

            index_x, index_y = int(index_pos.x * self.screen_width), int(index_pos.y * self.screen_height)
            thumb_x, thumb_y = int(thumb_pos.x * self.screen_width), int(thumb_pos.y * self.screen_height)

            distance = math.sqrt((index_x - thumb_x)**2 + (index_y - thumb_y)**2)

            if distance < 70:
                pyautogui.click()
                pyautogui.sleep(0.1)
            else:
                if self.prev_index_x is None:
                    self.prev_index_x, self.prev_index_y = index_x, index_y
                else:
                    factor = 0.5
                    new_x = (1 - factor) * self.prev_index_x + factor * index_x
                    new_y = (1 - factor) * self.prev_index_y + factor * index_y
                    pyautogui.moveTo(new_x, new_y)
                    self.prev_index_x, self.prev_index_y = new_x, new_y

            self.draw_lines(frame, hand_landmarks)
            
            # Draw gesture visualization
            if len(self.position_history) > 1:
                points = [(int(x), int(y)) for x, y in self.position_history]
                for i in range(len(points) - 1):
                    cv2.line(frame, points[i], points[i + 1], (0, 255, 0), 2)

        return frame

    def draw_lines(self, frame, hand_landmarks):
        image_height, image_width, _ = frame.shape
        color = (41, 98, 255, 1)

        for i in range(len(hand_landmarks.landmark) - 1):
            start = (
                int(hand_landmarks.landmark[i].x * image_width),
                int(hand_landmarks.landmark[i].y * image_height)
            )
            end = (
                int(hand_landmarks.landmark[i+1].x * image_width),
                int(hand_landmarks.landmark[i+1].y * image_height)
            )

            cv2.line(frame, start, end, color, thickness=3)