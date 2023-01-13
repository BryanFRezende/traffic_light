# Version 1.0

import RPi.GPIO as GPIO
import time

# Define the GPIO pins based on board pin numbering
r_led = 36
y_led = 38
g_led = 40

# Make the script read board pin numbers
GPIO.setmode(GPIO.BOARD)

# Set the led pins as output pins defaulted to LOW and disregard warnings
GPIO.setwarnings(False)
GPIO.setup(r_led, GPIO.OUT, initial=0)
GPIO.setup(y_led, GPIO.OUT, initial=0)
GPIO.setup(g_led, GPIO.OUT, initial=0)

# Test each one on startup
time.sleep(1)
GPIO.output(r_led, 1)
time.sleep(0.5)
GPIO.output(r_led, 0)
time.sleep(0.5)
GPIO.output(y_led, 1)
time.sleep(0.5)
GPIO.output(y_led, 0)
time.sleep(0.5)
GPIO.output(g_led, 1)
time.sleep(0.5)
GPIO.output(g_led, 0)
time.sleep(1)

# Define the waiting period in seconds for each light and declare the variable to hold the last
# timestamp for each light
r_per = 30
Rtime = None
y_per = 5
Ytime = None
g_per = 20
Gtime = None

# Define run variable to run While set to True
run = True

while run == True:
    try:
        GPIO.output(r_led, 1)               # Turn on the red light
        time.sleep(r_per)                   # Wait for the red light period to elapse
        GPIO.output(r_led, 0)               # Red light off
        GPIO.output(g_led, 1)               # Green light on
        time.sleep(g_per)                   # Wait green
        GPIO.output(g_led, 0)               # Green off
        GPIO.output(y_led, 1)               # Yellow on
        time.sleep(y_per)                   # Wait yellow
        GPIO.output(y_led, 0)               # Yellow off
    except KeyboardInterrupt:
        # Turn off the LEDs and cleanup the gpio pins
        run == False
        GPIO.output([r_led, y_led, g_led], 0)
        GPIO.cleanup()
        print('Lights off!')