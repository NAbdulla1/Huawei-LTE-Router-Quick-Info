from datetime import datetime, timedelta
import time
import math
import util


class LastKMinuteStat:
    def __init__(self, minute):
        self.k = timedelta(seconds=minute*60)  # converting to seconds
        self.list = []

    def append(self, up, down):
        cur = up+down
        self.list.append((datetime.now(), cur))
        now = datetime.now()
        while len(self.list) > 0 and (now-self.list[0][0]) > self.k:
            self.list.pop(0)

    def getStat(self):
        sum = 0
        perSec = 0
        now = datetime.now()
        while len(self.list) > 0 and (now-self.list[0][0]) > self.k:
            self.list.pop(0)
        if len(self.list) > 0:
            sum = math.fabs(self.list[-1][1]-self.list[0][1])
            perSec = sum/self.k.seconds
        return (util.data_unit_calc(sum, "B"), util.data_unit_calc(perSec, "Bps"))

    def getFormattedStat(self):
        (tot, totps) = self.getStat()
        return "%s\n%s" % (tot, totps)

    def clear(self):
        self.list.clear()
