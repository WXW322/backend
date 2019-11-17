
class DisWords:
    def __init__(self):
        pass

    def measureWords(self, wA, wB):
        lenMin = min(len(wA), len(wB))
        lo  =  -1
        for i in range(1, lenMin):
            if(i < lenMin and wA[-i:-1] + wA[-1:] == wB[0:i]):
                lo = i
            i = i + 1
        if lo == -1:
            return 0
        else:
            return lo

    def measureWList(self, words):
        wordsDis = [[0 for j in range(len(words))] for i in range(len(words))]
        for i in range(len(words)):
            for j in range(len(words)):
                if i == j:
                    wordsDis[i][j] = 0
                else:
                    wordsDis[i][j] = self.measureWords(words[i], words[j])
        return wordsDis

if __name__ == '__main__':
    disWords = DisWords()
    words = ['0_0_1', '0_1_2', '3_2_1']
    wordsList = []
    for word in words:
        wordsList.append(word.split('_'))
    print(disWords.measureWList(wordsList))