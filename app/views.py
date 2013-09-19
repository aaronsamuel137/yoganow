import yoga
import util
import json

from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext, loader
from app.models import Post
from app.models import Count

from time import localtime

def index(request):
    count = Count.objects.all()[0]
    count.num_vists = count.num_vists + 1
    count.save()

    context = {'studios': ['yogapod', 'yogaworkshop', 'adishakti']}
    # context = {'studios': ['test1', 'test2']}
    return render(request, 'index.html', context)

def api_call(request):
    studio = request.GET.get('studio', None)
    local_time = localtime()

    if studio == 'yogapod':
        data = yoga.get_yoga_pod(local_time)
    elif studio == 'yogaworkshop':
        data = yoga.get_yoga_workshop(local_time)
    elif studio == 'adishakti':
        data = yoga.get_adi_shakti(local_time)
    elif studio == 'test1':
        data = {'class_list': [{'class_name': 'Test1', 'start_time': '5:00 PM',
                                'end_time': '6:15 PM'},
                               {'class_name': 'Test2',
                                'start_time': '5:30 PM', 'end_time': '6:45 PM'}],
                'studio_name': 'Test Studio',
                'link': '/'}
    elif studio == 'test2':
        data = {'class_list': [{'class_name': 'Test3', 'start_time': '8:00 PM',
                                'end_time': '9:15 PM'},
                               {'class_name': 'Test4',
                                'start_time': '2:30 PM', 'end_time': '6:45 PM'}],
                'studio_name': 'Another Studio',
                'link': '/'}
    else:
        data = {}

    return HttpResponse(json.dumps(data))

def blog(request):
    posts = Post.objects.all().order_by('-created')
    context = {'posts': posts}
    return render(request, 'blog.html', context)

def tests(request):
    context = {}
    return render(request, 'tests.html', context)