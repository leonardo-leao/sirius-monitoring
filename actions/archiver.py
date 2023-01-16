# Author: Leonardo Rossi Leão
# E-mail: leonardo.leao@cnpem.br

import requests as httpRequest              # HTTP Requests
from alive_progress import alive_bar
from ast import literal_eval                # Convert text json to list
from datetime import datetime, timedelta    # Datatime functions
from actions.file import File               # Files treatment functions

class Archiver():

    """
        Functions for manipulating and obtaining data 
        from the CNPEM archiver
    """

    @staticmethod
    def getPVs(search: str, limit: int = 500) -> None:

        """
            Performs a textual lookup of a process variable 
            in the archiver's variable database

            search: string with parts of the PV's name
            limit: max number of PVs that will be returned
        """

        while True:
            try:
                url = 'http://ais-eng-srv-ta.cnpem.br/retrieval/bpl/getMatchingPVs'
                params = {'pv': search, 'limit': limit}

                response = httpRequest.get(url, params=params)
                
                return literal_eval(response.text)
                
            except: pass

    @staticmethod
    def __datetime2str(datetime: datetime) -> str:

        """
            Converts a datetime input to a string in the 
            archiver request format
        """     

        return datetime.strftime("%Y-%m-%dT%H:%M:%SZ")

    @staticmethod
    def request(pvs: list, ini: datetime, end: datetime, mean: int = None) -> dict:

        """
            Request PV data in the CNPEM Archiver

            pvs: list with the name of process variables
            ini: initial datetime of the request
            end: end datetime of the request
            mean: time in seconds for data windowing using temporal average
        """

        url = 'http://ais-eng-srv-ta.cnpem.br/retrieval/data/getData.json'
        result = {}

        with alive_bar(len(pvs), title='Archiver') as bar:

            for pv in pvs:
                
                params = {
                    'pv': f'({pv})' if mean == None else f'mean_{mean}({pv})',
                    'from': Archiver.__datetime2str(ini + timedelta(hours=3)),
                    'to': Archiver.__datetime2str(end + timedelta(hours=3))
                }

                try:
                    response = httpRequest.get(url=url, params=params).json()

                    meta = response[0]['meta']
                    data = response[0]['data']

                    x, y = [], []
                    for counter in range(len(data)):
                        x.append(datetime.fromtimestamp(data[counter]['secs']))
                        y.append(data[counter]['val'])
                        
                    result[pv] = {'x': x, 'y': y}
            
                except Exception as e:
                    File.insertLog(f'A problem occurred while requesting {pv} data')
                
                bar()

        return result