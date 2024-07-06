import RPi.GPIO as GPIO
import time
import threading
import numpy as np

GPIO.setmode(GPIO.BCM)

class DM542T:
    
    def __init__(self, pull: int, dir: int):
        self._pull = pull
        self._dir = dir
        self._stop = threading.Event()
        self._min_speed = 0.05
        self._max_speed = 1./1000.0
        self._speed = 0.0
        self._tacc = 10.0
        self._ti = None
        self._isMoving = False
        self._isMinSpeed = False
    
    @property
    def pull(self):
        return self._pull
    @pull.setter
    def pull(self, pins: tuple):
        self._pull = pins
    
    @property
    def dir(self):
        return self._dir
    @dir.setter
    def dir(self, pins: tuple):
        self._dir = pins
    
    @property
    def isMoving(self):
        return self._isMoving
    
    def s_curve_delay(self, t):
        
        
        """
        Genera una S-curve per il profilo di accelerazione/de-accelerazione.

        Parameters:
        - t: Il tempo corrente.
        - t_acc: Il tempo desiderato per raggiungere/superare la velocità massima.
        - max_speed: La velocità massima desiderata.

        Returns:
        - L'intervallo di tempo (delay) corrente tra gli step.
        """
        
        a = 1 / (1 + np.exp(-10 * (t - self._tacc/2) / self._tacc))
        current_speed = a * 1/self._max_speed
        current_delay = 1 / current_speed if current_speed != 0 else 0  # Evita divisione per zero
        
        return current_delay
    
    # Funzione per controllare il motore
    def motor_go(self, direction: bool = True):
        
        self._isMoving = True
        
        # Imposta la direzione (DIR+ e DIR-)
        GPIO.output(self._dir, direction)
        
        self._ti = time.time()
        
        #Accelleration
        while not self._stop.is_set():
            
            self._speed = self.s_curve_delay(t=time.time()-self._ti)
                
            GPIO.output(self._pull, GPIO.HIGH)
            time.sleep(self._speed)
            GPIO.output(self._pull, GPIO.LOW)
            time.sleep(self._speed)
        
        return
        
    def stop(self):
        
        t_eval = time.time() - self._ti
        if t_eval > self._tacc:
            t_elapsed = self._tacc    
        else:
            t_elapsed = t_eval
        
        self._ti = time.time()
        
        #Decelleration
        while (self._speed <= self._min_speed):
            
            self._speed = self.s_curve_delay(t = t_elapsed-(time.time()-self._ti))
            
            GPIO.output(self._pull, GPIO.HIGH)
            time.sleep(self._speed)
            GPIO.output(self._pull, GPIO.LOW)
            time.sleep(self._speed)

        self._isMoving = False
    
    def motor_go_min_speed(self, direction):
        
        self._isMoving = True
        
        # Imposta la direzione (DIR+ e DIR-)
        GPIO.output(self._dir, direction)
        
        self._ti = time.time()
        
        self._speed = self._min_speed
        #Accelleration
        while not self._stop.is_set():
                            
            GPIO.output(self._pull, GPIO.HIGH)
            time.sleep(self._speed)
            GPIO.output(self._pull, GPIO.LOW)
        
#         self._isMoving = False
#         print('stopped')
        
    def halt(self, brutal = False):
        if not self._isMoving:
            pass
        else:
            self._stop.set()
            if not self._isMinSpeed and not brutal:
                self.stop()
            else:
                self._isMinSpeed = False
                self._isMoving = False
                
        
    def start(self, direction: bool, min_speed: bool = False):
        
        if self._isMoving:
            self.halt()
            while self._isMoving:
                pass
            time.sleep(1.0)
            
        if not min_speed:
            thread_go = threading.Thread(target=self.motor_go, name='motor_go',
                                      kwargs={"direction": direction})
        else:
            self._isMinSpeed = True
            thread_go = threading.Thread(target=self.motor_go_min_speed, name='motor_go_min_speed',
                                      kwargs={"direction": direction})
        
        self._stop.clear()
        thread_go.start()
        
#
if __name__ == '__main__':
    motor_pin = {'pull': 24, 'dir': 23}
    for key, val in motor_pin.items():
        GPIO.setup(val, GPIO.OUT)

    motor = DM542T(motor_pin['pull'], motor_pin['dir'])