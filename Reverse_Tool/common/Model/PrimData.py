
class primeData:
    def __init__(self, message, boundaries, dataId):
        self.dataId = dataId
        self.message = message
        self.boundaries = boundaries
        self.loc = 0
        self.relaloc = 0

    def nextLoc(self):
        if(self.loc < len(self.boundaries) - 1):
            self.loc = self.loc + 1
        return self.boundaries[self.loc] - self.relaloc
        #return self.boundaries[self.loc] - self

    def updateLo(self):
        self.relaloc = self.boundaries[self.loc]

    def now(self):
        return self.boundaries[self.loc] - self.relaloc
        #return self.boundaries[self.loc]

    def getData(self, loc):
        return self.message[loc[0]:loc[1]]

    def getNowData(self):
        return self.message[self.boundaries[self.loc-1]: self.boundaries[self.loc]]
