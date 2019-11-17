import abc
from common.Converter.base_convert import Converter
import sys

class Base_voter(metaclass=abc.ABCMeta):
    def __init__(self, vocubulary):
        self.voc = vocubulary

    @abc.abstractmethod
    def vote_for_item(self, item, start=0):
        """
        :param item:
        :param start:
        :return:
        """


    def vote_for_sequence(self, message, win_L):
        """

        :param sequence:
        :return:
        """
        msg_len = len(message)
        i = 0
        f_fres = {}
        while (i < msg_len):
            if i < msg_len - win_L:
                t_fre = self.vote_for_item(message[i:i + win_L], i)
            else:
                t_fre = self.vote_for_item(message[i:msg_len], i)
            t_f_item = i + t_fre
            if t_f_item not in f_fres:
                f_fres[t_f_item] = 1
            else:
                f_fres[t_f_item] = f_fres[t_f_item] + 1
            i = i + 1
        i = 0
        while (i < win_L):
            if i in f_fres:
                f_fres[i] = f_fres[i] * (win_L / i)
            i = i + 1
        return f_fres



    def vote_for_messages(self, messages, win_L):
        """
        :param messages:
        :return:
        """
        result = []
        for message in messages:
            result.append(self.vote_for_sequence(message, win_L))
        return result