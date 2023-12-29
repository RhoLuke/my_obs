import RPi.GPIO as GPIO
import os
import time
from logging import Logger
#from RpiMotorLib.RpiMotorLib import A4988Nema
import dm542t

GPIO.setmode(GPIO.BCM)

class ROOF:

    def __init__(self, logger: Logger) -> None:

        self._state: int = None #0:OPEN|1:CLOSEd|2:OPENING|3:CLOSING|4:ERROR
        self._state_close: bool = None #TRUE when this status is reached
        self._state_open: bool = None #TRUE when this status is reached
        self._isMoving: bool = None #TRUE when the roof is moving
        self._mode: int = 0 #0: NORMAL | 1: BLIND
        self._target: bool = None #TRUE is aiming OPEN and FALSE is aiming CLOSE
        self._connected: bool = False
        self._abort: bool = False
        self.logger = logger

        self._mech_time = 3.0 #Time in sec to complete the colse/open movement !TO BE REFINE
        self._mid_time = 2.0 #Time in sec for mid velocity
        self._start_vel = 0.5 #Time in sec between step for inital phase movement
        self._mid_vel = 0.1 #Time in sec between step for mid phase movement
        self._final_vel = 0.05 #Time in sec between step for final phase movement

        #PIN
        self._open = {
            'com': 'GND',
            'nc': 19,
            'no': 26
        }

        self._close = {
            'com': 'GND',
            'nc': 11,
            'no': 0
        }

        self._motor_pin = {'pull': 24,
                           'dir': 23}

        self._motor = dm542t.DM542T(self._motor_pin['pull'], self._motor_pin['dir'])
    
    #CLASS PROPERTIES

    @property
    def connected(self) -> bool:
        res = self._connected
        return res
    
    @connected.setter
    def connected(self, connected: bool):
        self._connected = connected
    
    @property
    def state(self) -> int:
        res = self._state
        return res
    @state.setter
    def state(self, st: int):
        self._state = st
    
    @property
    def open_pin(self) -> dict:
        res = self._open
        return res
    
    @property
    def close_pin(self) -> dict:
        res = self._close
        return res
    
    @property
    def state_close(self) -> bool:
        res = self._state_close
        return res
    
    @property
    def state_open(self) -> bool:
        res = self._state_open
        return res
    
    @property
    def motor_pin(self) -> dict:
        res = self._motor_pin
        return res
    
    @property
    def isMoving(self) -> bool:
        res = self._isMoving
        return res
    @isMoving.setter
    def isMoving(self, state:bool):
        self._isMoving = state
    
    @property
    def mode(self) -> int:
        res = self._mode
        return res
    
    @mode.setter
    def mode(self, md: int):
        self._mode = md
    
    @property
    def target(self) -> bool:
        res = self._target
        return res
    
    @target.setter
    def target(self, tg: bool):
        self._target = tg
    
    @property
    def abort(self) -> bool:
        res = self._abort
        return self
    @abort.setter
    def abort(self, state: bool):
        self._abort = state

    #READING CLOSE/OPEN SENSOR FUNCTIONS
    def read_sensor(self, which: str) -> bool:
        
        if which == 'close':
            sensor = self._close
        elif which == 'open':
            sensor = self._open

        nc = GPIO.input(sensor['nc'])
        no = GPIO.input(sensor['no'])

        return (nc, no)
    
    def check_sensor(self) -> (bool, str):
        nc_open, no_open = self.read_sensor('open')
        nc_close, no_close = self.read_sensor('close')
        
        if nc_open == no_open:
            self.logger.warning('!!! WARNING: OPEN SENSOR IS NOT WORKING PROPERLY')
            return (False, 'open sensor')
        elif nc_close == no_close:
            self.logger.warning('!!! WARNING: CLOSE SENSOR IS NOT WORKING PROPERLY')
            return (False, 'close sensor')
        else:
            return (True, '')
        
    
    #FUNCTION THAT MOVE THE ROOF
    #Between moving it has to control the state of the sensor
    #EACH SENSOR IS HIGH PULLED AND COM IS GND, SO IN NORMAL STATE: 
    # NC = LOW (False)
    # NO = HIGH (True)
    # 
    # WHEN THE SENSOR IS ACTIVATED:
    # NC = HIGH (True)
    # NO = LOW (False)
    #
    def move_roof(self, tg: bool) -> None:

        self._target = tg
        #print(tg, self._mode)
        
        if self._mode == 0: #NORMAL MODE, USING SENSORS.
            if self._target: #Opening
                nc_close, no_close = self.read_sensor('close')
                nc_open, no_open = self.read_sensor('open')
                
                if nc_open == True and no_open == False:
                    print('ROOF ALREADY OPEN')
                elif ((nc_close == True and no_close == False) and
                      (nc_open == False and no_open == True)): # TODO: implement a stop procedure
                    print('CLOSE SENSOR ARE WORKING PROPERLY \nSTARTING OPENING')
                    self._isMoving = True
                    self._state = 2
                    #GPIO.output(self._motor_pin['enable'], True)
                    
                    try:
                        while(nc_close == False and no_close == True):
                            self._motor.motor_go(clockwise=False,
                                                steptype='Full',
                                                steps=1,
                                                stepdelay=self._start_vel)
                            sensor_state, which_sensor = self.check_sensor()
                            if not sensor_state:
                                self.logger.error('!!!SHUTTER ERROR! CANNOT OPENING!!!')
                                self._state = 4
                                self._isMoving = False
                                return
                            if self._abort:
                                self.logger.error('!!!ABORT OPENING!!!')
                                self._state = 0
                                self._isMoving = False
                                self._abort = False
                                return
                                
                    except:
                        self.logger.error('!!!SHUTTER ERROR! CANNOT OPENING!!!')
                        self._state = 4
                        self._isMoving = False
                        return
                        
                    while(nc_close == True and no_close == False):
                        self._motor.motor_go(clockwise=False,
                                            steptype='Full',
                                            steps=1,
                                            stepdelay=self._final_vel)
                        sensor_state, which_sensor = self.check_sensor()
                        if not sensor_state:
                                self.logger.error('!!!SHUTTER ERROR! CANNOT OPENING!!!')
                                self._state = 4
                                self._isMoving = False
                                return
                        if self._abort:
                                self.logger.error('!!!ABORT OPENING!!!')
                                self._state = 0
                                self._isMoving = False
                                self._abort = False
                                return
                    
                    ti = time.time()
                    while(time.time()-ti < self._mech_time):
                        self._motor.motor_go(clockwise=False,
                                            steptype='Full',
                                            steps=1,
                                            stepdelay=self._start_vel)
                        sensor_state, which_sensor = self.check_sensor()
                        if not sensor_state:
                                self.logger.error('!!!SHUTTER ERROR! CANNOT OPENING!!!')
                                self._state = 4
                                self._isMoving = False
                                return
                        if self._abort:
                                self.logger.error('!!!ABORT OPENING!!!')
                                self._state = 0
                                self._isMoving = False
                                self._abort = False
                                return
                    
                    print('ROOF OPENED')
                    self._isMoving = False
                    self._state = 0
                    #GPIO.output(self._motor_pin['enable'], False)

            if not self._target: #Closening
                nc_close, no_close = self.read_sensor('close')
                nc_open, no_open = self.read_sensor('open')
                if nc_close == True and no_close == False:
                    print('ROOF ALREADY CLOSE')
                elif ((nc_close == True and no_close == False) and
                      (nc_open == False and no_open == True)):
                    print('OPEN SENSOR IS WORKING PROPERLY \nSTARTING CLOSENING')
                    self._isMoving = True
                    self._state = 3
                    #GPIO.output(self._motor_pin['enable'], True)

                    try:
                        while(nc_close == True and no_close == False):
                            self._motor.motor_go(clockwise=True,
                                                steptype='Full',
                                                steps=1,
                                                stepdelay=self._start_vel)
                            sensor_state, which_sensor = self.check_sensor()
                            if not sensor_state:
                                self.logger.error('!!!SHUTTER ERROR! CANNOT CLOSING!!!')
                                self._state = 4
                                self._isMoving = False
                                return
                            if self._abort:
                                self.logger.error('!!!ABORT CLOSING!!!')
                                self._state = 1
                                self._isMoving = False
                                self._abort = False
                                return
                    except:
                        self.logger.error('!!!SHUTTER ERROR! CANNOT CLOSING!!!')
                        self._state = 4
                        self._isMoving = False
                        return
                        
                    while(nc_close == True and no_close == False):
                        self._motor.motor_go(clockwise=True,
                                            steptype='Full',
                                            steps=1,
                                            stepdelay=self._final_vel)
                        sensor_state, which_sensor = self.check_sensor()
                        if not sensor_state:
                                self.logger.error('!!!SHUTTER ERROR! CANNOT CLOSING!!!')
                                self._state = 4
                                self._isMoving = False
                                return
                        if self._abort:
                                self.logger.error('!!!ABORT CLOSING!!!')
                                self._state = 1
                                self._isMoving = False
                                self._abort = False
                                return
                    
                    ti = time.time()
                    while(time.time()-ti < self._mech_time):
                        self._motor.motor_go(clockwise=True,
                                            steptype='Full',
                                            steps=1,
                                                stepdelay=self._start_vel)
                        sensor_state, which_sensor = self.check_sensor()
                        if not sensor_state:
                                self.logger.error('!!!SHUTTER ERROR! CANNOT CLOSING!!!')
                                self._state = 4
                                self._isMoving = False
                                return
                        if self._abort:
                                self.logger.error('!!!ABORT CLOSING!!!')
                                self._state = 1
                                self._isMoving = False
                                self._abort = False
                                return
                            
                    print('ROOF CLOSED')
                    self._isMoving = False
                    self._state = 1
                    #GPIO.output(self._motor_pin['enable'], False)
        
        if self._mode == 1: #BLIND MODE, ONLY TIME
            print('ROOF MOTION IN BLIND MODE!! \nSENSOR VERIFICATION REQUIRED')
            
            if self._target: #Opening
                
                self._state = 2
                #GPIO.output(self._motor_pin['enable'], True)
                ti = time.time()

                try:
                    self._isMoving = True
                    while(time.time()-ti < self._mech_time):
                            self._motor.motor_go(clockwise=False,
                                                steptype='Full',
                                                steps=1,
                                                stepdelay=self._start_vel)
                            if self._abort:
                                self.logger.error('!!!ABORT OPENING!!!')
                                print('!!!ABORT OPENING!!!')
                                self._state = 0
                                self._isMoving = False
                                self._abort = False
                                return
                except:
                        self.logger.error('!!!SHUTTER ERROR! CANNOT OPENING!!!')
                        self._state = 4
                        self._isMoving = True
                        return

                ti = time.time()        
                while(time.time()-ti < self._mid_time):
                    self._motor.motor_go(clockwise=False,
                                        steptype='Full',
                                        steps=1,
                                        stepdelay=self._final_vel)
                    if self._abort:
                                self.logger.error('!!!ABORT OPENING!!!')
                                print('!!!ABORT OPENING!!!')
                                self._state = 0
                                self._isMoving = False
                                self._abort = False
                                return
                
                ti = time.time()
                while(time.time()-ti < self._mech_time):
                    self._motor.motor_go(clockwise=False,
                                        steptype='Full',
                                        steps=1,
                                        stepdelay=self._start_vel)
                    if self._abort:
                                self.logger.error('!!!ABORT OPENING!!!')
                                print('!!!ABORT OPENING!!!')
                                self._state = 0
                                self._isMoving = False
                                self._abort = False
                                return
                print('ROOF OPENED')
                self._isMoving = False
                self._state = 0
                #GPIO.output(self._motor_pin['enable'], False)

            if not self._target: #Closening
                
                self._state = 3
                #GPIO.output(self._motor_pin['enable'], True)
                ti = time.time()

                try:
                    self._isMoving = True
                    while(time.time()-ti < self._mech_time):
                            self._motor.motor_go(clockwise=True,
                                                steptype='Full',
                                                steps=1,
                                                stepdelay=self._start_vel)
                            if self._abort:
                                self.logger.error('!!!ABORT CLOSING!!!')
                                print('!!!ABORT CLOSING!!!')
                                self._state = 1
                                self._isMoving = False
                                return
                except:
                        self.logger.error('!!!SHUTTER ERROR! CANNOT CLOSING!!!')
                        self._state = 4
                        self._isMoving = False
                        self._abort = False
                        return

                ti = time.time()        
                while(time.time()-ti < self._mid_time):
                    self._motor.motor_go(clockwise=True,
                                        steptype='Full',
                                        steps=1,
                                        stepdelay=self._final_vel)
                    if self._abort:
                                self.logger.error('!!!ABORT CLOSING!!!')
                                print('!!!ABORT CLOSING!!!')
                                self._state = 1
                                self._isMoving = False
                                self._abort = False
                                return
                
                ti = time.time()
                while(time.time()-ti < self._mech_time):
                    self._motor.motor_go(clockwise=True,
                                        steptype='Full',
                                        steps=1,
                                        stepdelay=self._start_vel)
                    if self._abort:
                                self.logger.error('!!!ABORT CLOSING!!!')
                                print('!!!ABORT CLOSING!!!')
                                self._state = 1
                                self._isMoving = False
                                self._abort = False
                                return
                print('ROOF CLOSED')
                self._isMoving = False
                self._state = 1
                #GPIO.output(self._motor_pin['enable'], False)


                





        
    






