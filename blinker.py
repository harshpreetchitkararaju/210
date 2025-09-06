import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

led = 11  
GPIO.setup(led, GPIO.OUT)

print("LED will blink 5 times")
try:
    for i in range(5):
        GPIO.output(led, True)
        time.sleep(1)
        GPIO.output(led, False)
        time.sleep(1)
finally:
    GPIO.cleanup()
