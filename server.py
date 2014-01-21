#!/usr/bin/python
import time
import threading
from tail import Tail
from copy import deepcopy
from json import JSONEncoder, JSONDecoder
from paste import httpserver
from logparser import ParseLog
from objectpub import ObjectPublisher
# SUGGESTION: For testing the tail parsing code, use cat scnout.txt > somefile.txt
LOGFILE = '/usr/g/service/log/scn.out'
SLEEPTIME = 1 # in seconds

class ServerRoot(object):
    def __init__(self, scanLog):
        self.events = scanLog.getEvents # /events

    def __call__(self): # The "index" method
        return """
            Nothing to see here...
            """

class TailThread(threading.Thread):
    def __init__(self, tailFile, sleepTime, callback = None):
        # Filter skips the last argument if it's None
        self.args = filter(None, (tailFile, sleepTime, callback))
        threading.Thread.__init__(self)

    def run(self):
        Tail(*self.args)

class ScanLog:
    # Going to start without deleting old history for testing
    def __init__(self, memory = 60): # time in minutes to remember history
        self.log = []
        self.lock = threading.Lock()

    def addEvents(self, string):
        events = ParseLog(string)
        if events:
            events = sorted(events, key = lambda event: event[1]['datetime'])
            with self.lock:
                self.log.extend(events)

    def getEvents(self, json = False):
        # TODO does return release the lock within a with statement?
        with self.lock:
            log = deepcopy(self.log)
        if json:
            eventString = JSONEncoder().encode(log)
        else:
            eventString = ''
            for event in log:
                eventString += '%d # %s ' % (event[1]['datetime'], event[0])
                del event[1]['datetime'] # we've used this, now we'll iterate over the remaining keys
                for key in event[1]:
                    eventString += '# %s : %s ' % (key, event[1][key])
                eventString += '<br>'
        return eventString

if __name__ == "__main__":
    scanLog = ScanLog()
    tailThread = TailThread(LOGFILE, SLEEPTIME, scanLog.addEvents)
    tailThread.start()
    app = ObjectPublisher(ServerRoot(scanLog))
    httpserver.serve(app, host='cnimr.stanford.edu', port='8080')
