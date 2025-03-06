import pyfirmata
import Devices
import DunoTable

Uno = pyfirmata.Arduino("/dev/ttyACM0")

Xstepper = Devices.NemaStepper(Uno, 800, 2, 5)
YStepper = Devices.NemaStepper(Uno, 800, 3, 6)
ZStepper = Devices.NemaStepper(Uno, 800, 4, 7)

Stol = DunoTable.Table(Xstepper, YStepper, ZStepper, 1, Epin=8, XEnd=9, YEnd=10)

Stol.Calibrate()
