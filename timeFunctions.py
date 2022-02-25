from codecs import getdecoder
import time


def startTime():
    anchor = 1627101900
    current_time = time.time()
    time_since = current_time-anchor
    complete_5_min_periods = time_since // 300
    last_segment = anchor + complete_5_min_periods*300
    start_time = last_segment + 300.5

    return start_time


def wait(start_time):
    time.sleep(300.0 - ((time.time() - start_time) % 300.0))