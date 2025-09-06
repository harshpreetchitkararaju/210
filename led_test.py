import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BOARD)


red1 = 11   
red2 = 13   
red3 = 19   


GPIO.setup(red1, GPIO.OUT)
GPIO.setup(red2, GPIO.OUT)
GPIO.setup(red3, GPIO.OUT)

def menu():
    print("\nLED Control Menu:")
    print("1. Red LED 1 ON")
    print("2. Red LED 1 OFF")
    print("3. Red LED 2 ON")
    print("4. Red LED 2 OFF")
    print("5. Red LED 3 ON")
    print("6. Red LED 3 OFF")
    print("7. Exit")

try:
    while True:
        menu()
        choice = input("Enter your choice (1-7): ")

        if choice == '1':
            GPIO.output(red1, True)
        elif choice == '2':
            GPIO.output(red1, False)
        elif choice == '3':
            GPIO.output(red2, True)
        elif choice == '4':
            GPIO.output(red2, False)
        elif choice == '5':
            GPIO.output(red3, True)
        elif choice == '6':
            GPIO.output(red3, False)
        elif choice == '7':
            print("Exiting...")
            break
        else:
            print("Invalid choice!")

finally:
    GPIO.cleanup()
