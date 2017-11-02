import random
import json
import os

from pico2d import *
import game_framework
import GameTime
import GameMusic
import pause_state
import gameover_state
import Object

name = "Stage1"
fade = None
character = None
grass = None

GRAVITY = 9.8
Acceleration = 0.2
MaxSpeed = 10.0
JUMP = False
DOUBLE_JUMP = False


def enter():
    GameTime.init_time()
    GameMusic.Play_Stage()
    global fade, character, grass

    global JUMP, DOUBLE_JUMP
    JUMP = False
    DOUBLE_JUMP = False

    fade = Object.CObject(400.0, 300.0)
    fade.Apped_idleimage('Data\\Graphic\\Effect\\Fade.png')
    fade.Active_Fade_Out()

    character = Object.CObject(40.0, 90.0)
    character.Apped_moveimage('Data\\Graphic\\Instance\\Character.png')
    character.Apped_idleimage('Data\\Graphic\\Instance\\Character.png')
    character.Draw_PrevImages(True, 10)
    grass = Object.CObject(400.0, 30.0)
    grass.Apped_idleimage('Data\\Graphic\\Background\\grass.png')
    pass


def DeleteObject():
    global fade, character, grass
    if fade != None: del(fade); fade = None
    if character != None: del(character); character = None
    if grass != None: del(grass); grass = None


def exit():
    DeleteObject()
    pass


def pause():
    pass


def resume():
    pass


def handle_events():
    global fade, character
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            GameMusic.Stop_BGM()
            game_framework.push_state(pause_state)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_BACKSPACE):
            fade.Active_Fade_In()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_p):
            if character.draw_Previmages: character.Draw_PrevImages(False)
            else: character.Draw_PrevImages(True)
        elif event.type == SDL_MOUSEMOTION:
            character.Set_Pos(event.x, 599 - event.y)
    pass


def update_ActiveTime():
    global fade, character
    fade.Set_ActiveTime()
    character.Set_ActiveTime()
    GameTime.update_time()


def update():
    global fade, character
    if fade != None: fade.Set_ActiveTime()
    character.Move()
    GameTime.update_time()
    pass


def Scene_draw():
    global fade, character, grass
    grass.draw()
    character.draw()

    # Fade
    prevFade_In = fade.Fade_In
    if fade.Fade_In or fade.Fade_Out:
        fade.draw()
    # Fade상태에 따른 게임씬(Scene) 탈출
    if prevFade_In and not fade.Fade_In:
        game_framework.push_state(gameover_state)


def draw():
    clear_canvas()
    Scene_draw()
    update_canvas()
    delay(0.01)
    pass