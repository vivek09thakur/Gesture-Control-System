### INSTALLING REQUIREMENTS

To install the requirements, run the following command:

```bash
    pip install opencv-python
    pip install pyautogui
    pip install mediapipe
```

### RUNNING THE PROGRAM

To run the program, run the following command:

```bash
    python test_run.py
```

### CODE EXPLANATION

- [x] **Step 1 : The program first imports the required libraries: cv2 (OpenCV), mediapipe, and pyautogui.**

```python
    import cv2
    import mediapipe as mp
    import pyautogui
```

- [x] **Step 2: It then sets up the camera capture and initializes the MediaPipe Hands object and drawing utilities.**

```python
     cap = cv2.VideoCapture(0) 
    hand_detector = mp.solutions.hands.Hands() 
    drawing_utils = mp.solutions.drawing_utils 
```

- [x] **Step 3: The program then gets the screen dimensions using PyAutoGUI.

```python 
    screen_width, screen_height = pyautogui.size() 
    index_y = 0
```

- [x] **Step 4 : In the main loop, the program reads the video stream from the camera and flips it horizontally.**

```python
    while True: 
        _, frame = cap.read() 
        frame = cv2.flip(frame, 1)
```

- [x] **Step 5 : The program then converts the BGR image to RGB and passes it to the MediaPipe Hands object for hand landmark detection.**

```python 
     frame_height, frame_width, _ = frame.shape 
     rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
     output = hand_detector.process(rgb_frame) 
     hands = output.multi_hand_landmarks
```

- [x] **Step 6 : If hands are detected, the program loops through each hand and draws the landmarks on the frame.**

```python
     if hands: 
         for hand in hands: 
             drawing_utils.draw_landmarks(frame, hand) 
             landmarks = hand.landmark 
```

- [x] **Step 7 : The program then extracts the landmark positions and maps the position of the index finger and thumb to the screen coordinates.**

```python 
              for id, landmark in enumerate(landmarks): 
                 x = int(landmark.x*frame_width) 
                 y = int(landmark.y*frame_height) 
                 if id == 8: 
                     cv2.circle(img=frame, center=(x,y), radius=10, color=(0, 255, 255)) 
                     index_x = screen_width/frame_width*x 
                     index_y = screen_height/frame_height*y
```

***Finally, the program checks the distance between the index finger and thumb, and performs a click or moves the cursor accordingly.***

```python                 
        if id == 8: 
                     cv2.circle(img=frame, center=(x,y), radius=10, color=(0, 255, 255)) 
                     index_x = screen_width/frame_width*x 
                     index_y = screen_height/frame_height*y 
  
                 if id == 4: 
                     cv2.circle(img=frame, center=(x,y), radius=10, color=(0, 255, 255)) 
                     thumb_x = screen_width/frame_width*x 
                     thumb_y = screen_height/frame_height*y 
                     print('outside', abs(index_y - thumb_y)) 
                     if abs(index_y - thumb_y) < 20: 
                         pyautogui.click() 
                         pyautogui.sleep(1) 
                     elif abs(index_y - thumb_y) < 100: 
                         pyautogui.moveTo(index_x, index_y) 
     cv2.imshow('Virtual Mouse', frame) 
     cv2.waitKey(1)
 ```
 The above code is just a basic code explanation of this project. To read the full code explanation. Maybe in future we will add more features to this project or improve it. If you have any suggestions or ideas regarding this project, feel free to contribute.