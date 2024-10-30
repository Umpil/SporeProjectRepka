import time
import gpiod


class Motor:
    def __init__(self, StepsPerRevolution: int, SPin: int, DPin: int, EPin: int, Line: int = 1, Twist=False):
        self.StepsPerRevolution = StepsPerRevolution
        self.SpinNumber = SPin
        self.DPinNumber = DPin
        self.EPinNumber = EPin

        chip = gpiod.chip(Line)
        self.Spin = chip.get_line(SPin)
        config = gpiod.line_request()
        config.consumer = "StepPin"
        config.request_type = gpiod.line_request.DIRECTION_OUTPUT
        self.Spin.request(config)

        self.Spin.set_value(0)
        time.sleep(0.01)

        self.Dpin = chip.get_line(DPin)
        config = gpiod.line_request()
        config.consumer = "DirectionPin"
        config.request_type = gpiod.line_request.DIRECTION_OUTPUT
        self.Dpin.request(config)

        self.Dpin.set_value(0)
        time.sleep(0.01)

        self.Epin = chip.get_line(EPin)
        config = gpiod.line_request()
        config.consumer = "EnablePin"
        config.request_type = gpiod.line_request.DIRECTION_OUTPUT
        self.Epin.request(config)

        self.Epin.set_value(1)
        time.sleep(0.01)

        self.StepDelay = 3000

        if Twist:
            chip0 = gpiod.chip(0)
            self.MS1 = chip0.get_line(2)
            config = gpiod.line_request()
            config.consumer = "MS1PIN"
            config.request_type = gpiod.line_request.DIRECTION_OUTPUT
            self.MS1.request(config)

            self.MS1.set_value(1)
            time.sleep(0.01)

            self.MS2 = chip0.get_line(3)
            config = gpiod.line_request()
            config.consumer = "MS2PIN"
            config.request_type = gpiod.line_request.DIRECTION_OUTPUT
            self.MS2.request(config)

            self.MS2.set_value(1)
            time.sleep(0.01)

            self.MS3 = chip0.get_line(11)
            config = gpiod.line_request()
            config.consumer = "MS3PIN"
            config.request_type = gpiod.line_request.DIRECTION_OUTPUT
            self.MS3.request(config)

            self.MS3.set_value(1)
            time.sleep(0.01)

    def SetSpeed(self, whatspeed: int) -> int:
        self.StepDelay = int(60 * 1000 * 1000 / self.StepsPerRevolution / whatspeed)
        return self.StepDelay

    def Step(self, steps: int):
        stepstogo = abs(steps)
        if steps >= 0:
            self.Dpin.set_value(0)
            time.sleep(0.01)
        else:
            self.Dpin.set_value(1)
            time.sleep(0.01)
        self.Epin.set_value(0)
        time.sleep(0.01)
        for i in range(stepstogo):
            self.Spin.set_value(1)
            time.sleep(self.StepDelay * 10**(-6))
            self.Spin.set_value(0)
            time.sleep(0.000001)

        self.Epin.set_value(1)
        time.sleep(0.01)


class Rele:
    def __init__(self, Pin: int, Line: int = 1):
        self.PinNumber = Pin
        chip = gpiod.chip(Line)
        self.Pin = chip.get_line(Pin)
        config = gpiod.line_request()
        config.consumer = "StepPin"
        config.request_type = gpiod.line_request.DIRECTION_OUTPUT
        self.Pin.request(config)

        self.Pin.set_value(0)
        time.sleep(0.01)

    def Open(self):
        self.Pin.set_value(1)
        time.sleep(0.01)

    def Close(self):
        self.Pin.set_value(0)
        time.sleep(0.01)

    def __bool__(self):
        return True

# InputVent = Rele(10)
# OutputVent = Rele(8)
# FilterVent = Rele(7)
# Pomp = Rele(9)
#
# Pomp.Open()
# time.sleep(5)
#
# Pomp.Close()
# time.sleep(5)
#
# FilterVent.Open()
# time.sleep(5)
#
# FilterVent.Close()
# time.sleep(5)
#
# InputVent.Open()
# time.sleep(5)
#
# InputVent.Close()
# time.sleep(5)
#
# OutputVent.Open()
# time.sleep(5)
#
# OutputVent.Close()
# time.sleep(5)


