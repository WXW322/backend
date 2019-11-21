
class TextFormMeasureLogic:
    def __init__(self):
        pass

    def measureTextForm(self, formA, formB):
        tA = 0
        tB = 0
        for fA in formA:
            if fA in formB:
                tA = tA + 1
        for fB in formB:
            tNum = 0
            for fA in formA:
                if fA == fB:
                    tNum = tNum + 1
            if tNum == 1:
                tB = tB + 1
        return tA / len(formA), tB / len(formB)