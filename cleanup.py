import RPi.GPIO as GPIO
r_led = 36
y_led = 38
g_led = 40
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(r_led, GPIO.OUT, initial=0)
GPIO.setup(y_led, GPIO.OUT, initial=0)
GPIO.setup(g_led, GPIO.OUT, initial=0)
GPIO.output([r_led, y_led, g_led], 0)
GPIO.cleanup()
