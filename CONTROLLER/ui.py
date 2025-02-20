import cv2
import numpy as np
import time

class SciFiUI:
    def __init__(self):
        self.grid_color = (255, 140, 0)  # Deep Blue
        self.grid_spacing = 30
        self.animation_phase = 0
        self.last_time = time.time()
        self.accent_color = (255, 165, 0)  # Secondary blue
        self.glow_color = (255, 0, 0)     # Bright blue for glow effects

    def draw_grid(self, frame):
        h, w = frame.shape[:2]
        
        # Create animated grid effect with blue tones
        self.animation_phase += 0.05
        offset = int(self.animation_phase % self.grid_spacing)
        
        # Draw vertical lines with blue gradient
        for x in range(offset, w, self.grid_spacing):
            alpha = np.interp(x, [0, w], [0.2, 0.4])
            color = tuple(int(c * alpha) for c in self.grid_color)
            cv2.line(frame, (x, 0), (x, h), color, 1)
    
        # Draw horizontal lines with blue gradient
        for y in range(offset, h, self.grid_spacing):
            alpha = np.interp(y, [0, h], [0.2, 0.4])
            color = tuple(int(c * alpha) for c in self.grid_color)
            cv2.line(frame, (0, y), (w, y), color, 1)

    def draw_hand_effects(self, frame, hand_landmarks):
        if not hand_landmarks:
            return
        
        h, w = frame.shape[:2]
        landmarks = hand_landmarks.landmark
        
        # Define hand connections for a simple pattern
        connections = [
            # Palm base and fingers
            (0, 1), (1, 2), (2, 3), (3, 4),    # Thumb
            (0, 5), (5, 6), (6, 7), (7, 8),    # Index
            (0, 9), (9, 10), (10, 11), (11, 12),    # Middle
            (0, 13), (13, 14), (14, 15), (15, 16),  # Ring
            (0, 17), (17, 18), (18, 19), (19, 20),  # Pinky
        ]
        
        # Draw hand skeleton with single color
        for start_idx, end_idx in connections:
            pt1 = (int(landmarks[start_idx].x * w), int(landmarks[start_idx].y * h))
            pt2 = (int(landmarks[end_idx].x * w), int(landmarks[end_idx].y * h))
            cv2.line(frame, pt1, pt2, (0, 255, 255), 2)  # Yellow lines

    def draw_info_panel(self, frame, info_dict):
        h, w = frame.shape[:2]
        panel_w = 180
        panel_h = 100
        panel_x = 10
        panel_y = 10
        
        # Simple transparent background
        cv2.rectangle(frame, (panel_x, panel_y),
                     (panel_x + panel_w, panel_y + panel_h),
                     (0, 0, 0), -1)
        
        # Draw info text
        y_offset = panel_y + 25
        for key, value in info_dict.items():
            text = f"{key}: {value}"
            cv2.putText(frame, text, (panel_x + 10, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            y_offset += 25

    def draw_grid(self, frame):
        h, w = frame.shape[:2]
        spacing = 50
        
        # Simple static grid
        for x in range(0, w, spacing):
            cv2.line(frame, (x, 0), (x, h), (0, 50, 50), 1)
        for y in range(0, h, spacing):
            cv2.line(frame, (0, y), (w, y), (0, 50, 50), 1)

    def apply_effects(self, frame, hand_landmarks=None, info_dict=None):
        # Apply base grid
        self.draw_grid(frame)
        
        # Apply hand effects if landmarks are present
        if hand_landmarks:
            self.draw_hand_effects(frame, hand_landmarks)
        
        # Draw info panel if info is provided
        if info_dict:
            self.draw_info_panel(frame, info_dict)
        
        return frame