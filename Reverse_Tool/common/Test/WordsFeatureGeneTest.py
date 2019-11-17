
from common.DataTuning.FeatureGenerate.WordsFGene import WordsFeatureGene


class WordsFeatureGeneTest:
    def __init__(self, words):
        self.wordsFreature = WordsFeatureGene(words)

    def freatureGene(self, messages):
        print(self.wordsFreature.cvtMsgs(messages))

if __name__ == '__main__':
    words = [('GET', 0.5), ('POST', 0.6), ('HTTP', 0.7)]
    wordsFG = WordsFeatureGeneTest(words)
    messages = ['GET aaa bbb', 'POST xxx', 'HTTP aaa bbbb']
    wordsFG.freatureGene(messages)
