
from common.readdata import *
from common.DataTuning.RawDataTuning.FTPDataTuning import FTPDataTuning
from common.DataTuning.RawDataTuning.RedisDataTuning import RedisDataTuning
from Data_base.Data_redis.redis_deal import redis_deal
import sys
from Config.FileConfig import FileConfig


class DataTuning:
    def __init__(self):
        self.ftp = FTPDataTuning()
        self.redis = RedisDataTuning()
        self.redis_deal = redis_deal()
        self.fConfig = FileConfig()

    def readDatas(self, filePath):
        datas= read_filedatas(filePath)
        datas = get_puredatas(datas)
        return datas

    def readDataSummarys(self, filePath):
        datas = read_filedatas(filePath)
        return datas

    def readDatasTemp(self, filePath):
        srcDatas, desDatas = self.ftp.tuningHttpByregix()
        datas = []
        datas.extend(srcDatas)
        datas.extend(desDatas)
        return datas

    def icsReadDatasTemp(self, filePath):
        messages = read_datas('/home/wxw/data/ToolDatas/15895903730.10.222', 'single')
        messages = get_puredatas(messages)
        return messages

    def textReadDatasTemp(self, filePath):
        messages = self.redis.sampleDatas()
        return messages

    def readDatasByType(self, fileType):
        fileName = self.redis_deal.read_from_redis(fileType)
        filePath = os.path.join(self.fConfig.pathDir, fileName)
        return self.readDatas(filePath)

    def readSummaryByType(self, fileType):
        fileName = self.redis_deal.read_from_redis(fileType)
        filePath = os.path.join(self.fConfig.pathDir, fileName)
        print('aa')
        print(filePath)
        print('bb')
        return self.readDataSummarys(filePath)


