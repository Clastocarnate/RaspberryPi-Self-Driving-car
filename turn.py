import time
from gpiozero import Motor, OutputDevice

# Motor setup
motor1 = Motor(forward=21, backward=20)  # Motor 1: IN1 -> GPIO 20, IN2 -> GPIO 21
motor2 = Motor(forward=6, backward=5)    # Motor 2: IN3 -> GPIO 5, IN4 -> GPIO 6
en1 = OutputDevice(12)  # Enable pin for Motor 1 (GPIO 12)
en2 = OutputDevice(13)  # Enable pin for Motor 2 (GPIO 13)

# Turn on the enable pins
en1.on()
en2.on()

# Function to stop the motors
def stop_motors():
    motor1.stop()
    motor2.stop()

def turn_bot(direction, duration):
    if direction == "left":
        print(f"Turning left for {duration} seconds...")
        motor2.backward(0.5)  # Left motor backward
        motor1.forward(0.5)   # Right motor forward
    elif direction == "right":
        print(f"Turning right for {duration} seconds...")
        motor2.forward(0.5)  # Left motor forward
        motor1.backward(0.5)  # Right motor backward

    # Let the bot turn for the specified duration
    time.sleep(duration)
    stop_motors()

# Main logic
if __name__ == "__main__":
    # Get user input
    direction = input("Enter the direction to turn (left/right): ").lower()
    duration = float(input("Enter the number of seconds to turn: "))

    # Turn the bot based on user input
    turn_bot(direction, duration)

    # Turn off the enable pins when done
    en1.off()
    en2.off()
