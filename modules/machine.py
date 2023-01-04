# Author: Leonardo Rossi Leão
# E-mail: leonardo.leao@cnpem.br

from actions.archiver import Archiver           # CNPEM Archiver tools
from datetime import datetime, timedelta        # Datetime tools
from actions.math import Math                   # Mathematical functions

class Machine():

    operationModes = {
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
        pv = "AS-Glob:AP-MachShift:Mode-Sts"
        data = Archiver.request([pv], ini, end)
        return (data[pv]["x"], data[pv]["y"])

    @staticmethod
    def now():
        now = datetime.now()
        _, modes = Machine.mode(now, now)
        return modes[-1]

    @staticmethod
    def isThereThermalLoad():
        current = "SI-13C4:DI-DCCT:Current-Mon"
        rf = "RF-Gen:GeneralFreq-SP"

        # Requires the last 10 seconds of data
        end = datetime.now()
        ini = end - timedelta(seconds=10)
        data = Archiver.request([current, rf], ini, end)

        # Get the averages of the last 30 seconds to analyze thermal load
        currentValue = Math.avg(data[current]["y"])
        rfValue = Math.avg(data[rf]["y"])

        # Quando o feixe cai a carga térmica continua inalterada

        # Current less than 20 miliampere or RF is paused
        if currentValue <= 20 or rfValue == data[rf]["y"][0]:
            return False
        return True
        