import cv2 as cv
from cv2 import aruco
import numpy as np
from gpiozero import Motor, OutputDevice
from time import sleep

# Motor Setup
motor1 = Motor(forward=21, backward=20)  # Motor 1: IN1 -> GPIO 20, IN2 -> GPIO 21
motor2 = Motor(forward=6, backward=5)    # Motor 2: IN3 -> GPIO 5, IN4 -> GPIO 6
en1 = OutputDevice(12)  # Enable pin for Motor 1 (GPIO 12)
en2 = OutputDevice(13)  # Enable pin for Motor 2 (GPIO 13)

# Turn on the enable pins
en1.on()
en2.on()

# Camera Calibration values (hardcoded for now)
cam_mat = np.array([[1003.1076720832533, 0.0, 325.5842274588375],
                    [0.0, 1004.8079121262164, 246.67564927792367],
                    [0.0, 0.0, 1.0]])

dist_coef = np.array([0.1886629014531147, 0.0421057002310688, 0.011153911980654914, 0.012946956962024124, 0.0])

MARKER_SIZE = 10  # cm

marker_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
param_markers = aruco.DetectorParameters_create()

cap = cv.VideoCapture(0)

screen_center_x = 640 // 2  # Assuming a 640x480 resolution
tolerance = 50  # Tolerance for alignment in pixels

def stop_motors():
    motor1.stop()
    motor2.stop()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    marker_corners, marker_IDs, reject = aruco.detectMarkers(
        gray_frame, marker_dict, parameters=param_markers
    )

    # Draw center of the screen
    cv.drawMarker(frame, (screen_center_x, 480 // 2), (0, 255, 0), cv.MARKER_CROSS, 20, 2)

    if marker_corners:
        rVec, tVec, _ = aruco.estimatePoseSingleMarkers(
            marker_corners, MARKER_SIZE, cam_mat, dist_coef
        )
        total_markers = range(0, marker_IDs.size)

        for ids, corners, i in zip(marker_IDs, marker_corners, total_markers):
            # Calculate marker center
            corners = corners.reshape(4, 2)
            marker_center = np.mean(corners, axis=0).astype(int)

            # Draw marker and a line between the center of the screen and the marker center
            cv.polylines(frame, [corners.astype(np.int32)], True, (0, 255, 255), 4, cv.LINE_AA)
            cv.line(frame, (screen_center_x, 480 // 2), tuple(marker_center), (255, 0, 0), 2)

            # Calculate the distance
            distance = np.sqrt(
                tVec[i][0][2] ** 2 + tVec[i][0][0] ** 2 + tVec[i][0][1] ** 2
            )

            # Check horizontal alignment with screen center
            if abs(marker_center[0] - screen_center_x) <= tolerance:
                # Marker is horizontally aligned within tolerance, check distance
                if distance > 10:  # Move forward if the distance is greater than 10 cm
                    print("Moving forward")
                    motor1.forward()
                    motor2.forward()
                else:
                    print("Stopping, distance <= 10 cm")
                    stop_motors()
            elif marker_center[0] < screen_center_x - tolerance:
                # Marker is to the left of the screen center, turn left
                print("Turning left")
                motor2.backward(0.3)
                motor1.forward(0.3)
            elif marker_center[0] > screen_center_x + tolerance:
                # Marker is to the right of the screen center, turn right
                print("Turning right")
                motor2.forward(0.3)
                motor1.backward(0.3)

            # Display ID and distance
            cv.putText(
                frame,
                f"id: {ids[0]} Dist: {round(distance, 2)} cm",
                (marker_center[0] + 20, marker_center[1]),
                cv.FONT_HERSHEY_PLAIN,
                1.3,
                (0, 0, 255),
                2,
                cv.LINE_AA,
            )
    else:
        # Stop motors if no ArUco marker is detected
        print("No marker detected, stopping motors.")
        stop_motors()

    cv.imshow("frame", frame)
    key = cv.waitKey(1)
    if key == ord("q"):
        break

cap.release()
cv.destroyAllWindows()

# Turn off the enable pins when done
en1.off()
en2.off()
