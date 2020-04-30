import datetime


def time_stamp(start=False, end=False):
    now_time = datetime.datetime.now()
    time_diff = datetime.timedelta(minutes=10)
    s_time = now_time + time_diff * 3
    e_time = now_time + time_diff * 6
    if start:
        start_time = int(s_time.timestamp() * 1000)
        return start_time
    if end:
        end_time = int(e_time.timestamp() * 1000)
        return end_time
