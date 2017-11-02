from pico2d import *
import game_framework
import GameTime
import Stage1
import title_state
import Object

name = "MenuState"

selector = None
accelaration_x = 14
maxVelocity = -10.0

menu1 = None
menu2 = None
whitebar1 = None
whitebar2 = None
info = None
fade = None
scrollmenu = False
NEWSTART, CONTINUE = 0, 1
select_into = NEWSTART


def DeleteObject():
    global fade, selector, menu1, menu2, whitebar1, whitebar2, info
    if fade != None: del(fade); fade = None
    if selector != None: del(selector); selector = None
    if menu1 != None: del(menu1); menu1 = None
    if menu2 != None: del (menu2); menu2 = None
    if whitebar1 != None: del (whitebar1); whitebar1 = None
    if whitebar2 != None: del (whitebar2); whitebar2 = None
    if info != None: del (info); info = None


def enter():
    GameTime.init_time()
    title_state.ReCreateObject()
    global accelaration_x
    global scrollmenu
    scrollmenu = True

    global fade, selector, menu1, menu2, whitebar1, whitebar2, info
    fade = Object.CObject(400.0, 300.0)
    fade.Apped_idleimage('Data\\Graphic\\Effect\\Fade.png')
    fade.Num_opacify = 0.0

    menu1 = Object.CObject(600.0, 650.0)
    menu1.Apped_idleimage('Data\\Graphic\\Menu\\menu1.png')
    menu1.Apped_idleimage('Data\\Graphic\\Menu\\menu1_select.png')
    menu1.Set_idleFrames(0)
    menu1.Apped_moveimage('Data\\Graphic\\Menu\\menu1.png')
    menu1.Set_moveSpeed(0.0,-35.0)

    selector = Object.CObject(menu1.x - menu1.Size_Width / 2 - 30, menu1.y)
    selector.Apped_idleimage('Data\\Graphic\\Menu\\selector.png')
    selector.Apped_moveimage('Data\\Graphic\\Menu\\selector.png')

    menu2 = Object.CObject(600.0, -80.0)
    menu2.Apped_idleimage('Data\\Graphic\\Menu\\menu2.png')
    menu2.Apped_idleimage('Data\\Graphic\\Menu\\menu2_select.png')
    menu2.Set_idleFrames(0)
    menu2.Apped_moveimage('Data\\Graphic\\Menu\\menu2.png')
    menu2.Set_moveSpeed(0.0, 50.0)

    whitebar1 = Object.CObject(600.0, 620.0)
    whitebar1.Apped_idleimage('Data\\Graphic\\Menu\\white_bar_mini.png')
    whitebar1.Apped_moveimage('Data\\Graphic\\Menu\\white_bar_mini.png')
    whitebar1.Set_moveSpeed(0.0, -40.0)

    whitebar2 = Object.CObject(600.0, -110.0)
    whitebar2.Apped_idleimage('Data\\Graphic\\Menu\\white_bar_mini.png')
    whitebar2.Apped_moveimage('Data\\Graphic\\Menu\\white_bar_mini.png')
    whitebar2.Set_moveSpeed(0.0, 45.0)

    info = Object.CObject(400.0, 40.0)
    info.Apped_idleimage('Data\\Graphic\\Menu\\info_menu.png')
    pass


def exit():
    title_state.DeleteObject()
    DeleteObject()
    pass


def handle_events():
    global fade, selector, menu1, menu2, whitebar1, whitebar2
    global select_into, NEWSTART, CONTINUE
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            title_state.DeleteObject()
            DeleteObject()
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            if selector.y == menu1.y + 10: select_into = NEWSTART
            elif selector.y == menu2.y + 10: select_into = CONTINUE
            if selector.y == menu1.y + 10 or selector.y == menu2.y + 10:
                menu1.Set_moveSpeed(0.0, 0.1)
                menu2.Set_moveSpeed(0.0, -0.1)
                whitebar1.Set_moveSpeed(0.0, 0.05)
                whitebar2.Set_moveSpeed(0.0, -0.05)
                fade.Active_Fade_In()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_UP:
            if not scrollmenu:
                selector.Set_Pos(menu1.x - menu1.Size_Width / 2 - 5, menu1.y + 10)
                selector.RUN_SPEED_KMPH_x = 0.0
                menu1.Set_idleFrames(1)
                menu2.Set_idleFrames(0)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_DOWN:
            if not scrollmenu:
                selector.Set_Pos(menu2.x - menu2.Size_Width / 2 - 5, menu2.y + 10)
                selector.RUN_SPEED_KMPH_x = 0.0
                menu1.Set_idleFrames(0)
                menu2.Set_idleFrames(1)
    pass


def draw():
    global fade, menu1, menu2, whitebar1, whitebar2, info, scrollmenu
    global select_into, NEWSTART, CONTINUE
    clear_canvas()
    title_state.draw_title()

    if fade != None and menu1 != None and menu2 != None and whitebar1 != None and whitebar2 != None and info != None:
        menu1.draw()
        menu2.draw()
        whitebar1.draw()
        whitebar2.draw()
        if menu1.RUN_SPEED_KMPH_y == 0.0 and menu2.RUN_SPEED_KMPH_y == 0.0 and whitebar1.RUN_SPEED_KMPH_y == 0.0 and whitebar2.RUN_SPEED_KMPH_y == 0.0:
            if scrollmenu:
                selector.Set_Pos(menu1.x - menu1.Size_Width / 2 - 5, menu1.y + 10)
                menu1.Set_idleFrames(1)
                scrollmenu = False
            selector.draw()
            info.draw()

        if fade.Fade_In:
            fade.draw()
        if fade.Num_opacify == 1.0:
            if select_into == NEWSTART: game_framework.change_state(Stage1)
    update_canvas()
    pass


def update():
    title_state.update()
    global fade, selector, menu1, menu2, whitebar1, whitebar2, info
    global accelaration_x, maxVelocity

    if selector != None and menu1 != None and menu2 != None and whitebar1 != None and whitebar2 != None and info != None:
        # 메뉴 이동
        add_speed = 30.0 if fade.Fade_In else 0.0
        if menu1.y < 400.0: menu1.y = 400.0; menu1.Set_moveSpeed(0.0, 0.0)
        elif menu1.RUN_SPEED_KMPH_y != 0.0:
            menu1.Set_moveSpeed(0.0, menu1.RUN_SPEED_KMPH_y + (19.0 + add_speed) * GameTime.actiontime_frame)
        menu1.Move()
        if menu2.y > 200.0: menu2.y = 200.0; menu2.Set_moveSpeed(0.0, 0.0)
        elif menu2.RUN_SPEED_KMPH_y != 0.0:
            menu2.Set_moveSpeed(0.0, menu2.RUN_SPEED_KMPH_y - (34.0 + add_speed) * GameTime.actiontime_frame)
        menu2.Move()

        if whitebar1.y < 370.0: whitebar1.y = 370.0; whitebar1.Set_moveSpeed(0.0, 0.0)
        elif whitebar1.RUN_SPEED_KMPH_y != 0.0:
            whitebar1.Set_moveSpeed(0.0, whitebar1.RUN_SPEED_KMPH_y + (25.0 + add_speed) * GameTime.actiontime_frame)
        whitebar1.Move()
        if whitebar2.y > 170.0: whitebar2.y = 170.0; whitebar2.Set_moveSpeed(0.0, 0.0)
        elif whitebar2.RUN_SPEED_KMPH_y != 0.0:
            whitebar2.Set_moveSpeed(0.0, whitebar2.RUN_SPEED_KMPH_y - (28.0 + add_speed) * GameTime.actiontime_frame)
        whitebar2.Move()

        # fade 활성화
        fade.Set_ActiveTime()

        # Selector 좌우 이동
        if not scrollmenu:
            if selector.RUN_SPEED_KMPH_x < maxVelocity:
                selector.RUN_SPEED_KMPH_x *= -1
            if selector.RUN_SPEED_KMPH_x >= 0.0 and selector.RUN_SPEED_KMPH_x - accelaration_x * GameTime.actiontime_frame < 0.0:
                if selector.y == menu1.y + 10: selector.Set_Pos(menu1.x - menu1.Size_Width / 2 - 5, menu1.y + 10)
                elif selector.y == menu2.y + 10: selector.Set_Pos(menu2.x - menu2.Size_Width / 2 - 5, menu2.y + 10)
            selector.Set_moveSpeed(selector.RUN_SPEED_KMPH_x - accelaration_x * GameTime.actiontime_frame)
            selector.Move()
    pass


def pause():
    pass


def resume():
    pass


