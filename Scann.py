import time
from Devices import NemaStepper
from DevicesOnLines import Rele
import pyfirmata2
import cv2

StepsPerRevolutionUNO = 200

# ARDUINO UNO PINS
XStepperPinS = 2
XStepperPinD = 5

YSteppperPinS = 3
YStepperPinD = 6

ZStepperPinS = 4
ZStepperPinD = 7

EnablePin = 8


Xstepper = NemaStepper(Uno, StepsPerRevolutionUNO, XStepperPinS, XStepperPinD)
YStepper = NemaStepper(Uno, 400, YSteppperPinS, YStepperPinD)
ZStepper = NemaStepper(Uno, StepsPerRevolutionUNO, ZStepperPinS, ZStepperPinD)

# PHOTO TO TAKE

PhotoWidth = 15
PhotoHeight = 10

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

