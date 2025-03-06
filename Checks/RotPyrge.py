import DevicesOnLines
import Encoders
from sys import argv
import time


def RotateTo(Distance, rotator: DevicesOnLines.Rotator, Treshold=20, RollerRadius=18):
    Angle, Rotations = Encoders.EncoderAS5600.RotationsCount(Distance, RollerRadius)
    Encod = Encoders.EncoderAS5600()
    StartAngle = Encod.GetAngle()

    TRESHOLD = Treshold
    rotations = 0
    angle = StartAngle
    rotator.StartRotate()
    time.sleep(0.001)
    while rotations < Rotations:
        while angle < TRESHOLD:
            angle = Encod.GetAngle()

        while angle > TRESHOLD:
            angle = Encod.GetAngle()

        while angle < StartAngle:
            angle = Encod.GetAngle()

        rotations += 1

    rotator.StopRotate()
    time.sleep(0.001)
    if angle + Angle <= 4095:
        angle_to_go = angle + Angle
        rotator.StartRotate()
        time.sleep(0.001)
        while abs(angle - angle_to_go) > TRESHOLD:
            angle = Encod.GetAngle()
        rotator.StopRotate()
        time.sleep(0.001)
    else:
        angle_to_go = (angle + Angle) % 4096
        rotator.StartRotate()
        time.sleep(0.001)
        while angle < TRESHOLD:
            angle = Encod.GetAngle()
        while angle > TRESHOLD:
            angle = Encod.GetAngle()
        while abs(angle - angle_to_go) > TRESHOLD:
            angle = Encod.GetAngle()
        rotator.StopRotate()
        time.sleep(0.001)


Pyrge_distance = 135
if len(argv) == 1:
    TimePyrging = 60
elif len(argv) == 2:
    TimePyrging = int(argv[1])
    if not 0 < TimePyrging <= 300:
        raise Exception("0 < TimePyrging <= 300")
else:
    raise Exception("Unknown combination of arguments")

rotator_ = DevicesOnLines.Rotator(21)
shaft_ = DevicesOnLines.Shaft(6, 2)
InputVent = DevicesOnLines.Rele(8)
OutputVent = DevicesOnLines.Rele(7)
Pomp = DevicesOnLines.Rele(10)
RotateTo(Pyrge_distance, rotator_)

shaft_.Down()
time.sleep(30.)
shaft_.StopDown()
time.sleep(0.001)

InputVent.Open()
time.sleep(0.7)

OutputVent.Open()
time.sleep(0.7)

Pomp.Open()
time.sleep(0.7)

time.sleep(TimePyrging)

Pomp.Close()
time.sleep(0.7)

InputVent.Close()
time.sleep(0.7)
OutputVent.Close()
time.sleep(0.7)

shaft_.Up()
time.sleep(30.)
shaft_.StopUp()
time.sleep(0.7)