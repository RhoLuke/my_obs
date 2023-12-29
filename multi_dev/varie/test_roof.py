import time
import RPi.GPIO as GPIO
import dm542t
#from RpiMotorLib.RpiMotorLib import A4988Nema


GPIO.setmode(GPIO.BCM)

#PIN
open_pin = {
    'com': 'GND',
    'nc': 19,
    'no': 26
}

close_pin = {
    'com': 'GND',#5
    'nc': 11,
    'no': 0
}

for key_open, key_close in zip(open_pin, close_pin):
    if key_open == 'com' or key_close == 'com': continue
    GPIO.setup(open_pin[key_open], GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(close_pin[key_close], GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
# motor_pin = {# Now for A4988
#     'ms1':4,
#     'ms2':14,
#     'ms3':15,
#     'dirct':23,
#     'step':18,
# }
# 
# motor = A4988Nema(motor_pin['dirct'],
#                   motor_pin['step'],
#                   (motor_pin['ms1'],
#                    motor_pin['ms2'],
#                    motor_pin['ms3']),
#                   'A4988')

def read_sensor() -> (str, str):
    nc_open = GPIO.input(open_pin['nc'])
    no_open = GPIO.input(open_pin['no'])
    
    if nc_open == True and no_open == False:
        open_sensor = 'active'
    elif nc_open == False and no_open == True:
        open_sensor = 'non_active'
    else:
        open_sensor = 'not_working'
    
    nc_close = GPIO.input(close_pin['nc'])
    no_close = GPIO.input(close_pin['no'])
    
    if nc_close == True and no_close == False:
        close_sensor = 'active'
    elif nc_close == False and no_close == True:
        close_sensor = 'non_active'
    else:
        close_sensor = 'not_working'
    
    return (open_sensor, close_sensor)

# Imposta i pin come output
pull=(24,23)
dir=(18,4)

GPIO.setup(pull[0], GPIO.OUT)
GPIO.setup(pull[1], GPIO.OUT)
GPIO.setup(dir[0], GPIO.OUT)
GPIO.setup(dir[1], GPIO.OUT)

motor = dm542t.DM542T(dir=23, pull=24)
vel_max = 0.001
vel_min = 0.01
incr = 0.002
dirct = 1
while True:
    try:
        input()
        print(dirct)
        opens, closes = read_sensor()
        if opens != 'active':
            print('Activate open sensor')
            continue
        
        vel = vel_min
        while ((opens == 'active' or opens == 'non_active') and closes == 'non_active'):
            motor.motor_go(direction=dirct, steps=100, delay=vel)
            if vel-incr >= vel_max:
                vel -= incr
            opens, closes = read_sensor()
        
        motor.motor_go(direction=dirct, steps=500, delay=vel) #ENSURING THAT IT PASSED THE INTERMEDIATE SENSOR
        opens, closes = read_sensor()
        
        print('passed')
        while ((closes == 'non_active') and opens == 'non_active'):
            motor.motor_go(direction=dirct, steps=100, delay=vel_max)
            opens, closes = read_sensor()
        
        while(opens == 'non_active'):
            motor.motor_go(direction=dirct, steps=100, delay=vel)
            if vel+incr <= vel_min:
                vel += incr
            opens, closes = read_sensor()
        print('Cycle finished')
        dirct = int(not dirct)
    except KeyboardInterrupt:
        GPIO.cleanup()
        break
            
        
        
