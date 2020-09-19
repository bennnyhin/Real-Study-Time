import time

class Timer:
    def __init__(self):
        self._start = None
        self._end = None
        self._isEnded = False
    
    def startTimer(self):
        self._start = time.time()

    def endTimer(self):
        self._end = time.time()
        self._isEnded = True

    def getTime(self):
        if (self._isEnded):
            return self._end - self._start
        else:
            return time.time() - self._start