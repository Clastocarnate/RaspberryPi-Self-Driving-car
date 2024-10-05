import cv2 as cv
from cv2 import aruco
import numpy as np
from gpiozero import Motor, OutputDevice

class ArucoFollower:
    def __init__(self, motor_pins, enable_pins, cam_mat, dist_coef, marker_size=10, tolerance=50, screen_res=(640, 480)):
        # Motor Setup
        self.motor1 = Motor(forward=motor_pins[0]['forward'], backward=motor_pins[0]['backward'])
        self.motor2 = Motor(forward=motor_pins[1]['forward'], backward=motor_pins[1]['backward'])
        self.en1 = OutputDevice(enable_pins[0])
        self.en2 = OutputDevice(enable_pins[1])

        # Camera calibration values
        self.cam_mat = cam_mat
        self.dist_coef = dist_coef
        self.marker_size = marker_size  # Marker size in cm
        self.tolerance = tolerance  # Pixel tolerance for alignment
        self.screen_center_x = screen_res[0] // 2  # Half of screen width
        self.screen_center_y = screen_res[1] // 2  # Half of screen height
        self.cap = cv.VideoCapture(0)  # Camera setup
        
        self.marker_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
        self.param_markers = aruco.DetectorParameters_create()

        # Turn on motor enable pins
        self.en1.on()
        self.en2.on()

    def stop_motors(self):
        self.motor1.stop()
        self.motor2.stop()

    def move_forward(self):
        self.motor1.forward()
        self.motor2.forward()

    def turn_left(self, speed=0.3):
        self.motor2.backward(speed)
        self.motor1.forward(speed)

    def turn_right(self, speed=0.3):
        self.motor1.backward(speed)
        self.motor2.forward(speed)

    def process_frame(self):
        """
        Process a single frame from the camera feed, return marker ID and whether it's within 30 cm,
        and display the webcam feed with marker detection and distance.
        """
        ret, frame = self.cap.read()
        if not ret:
            return None, False

        gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        marker_corners, marker_IDs, _ = aruco.detectMarkers(
            gray_frame, self.marker_dict, parameters=self.param_markers)

        detected_marker_id = None  # Initialize to None

        if marker_corners:
            rVec, tVec, _ = aruco.estimatePoseSingleMarkers(
                marker_corners, self.marker_size, self.cam_mat, self.dist_coef)
            for id_array, corners, i in zip(marker_IDs, marker_corners, range(len(marker_IDs))):
                marker_id = int(id_array[0])  # Ensure marker_id is an integer
                detected_marker_id = marker_id  # Save the detected marker ID
                marker_center = np.mean(corners.reshape(4, 2), axis=0).astype(int)
                distance = np.linalg.norm(tVec[i][0])  # Use numpy's norm function

                # Draw the marker and display ID and distance on the frame
                cv.polylines(frame, [corners.astype(int)], True, (0, 255, 0), 2)
                cv.putText(frame, f"ID: {marker_id} Dist: {round(distance, 2)}cm", 
                           (marker_center[0], marker_center[1]), 
                           cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                # Check horizontal alignment and distance to the marker
                if abs(marker_center[0] - self.screen_center_x) <= self.tolerance:
                    if distance <= 30:
                        print(f"Within 30 cm of marker ID: {marker_id}")
                        self.stop_motors()  # Stop moving forward
                        # Show frame with marker detection and distance
                        cv.imshow('Aruco Detection', frame)
                        return marker_id, True  # Return ID and flag that it's within 30 cm
                    else:
                        print(f"Moving forward. Distance: {round(distance, 2)} cm")
                        self.move_forward()
                elif marker_center[0] < self.screen_center_x - self.tolerance:
                    print("Turning left.")
                    self.turn_left()
                elif marker_center[0] > self.screen_center_x + self.tolerance:
                    print("Turning right.")
                    self.turn_right()

        else:
            print("No marker detected, stopping motors.")
            self.stop_motors()

        # Show frame with marker detection and distance
        cv.imshow('Aruco Detection', frame)

        key = cv.waitKey(1)
        if key == ord('q'):  # Press 'q' to quit
            self.release_resources()

        # Return the detected marker ID even if it's not aligned or within 30 cm
        return detected_marker_id, False

    def release_resources(self):
        """
        Release camera and motor resources when done.
        """
        self.cap.release()
        self.en1.off()
        self.en2.off()
        cv.destroyAllWindows()

