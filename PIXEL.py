from pico2d import *
import game_framework
import main_state
# import start_state

# game_framework.run(start_state)
# 전체 게임프레임워크에 집어넣기 전에
# 다음과 같이 해당 게임프레임에 대해 테스트하여
# 문제가 없으면 집어넣는다.
# main_state 테스트
open_canvas()
game_framework.run(main_state)
close_canvas()
# title_state 테스트
# open_canvas()
# game_framework.run(title_state)
# close_canvas()
# 이런 식으로 여러 단계의 프레임을 나누고
# 현재 프레임워크에 다른 모듈을 작성해서 추가하는 것(다른 사람이 작성한 모듈 등)을 "인터페이스 설계"라고 한다.

# fill here
