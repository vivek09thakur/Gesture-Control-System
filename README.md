<h1 align="center">Science Week Project🔬🧪 </h1>

<h3 align="center">Gesture Sense Interface - Control System </h3>
<p> 




<h3 align="center">Project Objectives ~ </h3>
<p>In this project we have tried our best to create an 
interactive control system throuĀh which we can 
replace the use oÿ mouse and touch screen. Still 
currently this have many limitations but it’ll 
be improved in ÿurther days.</p>




<h3>Required Libraries : </h3>
  <h4 style="color:#006cff">
     <li>OpenCV  - pip install opencv-python</li>
     <li>Mediapipe - pip install mediapipe</li>
     <li>PyAutoGUI - pip install pyautogui </li>
  </h4>



<br/>
<h3>How it works</h3>
<p>
   The code uses OpenCV, MediaPipe, and PyAutoGUI libraries to create a virtual mouse. The program detects hand landmarks using MediaPipe Hands, and then maps the position of the index finger and thumb to the screen coordinates using PyAutoGUI.The index finger is used as a cursor, while the thumb is used as a clicker.
</p>





<br/>
<h3>Code Explanation ~ </h3> 

<li>Step 1 : The program first imports the required libraries: cv2 (OpenCV), mediapipe, and pyautogui.</li>

<li>Step 2 : It then sets up the camera capture and initializes the MediaPipe Hands object and drawing utilities.</li>

<li>Step 3 : The program then gets the screen dimensions using PyAutoGUI.</li>

<li>Step 4 : In the main loop, the program reads the video stream from the camera and flips it horizontally.</li>

<li>Step 5 : The program then converts the BGR image to RGB and passes it to the MediaPipe Hands object for hand landmark detection.</li>

<li>Step 6 : If hands are detected, the program loops through each hand and draws the landmarks on the frame.
</li>

<li>Step 7 : The program then extracts the landmark positions and maps the position of the index finger and thumb to the screen coordinates.</li>

<br/><br/> Finally, the program checks the distance between the index finger and thumb, and performs a click or moves the cursor accordingly.
