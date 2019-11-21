import sys

class Desiner:
    def __init__(self):
        pass

    def VoteSingleByDicParas(self, veParas, messageLos):
        diffMeasure = veParas['diff_measure']
        vWay = veParas['vWay']
        T = veParas['T']
        r = veParas['r']
        return self.VoteSingleM(messageLos, diffMeasure, vWay, T, r)

    def VoteMultyByDicParas(self, veParas, messageLos):
        diffMeasure = veParas['diff_measure']
        vWay = veParas['vWay']
        T = veParas['T']
        r = veParas['r']
        return self.addHead([self.VoteSingleM(messageLo, diffMeasure, vWay, T, r) for messageLo in messageLos])

    def addHead(self, boundaries):
        multyBorders = []
        for boudary in boundaries:
            boudary.insert(0 , 0)
            sorted(boudary)
            print(boudary)
            multyBorders.append(boudary)
        return multyBorders



    def VoteSingleM(self, messagelo, diff_measure, way,T = 0,r = 0):
        """
        funtion: get final los for one messages
        t_los:vote locations(dict)
        way:vote strategy:str
        T:vote threshold:int
        return: final locations(set)
        """
        t_flos = []
        for key in messagelo:
            t_now = messagelo[key]
            pre_key = key - 1
            last_key = key + 1
            t_pre = 0 if pre_key not in messagelo else messagelo[pre_key]
            t_last = 0 if last_key not in messagelo else messagelo[last_key]
            if diff_measure == "abs" and way == "normal":
                if t_now > T and t_now > t_pre and t_now > t_last:
                    t_flos.append(key)
            elif diff_measure == "abs" and way == "loose":
                if key != 1:
                    if t_now > T and ((t_now > t_pre) or (t_now > t_last)):
                        t_flos.append(key)
                else:
                    if t_now > T and ((t_now > t_pre) and (t_now > t_last)):
                        t_flos.append(key)
            elif diff_measure == "re" and way == "normal":
                if key != 1:
                    if t_now > T and (((t_pre == 0) or (t_now/t_pre > 1 + r)) and ((t_last == 0) or (t_now/t_last > 1 + r))):
                        t_flos.append(key)
                else:
                    if t_now > T and ((t_last == 0) or (t_now/t_last > 1 + r)):
                        t_flos.append(key)
            elif diff_measure == "re" and way == "loose":
                if key != 1:
                    if t_now > T and (((t_pre == 0) or (t_now/t_pre > 1 + r)) or ((t_last == 0) or (t_now/t_last > 1 + r))):
                        t_flos.append(key)
                else:
                    if t_now > T and ((t_last == 0) or (t_now/t_last > 1 + r)):
                        t_flos.append(key)
            else:
                print("error")
        return t_flos

    def VoteMultiM(self, Messages, diff_measure, way, T = 0, r = 0):
        ResultLos = []
        for message in Messages:
            ResultLos.append(self.VoteSingleM(message, diff_measure, way, T, r))
        return ResultLos


