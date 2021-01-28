#!/usr/bin/env python3
import argparse
import atexit
import signal
from pytz import utc
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from src.keyKeeper import *
from src.keySaver import *
from src.keyHandler import *

scheduler = BackgroundScheduler(timezone=utc, misfire_grace_time=3659)

parser = argparse.ArgumentParser()
parser.add_argument('path', type=str, help="Path to log file (including filename)")

@scheduler.scheduled_job('cron', id='saverJob', hour='*', coalesce=True)
def save():
    saver.addEntry(currentHour(-1), keeper.counter)
    keeper.counter = 0

@atexit.register
def emergencySave():
    saver.addEntry(currentHour(), keeper.counter)

def main():
    global saver, keeper, handler
    saver = Saver(path)
    keeper = Keeper(saver.lastValue)
    handler = Handler(keeper)

if __name__ == "__main__":
    args = parser.parse_args()
    path = args.path

    def receiveSignal(signalNumber, frame):
        exit()

    signal.signal(signal.SIGINT, receiveSignal)
    signal.signal(signal.SIGTSTP, receiveSignal)
    signal.signal(signal.SIGHUP, receiveSignal)
    signal.signal(signal.SIGQUIT, receiveSignal)
    signal.signal(signal.SIGTERM, receiveSignal)
    signal.signal(signal.SIGPIPE, receiveSignal)
    
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())
    main()