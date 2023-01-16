# Author: Leonardo Rossi Leão
# E-mail: leonardo.leao@cnpem.br

import os
import glob                             # Files and directory functions
from datetime import datetime           # Datetime functions

class File():

    """ Functions for creating, reading and manipulating files """

    logPath = os.getenv("tempMonitorPath")

    @staticmethod
    def __createFile(path: str) -> None:

        """ Create a file if one with the same name does not exist """

        if path not in glob.glob(path + '*'):
            file = open(path, 'w')
            file.close()
    
    @staticmethod
    def __appendFile(path: str, text: str) -> None:

        """ Add text to a txt file """

        File.__createFile(path)
        with open(path, 'a') as file:
            if type(text) == list:
                text.append("\n")
            else:
                text += "\n"
            file.writelines(text)
            file.close()
        

    @staticmethod
    def insertLog(message: str) -> None:

        """ Insert a message in a log file """

        now = datetime.now()

        path = f'{File.logPath}/log/log_{now.strftime("%Y_%m_%d")}.txt'
        message = f'[{now.strftime("%H:%M:%S")}] {message}'

        File.__appendFile(path, message)

    @staticmethod
    def updateMonitoredVariables(monitored: dict) -> None:

        """ Insert in the monitored variables file the values 
        obtained for each pv in the last analysis """

        path = f'{File.logPath}/log/monitoredVariables.txt'

        with open(path, 'w') as file:

            message = ''
            for pv in sorted(monitored.keys()):
                model = round(monitored[pv]['model'], 2)
                value = round(monitored[pv]['value'], 2)
                difference = round(value-model, 2)
                message += f'{pv}\n\tmodel: {model}\n\tvalue: {value}\n\tdifference: {difference}\n'
            message += f'Last update: {datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}\n'

            file.write(message)

            print("\t[4] Updating monitored variables")

            file.close()

    @staticmethod
    def insertModel(pv: str, model: str) -> None:

        """ Insert a new model from PV stability """

        name = pv.replace("-", "").replace(":", "")
        path = f'{File.logPath}/modules/training/models/{name}.txt'

        File.__appendFile(path, model)

    @staticmethod
    def loadModel(pv: str) -> None:
        
        name = pv.replace("-", "").replace(":", "")
        path = f'{File.logPath}/modules/training/models/{name}.txt'

        model = {}

        with open(path, 'r') as file:
            data = file.read()
            data = data.split('\n')

            for i in range(len(data)-1):
                mType, mValue = data[i].split('=')
                try:
                    model[mType] = float(mValue)
                except:
                    model[mType] = datetime.strptime(mValue, "%d/%m/%Y, %H:%M:%S")

        return model