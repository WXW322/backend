
from django.http import HttpResponse


def hello(request):
    jsonResponse = HttpResponse('HelloWord')
    jsonResponse.__setitem__('Access-Control-Allow-Origin', '*')
    jsonResponse.__setitem__('Access-Control-Allow-Credentials', 'true')
    return jsonResponse

def ProSplitSummary(request):
    pass

def ProSplitDetail(request):
    pass
