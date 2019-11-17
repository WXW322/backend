



def get_evisession(datas,t_lo,gap):
    t_result = {}
    for data in datas:
        t_key = data.data[t_lo:t_lo+gap]
        if t_key not in t_result:
            t_result[t_key] = []
            t_result[t_key].append(data)
        else:
            t_result[t_key].append(data)
    return t_result

def clusession_byt(datas,t_time):
    length = len(datas)
    i = 0
    t_result = []
    while(i < length - 1):
        t_r = []
        t_r.append(datas[i])
        j = 1
        while(j + i < length):
            t_lo = i + j
            if(datas[t_lo].date - t_r[-1].date > t_time):
                break;
            else:
                t_r.append(datas[t_lo])
            j = j + 1
        t_result.append(t_r)
        i = i + j
    return t_result

def test_rate(result,t_lo,gap):
    t_zhichi = 0
    for t_r in result:
        t_len = len(t_r)
        if(t_len > 0):
            t_s = t_r[0].data[t_lo:t_lo+gap]
        else:
            continue
        j = 1
        t_lo = 0
        while(j < t_len):
            if(t_r[j].data[t_lo:t_lo+gap] != t_s):
                t_lo = 1
                break
            j = j + 1
        if t_lo == 0:
            t_zhichi = t_zhichi + 1
    return float(t_zhichi)/float(len(result))








