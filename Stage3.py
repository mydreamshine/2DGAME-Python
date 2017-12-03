from pico2d import *
import game_framework
import GameTime
import GameMusic

import Object
import CollisionCheck
import Phisics

import pause_state
import gameover_state
import Stage4

Gameover = False
Nextstage_in = False

Stagename = "Stage3"

TrafficTime = 0.0
CurrentTrafficLight_R = False
CurrentTrafficLight_Y = False
CurrentTrafficLight_G = False


def enter():
    global Stagename
    GameTime.init_time()
    GameMusic.Play_Stage()
    SaveFile = open('Data\\Bin\\SaveStage.txt', 'w')
    SaveFile.write(Stagename)
    SaveFile.close()
    Object.info_list = Object.create_infoFrom('Data\\Bin\\stage3_information.txt')
    Object.ObjectList = Object.create_ObjectsFrom('Data\\Bin\\stage3_Object.txt')
    Object.Ground_Size.right = Object.ObjectList['BackGround'].Right()
    Object.ObjectList['TrafficLight_R'].Num_opacify = 0.3
    Object.ObjectList['TrafficLight_Y'].Num_opacify = 0.3

    global TrafficTime, CurrentTrafficLight_R, CurrentTrafficLight_Y, CurrentTrafficLight_G
    TrafficTime = 0.0
    CurrentTrafficLight_R = False
    CurrentTrafficLight_Y = False
    CurrentTrafficLight_G = True


def exit():
    Object.DeleteObjects()


def pause():
    pass


def resume():
    pass


def handle_events():
    global Nextstage_in
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            GameMusic.Delete()
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            GameMusic.Stop_BGM()
            game_framework.push_state(pause_state)
        else:
            Object.character.handle_events(event)
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_UP):
            intersectRect = CollisionCheck.Rect()
            if CollisionCheck.intersectRect(intersectRect, Object.character, Object.ObjectList['Arrival']):
                Nextstage_in = True
                Object.fade.Active_Fade_In()
    pass


def update_ActiveTime(): # 움직이는 물체에 대한 활동주기 갱신
    Object.fade.Set_ActiveTime()
    Object.character.Set_ActiveTime()
    GameTime.update_time()


def update():
    global Gameover
    global TrafficTime, CurrentTrafficLight_G, CurrentTrafficLight_Y, CurrentTrafficLight_R
    Object.fade.Set_ActiveTime()

    # 중력장 적용
    if Object.character.AffectedGravity:
        Phisics.Apply_GravityField(Object.character)
    for name in Object.ObjectList:
        if Object.ObjectList[name].AffectedGravity:
            Phisics.Apply_GravityField(Object.ObjectList[name])

    FrictionFactor = 0.9
    Object.character.Move(FrictionFactor) # 캐릭터 이동

    if CurrentTrafficLight_R and not CurrentTrafficLight_Y:
        if abs(Object.character.RUN_SPEED_KMPH_x) > 0.3 and not Gameover:
            Gameover = True
            Object.fade.Active_Fade_In()

    # 배경 원근이동
    Posx_factor = ((Object.ObjectList['BackGround'].Size_Width - Object.Canvas_SIZE.right) / 6) * ((400.0 - Object.character.x) / 400.0)
    Object.ObjectList['BackGround'].Set_Pos(400.0 + Posx_factor, Object.ObjectList['BackGround'].y)

    # 충돌체크 및 처리
    CollisionCheck.Collsion_WndBoundary(Object.character, Object.Ground_Size)
    CollisionCheck.Collsion_WndBoundary(Object.character, Object.Canvas_SIZE)
    for name in Object.ObjectList:
        if Object.character.Left() < Object.ObjectList['Arrival'].Right() - 10 \
                and Object.character.Right() > Object.ObjectList['Arrival'].Left() + 10:
            if Object.character.Bottom() >= Object.ObjectList['Arrival'].y - 10:
                Object.Ground_Size.bottom = Object.ObjectList['Arrival'].y - 10
                break
        elif name[0:6] == 'Ground' and Object.character.Left() < Object.ObjectList[name].Right() - 10\
                and Object.character.Right() > Object.ObjectList[name].Left() + 10:
            if Object.character.Bottom() >= Object.ObjectList[name].y - 10:
                Object.Ground_Size.bottom = Object.ObjectList[name].y - 10
                break
        else: Object.Ground_Size.bottom = 45

    GameTime.update_time()

    if Object.fade.Num_opacify == 0.0: TrafficTime += GameTime.actiontime_frame
    if CurrentTrafficLight_Y and TrafficTime >= 0.9:
        TrafficTime = 0.0
        if CurrentTrafficLight_G:
            CurrentTrafficLight_G = False
            CurrentTrafficLight_Y = False
            CurrentTrafficLight_R = True
            Object.ObjectList['TrafficLight_R'].Num_opacify = 1.0
            Object.ObjectList['TrafficLight_Y'].Num_opacify = 0.3
            Object.ObjectList['TrafficLight_G'].Num_opacify = 0.3
        elif CurrentTrafficLight_R:
            CurrentTrafficLight_R = False
            CurrentTrafficLight_Y = False
            CurrentTrafficLight_G = True
            Object.ObjectList['TrafficLight_R'].Num_opacify = 0.3
            Object.ObjectList['TrafficLight_Y'].Num_opacify = 0.3
            Object.ObjectList['TrafficLight_G'].Num_opacify = 1.0
    elif TrafficTime >= 1.5:
        TrafficTime = 0.0
        CurrentTrafficLight_Y = True
        Object.ObjectList['TrafficLight_R'].Num_opacify = 0.3
        Object.ObjectList['TrafficLight_Y'].Num_opacify = 1.0
        Object.ObjectList['TrafficLight_G'].Num_opacify = 0.3


def Scene_draw():
    global Gameover, Nextstage_in

    #BackGround
    Object.ObjectList['BackGround'].draw()

    #Ground
    for name in Object.ObjectList:
        if name[0:6] == 'Ground':
            Object.ObjectList[name].draw()

    #Arrival
    Object.ObjectList['Arrival'].draw()

    Object.character.draw()

    #Ground_Shade
    for name in Object.ObjectList:
        if name[0:12] == 'Ground_Shade':
            Object.ObjectList[name].draw()

    #Arrival_Shade
    Object.ObjectList['Arrival_Shade'].draw()

    #TrafficLight
    Object.ObjectList['TrafficLight_R'].draw()
    Object.ObjectList['TrafficLight_Y'].draw()
    Object.ObjectList['TrafficLight_G'].draw()

    for info in Object.info_list:
        info.draw()

    # Fade
    prevFade_In = Object.fade.Fade_In
    if Object.fade.Fade_In or Object.fade.Fade_Out:
        Object.fade.draw()
    # Fade상태에 따른 게임씬(Scene) 탈출
    if prevFade_In and not Object.fade.Fade_In:
        if Gameover:
            game_framework.push_state(gameover_state)
        if Nextstage_in:
            game_framework.change_state(Stage4)


def draw():
    clear_canvas()
    Scene_draw()
    update_canvas()
    delay(0.01)
    pass