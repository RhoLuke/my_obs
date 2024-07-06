from logging import Logger
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)


class FlatBox:
    def __init__(self, logger: Logger):
        
        self.__class__._state: int = 1 #1:OFF|2:NOTREADY|3:READY|4:UNKNOWN|5:ERROR
        self.__class__._connected: bool = False
        self.__class__.logger = logger
        
        self.__class__._pwm_pin = 13
        self.__class__._current_brightness = 0
        self.__class__._max_brightness = 255
        self.__class__._settling_time = 3.0
    
    
    # GUARDED PROPERTIES
    
    @property
    def connected(self) -> bool:
        res = self.__class__._connected
        return res
    @connected.setter
    def connected(self, connected: bool):
        self.__class__._connected = connected
        
        if connected:
            GPIO.setup(self.__class__._pwm_pin, GPIO.OUT)
            self.__class__._pwm = GPIO.PWM(self.__class__._pwm_pin, 50)
            self.__class__._pwm.start(0)
        else:
            self.__class__._pwm.stop()
            
    
    @property
    def state(self) -> int:
        res = self.__class__._state
        return res
    @state.setter
    def state(self, st: int):
        self.__class__._state = st
    
    @property
    def max_brightness(self) -> int:
        res = self.__class__._max_brightness
        return res
    
    @property
    def current_brightness(self) -> int:
        res = self.__class__._current_brightness
        return res
    
    def go_to(self, brightness: int) -> None:
        self.__class__._current_brightness = brightness
        self.__class__._state = 2
        self.__class__._pwm.ChangeDutyCycle(int((brightness/self.__class.__._max_brightness) * 100))
        time.sleep(self.__class__._settling_time)
        self.__class__._state = 3
        