#include <iostream>
#include <Windows.h>
#include <opencv2/opencv.hpp>

using namespace cv;

int main()
{
    // Initialize video capture from default camera
    VideoCapture cap(0);
    if (!cap.isOpened()) {
        std::cout << "Error: Failed to open video capture device\n";
        return -1;
    }

    // Initialize screen dimensions and mouse position
    int screen_width = GetSystemMetrics(SM_CXSCREEN);
    int screen_height = GetSystemMetrics(SM_CYSCREEN);
    int prev_index_x = -1, prev_index_y = -1;

    // Main loop
    while (true) {
        // Read frame from video capture device
        Mat frame;
        cap.read(frame);
        if (frame.empty()) {
            std::cout << "Error: Failed to read frame\n";
            break;
        }

        // Flip frame horizontally
        flip(frame, frame, 1);

        // Convert frame to grayscale
        Mat gray;
        cvtColor(frame, gray, COLOR_BGR2GRAY);

        // Apply Gaussian blur to reduce noise
        GaussianBlur(gray, gray, Size(5, 5), 0);

        // Apply threshold to segment hand region
        Mat thresh;
        threshold(gray, thresh, 0, 255, THRESH_BINARY_INV | THRESH_OTSU);

        // Find contours of hand region
        std::vector<std::vector<Point>> contours;
        findContours(thresh, contours, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE);

        // Find largest contour (hand)
        int max_contour_idx = -1;
        double max_contour_area = 0;
        for (int i = 0; i < contours.size(); i++) {
            double area = contourArea(contours[i]);
            if (area > max_contour_area) {
                max_contour_area = area;
                max_contour_idx = i;
            }
        }

        // If hand is detected
        if (max_contour_idx != -1) {
            // Get center of hand contour
            Moments m = moments(contours[max_contour_idx], true);
            int cx = m.m10 / m.m00;
            int cy = m.m01 / m.m00;

            // Simulate left mouse button click if index finger and thumb are close
            if (norm(Point(cx, cy) - contours[max_contour_idx][0]) < 70) {
                mouse_event(MOUSEEVENTF_LEFTDOWN | MOUSEEVENTF_LEFTUP, cx * 65535 / screen_width, cy * 65535 / screen_height, 0, 0);
                Sleep(100);
            }
            // Otherwise, move mouse pointer based on index finger position
            else {
                if (prev_index_x == -1 && prev_index_y == -1) {
                    prev_index_x = cx;
                    prev_index_y = cy;
                }
                else {
                    double factor = 0.5;
                    int new_x = (1 - factor) * prev_index_x + factor * cx;
                    int new_y = (1 - factor) * prev_index_y + factor * cy;
                    SetCursorPos(new_x * 65535 / screen_width, new_y * 65535 / screen_height);
                    prev_index_x = new_x;
                    prev_index_y = new_y;
                }
            }
        }

        // Display frame
        imshow("Hand Gesture Recognition", frame);
        if (waitKey(10) == 27) break; // Press 'Esc' key to exit
    }

    // Release video capture and destroy window
    cap.release();
    destroyAllWindows();
    
    return 0;
}

