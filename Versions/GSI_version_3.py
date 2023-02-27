import cv2 
import mediapipe as mp 
import pyautogui 

cap = cv2.VideoCapture(0) 
hand_detector = mp.solutions.hands.Hands() 
drawing_utils = mp.solutions.drawing_utils 
screen_width, screen_height = pyautogui.size() 
index_y = 0 
zoom_level = 1.0 

while True: 
    _, frame = cap.read() 
    frame = cv2.flip(frame, 1) 
    frame_height, frame_width, _ = frame.shape 
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
    output = hand_detector.process(rgb_frame) 
    hands = output.multi_hand_landmarks 
    
    if hands: 
        for hand in hands: 
            drawing_utils.draw_landmarks(frame, hand) 
            landmarks = hand.landmark 
            for id, landmark in enumerate(landmarks): 
                x = int(landmark.x*frame_width) 
                y = int(landmark.y*frame_height) 
                
                if id == 8: 
                    cv2.circle(img=frame, center=(x,y), radius=10, color=(0, 255, 255)) 
                    index_x = screen_width/frame_width*x 
                    index_y = screen_height/frame_height*y 
                    
                if id == 4: 
                    cv2.circle(img=frame, center=(x,y), radius=10, color=(0, 255, 255)) 
                    thumb_x = screen_width/frame_width*x 
                    thumb_y = screen_height/frame_height*y 
                    
                    if abs(index_y - thumb_y) < 20: 
                        pyautogui.click() 
                        pyautogui.sleep(1) 
                    elif abs(index_y - thumb_y) < 100: 
                        pyautogui.moveTo(index_x, index_y) 

                        # Check for zoom in and zoom out gestures
                        if landmarks[12].y < landmarks[11].y and landmarks[16].y < landmarks[15].y:
                            zoom_level += 0.05
                            pyautogui.hotkey('ctrl', '+')
                        elif landmarks[12].y > landmarks[11].y and landmarks[16].y > landmarks[15].y:
                            zoom_level -= 0.05
                            pyautogui.hotkey('ctrl', '-')
                        
                        # Check for scroll gesture
                        if landmarks[4].x < landmarks[3].x and landmarks[8].x < landmarks[7].x:
                            pyautogui.scroll(1)
                        elif landmarks[4].x > landmarks[3].x and landmarks[8].x > landmarks[7].x:
                            pyautogui.scroll(-1)
    
    # Set the zoom level
    pyautogui.hotkey('ctrl', '0')
    pyautogui.hotkey('ctrl', '-')
    for _ in range(int(zoom_level * 20)):
        pyautogui.hotkey('ctrl', '+')

    cv2.imshow('Virtual Mouse', frame) 
    cv2.waitKey(1)
