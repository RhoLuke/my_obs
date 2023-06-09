
# -*- coding: utf-8 -*-
#
# -----------------------------------------------------------------------------
# Driver for the control of 8 switch board
#
# Author:   Luca Rosignoli
#
# -----------------------------------------------------------------------------
# Edit History:
#   Generated by Python Interface Generator for AlpycaDevice
#
#
#import RPi.GPIO as GPIO
#GPIO.setup(GPIO.BCM)

from logging import Logger

class SwitchDevice:

    def __init__(self, logger: Logger):
        self.name: str = 'SwitchDevice'
        self.logger = logger
        self._connected: bool = False

        # Device properties
        self._maxswitch: int = 8
        self._canwrite: bool = True
        self._minswitchvalue: float = 0.0
        self._maxswitchvalue: float = 1.0
        self._switchstep: int = 1.0

        # Switch porperty
        self._roof: dict ={'Name': 'ROOF',
                           'Id': 0,
                           'Description': 'Roof power',
                           'Switchpinout': 18,
                           'State': False,
                           'Value': 0.0}
        
        self._weather: dict ={'Name': 'Weather sensor',
                              'Id': 1,
                            'Description': 'Weather sensor power',
                            'Switchpinout': 23,
                            'State': False,
                            'Value': 0.0}
        
        self._mount: dict ={'Name': 'Telescope mount',
                            'Id': 2,
                           'Description': 'Telescope mount power',
                           'Switchpinout': 24,
                           'State': False,
                           'Value': 0.0}
        
        self._camera: dict ={'Name': 'Camera',
                             'Id': 3,
                           'Description': 'Camera power',
                           'Switchpinout': 25,
                           'State': False,
                           'Value': 0.0}
        
        self._astropc: dict ={'Name': 'Astro pc',
                              'Id': 4,
                           'Description': 'Astro pc power',
                           'Switchpinout': 8,
                           'State': False,
                           'Value': 0.0}
        
        self._security: dict ={'Name': 'Security',
                            'Id': 5,
                           'Description': 'Security power',
                           'Switchpinout': 7,
                           'State': False,
                           'Value': 0.0}
        
        self._light: dict ={'Name': 'Light',
                            'Id': 6,
                           'Description': 'Light power',
                           'Switchpinout': 12,
                           'State': False,
                           'Value': 0.0}
        
        self._flat: dict ={'Name': 'Flat box',
                           'Id': 7,
                           'Description': 'Flat box power',
                           'Switchpinout': 16,
                           'State': False,
                           'Value': 0.0}

    #
    # Guarded properties
    #

    @property
    def maxswitch(self) -> int:
        res = self._maxswitch
        return res
    
    @property
    def connected(self) -> bool:
        res = self._connected
        return res
    
    @connected.setter
    def connected(self, connected: bool):
        self._connected = connected
        if connected:
            self.logger.info('Setting the following RPi pins to LOW state')
            for attr, val in self.__dict__.items():
               if type(val) == dict and 'Switchpinout' in val.keys():
                    #print(f"{val['Name']}: {val['Switchpinout']}")
                    self.logger.info(f"{val['Name']}: {val['Switchpinout']}")
                    #GPIO.setup(val['Switchpinout'], GPIO.OUT)
                    #GPIO.output(val['Switchpinout'], False)
        else:
            self.logger.info('Cleaning the pinout.')
            #GPIO.cleanup()

    
    ## ROOF
    @property
    def roof_state(self) -> bool:
        res = self._roof['State']
        return res
    
    @roof_state.setter
    def roof_state(self, state: bool):
        self._roof['State'] = state
        self._roof['Value'] = float(state)
        #GPIO.output(self._roof['Switchpinout'], state)

    @property
    def roof_value(self) -> float:
        res = self._roof['Value']
        return res
    
    @roof_value.setter
    def roof_value(self, value: float):
        self._roof['Value'] = value
        self._roof['State'] = bool(value)
        #GPIO.output(self._roof['Switchpinout'], bool(state))

    ## WEATHER
    @property
    def weather_state(self) -> bool:
        res = self._weather['State']
        return res
    
    @weather_state.setter
    def weather_state(self, state: bool):
        self._weather['State'] = state
        self._weather['Value'] = float(state)
        #GPIO.output(self._weather['Switchpinout'], state)

    @property
    def weather_value(self) -> float:
        res = self._weather['Value']
        return res
    
    @weather_value.setter
    def weather_value(self, value: float):
        self._weather['Value'] = value
        self._weather['State'] = bool(value)
        #GPIO.output(self._weather['Switchpinout'], bool(state))

    ## MOUNT
    @property
    def mount_state(self) -> bool:
        res = self._mount['State']
        return res
    
    @mount_state.setter
    def mount_state(self, state: bool):
        self._mount['State'] = state
        self._mount['Value'] = float(state)
        #GPIO.output(self._mount['Switchpinout'], state)

    @property
    def mount_value(self) -> float:
        res = self._mount['Value']
        return res
    
    @mount_value.setter
    def mount_value(self, value: float):
        self._mount['Value'] = value
        self._mount['State'] = bool(value)
        #GPIO.output(self._mount['Switchpinout'], bool(state))

    ## CAMERA
    @property
    def camera_state(self) -> bool:
        res = self._camera['State']
        return res
    
    @camera_state.setter
    def camera_state(self, state: bool):
        self._camera['State'] = state
        self._camera['Value'] = float(state)
        #GPIO.output(self._camera['Switchpinout'], state)

    @property
    def camera_value(self) -> float:
        res = self._camera['Value']
        return res
    
    @camera_value.setter
    def camera_value(self, value: float):
        self._camera['Value'] = value
        self._camera['State'] = bool(value)
        #GPIO.output(self._camera['Switchpinout'], bool(state))
    
    ## ASTROPC
    @property
    def astropc_state(self) -> bool:
        res = self._astropc['State']
        return res
    
    @astropc_state.setter
    def astropc_state(self, state: bool):
        self._astropc['State'] = state
        self._astropc['Value'] = float(state)
        #GPIO.output(self._astropc['Switchpinout'], state)

    @property
    def astropc_value(self) -> float:
        res = self._astropc['Value']
        return res
    
    @astropc_value.setter
    def astropc_value(self, value: float):
        self._astropc['Value'] = value
        self._astropc['State'] = bool(value)
        #GPIO.output(self._astropc['Switchpinout'], bool(state))

    ## SECURITY
    @property
    def security_state(self) -> bool:
        res = self._security['State']
        return res
    
    @security_state.setter
    def security_state(self, state: bool):
        self._security['State'] = state
        self._security['Value'] = float(state)
        #GPIO.output(self._security['Switchpinout'], state)

    @property
    def security_value(self) -> float:
        res = self._security['Value']
        return res
    
    @security_value.setter
    def security_value(self, value: float):
        self._security['Value'] = value
        self._security['State'] = bool(value)
        #GPIO.output(self._security['Switchpinout'], bool(state))

    ## LIGHT
    @property
    def light_state(self) -> bool:
        res = self._light['State']
        return res
    
    @light_state.setter
    def light_state(self, state: bool):
        self._light['State'] = state
        self._light['Value'] = float(state)
        #GPIO.output(self._light['Switchpinout'], state)

    @property
    def light_value(self) -> float:
        res = self._light['Value']
        return res
    
    @light_value.setter
    def light_value(self, value: float):
        self._light['Value'] = value
        self._light['State'] = bool(value)
        #GPIO.output(self._light['Switchpinout'], bool(state))

    ## FLAT
    @property
    def flat_state(self) -> bool:
        res = self._flat['State']
        return res
    
    @flat_state.setter
    def flat_state(self, state: bool):
        self._flat['State'] = state
        self._flat['Value'] = float(state)
        #GPIO.output(self._flat['Switchpinout'], state)

    @property
    def flat_value(self) -> float:
        res = self._flat['Value']
        return res
    
    @flat_value.setter
    def flat_value(self, value: float):
        self._flat['Value'] = value
        self._flat['State'] = bool(value)
        #GPIO.output(self._flat['Switchpinout'], bool(state))
    
    #    
    # GET, SET METHOD (need more than self parameter)
    #

    def get_minswitchvalue(self, key) -> float:
        res = self._minswitchvalue
        return res
    
    def get_maxswitchvalue(self, key) -> float:
        res = self._maxswitchvalue
        return res
    
    def get_switchstep(self, key) -> float:
        res = self._switchstep
        return res
    
    def get_canwrite(self, key) -> bool:
        res = self._canwrite
        return res
    
    def get_switchdescription(self, id) -> str:
        key = 'Description'
        if id == 0:
            res = self._roof[key]
        elif id == 1:
            res = self._weather[key]
        elif id == 2:
            res = self._mount[key]
        elif id == 3:
            res = self._camera[key]
        elif id == 4:
            res = self._astropc[key]
        elif id == 5:
            res = self._security[key]
        elif id == 6:
            res = self._light[key]
        elif id == 7:
            res = self._flat[key]
        return res
    
    def get_switchname(self, id) -> str:
        key = 'Name'
        if id == 0:
            res = self._roof[key]
        elif id == 1:
            res = self._weather[key]
        elif id == 2:
            res = self._mount[key]
        elif id == 3:
            res = self._camera[key]
        elif id == 4:
            res = self._astropc[key]
        elif id == 5:
            res = self._security[key]
        elif id == 6:
            res = self._light[key]
        elif id == 7:
            res = self._flat[key]
        return res
    
    def set_switchname(self, id, value) -> None:
        key = 'Name'
        if id == 0:
            self._roof[key] = value
        elif id == 1:
            self._weather[key] = value
        elif id == 2:
            self._mount[key] = value
        elif id == 3:
            self._camera[key] = value
        elif id == 4:
            self._astropc[key] = value
        elif id == 5:
            self._security[key] = value
        elif id == 6:
            self._light[key] = value
        elif id == 7:
            self._flat[key] = value