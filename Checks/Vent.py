from sys import argv
import DevicesOnLines
from time import sleep

type_vent = argv[1]
secs = int(argv[2])


if 0 < secs < 20:
    if type_vent.lower() == "in" or type_vent.lower() == "i":
        Vent = DevicesOnLines.Rele(8)
        Vent.Open()
        sleep(secs)
        Vent.Close()
    elif type_vent.lower() == "out" or type_vent.lower() == "o":
        Vent = DevicesOnLines.Rele(9)
        Vent.Open()
        sleep(secs)
        Vent.Close()
    elif type_vent.lower() == "fil" or type_vent.lower() == "f":
        Vent = DevicesOnLines.Rele(10)
        Vent.Open()
        sleep(secs)
        Vent.Close()
    elif type_vent.lower() == "pomp" or type_vent.lower() == "p":
        Vent = DevicesOnLines.Rele(7)
        Vent.Open()
        sleep(secs)
        Vent.Close()
    else:
        print("Unknown vent")
else:
    print("0 < secs < 20")