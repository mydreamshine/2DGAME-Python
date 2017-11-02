from pico2d import *

actiontime_cur = 0.0
actiontime_frame = 0.0


def init_time():
    global actiontime_cur
    actiontime_cur = get_time()


def update_time():
    global actiontime_cur, actiontime_frame
    actiontime_frame = get_time() - actiontime_cur
    actiontime_cur += actiontime_frame