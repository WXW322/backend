from common.Model.PrimData import primeData

class primDataDealer:
    def __init__(self, primDatas):
        self.datas = []
        for primData in primDatas:
            self.datas.append(primData)

    def getPreMessage(self, message):
        if message.dataId - 1 >= 0:
            return self.datas[message.dataId - 1]
        else:
            return None

    def generatePreMessagePairs(self, messages):
        return [(self.getPreMessage(message), message) for message in messages]

    def getNextMessage(self, message):
        if message.dataId + 1 < len(self.datas):
            return self.datas[message.dataId + 1]
        else:
            return None

    def generateNextMessagePairs(self, messages):
        return [(message, self.getNextMessage(message)) for message in messages]

