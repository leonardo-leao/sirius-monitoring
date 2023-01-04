# Author: Leonardo Rossi Leão
# E-mail: leonardo.leao@cnpem.br

from time import sleep
from datetime import datetime, timedelta

from modules.monitor import Monitor
from modules.machine import Machine
from modules.training.train import Train
from modules.telegram.group import TelegramGroupMessage as tgm

from actions.file import File

# Processing characteristics
sleepTime = 1
startAnalysis = 5

# Starts temperature monitoring
pvs = ["TU-*:AC-PT100:Temperature-Mon"]
tunnelTemperature = Monitor(pvs, limit=0.1)

# Machine characteristics (data delayed by 3 hours)
while True:
    try:
        lastMachineMode = {
            "mode": Machine.now(),
            "hour": datetime.now()
        }
        break
    except:
        File.insertLog("There is a problem with machine mode acquisition")
        sleep(60)

while True:
    now = datetime.now()
    if now.minute % startAnalysis == 0:

        print(now)

        # Re-train data if changed machine mode (after 3 hours)
        machineMode = Machine.now()
        print(f"\t[1] Machine mode: {Machine.operationModes[machineMode]}")

        if lastMachineMode["mode"] != machineMode:
            pastHours = now - lastMachineMode["hour"]
            if pastHours >= timedelta(hours=3) and machineMode == 0:
                ini = lastMachineMode["hour"] - timedelta(hours=1)
                Train.pvs(pvs, ini, lastMachineMode["hour"])

                # Update machine mode
                lastMachineMode["mode"] = machineMode
                lastMachineMode["hour"] = now 

            # Send an alert of changed in machine mode
            strMachineMode = Machine.operationModes[machineMode]
            tgm.sendMessage(f"Novo modo de operação da máquina: {strMachineMode}")

        # Just request data if machine mode is beam for users
        if lastMachineMode["mode"] == 0:

            print("\t[2] Requesting")
            outsideLimits = tunnelTemperature.run()

            print("\t[3] Sending messages")

            # PV with data outside limits
            for pv in outsideLimits.keys():
                tgm.sendAlert(pv, outsideLimits[pv])

    sleep(sleepTime*60)