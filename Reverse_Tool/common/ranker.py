from netzob.all import *
import sys

class ranker:
    def rank_dic(self, dics, reverse = False):
        try:
            dic_r = sorted(dics.items(), key = lambda x:x[1], reverse=reverse)
            return dic_r
        except Exception as e:
            print("rank ley error:" + e)

    def rank_tulple(self, datas, reverse=False, order=None):
        try:
            if order:
                dic_r = sorted(datas, key=lambda x: x[order], reverse=reverse)
            else:
                dic_r = sorted(datas, key=lambda x: x[1], reverse=reverse)
            return dic_r
        except Exception as e:
            print("rank ley error:" + e)


