
from django.http import HttpResponse
import json
from BinaryProtocol.Logic.MsgForMatG import MsgForMatG


def hello(request):
    jsonResponse = HttpResponse('HelloWord')
    jsonResponse.__setitem__('Access-Control-Allow-Origin', '*')
    jsonResponse.__setitem__('Access-Control-Allow-Credentials', 'true')
    return jsonResponse

def ProSplitSummary(request):
    pass

def ProSplitDetail(request):
    pass

def getPostJson(request):
    datas = request.POST.items()
    keys = []
    for data in datas:
        keys.append(data[0])
    sendDatas = json.loads(keys[0])
    return sendDatas

def getFormatTree(request):
    postDatas = getPostJson(request)
    protocolType = postDatas['protocolType']
    msgF = MsgForMatG()
    treeDatas = msgF.msgToTree(filePath='aaa')
    return HttpResponse(json.dumps(treeDatas), content_type='application/json')
