import json
import time

import pyfirmata
from Devices import NemaStepper
import requests
import subprocess
duno = pyfirmata.Arduino("/dev/ttyUSB0")
Xstepper = NemaStepper(duno, 200, 2, 5)
YStepper = NemaStepper(duno, 200, 3, 6)
ZStepper = NemaStepper(duno, 200, 4, 7)
EnablePin = duno.get_pin("d:8:o")
checks = {"repka_id": 1, "login": "1234"}

responce = requests.get("https://spore.k-lab.su/", json=json.dumps(checks))
data = responce.json()
EnablePin.write(0)
if int(data["MoveYU"]) > 0:
    print(data["MoveYU"])
    YStepper.Step(100)
    time.sleep(1)
if int(data["MoveYD"]) > 0:
    print(data["MoveYD"])
    YStepper.Step(-100)
    time.sleep(1)
if int(data["MoveXU"]) > 0:
    print(data["MoveXU"])
    Xstepper.Step(100)
    time.sleep(1)
if int(data["MoveXD"]) > 50:
    print(data["MoveXD"])
    Xstepper.Step(-100)
    time.sleep(1)
if int(data["MoveZU"]) > 0:
    print(data["MoveZU"])
    ZStepper.Step(100)
    time.sleep(1)
if int(data["MoveZD"]) > 0:
    print(data["MoveZD"])
    ZStepper.Step(-100)
    time.sleep(1)

EnablePin.write(1)
duno.exit()

subprocess.run(["sudo", "reboot"])
