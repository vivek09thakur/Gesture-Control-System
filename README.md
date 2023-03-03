<h2>Science Week Project - Gesture Control System </h2>
   <img src="https://i.ibb.co/tDkDQCC/Team-Amazing1-01.jpg" alt="Team-Amazing1-01" border="0">
<p>This code implements a virtual mouse that tracks hand gestures using Mediapipe and OpenCV libraries, which allows the user to perform clicks and move the mouse pointer using hand movements.</p>

<br/>
<h3>Required Libraries : </h3>
  <h4 style="color:#006cff">
     <li>OpenCV  - pip install opencv-python</li>
     <li>Mediapipe - pip install mediapipe</li>
     <li>PyAutoGUI - pip install pyautogui </li>
  </h4>

<br/>
<h3>How it works</h3>
<p>
   The code uses OpenCV, MediaPipe, and PyAutoGUI libraries to create a virtual mouse.
   The program detects hand landmarks using MediaPipe Hands, and then maps the position of the index finger and thumb to the screen coordinates using PyAutoGUI.
   The index finger is used as a cursor, while the thumb is used as a clicker.
</p>

<br/>
<h3>Work Flow of Program :</h3> 

<br/>Step 1 : The program first imports the required libraries: cv2 (OpenCV), mediapipe, and pyautogui.

<br/>Step 2 : It then sets up the camera capture and initializes the MediaPipe Hands object and drawing utilities.

<br/>Step 3 : The program then gets the screen dimensions using PyAutoGUI.

<br/>Step 4 : In the main loop, the program reads the video stream from the camera and flips it horizontally.

<br/>Step 5 : The program then converts the BGR image to RGB and passes it to the MediaPipe Hands object for hand landmark detection.

<br/>Step 6 : If hands are detected, the program loops through each hand and draws the landmarks on the frame.

<br/><br/>Step 7 : The program then extracts the landmark positions and maps the position of the index finger and thumb to the screen coordinates.

<br/><br/> Finally, the program checks the distance between the index finger and thumb, and performs a click or moves the cursor accordingly.
