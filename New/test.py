import RPi.GPIO as GPIO

# GPIO pin
pin1 = 18
pin2 = 17
pin3 = 27
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pin1, GPIO.OUT)
GPIO.setup(pin2, GPIO.OUT)
GPIO.setup(pin3, GPIO.OUT)
while True:
	GPIO.output(pin1, GPIO.HIGH)
	GPIO.output(pin2, GPIO.HIGH)
	GPIO.output(pin3, GPIO.HIGH)
#HIGH  LOW