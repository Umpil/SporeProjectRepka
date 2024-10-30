import os
import time
import pyfirmata
import pyfirmata.util
from DevicesOnLines import Rele

from Devices import NemaStepper
from DunoTable import Table

duno_port = "/dev/ttyACM0"
Uno = pyfirmata.Arduino(duno_port)


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

# RELAYS
Ligth = Rele(19)
Cam = Rele(18)
UsbOn = Rele(0)

# TABLE
Stol = Table(Xstepper, YStepper, ZStepper, 1, UsbOn=UsbOn, Epin=EnablePin, XEnd=9, YEnd=10, Light=Ligth, Cam=Cam, PhotoWidth=10, PhotoHeight=10)

Stol.ScanNow("/home/admin/imagestable/test", "/home/admin/imagestable/text.txt")