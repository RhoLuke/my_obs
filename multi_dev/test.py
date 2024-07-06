import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

sensor = {
    'nc': 19,
    'no': 26}

GPIO.setup(sensor['nc'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(sensor['no'], GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    try:
        input()
        state = {'nc': GPIO.input(sensor['nc']),
                 'no': GPIO.input(sensor['no'])}
        print(state)
    except KeyboardInterrupt:
        break
