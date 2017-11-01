from pico2d import *
import game_framework
import main_state
import title_state
import Object

name = "MenuState"

menu1 = None
menu2 = None
whitebar1 = None
whitebar2 = None
info = None

actiontime_cur = 0.0
actiontime_frame = 0.0
actionstart = False

def enter():
    global menu1, menu2, whitebar1, whitebar2, info
    menu1 = Object.CObject(600.0, 650.0)
    menu1.Set_idleimage('Data\\Graphic\\Menu\\menu1.png')
    menu1.Set_moveimage('Data\\Graphic\\Menu\\menu1.png')
    menu1.Set_moveSpeed(0.0,-30.0)

    menu2 = Object.CObject(600.0, -80.0)
    menu2.Set_idleimage('Data\\Graphic\\Menu\\menu1.png')
    menu2.Set_moveimage('Data\\Graphic\\Menu\\menu1.png')
    menu2.Set_moveSpeed(0.0, 30.0)

    whitebar1 = Object.CObject(600.0, 630.0)
    whitebar1.Set_idleimage('Data\\Graphic\\Menu\\white_bar_mini.png')
    whitebar1.Set_moveimage('Data\\Graphic\\Menu\\white_bar_mini.png')
    whitebar1.Set_moveSpeed(0.0, -30.0)

    whitebar2 = Object.CObject(600.0, -50.0)
    whitebar2.Set_idleimage('Data\\Graphic\\Menu\\white_bar_mini.png')
    whitebar2.Set_moveimage('Data\\Graphic\\Menu\\white_bar_mini.png')
    whitebar2.Set_moveSpeed(0.0, 30.0)

    info = Object.CObject(400.0, 40.0)
    info.Set_idleimage('Data\\Graphic\\Menu\\info.png')

    pass


def exit():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.change_state(main_state)
    pass


def draw():
    clear_canvas()
    title_state.draw_title()


    update_canvas()
    pass


def update():
    title_state.update()
    global actiontime_cur, actiontime_frame, actionstart
    if not actionstart:
        actionstart = True
        actiontime_cur = get_time()


    actiontime_frame = get_time() - actiontime_cur
    actiontime_cur += actiontime_frame
    pass


def pause():
    pass


def resume():
    pass


