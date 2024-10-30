import datetime
import subprocess
import time
import requests
import Full3
from Utils.serianumber import repka_id, url_check, username, password

checks = {"username": username, "repka_id": repka_id, "password": password}
time_ask = 300

try:
    responce = requests.get(url_check, json=checks)
    data: dict = responce.json()

    Next = int(data["Next"])
    time_ask = int(data["TimeAsk"]) * 60
    if Next:

        today = datetime.datetime.today().replace(second=0, microsecond=0).timestamp()
        print(Next - today)
        if Next - today > time_ask:
            print(">t_ask")
            time.sleep(time_ask - 65)
            subprocess.run(["sudo", "reboot"])
        else:
            Area = data["Area"]
            TimePyrge = int(data["Pyrge"]) * 60
            TimeSpraying = int(data["Spray"]) * 60
            time.sleep(abs(Next - today - 10))
            Full3.Run(Area=Area, TimePyrge=TimePyrge, TimeSpraying=TimeSpraying, date=Next)
    else:
        time.sleep(time_ask - 65)
        subprocess.run(["sudo", "reboot"])

except Exception as e:
    print(e)
    time.sleep(time_ask - 65)
    subprocess.run(["sudo", "reboot"])

