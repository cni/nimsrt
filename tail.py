#!/usr/bin/python
import time

def PrintFn(string):
    print string

def Tail(filename, sleepTime = 1, updateCallback = PrintFn):
    try:
        file = open(filename, 'r')
    except:
        print "Error opening file: %s" % filename
        return

    file.seek(0, 2)
    while True:
        where = file.tell()
        lines = file.read()
        if not lines:
            time.sleep(sleepTime)
            file.seek(where)
        else:
            updateCallback(lines)
