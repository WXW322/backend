
from common.Spliter.vertical_splitter import vertical_splitter
from common.Merger.base_merger import base_merger
from Inferformat.node import node
from common.FieldTypeInfer.WholeFieldTypeInfer import WholeFieldTypeInfer

class ReAjustLogic:
    def __init__(self, words, msgs):
        self.words = words
        self.msgs = msgs
        self.wholeTypeInfer = WholeFieldTypeInfer(self.msgs)

    def reSplit(self):
        self.words.sort(key =lambda word:word[0])
        t_len = len(self.words)
        i = 0
        while (i < t_len):
            t_idom = self.words[i]
            t_pre = t_idom[0]
            t_last = t_idom[1]
            t_middle = t_pre + 1
            if (t_idom[1] - t_idom[0] >= 2):
                if(((self.wholeTypeInfer.inferConst((t_pre, t_middle))) and not (self.wholeTypeInfer.inferConst((t_middle, t_last))))
                    or ((self.wholeTypeInfer.inferConst((t_middle, t_last))) and not (self.wholeTypeInfer.inferConst((t_pre, t_middle))))):
                    self.words.remove(t_idom)
                    self.words.append((t_pre, t_middle))
                    self.words.append((t_middle, t_last))
                    self.words.sort(key =lambda word:word[0])
                    t_len = t_len + 1
            i = i + 1


    def reCluster(self):
        t_len = len(self.words)
        i = 0
        while(i < t_len - 1):
            t_next = self.words[i+1]
            t_now = self.words[i]
            if self.wholeTypeInfer.inferConst((t_now)) and self.wholeTypeInfer.inferConst((t_next)):
                t_s = t_now[0]
                t_e = t_next[1]
                self.words.remove(t_now)
                self.words.remove(t_next)
                self.words.append((t_s, t_e))
                t_len = t_len - 1
                i = i - 1
            i = i + 1


    def reAjustBorders(self, words, messages):
        vSpliter = vertical_splitter(messages)
        words = vSpliter.splitWordsSimple(words)
        Nodes = []
        typeInfer = WholeFieldTypeInfer(messages)
        mgerItoms = base_merger()
        for word in words:
            if typeInfer.inferConst(word):
                tNode = node(loc=word, wType=1)
            else:
                tNode = node(loc=word, wType=6)
            Nodes.append(tNode)
        return mgerItoms.merge_words(Nodes)



