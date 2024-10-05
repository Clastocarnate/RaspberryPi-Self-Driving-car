from ArucoFollower import ArucoFollower
import numpy as np

# Motor and enable pin configuration
motor_pins = [{'forward': 21, 'backward': 20}, {'forward': 6, 'backward': 5}]
enable_pins = [12, 13]

# Camera calibration parameters
cam_mat = np.array([[1003.1076720832533, 0.0, 325.5842274588375],
                    [0.0, 1004.8079121262164, 246.67564927792367],
                    [0.0, 0.0, 1.0]])
dist_coef = np.array([0.1886629014531147, 0.0421057002310688, 0.011153911980654914, 0.012946956962024124, 0.0])

# Initialize the ArucoFollower object
aruco_follower = ArucoFollower(motor_pins, enable_pins, cam_mat, dist_coef)

# Path planning logic based on detected ArUco markers
while True:
    marker_id = aruco_follower.follow_aruco()

    if marker_id is not None:
        # Determine whether to turn left or right based on the marker ID
        if marker_id == 2:
            print("Detected marker ID 1, turning left.")
            aruco_follower.turn_left()
        elif marker_id == 4:
            print("Detected marker ID 2, turning right.")
            aruco_follower.turn_right()

    # Add additional path planning logic as necessary
