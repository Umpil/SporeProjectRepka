import DevicesOnLines
from sys import argv
import time

if len(argv) == 1:
    TimePyrging = 60
elif len(argv) == 2:
    TimePyrging = int(argv[1])
    if not 0 < TimePyrging <= 300:
        raise Exception("0 < TimePyrging <= 300")
else:
    raise Exception("Unknown combination of arguments")

shaft_ = DevicesOnLines.Shaft(6, 2)
InputVent = DevicesOnLines.Rele(8)
OutputVent = DevicesOnLines.Rele(7)
Pomp = DevicesOnLines.Rele(10)

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
