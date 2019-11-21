

class BaseClasser:
    def __init__(self):
        pass

    def clsMsgs(self, results, messages):
        dataLabels = results.labels_
        i = 0
        clsMessages = {}
        while (i < len(dataLabels)):
            key = dataLabels[i]
            if key not in clsMessages:
                clsMessages[key] = []
            clsMessages[key].append(messages[i])
            i = i + 1
        return clsMessages
