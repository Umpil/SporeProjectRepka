import pyfirmata2
from Devices import NemaStepper
import tkinter
ard = pyfirmata2.Arduino("COM4")
ZS = NemaStepper(ard, 1600, 4, 7, 8)
ZS.SetSpeed(50)


win = tkinter.Tk()


def go_up():
    global ZS
    ZS.Step(2)


def go_dow():
    global ZS
    ZS.Step(-2)


btnup = tkinter.Button(text="up", master=win, command=go_up)
btnup.grid(row=1, column=0)
btndown = tkinter.Button(text="down", master=win, command=go_dow)
btndown.grid(row=2, column=0)
win.mainloop()
# import os
# import time
# import pyfirmata2
# from Devices import NemaStepper
# import cv2
# arduinoUno = pyfirmata2.Arduino("/dev/ttyUSB0")
# time.sleep(2)
# Xstepper = NemaStepper(arduinoUno, 200, 2, 5, 8)
# YStepper = NemaStepper(arduinoUno, 200, 3, 6)
#
#
# Xstepper.SetSpeed(10)
# YStepper.SetSpeed(10)
# ZStepper = NemaStepper(arduinoUno, 200, 4, 7)
# ZStepper.SetSpeed(5)
# camera = cv2.VideoCapture(1)
# for i in range(3, 15):
#     Xstepper.Epin.write(0)
#     for j in range(15):
#         print(i, j)
#         ZStepper.Step(-20)
#         time.sleep(3)
#         os.mkdir(f"/home/admin/focus/{i}_{j}")
#         for k in range(20):
#             _, frame = camera.read()
#             ZStepper.Step(1)
#             time.sleep(0.4)
#             print(k)
#             cv2.imwrite(f"/home/admin/focus/{i}_{j}/{k}.jpg", cv2.flip(frame, 1))
#
#         for k in range(20):
#             _, frame = camera.read()
#             ZStepper.Step(1)
#             time.sleep(0.4)
#             print(-k)
#             cv2.imwrite(f"/home/admin/focus/{i}_{j}/{21 - k}.jpg", cv2.flip(frame, 1))
#
#         ZStepper.Step(-20)
#         time.sleep(1)
#         YStepper.Step(-28)
#         time.sleep(1)
#     Xstepper.Step(34)
#     time.sleep(1)
#     Xstepper.Epin.write(0)
#     YStepper.Step(28 * 15)
#     time.sleep(5)
#
# Xstepper.Epin.write(1)
# arduinoUno.exit()
# camera.release()
# import time
#
# from FullMega import MegaBoard
#
# mg = MegaBoard("/dev/ttyUSB1")
#
# mg.SetLiftSpeed(50)
# mg.LiftStep(500)
# mg.LiftStep(-500)
# time.sleep(5)
#
# mg.SetLiftSpeed(25)
# mg.LiftStep(500)
# mg.LiftStep(-500)
# time.sleep(5)
#
# mg.SetLiftSpeed(10)
# mg.LiftStep(500)
# mg.LiftStep(-500)
# time.sleep(5)
#
# mg.SetLiftSpeed(5)
# mg.LiftStep(500)
# mg.LiftStep(-500)
# time.sleep(5)
