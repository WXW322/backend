# coding=utf-8
from netzob.all import *
import struct
import math
import os
import sys
from protocol_analysis.words_basic import words_base
import numpy as np

from deal_data.session_deal import session_deal

class message_dealer:
    def __init__(self):
        self.messages = None
        self.semessages = None
        self.condilo = None
        self.rightlo = None
        self.conborders = None
        self.rborders = None

    def read_datas(self,dirs):
        paths = os.listdir(dirs)
        t_datas = []
        t_sedatas = []
        for path in paths:
            t_path = os.path.join(dirs,path)
            t_data = PCAPImporter.readFile(t_path).values()
            t_datas.extend(t_data)
            t_sedatas.append((t_data,path))
        self.messages = t_datas
        self.semessages = t_sedatas

    def set_conlo(self,los):
        self.condilo = los

    def set_rlo(self,los):
        self.rightlo = los
    
    def set_dataM(self,messages):
        self.messages = messages


    def clus_sesionbydi(self,messages,data="no"):
        src = self.get_ip(messages[0].source)
        des = self.get_ip(messages[0].destination)
        srcs = []
        dess = []
        for message in messages:
            if(self.get_ip(message.source) == src):
                srcs.append(message)
            else:
                dess.append(message)
        return srcs,dess





    def find_constone(self, lo_b, lo_e,data="no"):
        # develop absolute or relative
        conster = words_base()
        t_messages = []
        if data == "no":
            for message in self.messages:
                t_messages.append(message.data)
        else:
            t_messages = self.messages
        t_r, t_l,_,_,_ = conster.get_logapinfo(t_messages,lo_b,lo_e)
        if (t_l[0][1] > 0.98):
            return 1
        else:
            return 0

    def get_constone(self,lo_b,lo_e):
        conster = words_base()
        t_messages = []
        for message in self.messages:
            t_messages.append(message.data)
        t_r, t_l, _ = conster.get_pureproinfo(t_messages, lo_b, lo_e)
        return int.from_bytes(t_l[0][0],byteorder='little',signed=False)

    def pearson(self, vector1, vector2):
        n = len(vector1)
        sum1 = sum(float(vector1[i]) for i in range(n))
        sum2 = sum(float(vector2[i]) for i in range(n))
        sum1_pow = sum([pow(v, 2.0) for v in vector1])
        sum2_pow = sum([pow(v, 2.0) for v in vector2])
        p_sum = sum([vector1[i] * vector2[i] for i in range(n)])
        num = p_sum - (sum1 * sum2 / n)
        den = math.sqrt((sum1_pow - pow(sum1, 2) / n) * (sum2_pow - pow(sum2, 2) / n))
        if den == 0:
            return 0.0
        return num / den

    def caculate_prob(self, vector):
        t_r = {}
        for v in vector:
            if v not in t_r:
                t_r[v] = 1
            else:
                t_r[v] = t_r[v] + 1
        for key in t_r:
            t_r[key] = t_r[key] / len(vector)
        return t_r

    def huxinxi(self, vectorone, vectortwo):
        vectorthree = []
        for i in range(len(vectorone)):
            vectorthree.append(vectorone[i] + vectortwo[i])
        t_probone = self.caculate_prob(vectorone)
        t_probtwo = self.caculate_prob(vectortwo)
        t_probsum = self.caculate_prob(vectorthree)
        t_info = 0
        for key_one in t_probone:
            for key_two in t_probtwo:
                if key_one + key_two not in t_probsum:
                    continue
                t_info = t_info + t_probsum[key_one + key_two] * np.log(
                    t_probsum[key_one + key_two] / (t_probone[key_one] * t_probtwo[key_two]))
        return -t_info

    def find_len(self, datas, lo_s, lo_e):
        t_lener = words_base()
        t_messages = []
        for message in self.messages:
            t_messages.append(message.data)
        t_dataone, t_datatwo, t_lens = t_lener.get_lengthinfo(t_messages, lo_s, lo_e)
        print(t_datatwo)
        print(t_lens)
        p_one = self.pearson(t_dataone, t_lens)
        p_two = self.pearson(t_datatwo, t_lens)
        print(p_one)
        print(p_two)
        if (p_one > 0.9 or p_two > 0.9):
            return 1
        else:
            return 0

    def find_lenbyaccu(self, lo_s, lo_e,data="no"):
        t_lener = words_basic.words_base()
        t_messages = []
        if data == "no":
            for message in self.messages:
                t_messages.append(message.data)
        else:
            t_messages = self.messages
        t_dataone, t_datatwo, t_lens = t_lener.get_lengthinfo(t_messages, lo_s, lo_e)
        acc_big = 0
        for i in range(len(t_dataone)):
            if (abs((t_dataone[i] - t_lens[i])) <= 1):
                acc_big = acc_big + 1
        acc_small = 0
        for i in range(len(t_datatwo)):
            if (abs((t_datatwo[i] - t_lens[i])) <= 1):
                acc_small = acc_small + 1
        if ((acc_small / len(t_dataone)) > 0.8 or (acc_big / len(t_dataone)) > 0.8):
            return 1
        else:
            return 0


    def ressemb(self, datas, lo):
        t_puredata = []
        for data in datas:
            t_puredata.append(data.data)
        t_listone = []
        t_listtwo = []
        for t_data in t_puredata:
            if (len(t_data) > lo):
                t_listone.append(t_data[lo - 1:lo])
                t_listtwo.append(t_data[lo:lo + 1])
        print(self.huxinxi(t_listone, t_listtwo))


    def findserienum(self, messages, lo_s, lo_e):
        t_lener = words_base()
        t_messages = []
        for message in messages:
            t_messages.append(message.data)
        t_dataone, t_datatwo, t_series = t_lener.get_seidinfo(t_messages, lo_s, lo_e)
        j_one = self.pearson(t_dataone, t_series)
        j_two = self.pearson(t_datatwo, t_series)
        j_final = max(j_one, j_two)
        return j_final

    def findseid(self,lo_s,lo_e):
        t_serate = 0
        i = 0
        t_clus = session_deal("")
        for message in self.semessages:
            me_src,me_des = t_clus.clus_sesionbydi(message[0])
            if(len(me_src) ==0 or len(me_des) == 0):
                continue
            src_num = self.findserienum(me_src,lo_s,lo_e)
            des_num = self.findserienum(me_des,lo_s,lo_e)
            t_num = max(src_num,des_num)
            t_serate = t_serate + t_num
            i = i + 1
        t_rate = t_serate/i
        if(t_rate > 0.7):
            return 1
        else:
            return 0



    def find_constfunc(self, lo_b, lo_e,data="no"):
        conster = words_base()
        t_messages = []
        if data == "no":
            for message in self.messages:
                t_messages.append(message.data)
        else:
            t_messages = self.messages
        t_r, t_l, _ = conster.get_logapinfo(t_messages, lo_b, lo_e)
        t_en = 0
        for t_pro in t_l:
            t_en = t_en + t_pro[1] * np.log(t_pro[1])
        t_en = -t_en
        return t_en,len(t_l)

    def find_func(self,t_idoms,h_len,T=0):
        t_max = -10000
        t_f = None
        t_es = []
        t_cs = []
        t_L = t_idoms[-1][1]
        t_E = -100
        t_C = -100
        T_f = []
        for t_idom in t_idoms:
            t_en,t_l = self.find_constfunc(t_idom[0],t_idom[1])
            if t_E < t_en:
                t_E = t_en
            if t_C < t_l:
                t_C = t_l
            t_es.append(t_en)
            t_cs.append(t_l)
        t_E = t_E + 1
        t_C = t_C + 1
        i = 0
        while(i < len(t_idoms)):
            t_num = 1 - t_idoms[i][0]/t_L
            t_eum = 1 - t_es[i]/t_E
            t_cum = 1 - t_cs[i]/t_C
            t_fnum = t_num * t_eum * t_cum
            if (t_fnum > t_max):
                t_max = t_fnum
                t_f = t_idoms[i]
            if t_fnum > T:
                T_f.append(t_idoms[i])
            i = i + 1
        return t_f


    def find_head(self):
        min_len = 10000
        for message in self.messages:
            t_len = len(message.data)
            if t_len < min_len:
                min_len = t_len
        return min_len

    def get_loinfo(self,location):
        l_s = location[0]
        l_e = location[1]
        #location_f = words_deal.message_dealer(datas)
        #file = open(info_dir, 'w+')
        #sys.stdout = file
        if (self.find_constone(l_s,l_e) == 1):
            return 1
        elif(self.find_lenbyaccu(l_s,l_e) == 1):
            return 2
        elif(self.findseid(l_s,l_e) == 1):
            return 3
        else:
            return 4


    def get_datainfo(self,location,data):
        l_s = location[0]
        l_e = location[1]
        if (self.find_constone(l_s,l_e,data) == 1):
            return 1
        elif(self.find_lenbyaccu(l_s,l_e,data) == 1):
            return 2
        else:
            return 4


    def takefirst(self,elem):
        return elem[0]

    def resplit(self,way):
        self.condilo.sort(key = self.takefirst)
        t_len = len(self.condilo)
        i = 0
        while(i < t_len):
            t_idom = self.condilo[i]
            t_pre = t_idom[0]
            t_last = t_idom[1]
            t_middle = t_pre + 1
            if(t_idom[1] - t_idom[0] <= 2):
                if(t_idom[1] - t_idom[0] == 2):
                    if(self.find_constone(t_idom[0],t_idom[0] + 1,way) and self.get_constone(t_idom[0],t_idom[0] + 1,way) != 0):
                        t_pre = t_idom[0]
                        t_middle = t_pre + 1
                        t_last = t_idom[1]
                        self.condilo.remove(t_idom)
                        self.condilo.append((t_pre, t_middle))
                        self.condilo.append((t_middle, t_last))
                        self.condilo.sort(key=self.takefirst)
                        t_len = t_len + 1
                    elif(self.find_constone(t_idom[0] + 1,t_idom[1],way) and self.get_constone(t_idom[0] + 1,t_idom[1],way) != 0):
                        t_pre = t_idom[0]
                        t_middle = t_pre + 1
                        t_last = t_idom[1]
                        self.condilo.remove(t_idom)
                        self.condilo.append((t_pre, t_middle))
                        self.condilo.append((t_middle, t_last))
                        self.condilo.sort(key=self.takefirst)
                        t_len = t_len + 1
                i = i + 1
                continue
            elif(self.find_constone(t_idom[0],t_idom[1],way) == 1):
                i = i + 1
                continue
            elif(self.find_constone(t_pre,t_middle,way) or self.find_constone(t_middle,t_last,way)):
                t_pre = t_idom[0]
                t_middle = t_pre + 1
                t_last = t_idom[1]
                self.condilo.remove(t_idom)
                self.condilo.append((t_pre,t_middle))
                self.condilo.append((t_middle,t_last))
                self.condilo.sort(key = self.takefirst)
                t_len = t_len + 1
            i = i + 1
        self.condilo.sort(key = self.takefirst)

    def reclus(self,way):
        t_len = len(self.condilo)
        i = 0
        while(i < t_len - 1):
            t_next = self.condilo[i + 1]
            if(self.find_constone(self.condilo[i][0],self.condilo[i][1],way) ==1 and self.find_constone(t_next[0],t_next[1],way) == 1):
                t_s = self.condilo[i][0]
                t_e = self.condilo[i + 1][1]
                t_now = self.condilo[i]
                self.condilo.remove(t_now)
                self.condilo.remove(t_next)
                self.condilo.append((t_s,t_e))
                i = i - 1
                t_len = t_len - 1
                self.condilo.sort(key = self.takefirst)
            i = i + 1

    def extract_words(self,t_idoms,head):
        print(head)
        print(t_idoms)
        for t_idom in t_idoms:
            if t_idom[1] > head:
                t_idoms.remove(t_idom)
        t_words = {}
        for t_idom in t_idoms:
            t_info = self.get_loinfo(t_idom)
            if t_info != 4:
                t_words[t_idom] = t_info
        t_funcs = []
        for t_idom in t_idoms:
            if(t_idom not in t_words):
                t_funcs.append(t_idom)
        t_funw = self.find_func(t_funcs,head)
        t_words[t_funw] = 0
        for t_idom in t_idoms:
            if t_idom not in t_words:
                t_words[t_idom] = 6
        print(t_words)
        return t_words

    def extract_Dwords(self,t_idoms,head,T):
        t_words = {}
        for t_idom in t_idoms:
            t_info = self.get_datainfo(t_idom,data="yes")
            if t_info != 4:
                t_words[t_idom] = t_info
        t_funcs = []
        for t_idom in t_idoms:
            if(t_idom not in t_words):
                t_funcs.append(t_idom)
        t_funw,T_f = self.find_func(t_funcs,head,T)
        for t_f in T_f:
            t_words[t_f] = 0
        for t_idom in t_idoms:
            if t_idom not in t_words:
                t_words[t_idom] = 6
        print(t_words)
        return t_words

    def idomtobor(self,borders):
        t_borders = []
        for t_idom in borders:
            t_borders.append(t_idom[0])
        t_borders.append(borders[-1][1])
        return t_borders

    def get_f1(self):
        self.conborders = self.idomtobor(self.condilo)
        self.rborders = self.idomtobor(self.rightlo)
        t_H = self.rborders[-1]
        conpbors = set(self.conborders)
        rpborders = set(self.rborders)
        T_boders = set([i for i in range(t_H + 1)])
        rnborders = T_boders - rpborders
        connbors = T_boders - conpbors
        tpborders = rpborders&conpbors
        fnborders = rpborders&connbors
        fpborders = rnborders&conpbors
        tnborders = rnborders&connbors
        acc = (len(tpborders) + len(tnborders))/(len(tpborders) + len(tnborders) + len(fnborders) + len(fnborders))
        pre = len(tpborders)/(len(tpborders) + len(fpborders))
        recall = (len(tpborders)/(len(tpborders) + len(fnborders)))
        f1 = 2*pre*recall/(pre + recall)
        print("conb:",self.conborders)
        print("rb:",self.rborders)
        print("To;",T_boders)
        print("tp:",tpborders)
        print("fn:",tnborders)
        print("fp:",fpborders)
        print("tn:",tnborders)
        print("pre:",pre)
        print("recall:",recall)
        print("f1:",f1)
        return f1


    def clus_byfun(self):
        print('111')






def t_fone(s_file,r_outdir,t_s,t_r):
    Me = message_dealer()
    Me.read_datas(s_file)
    standardout = sys.stdout
    outpath = r_outdir
    # outpath = os.path.join(r_outdir,'mout')
    #fileone = open(outpath, 'w+')
    #sys.stdout = fileone
    Me.set_conlo(t_s)
    Me.set_rlo(t_r)
    Me.resplit()
    Me.reclus()
    #Me.get_f1()
    t_head = Me.find_head()
    t_fhead = min(23,t_head + 2)
    words_path = os.path.join(r_outdir,'wordsf_out')
    t_w = open(words_path,'w+')
    sys.stdout = t_w
    t_idoms = Me.condilo
    t_results = Me.extract_words(t_idoms,t_fhead)
    t_results = sorted(t_results.items(),key = lambda x:x[0][0])
    print(t_results)
    


def t_two(s_file,r_outdir,t_s,t_r):
    Me = message_dealer()
    Me.read_datas(s_file)
    standardout = sys.stdout
    #outpath = os.path.join(r_outdir,'mout')
    outpath = r_outdir
    fileone = open(outpath, 'w+')
    sys.stdout = fileone
    Me.set_conlo(t_s)
    Me.set_rlo(t_r)
    Me.get_f1()
    #t_head = Me.find_head()
    #t_fhead = min(23,t_head + 2)
    #t_fhead = t_head + 2
    #print(t_fhead)
    #words_path = os.path.join(r_outdir,'words_outnew')
    #t_w = open(words_path,'w+')
    #sys.stdout = t_w



def get_words(file_to,data_file,borders):
    temp_out = sys.stdout
    fpath = os.path.join(fpath,'f_test')
    file_out = open(fpath,'w+')
    sys.stdout = file_out
    Me = message_dealer()
    Me.read_datas(data_file)
    Me.set_conlo(borders)

    t_head = Me.find_head()
    t_fhead = min(23,t_head + 2)













"""
t_fone('/home/wxw/data/modbusdata','/home/wxw/paper/researchresult/words_find/modbus/',[(0, 2), (2, 3), (3, 5), (5, 7), (7, 8), (8, 9), (9, 11), (11, 12), (12, 14), (14, 16), (16, 17), (17, 19), (19, 20)],[(0,2),(2,4),(4,6),(6,7),(7,8)])
#t_fone('/home/wxw/data/modbusdata','/home/wxw/paper/researchresult/words_find/modbus',[(0, 2), (2, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 12), (12, 14), (14, 16), (16, 17), (17, 18), (18, 19)],[(0,2),(2,4),(4,6),(6,7),(7,8)])
#t_two('/home/wxw/data/modbusdata','/home/wxw/paper/researchresult/modbus/borders/base/fourhout',[(0, 2), (2, 5), (5, 9), (9, 11)],[(0,2),(2,4),(4,6),(6,7),(7,8)])
#t_two('/home/wxw/data/iec104','/home/wxw/paper/researchresult/iec104/borders/base/fourhout',[(0,3),(3,7),(7,10),(10,12),(12,15),(15,20),(20,23),(23,28)],[(0,1),(1,2),(2,4),(4,6),(6,7),(7,8),(8,9),(9,10),(10,12)])
t_fone('/home/wxw/data/iec104','/home/wxw/paper/researchresult/words_find/iec104/',[(0, 1), (1, 2), (2, 3), (3, 4), (4, 6), (6, 7), (7, 8), (8, 10), (10, 12),     (12, 13), (13, 15), (15, 16), (16, 18), (18, 20)],[(0,1),(1,2),(2,4),(4,6),(6,7),(7,8),(8,9),(9,10),(10,12)])
#t_two('/home/wxw/data/cip_datanew','/home/wxw/paper/researchresult/cip/borders/base/fourhout',[(0, 2), (2, 4), (4, 6), (6, 10), (10, 13), (13, 17), (17, 23), (23, 28)       , (28, 30), (30, 32), (32, 36), (36, 38), (38, 40), (40, 42)],[(0, 2), (2, 4), (4, 8), (8, 12), (12, 20), (20, 24)])
#t_fone('/home/wxw/data/cip_datanew','/home/wxw/paper/researchresult/cip/borders/ours/fourout',[(0, 2), (2, 4), (4, 6), (6, 10), (10, 13), (13, 17), (17, 23), (23, 28) , (28, 30), (30, 32), (32, 36), (36, 38), (38, 40)],[(0, 2), (2, 4), (4, 8), (8, 12), (12, 20), (20, 24)])

#t_fone('/home/wxw/data/iec104','/home/wxw/paper/researchresult/words_find/iec104',[(0, 1),(1, 2),(2, 4), (4, 6),(6, 7),(7, 9), (9, 11), (11, 12)],[(0,1),(1,2),(2,4),(4,6),(6,7),(7,8),(8,9),(9,10),(10,12)])

#t_fone('/home/wxw/data/cip_datanew','/home/wxw/paper/researchresult/words_find/cip',[(0, 2), (2, 3), (3, 4), (4, 6), (6, 7), (7, 10), (10, 11), (11, 12), (12, 15), (15, 16), (16, 17), (17, 18), (18, 20), (20, 23)],[(0, 2), (2, 4), (4, 8), (8, 12), (12, 20), (20, 23),(23, 30),(30, 33),(33, 34),(34, 35)])
"""
"""
Me = message_dealer()

Me.read_datas('/home/wxw/data/cip_datanew')
#Me.read_datas('/home/wxw/data/iec104')
#Me.read_datas('/home/wxw/data/modbusdata')
standardout = sys.stdout
file = open('/home/wxw/paper/researchresult/cip/borders/out','w+')
#file = open('/home/wxw/paper/researchresult/iec104/words/out','w+')
#file = open('/home/wxw/paper/researchresult/modbus/words_de/out','w+')
sys.stdout = file
#print(Me.get_constone(2,3))
#print(Me.get_constone(6,7))
#t_se = [(0, 2), (2, 3), (3, 4), (4, 6), (6, 7), (7, 10), (10, 11), (11, 12), (12, 15), (15, 16), (16, 18), (18, 20), (20, 23)]
#t_se = [(0, 2), (2, 5), (5, 7), (7, 8), (8, 9), (9, 11)]

#t_se = [(0, 2), (2, 5), (5, 7), (7, 8), (8, 9), (9, 11), (11, 12),(12, 14)]
t_se = [(0, 2), (2, 3), (3, 4), (4, 6), (6, 7), (7, 10), (10, 11), (11, 12), (12, 15), (15, 16), (16, 18), (18, 20), (20, 23)]

Me.set_conlo(t_se)
Me.resplit()
Me.reclus()
Me.idomtobor()
#print(Me.extract_words(t_se,23))

sys.stdout = standardout
"""
