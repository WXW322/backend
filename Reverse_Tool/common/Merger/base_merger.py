from Fields_info.const_field import loc_field

class base_merger:
    def __init__(self):
        pass

    def is_merge(self, item_a, item_b):
        if(item_a.word_type == item_b.word_type and item_a.word_type == 1):
            return True
        return False

    def get_candidate_merge(self, words):
        i = 0
        while(i < len(words) - 1):
            t_last = words[i+1]
            if(self.is_merge(words[i], t_last)):
                return i
            i = i + 1
        return -1

    def merge_word(self, word_f, word_s):
        loc = (word_f.loc[0], word_s.loc[1])
        word_type = word_f.word_type
        word_merge = loc_field(loc=loc, word_type=word_type)
        return word_merge

    def merge_words(self, words):
        t_lo = 0
        while(t_lo != -1):
            t_lo = self.get_candidate_merge(words)
            if t_lo != -1:
                word_f = words[t_lo]
                word_s = words[t_lo+1]
                words_three = self.merge_word(word_f, word_s)
                words.remove(word_f)
                words.remove(word_s)
                words.append(words_three)
                words.sort(key=lambda x:x.loc[0])
        return words


    def merge_diff_borders(self, border_a, border_b):
        """
        merger different candidate borders
        :param border_a:
        :param border_b:
        :return:
        """
        set_a = set(border_a)
        set_b = set(border_b)
        merge_borders = list(set_a | set_b)
        merge_borders.sort()
        return merge_borders

Base_meger = base_merger()

if __name__ == '__main__':
    """
    locs = []
    locs.append(loc_field((0, 2), 1))
    locs.append(loc_field((2, 3), 0))
    locs.append(loc_field((3, 5), 0))
    locs.append(loc_field((5, 6), 1))
    merger = base_merger()
    for word in merger.merge_words(locs):
        print(word.loc, word.word_type)
    """
    merger = base_merger()
    b_r = merger.merge_diff_borders([1,2,3,7,9], [4,5])
    print(b_r)



