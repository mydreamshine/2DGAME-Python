from pico2d import *
import game_framework
import menu_state
import Object
import GameTime
import GameMusic

name = "TitleState"
background1 = None
background2 = None
whitebar = None
game_name = None
info = None
varScale = 1.0
varReScale = 1.0
velocity_Scale = 0.0
accelaration_Scale = 0.004
MaxScale = 1.2


def DeleteObject():
    global background1, background2, whitebar, game_name, info
    GameMusic.Delete()
    if background1 != None: del (background1); background1 = None
    if background2 != None: del (background2); background2 = None
    if whitebar != None: del (whitebar); whitebar = None
    if game_name != None: del (game_name); game_name = None
    if info != None: del(info); info = None


def ReCreateObject():
    global background1, background2, game_name
    if background1 == None:
        GameMusic.Play_Title()
        background1 = Object.CObject(400.0, 300.0)
        background1.Append_moveimage('Data\\Graphic\\Background\\title.png')
        background1.Set_moveSpeed(-8.0)
        background1.nonFriction = True

        right = background1.x + background1.Size_Width

        if background2 == None:
            background2 = Object.CObject(right, 300.0)
            background2.Append_moveimage('Data\\Graphic\\Background\\title.png')
            background2.Set_moveSpeed(-8.0)
            background2.nonFriction = True

    if game_name == None:
        game_name = Object.CObject(200.0, 300.0)
        game_name.Append_idleimage('Data\\Graphic\\Menu\\game_name.png')
        game_name.Append_moveimage('Data\\Graphic\\Menu\\game_name.png')


def enter():
    GameTime.init_time()
    GameMusic.Play_Title()

    global background1, background2, whitebar, game_name, info
    background1 = Object.CObject(400.0, 300.0)
    background1.Append_moveimage('Data\\Graphic\\Background\\title.png')
    background1.Set_moveSpeed(-8.0)
    background1.nonFriction = True

    right = background1.x + background1.Size_Width

    background2 = Object.CObject(right, 300.0)
    background2.Append_moveimage('Data\\Graphic\\Background\\title.png')
    background2.Set_moveSpeed(-8.0)
    background2.nonFriction = True

    whitebar = Object.CObject(400.0, 465.0)
    whitebar.Append_idleimage('Data\\Graphic\\Menu\\white_bar.png')
    whitebar.Append_moveimage('Data\\Graphic\\Menu\\white_bar.png')
    whitebar.nonFriction = True

    game_name = Object.CObject(400.0, 300.0)
    game_name.Append_idleimage('Data\\Graphic\\Menu\\game_name.png')
    game_name.Append_moveimage('Data\\Graphic\\Menu\\game_name.png')
    game_name.nonFriction = True

    info = Object.CObject(400.0, 100.0)
    info.Append_idleimage('Data\\Graphic\\Menu\\info_title.png')
    pass


def exit():
    pass


def handle_events():
    global whitebar, game_name
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            DeleteObject()
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_name.Set_moveSpeed(-30.0)
            whitebar.Set_moveSpeed(-7.0)
            game_framework.change_state(menu_state)
    pass


def draw_title():
    global background1, background2, whitebar, game_name
    # 타이틀 배경
    if background1 != None and background2 != None:
        background1.draw()
        background2.draw()

    # 타이틀 메뉴 테두리
    if whitebar != None:
        whitebar.draw()
        whitebar.Set_Pos(whitebar.x, 134.0)
        whitebar.draw()
        whitebar.Set_Pos(whitebar.x, 465.0)

    # 게임 이름 텍스트
    if game_name != None:
        game_name.draw()


def draw():
    global info
    clear_canvas()
    draw_title()
    if info != None: info.draw()
    update_canvas()
    pass


def update():
    global background1, background2, whitebar, game_name
    global MaxScale, varScale, varReScale, velocity_Scale, accelaration_Scale

    if background1 != None and background2 != None and game_name != None:
        background1.Move()
        background2.Move()

        # 배경 횡스크롤링
        if background1.x + background1.Size_Width / 2 < 0:
            right = background2.x + background2.Size_Width
            background1.Set_Pos(right, background1.y)
        elif background2.x + background2.Size_Width / 2 < 0:
            right = background1.x + background1.Size_Width
            background2.Set_Pos(right, background2.y)

        # 타이틀 텍스트 확대 축소
        if varScale > MaxScale or varScale < 1.0:
            varScale = MaxScale if varScale > MaxScale else 1.0
            velocity_Scale *= -1
        else: velocity_Scale += accelaration_Scale * GameTime.actiontime_frame

        # 부동소수점 연산 오차 조정
        if abs(velocity_Scale) < 0.0011041:
            velocity_Scale = 0.0011041 if velocity_Scale > 0.0 else -0.0011041
        elif abs(velocity_Scale) > 0.005115:
            velocity_Scale = 0.005115 if velocity_Scale > 0.0 else -0.005115

        varScale += velocity_Scale
        varReScale -= velocity_Scale
        if whitebar != None:
            Size_Width = (whitebar.MoveFrameWidth if whitebar.move_state else whitebar.idleFrameWidth) * varScale
            Size_Height = whitebar.MoveFrameHeight if whitebar.move_state else whitebar.idleFrameHeight
            whitebar.Size(Size_Width, Size_Height)
        game_name.Scale(varReScale)


        # 타이틀 텍스트 이동
        if whitebar != None and whitebar.x + whitebar.Size_Width / 2 < 0:
            del(whitebar); whitebar = None
        elif whitebar != None:
            if whitebar.RUN_SPEED_KMPH_x != 0.0: whitebar.Set_moveSpeed(whitebar.RUN_SPEED_KMPH_x - 200 * GameTime.actiontime_frame)
            whitebar.Move()

        if game_name.x < 200: game_name.x = 200.0; game_name.Set_moveSpeed(0.0)
        game_name.Move()

    GameTime.update_time()
    delay(0.01)
    pass


def pause():
    pass


def resume():
    pass


