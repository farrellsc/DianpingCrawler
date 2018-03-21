# encoding: gb2312
from selenium import webdriver
import codecs
import httplib
import urllib
import re
import json
import time
import datetime
import random

def translate_checkin_time(this_time):
    string_seconds_before = unicode('秒前','gb2312')
    string_minutes_before = unicode('分钟前','gb2312')
    string_hours_before = unicode('小时前','gb2312')
    string_yesterday = unicode('昨天','gb2312')
    string_2_days_before = unicode('前天','gb2312')
    current_time = time.localtime()
    result = ''
    today = datetime.date(current_time.tm_year,current_time.tm_mon,current_time.tm_mday)
    today_time = datetime.datetime(current_time.tm_year,current_time.tm_mon,current_time.tm_mday,current_time.tm_hour,current_time.tm_min)
    if string_yesterday in this_time:
        hour,minute = this_time[2:].split(':')
        result = today - datetime.timedelta(1)
        result = datetime.datetime(result.year,result.month,result.day,int(hour),int(minute))
    elif string_2_days_before in this_time:
        hour,minute = this_time[2:].split(':')
        result = today - datetime.timedelta(2)
        result = datetime.datetime(result.year,result.month,result.day,int(hour),int(minute))
    elif string_seconds_before in this_time:
        result = str(today_time - datetime.timedelta(float(this_time[:-2])/3600/24))
    elif string_minutes_before in this_time:
        result = str(today_time - datetime.timedelta(float(this_time[:-3])/60/24))
    elif string_hours_before in this_time:
        print this_time
        result = str(today_time - datetime.timedelta(float(this_time[:-3])/24))
    else:
        this_time_list = this_time.split(' ')
        this_time_list[0] = this_time_list[0].split('-')
        this_time_list[1] = this_time_list[1].split(':')
        if len(this_time_list[0]) == 2:
            this_time_list[0].insert(0,str(current_time.tm_year))
        if len(this_time_list[0][0]) == 2:
            this_time_list[0][0] = '20' + this_time_list[0][0]
        result = datetime.datetime(int(this_time_list[0][0]),int(this_time_list[0][1]),int(this_time_list[0][2]),int(this_time_list[1][0]),int(this_time_list[1][1]))
    result = str(result)
    return result

def translate_review_time(this_time):
    this_time_list = this_time[3:].split('-')
    if len(this_time_list[0]) == 2:
        this_time_list[0] = '20' + this_time_list[0]
    result = datetime.datetime(int(this_time_list[0]),int(this_time_list[1]),int(this_time_list[2]))
    result = str(result)
    return result
