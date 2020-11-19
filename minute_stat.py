from datetime import datetime, timedelta
import time
import math


class LastKMinuteStat:
    def __init__(self, minute):
        self.k = timedelta(seconds=minute*60)  # converting to seconds
        self.list = []

    def append(self, up, down):
        self.list.append((datetime.now(), up+down))
        while len(self.list) > 1000:
            self.list.pop(0)

    def getStat(self):
        now = datetime.now()
        sum = 0
        perSec = 0
        while len(self.list) > 0 and (now-self.list[0][0]) > self.k:
            self.list.pop(0)
        l = len(self.list)
        if l > 0:
            sum = math.fabs(self.list[l-1][1]-self.list[0][1])
            perSec = sum/self.k.seconds
        return (self._data_unit_calc(sum, "B"), self._data_unit_calc(perSec, "Bps"))

    def getFormattedStat(self):
        (tot, totps) = self.getStat()
        return "%s\n%s" % (tot, totps)

    def _data_unit_calc(self, bytes: float, unit):
        units = ["", "K", "M", "G"]
        unitInd = 0
        while bytes >= 1024:
            bytes /= 1024
            unitInd += 1
        return ("%6.2f %s%s") % (bytes, units[unitInd], unit)
