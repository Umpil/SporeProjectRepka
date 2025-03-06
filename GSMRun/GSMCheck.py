import datetime
import subprocess
import time
from StartProcess_GSM import Run
from serianumber import repka_id, url_check, username, password
import sim800l
import json

checks = {"un": username, "ri": repka_id, "pw": password}
time_ask = 300

try:
    sim = sim800l.SIM800L()
    sim.setup()
    time.sleep(1)
    responce = sim.http(url=url_check, data=json.dumps(checks).encode(), method="PUT", apn="internet.tele2.ru", allow_redirection=True)
    if not responce:
        raise Exception
    data: dict = json.loads(responce)

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
            Run(sim, Area=Area, TimePyrge=TimePyrge, TimeSpraying=TimeSpraying, date=Next)
    else:
        time.sleep(time_ask - 65)
        subprocess.run(["sudo", "reboot"])

except Exception as e:
    print(e)
    time.sleep(time_ask - 80)
    subprocess.run(["sudo", "reboot"])

