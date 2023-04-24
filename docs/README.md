<h1 align="center">Science Week Project 🛸🔭</h1>


<br/><h3>
  Gesture Sense Interface - Control System
</h3>

<p align="left"> As a basic computer setup have essential components such as monitor, CPU , keyboard and mouse. <img width="400px" height="auto" align="right" src="https://user-images.githubusercontent.com/37477845/102235423-aa6cb680-3f35-11eb-8ebd-5d823e211447.jpg" style="margin:25px"/>
<br/>In morden days many PCs and Laptops comes with Touch Screen displays which is quite good.But For now let's go a step further , What about if we can control our display without 
touching it? Seems awesome right?
<br/><br/>We have just tried to make a system that can fingure out coordinate of our finger or say it just track position of our hand and then tracks the cursors location in the screen and matches it.
<br/>Through this we can create a virtual mouse with we can control system gesture without any 
physical contact. Let's know how it works and it's components.
</p>





<br/><br/>


<h3>Project Objectives : </h3>
<p>In this project we have tried our best to create an interactive control system through which we can replace the use of mouse and touch screen. Still currently this have many limitations but it’ll be improved in further days.</p>

<br/><br/>

<h3 align="center">Libraries Used </h3>

  ```sh
     pip install opencv-python
     pip install mediapipe
     pip install pyautogui
 ```





<br/><br/>
<h3>How it works?</h3>
<p>
   The code uses OpenCV, MediaPipe, and PyAutoGUI libraries to create a virtual mouse. The program detects hand landmarks using MediaPipe Hands, and then maps the position of the index finger and thumb to the screen coordinates using PyAutoGUI.The index finger is used as a cursor, while the thumb is used as a clicker.
</p>





<br/><br/>
<h3>Code Explanation ~ </h3> 

<p>Step 1 : The program first imports the required libraries: cv2 (OpenCV), mediapipe, and pyautogui.</p>

```py
 import cv2 
 import mediapipe as mp 
 import pyautogui

 ```

<p>Step 2 : It then sets up the camera capture and initializes the MediaPipe Hands object and drawing utilities.</p>

```py
 cap = cv2.VideoCapture(0) 
 hand_detector = mp.solutions.hands.Hands() 
 drawing_utils = mp.solutions.drawing_utils 

 ```


<p>Step 3 : The program then gets the screen dimensions using PyAutoGUI.</p>

```py
 screen_width, screen_height = pyautogui.size() 
 index_y = 0


 ```


<p>Step 4 : In the main loop, the program reads the video stream from the camera and flips it horizontally.</p>

```py
 while True: 
     _, frame = cap.read() 
     frame = cv2.flip(frame, 1)

 ```


<p>Step 5 : The program then converts the BGR image to RGB and passes it to the MediaPipe Hands object for hand landmark detection.</p>


```py
     frame_height, frame_width, _ = frame.shape 
     rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
     output = hand_detector.process(rgb_frame) 
     hands = output.multi_hand_landmarks

 ```


<p>Step 6 : If hands are detected, the program loops through each hand and draws the landmarks on the frame.
</p>

```sh 
     if hands: 
         for hand in hands: 
             drawing_utils.draw_landmarks(frame, hand) 
             landmarks = hand.landmark 
 ```


<p>Step 7 : The program then extracts the landmark positions and maps the position of the index finger and thumb to the screen coordinates.</p>

```sh 
              for id, landmark in enumerate(landmarks): 
                 x = int(landmark.x*frame_width) 
                 y = int(landmark.y*frame_height) 
                 if id == 8: 
                     cv2.circle(img=frame, center=(x,y), radius=10, color=(0, 255, 255)) 
                     index_x = screen_width/frame_width*x 
                     index_y = screen_height/frame_height*y
 ```


<br/> Finally, the program checks the distance between the index finger and thumb, and performs a click or moves the cursor accordingly.


```py
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



