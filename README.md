# ArUco Marker Following and Path Planning Robot

## Overview

This project demonstrates a robot that autonomously follows a sequence of ArUco markers using a camera and motors. The robot uses a combination of computer vision (OpenCV and ArUco module) and GPIO-based motor control to detect markers, align itself, and move to predefined positions in a step-by-step path planning process.

## Features

1. **ArUco Marker Detection**:
   - Identifies ArUco markers in real-time using a webcam.
   - Estimates the pose of the markers (position and orientation) using calibrated camera parameters.

2. **Motor Control**:
   - Controls two DC motors using the `gpiozero` library for movement (forward, left, right, stop).
   - Ensures precise navigation toward markers.

3. **Path Planning**:
   - Implements a sequence of steps to navigate to specific marker IDs:
     - Move to marker ID 2.
     - Turn left to locate marker ID 4.
     - Turn right to locate marker ID 0.
     - Turn right to locate marker ID 1.

4. **Proximity-Based Actions**:
   - Stops the robot when it is within 30 cm of a marker.

## Requirements

### Hardware
- Raspberry Pi (or compatible device)
- Camera (e.g., USB webcam)
- Two DC motors
- Motor driver with enable and control pins

### Software
- Python 3.7+
- Required Python libraries:
  - OpenCV (`cv2`)
  - NumPy
  - gpiozero

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/aruco-robot.git
   cd aruco-robot
   ```

2. **Install Dependencies**:
   Install the required Python libraries:
   ```bash
   pip install opencv-python-headless numpy gpiozero
   ```

3. **Connect Hardware**:
   - Connect the motors to GPIO pins on the Raspberry Pi using the specified pin configuration in the code.

4. **Camera Calibration**:
   - Use a calibrated camera to ensure accurate pose estimation.
   - Replace the `cam_mat` and `dist_coef` arrays in the code with your camera's calibration parameters.

## How It Works

1. **Marker Following**:
   - The `ArucoFollower` class handles real-time marker detection and motor control.
   - The robot adjusts its movement based on the marker's position relative to the center of the screen and stops within 30 cm of the marker.

2. **Path Planning**:
   - The `path_planning` function defines a sequence of steps for the robot:
     - Navigate to specific ArUco markers based on their IDs.
     - Perform specific actions (e.g., turning left or right) to find the next marker.

3. **Autonomous Navigation**:
   - The robot dynamically adjusts its path using real-time feedback from the camera and proximity calculations.

## Usage

1. **Execute Path Planning**:
   ```bash
   sudo python3 PathPlanning.py
   ```

2. **Control Actions**:
   - The robot will autonomously follow the sequence of steps defined in the path planning logic.

3. **Quit Execution**:
   - Press `q` to terminate the program safely.

## Pin Configuration

| Component       | GPIO Pin Numbers |
|-----------------|------------------|
| Motor 1 Forward | 21               |
| Motor 1 Backward| 20               |
| Motor 2 Forward | 6                |
| Motor 2 Backward| 5                |
| Motor 1 Enable  | 12               |
| Motor 2 Enable  | 13               |

## Project Files

1. **aruco_follower.py**:
   - Implements the `ArucoFollower` class for real-time marker detection and motor control.

2. **aruco_path_planning.py**:
   - Defines a path planning sequence to follow specific ArUco markers in a predefined order.

## Future Improvements

1. Implement obstacle avoidance while navigating between markers.
2. Add support for more complex path planning algorithms.
3. Integrate additional sensors like LiDAR or ultrasonic for enhanced navigation.

