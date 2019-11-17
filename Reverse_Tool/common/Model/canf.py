
class prime_b:
    def __init__(self, message, boundaries):
        self.message = message
        self.boundaries = boundaries;
        self.loc = 0

    def nextLoc(self):
        if(self.loc < len(self.datas) - 1):
            self.loc = self.loc + 1
        return self.datas[self.loc]

    def now(self):
        return self.datas[self.loc]

    def getData(self, loc):
        return self.message[loc[0]:loc[1]]
