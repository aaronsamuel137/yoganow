import urllib
import urllib2
import re
import datetime
import util
import json
from time import strftime

MAX_NUM_CLASSES = 2

def get_yoga_pod(local_time):
    current_day = strftime('%a', local_time)
    next_day = util.next_day(local_time.tm_wday)
    current_time = util.time_str2float(strftime('%I:%M %p', local_time))
    time_regex = r'(1?[0-9]:[0-5][0-9] [A|P]M)'
    class_regex = r'filterable (\w*)'
    url = 'http://www.healcode.com/widgets/schedules/print/dq55683k9o'

    response = urllib2.urlopen(url)
    line = response.readline()

    class_list = []
    while not ('hc_day' in line and current_day in line):
        line = response.readline()

    while True:
        line = response.readline()
        if 'filterable' in line and 'cancelled' not in line:
            class_name = re.findall(class_regex, line)[0]
            line = response.readline()
            times = re.findall(time_regex, line)
            class_time = util.time_str2float(times[0])
            if class_time >= current_time:
                class_list.append({'class_name': class_name,
                                   'start_time': times[0],
                                   'end_time':   times[1]})
        if len(class_list) >= MAX_NUM_CLASSES:
            break
        if 'hc_day' in line and next_day in line:
            break
    return {'studio_name': 'Yoga Pod',
            'class_list': class_list}

def get_yoga_workshop(local_time):
    next_day = util.next_day(local_time.tm_wday)
    current_time = util.time_str2float(strftime("%I:%M %p", local_time))
    time_regex = r'(1?[0-9]:[0-5][0-9]) &#8211; +(1?[0-9]:[0-5][0-9]) ([a|p]m)'
    class_regex = r'<div class="class_type">([\w\s-]*)</div>'

    query_args = {'callback': 'jQuery20207575509008020163_1378411104645',
                  '_': '1378411104646'}
    url = 'http://ws.yogaworkshop.com/cal?' + urllib.urlencode(query_args)

    paren_regex = r'\((.*)\)'
    response = urllib2.urlopen(url).read()
    data = re.findall(paren_regex, response)[0]
    data = json.loads(data)

    class_list = []
    data_rows = data['html'].split('\n')
    for i, line in enumerate(data_rows):
        times = re.findall(time_regex, line)
        if times:
            times = times[0]
            time_str = ' '.join([str(times[0]), str(times[2]).upper()])
            class_time = util.time_str2float(time_str)
            if class_time >= current_time:
                class_line = data_rows[i + 2]
                class_name = re.findall(class_regex, class_line)[0]
                start_time = ' '.join([str(times[0]), str(times[2])])
                end_time   = ' '.join([str(times[1]), str(times[2])])
                class_list.append({'class_name': class_name,
                                   'start_time': start_time,
                                   'end_time':   end_time})
        if len(class_list) >= MAX_NUM_CLASSES:
            break
        if next_day in line:
            break
    return {'studio_name': 'Yoga Workshop',
            'class_list': class_list}