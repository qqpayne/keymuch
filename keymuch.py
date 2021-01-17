#!/usr/bin/env python3
import signal
import argparse
from threading import Timer
from src.keyKeeper import *
from src.keySaver import *
from src.keyHandler import *
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument('path', type=str, help="Path to log file (including filename)")

def setHourlyTimer():
    global saveCallback, renewalCallback
    # firstly, it check how much time left until next hour
    # and sets timer to commit save after this time
    now = datetime.now()
    nextHour = datetime(now.year, now.month, now.day, now.hour+1)
    waitFor = (nextHour-now).seconds+2 # just to be sure
    saveCallback = Timer(waitFor, save)
    saveCallback.start()
    # then, it sets itself to be executed again after this time 
    renewalCallback = Timer(waitFor+1, setHourlyTimer)
    renewalCallback.start()

def save():
    saver.addEntry(currentHour(-1), keeper.counter)
    keeper.counter = 0

def main():
    setHourlyTimer()
    global saver, keeper, handler
    saver = Saver(path)
    keeper = Keeper(saver.lastValue)
    handler = Handler(keeper)

if __name__ == "__main__":
    args = parser.parse_args()
    path = args.path

    catched = False
    def receiveSignal(signalNumber, frame):
        global catched
        if catched == False:
            catched = True
            saver.addEntry(currentHour(), keeper.counter)
            saveCallback.cancel()
            renewalCallback.cancel()
            exit()

    signal.signal(signal.SIGINT, receiveSignal)
    signal.signal(signal.SIGTSTP, receiveSignal)
    signal.signal(signal.SIGHUP, receiveSignal)
    signal.signal(signal.SIGQUIT, receiveSignal)
    signal.signal(signal.SIGTERM, receiveSignal)
    signal.signal(signal.SIGPIPE, receiveSignal)

    main()