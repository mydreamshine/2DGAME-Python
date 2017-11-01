from pico2d import *
import pygame
import game_framework
import main_state
import title_state
import Object

name = "MenuState"

selector = None
velocity_x = 0.0
accelaration_x = 0.07
Speed = 0.0
maxVelocity = -10.0

menu1 = None
menu2 = None
whitebar1 = None
whitebar2 = None
info = None
scrollmenu = False

actiontime_cur = 0.0
actiontime_frame = 0.0


def DeleteObject():
    global selector, menu1, menu2, whitebar1, whitebar2, info
    if selector != None: del(selector); selector = None
    if title_state.BGM != None:
        title_state.BGM.stop()
        del(title_state.BGM); title_state.BGM = None
    if menu1 != None: del(menu1); menu1 = None
    if menu2 != None: del (menu2); menu2 = None
    if whitebar1 != None: del (whitebar1); whitebar1 = None
    if whitebar2 != None: del (whitebar2); whitebar2 = None
    if info != None: del (info); info = None


def enter():
    global velocity_x, accelaration_x, Speed
    global scrollmenu
    scrollmenu = True

    global selector, menu1, menu2, whitebar1, whitebar2, info
    if title_state.BGM == None:
        pygame.init()
        pygame.mixer.init()
        title_state.BGM = pygame.mixer.Sound('Data\\Sound\\title_bgm.wav')
        title_state.BGM.play()

    menu1 = Object.CObject(600.0, 650.0)
    menu1.Apped_idleimage('Data\\Graphic\\Menu\\menu1.png')
    menu1.Apped_idleimage('Data\\Graphic\\Menu\\menu1_select.png')
    menu1.Set_idleFrames(0)
    menu1.Apped_moveimage('Data\\Graphic\\Menu\\menu1.png')
    menu1.Set_moveSpeed(0.0,-35.0)

    selector = Object.CObject(menu1.x - menu1.Size_Width / 2 - 30, menu1.y)
    selector.Apped_idleimage('Data\\Graphic\\Menu\\selector.png')
    selector.Apped_moveimage('Data\\Graphic\\Menu\\selector.png')
    velocity_x = 0.0
    accelaration_x = 0.06
    Speed = 0.0

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

    global actiontime_cur
    title_state.actiontime_cur = get_time()
    actiontime_cur = get_time()

    pass


def exit():
    DeleteObject()
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            title_state.DeleteObject()
            DeleteObject()
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            if selector.y == menu1.y + 10:
                game_framework.change_state(main_state)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_UP:
            if not scrollmenu:
                selector.Set_Pos(menu1.x - menu1.Size_Width / 2 - 30, menu1.y + 10)
                menu1.Set_idleFrames(1)
                menu2.Set_idleFrames(0)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_DOWN:
            if not scrollmenu:
                selector.Set_Pos(menu2.x - menu2.Size_Width / 2 - 30, menu2.y + 10)
                menu1.Set_idleFrames(0)
                menu2.Set_idleFrames(1)
    pass


def draw():
    global menu1, menu2, whitebar1, whitebar2, info, scrollmenu
    clear_canvas()
    title_state.draw_title()

    if menu1 != None and menu2 != None and whitebar1 != None and whitebar2 != None and info != None:
        menu1.draw()
        menu2.draw()
        whitebar1.draw()
        whitebar2.draw()
        if menu1.RUN_SPEED_KMPH_y == 0.0 and menu2.RUN_SPEED_KMPH_y == 0.0 and whitebar1.RUN_SPEED_KMPH_y == 0.0 and whitebar2.RUN_SPEED_KMPH_y == 0.0:
            if scrollmenu:
                selector.Set_Pos(menu1.x - menu1.Size_Width / 2 - 10, menu1.y + 10)
                menu1.Set_idleFrames(1)
                scrollmenu = False
            selector.draw()
            info.draw()

    update_canvas()
    pass


def update():
    title_state.update()
    global selector, menu1, menu2, whitebar1, whitebar2, info
    global actiontime_cur, actiontime_frame
    global velocity_x, accelaration_x, maxVelocity, Speed


    if selector != None and menu1 != None and menu2 != None and whitebar1 != None and whitebar2 != None and info != None:
        # 메뉴 이동
        if menu1.y < 400.0: menu1.y = 400.0; menu1.Set_moveSpeed(0.0, 0.0)
        elif menu1.RUN_SPEED_KMPH_y < 0.0:
            menu1.Set_moveSpeed(0.0, menu1.RUN_SPEED_KMPH_y + 22.5 * actiontime_frame)
            menu1.Move()
        if menu2.y > 200.0: menu2.y = 200.0; menu2.Set_moveSpeed(0.0, 0.0)
        elif menu2.RUN_SPEED_KMPH_y > 0.0:
            menu2.Set_moveSpeed(0.0, menu2.RUN_SPEED_KMPH_y - 40 * actiontime_frame)
            menu2.Move()

        if whitebar1.y < 370.0: whitebar1.y = 370.0; whitebar1.Set_moveSpeed(0.0, 0.0)
        elif whitebar1.RUN_SPEED_KMPH_y < 0.0:
            whitebar1.Set_moveSpeed(0.0, whitebar1.RUN_SPEED_KMPH_y + 29 * actiontime_frame)
            whitebar1.Move()
        if whitebar2.y > 170.0: whitebar2.y = 170.0; whitebar2.Set_moveSpeed(0.0, 0.0)
        elif whitebar2.RUN_SPEED_KMPH_y > 0.0:
            whitebar2.Set_moveSpeed(0.0, whitebar2.RUN_SPEED_KMPH_y - 32.5 * actiontime_frame)
            whitebar2.Move()

        # Selector 좌우 이동
        if not scrollmenu:
            if Speed < maxVelocity or (Speed + (velocity_x if Speed < 0.0 else -velocity_x) * actiontime_frame < 0.0 and Speed > 0.0):
                Speed = maxVelocity if Speed < maxVelocity else 0.0
                Speed *= -1
                velocity_x *= -1
            else: velocity_x -= accelaration_x
            Speed += (velocity_x if Speed <= 0.0 and velocity_x < 0.0 else -velocity_x) * actiontime_frame
            print("velocity_x:", velocity_x)
            print("Speed:", Speed)
            selector.Set_moveSpeed(Speed, 0.0)
            selector.Move()


    actiontime_frame = get_time() - actiontime_cur
    actiontime_cur += actiontime_frame
    pass


def pause():
    pass


def resume():
    pass


