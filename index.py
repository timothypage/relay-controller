import time
import RPi.GPIO as GPIO

pin_list = [2, 3, 4, 17, 27, 22, 9, 10]

GPIO.setmode(GPIO.BCM)

for i in pin_list:
    GPIO.setup(i, GPIO.OUT)
    GPIO.output(i, GPIO.HIGH)

counter = 2

for i in pin_list:
    GPIO.output(i, GPIO.LOW)
    print(f"relay index: {counter}")
    print(f"GPIO pin: {i}")
    counter += 1
    time.sleep(1)
    
GPIO.cleanup()
