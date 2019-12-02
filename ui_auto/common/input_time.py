import time
import datetime


def input_time(now=False, front=False, start=False):
    """
    提供公用的输入时间，格式为YYYY-MM-DD hh:mm:ss
    :param now: 返回当前时间
    :param front: 返回10分钟前
    :param start: 返回30分钟后
    :return:
    """
    time_diff = datetime.timedelta(minutes=10)
    now_time = datetime.datetime.now()
    if now:
        a_time = now_time
    elif front:
        a_time = now_time - time_diff
    elif start:
        a_time = now_time + time_diff * 3
    else:
        a_time = now_time + time_diff * 4
    b_time = int(a_time.timestamp())
    time_local = time.localtime(b_time)
    i_time = time.strftime('%Y-%m-%d %H:%M:%S', time_local)

    return i_time


# print(input_time())
