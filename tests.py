import serial
import time
import pyfirmata2
import numpy as np


class L288N:
    def __init__(self, master: pyfirmata2.Arduino, pinMotorA1: int, pinMotorA2: int, pinMotorB1: int = None, pinMotorB2: int = None) -> None:
        self._master = master
        self._pinMotorA1 = self._master.get_pin(f"d:{pinMotorA1}:p")
        self._pinMotorA2 = self._master.get_pin(f"d:{pinMotorA2}:p")
        if pinMotorB1 and pinMotorB2:
            self.double = True
            self._pinMotorB1 = self._master.get_pin(f"d:{pinMotorB1}:p")
            self._pinMotorB2 = self._master.get_pin(f"d:{pinMotorB2}:p")
        else:
            self.double = False

    def StepClock(self, strenght: float, timeskip=0.003):
        if not 0 <= strenght <= 100:
            print("0 <= strenght <= 100")
            return
        value = float(strenght)
        self._pinMotorA1.write(value)
        time.sleep(timeskip)

    def StepClockWise(self, strenght: float, timeskip=0.003):
        if not 0 <= strenght <= 100:
            print("0 <= strenght <= 100")
            return
        value = float(strenght)
        self._pinMotorA2.write(value)
        time.sleep(timeskip)

    def Off(self):
        self._pinMotorA1.write(0)
        time.sleep(0.003)
        self._pinMotorA2.write(0)
        time.sleep(0.003)
        if self.double:
            self._pinMotorB1.write(0)
            time.sleep(0.003)
            self._pinMotorB2.write(0)


if __name__ == "__main__":
    PORT = pyfirmata2.Arduino.AUTODETECT
    board = pyfirmata2.Arduino(PORT)
    print("Set connection")
    time.sleep(1)
    frequency = 1400
    n = 1
    driver = L288N(board, 3, 5)
    revolution_before = n * 1400
    t_max = revolution_before / 163.33333333333333
    t_linspace, step = np.linspace(0, t_max, frequency+1, retstep=True)
    for t in t_linspace:
        driver.StepClock(np.sin(np.pi * (t/t_max)), step)
    driver.Off()
    # linspace = np.linspace(0, np.pi, denominant)
    # times, h = np.linspace(0, 9, denominant, retstep=True)
    # signal_strenght = [100*np.sin(x) for x in linspace] + [np.sin(np.pi)]
    # for sign in signal_strenght:
    #     driver.StepClock(sign, h)
    # time_on_one_ob = 8.571428
    # driver = L288N(board, 3, 5)
    # steps = int(time_on_one_ob / 0.003)
    # step = 1.0/float(steps)
    # dropp = np.linspace(0.0, np.pi, steps)
    #
    # strenghts = [100*np.sin(x) for x in dropp]
    #
    # print("Stepping clock")
    # for st in strenghts:
    #     driver.StepClock(st, step)
    #
    # time.sleep(3)
    # print("SteppingClockWise")
    # for st in strenghts:
    #     driver.StepClockWise(st, step)

    board.exit()

