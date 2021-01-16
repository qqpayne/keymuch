import os
from datetime import datetime

def lastlines(fname, N): 
    bufsize = 1024
    fsize = os.stat(fname).st_size 
    itera = 0
    with open(fname) as f: 

        if bufsize > fsize: 
            bufsize = fsize-1

        fetched_lines = []   
        while True: 
            itera += 1
            f.seek(fsize-bufsize * itera)
            fetched_lines.extend(f.readlines())   
            if len(fetched_lines) >= N or f.tell() == 0: 
                    return fetched_lines[-N:] 
                    break

def removeLines(name, number):
    with open(name,'r+b', buffering=0) as f:
        f.seek(0, os.SEEK_END)
        end = f.tell()
        count = 0
        while f.tell() > 0:
            f.seek(-1, os.SEEK_CUR)
            char = f.read(1)
            if char != b'\n' and f.tell() == end:
                return 1 # file doesn't end with newline
            if char == b'\n':
                count += 1
            if count == number + 1:
                f.truncate()
                return 0 # it's good
            f.seek(-1, os.SEEK_CUR)
        if count < number + 1:
            return 1 # it will leave file empty

def currentHour():
    now = datetime.now()
    return "{}-{}-{} {}:00:00.000000".format(now.year,now.month,now.day,now.hour)


