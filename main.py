import cv2
import numpy as np
from datetime import datetime
from hand_detector import HandDetector

def draw_scifi_overlay(frame):
    height, width = frame.shape[:2]
    overlay = frame.copy()
    
    # Draw hexagonal corners with blue color
    corners = [
        (0, 0), (width-100, 0),
        (0, height-100), (width-100, height-100)
    ]
    
    for x, y in corners:
        pts = np.array([
            [x, y+30], [x+15, y+50],
            [x+45, y+50], [x+60, y+30],
            [x+45, y+10], [x+15, y+10]
        ], np.int32)
        cv2.fillPoly(overlay, [pts], (255, 140, 0))  # Blue fill
        cv2.polylines(overlay, [pts], True, (255, 140, 0), 2)  # Blue outline
    
    # Draw scanning lines in blue
    t = datetime.now().timestamp()
    scan_y = int(height * (0.5 + 0.5 * np.sin(t)))
    cv2.line(overlay, (0, scan_y), (width, scan_y), (255, 140, 0), 1)
    
    # Draw grid pattern in blue
    grid_spacing = 50
    alpha = 0.3
    
    for x in range(0, width, grid_spacing):
        cv2.line(overlay, (x, 0), (x, height), (255, 140, 0), 1)
    for y in range(0, height, grid_spacing):
        cv2.line(overlay, (0, y), (width, y), (255, 140, 0), 1)
    
    # Blend the overlay
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
    return frame

def draw_scifi_hud(frame, fps):
    height, width = frame.shape[:2]
    
    # Draw top HUD with dark blue background
    cv2.rectangle(frame, (0, 0), (width, 60), (50, 0, 0), -1)
    cv2.line(frame, (0, 60), (width, 60), (255, 140, 0), 2)
    
    # Draw system status in blue
    current_time = datetime.now().strftime("%H:%M:%S")
    cv2.putText(frame, f"SYSTEM ACTIVE | TIME: {current_time}", 
                (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, 
                (255, 140, 0), 2)
    
    # Draw FPS counter with dynamic blue shades
    fps_color = (255, 140, 0) if fps > 25 else (200, 100, 0) if fps > 15 else (150, 60, 0)
    cv2.putText(frame, f"FPS: {int(fps)}", 
                (width - 150, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, 
                fps_color, 2)
    
    return frame

def create_scifi_instructions():
    instructions = np.zeros((300, 500, 3), dtype=np.uint8)  # Wider instructions window
    
    # Draw border in blue
    cv2.rectangle(instructions, (0, 0), (499, 299), (255, 140, 0), 2)
    
    # Draw header with dark blue background
    cv2.rectangle(instructions, (0, 0), (500, 50), (50, 0, 0), -1)
    cv2.line(instructions, (0, 50), (500, 50), (255, 140, 0), 2)
    cv2.putText(instructions, "GESTURE CONTROL SYSTEM", (20, 35), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 140, 0), 2)
    
    # Draw instructions with blue styling
    instructions_text = [
        ("CURSOR CONTROL:", 80, 0.6, 2),
        ("- Index finger movement", 120, 0.5, 1),
        ("ACTIONS:", 160, 0.6, 2),
        ("- Pinch: Execute click", 200, 0.5, 1),
        ("- Swipe left/right: Switch applications", 240, 0.5, 1),
        ("Press 'Q' to terminate system", 280, 0.5, 1)
    ]
    
    for text, y, size, thickness in instructions_text:
        cv2.putText(instructions, text, (20, y), 
                    cv2.FONT_HERSHEY_SIMPLEX, size, (255, 140, 0), thickness)
    
    return instructions

def main():
    cap = cv2.VideoCapture(0)
    # Set wider resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # Doubled width
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # 16:9 aspect ratio
    
    detector = HandDetector()
    
    # Create windows with specific sizes
    cv2.namedWindow('Neural Interface', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Neural Interface', 1280, 720)  # Set initial size
    
    cv2.namedWindow('System Instructions', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('System Instructions', 500, 300)  # Wider instructions window
    
    # Make windows topmost
    cv2.setWindowProperty('Neural Interface', cv2.WND_PROP_TOPMOST, 1)
    cv2.setWindowProperty('System Instructions', cv2.WND_PROP_TOPMOST, 1)
    
    instructions = create_scifi_instructions()
    
    print("Neural Interface Activated. Press 'Q' to terminate.")
    
    # FPS calculation
    fps = 0
    frame_time = datetime.now()
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Neural Interface disconnected")
                break
            
            # Calculate FPS
            current_time = datetime.now()
            dt = (current_time - frame_time).total_seconds()
            fps = 1.0 / dt if dt > 0 else 0
            frame_time = current_time
            
            # Process frame
            processed_frame = detector.detect(frame)
            
            # Add sci-fi overlays
            processed_frame = draw_scifi_overlay(processed_frame)
            processed_frame = draw_scifi_hud(processed_frame, fps)
            
            # Show frames
            cv2.imshow('Neural Interface', processed_frame)
            cv2.imshow('System Instructions', instructions)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("System shutdown initiated...")
                break
                
    except Exception as e:
        print(f"System Error: {str(e)}")
        
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("Neural Interface deactivated")

if __name__ == "__main__":
    main()