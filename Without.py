import os
import time
import pyfirmata

from Devices import NemaStepper
from Encoders import EncoderAS5600
from DunoTable import Table
from DevicesOnLines import Rele
from FullMega import MegaBoard
import datetime
import subprocess
import serianumber
import requests
import serial.tools.list_ports
ports = serial.tools.list_ports.comports()
mega_port = "/dev/ttyUSB0"
duno_port = "/dev/ttyACM0"


def RotateTo(Distance, Treshold=20, RollerRadius=18, Down=False):
    dun = MegaBoard(mega_port)
    time.sleep(1)
    dun.SetTwistSpeed(5)
    Angle, Rotations = EncoderAS5600.RotationsCount(Distance, RollerRadius)
    Encod = EncoderAS5600()
    StartAngle = Encod.GetAngle()

    TRESHOLD = Treshold
    rotations = 0
    angle = StartAngle

    while rotations < Rotations:
        print(f"Rotating {Rotations} times")
        while angle < TRESHOLD:
            dun.TwistStep(2)
            angle = Encod.GetAngle()

        while angle > TRESHOLD:
            dun.TwistStep(2)
            angle = Encod.GetAngle()

        while angle < StartAngle:
            dun.TwistStep(2)
            angle = Encod.GetAngle()

        rotations += 1

    if angle + Angle <= 4095:
        print("<= 4095")
        angle_to_go = angle + Angle
        while abs(angle - angle_to_go) > TRESHOLD:
            print(angle)
            dun.TwistStep(2)
            angle = Encod.GetAngle()

    else:
        print("> 4095")
        angle_to_go = (angle + Angle) % 4096
        while angle < TRESHOLD:
            dun.TwistStep(2)
            angle = Encod.GetAngle()
        print(">Treshold")
        while angle > TRESHOLD:
            print(angle)
            dun.TwistStep(2)
            angle = Encod.GetAngle()
        print("Go to end angle")
        while abs(angle - angle_to_go) > TRESHOLD:
            print(angle)
            dun.TwistStep(2)
            angle = Encod.GetAngle()

    if Down:
        dun.LiftStep(-400)
        time.sleep(1)
        dun.TwistStep(2)

    dun.exit()



# ENCODER DISTNCES
DISTANCE_PYRGING = 100
DISTANCE_SCANNING = 170

Area = "15x30"
TimeSpraying = 300
TimePyrging = 10
TimeRecall = 3600

# responce = requests.get(serianumber.url, {"type_": "get", "repkaid": serianumber.repka_id, "login": serianumber.login,
#                                           "timespraying": TimeSpraying, "timepyrging": TimePyrging, "area": Area,
#                                           "recalltime": TimeRecall}).json()
# try:
#     if responce["Area"] != Area:
#         Area = responce["Area"]
#         PhotoWidth = int(Area.split("x")[0])
#         PhotoHeight = int(Area.split("x")[1])
#         print(f"AREA : {PhotoWidth}, {PhotoHeight}")
#
#     if int(responce["timespraying"]) != TimeSpraying:
#         TimeSpraying = int(responce["timespraying"])
#         print(f"TimeSp: {TimeSpraying}")
#
#     if int(responce["TimePyrging"]) != TimePyrging:
#         TimePyrging = int(responce["timepyrging"])
#         print(f"TimePy: {TimePyrging}")
#
#     if int(responce["recalltime"]) != TimeRecall:
#         TimeRecall = int(responce["recalltime"])
#         print(f"TimeRecall: {TimeRecall}")
#
# except Exception as e:
#     print(e)

DISTANCE_PYRGING = 100
DISTANCE_SCANNING = 160

Area = "15x30"
TimeSpraying = 300
TimePyrging = 10
TimeRecall = 3600

# REVOLUTIONS
StepsPerRevolutionUNO = 200

# ARDUINO UNO
arduinoUno = pyfirmata.Arduino(duno_port)
time.sleep(1)

# ARDUINO UNO PINS
XStepperPinS = 2
XStepperPinD = 5

YSteppperPinS = 3
YStepperPinD = 6

ZStepperPinS = 4
ZStepperPinD = 7

EnablePin = 8

# STEPPERS
Xstepper = NemaStepper(arduinoUno, StepsPerRevolutionUNO, XStepperPinS, XStepperPinD)
YStepper = NemaStepper(arduinoUno, StepsPerRevolutionUNO, YSteppperPinS, YStepperPinD)
ZStepper = NemaStepper(arduinoUno, StepsPerRevolutionUNO, ZStepperPinS, ZStepperPinD)

# PHOTO TO TAKE

PhotoWidth = 15
PhotoHeight = 30

# TABLE
Stol = Table(Xstepper, YStepper, ZStepper, 1, Epin=EnablePin, PhotoWidth=PhotoWidth, PhotoHeight=PhotoHeight)

arduinoUno.exit()
time.sleep(1)
# REVOLUTIONS

print("Lift up")
duno = MegaBoard(mega_port)
time.sleep(1)

duno.LiftStep(400)
time.sleep(1)
duno.exit()


# FOURTH MOVE ###########################################################################
print("FourthMove")
time_strt = time.time()
RotateTo(DISTANCE_SCANNING-1, Down=True)
RotateTo(1, Treshold=20)




