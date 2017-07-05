#!/usr/bin/env python
# !-*- coding:utf-8 -*-

import time
import datetime


class Time(object):
    def __init__(self):
        pass


def getStepCount(start_time=None, end_time=None, step=None):
    stepCount = int((string2timestamp(end_time) - string2timestamp(start_time)) / (step * 60))
    return stepCount


# step 单位分钟
def getComputeTimes(start_time=None, end_time=None, step=None):
    if step is None:
        step = 1
    result_times = []
    if start_time is None:
        # 获取递前的一个时间点
        now_str = time.strptime(getNowStr(), "%Y-%m-%d %H:%M:%S")
        current_timeStamp = int(time.mktime(now_str))
        currentTime_count = int(current_timeStamp / (step * 60))

        lastStamp = currentTime_count * step * 60
        last_timeArray = time.localtime(lastStamp)
        lastTime = time.strftime("%Y-%m-%d %H:%M:%S", last_timeArray)
        result_times.append(lastTime)
    else:
        star_time_f = time.strptime(str(start_time)[:19], "%Y-%m-%d %H:%M:%S")
        start_time_stamp = int(time.mktime(star_time_f))
        start_count = int(start_time_stamp / (step * 60))
        if end_time is None:
            end_time = getNowStr()
        end_time_f = time.strptime(str(end_time)[:19], "%Y-%m-%d %H:%M:%S")
        end_time_stamp = int(time.mktime(end_time_f))
        end_count = int(end_time_stamp / (step * 60))

        if start_count < end_count:
            count = end_count - start_count
            for i in range(count + 1):
                res_Stamp = (start_count + i) * step * 60
                res_timeArray = time.localtime(res_Stamp)
                res_Time = time.strftime("%Y-%m-%d %H:%M:%S", res_timeArray)
                result_times.append(res_Time)
    return result_times


# 获取当前时间（字符创）
def getNowStr():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')


# 获取应该开始的时间
def getStartTime(step=7, step_count=60):
    start_timestamp = getNowTimeStamp() - step * step_count * 60
    return timestamp2string(start_timestamp)


def getNowTimeStamp():
    return int(time.mktime(datetime.datetime.now().timetuple()))


def timestamp2string(timeStamp):
    try:
        d = datetime.datetime.fromtimestamp(timeStamp)
        str1 = d.strftime("%Y-%m-%d %H:%M:%S.%f")
        return str1
    except Exception as e:
        return '1970-01-01 08:00:00'


def string2timestamp(strValue):
    try:
        d = datetime.datetime.strptime(strValue, "%Y-%m-%d %H:%M:%S.%f")
        t = d.timetuple()
        timeStamp = int(time.mktime(t))
        timeStamp = float(str(timeStamp) + str("%06d" % d.microsecond)) / 1000000
        return timeStamp
    except ValueError as e:
        d = datetime.datetime.strptime(strValue, "%Y-%m-%d %H:%M:%S")
        t = d.timetuple()
        timeStamp = int(time.mktime(t))
        timeStamp = float(str(timeStamp) + str("%06d" % d.microsecond)) / 1000000
        return timeStamp


if __name__ == "__main__":
    # print(getComputeTimes(startTime='2017-05-15 18:10:43.369', step=5))
    # print(getComputeTimes(step=60 * 1))
    print(getNowStr())
