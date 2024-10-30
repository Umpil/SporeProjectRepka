import smbus
import math


class EncoderAS5600:
    def __init__(self):
        self.bus = smbus.SMBus(1)
        self.Address = 0x36
        self.RawAngleWire = 0x0C
        self.MagnitudeWire = 0x1B
        self.AngleWire = 0x0E
        self.MagnetWire = 0x0B
        self.TwoBytes = 2
        self.OneByte = 1

    def GetRawAngle(self) -> int:
        read_bytes = self.bus.read_i2c_block_data(self.Address, self.RawAngleWire, self.TwoBytes)
        return (read_bytes[0] << 8) | read_bytes[1]

    def ReadMagnitude(self) -> int:
        read_bytes = self.bus.read_i2c_block_data(self.Address, self.MagnitudeWire, self.TwoBytes)
        return (read_bytes[0] << 8) | read_bytes[1]

    def GetAngle(self) -> int:
        read_bytes = self.bus.read_i2c_block_data(self.Address, self.AngleWire, self.TwoBytes)
        return (read_bytes[0] << 8) | read_bytes[1]

    def CheckMagnet(self) -> int:
        read_bytes = self.bus.read_i2c_block_data(self.Address, self.MagnetWire, self.OneByte)
        value = read_bytes[0]
        if value == 0x37:
            return 0x01
        elif value == 0x27:
            return 0x02
        elif value == 0x17:
            return 0x00
        else:
            return -1

    @staticmethod
    def RotationsCount(Distancemm: int, RollLerRadiusmm: int):
        roller_lenght = 2 * math.pi * RollLerRadiusmm
        k = Distancemm / roller_lenght
        angle_count = int(k * 4096)
        return angle_count % 4096, angle_count // 4096

