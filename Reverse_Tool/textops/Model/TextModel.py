
from common.Model.PrimData import primeData

class TextModel(primeData):
    def __init__(self, message, boundaries, id):
        super().__init__(message, boundaries, id)

    def now(self):
        return self.boundaries[self.loc]

    def nextLoc(self):
        self.loc = self.loc + 1


