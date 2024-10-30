import time
import pyfirmata.util


class Ventile:
    def __init__(self, Master: pyfirmata.ArduinoMega, VentilePin: int):
        self.VentilePinNumber = VentilePin

        self.Opened = 0
        self.Master = Master

        self.VentilePin = self.Master.get_pin(f'd:{self.VentilePinNumber}:o')

        self.VentilePin.write(0)
        time.sleep(0.0003)

    def IsOpened(self) -> int:
        return self.Opened

    def Open(self) -> None:
        if not self.IsOpened():
            self.VentilePin.write(1)
            time.sleep(0.0003)
            self.Opened = 1

    def Close(self) -> None:
        if self.IsOpened():
            self.VentilePin.write(0)
            time.sleep(0.0003)
            self.Opened = 0


class NemaStepper:
    def __init__(self, Master: pyfirmata.Arduino or pyfirmata.ArduinoMega, StepsPerRevolution: int, SPin: int, DPin: int,
                 EPin: int = None):
        self.StepsPerRevolution = StepsPerRevolution
        self.SPinNumber = SPin
        self.DPinNumber = DPin
        self.EPinNumber = EPin

        self.Master = Master

        self.DPin = self.Master.get_pin(f'd:{self.DPinNumber}:o')
        self.SPin = self.Master.get_pin(f'd:{self.SPinNumber}:o')
        if EPin:
            self.Epin = self.Master.get_pin(f'd:{self.EPinNumber}:o')
        else:
            self.Epin = None

        if EPin:
            self.Epin.write(1)
            time.sleep(0.0003)
        self.SPin.write(0)
        time.sleep(0.0003)
        self.DPin.write(0)
        time.sleep(0.0003)

        self.StepDelay = 3000

    def SetSpeed(self, WhatSpeed: int) -> int:
        self.StepDelay = int(60 * 1000 * 1000 / self.StepsPerRevolution/WhatSpeed)
        return self.StepDelay

    def Step(self, StepsToMove: int, LeftOn: bool = False):
        if self.Epin:
            self.Epin.write(0)
        steps_left = abs(StepsToMove)
        if StepsToMove >= 0:
            self.DPin.write(0)
        else:
            self.DPin.write(1)

        for i in range(steps_left):
            self.SPin.write(1)
            time.sleep(self.StepDelay * 10**(-6))
            self.SPin.write(0)
            time.sleep(self.StepDelay * 10**(-6))

        if self.Epin and not LeftOn:
            self.Epin.write(1)
            time.sleep(0.0003)
        elif self.Epin and LeftOn:
            return self.Epin


class Pomp:
    def __init__(self, Master: pyfirmata.ArduinoMega, PompPin: int):
        self.PopmPinNumber = PompPin

        self.Master = Master

        self.PompPin = self.Master.get_pin(f'd:{self.PopmPinNumber}:o')
        self.PompPin.write(0)

        self.Running = 0

    def IsRunning(self):
        return self.Running

    def Start(self):
        if not self.IsRunning():
            self.PompPin.write(1)
            time.sleep(0.0003)
            self.Running = 1

    def Stop(self):
        if self.IsRunning():
            self.PompPin.write(0)
            time.sleep(0.0003)
            self.Running = 0


class TwoSteppersAsOne:
    def __init__(self, Master: pyfirmata.ArduinoMega, StepsPerRevolution: int,
                 FirstStepperPinS: int, FirstStepperPinD: int, FisrtStepperPinE: int, SecondStepperPinS: int,
                 SecondStepperPinD: int, SecondStepperPinE: int):

        self.Master = Master

        self.FirstStepperPinSNumber = FirstStepperPinS
        self.FirstStepperPinDNumber = FirstStepperPinD
        self.FirstStepperPinENumber = FisrtStepperPinE

        self.SecondStepperPinSNumber = SecondStepperPinS
        self.SecondStepperPinDNumber = SecondStepperPinD
        self.SecondStepperPinENumber = SecondStepperPinE

        self.FirstStepperPinS = self.Master.get_pin(f'd:{self.FirstStepperPinSNumber}:o')
        self.FirstStepperPinD = self.Master.get_pin(f'd:{self.FirstStepperPinDNumber}:o')
        self.FirstStepperPinE = self.Master.get_pin(f'd:{self.FirstStepperPinENumber}:o')

        self.SecondStepperPinS = self.Master.get_pin(f'd:{self.SecondStepperPinSNumber}:o')
        self.SecondStepperPinD = self.Master.get_pin(f'd:{self.SecondStepperPinDNumber}:o')
        self.SecondStepperPinE = self.Master.get_pin(f'd:{self.SecondStepperPinENumber}:o')

        self.FirstStepperPinE.write(1)
        time.sleep(0.0003)
        self.SecondStepperPinE.write(1)
        time.sleep(0.0003)

        self.FirstStepperPinD.write(0)
        time.sleep(0.0003)
        self.SecondStepperPinD.write(0)
        time.sleep(0.0003)

        self.FirstStepperPinS.write(0)
        time.sleep(0.0003)
        self.SecondStepperPinS.write(0)
        time.sleep(0.0003)

        self.StepDelay = 3000
        self.StepsPerRevolution = StepsPerRevolution

    def SetSpeed(self, WhatSpeed: int) -> int:
        self.StepDelay = int((60 * 1000 * 1000 / self.StepsPerRevolution)/ WhatSpeed)
        return self.StepDelay

    def Step(self, StepsToMove: int):
        steps_left = abs(StepsToMove)
        if StepsToMove >= 0:
            self.FirstStepperPinD.write(0)
            time.sleep(0.0003)
            self.SecondStepperPinD.write(1)
            time.sleep(0.0003)
        else:
            self.FirstStepperPinD.write(1)
            time.sleep(0.0003)
            self.SecondStepperPinD.write(0)
            time.sleep(0.0003)
        for i in range(steps_left):
            self.FirstStepperPinE.write(1)
            time.sleep(0.0003)
            self.SecondStepperPinE.write(0)
            time.sleep(0.0003)

            self.SecondStepperPinS.write(1)
            time.sleep((self.StepDelay * 10**(-6)) / 2)
            self.SecondStepperPinS.write(0)
            time.sleep((self.StepDelay * 10 ** (-6)) / 2)

            self.FirstStepperPinE.write(0)
            time.sleep(0.0003)
            self.SecondStepperPinE.write(1)
            time.sleep(0.0003)

            self.FirstStepperPinS.write(1)
            time.sleep((self.StepDelay * 10**(-6)) / 2)
            self.FirstStepperPinS.write(0)
            time.sleep((self.StepDelay * 10 ** (-6)) / 2)

        self.FirstStepperPinE.write(1)


class RunTwoAsOneBoard:
    def __init__(self, Master: pyfirmata.Arduino or pyfirmata.ArduinoMega, StepsPerRevolution: int, FirstStepperPinS: int,
                 FirstStepperPinD: int, SecondStepperPinS: int, SecondStepperPinD: int, SecondStepperPinE: int):
        self.Master = Master

        self.FirstStepperPinSNumber = FirstStepperPinS
        self.FirstStepperPinDNumber = FirstStepperPinD

        self.SecondStepperPinSNumber = SecondStepperPinS
        self.SecondStepperPinDNumber = SecondStepperPinD
        self.SecondStepperPinENumber = SecondStepperPinE

        self.FirstStepperPinS = self.Master.get_pin(f'd:{self.FirstStepperPinSNumber}:o')
        self.FirstStepperPinD = self.Master.get_pin(f'd:{self.FirstStepperPinDNumber}:o')
        self.SecondStepperPinS = self.Master.get_pin(f'd:{self.SecondStepperPinSNumber}:o')
        self.SecondStepperPinD = self.Master.get_pin(f'd:{self.SecondStepperPinDNumber}:o')
        self.SecondStepperPinE = self.Master.get_pin(f'd:{self.SecondStepperPinENumber}:o')

        self.SecondStepperPinE.write(1)

        self.FirstStepperPinD.write(0)
        self.SecondStepperPinD.write(0)

        self.StepDelay = 3000
        self.StepsPerRevolution = StepsPerRevolution

    def SetSpeed(self, WhatSpeed: int) -> int:
        self.StepDelay = int((60 * 1000 * 1000 / self.StepsPerRevolution) / WhatSpeed)
        return self.StepDelay

    def Step(self, StepsToMove: int):
        steps_left = abs(StepsToMove)
        if StepsToMove >= 0:
            self.FirstStepperPinD.write(0)
            self.SecondStepperPinD.write(1)
        else:
            self.FirstStepperPinD.write(0)
            self.SecondStepperPinD.write(1)
        for i in range(steps_left):
            self.SecondStepperPinE.write(0)
            time.sleep(0.0003)

            self.FirstStepperPinS.write(1)
            time.sleep((self.StepDelay / 1000000)/2)
            self.FirstStepperPinS.write(0)
            time.sleep(0.0003)

            time.sleep(0.0003)
            self.SecondStepperPinS.write(1)
            time.sleep((self.StepDelay/1000000)/2)
            self.SecondStepperPinS.write(0)
        self.SecondStepperPinE.write(1)
