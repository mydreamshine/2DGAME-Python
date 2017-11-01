from pico2d import *
import winsound
import game_framework
import menu_state
import Object


name = "TitleState"
background1 = None
background2 = None
whitebar = None
game_name = None
varScale = 1.0
varReScale = 1.0
velocity_Scale = 0.0
accelaration_Scale = 0.0022
MaxScale = 1.2

actiontime_cur = 0.0
actiontime_frame = 0.0
actionstart = False

def DeleteObject():
    global background1, background2, whitebar, game_name
    if background1 != None: del (background1)
    if background2 != None: del (background2)
    if whitebar != None: del (whitebar)
    if game_name != None: del (game_name)


def enter():
    winsound.PlaySound('Data\\Sound\\title_bgm.wav', winsound.SND_ASYNC | winsound.SND_LOOP)
    global background1, background2, whitebar, game_name
    background1 = Object.CObject(400.0, 300.0)
    background1.Set_moveimage('Data\\Graphic\\Background\\title.png')
    background1.Set_moveSpeed(-8.0)

    right = background1.x + background1.Size_Width

    background2 = Object.CObject(right, 300.0)
    background2.Set_moveimage('Data\\Graphic\\Background\\title.png')
    background2.Set_moveSpeed(-8.0)

    whitebar = Object.CObject(400.0, 465.0)
    whitebar.Set_idleimage('Data\\Graphic\\Menu\\white_bar.png')
    whitebar.Set_moveimage('Data\\Graphic\\Menu\\white_bar.png')

    game_name = Object.CObject(400.0, 300.0)
    game_name.Set_idleimage('Data\\Graphic\\Menu\\game_name.png')
    game_name.Set_moveimage('Data\\Graphic\\Menu\\game_name.png')
    pass


def exit():
    pass


def handle_events():
    global whitebar, game_name
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            DeleteObject
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            winsound.SND_PURGE
            game_name.Set_moveSpeed(-30.0)
            whitebar.Set_moveSpeed(-40.0)
            game_framework.change_state(menu_state)
    pass

def draw_title():
    # 타이틀 배경
    background1.draw()
    background2.draw()

    # 타이틀 메뉴 테두리
    whitebar.draw()
    whitebar.Set_Pos(400.0, 134.0)
    whitebar.draw()
    whitebar.Set_Pos(400.0, 465.0)

    # 게임 이름 텍스트
    game_name.draw()

def draw():
    global background1, background2, whitebar, game_name
    clear_canvas()
    draw_title()
    update_canvas()
    pass

def update():
    global background1, background2, whitebar, game_name
    global MaxScale, varScale, varReScale, velocity_Scale, accelaration_Scale
    global actiontime_cur, actiontime_frame, actionstart
    if not actionstart:
        actionstart = True
        actiontime_cur = get_time()

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
    else: velocity_Scale += accelaration_Scale
    varScale += velocity_Scale * actiontime_frame
    varReScale -= velocity_Scale * actiontime_frame
    if whitebar != None:
        Size_Width = (whitebar.MoveFrameWidth if whitebar.move_state else whitebar.idleFrameWidth) * varScale
        Size_Height = whitebar.MoveFrameHeight if whitebar.move_state else whitebar.idleFrameHeight
        whitebar.Size(Size_Width, Size_Height)
    game_name.Scale(varReScale)

    #타이틀 텍스트 이동
    if whitebar != None and whitebar.x + whitebar.Size_Width / 2 < 0: del(whitebar); whitebar = None
    else:
        whitebar.Move()

    if game_name.x < 200: game_name.x = 200.0; game_name.Set_moveSpeed(0.0)
    else: game_name.Move()


    actiontime_frame = get_time() - actiontime_cur
    actiontime_cur += actiontime_frame
    pass


def pause():
    pass


def resume():
    pass


