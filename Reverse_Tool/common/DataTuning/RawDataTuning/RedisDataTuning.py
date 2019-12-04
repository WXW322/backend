
from netzob.all import *
from common.readdata import *
from common.Converter.MessageConvert import MessageConvert

class RedisDataTuning:
    def __init__(self, path = '/home/wxw/data/RedisData'):
        self.msgConvert = MessageConvert()
        self.path = path
        self.cmds = [b'SADD', b'LLEN', b'STRLEN', b'SET',
                     b'SMEMBERS', b'MSET', b'SELECT',
                     b'LPUSH', b'MGET', b'GET', b'LPOP']

    def readDatas(self, path='/home/wxw/data/RedisData'):
        redisDatas = read_datas(path, 'single')
        return redisDatas

    def sampleDatas(self):
        datas = self.readDatas()
        srcDatas, desDatas = self.splitByPureDatas(datas)
        splitSrcDatas = self.sampleSourceDatas(srcDatas, 2)
        print(len(splitSrcDatas))
        return splitSrcDatas


    def splitByDire(self, datas):
        srcDatas, desDatas = self.msgConvert.clsMessageByDire(datas)
        return srcDatas, desDatas

    def splitByPureDatas(self, datas):
        srcDatas, desDatas = self.splitByDire(datas)
        return get_puredatas(srcDatas), get_puredatas(desDatas)

    def getProDatas(self):
        datas = self.readDatas(self.path)
        srcDatas, desDatas = self.splitByPureDatas(datas)
        return srcDatas, desDatas

    def getSouceCommond(self, srcDatas):
        srcCommond = {}
        srcOne = {}
        for srcData in srcDatas:
            srcSplitData = srcData.split(b'\r\n')
            srcDataCommond = srcSplitData[2]
            if srcDataCommond not in srcCommond:
                srcCommond[srcDataCommond] = 0
            srcCommond[srcDataCommond] = srcCommond[srcDataCommond] + 1
            srcDataOne = srcSplitData[0]
            if srcDataOne not in srcOne:
                srcOne[srcDataOne] = 0
            srcOne[srcDataOne] = srcOne[srcDataOne] + 1
        return srcCommond, srcOne

    def sampleSourceDatas(self, srcDatas, msgLen, dataLen=300):
        srcCDatas = {}
        for srcData in srcDatas:
            srcSplitData = srcData.split(b'\r\n')
            srcC = srcSplitData[msgLen]
            if srcC not in srcCDatas:
                srcCDatas[srcC] = []
            if len(srcCDatas[srcC]) < dataLen:
                srcCDatas[srcC].append(srcData)
        srcDatasList = []
        for key in srcCDatas:
            print(key)
            srcDatasList.extend(srcCDatas[key])
        return srcDatasList

    def sampleDesDatas(self, desSrcDatas, dataLen=300):
        desDatas = {}
        for desData in desSrcDatas:
            if desData[0] not in desDatas:
                desDatas[desData[0]] = []
            desDatas[desData[0]].append(desData)
        Fdatas = []
        Fdatas.extend(desDatas[b'+'])
        Fdatas.extend(desDatas[b'-'])
        return Fdatas


    def getDesCommond(self, desDatas):
        desCommond = {}
        desCommondS = {}
        desCommonT = {}
        for desData in desDatas:
            desSplitData = desData.split(b'\r\n')
            desDataCommond = desSplitData[0]
            if desDataCommond not in desCommond:
                desCommond[desDataCommond] = 0
            desCommond[desDataCommond] = desCommond[desDataCommond] + 1
            if len(desSplitData) > 1:
                desDataCommondS = desSplitData[1]
                if desDataCommondS not in desCommondS:
                    desCommondS[desDataCommondS] = 0
                desCommondS[desDataCommondS] = desCommondS[desDataCommondS] + 1
            if len(desSplitData) > 2:
                desDataCommondT = desSplitData[2]
                if desDataCommondT not in desCommonT:
                    desCommonT[desDataCommondT] = 0
                desCommonT[desDataCommondT] = desCommonT[desDataCommondT] + 1
        return self.filterDatas(desCommond), self.filterDatas(desCommondS), self.filterDatas(desDataCommondT)

    def getMsgsLen(self, clses):
        correLen = 0
        conciouLen = 0
        print(len(clses))
        clsCmds = []
        for cls in clses:
            clsCmd = MessageConvert.clsMsgsByRegix(self.cmds, 20, cls)
            clsCmds.append(clsCmd)
        for clscmd in clsCmds:
            if len(clscmd) == 1:
                #print(clscmd)
                correLen = correLen + 1
        for cmd in self.cmds:
            tLo = 0
            for clscmd in clsCmds:
                if cmd in clscmd:
                    tLo = tLo + 1
            if tLo == 1:
                #print('ss ',cmd)
                conciouLen = conciouLen + 1
        print(correLen, conciouLen)






    def filterDatas(self, datas):
        tNewDatas = {}
        for data in datas:
            if datas[data] > 5:
                tNewDatas[data] = datas[data]
        return tNewDatas




if __name__ == '__main__':
    redisDataTuning = RedisDataTuning()
    redisDataTuning.sampleDatas()
    """
    datas = redisDataTuning.readDatas('/home/wxw/data/RedisData')
    srcDatas, desDatas = redisDataTuning.splitByDire(datas)
    srcDatas = get_puredatas(srcDatas)
    cmdOne, cmdTwo = redisDataTuning.getSouceCommond(srcDatas)
    print(cmdOne)
    print(cmdTwo)
    """
    #print(redisDataTuning.getSouceCommond(srcDatas))