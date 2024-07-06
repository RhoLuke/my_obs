# import RPi.GPIO as GPIO
# GPIO.setmode(GPIO.BCM)
# 
# pwm_pin = 13
# GPIO.setup(pwm_pin, GPIO.OUT)
# 
# 
# pwm = GPIO.PWM(pwm_pin, 100000)
# pwm.start(0)
#ChangeDutyCycle(int((brightness/self.__class.__._max_brightness) * 100))

import pigpio

pwm_pin = 13
pi = pigpio.pi()
pi.set_PWM_dutycycle(pwm_pin,   0)
pi.hardware_PWM(pwm_pin, int(8e+4), int(3e+4))