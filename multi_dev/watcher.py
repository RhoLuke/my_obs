from weatherdevice import WeatherDevice
from ror_device import ROOF
from time import time, sleep
from threading import Thread, Event
from logging import Logger

class Watcher:
    
    def __init__(self, logger: Logger):
        self._logger = logger
        self._safectd: float = 60.0
        self._count_down: bool = False
        self._danger_cts: int = 5
        self._false_alarm_cts: int = 5
        self._evt = Event()
        self._roof = ROOF(logger=self._logger, master=True)
        self._wth = WeatherDevice(logger=self._logger)
    
    def start_watching(self):
        while not self._evt.is_set():
            if self._wth.__class__._sensors["RainRate"]['Value']:
                false_alarm = False
                c = 0
                cf = 0
                while (c <= self._danger_cts):
                    sleep(2)
                    if self._wth.__class__._sensors["RainRate"]['Value']:
                        c += 1
                    else:
                        cf += 1
                    if cf > self._false_alarm_cts:
                        false_alarm = True
                        break
                    
                if false_alarm:
                    continue
                
                sleep(self._safectd)
                if self._roof.__class__._state in [0, 2] and self._wth.__class__._sensors["RainRate"]['Value']:
                    self._roof.move_roof(False)
                    self._logger.warning("Watcher decide to take over and close the roof for safety reason.")
                
                if self._evt.is_set():
                    self._evt.clear()
                    return
            else:
                sleep(3)
                
    def stop_watching(self):
        self.__class._evt.set()
    
    def run(self):
        t1 = Thread(target=self.start_watching, name="watcher").start()