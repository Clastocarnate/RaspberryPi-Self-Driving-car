import RPi.GPIO as GPIO
from Lane_Control import getLaneCurve
import WebcamModule

# Set up GPIO mode
GPIO.setmode(GPIO.BOARD)

# Define motor pins
motor1pin1 = 16  # BOARD number for BCM 23
motor1pin2 = 18  # BOARD number for BCM 24
motor2pin1 = 11  # BOARD number for BCM 17
motor2pin2 = 13  # BOARD number for BCM 27

# Setup GPIO pins
GPIO.setup(motor1pin1, GPIO.OUT)
GPIO.setup(motor1pin2, GPIO.OUT)
GPIO.setup(motor2pin1, GPIO.OUT)
GPIO.setup(motor2pin2, GPIO.OUT)

class Motor:
    def __init__(self, pin1, pin2, pin3, pin4):
        self.pin1 = pin1
        self.pin2 = pin2
        self.pin3 = pin3
        self.pin4 = pin4

    def move_forward(self):
        GPIO.output(self.pin1, GPIO.HIGH)
        GPIO.output(self.pin4, GPIO.HIGH)
        GPIO.output(self.pin2, GPIO.LOW)
        GPIO.output(self.pin3, GPIO.LOW)

    def steer_left(self):
        GPIO.output(self.pin1, GPIO.HIGH)
        GPIO.output(self.pin3, GPIO.LOW)

    def steer_right(self):
        GPIO.output(self.pin1, GPIO.LOW)
        GPIO.output(self.pin3, GPIO.HIGH)

    def stop(self):
        GPIO.output(self.pin1, GPIO.LOW)
        GPIO.output(self.pin2, GPIO.LOW)
        GPIO.output(self.pin3, GPIO.LOW)
        GPIO.output(self.pin4, GPIO.LOW)

##################################################
motor = Motor(motor1pin1, motor1pin2, motor2pin1, motor2pin2)
##################################################

def main():
    img = WebcamModule.getImg()
    curveVal = getLaneCurve(img, display=1)

    # Sensitivity to control how sharply we turn based on the curve
    sen = 1.3
    maxVal = 1.0  # Maximum steering limit (curve value)
    
    # Limiting the steering commands to the maxVal range
    if curveVal > maxVal:
        curveVal = maxVal
    elif curveVal < -maxVal:
        curveVal = -maxVal
    
    # Basic steering logic
    if curveVal > 0:
        motor.steer_left()  # Steering without considering the intensity
    elif curveVal < 0:
        motor.steer_right()
    else:
        motor.move_forward()

if __name__ == '__main__':
    try:
        while True:
            main()
    except KeyboardInterrupt:
        motor.stop()
        GPIO.cleanup()
