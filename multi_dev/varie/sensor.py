import RPi.GPIO as GPIO
import time 
GPIO.setmode(GPIO.BCM)

class SENSOR:
    
    def __init__(self):
        
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
            
        except Exception as e:
            self._state = 4
            raise Exception (f'Sensor check failed: {e}')
    
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
            self._state = 4
            raise Exception (f'Sensor {which} is not working')

        return state

sensor = SENSOR()
sens = ['close1',
     'close2',
     'open1',
     'open2',
     ]

sensor.check_sensor()

try:
    while True:
        for s in sens:
            res = sensor.read_sensor(s)
            if res == 'active':
                print(f'Sensor {s}: {res}')
            time.sleep(0.1)
except KeyboardInterrupt:
    pass