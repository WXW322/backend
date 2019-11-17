
class word_infer:
    def __init__(self):
        pass

    def is_const_word(self, words, T):
        if type(words) == list:
            words = sorted(words, key= lambda x:x ,reverse=True)
        elif type(words) == dict:
            words = sorted(words.items(), key= lambda x:x[1] ,reverse=True)
        if words[0][1] > T:
            return True
        else:
            return False

    def is_len(self):
        pass

    def is_ids(self):
        pass


