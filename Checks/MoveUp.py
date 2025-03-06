from sys import argv
import DevicesOnLines
from time import sleep

mm = float(argv[1])

if 0 < mm < 20:
    motor = DevicesOnLines.Shaft(0, 0)
    k = 48/7  # (7 ob / 60sec * 1,25 mm/ ob)^-1
    seconds = mm * k
    motor.Up()
    sleep(seconds)
    motor.StopUp()
    sleep(0.01)
else:
    print("0 < mm < 20")

