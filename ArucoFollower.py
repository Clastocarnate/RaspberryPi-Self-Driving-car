import cv2 as cv
from cv2 import aruco
import numpy as np
from gpiozero import Motor, OutputDevice
from time import sleep

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

    def process_frame(self, frame):
        gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        marker_corners, marker_IDs, _ = aruco.detectMarkers(gray_frame, self.marker_dict, parameters=self.param_markers)

        if marker_corners:
            rVec, tVec, _ = aruco.estimatePoseSingleMarkers(marker_corners, self.marker_size, self.cam_mat, self.dist_coef)
            for ids, corners, i in zip(marker_IDs, marker_corners, range(marker_IDs.size)):
                marker_center = np.mean(corners.reshape(4, 2), axis=0).astype(int)
                distance = np.sqrt(tVec[i][0][2] ** 2 + tVec[i][0][0] ** 2 + tVec[i][0][1] ** 2)

                if abs(marker_center[0] - self.screen_center_x) <= self.tolerance and distance > 30:
                    print(f"Moving forward. Distance: {round(distance, 2)} cm")
                    self.move_forward()
                elif distance <= 30:
                    print("Stopping at marker, distance <= 30 cm.")
                    self.stop_motors()
                    return ids[0]  # Return ID of the detected marker
                elif marker_center[0] < self.screen_center_x - self.tolerance:
                    print("Turning left.")
                    self.turn_left()
                elif marker_center[0] > self.screen_center_x + self.tolerance:
                    print("Turning right.")
                    self.turn_right()
        else:
            print("No marker detected, stopping motors.")
            self.stop_motors()
        return None

    def follow_aruco(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            marker_id = self.process_frame(frame)
            if marker_id is not None:
                return marker_id  # Return the detected marker's ID for path planning

            cv.imshow("Frame", frame)
            key = cv.waitKey(1)
            if key == ord('q'):
                break

        self.cap.release()
        cv.destroyAllWindows()
        self.en1.off()
        self.en2.off()
