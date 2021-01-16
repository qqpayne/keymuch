#!/usr/bin/env python3
import signal
from threading import Timer
from src.keyKeeper import *
from src.keySaver import *
from src.keyHandler import *
from datetime import datetime

def setHourlyTimer():
    # firstly, it check how much time left until next hour
    # and sets timer to commit save after this time
    now = datetime.now()
    nextHour = datetime(now.year, now.month, now.day, now.hour+1)
    waitFor = (nextHour-now).seconds+2 # just to be sure
    Timer(waitFor, save).start()
    # then, it sets itself to be executed again after this time 
    Timer(waitFor+1, setHourlyTimer).start()

def save():
    saver.addEntry(currentHour(-1), keeper.counter)
    keeper.counter = 0

def main():
    global saver, keeper, handler
    saver = Saver(path)
    keeper = Keeper(saver.lastValue)
    handler = Handler(keeper)

    setHourlyTimer()

if __name__ == "__main__":
    path = 'logfile.csv'

    def receiveSignal(signalNumber, frame):
        saver.addEntry(currentHour(), keeper.counter)
        exit()

    signal.signal(signal.SIGINT, receiveSignal)
    signal.signal(signal.SIGQUIT, receiveSignal)
    signal.signal(signal.SIGTERM, receiveSignal)
    
    main()