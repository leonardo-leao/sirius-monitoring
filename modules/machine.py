# Author: Leonardo Rossi Leão
# E-mail: leonardo.leao@cnpem.br

from actions.archiver import Archiver           # CNPEM Archiver tools
from datetime import datetime, timedelta        # Datetime tools
from actions.math import Math                   # Mathematical functions
from actions.file import File

class Machine():

    operations_modes = {
        0: 'Feixe para Usuários',
        1: 'Comissionamento',       # A partir de março não terá mais (?)
        2: 'Condicionamento',       # Igual feixe pra usuarios mas sem usuarios
        3: 'Injeção de feixe',
        4: 'Estudo de Máquina',
        5: 'Manutenção',
        6: 'Em espera',
        7: 'Desligada'
    }

    @staticmethod
    def mode(ini, end):
        while True:
            try:
                pv = "AS-Glob:AP-MachShift:Mode-Sts"
                data = Archiver.request([pv], ini, end)
                return (data[pv]["x"], data[pv]["y"])
            except: pass

    @staticmethod
    def now():
        now = datetime.now()
        _, modes = Machine.mode(now, now)
        return modes[-1]

    @staticmethod
    def isThereThermalLoad():

        # Temperature of water used to magnets refrigeration
        magnets = "SI-18-MBTemp-13-CH7"

        # Requires the last 10 seconds of data
        end = datetime.now()
        ini = end - timedelta(seconds=10)
        data = Archiver.request([magnets], ini, end)

        # Get the averages of the last 30 seconds to analyze thermal load
        magnets_hot_value = Math.avg(data[magnets]["y"])

        # If the water temperature of magnets refrigeration is less than 25
        # degrees, the magnets is off
        if magnets_hot_value < 25:
            return False
        return True
        

# current = "SI-13C4:DI-DCCT:Current-Mon"
# rf = "RF-Gen:GeneralFreq-SP"
# # Current in dipole sources
# dipole = "SI-Fam:PS-B1B2-1:Current-Mon"
# current_value = Math.avg(data[current]["y"])
# rf_value = Math.avg(data[rf]["y"])
# dipole_value = Math.avg(data[dipole]["y"])
# magnets_cold_value= Math.avg(data[magnets[1]]["y"])