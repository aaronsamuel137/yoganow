from time import strftime, localtime
import re
import HTMLParser

int2days = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu',
            4: 'Fri', 5: 'Sat', 6: 'Sun'}

def time_str2float(s):
    """convert string of from 10:30 PM to 22.5"""
    hr_min = s.split(':')
    float_time = int(hr_min[0])
    am_pm = hr_min[1].split()
    if am_pm[1] == 'PM' and float_time != 12:
        float_time += 12
    float_time += float(am_pm[0]) / 60
    return float_time

def next_day(today):
    """get day of week for tomorrow"""
    tomorrow = (today + 1) % 7
    return int2days[tomorrow]

def print_class_list(class_list, name):
    print 'Schedule for {}:'.format(name)
    for item in class_list:
        print item
    print ''

def class_list2str(class_list, name):
    s = ''
    s += 'Schedule for {}:<br>'.format(name)
    if not class_list: class_list.append('No classes left today :(')
    for item in class_list:
        s += '{}<br>'.format(item)
    return s