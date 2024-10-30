from DevicesOnLines import Rele

Usb = Rele(0)
d = True
while d:
    ds = input("O/C")
    if ds.lower() == "o":
        Usb.Open()
    elif ds.lower() == "c":
        Usb.Close()
    else:
        d = False
