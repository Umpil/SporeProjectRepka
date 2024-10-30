import time
import serial
import pyfirmata

from Devices import Pomp, NemaStepper, Ventile
from Encoders import EncoderAS5600
from DunoTable import Table
import configparser


config = configparser.ConfigParser()
config.read("config.ini")

# ENCODER CONSTANTS
# DISTANCES IN MILLIMETERS
CONVERSION = 360 / 4096
TRESHOLD = 20

# ENCODER
Encod = EncoderAS5600()
StartAngle = Encod.GetRawAngle()

# DISTANCES
RollerRadius = 18
DISTANCE_PYRGING = 100
DISTANCE_SCANNING = 210

AnglePyrging, RotationsPyrging = EncoderAS5600.RotationsCount(DISTANCE_PYRGING, RollerRadius)
AngleScanning, RotationsScanning = EncoderAS5600.RotationsCount(DISTANCE_SCANNING, RollerRadius)


try:
    TimeSpraying = int(config["User"]["TimeSpraying"])
except:
    TimeSpraying = int(config["DEFAULT"]["TimeSpraying"])
TimeSpraying = 300
try:
    TimePyrging = int(config["User"]["TimePyrging"])
except:
    TimePyrging = int(config["DEFAULT"]["TimePyrging"])
TimePyrging = 10

try:
    TimeRecall = int(config["User"]["TimeRecall"])
except:
    TimeRecall = int(config["DEFAULT"]["TimeRecall"])

try:
    Area = config["User"]["Area"]
except:
    Area = config["DEFAULT"]["Area"]

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
arduinoUno = pyfirmata.Arduino("/dev/ttyUSB0")
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


# MILLIMETERS ON PHOTO
MMHeight = 0.56
MMWidth = 0.68

PhotoWidth = 15
PhotoHeight = 15

# TABLE
Stol = Table(Xstepper, YStepper, ZStepper, 1, Epin=EnablePin, PhotoWidth=PhotoWidth, PhotoHeight=PhotoHeight)


# REVOLUTIONS
StepsPerRevolutionMEGA = 800

# ARDUINO MEGA 2560
arduinoMega = pyfirmata.ArduinoMega("/dev/ttyUSB2")
time.sleep(2)

# ARDUINO MEGA 2560 PINS

# TWIST STEPPERS
FirstStepperPinS = 25
FirstStepperPinD = 27
FirstStepperPinE = 23

SecondStepperPinS = 24
SecondStepperPinD = 26
SecondStepperPinE = 22

#TwistStepper = TwoSteppersAsOne(arduinoMega, 800, FirstStepperPinS, FirstStepperPinD, FirstStepperPinE, SecondStepperPinS, SecondStepperPinD, SecondStepperPinE)
TwistStepper = NemaStepper(arduinoMega, 200, SecondStepperPinS, SecondStepperPinD, SecondStepperPinE)
#TwistStepper = NemaStepper(arduinoMega, 800, FirstStepperPinS, FirstStepperPinD, FirstStepperPinE)
TwistStepper.SetSpeed(20)
TwistStepperSteps = 2
TwistStepperStepsEnd = 2

# LIFT STEPPER
LiftStepperPinS = 23
LiftStepperPinD = 25
LiftStepperPinE = 27
LiftStepperSteps = 1320
LiftStepper = NemaStepper(arduinoMega, StepsPerRevolutionMEGA, LiftStepperPinS, LiftStepperPinD)
LiftStepper.SetSpeed(50)

# OUTPUT VENTILE
OutputVentilePin = 46
OutputVentile = Ventile(arduinoMega, OutputVentilePin)

# INPUT VENTILE
InputVentilePin = 48
InputVentile = Ventile(arduinoMega, InputVentilePin)

# FILTER VENTILE
FilterVentilePin = 42
FilterVent = Ventile(arduinoMega, FilterVentilePin)

# POMP
PompPin = 44
Pompa = Pomp(arduinoMega, PompPin)


print("FisrtMove")
# FIRST MOVE
rotations = 0
angle = StartAngle
time.sleep(0.05)
print(angle)
while rotations < RotationsPyrging:
    while angle < TRESHOLD:
        TwistStepper.Step(TwistStepperSteps)
        angle = Encod.GetAngle()

    while angle > TRESHOLD:
        TwistStepper.Step(TwistStepperSteps)
        angle = Encod.GetAngle()

    while angle < StartAngle:
        TwistStepper.Step(TwistStepperSteps)
        angle = Encod.GetAngle()

    rotations += 1


if angle + AnglePyrging <= 4095:
    angle_to_go = angle + AnglePyrging
    while abs(angle - angle_to_go) > TRESHOLD:
        print(angle)
        TwistStepper.Step(TwistStepperSteps)
        angle = Encod.GetAngle()

else:
    print("More 4096")
    angle_to_go = (angle + AnglePyrging) % 4096
    while angle < TRESHOLD:
        TwistStepper.Step(TwistStepperSteps)
        angle = Encod.GetAngle()
    print(">Trehold")
    while angle > TRESHOLD:
        print(angle)
        TwistStepper.Step(TwistStepperSteps)
        angle = Encod.GetAngle()
    print("go to angle")
    while abs(angle - angle_to_go) > TRESHOLD:
        print(angle)
        TwistStepper.Step(TwistStepperSteps)
        angle = Encod.GetAngle()

time.sleep(0.05)
print("Lift down")
LiftStepper.Step(LiftStepperSteps)
time.sleep(0.05)

print("SecondMove")
# SECOND MOVE
print("In Open")
InputVentile.Open()
time.sleep(0.05)
print("Out Open")
OutputVentile.Open()
time.sleep(0.05)
Pompa.Start()
time.sleep(0.05)
# WAITING TO SPRAYING
N = 10
for i in range(N):
    time.sleep(TimeSpraying/10)
    Pompa.Stop()
    time.sleep(0.05)
    Pompa.Start()
    time.sleep(0.05)

print("Pomp Stop")
Pompa.Stop()
time.sleep(0.05)

# THIRD MOVE
print("ThirdMove")
print("In Close")
InputVentile.Close()
time.sleep(0.05)
print("Filter Open")
FilterVent.Open()
time.sleep(0.05)

print("Pomp Start")
Pompa.Start()
time.sleep(0.05)
time.sleep(TimePyrging)
print("Pomp Stop")
Pompa.Stop()
time.sleep(0.05)
print("Out CLose")
OutputVentile.Close()
time.sleep(0.05)
print("Fil Close")
FilterVent.Close()
time.sleep(0.05)

print("Lift up")
LiftStepper.Step(-LiftStepperSteps)
time.sleep(0.05)

print("FourthMove")
# FOURTH MOVE
rotations = 0
StartAngle = angle
time.sleep(0.05)
while rotations < RotationsScanning:
    while angle < TRESHOLD:
        TwistStepper.Step(TwistStepperSteps)
        angle = Encod.GetAngle()

    while angle > TRESHOLD:
        TwistStepper.Step(TwistStepperSteps)
        angle = Encod.GetAngle()

    while angle < StartAngle:
        TwistStepper.Step(TwistStepperSteps)
        angle = Encod.GetAngle()

    rotations += 1

if angle + AngleScanning <= 4095:
    angle_to_go = angle + AngleScanning
    while abs(angle - angle_to_go) > TRESHOLD:
        TwistStepper.Step(TwistStepperSteps)
        angle = Encod.GetAngle()

else:
    angle_to_go = angle + AngleScanning % 4096
    while angle < TRESHOLD:
        TwistStepper.Step(TwistStepperSteps)
        angle = Encod.GetAngle()

    while angle > TRESHOLD:
        TwistStepper.Step(TwistStepperSteps)
        angle = Encod.GetAngle()

    while abs(angle - angle_to_go) > TRESHOLD:
        TwistStepper.Step(TwistStepperSteps)
        angle = Encod.GetAngle()

time.sleep(0.05)

arduinoMega.exit()
# FIFTH MOVE




Stol.ScanNow("/home/admin/imagestable", "/home/admin/logs.txt", SendData=False)
arduinoUno.exit()

print("DONE")
