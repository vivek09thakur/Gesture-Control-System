from GSI.GSI import GestureInterfaceController
import cv2

controller = GestureInterfaceController()

if __name__=='__main__':
    
    controller.initialize()
    while True:
        ret, frame = controller.cap.read()
        if not ret:
            break

        controller.frame_counter += 1
        if controller.frame_counter % controller.frame_skip != 0:
            continue

        frame = controller.detector.detect(frame)

        cv2.imshow('Gesture Sense Interface Control System', frame)
        if cv2.waitKey(controller.delay) & 0xFF == ord('q'):
            break
    
    controller.cleanup()