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
        # if user turns PC off at 22:30, then we record all data collected to "22:00"
        # then, if user turns PC on at 22:45, we load data that we wrote at 22:30 to be stored at keeper
        # and delete last line ("22:00")
        # it will allow us to keep actual hourly data in keeper at any moment
        lastRecord = lastlines(self.path, 1)[0].split(',')
        if currentHour() == lastRecord[0]:
            removeLines(self.path, 1)
            return int(lastRecord[1])
        else:
            return 0

    def addEntry(self, date, value):
        with open(self.path, 'a') as f:
            f.write('{},{}\n'.format(date, value))