
from common.Model.PrimData import primeData

class TextModel(primeData):
    def __init__(self, message, boundaries, id, h=1):
        super().__init__(message, boundaries, id)
        self.h = h

    def now(self, h=0):
        if self.h == 0:
            return self.boundaries[self.loc]
        else:
            nowData = b''
            i = 0
            while(i <= self.h and i < len(self.boundaries)):
                nowData = nowData + self.boundaries[i]
                i = i + 1
            return nowData


    def nextLoc(self):
        self.loc = self.loc + 1


