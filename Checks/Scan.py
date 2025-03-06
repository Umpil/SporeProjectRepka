import pyfirmata
import datetime
import Devices
import DevicesOnLines
import DunoTable
from sys import argv
import os
if not os.path.exists("/dev/ttyACM0"):
    raise Exception("Arduino not connected")


Uno = pyfirmata.Arduino("/dev/ttyACM0")
Xstepper = Devices.NemaStepper(Uno, 800, 2, 5)
YStepper = Devices.NemaStepper(Uno, 800, 3, 6)
ZStepper = Devices.NemaStepper(Uno, 800, 4, 7)

if len(argv) == 1:
    PhotoWidth = 60
    PhotoHeight = 46
elif len(argv) == 3:
    PhotoWidth = int(argv[1])
    PhotoHeight = int(argv[2])
else:
    raise Exception("Unknown arguments. Needs w h")

Ligth = DevicesOnLines.Rele(19)
Cam = DevicesOnLines.Rele(0)
UsbOn = DevicesOnLines.Rele(18)

Stol = DunoTable.Table(Xstepper, YStepper, ZStepper, 1, UsbOn=UsbOn, Epin=8, PhotoWidth=PhotoWidth, PhotoHeight=PhotoHeight, XEnd=9, YEnd=10, Light=Ligth, Cam=Cam)


Stol.ScanNow(f"/home/admin/imagestable/self/{datetime.datetime.today().isoformat()}")
