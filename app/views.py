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

def api_call(request):
    studio = request.GET.get('studio', None)
    local_time = localtime()

    if studio == 'yogapod':
        data = yoga.get_yoga_pod(local_time)
    elif studio == 'yogaworkshop':
        data = yoga.get_yoga_workshop(local_time)
    elif studio == 'test':
        data = {"class_list": [{"class_name": "yin", "start_time": "5:00 PM",
                                "end_time": "6:15 PM"},
                               {"class_name": "sweat_heat_beatz_level_2_flow",
                                "start_time": "5:30 PM", "end_time": "6:45 PM"}],
                "studio_name": "Yoga Pod",
                "link": "http://yogapodcommunity.com/boulder/schedule"}
    else:
        data = {}

    return HttpResponse(json.dumps(data))


def api_test(request):
    dat = [{'class_name': 'yin',}]
    return HttpResponse(json.dumps(data))
"""{"class_list": [{"class_name": "yin", "start_time": "5:00 PM", "end_time": "6:15 PM"}, {"class_name": "sweat_heat_beatz_level_2_flow", "start_time": "5:30 PM", "end_time": "6:45 PM"}], "studio_name": "Yoga Pod", "link": "http://yogapodcommunity.com/boulder/schedule"}"""