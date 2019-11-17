from common.measure_tool.measure_base import Base_measure
from common.analyzer.analyzer_common import base_analyzer

class MessageSplitMeasure(Base_measure):
    def __init__(self):
        super().__init__()
        self.analyzer = base_analyzer()

    def AlignMessage(self, MessagePre, MessageRight):
        MessageNewPre = []
        lastlo = MessageRight[-1]
        for x in MessagePre:
            if x > lastlo:
                break
            MessageNewPre.append(x)
        return MessageNewPre

    def MeasureMessage(self, MessagePre, MessageRight):
        MessagePre = self.AlignMessage(MessagePre, MessageRight)
        return self.analyzer.get_f1(MessagePre, MessageRight)


    def Measure(self, DataTrue, DataPrefict):
        facc = 0
        frecall = 0
        f1 = 0
        i = 0
        while(i < len(DataTrue)):
            tempdata = self.MeasureMessage(DataPrefict[i], DataTrue[i])
            facc = facc + tempdata[0]
            frecall = frecall + tempdata[1]
            f1 = f1 + tempdata[2]
            i = i + 1
        return (facc/len(DataTrue), frecall/len(DataTrue), f1/len(DataTrue))


