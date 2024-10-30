import time
import pyfirmata2

from Devices import NemaStepper
from Encoders import EncoderAS5600
from DunoTable import Table
from DevicesOnLines import Rele
import configparser


def RotateTo(Distance, Treshold=20, RollerRadius=18):
    dun = pyfirmata2.Arduino("/dev/ttyUSB1")
    TwistMotor = NemaStepper(dun, 200, 2, 5)
    TwistMotor.SetSpeed(10)
    Angle, Rotations = EncoderAS5600.RotationsCount(Distance, RollerRadius)
    Encod = EncoderAS5600()
    StartAngle = Encod.GetAngle()

    TRESHOLD = Treshold
    rotations = 0
    angle = StartAngle
    Epi = dun.get_pin("d:8:o")

    Epi.write(0)

    while rotations < Rotations:
        print(f"Rotating {Rotations} times")
        while angle < TRESHOLD:
            TwistMotor.Step(2)
            angle = Encod.GetAngle()

        while angle > TRESHOLD:
            TwistMotor.Step(2)
            angle = Encod.GetAngle()

        while angle < StartAngle:
            TwistMotor.Step(2)
            angle = Encod.GetAngle()

        rotations += 1

    if angle + Angle <= 4095:
        print("<= 4095")
        angle_to_go = angle + Angle
        while abs(angle - angle_to_go) > TRESHOLD:
            print(angle)
            TwistMotor.Step(2)
            angle = Encod.GetAngle()

    else:
        print("> 4095")
        angle_to_go = (angle + Angle) % 4096
        while angle < TRESHOLD:
            TwistMotor.Step(2)
            angle = Encod.GetAngle()
        print(">Treshold")
        while angle > TRESHOLD:
            print(angle)
            TwistMotor.Step(2)
            angle = Encod.GetAngle()
        print("Go to end angle")
        while abs(angle - angle_to_go) > TRESHOLD:
            print(angle)
            TwistMotor.Step(2)
            angle = Encod.GetAngle()
    Epi.write(1)
    dun.exit()


config = configparser.ConfigParser()
config.read("config.ini")

# ENCODER DISTANCES

DISTANCE_PYRGING = 100
DISTANCE_SCANNING = 155

# responce = requests.get(serianumber.url, {"type_": "get", "repkaid": serianumber.repka_id, "login": serianumber.login,
#                                           "timespraying": TimeSpraying, "timepyrging": TimePyrging, "area": Area,
#                                           "recalltime": TimeRecall}).json()
# if responce["Area"] != Area:
#     config["User"]["area"] = responce["area"]
#
# if int(responce["timespraying"]) != TimeSpraying:
#     config["User"]["TimeSpraying"] = responce["timespraying"]
#
# if int(responce["TimePyrging"]) != TimePyrging:
#     config["User"]["timepyrging"] = responce["timepyrging"]
#
# if int(responce["recalltime"]) != TimeRecall:
#     config["User"]["TimeRecall"] = responce["recalltime"]


# REVOLUTIONS
StepsPerRevolutionUNO = 200

# ARDUINO UNO
arduinoUno = pyfirmata2.Arduino("/dev/ttyUSB0")
time.sleep(2)

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
time.sleep(2)

# REVOLUTIONS

InputVent = Rele(7)
OutputVent = Rele(8)
FilterVent = Rele(10)
Pomp = Rele(9)
print("FisrtMove")
# FIRST MOVE
RotateTo(DISTANCE_PYRGING)

print("Lift down")
duno = pyfirmata2.ArduinoMega("/dev/ttyUSB1")
time.sleep(2)
Lifter = NemaStepper(duno, 200, 3, 6)
Lifter.SetSpeed(20)
Ep = duno.get_pin("d:8:o")

Ep.write(0)
time.sleep(0.05)
Lifter.Step(-1000)
time.sleep(0.05)
Ep.write(1)
time.sleep(2.5)
duno.exit()
time.sleep(5)


# SECOND MOVE
print("SecondMove")

print("In Open")
InputVent.Open()
time.sleep(0.7)

print("Out Open")
OutputVent.Open()
time.sleep(0.7)

print("PompStart")
Pomp.Open()
time.sleep(0.7)

print("WaitToSpray")
time.sleep(300)

print("Pomp Stop")
Pomp.Close()
time.sleep(0.7)

# THIRD MOVE
print("ThirdMove")

print("In Close")
InputVent.Close()
time.sleep(0.7)

print("Filter Open")
FilterVent.Open()
time.sleep(0.7)

print("Pomp Start")
Pomp.Open()

print("WaitToPyrge")
time.sleep(10)

print("Pomp Stop")
Pomp.Close()
time.sleep(0.7)

print("Out CLose")
OutputVent.Close()
time.sleep(0.7)

print("Fil Close")
FilterVent.Close()
time.sleep(0.7)

print("Lift up")
duno = pyfirmata2.Arduino("/dev/ttyUSB1")
time.sleep(2)
Lifter = NemaStepper(duno, 200, 3, 6)
Lifter.SetSpeed(50)
Ep = duno.get_pin("d:8:o")

Ep.write(0)
time.sleep(0.05)
Lifter.Step(900)
time.sleep(0.05)
Ep.write(1)
duno.exit()


# FOURTH MOVE
print("FourthMove")

RotateTo(DISTANCE_SCANNING)

# FIFTH MOVE
print("FifthMove")
arduinoUno = pyfirmata2.Arduino("/dev/ttyUSB0")
time.sleep(2)
Xstepper = NemaStepper(arduinoUno, StepsPerRevolutionUNO, XStepperPinS, XStepperPinD)
YStepper = NemaStepper(arduinoUno, StepsPerRevolutionUNO, YSteppperPinS, YStepperPinD)
ZStepper = NemaStepper(arduinoUno, StepsPerRevolutionUNO, ZStepperPinS, ZStepperPinD)
Stol = Table(Xstepper, YStepper, ZStepper, 1, Epin=EnablePin, PhotoWidth=PhotoWidth, PhotoHeight=PhotoHeight)
Stol.ScanNow("/home/admin/imagestable", "/home/admin/logs.txt", SendData=False)

arduinoUno.exit()

print("DONE")
