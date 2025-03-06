import pyfirmata
import pyfirmata.util
from sys import argv
import Devices
import os
import time
motor_type = argv[1]
steps = int(argv[2])

if not os.path.exists("/dev/ttyACM0"):
    raise Exception("Arduino not connected")

if motor_type.lower() == "x":
    if -20000 < steps < 20000:
        duno = pyfirmata.Arduino("/dev/ttyACM0")
        motor = Devices.NemaStepper(duno, 800, 2, 5, 8)
        XEnd = duno.get_pin(f"d:{9}:i")
        it = pyfirmata.util.Iterator(duno)
        it.start()
        if steps < 0:
            sign = -1
        else:
            sign = 1
        while abs(steps) > 0:
            if not XEnd.read():
                break
            if steps < 100:
                motor.Step(sign*steps)
                steps -= sign*steps
            else:
                motor.Step(sign*100)
                steps -= sign*100

            rd = XEnd.read()
            time.sleep(0.003)
            if not rd:
                break
    else:
        print("For x motor min -20000, max 20000")

elif motor_type.lower() == "y":
    if -11800 < steps < 11800:
        duno = pyfirmata.Arduino("/dev/ttyACM0")
        motor = Devices.NemaStepper(duno, 800, 3, 6, 8)
        YEnd = duno.get_pin(f"d:{10}:i")
        it = pyfirmata.util.Iterator(duno)
        it.start()
        if steps < 0:
            sign = -1
        else:
            sign = 1
        while abs(steps) > 0:
            if not YEnd.read():
                break
            if abs(steps) < 100:
                motor.Step(sign*steps)
                steps -= sign*steps
            else:
                motor.Step(sign*100)
                steps -= sign*100

            rd = YEnd.read()
            time.sleep(0.003)
            if not rd:
                break
    else:
        print("For y motor min -11800 max 11800")

elif motor_type.lower() == "z":
    if -8000 < steps < 8000:
        duno = pyfirmata.Arduino("/dev/ttyACM0")
        motor = Devices.NemaStepper(duno, 800, 4, 7, 8)
        if steps < 0:
            sign = -1
        else:
            sign = 1
        while abs(steps) > 0:
            if abs(steps) < 100:
                motor.Step(sign * steps)
                steps -= sign*steps
            else:
                motor.Step(sign * 100)
                steps -= sign*100
    else:
        print("For z motor min 0 max 8000")

else:
    print("Unknown motor type")
