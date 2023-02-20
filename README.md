9<img src="https://i.ibb.co/tDkDQCC/Team-Amazing1-01.jpg" alt="Team-Amazing1-01" border="0">

<h2>Gesture Control System</h2>
<p>This code implements a virtual mouse that tracks hand gestures using Mediapipe and OpenCV libraries, which allows the user to perform clicks and move the mouse pointer using hand movements.</p>

</br>
<h3>Required Libraries : </h3>
  <h4 style="color:blue">
     <li>OpenCV  - pip install opencv-python</li>
     <li>Mediapipe - pip install mediapipe</li>
     <li>PyAutoGUI - pip install pyautogui </li>
  </h4>

</br>
<h3>How it works</h3>
<p>
   The code uses OpenCV, MediaPipe, and PyAutoGUI libraries to create a virtual mouse.
   The program detects hand landmarks using MediaPipe Hands, and then maps the position of the index finger and thumb to the screen coordinates using PyAutoGUI.
   The index finger is used as a cursor, while the thumb is used as a clicker.
</p>

</br>
<h3>Work Flow of Program :</h3> 

<p>Step 1 : The program first imports the required libraries: cv2 (OpenCV), mediapipe, and pyautogui.</p>
</br>Step 2 : It then sets up the camera capture and initializes the MediaPipe Hands object and drawing utilities.</p>
<br>Step 3 : The program then gets the screen dimensions using PyAutoGUI.</p>
