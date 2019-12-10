
import datetime
import time

class TimeCvter:
    def __init__(self):
        pass

    def datetime_toString(self, dt):
        return dt.strftime("%Y-%m-%d")

    def getNowTimeStr(self):
        nowTime = datetime.datetime.now()
        return self.datetime_toString(nowTime)

if __name__ == '__main__':
    tmcvt = TimeCvter()
    timeNow = datetime.datetime.now()
    tmcvt.datetime_toString(timeNow)