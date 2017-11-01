import random
import json
import os

from pico2d import *
import game_framework
import title_state
import Object

name = "MainState"
boy = None
grass = None
font = None
pause_flag = False

class Font:
    def __init__(self):
        self.intervalTime = 0
        self.image = load_image('Data\\Graphic\\Effect\\PAUSE.png')

    def intervaltime_init(self):
        self.intervalTime = 0

    def update(self):
        self.intervalTime += 1
        self.intervalTime %= 201

    def draw(self):
        if self.intervalTime < 100:
            self.image.draw(400, 310)

def enter():
    global boy, grass, font
    boy = Object.CObject(0.0, 90.0)
    #boy.Set_moveimage('Data\\Graphic\\Instance\\run_animation.png', True, 8, 100, 100)
    #boy.Set_idleimage('Data\\Graphic\\Instance\\run_animation.png', True, 8, 100, 100)
    boy.Set_moveimage('Data\\Graphic\\Instance\\test.png')
    boy.Set_idleimage('Data\\Graphic\\Instance\\test.png')
    boy.Draw_PrevImages(True, 10)
    grass = Object.CObject(400.0, 30.0)
    grass.Set_idleimage('Data\\Graphic\\Background\\grass.png')
    font = Font()
    pass


def exit():
    global boy, grass
    del(boy)
    del(grass)
    #del(font)
    pass


def pause():
    global pause_flag, font
    if pause_flag == True:
        pause_flag = False
        font.intervaltime_init()
    else:
        pause_flag = True
    pass


def resume():
    pass


def handle_events():
    global boy
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.change_state(title_state)
        elif event.type == SDL_MOUSEMOTION:
            boy.Set_Pos(event.x, 599 - event.y)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_p):
            pause()
    pass


def update():
    global boy, font
    if pause_flag == False:
        boy.Move()
    else:
        font.update()
    pass


def draw():
    global boy, grass, font
    clear_canvas()
    grass.draw()
    boy.draw()
    if pause_flag:
        font.draw()
    update_canvas()
    # delay(0.001)
    pass





