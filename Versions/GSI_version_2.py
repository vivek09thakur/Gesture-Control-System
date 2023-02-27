import cv2
import mediapipe as mp
import pyautogui

# Adjustment for hands
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    max_num_hands=1
)

screen_width, screen_height = pyautogui.size()
prev_index_x, prev_index_y = None, None


def interpolate(current, target, factor):
    return (1 - factor) * current + factor * target

# Main loop
cap = cv2.VideoCapture(0)
while True:
    # Capture frame from webcam
    ret, frame = cap.read()
    if not ret:
        break
    
    # Flip image horizontally
    frame = cv2.flip(frame, 1)
    
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    if results.multi_hand_landmarks:
       
        hand_landmarks = results.multi_hand_landmarks[0]
        
        mp_drawing.draw_landmarks(
            frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
 
        index_pos = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
        thumb_pos = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
        
        index_x, index_y = int(index_pos.x * screen_width), int(index_pos.y * screen_height)
        thumb_x, thumb_y = int(thumb_pos.x * screen_width), int(thumb_pos.y * screen_height)
        
        # Handle click gesture
        if abs(index_y - thumb_y) < 20:
            pyautogui.click()
            pyautogui.sleep(0.1)
        else:
            if prev_index_x is None:
                prev_index_x, prev_index_y = index_x, index_y
            else:
                factor = 0.5 
                new_x = interpolate(prev_index_x, index_x, factor)
                new_y = interpolate(prev_index_y, index_y, factor)
                pyautogui.moveTo(new_x, new_y)
                prev_index_x, prev_index_y = new_x, new_y
        
    # Display frame
    cv2.imshow('Virtual Mouse', frame)
    
    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
cap.release()
cv2.destroyAllWindows()
hands.close()
