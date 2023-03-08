<h1 align="center">Science Week Project🔬🧪 </h1>

<h3 align="center">Gesture Sense Interface - Control System </h3>
<p> As a basic computer setup have essential components such as monitor, CPU , keyboard and mouse. In morden days many PCs and Laptops comes with Touch Screen displays which is quite good.But For now let's go a step further , What about if we can control our display without 
touching it? Seems awesome right?

<br/>We have just tried to make a system that can finger out coordinate of our fingure or say it just 
track position of our hand and then tracks the cursors location in the screen and matches it.

<br/>Through this we can create a virtual mouse with we can control system gesture without any 
physical contact. Let's know how it works and it's components.
</p>





<br/><br/>


<h3 align="center">Project Objectives ~ </h3>
<p>In this project we have tried our best to create an 
interactive control system throuĀh which we can 
replace the use oÿ mouse and touch screen. Still 
currently this have many limitations but it’ll 
be improved in ÿurther days.</p>



<br/><br/>

<h3 align="center">Libraries and Modules Used ~ </h3>

<p align="center">
   <a href="#">
     OpenCV-Python | Mediapipe | PyAutoGUI
   </a>
</p>





<br/><br/>
<h3>How it works?</h3>
<p>
   The code uses OpenCV, MediaPipe, and PyAutoGUI libraries to create a virtual mouse. The program detects hand landmarks using MediaPipe Hands, and then maps the position of the index finger and thumb to the screen coordinates using PyAutoGUI.The index finger is used as a cursor, while the thumb is used as a clicker.
</p>





<br/><br/>
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

