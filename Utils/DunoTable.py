import time
import os
import pyfirmata.util
from Devices import NemaStepper
import cv2
import ultralytics
sign = -1


class Table:
    def __init__(self, XNema: NemaStepper, YNema: NemaStepper, ZNema: NemaStepper, CamIndex: int, PhotoWidth: int = 60,
                 PhotoHeight: int = 46, StepsHeight: int = 40, StepsWidth: int = 108, Epin: int = 0,
                 XEnd: int = None, YEnd: int = None, Light=None, Cam=None, UsbOn=None, Neuro=False):

        self.XNema = XNema
        self.YNema = YNema
        self.ZNema = ZNema

        self.PhotoWidth = PhotoWidth
        self.PhotoHeight = PhotoHeight

        self.StepsHeight = StepsHeight
        self.StepsWidth = StepsWidth

        self.CamIndex = CamIndex

        self.XNema.SetSpeed(60)
        self.YNema.SetSpeed(60)
        self.ZNema.SetSpeed(8)

        if Light:
            self.Light = Light

        if Cam:
            self.Cam = Cam

        if Epin:
            self.EPinNumber = Epin
            self.EPin = XNema.Master.get_pin(f'd:{self.EPinNumber}:o')
            self.EPin.write(1)

        if XEnd:
            self.XEndnumber = XEnd
            self.XEnd = XNema.Master.get_pin(f"d:{self.XEndnumber}:i")

        if YEnd:
            self.YEndNumber = YEnd
            self.YEnd = XNema.Master.get_pin(f"d:{self.YEndNumber}:i")

        if UsbOn:
            self.UsbOn = UsbOn

        self.Neuro = Neuro
        if Neuro:
            self.model = ultralytics.YOLO("/home/admin/PyFiles/AIModels/best.pt")

    def SendToPos(self):
        self.EPin.write(0)
        time.sleep(0.003)
        # center_pos = (2000, 4000)
        XPos = 2000 - (self.PhotoWidth // 2) * self.StepsWidth
        YPos = 4000 - (self.PhotoHeight // 2) * self.StepsHeight
        self.XNema.Step(sign*XPos)
        self.YNema.Step(sign*YPos)
        time.sleep(1)
        self.EPin.write(1)
        time.sleep(0.003)

    def ScanNow(self, PathsaveTo: str, LogFile=None, shaft=None):
        if self.UsbOn:
            self.UsbOn.Open()
            time.sleep(0.01)

        if not os.path.exists(PathsaveTo):
            os.mkdir(PathsaveTo)

        get_cam = False
        time_check = time.time()

        while time.time() - time_check < 2:
            if os.path.exists("/dev/video1"):
                get_cam = True
                break
        if not get_cam:
            time_check = time.time()
            while time.time() - time_check < 2:
                if os.path.exists("/dev/video1"):
                    get_cam = True
                    break
        if not get_cam:
            raise NoCam(shaft)

        self.Calibrate()
        time.sleep(2)
        Camera = cv2.VideoCapture(self.CamIndex)
        Camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        Camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
        time.sleep(1)
        photo_count = 1
        full_path_save_to = PathsaveTo + "/images"
        os.mkdir(full_path_save_to)

        if not os.path.exists(LogFile):
            open("/home/admin/imagestable/log.txt", "w", encoding='utf-8').close()
            time.sleep(0.01)

        if LogFile:
            file = open(LogFile, 'a', encoding='utf-8')
            time.sleep(0.01)
            file.write("Good Start\n")
            time.sleep(0.01)
            file.close()

        self.SendToPos()

        if self.Cam and self.Light:
            self.Cam.Open()
            self.Light.Open()

        time_start_scanning = time.time()
        for i in range(1, self.PhotoWidth + 1, 1):
            for j in range(1, self.PhotoHeight + 1, 1):
                _, frame = Camera.read()

                cv2.imwrite(full_path_save_to + f"/{photo_count}.jpg", cv2.flip(frame, 1))

                if LogFile:
                    file = open(LogFile, 'a', encoding='utf-8')
                    time.sleep(0.01)
                    file.write(f"Photo_{photo_count}:Succses\n")
                    time.sleep(0.01)
                    file.close()

                self.EPin.write(0)
                time.sleep(0.003)
                if i % 2 == 0:
                    self.YNema.Step(-sign*self.StepsHeight)
                else:
                    self.YNema.Step(sign*self.StepsHeight)
                self.EPin.write(1)
                time.sleep(0.5)
                photo_count += 1
            self.EPin.write(0)
            time.sleep(0.003)
            self.XNema.Step(sign*self.StepsWidth)
            self.EPin.write(1)
            time.sleep(0.003)
        Camera.release()
        if self.Cam and self.Light:
            self.Cam.Close()
            self.Light.Close()
            time.sleep(1.5)

        Camera.release()
        if self.UsbOn:
            self.UsbOn.Close()

        time_end_scanning = time.time()
        if LogFile:
            file = open(LogFile, 'a', encoding='utf-8')
            time.sleep(0.01)
            file.write(f"ScanTime:{time_end_scanning - time_start_scanning}\n")
            time.sleep(0.01)
            file.close()

        if shaft:
            shaft.Up()
            time.sleep(0.5)
            shaft.StopUp()

        biggest_photo = None
        if self.Neuro:
            Rust = 0
            Much = 0
            Pirena = 0
            biggest = -1
            for i in range(1, len(os.listdir(full_path_save_to)) + 1, 1):
                result = self.model(source=full_path_save_to + f"/{i}.jpg", save=False, show=False, verbose=False)
                for predict in result:
                    boxes = predict.boxes
                    if biggest < len(boxes):
                        biggest = len(boxes)
                        biggest_photo = full_path_save_to + f"/{i}.jpg"
                    for box in boxes:
                        if box.cls.nelement():
                            if int(box.cls.item()) == 0:
                                Rust += 1
                            elif int(box.cls.item()) == 1:
                                Much += 1
                            elif int(box.cls.item()) == 2:
                                Pirena += 1
            file = open(LogFile, 'a', encoding='utf-8')
            file.write(f"PredictTime:{time.time() - time_end_scanning}\n")
            file.write(f"Rust:{Rust}\n")
            file.write(f"Much:{Much}\n")
            file.write(f"Pirena:{Pirena}")
            file.close()
            result = {"Rust": Rust, "Much": Much, "Pirena": Pirena}
        else:
            result = {}
        ret_mass = []
        if biggest_photo:
            ret_mass.append(full_path_save_to + "/1.jpg")
            ret_mass.append(biggest_photo)
            for i in range(self.PhotoWidth, self.PhotoWidth * self.PhotoHeight - 1, self.PhotoWidth*self.PhotoHeight // 10):
                ret_mass.append(full_path_save_to + f"/{i}")
            ret_mass.append(full_path_save_to + f"/{self.PhotoWidth * self.PhotoHeight}.jpg")
            return ret_mass, result

        ret_mass.append(full_path_save_to + "/1.jpg")
        ret_mass.append(full_path_save_to + "/2.jpg")
        for i in range(self.PhotoWidth, self.PhotoWidth * self.PhotoHeight - 1,
                       self.PhotoWidth * self.PhotoHeight // 10):
            ret_mass.append(full_path_save_to + f"/{i}")
        ret_mass.append(full_path_save_to + f"/{self.PhotoWidth * self.PhotoHeight}.jpg")
        return ret_mass, result

    def Calibrate(self) -> None:
        it = pyfirmata.util.Iterator(self.XNema.Master)
        it.start()
        self.EPin.write(0)
        time.sleep(0.003)
        self.XEnd.read()
        self.YEnd.read()
        first_time = True
        time_start = time.time()
        while self.XEnd.read() and first_time:
            if time.time() - time_start > 50:
                first_time = False
                break
            self.XNema.Step(-sign*80)
            rd = self.XEnd.read()
            time.sleep(0.003)
            if not rd:
                break

        if not first_time:
            time.sleep(5)
            time_start = time.time()
            while self.XEnd.read():
                if time.time() - time_start > 50:
                    break
                self.XNema.Step(-sign*80)
                rd = self.XEnd.read()
                time.sleep(0.003)
                if not rd:
                    break

        first_time = True
        time_start = time.time()
        while self.YEnd.read() and first_time:
            if time.time() - time_start > 50:
                first_time = False
                break
            self.YNema.Step(-sign*80)
            rd = self.YEnd.read()
            time.sleep(0.003)
            if not rd:
                break

        if not first_time:
            time.sleep(5)
            time_start = time.time()
            while self.YEnd.read() and first_time:
                if time.time() - time_start > 50:
                    break
                self.YNema.Step(-sign*80)
                rd = self.YEnd.read()
                time.sleep(0.003)
                if not rd:
                    break

        self.EPin.write(1)
        time.sleep(0.003)


class NoCam(Exception):
    def __init__(self, shaft):
        if shaft:
            shaft.Up()
            time.sleep(0.5)
            shaft.StopUp()

    def __str__(self):
        return "USBCam"
