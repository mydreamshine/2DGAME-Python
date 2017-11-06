from pico2d import *
import game_framework
import Object
import GameTime
import GameMusic

name = "GameOverState"
gameover = None
background1 = None
background2 = None
menu = None
whitebar = None
fade = None
scrollmenu = True

selector = None
accelaration_x = 14
maxVelocity = -10.0

def DeleteObject():
    GameMusic.Delete()
    global gameover, fade, background1, background2, whitebar, menu, selector
    if gameover != None: del (gameover); gameover = None
    if background1 != None: del (background1); background1 = None
    if background2 != None: del (background2); background2 = None
    if whitebar != None: del (whitebar); whitebar = None
    if fade != None: del (fade); fade = None
    if selector != None: del(selector); selector = None
    if menu != None: del (menu); menu = None


def enter():
    GameTime.init_time()
    GameMusic.Play_GameOver()

    global gameover, fade, background1, background2, whitebar, menu, scrollmenu, selector

    fade = Object.CObject(400.0, 300.0)
    fade.Apped_idleimage('Data\\Graphic\\Effect\\Fade.png')
    fade.Active_Fade_Out()

    gameover = Object.CObject(400.0, 300.0)
    gameover.Apped_idleimage('Data\\Graphic\\Menu\\game_over.png')

    background1 = Object.CObject(400.0, 300.0)
    background1.Apped_moveimage('Data\\Graphic\\Background\\title.png')
    background1.Set_moveSpeed(-8.0)
    background1.nonFriction = True

    right = background1.x + background1.Size_Width

    background2 = Object.CObject(right, 300.0)
    background2.Apped_moveimage('Data\\Graphic\\Background\\title.png')
    background2.Set_moveSpeed(-8.0)
    background2.nonFriction = True

    whitebar = Object.CObject(600.0, -210.0)
    whitebar.Apped_idleimage('Data\\Graphic\\Menu\\white_bar_mini.png')
    whitebar.Apped_moveimage('Data\\Graphic\\Menu\\white_bar_mini.png')
    whitebar.Set_moveSpeed(0.0, 45.0)

    scrollmenu = True
    menu = Object.CObject(600.0, -180.0)
    menu.Apped_idleimage('Data\\Graphic\\Menu\\menu2.png')
    menu.Apped_idleimage('Data\\Graphic\\Menu\\menu2_select.png')
    menu.Set_idleFrames(0)
    menu.Apped_moveimage('Data\\Graphic\\Menu\\menu2.png')
    menu.Set_moveSpeed(0.0, 50.0)

    selector = Object.CObject(menu.x - menu.Size_Width / 2 - 30, menu.y)
    selector.Apped_idleimage('Data\\Graphic\\Menu\\selector.png')
    selector.Apped_moveimage('Data\\Graphic\\Menu\\selector.png')
    selector.nonFriction = True
    pass


def exit():
    DeleteObject()
    pass


def handle_events():
    global whitebar, menu, selector
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            if selector.y == menu.y + 10 and not fade.Fade_Out:
                menu.Set_moveSpeed(0.0, -0.1)
                whitebar.Set_moveSpeed(0.0, -0.05)
                fade.Active_Fade_In()
    pass


def draw():
    global gameover, fade, background1, background2, whitebar, menu, scrollmenu, selector
    clear_canvas()

    if gameover != None and fade != None and background1 != None and background2 != None and whitebar != None and menu != None and selector != None:
        background1.draw()
        background2.draw()
        gameover.draw()
        menu.draw()
        whitebar.draw()

        # 메뉴 Selector
        if whitebar.RUN_SPEED_KMPH_y == 0.0 and menu.RUN_SPEED_KMPH_y == 0.0:
            if scrollmenu:
                selector.Set_Pos(menu.x - menu.Size_Width / 2 - 5, menu.y + 10)
                menu.Set_idleFrames(1)
                scrollmenu = False
            selector.draw()

        # Fade
        prevFade_In = fade.Fade_In
        if fade.Fade_In or fade.Fade_Out:
            fade.draw()
        # Fade상태에 따른 게임씬(Scene) 탈출
        if prevFade_In and not fade.Fade_In:
            game_framework.pop_state()
            if len(game_framework.stack) > 0:
                game_framework.stack[-1].DeleteObject()
                game_framework.stack[-1].enter()

    update_canvas()
    pass


def update():
    global fade, background1, background2, whitebar, menu, scrollmenu, selector
    global accelaration_x, maxVelocity

    if fade != None and background1 != None and background2 != None and whitebar != None and menu != None and selector != None:
        # 배경 횡스크롤링
        background1.Move()
        background2.Move()
        if background1.x + background1.Size_Width / 2 < 0:
            right = background2.x + background2.Size_Width
            background1.Set_Pos(right, background1.y)
        elif background2.x + background2.Size_Width / 2 < 0:
            right = background1.x + background1.Size_Width
            background2.Set_Pos(right, background2.y)

        # 메뉴 이동
        add_speed = 30.0 if fade.Fade_In else 0.0
        if menu.y > 100.0: menu.y = 100.0; menu.Set_moveSpeed(0.0, 0.0)
        elif menu.RUN_SPEED_KMPH_y != 0.0:
            menu.Set_moveSpeed(0.0, menu.RUN_SPEED_KMPH_y - (27.0 + add_speed) * GameTime.actiontime_frame)
        menu.Move()
        if whitebar.y > 70.0: whitebar.y = 70.0; whitebar.Set_moveSpeed(0.0, 0.0)
        elif whitebar.RUN_SPEED_KMPH_y != 0.0:
            whitebar.Set_moveSpeed(0.0, whitebar.RUN_SPEED_KMPH_y - (23.0 + add_speed) * GameTime.actiontime_frame)
        whitebar.Move()

        # fade 활성화
        fade.Set_ActiveTime()

        # Selector 좌우 이동
        if not scrollmenu:
            if selector.RUN_SPEED_KMPH_x < maxVelocity:
                selector.RUN_SPEED_KMPH_x = -maxVelocity
            if selector.RUN_SPEED_KMPH_x >= 0.0 and selector.RUN_SPEED_KMPH_x - accelaration_x * GameTime.actiontime_frame < 0.0:
                selector.Set_Pos(menu.x - menu.Size_Width / 2 - 5, menu.y + 10)
            selector.Set_moveSpeed(selector.RUN_SPEED_KMPH_x - accelaration_x * GameTime.actiontime_frame)
            selector.Move()

    GameTime.update_time()
    delay(0.01)
    pass


def pause():
    pass


def resume():
    pass