from datetime import datetime
from src.helpers import *
import os

class Saver:

    def __init__(self, path):
        self.path = path
        self.checkFile()
        self.lastValue = self.checkLastHour()

    def checkFile(self):
        csvHeader = 'time,value\n'

        try:
            with open(self.path, 'r') as f:
                line = f.readline()
            if line != csvHeader:
                print("Corrupt CSV header in logfile.\nCheck and correct it manually to avoid data loss.")
                os._exit(1)
        except FileNotFoundError:
            with open(self.path, 'w+') as f:
                    f.write(csvHeader)

    def checkLastHour(self):
        lastRecord = lastlines(self.path, 1)[0].split(',')
        if currentHour() == lastRecord[0]:
            removeLines(self.path, 1)
            return int(lastRecord[1])
        else:
            return 0

    def addEntry(self, date, value):
        with open(self.path, 'a') as f:
            f.write('{},{}\n'.format(date, value))

    def flush(self, value):
        self.addEntry(currentHour(), value)

# если юзер вырубает приложение в 22:30, то записи накопившиеся до этого записываются в слот для 22:00
# потом он запускает его в 22:45, но мы обнаруживаем что слот для 22:00 уже занят
# в этом случае мы выгружаем эти данные для кипера
# а сэйвер удаляет эту запись 
# это уберет необходимость проверять целостность данных при запуске
# все аварийные события будут просто записывать в текущий слот, а затем мы его будем удалять с выгрузкой данных в RAM
# идеально!