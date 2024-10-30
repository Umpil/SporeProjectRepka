import os
import time
import pyfirmata
import pyfirmata.util

from Utils.Devices import NemaStepper
from Utils.Encoders import EncoderAS5600
from Utils.DunoTable import Table
from Utils.DevicesOnLines import Rele
from Utils.FullMega import MegaBoard
import datetime


def RotateTo(Distance, duno, Treshold=20, RollerRadius=18, Down=False):
    Angle, Rotations = EncoderAS5600.RotationsCount(Distance, RollerRadius)
    Encod = EncoderAS5600()
    StartAngle = Encod.GetAngle()

    TRESHOLD = Treshold
    rotations = 0
    angle = StartAngle
    while rotations < Rotations:
        while angle < TRESHOLD:
            duno.TwistStep(2)
            angle = Encod.GetAngle()

        while angle > TRESHOLD:
            duno.TwistStep(2)
            angle = Encod.GetAngle()

        while angle < StartAngle:
            duno.TwistStep(2)
            angle = Encod.GetAngle()

        rotations += 1

    if angle + Angle <= 4095:
        angle_to_go = angle + Angle
        while abs(angle - angle_to_go) > TRESHOLD:
            duno.TwistStep(2)
            angle = Encod.GetAngle()

    else:
        angle_to_go = (angle + Angle) % 4096
        while angle < TRESHOLD:
            duno.TwistStep(2)
            angle = Encod.GetAngle()
        while angle > TRESHOLD:
            duno.TwistStep(2)
            angle = Encod.GetAngle()
        while abs(angle - angle_to_go) > TRESHOLD:
            duno.TwistStep(2)
            angle = Encod.GetAngle()

    if Down:
        duno.LiftStep(605)
        time.sleep(1)


def Run(Area="15x30", TimePyrge=10, TimeSpraying=360, date=0):
    InitTime = time.time()
    mega_port = "/dev/ttyUSB0"
    duno_port = "/dev/ttyACM0"

    Mega = MegaBoard(mega_port)

    Uno = pyfirmata.Arduino(duno_port)

    # LOG FILE
    if date:
        date = datetime.datetime.fromtimestamp(date).replace(second=0, microsecond=0).isoformat()
    else:
        date = datetime.datetime.today().replace(second=0, microsecond=0).isoformat()
    filename = f"/home/admin/imagestable/{date}/log.txt"
    directory = f"/home/admin/imagestable/{date}"
    os.mkdir(directory)
    file = open(filename, "w", encoding="utf-8")
    try:
        # ENCODER DISTNCES
        DISTANCE_PYRGING = 135
        DISTANCE_SCANNING = 140
        Mega.SetTwistSpeed(5)

        # REVOLUTIONS
        StepsPerRevolutionUNO = 200

        # ARDUINO UNO PINS
        XStepperPinS = 2
        XStepperPinD = 5

        YSteppperPinS = 3
        YStepperPinD = 6

        ZStepperPinS = 4
        ZStepperPinD = 7

        EnablePin = 8

        # STEPPERS
        Xstepper = NemaStepper(Uno, StepsPerRevolutionUNO, XStepperPinS, XStepperPinD)
        YStepper = NemaStepper(Uno, 400, YSteppperPinS, YStepperPinD)
        ZStepper = NemaStepper(Uno, StepsPerRevolutionUNO, ZStepperPinS, ZStepperPinD)

        # PHOTO TO TAKE

        PhotoWidth = int(Area.split("x")[0])
        PhotoHeight = int(Area.split("x")[1])

        # RELAYS
        InputVent = Rele(8)
        OutputVent = Rele(7)
        FilterVent = Rele(9)
        Pomp = Rele(10)
        Ligth = Rele(19)
        Cam = Rele(18)
        UsbOn = Rele(0)

        # TABLE
        Stol = Table(Xstepper, YStepper, ZStepper, 1, UsbOn=UsbOn, Epin=EnablePin, PhotoWidth=PhotoWidth, PhotoHeight=PhotoHeight, XEnd=9, YEnd=10, Light=Ligth, Cam=Cam)
        # FIRST MOVE ###########################################################################

        file.write("Rotating to pyrge\n")
        file.close()
        RotatePyrgeTime = time.time()
        RotateTo(DISTANCE_PYRGING, Mega)

        SprayTime = time.time()
        file = open(filename, "a", encoding="utf-8")
        file.write("Go down\n")
        file.close()
        Mega.LiftStep(605)
        file = open(filename, "a", encoding="utf-8")
        file.write("Stand down\n")

        # SECOND MOVE ###########################################################################
        InputVent.Open()
        file.write("In Open\n")
        time.sleep(0.7)

        OutputVent.Open()
        file.write("Out Open\n")
        time.sleep(0.7)

        Pomp.Open()
        file.write("Pomp Start\n")
        file.write("Wait to spray\n")
        time.sleep(0.7)
        file.close()

        time.sleep(TimeSpraying)

        file = open(filename, "a", encoding="utf-8")
        file.write("Stop Spraying\n")

        Pomp.Close()
        file.write("Pomp Stop\n")
        time.sleep(0.7)

        # THIRD MOVE ###########################################################################
        PyrgeTime = time.time()
        InputVent.Close()
        file.write("In Closed\n")
        time.sleep(0.7)

        FilterVent.Open()
        file.write("Filter Open\n")
        time.sleep(0.7)

        Pomp.Open()
        file.write("Pomp Start\n")
        file.write("Wait to pyrge\n")
        file.close()

        time.sleep(TimePyrge)

        file = open(filename, "a", encoding="utf-8")

        Pomp.Close()
        file.write("Pomp Stop\n")
        file.write("Pyrge end\n")
        time.sleep(0.7)

        FilterVent.Close()
        file.write("Filter CLosed\n")
        time.sleep(0.7)

        OutputVent.Close()
        file.write("Out Closed\n")
        time.sleep(0.7)

        file.write("Go up\n")
        file.close()

        Mega.LiftStep(-600)
        file = open(filename, "a", encoding="utf-8")
        file.write("Stand up\n")

        # FOURTH MOVE ###########################################################################
        file.write("Rotating to scan\n")
        file.close()
        TimeRotateToScan = time.time()
        RotateTo(DISTANCE_SCANNING-1, Mega, Down=True)
        RotateTo(1, Mega, Treshold=20)
        Mega.RightStepperPinE.write(0)

        # FIFTH MOVE ###########################################################################
        file = open(filename, "a", encoding="utf-8")
        file.write("Start Scanning\n")
        file.close()
        TimeScan = time.time()
        photo, result = Stol.ScanNow(directory, filename)
        Uno.exit()

        Mega.LiftStep(-600)
        Mega.RightStepperPinE.write(1)
        Mega.exit()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    Run(Area="10x10", TimePyrge=50, TimeSpraying=120)
