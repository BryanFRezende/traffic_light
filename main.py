import RPi.GPIO as GPIO
import time
import asyncio
from sshkeyboard import listen_keyboard, stop_listening

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

# Define asynchronous function to change run variable to false when the 'q' key is pressed
async def press(key):
    if key == "q":
        global run
        run = False
        print(f"{key}")
        stop_listening()
    else:
        print(f"{key}")
        stop_listening()

# Define asynchronous function to capture key press (based on sshkeyboard python library: https://sshkeyboard.readthedocs.io/en/latest/reference.html#sshkeyboard.stop_listening)
async def key_check():
    listen_keyboard(on_press=press)

# Define the main loop controlling the traffic signal LEDs
async def main():
    task = asyncio.create_task(key_check())
    while run == True:
        Ctime = time.perf_counter()         # Get a current timestamp
        pin_states = [GPIO.input(r_led), GPIO.input(y_led), GPIO.input(g_led)]      # Get a list of pin states

        if pin_states == [0,0,0]:            # Define the initial condition handling
            GPIO.output(r_led, 1)            # Red on
            Rtime = time.perf_counter()     # Start red timer
            continue

        elif pin_states == [1,0,0]:          # Define red handling
            if Ctime - Rtime >= r_per:      # Check if red period has elapsed
                GPIO.output(r_led, 0)       # If so, red off
                GPIO.output(g_led, 1)        # Green on
                Gtime = time.perf_counter() # Start green timer
                continue
            else:                           # If not, continue
                continue

        elif pin_states == [0,1,0]:          # Define yellow handling
            if Ctime - Ytime >= y_per:      # Check yellow period elapse
                GPIO.output(y_led, 0)       # If so, yellow off
                GPIO.output(r_led, 1)        # Red on
                Rtime = time.perf_counter() # Start red timer
                continue
            else:                           # If not, continue
                continue

        elif pin_states == [0,0,1]:          # Define green handling
            if Ctime - Gtime >= g_per:      # Check green period elapse
                GPIO.output(g_led, 0)       # If so, green off
                GPIO.output(y_led, 1)        # Yellow on
                Ytime = time.perf_counter() # Start yellow timer
                continue
            else:                           # If not, continue
                continue

# Asynchronously run the loop
asyncio.run(main())

# Turn off the LEDs and cleanup the gpio pins
GPIO.output([r_led, y_led, g_led], 0)
GPIO.cleanup()
print('Lights off!')
