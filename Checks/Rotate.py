from sys import argv
from Utils import DevicesOnLines
from time import sleep

secs = float(argv[1])

if 0 < secs < 100:
    motor = DevicesOnLines.Rotator(21)
    motor.StartRotate()
    sleep(secs)
    motor.StopRotate()
    sleep(0.01)
else:
    print("0 < secs < 100")