from netzob.all import *
from treelib import *
import numpy as np
import sys
import time
from ngrambuild.pyngram import voters
from common.classer.parse import parse
from common.readdata import *
from common.output import R_out
import time
from Inferformat.treef_loc import treefL
from Inferformat.node import node
from common.f_cg import transer
from Inference.words_deal import message_dealer

class gformat:
    def __init__(self):
        self.vote_fs = None
        self.vote_es = None
        self.lo_f = None
        self.lo_e = None
        self.f_los = None

    def loctotree(self, candidate_locs):
        prim_los = {}
        for i,item in enumerate(candidate_locs):
            prim_los[i] = item
        tree_generater = treefL(prim_los, 0.1 * len(candidate_locs), 0.2)
        t_format_tree = tree_generater.generate_T()
        t_format_tree.depth_traverse()
        return t_format_tree




    def get_format(self,format_type, messages, h, combine, model, v_way, T=0, r=0, ways="g"):
        """
        get single format
        """
        voter = voters()
        infer_format = None
        if format_type == "ies":
            infer_format = voter.get_info(messages, h, combine, model, v_way, T, r, ways)
        elif format_type == "tree":
            prime_los = voter.single_message_voter(messages, h, combine, model, v_way, T, r)
            infer_format = self.loctotree(prime_los)
        return infer_format

    def get_formats(self,messages,rules,clus,h,ways,combine,model,v_way,T=0,r=0):
        t_data = None
        paser = parse()
        t_formats = {}
        if rules == "lo":
            t_data,_ = paser.cls_fun(messages,clus[0],clus[1])
        for key in t_data:
            t_formats[key] = cutmessage(t_data[key],clus[1])
            l_num = 0
            if len(t_formats[key]) < 100:
                continue
            t_formats[key] = add_tail(t_formats[key],h)
            t_formats[key] = self.get_format(t_formats[key],h,ways,combine,model,v_way,len(t_formats[key])*T,r = r)
        return t_formats

   

def get_f(T_path,data_path,r_way,rules,clus,h,ways,combine,model,v_way,T,r):
    datas = read_datas(data_path,r_way)
    datas_src,datas_des = clusbydesT(datas)
    datas_src = get_puredatas(datas_src)
    datas_des = get_puredatas(datas_des)
    f_name = "tempone" + str(h) + ways + combine + model + v_way + str(T) + str(r) + ".txt" 
    out_f = R_out()
    out_f.set_path(T_path,f_name)
    out_f.trans_out()
    g_f = gformat()
    t_f = g_f.get_formats(datas_des,rules,clus,h,ways,combine,model,v_way,T,r)
    print("des")
    out_f.print_dic(t_f)
    print("src")
    t_f = g_f.get_formats(datas_src,rules,clus,h,ways,combine,model,v_way,T,r)
    out_f.print_dic(t_f)
    out_f.back_out()
 


def get_common(T_path,data_path,r_way,h,ways,combine,model,v_way,T,r,R_los):
    datas = read_datas(data_path,r_way)
    datas = get_puredatas(datas)
    messages = add_tail(datas,h)
    f_name = str(h) + ways + combine + model + v_way + str(T) + str(r) +str(time.time()) + ".txt" 
    out_f = R_out()
    out_f.set_path(T_path,f_name)
    out_f.trans_out()
    print(h,ways,combine,model,v_way,T,r)
    g_f = gformat()
    t_f = g_f.get_format(datas,h,ways,combine,model,v_way,T,r)
    f_trans = transer()
    borders_pre = f_trans.border2item(t_f)
    M_dealer = message_dealer()
    M_dealer.set_conlo(borders_pre)
    M_dealer.set_rlo(R_los)
    M_dealer.get_f1()
    M_dealer.set_dataM(messages)
    print("after")
    M_dealer.resplit("yes")
    M_dealer.reclus("yes")
    M_dealer.get_f1()
    out_f.back_out()

def get_prime(data_path, r_way, h, combine, model, v_way, T, r):
    datas = read_datas(data_path,r_way)
    datas = get_puredatas(datas)
    messages = add_tail(datas,h)
    g_f = gformat()
    t_f = g_f.get_format('tree', messages, h, combine, model, v_way, T, r)
    t_f.print_tree('single')




#for key in t_f:
#    print(key,t_f[key])
#parameters = [i*0.1 for i in range(1,11)]

#for h in [2,4]:
#get_common("/home/wxw/paper/researchresult/modbus/bordertwo","/home/wxw/data/modbusdata/","single",h,"g","no","re","normal",0.1,0.1,[(0,2),(2,5),(5,6),(6,7),(7,8)])

#   get_common("/home/wxw/paper/researchresult/iec104/bordertwo/","/home/wxw/data/iec104/","single",h,"g","no","re","loose",0.1,0.1,[(0,1),(1,2),(2,4),(4,6),(6,7),(7,8),(8,9),(9,10),(10,12)])
    
    #get_common("/home/wxw/paper/researchresult/cip/borderfour","/home/wxw/data/cip_datanew/","single",h,"g","no","re","loose",0.1,0.9,[(0, 2), (2, 4), (4, 8), (8, 12), (12, 20), (20, 24)])


get_prime("/home/wxw/data/iec104_test","single",4,"yes","abs","normal", 0, 0)
"""
get_common("/home/wxw/paper/researchresult/modbus/bordertwo","/home/wxw/data/modbusdata/","single",4,"g","no","re","loose",0.1,0.1,[(0,2),(2,5),(5,6),(6,7),(7,8)])

get_common("/home/wxw/paper/researchresult/modbus/bordertwo","/home/wxw/data/modbusdata/","single",3,"g","no","re","normal",0.1,0.1,[(0,2),(2,5),(5,6),(6,7),(7,8)])

get_common("/home/wxw/paper/researchresult/modbus/bordertwo","/home/wxw/data/modbusdata/","single",3,"g","no","re","loose",0.1,0.1,[(0,2),(2,5),(5,6),(6,7),(7,8)])
start = time.time()
    
get_common("/home/wxw/paper/researchresult/iec104/bordertwo","/home/wxw/data/iec104/","single",4,"g","no","re","normal",0.1,0.1,[(0,1),(1,2),(2,4),(4,6),(6,7),(7,8),(8,9),(9,10),(10,12)])

get_common("/home/wxw/paper/researchresult/iec104/bordertwo/","/home/wxw/data/iec104/","single",4,"g","no","re","loose",0.1,0.1,[(0,1),(1,2),(2,4),(4,6),(6,7),(7,8),(8,9),(9,10),(10,12)])

get_common("/home/wxw/paper/researchresult/iec104/bordertwo","/home/wxw/data/iec104/","single",3,"g","no","re","normal",0.1,0.1,[(0,1),(1,2),(2,4),(4,6),(6,7),(7,8),(8,9),(9,10),(10,12)])


get_common("/home/wxw/paper/researchresult/iec104/bordertwo","/home/wxw/data/iec104/","single",3,"g","no","re","loose",0.1,0.1,[(0,1),(1,2),(2,4),(4,6),(6,7),(7,8),(8,9),(9,10),(10,12)])
end = time.time()
print(end - start)
"""
#get_common("/home/wxw/paper/researchresult/cip/borderthree","/home/wxw/data/cip_datanew/","single",4,"g","no","re","normal",0.1,0.1,[(0, 2), (2, 4), (4, 8), (8, 12), (12, 20), (20, 24)])

#get_common("/home/wxw/paper/researchresult/cip/borderthree","/home/wxw/data/cip_datanew/","single",4,"g","no","re","loose",0.1,0.1,[(0, 2), (2, 4), (4, 8), (8, 12), (12, 20), (20, 24)])

#get_common("/home/wxw/paper/researchresult/cip/borderthree","/home/wxw/data/cip_datanew/","single",3,"g","no","re","normal",0.1,0.1,[(0, 2), (2, 4), (4, 8), (8, 12), (12, 20), (20, 24)])

#get_common("/home/wxw/paper/researchresult/cip/borderfour","/home/wxw/data/cip_datanew/","single",3,"g","no","re","loose",0.1,0.9,[(0, 2), (2, 4), (4, 8), (8, 12), (12, 20), (20, 24)])
#last = time.time()
#print(last - end)

#get_f("/home/wxw/paper/researchresult/iec104/format","/home/wxw/data/iec104/","multiple","lo",(6,7),3,"g","no","re","normal",0.8,0.1)

#get_f("/home/wxw/paper/researchresult/modbus/format","/home/wxw/data/modbusdata/","multiple","lo",(7,8),3,"g","no","re","normal",0.8,0.1)


#get_f("/home/wxw/paper/researchresult/modbus/format","/home/wxw/data/modbusdata/","multiple","lo",(7,8),3,"g","no","abs","loose",0.1,0.1)

#get_f("/home/wxw/paper/researchresult/modbus/format","/home/wxw/data/modbusdata/","multiple","lo",(7,8),3,"g","no","re","loose",0.1,0.1)






