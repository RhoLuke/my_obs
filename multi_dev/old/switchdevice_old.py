
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
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

#from logging import Logger

class SwitchDevice:

    def __init__(self)#, logger: Logger):
        self.name: str = 'SwitchDevice'
        #self.logger = logger
        self._connected: bool = False

        # Device properties
        self._maxswitch: int = 5
        self._canwrite: bool = True
        self._minswitchvalue: float = 0.0
        self._maxswitchvalue: float = 1.0
        self._switchstep: int = 1.0

        # Switch porperty
        self._roof: dict ={'Name': 'Roof',
                           'Id': 0,
                           'Description': 'Roof power',
                           'Switchpinout': 21,
                           'State': False,
                           'Value': 0.0}
        
        self._mount: dict ={'Name': 'Telescope mount',
                            'Id': 1,
                           'Description': 'Telescope mount power',
                           'Switchpinout': 16,
                           'State': False,
                           'Value': 0.0}
        
        self._aux1: dict ={'Name': 'Aux1',
                             'Id': 2,
                           'Description': 'Ancillary dev1',
                           'Switchpinout': 12,
                           'State': False,
                           'Value': 0.0}
        
        self._aux2: dict ={'Name': 'Aux2',
                              'Id': 3,
                               'Description': 'Ancillary dev2',
                               'Switchpinout': 18,
                               'State': True,
                               'Value': 0.0}
        
        self._light: dict ={'Name': 'Light',
                            'Id': 4,
                           'Description': 'Light power',
                           'Switchpinout': 7,
                           'State': False,
                           'Value': 0.0}
        
        self._flat: dict ={'Name': 'Flat box',
                           'Id': 5,
                           'Description': 'Flat box power',
                           'Switchpinout': 8,
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

    
    ## ROOF
    @property
    def roof_state(self) -> bool:
        res = self._roof['State']
        return res
    
    @roof_state.setter
    def roof_state(self, state: bool):
        self._roof['State'] = state
        self._roof['Value'] = state
        GPIO.output(self._roof['Switchpinout'], not state)

    @property
    def roof_value(self) -> float:
        res = self._roof['Value']
        return res
    
    @roof_value.setter
    def roof_value(self, value: float):
        self._roof['Value'] = value
        self._roof['State'] = bool(value)
        GPIO.output(self._roof['Switchpinout'], not bool(value))

    ## MOUNT
    @property
    def mount_state(self) -> bool:
        res = self._mount['State']
        return res
    
    @mount_state.setter
    def mount_state(self, state: bool):
        self._mount['State'] = state
        self._mount['Value'] = float(state)
        GPIO.output(self._mount['Switchpinout'], not state)

    @property
    def mount_value(self) -> float:
        res = self._mount['Value']
        return res
    
    @mount_value.setter
    def mount_value(self, value: float):
        self._mount['Value'] = value
        self._mount['State'] = bool(value)
        GPIO.output(self._mount['Switchpinout'], not bool(value))
        
    ## AUX1
    @property
    def aux1_state(self) -> bool:
        res = self._aux1['State']
        return not res
    
    @aux1_state.setter
    def aux1_state(self, state: bool):
        self._aux1['State'] = state
        self._aux1['Value'] = float(state)
        GPIO.output(self._aux1['Switchpinout'], not state)

    @property
    def aux1_value(self) -> float:
        res = self._aux1['Value']
        return res
    
    @aux1_value.setter
    def aux1_value(self, value: float):
        self._aux1['Value'] = value
        self._aux1['State'] = bool(value)
        GPIO.output(self._aux1['Switchpinout'], not bool(value))
        
    ## AUX2
    @property
    def aux2_state(self) -> bool:
        res = self._aux2['State']
        return res
    
    @aux2_state.setter
    def aux2_state(self, state: bool):
        self._aux2['State'] = state
        self._aux2['Value'] = float(state)
        GPIO.output(self._aux2['Switchpinout'], not state)

    @property
    def aux2_value(self) -> float:
        res = self._aux2['Value']
        return res
    
    @aux2_value.setter
    def aux2_value(self, value: float):
        self._aux2['Value'] = value
        self._aux2['State'] = bool(value)
        GPIO.output(self._aux2['Switchpinout'], not bool(value))

    ## LIGHT
    @property
    def light_state(self) -> bool:
        res = self._light['State']
        return res
    
    @light_state.setter
    def light_state(self, state: bool):
        self._light['State'] = state
        self._light['Value'] = state
        GPIO.output(self._light['Switchpinout'], not state)

    @property
    def light_value(self) -> float:
        res = self._light['Value']
        return res
    
    @light_value.setter
    def light_value(self, value: float):
        self._light['Value'] = value
        self._light['State'] = bool(value)
        GPIO.output(self._light['Switchpinout'], not bool(value))

    ## FLAT
    @property
    def flat_state(self) -> bool:
        res = self._flat['State']
        return res
    
    @flat_state.setter
    def flat_state(self, state: bool):
        self._flat['State'] = state
        self._flat['Value'] = float(state)
        GPIO.output(self._flat['Switchpinout'], not state)

    @property
    def flat_value(self) -> float:
        res = self._flat['Value']
        return res
    
    @flat_value.setter
    def flat_value(self, value: float):
        self._flat['Value'] = value
        self._flat['State'] = bool(value)
        GPIO.output(self._flat['Switchpinout'], not bool(value))
    
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
            res = self._mount[key]
        elif id == 2:
            res = self._aux1[key]
        elif id == 3:
            res = self._aux2[key]
        elif id == 4:
            res = self._light[key]
        elif id == 5:
            res = self._flat[key]
        return res
    
    def get_switchname(self, id) -> str:
        key = 'Name'
        if id == 0:
            res = self._roof[key]
        elif id == 1:
            res = self._mount[key]
        elif id == 2:
            res = self._aux1[key]
        elif id == 3:
            res = self._aux2[key]
        elif id == 4:
            res = self._light[key]
        elif id == 5:
            res = self._flat[key]
        return res
    
    def set_switchname(self, id, value) -> None:
        key = 'Name'
        if id == 0:
            self._roof[key] = value
        elif id == 1:
            self._mount[key] = value
        elif id == 2:
            self._aux1[key] = value
        elif id == 3:
            self._aux2[key] = value
        elif id == 4:
            self._light[key] = value
        elif id == 5:
            self._flat[key] = value

if __name__ == '__main__':
    swt_dev = SwitchDevice()
    for attr, val in swt_dev.__dict__.items():
        if type(val) == dict and 'Switchpinout' in val.keys():
            GPIO.setup(val['Switchpinout'], GPIO.OUT)
            GPIO.output(val['Switchpinout'], True)
    GPIO.cleanup()
    