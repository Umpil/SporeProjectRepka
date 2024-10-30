import pyfirmata
import time


class MegaBoard(pyfirmata.ArduinoMega):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.LeftStepperPinS = self.get_pin("d::o")
        # self.LeftStepperPinS.mode = pyfirmata.OUTPUT
        self.LeftStepperPinD = self.get_pin("d:48:o")
        # self.LeftStepperPinD.mode = pyfirmata.OUTPUT
        # self.LeftStepperPinE = self.get_pin("d:24:o")
        # self.LeftStepperPinS.write(0)
        #
        # time.sleep(0.00003)

        # self.LeftStepperPinE.write(1)
        # time.sleep(0.00003)

        self.RightStepperPinS = self.get_pin("d:26:o")
        self.RightStepperPinS.mode = pyfirmata.OUTPUT
        self.RightStepperPinD = self.get_pin("d:28:o")
        self.RightStepperPinD.mode = pyfirmata.OUTPUT
        self.RightStepperPinE = self.get_pin("d:24:o")
        self.RightStepperPinE.mode = pyfirmata.OUTPUT

        self.RightStepperPinS.write(0)
        time.sleep(0.00003)

        self.RightStepperPinE.write(1)
        time.sleep(0.00003)

        self.LiftStepperPinS = self.get_pin("d:36:o")
        self.LiftStepperPinD = self.get_pin("d:34:o")
        self.LiftStepperPinE = self.get_pin("d:30:o")

        self.LiftStepperPinS.write(0)
        time.sleep(0.00003)

        self.LiftStepperPinE.write(1)
        time.sleep(0.00003)

        self.Revolutions = 200
        self.TwistStepDelay = 30000
        self.LiftStepDelay = 15000

    def TwistStep(self, steps: int, LeftOn: bool):
        steps_to_go = abs(steps)
        if steps >= 0:
            #self.LeftStepperPinD.write(0)
            #time.sleep(0.00003)
            self.RightStepperPinD.write(1)
            self.LeftStepperPinD.write(0)
            time.sleep(0.00003)
        else:
            #self.LeftStepperPinD.write(1)
            #time.sleep(0.00003)
            self.LeftStepperPinD.write(1)
            self.RightStepperPinD.write(1)
            time.sleep(0.00003)

        # Включили  первый
        #self.LeftStepperPinE.write(0)
        #time.sleep(0.00003)

        # Включили второй
        self.RightStepperPinE.write(0)
        time.sleep(0.00003)

        for i in range(steps_to_go):
            # Первый прошагал, как и второй
            self.RightStepperPinS.write(1)
            time.sleep(self.TwistStepDelay * 10**(-6))
            self.RightStepperPinS.write(0)
            time.sleep(0.00003)

        #self.LeftStepperPinE.write(1)
        #time.sleep(0.00003)

        # Включили второй
        if not LeftOn:
            self.RightStepperPinE.write(1)
            time.sleep(0.00003)

    def LiftStep(self, steps: int):
        steps_to_go = abs(steps)
        if steps >= 0:
            self.LiftStepperPinD.write(0)
            time.sleep(0.00003)
        else:
            self.LiftStepperPinD.write(1)
            time.sleep(0.00003)

        self.LiftStepperPinE.write(0)
        time.sleep(0.00003)

        for i in range(steps_to_go):
            self.LiftStepperPinS.write(1)
            time.sleep(self.LiftStepDelay * 10**(-6))
            self.LiftStepperPinS.write(0)
            time.sleep(0.00003)

        self.LiftStepperPinE.write(1)
        time.sleep(0.00003)

    def SetTwistSpeed(self, RevPerMin: int) -> int:
        self.TwistStepDelay = int(60 * 1000 * 1000 / self.Revolutions / RevPerMin)
        return self.TwistStepDelay

    def SetLiftSpeed(self, RevPerMin: int) -> int:
        self.LiftStepDelay = int(60 * 1000 * 1000 / self.Revolutions / RevPerMin)
        return self.LiftStepDelay




