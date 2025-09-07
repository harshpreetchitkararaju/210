import RPi.GPIO as GPIO
import sys

LED_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)


if len(sys.argv) > 1:
    cmd = sys.argv[1].lower()

    if cmd == "on":
        GPIO.output(LED_PIN, GPIO.HIGH)
        print("LED turned ON")

    elif cmd == "off":
        GPIO.output(LED_PIN, GPIO.LOW)
        print("LED turned OFF")
