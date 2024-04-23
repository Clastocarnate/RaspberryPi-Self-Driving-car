import cv2

def main():
    # Initialize the webcam (use 1 or other number if the external webcam is not the default camera)
    cap = cv2.VideoCapture(0)

    # Check if the webcam is opened correctly
    # if not cap.isOpened():
    #     raise IOError("Cannot open webcam")

    # Define the codec and create VideoWriter object to save the video
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = None

    is_recording = False
    print("Press 's' to start recording and 'q' to stop and exit...")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Display the resulting frame
        cv2.imshow('Webcam Recording', frame)

        # Start or stop recording when 's' or 'q' is pressed
        k = cv2.waitKey(1)
        if k & 0xFF == ord('s'):
            if not is_recording:
                # Start recording
                is_recording = True
                out = cv2.VideoWriter('output.avi', fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))
                print("Recording started...")
        elif k & 0xFF == ord('q'):
            if is_recording:
                # Stop recording
                is_recording = False
                out.release()
                print("Recording stopped and saved as output.avi")
            break

        # Write the frame into the file 'output.avi' if recording
        if is_recording:
            out.write(frame)

    # Release everything when job is finished
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
