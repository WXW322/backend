
class ngaram_order:
    def __init__(self, order_words):
        self.order_words = order_words

    def vote_single_message(self, message):
        for key in t_los:
            t_now = t_los[key]
            pre_key = key - 1
            last_key = key + 1
            t_pre = 0 if pre_key not in t_los else t_los[pre_key]
            t_last = 0 if last_key not in t_los else t_los[last_key]