from datetime import datetime, timedelta
from threading import Lock
import time
import math
import util


class LastKMinuteStat:
    def __init__(self, k_minute):
        self.k = timedelta(seconds=k_minute*60)  # converting to seconds
        self.list = []
        self.last = -1
        self.sum = 0
        self.lock = Lock()

    def append(self, up, down):
        cur = up+down
        to_add = 0
        if self.last != -1:
            to_add = cur-self.last
        self.last = cur
        self.list.append((datetime.now(), to_add))
        self.sum += to_add
        self.removeOlderStat()

    def removeOlderStat(self):
        now = datetime.now()
        while len(self.list) > 0 and (now-self.list[0][0]) > self.k:
            self.sum -= self.list[0][1]
            self.list.pop(0)
        if len(self.list) == 0:
            self.sum = 0
            self.last = -1

    def getStat(self):
        perSec = 0
        self.removeOlderStat()
        if len(self.list) > 0:
            perSec = self.sum/self.k.seconds
        return (util.data_unit_calc(self.sum, "B"), util.data_unit_calc(perSec, "Bps"))

    def getFormattedStat(self):
        with self.lock:
            (tot, totps) = self.getStat()
            return "%s\n%s" % (tot, totps)

    def clear(self):
        with self.lock:
            self.list.clear()
            self.sum = 0
            self.last = -1
