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
sleep_time = 1
start_analysis = 5

# Starts temperature monitoring
pvs = ["TU-*:AC-PT100:MeanTemperature-Mon"]
tunnel_temperature = Monitor(pvs, limit=0.1)

# Machine characteristics (data delayed by 3 hours)
while True:
    try:
        last_machine_mode = {
            #"mode": Machine.now(),
            "mode": 0,
            "hour": datetime.now()
        }
        break
    except:
        File.insertLog("There is a problem with machine mode acquisition")
        sleep(60)

while True:
    now = datetime.now()
    if now.minute % start_analysis == 0:

        print(now)

        # Re-train data if changed machine mode (after 3 hours)
        #machine_mode = Machine.now()
        machine_mode = 0
        print(f"\t[1] Machine mode: {Machine.operations_modes[machine_mode]}")

        if last_machine_mode["mode"] != machine_mode:
            past_hours = now - last_machine_mode["hour"]
            if past_hours >= timedelta(hours=3) and machine_mode == 0:
                ini = last_machine_mode["hour"] - timedelta(hours=1)
                Train.pvs(pvs, ini, last_machine_mode["hour"])

                # Update machine mode
                last_machine_mode["mode"] = machine_mode
                last_machine_mode["hour"] = now 

            # Send an alert of changed in machine mode
            str_machine_mode = Machine.operations_modes[machine_mode]
            tgm.sendMessage(f"Novo modo de operação da máquina: {str_machine_mode}")

        # Just request data if machine mode is beam for users
        if last_machine_mode["mode"] == 0:

            print("\t[2] Requesting")
            outside_limits = tunnel_temperature.run()


            if len(outside_limits.keys()) > 0:

                print("\t[3] Sending messages")

                # PV with data outside limits
                for pv in outside_limits.keys():
                    tgm.sendAlert(pv, outside_limits[pv])
            
            else:

                print("\t[3] No messages to send")

    sleep(sleep_time*60)