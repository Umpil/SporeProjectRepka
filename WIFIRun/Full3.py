import os
import time
import pyfirmata
import pyfirmata.util
import requests

from Utils.serianumber import repka_id, url_upload_logimage, username, password, url_update_log
from Utils.Devices import NemaStepper
from Utils.Encoders import EncoderAS5600
from Utils.DunoTable import Table
from Utils.DevicesOnLines import Rele, Rotator, Shaft
import datetime
import subprocess
from PIL import Image
import base64
from io import BytesIO


TIME_TO_GO_DOWN = 30.
TIME_TO_GO_UP = 30.


def update_log(command: str, tsdate: str, etap_time: int or str):
    checks = {"username": username, "repka_id": repka_id, "password": password, "etap": command, "date": tsdate, "etap_time": etap_time}
    try:
        requests.post(url_update_log, json=checks)
    except Exception as e:
        print(e)


def RotateTo(Distance, rotator: Rotator, Treshold=20, RollerRadius=18, Down: Shaft = None):
    Angle, Rotations = EncoderAS5600.RotationsCount(Distance, RollerRadius)
    Encod = EncoderAS5600()
    StartAngle = Encod.GetAngle()

    TRESHOLD = Treshold
    rotations = 0
    angle = StartAngle
    rotator.StartRotate()
    time.sleep(0.001)
    while rotations < Rotations:
        while angle < TRESHOLD:
            angle = Encod.GetAngle()

        while angle > TRESHOLD:
            angle = Encod.GetAngle()

        while angle < StartAngle:
            angle = Encod.GetAngle()

        rotations += 1

    rotator.StopRotate()
    time.sleep(0.001)
    if angle + Angle <= 4095:
        angle_to_go = angle + Angle
        rotator.StartRotate()
        time.sleep(0.001)
        while abs(angle - angle_to_go) > TRESHOLD:
            angle = Encod.GetAngle()
        rotator.StopRotate()
        time.sleep(0.001)
    else:
        angle_to_go = (angle + Angle) % 4096
        rotator.StartRotate()
        time.sleep(0.001)
        while angle < TRESHOLD:
            angle = Encod.GetAngle()
        while angle > TRESHOLD:
            angle = Encod.GetAngle()
        while abs(angle - angle_to_go) > TRESHOLD:
            angle = Encod.GetAngle()
        rotator.StopRotate()
        time.sleep(0.001)

    if Down:
        Down.Down()
        time.sleep(TIME_TO_GO_DOWN)
        Down.StopDown()
        time.sleep(0.001)


def Run(Area="15x30", TimePyrge=10, TimeSpraying=360, date=0):
    InitTime = time.time()
    duno_port = "/dev/ttyACM0"

    Uno = pyfirmata.Arduino(duno_port)

    # LOG FILE
    if date:
        date = datetime.datetime.fromtimestamp(date).replace(second=0, microsecond=0).isoformat()
    else:
        date = datetime.datetime.today().replace(second=0, microsecond=0).isoformat()
    filename = f"/home/admin/imagestable/{date}/log.txt"
    directory = f"/home/admin/imagestable/{date}"
    os.mkdir(directory)
    file = open(filename, "w", encoding="utf-8")
    try:
        # ENCODER DISTNCES
        DISTANCE_PYRGING = 135
        DISTANCE_SCANNING = 140

        # REVOLUTIONS
        StepsPerRevolutionUNO = 800

        # ARDUINO UNO PINS
        XStepperPinS = 2
        XStepperPinD = 5

        YSteppperPinS = 3
        YStepperPinD = 6

        ZStepperPinS = 4
        ZStepperPinD = 7

        EnablePin = 8

        # STEPPERS
        Xstepper = NemaStepper(Uno, StepsPerRevolutionUNO, XStepperPinS, XStepperPinD)
        YStepper = NemaStepper(Uno, 400, YSteppperPinS, YStepperPinD)
        ZStepper = NemaStepper(Uno, StepsPerRevolutionUNO, ZStepperPinS, ZStepperPinD)

        # PHOTO TO TAKE

        PhotoWidth = int(Area.split("x")[0])
        PhotoHeight = int(Area.split("x")[1])

        # RELAYS
        InputVent = Rele(8)
        OutputVent = Rele(7)
        FilterVent = Rele(9)
        Pomp = Rele(10)
        Ligth = Rele(19)
        Cam = Rele(18)
        UsbOn = Rele(0)
        rotator_ = Rotator(0)
        shaft_ = Shaft(0, 0)

        # TABLE
        Stol = Table(Xstepper, YStepper, ZStepper, 1, UsbOn=UsbOn, Epin=EnablePin, PhotoWidth=PhotoWidth, PhotoHeight=PhotoHeight, XEnd=9, YEnd=10, Light=Ligth, Cam=Cam)
        update_log("Init", date, int(time.time() - InitTime))
        # FIRST MOVE ###########################################################################

        file.write("Rotating to pyrge\n")
        file.close()
        RotatePyrgeTime = time.time()
        RotateTo(DISTANCE_PYRGING, rotator_)
        update_log("RotSpray", date, int(time.time() - RotatePyrgeTime))

        SprayTime = time.time()
        file = open(filename, "a", encoding="utf-8")
        file.write("Go down\n")
        file.close()

        shaft_.Down()
        time.sleep(TIME_TO_GO_DOWN)
        shaft_.StopDown()
        time.sleep(0.001)

        file = open(filename, "a", encoding="utf-8")
        file.write("Stand down\n")

        # SECOND MOVE ###########################################################################
        InputVent.Open()
        file.write("In Open\n")
        time.sleep(0.7)

        OutputVent.Open()
        file.write("Out Open\n")
        time.sleep(0.7)

        Pomp.Open()
        file.write("Pomp Start\n")
        file.write("Wait to spray\n")
        time.sleep(0.7)
        file.close()

        time.sleep(TimeSpraying)
        update_log("Spray", date, int(time.time() - SprayTime))

        file = open(filename, "a", encoding="utf-8")
        file.write("Stop Spraying\n")

        Pomp.Close()
        file.write("Pomp Stop\n")
        time.sleep(0.7)

        # THIRD MOVE ###########################################################################
        PyrgeTime = time.time()
        InputVent.Close()
        file.write("In Closed\n")
        time.sleep(0.7)

        FilterVent.Open()
        file.write("Filter Open\n")
        time.sleep(0.7)

        Pomp.Open()
        file.write("Pomp Start\n")
        file.write("Wait to pyrge\n")
        file.close()

        time.sleep(TimePyrge)

        file = open(filename, "a", encoding="utf-8")

        Pomp.Close()
        file.write("Pomp Stop\n")
        file.write("Pyrge end\n")
        time.sleep(0.7)

        FilterVent.Close()
        file.write("Filter CLosed\n")
        time.sleep(0.7)

        OutputVent.Close()
        file.write("Out Closed\n")
        time.sleep(0.7)

        file.write("Go up\n")
        file.close()
        update_log("Pyrge", date, int(time.time() - PyrgeTime))

        shaft_.Up()
        time.sleep(TIME_TO_GO_UP)
        shaft_.StopUp()
        time.sleep(0.001)

        file = open(filename, "a", encoding="utf-8")
        file.write("Stand up\n")

        # FOURTH MOVE ###########################################################################
        file.write("Rotating to scan\n")
        file.close()
        TimeRotateToScan = time.time()
        RotateTo(DISTANCE_SCANNING-1, rotator_, Down=shaft_)
        RotateTo(1, rotator_, Treshold=20)
        update_log("RotScan", date, int(time.time() - TimeRotateToScan))

        # FIFTH MOVE ###########################################################################
        file = open(filename, "a", encoding="utf-8")
        file.write("Start Scanning\n")
        file.close()
        TimeScan = time.time()
        photo, result = Stol.ScanNow(directory, filename, shaft=shaft_)
        update_log("Scan", date, int(time.time() - TimeScan))
        Uno.exit()

        TimeSend = time.time()
        try:
            img = Image.open(photo[0])
            img2 = Image.open(photo[1])
            img3 = Image.open(photo[2])

            buffer = BytesIO()
            buffer2 = BytesIO()
            buffer3 = BytesIO()

            img.save(buffer, format="JPEG")
            img2.save(buffer2, format="JPEG")
            img3.save(buffer3, format="JPEG")

            img_byte = buffer.getvalue()
            img2_byte = buffer2.getvalue()
            img3_byte = buffer3.getvalue()

            img_base64 = base64.b64encode(img_byte)
            img2_base64 = base64.b64encode(img2_byte)
            img3_base64 = base64.b64encode(img3_byte)

            img_str = img_base64.decode('utf-8')
            img2_str = img2_base64.decode('utf-8')
            img3_str = img3_base64.decode('utf-8')

            file = open(filename, "r", encoding="utf-8")
            files = {"Image1": img_str, "Image2": img2_str, "Image3": img3_str, "File": file.read(), "repka_id": repka_id, "username": username, "date": date, "password": password, "result": result}
            file.close()
            try:
                requests.post(url_upload_logimage, json=files)
            except Exception as e:
                file = open(filename, "a", encoding="utf-8")
                file.write(str(e))
                file.close()
        except Exception as e:
            file = open(filename, "a", encoding="utf-8")
            file.write(str(e))
            file.close()
        update_log("Send", date, int(time.time() - TimeSend))
        time.sleep(10)
    except Exception as e:
        file = open(filename, "a", encoding="utf-8")
        file.write(str(e))
        file.close()
        update_log("error", date, str(e))
    finally:
        subprocess.run(["sudo", "reboot"])


if __name__ == "__main__":
    Run(Area="10x5", TimePyrge=5, TimeSpraying=10)
