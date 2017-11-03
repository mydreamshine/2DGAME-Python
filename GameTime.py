from pico2d import *

FPS = 60.0
# LoopTime : GameLoop에서 한 Cycle이 처리되는 시간
# LoopTime = Cycle 후 시간 - Cycle 전 시간
# 속력 = 거리 / 시간 -> 시간당 이동한 거리 -> 거리 : 시간 반비례 관계
# 현재 FPS = ? -> 1초당 갱신된 Frame수 (갱신된 Frame수 ≒ 이동한 거리)
# 현재 FPS = Frame수 / 1
# Frame 수 = N * LoopTime (속력 * 시간)
# ?????
# 현재 FPS = 1 / LoopTime (1초동안 걸린 LoopTime(?)) => sec / LoopTime (sec당 LoopTime)
# LoopTime이 적으면 많이 이동, LoopTime이 많으면 적게 이동.
# ≒ 현재 FPS가 기준 FPS보다 많으면 적게 이동, 적으면 많이 이동
# ≒ 기준 FPS / 현재 FPS
# = 기준 FPS / (1 / LoopTime) = 기준 FPS * LoopTime

actiontime_cur = 0.0
actiontime_frame = 0.0


def init_time():
    global actiontime_cur
    actiontime_cur = get_time()


def update_time():
    global actiontime_cur, actiontime_frame
    actiontime_frame = get_time() - actiontime_cur
    actiontime_cur += actiontime_frame


def action_Factor():
    global FPS, actiontime_frame
    if actiontime_frame != 0.0:
        if 1 / actiontime_frame >= FPS / 2 - 5.0:
            return FPS * actiontime_frame
    return 0.0