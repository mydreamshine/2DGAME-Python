import json
import os

from pico2d import *
import game_framework

import pause_state
import gameover_state
import Stage2

import GameTime
import GameMusic

import Object
import CollisionCheck
import Phisics

Gameover = False
Nextstage_in = False

name = "Stage1"
fade = None
character = None
BackGround = None
Canvas_SIZE = None
Ground_Size = None
Ground = []
Ground_Shade = []
Arrival = None
Arrival_Shade = None


class info:
    def __init__(self):
        self.name = None
        self.x, self.y = 0.0, 0.0
        self.image = None
        self.row, self.col= 1, 1
        self.left, self.bottom = 0, 0
        self.width, self.height = 0, 0

    def draw(self):
        self.image.clip_draw(self.left + self.width * (self.col - 1) if self.col > 0 else 0, self.bottom + self.height * (self.row - 1) if self.row > 0 else 0, self.width, self.height, self.x, self.y)


info_list = None


def create_info():
    info_file = open('Data\\Bin\\stage1_test.txt', 'r')
    info_dic = json.load(info_file)
    info_file.close()

    info_list_source = []
    for name in info_dic:
        info_object = info()
        info_object.name = name

        info_object.image = load_image(info_dic[name]['ImagePath'])
        info_object.left = info_dic[name]['left']
        info_object.bottom = info_dic[name]['bottom']
        info_object.width = info_dic[name]['width']
        info_object.height = info_dic[name]['height']
        info_object.row = info_dic[name]['row']
        info_object.col = info_dic[name]['col']
        info_object.x = info_dic[name]['x']
        info_object.y = info_dic[name]['y']

        info_list_source.append(info_object)

    return info_list_source


def enter():
    GameTime.init_time()
    GameMusic.Play_Stage()
    global fade, character, BackGround
    global Canvas_SIZE, Ground_Size
    global Ground, Ground_Shade, Arrival, Arrival_Shade
    global info_list
    info_list = create_info()

    BackGround = Object.CObject(400.0, 300.0)
    BackGround.Append_idleimage('Data\\Graphic\\Background\\background.png')
    image = load_image('Data\\Graphic\\Background\\background.png')

    Canvas_SIZE = CollisionCheck.Rect(0.0, get_canvas_height(), get_canvas_width(), 0.0)
    Ground_Size = CollisionCheck.Rect(0.0, get_canvas_height(), BackGround.Right(), 45.0)

    Ground.append(Object.CObject(650.0, 150.0))
    Ground[0].Append_idleimage('Data\\Graphic\\Background\\Tile_sky.png')
    Arrival = Object.CObject()
    Arrival.Append_idleimage('Data\\Graphic\\Background\\Tile_sky_Arrival.png')
    Arrival.Set_Pos(Ground[0].Right() - Arrival.Size_Width / 2, 150.0)

    Ground_Shade.append(Object.CObject(650.0, 45.0))
    Ground_Shade[0].Append_idleimage('Data\\Graphic\\Background\\Tile_sky_Shade.png')
    Arrival_Shade = Object.CObject()
    Arrival_Shade.Append_idleimage('Data\\Graphic\\Background\\Tile_sky_Arrival_Shade.png')
    Arrival_Shade.Set_Pos(Ground_Shade[0].Right() - Arrival_Shade.Size_Width / 2, 45.0)

    fade = Object.CObject(400.0, 300.0)
    fade.Append_idleimage('Data\\Graphic\\Effect\\Fade.png')
    fade.Active_Fade_Out()

    character = Object.CObject(400.0, 300.0)
    character.Append_moveimage('Data\\Graphic\\Instance\\Character.png')
    character.Append_idleimage('Data\\Graphic\\Instance\\Character.png')
    character.Draw_PrevImages(True, 10)
    character.AffectedGravity = True

    pass


def DeleteObject():
    global Ground, Ground_Shade, Arrival, Arrival_Shade
    global fade, Canvas_SIZE, character, BackGround
    global info_list
    info_list.clear()
    if fade != None: del(fade); fade = None
    if Canvas_SIZE != None: del(Canvas_SIZE); Canvas_SIZE = None
    if character != None: del(character); character = None
    if BackGround != None: del(BackGround); BackGround = None
    if Arrival !=  None: del(Arrival); Arrival = None
    if Arrival_Shade != None: del (Arrival_Shade); Arrival_Shade = None
    while(len(Ground) > 0): Ground.pop()
    while (len(Ground_Shade) > 0): Ground_Shade.pop()


def exit():
    DeleteObject()
    pass


def pause():
    pass


def resume():
    pass


def handle_events():
    global fade, character, Arrival
    global Nextstage_in
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            GameMusic.Delete()
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            GameMusic.Stop_BGM()
            game_framework.push_state(pause_state)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_BACKSPACE): # GameOver씬 테스트용
            fade.Active_Fade_In()
        else:
            character.handle_events(event)
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_w):
            intersectRect = CollisionCheck.Rect()
            if CollisionCheck.intersectRect(intersectRect, character, Arrival):
                Nextstage_in = True
                fade.Active_Fade_In()
    pass


def update_ActiveTime(): # 움직이는 물체에 대한 활동주기 갱신
    global fade, character
    fade.Set_ActiveTime()
    character.Set_ActiveTime()
    GameTime.update_time()


def update():
    global Canvas_SIZE
    global fade, character, BackGround, Ground_Size
    global Ground, Arrival

    if fade != None: fade.Set_ActiveTime()

    # 중력장 적용
    if character.AffectedGravity:
        Phisics.Apply_GravityField(character)
    character.Move() # 캐릭터 이동

    # 배경 원근이동
    Posx_factor = ((BackGround.Size_Width - Canvas_SIZE.right) / 6) * ((400.0 - character.x) / 400.0)
    BackGround.Set_Pos(400.0 + Posx_factor, BackGround.y)

    # 충돌체크 및 처리
    for ground in Ground:
        if character.Left() < Arrival.Right() - 10 and character.Right() > Arrival.Left() + 10:
            if character.Bottom() > Arrival.y - 10:
                Ground_Size.bottom = Arrival.y - 10
                break
        elif character.Left() < ground.Right() - 10 and character.Right() > ground.Left() + 10:
            if character.Bottom() > ground.y - 10:
                Ground_Size.bottom = ground.y - 10
                break
        else: Ground_Size.bottom = 45.0

    CollisionCheck.Collsion_WndBoundary(character, Ground_Size)
    CollisionCheck.Collsion_WndBoundary(character, Canvas_SIZE)

    GameTime.update_time()
    pass


def Scene_draw():
    global Gameover, Nextstage_in
    global fade, character, BackGround
    global Ground, Ground_Shade, Arrival, Arrival_Shade
    global info_list

    BackGround.draw()

    # Tile
    for ground in Ground:
        ground.draw()

    # Arrival
    Arrival.draw()

    character.draw()

    # Tile Shade
    for ground_shade in Ground_Shade:
        ground_shade.draw()

    # Arrival_Shade
    Arrival_Shade.draw()

    for infos in info_list:
        infos.draw()

    # Fade
    prevFade_In = fade.Fade_In
    if fade.Fade_In or fade.Fade_Out:
        fade.draw()
    # Fade상태에 따른 게임씬(Scene) 탈출
    if prevFade_In and not fade.Fade_In:
        if Gameover:
            game_framework.push_state(gameover_state)
        if Nextstage_in:
            game_framework.change_state(Stage2)


def draw():
    clear_canvas()
    Scene_draw()
    update_canvas()
    delay(0.01)
    pass