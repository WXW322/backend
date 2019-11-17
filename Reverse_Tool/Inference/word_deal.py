# coding=utf-8
from netzob.all import *
import math
import os
import sys
from Inference.words_basic import words_base
from common.readdata import *
from common.Converter.base_convert import Converter
from common.analyzer.analyzer_common import base_analyzer

class message_dealer:
    def __init__(self):
        self.MaxLen = 40
        self.lengthThreshold = 0.8
        self.constThreshold = 0.98
        self.idThreshold = 0.7



    def set_conlo(self,los):
        self.condilo = los

    def set_rlo(self,los):
        self.rightlo = los
    
    def set_dataM(self,messages):
        self.messages = messages

    def find_constone(self, datas):
        wordDic = Converter.convert_raw_to_count(datas)
        wordDic = sorted(wordDic.items(), key = lambda x:x[1])
        if (wordDic[0][1] > self.constThreshold):
            return 1
        else:
            return 0


    def find_len(self, datas, lens):
        t_lener = words_base()
        t_dataone, t_datatwo = t_lener.get_lengthinfo(datas)
        p_one = self.pearson(t_dataone, lens)
        p_two = self.pearson(t_datatwo, lens)
        if (p_one > self.lengthThreshold or p_two > self.lengthThreshold):
            return 1
        else:
            return 0

    def find_lenbyaccuone(self, datas, lengths):
        t_lener = words_base()
        t_dataone, t_datatwo = t_lener.get_lengthinfo(datas)
        acc_big = 0
        data_nums = {}
        data_smalls = {}
        for i in range(len(t_dataone)):
            diff = abs(t_dataone[i] - lengths[i])
            if diff not in data_nums:
                data_nums[diff] = 1
            else:
                data_nums[diff] = data_nums[diff] + 1
        acc_small = 0
        for i in range(len(t_datatwo)):
            diff = abs(t_datatwo[i] - lengths[i])
            if diff not in data_smalls:
                data_smalls[diff] = 1
            else:
                data_smalls[diff] = data_smalls[diff] + 1
        for key in data_nums:
            if acc_small < data_nums[key]:
                acc_small = data_nums[key]
        for key in data_smalls:
            if acc_big < data_smalls[key]:
                acc_big = data_smalls[key]
        if ((acc_small / len(t_dataone)) > self.lengthThreshold or (acc_big / len(t_dataone)) > self.lengthThreshold):
            return 1
        else:
            return 0

    def find_lenbyaccu(self, datas, lengths):
        t_lener = words_base()
        t_messages = []
        t_dataone, t_datatwo = t_lener.get_lengthinfo(datas)
        acc_big = 0
        for i in range(len(t_dataone)):
            if (abs((t_dataone[i] - lengths[i])) <= 1):
                acc_big = acc_big + 1
        acc_small = 0
        for i in range(len(t_datatwo)):
            if (abs((t_datatwo[i] - lengths[i])) <= 1):
                acc_small = acc_small + 1
        if ((acc_small / len(t_dataone)) > self.lengthThreshold or (acc_big / len(t_dataone)) > self.lengthThreshold):
            return 1
        else:
            return 0

    def resplit(self):
        print('111')

    def ressemb(self, datas, lo):
        t_puredata = []
        for data in datas:
            t_puredata.append(data.data)
        t_listone = []
        t_listtwo = []
        for t_data in t_puredata:
            if (len(t_data) > lo):
                t_listone.append(t_data[lo-1:lo])
                t_listtwo.append(t_data[lo:lo + 1])
        print(self.huxinxi(t_listone, t_listtwo))


    def findserienum(self, datas, t_series):
        t_lener = words_base()
        t_dataone, t_datatwo = t_lener.get_seidinfo(datas)
        j_one = base_analyzer.pearson(t_dataone, t_series)
        j_two = base_analyzer.pearson(t_datatwo, t_series)
        j_final = max(j_one, j_two)
        return j_final

    def findseid(self, datas):
        ids = []
        for i,data in enumerate(datas):
            ids.append(i)
        tRate = self.findserienum(datas, ids)
        if(tRate > self.idThreshold):
            return 1
        else:
            return 0



    def find_constfunc(self, datas):
        """
        get the feature of the function code
        :param datas: List of bytes
        :return: entry and distinct num of datas
        """
        t_l = Converter.convert_raw_to_count(datas)
        t_en = base_analyzer.get_entry([value for value in t_l.values()])
        return t_en,len(t_l)

    def findFuncRe(self,t_idoms,h_len,T=0,data="no"):
        t_max = -10000
        t_f = None
        t_es = []
        t_cs = []
        t_L = t_idoms[-1][1]
        t_E = -100
        t_C = -100
        T_f = []
        for t_idom in t_idoms:
            t_en,t_l = self.find_constfunc(t_idom[0],t_idom[1],data)
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
        return t_f, T_f

    def findFunAbs(self, datas, startLo):
        if len(datas) == 0:
            return -1
        itomLen = len(datas[0])
        TC = 255 * itomLen
        TE = base_analyzer.get_entry([1.0 / num for num in range(TC)])
        dataE, dataC = self.find_constfunc(datas)
        fValue = (1 - dataC / TC) * (1 - dataE / TE) * (1 - startLo / self.MaxLen)
        return fValue



    def getWordType(self,location,T_c,T_l,T_s):
        l_s = location[0]
        l_e = location[1]
        if (self.find_constone(l_s,l_e,T_c) == 1):
            return 1
        elif(self.find_lenbyaccu(l_s,l_e,T_l) == 1):
            return 2
        elif(self.findseid(l_s,l_e,T_s) == 1):
            return 3
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
                    if(self.find_constone(t_idom[0],t_idom[0] + 1,way) and self.find_constone(t_idom[0],t_idom[0] + 1,way) != 0):
                        t_pre = t_idom[0]
                        t_middle = t_pre + 1
                        t_last = t_idom[1]
                        self.condilo.remove(t_idom)
                        self.condilo.append((t_pre, t_middle))
                        self.condilo.append((t_middle, t_last))
                        self.condilo.sort(key=self.takefirst)
                        t_len = t_len + 1
                    elif(self.find_constone(t_idom[0] + 1,t_idom[1],way) and self.find_constone(t_idom[0] + 1,t_idom[1],way) != 0):
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

    def extract_words(self,t_idoms,head,T_c,T_l,T_I):
        print(head)
        print(t_idoms)
        for t_idom in t_idoms:
            if t_idom[1] > head:
                t_idoms.remove(t_idom)
        t_words = {}
        for t_idom in t_idoms:
            t_info = self.get_loinfo(t_idom,T_c,T_l,T_I)
            if t_info != 4:
                t_words[t_idom] = t_info
        t_funcs = []
        for t_idom in t_idoms:
            if(t_idom not in t_words):
                t_funcs.append(t_idom)
        t_funw,_ = self.find_func(t_funcs,head)
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
        t_funw,T_f = self.find_func(t_funcs,head,T,data="yes")
        for t_f in T_f:
            t_words[t_f] = 0
        for t_idom in t_idoms:
            if t_idom not in t_words:
                t_words[t_idom] = 6
        print(t_words)
        return t_words




def t_fone(s_file,r_outdir,t_s,t_r,T_c,T_l,T_I):
    Me = message_dealer()
    Me.read_datas(s_file)
    standardout = sys.stdout
    #outpath = r_outdir
    # outpath = os.path.join(r_outdir,'mout')
    #fileone = open(outpath, 'w+')
    #sys.stdout = fileone
    transer = f_cg.transer()
    t_s = transer.border2item(t_s)
    Me.set_conlo(t_s)
    Me.set_rlo(t_r)
    #Me.resplit()
    #Me.reclus()
    #Me.get_f1()
    #t_head = Me.find_head()
    #t_fhead = min(23,t_head + 2)
    words_path = os.path.join(r_outdir,'temp' + str(T_c) + str(T_l) + str(T_I) + 'words_twoout')
    t_fhead = transer.get_range(0.8,Me.messages)
    t_w = open(words_path,'w+')
    sys.stdout = t_w
    t_idoms = Me.condilo
    t_results = Me.extract_words(t_idoms,t_fhead,T_c,T_l,T_I)
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


def get_compaire():
    s = [9, 12, 24]
    rights = [[(0,2),(2,5),(5,6),(6,7),(7,8)], [(0,1),(1,2),(2,4),(4,6),(6,7),(7,8),(8,9),(9,10),(10,12)], [(0, 2), (2, 4), (4, 8), (8, 12), (12, 20), (20,24)]]
    pathsf = ['/home/wxw/data/modbusdata/', '/home/wxw/data/iec104/', '/home/wxw/data/cip_datanew/']
    pathst = ['/home/wxw/paper/researchresult/icccn/modbuswc.txt', '/home/wxw/paper/researchresult/icccn/iec104wc.txt', '/home/wxw/paper/researchresult/icccn/cipwc.txt']
    Me = message_dealer()
    for i in range(3):
        t_pathf = pathsf[i]
        t_pathst = pathst[i]
        temp_file = open(t_pathst, 'w+')
        sys.stdout = temp_file
        t_ftype = {}
        Me.read_datas(t_pathf)
        for lo in rights[i]:
            t_type =  Me.find_len(lo[0], lo[1])
            t_ftype[lo] = t_type
        print(t_ftype)
        temp_file.close()


