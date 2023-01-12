# Author: Leonardo Rossi Leão
# E-mail: leonardo.leao@cnpem.br

import os                                       # System properties
import itertools                                # Iteration tools
from actions.math import Math                   # Mathematical functions
from actions.file import File                   # File treatment tools 
from modules.plot import Plot as plt            # Plot tools
from modules.machine import Machine
from modules.training.train import Train
from actions.archiver import Archiver           # CNPEM Archiver tools
from datetime import datetime, timedelta        # Datetime tools

class Monitor():

    """
        This class is responsible for monitoring a set of PVs to 
        identify failures or problems associated with stability and 
        provide the necessary information for telegram messages.
    """

    def __init__(self, pvList: list, limit: int, window: int = 10) -> None:

        """
            Constructor method

            pvList: list with PVs that will be monitored
            limit: limit amplitude, in absolute value, that a PV of this group can oscillate
            window: Data verification window in minutes | Default = 10 minutes
        """

        pvs = [Archiver.getPVs(pvs) for pvs in pvList]
        self.pvs = list(itertools.chain(*pvs))

        self.limit = limit
        self.window = timedelta(minutes=window)

    def insideLimits(self, pv, y, monitored):
        # Load the model of stability
        try:
            model = File.loadModel(pv)
        except:
            end = datetime.now()
            ini = end - timedelta(hours=3)
            Train.pvs([pv], ini, end)
            model = File.loadModel(pv)

        # Parameters of comparison
        avg = Math.avg(y)
        std = Math.std(y)

        # Update monitored variables
        monitored[pv] = {'model': model['mean'], 'value': avg}

        if abs(avg - model['mean']) <= self.limit:
            if std <= self.limit:
                return True
        return avg, model['mean']

    def run(self):

        end = datetime.now()
        ini = end-self.window
        self.data = Archiver.request(self.pvs, ini, end)

        # Machine operating characteristics
        machine_mode = Machine.now()
        thermal_load = Machine.isThereThermalLoad()

        monitored = {}
        outsideLimits = {}
        
        for pv in self.data.keys():

            x = self.data[pv]["x"]
            y = self.data[pv]["y"]

            insideLimits = self.insideLimits(pv, y, monitored)

            if insideLimits != True:

                # Save a plot of the problem with one hour
                path = f".\\modules\\figures\\{pv[3:7]}_{end.strftime('%d%m%Y%H%M%S')}.png"
                plotOptions = {"savefig": path, "xIsDate": True}
                plt.telegram(x, y, plotOptions)
                plot = open(path, 'rb')
                
                outsideLimits[pv] = {
                    "timeItWasDetected": ini,
                    "machineMode": machine_mode,
                    "thermalLoad": thermal_load,
                    "value": insideLimits[0],
                    "trainedValue": insideLimits[1],
                    "plot": plot
                }

        File.updateMonitoredVariables(monitored)

        return outsideLimits