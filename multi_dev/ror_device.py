import threading
import RPi.GPIO as GPIO
import os
import time
from logging import Logger
import dm542t

GPIO.setmode(GPIO.BCM)

class ROOF:

    def __init__(self, logger: Logger, master: bool) -> None:
        
        self.event = threading.Event()
        self.master = master

        self.__class__._state: int = None #0:OPEN|1:CLOSED|2:OPENING|3:CLOSING|4:ERROR
        self.__class__._direction: bool = None #TRUE is aiming OPEN and FALSE is aiming CLOSE
        self.__class__._connected: bool = False
        self.__class__.logger = logger

        #PIN
        self.__class__._open1 = {
            'com': 'GND',
            'nc': 19,
            'no': 26
        }
        
        self.__class__._open2 = {
            'com': 'GND',
            'nc': 6,
            'no': 5
        }

        self.__class__._close1 = {
            'com': 'GND',
            'nc': 11,
            'no': 0
        }
        
        self.__class__._close2 = {
            'com': 'GND',
            'nc': 10,
            'no': 9
        }
        
        self.__class__._motor_pin = {'pull': 24,
                           'dir': 23}
        self.__class__._motor = dm542t.DM542T(self._motor_pin['pull'], self._motor_pin['dir'])
    
    #CLASS PROPERTIES

    @property
    def connected(self) -> bool:
        res = self.__class__._connected
        return res
    @connected.setter
    def connected(self, connected: bool):
        self.__class__._connected = connected
    
    @property
    def state(self) -> int:
        res = self.__class__._state
        return res
    @state.setter
    def state(self, st: int):
        self.__class__._state = st
    
    @property
    def open_pin(self) -> dict:
        res = [self.__class__._open1, self.__class__._open2]
        return res
    
    @property
    def close_pin(self) -> dict:
        res = [self.__class__._close1, self.__class__._close2]
        return res
    
    @property
    def motor_pin(self) -> dict:
        res = self.__class__._motor_pin
        return res
    
    @property
    def direction(self) -> bool:
        res = self.__class__._direction
        return res
    @direction.setter
    def direction(self, d: bool):
        self.__class__._direction = d
        

    #READING SENSORS STATE
    def read_sensor(self, which: str) -> str:
        
            
        if which == 'close1':
            sensor = self.__class__._close1
        elif which == 'close2':
            sensor = self.__class__._close2
        elif which == 'open1':
            sensor = self.__class__._open1
        elif which == 'open2':
            sensor = self.__class__._open2
        else:
            raise ValueError('Sensor not recognized')

        nc = GPIO.input(sensor['nc'])
        no = GPIO.input(sensor['no'])
        
        if nc == True and no == False:
            state = 'active'
        elif nc == False and no == True:
            state = 'inactive'
        else:
            if self.__class__._motor.isMoving:
                self.abort()
            self.__class__._state = 4
            raise Exception (f'Sensor {which} is not working')

        return state
    
    def check_sensor(self) -> (bool, str):
        try:
            GPIO.setup(self.__class__._close1['nc'], GPIO.IN)
            GPIO.setup(self.__class__._close1['no'], GPIO.IN)
            GPIO.setup(self.__class__._close2['nc'], GPIO.IN)
            GPIO.setup(self.__class__._close2['no'], GPIO.IN)
            GPIO.setup(self.__class__._open1['nc'], GPIO.IN)
            GPIO.setup(self.__class__._open1['no'], GPIO.IN)
            GPIO.setup(self.__class__._open2['nc'], GPIO.IN)
            GPIO.setup(self.__class__._open2['no'], GPIO.IN)
            
            GPIO.setup(self.__class__._motor_pin['pull'], GPIO.OUT)
            GPIO.setup(self.__class__._motor_pin['dir'], GPIO.OUT)
            
        except Exception as e:
            self.__class__._state = 4
            raise Exception (f'Sensor check failed: {e}')

    #FUNCTION THAT MOVE THE ROOF
    #Between moving it has to control the state of the sensor
    #EACH SENSOR IS HIGH PULLED AND COM IS GND, SO IN NORMAL STATE: 
    # NC = LOW (False)
    # NO = HIGH (True)
    # 
    # WHEN THE SENSOR IS ACTIVATED:
    # NC = HIGH (True)
    # NO = LOW (False)

    def move_roof(self, direction: bool) -> None:

        self._direction = direction
        
        close1 = self.read_sensor('close1')
        close2 = self.read_sensor('close2')
        open1 = self.read_sensor('open1')
        open2 = self.read_sensor('open2')
            
        if self._direction: #Opening
            if open1 == 'active':
                self.logger.info('Shutter already open')
                self.__class__._state = 0
                return
            else:
                mid_sensor = 'open2'
                final_sensor = 'open1'
            
        elif not self._direction: #Closing
            if close1 == 'active':
                self.logger.info('Shutter already closed')
                self.__class__._state = 1
                return
            else:
                mid_sensor = 'close2'
                final_sensor = 'close1'
                
        self._second_sensor_reached = False    
        try:
            self.__class__._motor.start(direction=self._direction)
            if self._direction:
                self.__class__._state = 2
            else:
                self.__class__._state = 3
            
            while self.read_sensor(mid_sensor) != 'active':
                if self.read_sensor(final_sensor) == 'active':
                    self.__class__._state = 0 if self._direction else 1
                time.sleep(0.3)
            
            self.__class__._motor.start(direction=self._direction, min_speed=True)
            while self.read_sensor(final_sensor) != 'active':
                time.sleep(0.3)
            
            self.__class__._motor.halt()
            while self.__class__._motor._isMoving:
                pass
            
            if self.read_sensor('open1') == 'active':
                self.logger.info('Shutter open')
                self.__class__._state = 0
            elif self.read_sensor('close1') == 'active':
                self.logger.info('Shutter close')
                self.__class__._state = 1
            
        except Exception as e:
            self.logger.error(f'!!!SHUTTER ERROR: {e}!!!')
            self.__class__._state = 4
            return
        
    def abort(self):
        self.__class__._motor.halt()
