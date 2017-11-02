import random
import json
import os

from pico2d import *
import game_framework
import GameTime
import pause_state
import Object

name = "MainState"
fade = None
boy = None
grass = None


def enter():
    GameTime.init_time()
    global fade, boy, grass

    fade = Object.CObject(400.0, 300.0)
    fade.Apped_idleimage('Data\\Graphic\\Effect\\Fade.png')
    fade.Active_Fade_Out()

    boy = Object.CObject(0.0, 90.0)
    boy.Apped_moveimage('Data\\Graphic\\Instance\\test.png')
    boy.Apped_idleimage('Data\\Graphic\\Instance\\test.png')
    boy.Draw_PrevImages(True, 10)
    grass = Object.CObject(400.0, 30.0)
    grass.Apped_idleimage('Data\\Graphic\\Background\\grass.png')
    pass


def DeleteObject():
    global boy, grass
    del (boy)
    del (grass)


def exit():
    DeleteObject()
    pass


def pause():
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
            game_framework.push_state(pause_state)
        elif event.type == SDL_MOUSEMOTION:
            boy.Set_Pos(event.x, 599 - event.y)
    pass


def update_ActiveTime():
    global boy
    boy.Set_ActiveTime()
    GameTime.update_time()

def update():
    global fade, boy
    if fade != None: fade.Set_ActiveTime()
    boy.Move()
    GameTime.update_time()
    pass


def Scene_draw():
    global fade, boy, grass
    grass.draw()
    boy.draw()
    if fade != None:
        fade.draw()
        if fade.Num_opacify == 0.0: del(fade); fade = None


def draw():
    global boy, grass
    clear_canvas()
    Scene_draw()
    update_canvas()
    delay(0.01)
    pass