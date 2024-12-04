from ArucoFollower import ArucoFollower  # Import the ArucoFollower class
import numpy as np

def path_planning(aruco_follower):
    # Step 1: Move to Id 2
    print("Step 1: Moving to ID 2.")
    while True:
        print("Finding Aruco 2")
        marker_id, within_30cm = aruco_follower.process_frame()
        print(f"Debug - Marker ID: {marker_id}, Within 30 cm: {within_30cm}")
        if marker_id == 2 and within_30cm:
            print("Reached ID 2 within 30 cm.")
            aruco_follower.stop_motors()  # Ensure motors stop after reaching the target
            break  # Move to the next step

    # Step 2: Turn left until ID 4 is seen
    print("Step 2: Turning left to find ID 4.")
    while True:
        print("Finding Aruco 4")
        aruco_follower.turn_left()  # Start turning left to find ID 4
        marker_id, _ = aruco_follower.process_frame()
        print(marker_id)
        if marker_id == 4:
            print("Found ID 4, moving towards it.")
            while True:
                marker_id, within_30cm = aruco_follower.process_frame()
                if marker_id == 4 and within_30cm:
                    print("Reached ID 4 within 30 cm.")
                    aruco_follower.stop_motors()  # Stop motors when within 30 cm
                    break
            break

    # Step 3: Turn right until ID 0 is seen
    print("Step 3: Turning right to find ID 0.")
    while True:
        print("Finding Aruco 0")
        aruco_follower.turn_right()  # Start turning right to find ID 0
        marker_id, _ = aruco_follower.process_frame()
        if marker_id == 0:
            print("Found ID 0, moving towards it.")
            while True:
                marker_id, within_30cm = aruco_follower.process_frame()
                if marker_id == 0 and within_30cm:
                    print("Reached ID 0 within 30 cm.")
                    aruco_follower.stop_motors()  # Stop motors when within 30 cm
                    break
            break

    # Step 4: Turn right until ID 1 is seen
    print("Step 4: Turning right to find ID 1.")
    while True:
        print("Finding Aruco 1")
        aruco_follower.turn_right()  # Start turning right to find ID 1
        marker_id, _ = aruco_follower.process_frame()
        if marker_id == 1:
            print("Found ID 1, moving towards it.")
            while True:
                marker_id, within_30cm = aruco_follower.process_frame()
                if marker_id == 1 and within_30cm:
                    print("Reached ID 1 within 30 cm. Stopping.")
                    aruco_follower.stop_motors()  # Stop motors
                    return  # End the sequence

def main():
    # Motor and enable pin configuration
    motor_pins = [{'forward': 21, 'backward': 20}, {'forward': 6, 'backward': 5}]
    enable_pins = [12, 13]

    # Camera calibration parameters
    cam_mat = np.array([[1003.1076720832533, 0.0, 325.5842274588375],
                        [0.0, 1004.8079121262164, 246.67564927792367],
                        [0.0, 0.0, 1.0]])
    dist_coef = np.array([0.1886629014531147, 0.0421057002310688, 0.011153911980654914, 0.012946956962024124, 0.0])

    # Initialize the ArUco follower
    aruco_follower = ArucoFollower(motor_pins, enable_pins, cam_mat, dist_coef)

    # Perform the path planning based on the specified sequence
    path_planning(aruco_follower)

    # Release resources
    aruco_follower.release_resources()

if __name__ == "__main__":
    main()

