from netzob.all import *


class NetZobFormatInfer:
    def __init__(self):
        pass

    def clsMessages(self, messages):
        msgs = []
        for message in messages:
            tMsg = RawMessage(message)
            msgs.append(tMsg)
        ff = Format()
        clustering = ff.clusterByAlignment(messages = msgs, minEquivalence = 50)
        for f in clustering:
            print(f._str_debug())


    def getSymbol(self, datas):
        pass