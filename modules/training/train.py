# Author: Leonardo Rossi Leão
# E-mail: leonardo.leao@cnpem.br

import itertools                                # Iteration tools
from datetime import datetime, timedelta        # Datetime tools
from actions.archiver import Archiver           # CNPEM Archiver tools
from actions.file import File                   # File treatment tools 
from actions.math import Math                   # Mathematical functions

from matplotlib import pyplot as plt
import numpy as np

class Train():

    """
        Train a model based on mean, standard deviation, amplitude and 
        natural frequencies to get stable characteristics of a signal
    """

    @staticmethod
    def pvs(pvList: list, ini: datetime, end: datetime) -> None:
        
        """
        
        """

        pvs = [Archiver.getPVs(pvs) for pvs in pvList]
        pvs = list(itertools.chain(*pvs))

        data = Archiver.request(pvs, ini, end, 1)
        
        for pv in data.keys():
            
            x = data[pv]["x"]
            y = data[pv]["y"]

            mean = Math.avg(y)
            std = Math.std(y)
            now = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")

            text = f"""mean={mean}\nstd={std}\nlastUpdate={now}"""
            File.insertModel(pv, text)

        File.insertLog(f"New training on pvs ${pvList}")
