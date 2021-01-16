#!/usr/bin/env python3
import signal
from src.keyKeeper import *
from src.keySaver import *
from src.keyHandler import *

def main():
    global saver, keeper, handler
    saver = Saver(path)
    keeper = Keeper(saver.lastValue)
    handler = Handler(keeper)
    # peridocally save
    # display keeper value somewhere

if __name__ == "__main__":
    path = 'logfile.csv'

    def receiveSignal(signalNumber, frame):
        saver.flush(keeper.counter)
        exit()

    signal.signal(signal.SIGINT, receiveSignal)
    signal.signal(signal.SIGQUIT, receiveSignal)
    signal.signal(signal.SIGTERM, receiveSignal)
    
    main()