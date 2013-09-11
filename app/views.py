import yoga
import util
import json

from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext, loader
from time import localtime

def index(request):
    context = {'studios': ['yogapod', 'yogaworkshop']}
    return render(request, 'index.html', context)

def yoga_pod_API(request):
    local_time = localtime()
    yoga_pod_data = yoga.get_yoga_pod(local_time)
    return HttpResponse(json.dumps(yoga_pod_data))

def yoga_workshop_API(request):
    local_time = localtime()
    yoga_workshop_data = yoga.get_yoga_workshop(local_time)
    return HttpResponse(json.dumps(yoga_workshop_data))

def api_call(request):
    studio = request.GET.get('studio', None)
    local_time = localtime()

    if studio == 'yogapod':
        data = yoga.get_yoga_pod(local_time)
    elif studio == 'yogaworkshop':
        data = yoga.get_yoga_workshop(local_time)
    else:
        data = {}

    return HttpResponse(json.dumps(data))