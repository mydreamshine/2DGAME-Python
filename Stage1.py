import random
import json
import os

from pico2d import *
import game_framework

import pause_state
import gameover_state

import GameTime
import GameMusic

import Object
import CollisionCheck
import Phisics

event = None

name = "Stage1"
fade = None
character = None
grass = None
Canvas_SIZE = None


Acceleration = 2.0
MaxSpeed = 30.0
JumpSpeed = 90.0
JUMP = False
DOUBLE_JUMP = False


def enter():
    GameTime.init_time()
    GameMusic.Play_Stage()

    global Canvas_SIZE
    Canvas_SIZE = CollisionCheck.Rect(0.0, get_canvas_height(), get_canvas_width(), 0.0)

    global fade, character, grass
    fade = Object.CObject(400.0, 300.0)
    fade.Apped_idleimage('Data\\Graphic\\Effect\\Fade.png')
    fade.Active_Fade_Out()

    global JUMP, DOUBLE_JUMP
    character = Object.CObject(400.0, 300.0)
    character.Apped_moveimage('Data\\Graphic\\Instance\\Character.png')
    character.Apped_idleimage('Data\\Graphic\\Instance\\Character.png')
    character.Draw_PrevImages(True, 10)
    JUMP = False
    DOUBLE_JUMP = False

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
    global event
    global fade, character
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            GameMusic.Stop_BGM()
            game_framework.push_state(pause_state)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_BACKSPACE): # GameOver씬 테스트용
            fade.Active_Fade_In()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_p): # 캐릭터 잔상 On/Off
            if character.draw_Previmages: character.Draw_PrevImages(False)
            else: character.Draw_PrevImages(True)
        #elif event.type == SDL_MOUSEMOTION:
            #character.Set_Pos(event.x, 599 - event.y)


    pass


def update_ActiveTime():
    global fade, character
    fade.Set_ActiveTime()
    character.Set_ActiveTime()
    GameTime.update_time()


def update():
    global event
    global Canvas_SIZE
    global fade, character, grass
    global Acceleration, MaxSpeed, JUMP, DOUBLE_JUMP

    if fade != None: fade.Set_ActiveTime()

    # 캐릭터 물리(가속, 관성, 탄성, 중력)
    if event != None:
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):  # 캐릭터 오른쪽으로 가속
            Phisics.Apply_Accelaration_X(character, Acceleration, MaxSpeed)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):  # 캐릭터 왼쪽으로 가속
            Phisics.Apply_Accelaration_X(character, -Acceleration, MaxSpeed)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):  # 캐릭터 점프
            if not JUMP:
                Phisics.Apply_Jump(character, JumpSpeed)
                DOUBLE_JUMP = True if JUMP else False
                JUMP = True
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_SPACE):  # 캐릭터 점프
            JUMP = False
        else:
            Phisics.Apply_Friction_X(character) # 이동속도 감속
    Phisics.Apply_GravityField(character) # 중력장 적용
    character.Move()# 캐릭터 이동

    # 충돌체크
    if CollisionCheck.Collision_MoveWithHold(character, grass):
        JUMP, DOUBLE_JUMP = False, False
    CollisionCheck.Collsion_WndBoundary(character, Canvas_SIZE)

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