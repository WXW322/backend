

class WordsFeatureGene:
    def __init__(self, words):
        self.words = words

    def cvtMsg(self, message):
        tFeature = []
        for word in self.words:
            if message.find(word[0]) != -1:
                tFeature.append(word[1])
            else:
                tFeature.append(0)
        return tFeature

    def cvtMsgs(self, messages):
        tFeatures = []
        for message in messages:
            tFeatures.append(self.cvtMsg(message))
        return tFeatures
