import RPi.GPIO as GPIO
import time

# Imposta la numerazione dei pin in base al BCM
GPIO.setmode(GPIO.BCM)

# Definisci i pin per PUL+, PUL-, DIR+, DIR-, ENA+, e ENA-
PUL_PLUS = 24
#PUL_MINUS = 23
DIR_PLUS = 23
#DIR_MINUS = 15


# Imposta i pin come output
GPIO.setup(PUL_PLUS, GPIO.OUT)
#GPIO.setup(PUL_MINUS, GPIO.OUT)
GPIO.setup(DIR_PLUS, GPIO.OUT)
#GPIO.setup(DIR_MINUS, GPIO.OUT)

# Funzione per controllare il motore
def control_motor(direction, steps, delay):
    # Imposta la direzione (DIR+ e DIR-)
    GPIO.output(DIR_PLUS, direction)
    #GPIO.output(DIR_MINUS, not direction)

    # Genera impulsi (PUL+ e PUL-)
    for _ in range(steps):
        GPIO.output(PUL_PLUS, GPIO.HIGH)
        #GPIO.output(PUL_MINUS, GPIO.LOW)
        time.sleep(delay)
        GPIO.output(PUL_PLUS, GPIO.LOW)
        #GPIO.output(PUL_MINUS, GPIO.HIGH)
        time.sleep(delay)

# Esempio di utilizzo
#time.sleep(5)
try:
    control_motor(direction=True, steps=200, delay=0.0003)  # Esegui 200 passi in avanti con un ritardo di 1 ms tra i passi
    time.sleep(1)  # Pausa di 1 secondo
    control_motor(direction=False, steps=200, delay=0.0003)  # Esegui 200 passi all'indietro
except KeyboardInterrupt:
    pass
finally:
    # Pulisci i pin GPIO alla fine
    GPIO.cleanup()
