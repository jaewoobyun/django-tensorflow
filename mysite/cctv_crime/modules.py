from dataclasses import dataclass
from abc import *
import pandas as pd
import numpy as np
import json
import googlemaps

@dataclass
class File(object):
    context: str
    fname: str
    dframe: object

    @property
    def context(self) -> str: return self._context

    @context.setter
    def context(self, context): self._context = context

    @property
    def fname(self) -> str: return self._fname

    @fname.setter
    def fname(self, fname): self._fname = fname

    @property
    def dframe(self) -> str: return self._dframe

    @dframe.setter
    def dframe(self, dframe): self._dframe = dframe

class ReaderBase(metaclass=ABCMeta):

    @abstractmethod
    def new_file(self):
        pass

    @abstractmethod
    def csv(self):
        pass

    @abstractmethod
    def xls(self):
        pass

    @abstractmethod
    def json(self):
        pass

class PrinterBase(metaclass=ABCMeta):

    @abstractmethod
    def dframe(self):
        pass

class Reader(ReaderBase):

    def new_file(self, file) -> str:
        return file.context + file.fname

    def csv(self, file) -> object:
        return pd.read_csv(f'{self.new_file((file))}.csv', encoding='UTF-8', thousands=',')

    def xls(self, file, header, usecols) -> object:
        return pd.read_excel(f'{self.new_file((file))}.xls', header=header, usecols=usecols)

    def json(self, file) -> object:
        return json.load(open(f'{self.new_file((file))}.json'), encoding='UTF-8')

    def gmaps(self) -> object:
        return googlemaps.Client(key='')


class Printer(PrinterBase):
    def dframe(self, this):
        print('*' * 100)
        print(f'1. Target type \n {type(this)} ')
        print(f'2. Target column \n {this.columns} ')
        print(f'3. Target top 1개 행\n {this.head(1)} ')
        print(f'4. Target bottom 1개 행\n {this.tail(1)} ')
        print(f'5. Target null 의 갯수\n {this.isnull().sum()}개')
        print('*' * 100)

class Service(Reader):

    def __init__(self):
        self.file = File()
        self.reader = Reader()
        self.printer = Printer()

        self.crime_rate_columns = ['살인검거율', '강도검거율', '강간검거율', '절도검거율', '폭력검거율']
        self.crime_columns = ['살인', '강도', '강간', '절도', '폭력']

    def save_plolice_pos(self):
        file = self.file
        reader = self.reader
        printer = self.printer

        file.context = './data/'
        file.fname = 'crime_in_seoul'
        crime = reader.csv(file)
        # printer.dframe(crime)
        station_names = []
        for name in crime['관서명']:
            station_names.append('서울' + str(name[:-1] + '경찰서'))
        station_addrs = []
        station_lats = []
        station_lngs = []
        gmaps = reader.gmaps()


if __name__ == '__main__':

    s = Service()
    s.save_plolice_pos()

