
from common.DataTuning.RawDataTuning.RedisDataTuning import RedisDataTuning
from common.readdata import *
from common.Converter.MessageConvert import MessageConvert


class RedisDataTuningTest:
    def __init__(self, path):
        self.redisData = RedisDataTuning(path)
        self.msgConvert = MessageConvert()

    def getDatas(self, path):
        redisDatas = read_datas(path, 'single')
        return redisDatas

    def splitDatas(self, datas):
        srcDatas, desDatas = self.msgConvert.clsMessageByDire(datas)
        return srcDatas, desDatas

    def getDesCommondTest(self, desDatas):
        print(self.redisData.getDesCommond(desDatas))

    def testSample(self):
        srcDatas, desDatas = self.redisData.getProDatas()
        sPSrcDatas = self.redisData.sampleSourceDatas(srcDatas, 150)
        for datas in sPSrcDatas:
            print(datas, len(sPSrcDatas[datas]))


if __name__ == '__main__':
    redisDataTuningTest = RedisDataTuningTest('/home/wxw/data/RedisData')
    redisDataTuningTest.testSample()
    """
    redisDataTuningTest = RedisDataTuningTest()
    Datas = redisDataTuningTest.getDatas('/home/wxw/data/RedisData')
    srcDatas, desDatas = redisDataTuningTest.splitDatas(Datas)
    srcDatas = get_puredatas(srcDatas)
    desDatas = get_puredatas(desDatas)
    redisDataTuningTest.getDesCommondTest(desDatas)
    """