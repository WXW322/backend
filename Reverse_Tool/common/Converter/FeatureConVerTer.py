
from common.Converter.base_convert import Converter

class FeatureConVerTer(Converter):
    def __init__(self):
        super().__init__()

    def cVertMessageToDict(self, words, message):
        mFeature = []
        for word in words:
            if message.find(word) != -1:
                mFeature.append(words[word])
            else:
                mFeature.append(0)
        return mFeature

    def cVertMessagesToDict(self, words, messages):
        mFeatures = []
        for message in messages:
            mFeatures.append(self.cVertMessageToDict(words, message))
        return mFeatures
