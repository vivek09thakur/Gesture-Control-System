import cv2
import mediapipe as mp
import pyautogui
import math

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

    def detect(self, frame):

        frame = cv2.flip(frame, 1)
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image)
        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
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

        return frame

    def draw_lines(self, 
                   frame, 
                   hand_landmarks):
        
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


class GestureInterfaceController:
    def __init__(self, webcam_id=0, frame_width=640, frame_height=480, target_fps=30):
        self.webcam_id = webcam_id
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.target_fps = target_fps
        self.delay = int(1000 / target_fps)
        self.frame_counter = 0
        self.frame_skip = 3  # Process every 3rd frame
        self.cap = None
        self.detector = None

    def initialize(self):
        self.cap = cv2.VideoCapture(self.webcam_id)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_height)
        self.detector = HandDetector()

    def run(self):
        self.initialize()
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            self.frame_counter += 1
            if self.frame_counter % self.frame_skip != 0:
                continue

            frame = self.detector.detect(frame)

            cv2.imshow('Gesture Sense Interface Control System', frame)
            if cv2.waitKey(self.delay) & 0xFF == ord('q'):
                break

        self.cleanup()

    def cleanup(self):
        if self.cap is not None:
            self.cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    controller = GestureInterfaceController()
    controller.run()
