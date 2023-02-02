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

# Machine characteristics (data delayed by 3 hours)
while True:
    try:
        last_machine_mode = {
            "mode": Machine.now(),
            "hour": datetime.now(),
            "thermalLoad": Machine.isThereThermalLoad()
        }
        break
    except:
        File.insertLog("There is a problem with machine mode acquisition")
        sleep(60)

while True:
    now = datetime.now()
    settings = File.loadSettings()

    if settings["status"] == 1 and (now.minute % settings["alarm_time"] == 0):

        tunnel_temperature = Monitor(pvs, limit=0.1, window=settings["alarm_time"])

        # Re-train data if changed machine mode (after 3 hours)
        machine_mode = Machine.now()
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

        print("\t[2] Requesting")
        outside_limits = tunnel_temperature.run()

        # Just request data if machine mode is beam for users
        if last_machine_mode["mode"] == 0:

            if len(outside_limits.keys()) > 0:

                print("\t[3] Sending messages")

                # PV with data outside limits
                for pv in outside_limits.keys():
                    
                    thermalLoad = outside_limits[pv]["thermalLoad"]
                    
                    # Alert of change in tunnel thermal load
                    if thermalLoad != last_machine_mode["thermalLoad"]:
                        if thermalLoad:
                            tgm.sendMessage("⚠️Alerta!\nAumento de carga térmica no túnel")
                        else:
                            tgm.sendMessage("⚠️Alerta!\nQueda de carga térmica no túnel")
                        last_machine_mode["thermalLoad"] = thermalLoad

                    # Just send messages if tunnel thermal load is in standard mode
                    if thermalLoad:
                        tgm.sendAlert(pv, outside_limits[pv])
            
            else:

                print("\t[3] No messages to send")

    sleep(sleep_time*60)