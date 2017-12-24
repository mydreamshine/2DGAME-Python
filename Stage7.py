from pico2d import *
import game_framework
import GameTime
import GameMusic

import Object
import CollisionCheck
import Phisics

import pause_state
import gameover_state
import Stage8

Gameover = False
Nextstage_in = False

Stagename = "Stage7"

Enable_Dark = False
Disable_Dark = True
Active_Fog = False


def Active_dark_Fog_update():
    global Enable_Dark, Disable_Dark, Active_Fog
    if Object.fade_dark.x > Object.Canvas_SIZE.right / 2 and Disable_Dark and Active_Fog:
        Object.fade_dark.x -= (Object.Canvas_SIZE.right / 2) * 1.1 * Object.fade_dark.frameTime
        Object.fade_dark.Size_Width = (Object.Canvas_SIZE.right - Object.fade_dark.x) * 2

    if Object.fade_dark.x < Object.Canvas_SIZE.right / 2 and not Enable_Dark:
        Object.fade_dark.x = Object.Canvas_SIZE.right / 2
        Object.fade_dark.Size_Width = Object.fade_dark.x * 2
        Enable_Dark = True
        Disable_Dark = False
        Active_Fog = False


def Deactive_dark_Fog_update():
    global Enable_Dark, Disable_Dark, Active_Fog
    if Object.fade_dark.x > 0 and Enable_Dark and Active_Fog:
        Object.fade_dark.x -= (Object.Canvas_SIZE.right / 2) * 1.1 * Object.fade_dark.frameTime
        Object.fade_dark.Size_Width = Object.fade_dark.x * 2

    if Object.fade_dark.x < 0 and not Disable_Dark:
        Enable_Dark = False
        Disable_Dark = True
        Active_Fog = False
        Object.fade_dark.x = Object.Canvas_SIZE.right
        Object.fade_dark.Size_Width = 0



def process_Collision():
    global Gameover
    # 충돌체크 및 처리
    CollisionCheck.Collsion_WndBoundary(Object.character, Object.Ground_Size)
    CollisionCheck.Collsion_WndBoundary(Object.character, Object.Canvas_SIZE)
    for name in Object.ObjectList:
        if name[0:5] == 'Thorn':
            CollisionCheck.Collsion_WndBoundary(Object.ObjectList[name], Object.ObjectList[name].GroundField)

    if Object.character.y < 0 and not Gameover:
        Gameover = True
        Object.fade.Active_Fade_In()

    PositionTopGround = False
    for name in Object.ObjectList:
        if Object.character.Left() < Object.ObjectList['Arrival'].Right() - 10 \
                and Object.character.Right() > Object.ObjectList['Arrival'].Left() + 10:
            if Object.character.Bottom() >= Object.ObjectList['Arrival'].y - 10:
                Object.Ground_Size.bottom = Object.ObjectList['Arrival'].y - 10
        elif not PositionTopGround and name[0:6] == 'Ground' and name[6] != '_' \
                and Object.character.Left() < Object.ObjectList[name].Right() - 10 \
                and Object.character.Right() > Object.ObjectList[name].Left() + 10:
            if Object.character.Bottom() >= Object.ObjectList[name].y - 10 and Object.ObjectList[name].Num_opacify >= 0.6:
                Object.Ground_Size.bottom = Object.ObjectList[name].y - 10
                PositionTopGround = True
        elif name[0:5] == 'Thorn' and not Gameover:
            IntersectRect = CollisionCheck.Rect()
            Rect1 = CollisionCheck.Rect()
            Rect2 = CollisionCheck.Rect()
            Rect1.left = Object.character.Left() + 10
            Rect1.top = Object.character.Top() - 10
            Rect1.right = Object.character.Right() - 10
            Rect1.bottom = Object.character.Bottom() + 10
            Rect2.left = Object.ObjectList[name].Left() + 15
            Rect2.top = Object.ObjectList[name].Top() - 17
            Rect2.right = Object.ObjectList[name].Right() - 15
            Rect2.bottom = Object.ObjectList[name].Bottom() + 9
            if CollisionCheck.intersectRect_s(IntersectRect, Rect1, Rect2):
                Gameover = True
                Object.fade.Active_Fade_In()
        elif not PositionTopGround:
            Object.Ground_Size.bottom = Object.Canvas_SIZE.bottom = 45

        if name[0:5] == 'Thorn':
            for notThorn in Object.ObjectList:
                if notThorn[0:6] == 'Ground' and notThorn[6] != '_' \
                        and Object.ObjectList[name].Left() < Object.ObjectList[notThorn].Right() - 10 \
                        and Object.ObjectList[name].Right() > Object.ObjectList[name].Left() + 10:
                    if Object.ObjectList[name].Bottom() >= Object.ObjectList[notThorn].y - 10 and Object.ObjectList[
                        notThorn].Num_opacify >= 0.6:
                        Object.ObjectList[name].GroundField.bottom = Object.ObjectList[notThorn].y - 10
                        break
                else:
                    Object.ObjectList[name].GroundField.bottom = 45


def enter():
    global Stagename, Gameover, Nextstage_in
    global Enable_Dark, Disable_Dark, Active_Fog

    Enable_Dark = False
    Disable_Dark = True
    Active_Fog = False
    Gameover = Nextstage_in = False
    GameTime.init_time()
    GameMusic.Play_Stage()
    SaveFile = open('Data\\Bin\\SaveStage.txt', 'w')
    SaveFile.write(Stagename)
    SaveFile.close()
    Object.info_list = Object.create_infoFrom('Data\\Bin\\stage7_information.txt')
    Object.ObjectList = Object.create_ObjectsFrom('Data\\Bin\\stage7_Object.txt')
    Object.Ground_Size.right = Object.ObjectList['BackGround'].Right()

    for name in Object.ObjectList:
        if name[0:5] == 'Thorn':
            Object.ObjectList[name].Set_GroundField(Object.Ground_Size)

def exit():
    Object.DeleteObjects()


def pause():
    pass


def resume():
    pass


def handle_events():
    global Nextstage_in, Active_Fog
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
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_LCTRL):

            DecidedOpacifyAll = True
            for name in Object.ObjectList:
                if name[0:6] == 'Ground' and Object.ObjectList[name].Num_opacify != 1.0 and Object.ObjectList[name].Num_opacify != 0.0:
                    DecidedOpacifyAll = False
                    break

            if DecidedOpacifyAll:
                for name in Object.ObjectList:
                    if name[0:6] == 'Ground':
                        if Object.ObjectList[name].Num_opacify == 1.0:
                            Object.ObjectList[name].Active_Fade_Out()
                        elif Object.ObjectList[name].Num_opacify == 0.0:
                            Object.ObjectList[name].Active_Fade_In()

            if not Active_Fog: Active_Fog = True

        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_UP):
            intersectRect = CollisionCheck.Rect()
            if CollisionCheck.intersectRect(intersectRect, Object.character, Object.ObjectList['Arrival']):
                Nextstage_in = True
                Object.fade.Active_Fade_In()
    pass


def update_ActiveTime(): # 움직이는 물체에 대한 활동주기 갱신
    Object.fade.Set_ActiveTime()
    if Object.fade_dark != None: Object.fade_dark.Set_ActiveTime()
    Object.character.Set_ActiveTime()
    for name in Object.ObjectList:
        Object.ObjectList[name].Set_ActiveTime()
    GameTime.update_time()


def update():
    Object.fade.Set_ActiveTime()
    if Object.fade_dark != None:
        Object.fade_dark.Set_ActiveTime()
        Active_dark_Fog_update()
        Deactive_dark_Fog_update()

    # 중력장 적용
    if Object.character.AffectedGravity:
        GravityFactor = 0.1
        if Object.character.RUN_SPEED_KMPH_y < 0.0:
            GravityFactor = 0.3
        Phisics.Apply_GravityField(Object.character, GravityFactor)
    for name in Object.ObjectList:
        if Object.ObjectList[name].AffectedGravity:
            Phisics.Apply_GravityField(Object.ObjectList[name], 0.1)
            Object.ObjectList[name].Move()
        else: Object.ObjectList[name].Set_ActiveTime()

    Object.character.Move()  # 캐릭터 이동

    # 배경 원근이동
    Posx_factor = ((Object.ObjectList['BackGround'].Size_Width - Object.Canvas_SIZE.right) / 6) * ((400.0 - Object.character.x) / 400.0)
    Object.ObjectList['BackGround'].Set_Pos(400.0 + Posx_factor, Object.ObjectList['BackGround'].y)
    GameTime.update_time()


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

    # Thorn
    for name in Object.ObjectList:
        if name[0:5] == 'Thorn':
            Object.ObjectList[name].draw()

    Object.character.draw()

    #Ground_Shade
    for name in Object.ObjectList:
        if name[0:12] == 'Ground_Shade':
            Object.ObjectList[name].draw()

    #Arrival_Shade
    Object.ObjectList['Arrival_Shade'].draw()

    # 충돌 처리
    process_Collision()

    for info in Object.info_list:
        info.draw()

    # Fade
    if Object.fade_dark != None: Object.fade_dark.draw()
    prevFade_In = Object.fade.Fade_In
    if Object.fade.Fade_In or Object.fade.Fade_Out:
        Object.fade.draw()
    # Fade상태에 따른 게임씬(Scene) 탈출
    if prevFade_In and not Object.fade.Fade_In:
        if Gameover:
            game_framework.push_state(gameover_state)
        if Nextstage_in:
            game_framework.change_state(Stage8)


def draw():
    clear_canvas()
    Scene_draw()
    update_canvas()
    delay(0.01)
    pass