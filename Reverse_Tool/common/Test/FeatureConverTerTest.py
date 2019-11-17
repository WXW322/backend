
from common.Converter.FeatureConVerTer import FeatureConVerTer

class FeatureConverTerTest:
    def __init__(self):
        self.fCverter = FeatureConVerTer()

    def TestWordsToFeatures(self, words, messages):
        return self.fCverter.cVertMessagesToDict(words, messages)


if __name__ == '__main__':
    featureCvert = FeatureConverTerTest()
    words = {'Get': 0.5, 'POST': 0.4, 'link': 0.1}
    msgs = ['Get it down', 'POST link Get']
    print(featureCvert.TestWordsToFeatures(words, msgs))