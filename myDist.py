import cv2 as cv
import numpy as np
from cv2 import aruco

# Hardcoded camera matrix and distortion coefficients
cameraMatrix = np.array([[1003.1076720832533, 0.0, 325.5842274588375],
                         [0.0, 1004.8079121262164, 246.67564927792367],
                         [0.0, 0.0, 1.0]])

distCoeffs = np.array([0.1886629014531147, 0.0421057002310688, 0.011153911980654914, 0.012946956962024124, 0.0])

# Define the ArUco marker size (for example, 9.5 cm)
markerLength = 0.095  # In meters

# Define the ArUco dictionary (4x4 with 50 markers)
arucoDict = aruco.Dictionary_get(aruco.DICT_4X4_50)
arucoParams = aruco.DetectorParameters_create()

def main():
    # Start video capture
    cap = cv.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return 1  # Return error code if capture fails

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            return 2  # Return error code if frame read fails

        # Convert to grayscale
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        # Detect ArUco markers
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, arucoDict, parameters=arucoParams)

        # If markers are detected, process only the first detected marker
        if ids is not None and len(ids) > 0:
            # Estimate pose of the first marker
            rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners[0], markerLength, cameraMatrix, distCoeffs)
            R, _ = cv.Rodrigues(rvec)

            # Invert the rotation matrix
            R_inv = np.transpose(R)

            # Invert the translation vector
            tvec_inv = -np.dot(R_inv, tvec[0][0].reshape((3, 1)))

            # Draw the marker axes and the ID on the frame
            cv.putText(frame, str(ids[0][0]), (int(corners[0][0][0][0]), int(corners[0][0][0][1])), 
                       cv.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2, cv.LINE_AA)

            # Calculate and display the distance
            distance = np.linalg.norm(tvec[0][0])
            cv.putText(frame, f"Dist: {distance:.2f}m", (int(corners[0][0][0][0]), int(corners[0][0][0][1])+15),
                       cv.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2, cv.LINE_AA)
            print(tvec)

        # Display the frame
        cv.imshow('Frame', frame)

        # Exit if 'q' is pressed
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture and close windows
    cap.release()
    cv.destroyAllWindows()
    return 0  # Success

if __name__ == "__main__":
    exit_code = main()
    if exit_code != 0:
        print(f"Program exited with error code {exit_code}")
