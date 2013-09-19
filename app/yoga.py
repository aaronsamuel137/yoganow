import urllib
import urllib2
import re
import datetime
import util
import json
from time import strftime

MAX_NUM_CLASSES = 3

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
            class_name = ' '.join([s.title() for s in class_name.split('_')])
            line = response.readline()
            times = re.findall(time_regex, line)
            class_time = util.time_str2float(times[0])
            if class_time >= current_time:
                class_list.append({'class_name': class_name,
                                   'start_time': times[0].lower(),
                                   'end_time':   times[1].lower()})
        if len(class_list) >= MAX_NUM_CLASSES:
            break
        if 'hc_day' in line and next_day in line:
            break
    return {'studio_name': 'Yoga Pod',
            'class_list': class_list,
            'link': 'http://yogapodcommunity.com/boulder/schedule'}

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
            'class_list': class_list,
            'link': 'http://yogaworkshop.com/schedule/class-schedule'}

def get_adi_shakti(local_time):
    def parse_gcal_time(time_str):
        hour, minutes, x, y = time_str.split(':')
        if hour < current_hour or (hour == current_hour and minutes < current_mintue):
            return None
        if int(hour) > 12:
            hour = str(int(hour) - 12)
            am_pm = ' pm'
        elif int(hour) == 12:
            am_pm = ' pm'
        else:
            am_pm = ' am'
        return ':'.join([hour, minutes]) + am_pm

    current_date = strftime('%Y-%m-%d', local_time)
    current_hour = strftime('%H')
    current_mintue = strftime('%M')

    url = 'https://www.google.com/calendar/embed?showTitle=0&showNav=0&showPrint=0&showTabs=0&showCalendars=0&mode=AGENDA&height=600&wkst=1&bgcolor=%23FFFFFF&src=74b03lpbo956gtpdpjjj2ak0d0%40group.calendar.google.com&color=%2323164E&src=rachel.zelaya%40gmail.com&color=%23182C57&ctz=America%2FDenver'
    ds = urllib2.urlopen(url).readlines()
    line = ds[9]
    line = line.replace('<script>function _onload() {window._init(', '')
    line = line.replace(');}</script>', '')
    data = json.loads(line)
    entries = data['cids']['74b03lpbo956gtpdpjjj2ak0d0%40group.calendar.google.com/public/embed']['gdata']['feed']['entry']

    class_list = []
    for entry in entries:
        status = entry['gd$eventStatus']['value']
        start = entry['gd$when'][0]['startTime']
        start_date, start_time = start.split('T')
        if start_date == current_date and 'confirmed' in status:
            class_name = entry['title']['$t']
            end = entry['gd$when'][0]['endTime']
            end_date, end_time = end.split('T')
            start_time = parse_gcal_time(start_time)
            if start_time:
                end_time = parse_gcal_time(end_time)
                class_list.append({'class_name': class_name,
                                   'start_time': start_time,
                                   'end_time':   end_time})
    return {'studio_name': 'Adi Shakti',
            'class_list': class_list,
            'link': 'http://www.adishakticenter.com/kundalini-yoga-class-schedule'}
