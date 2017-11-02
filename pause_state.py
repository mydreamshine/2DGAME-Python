from pico2d import *
import game_framework
import Object

name = "PauseState"
font = None


def enter():
    global font
    font = Object.CObject(400.0, 310.0)
    font.Apped_idleimage('Data\\Graphic\\Effect\\PAUSE.png')
    pass


def DeleteObject():
    global font
    del (font)


def exit():
    DeleteObject()
    pass


def pause():
    pass


def resume():
    pass


def handle_events():
    global boy
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.pop_state()
    pass


def update():
    global font
    game_framework.stack[-2].update_ActiveTime()
    pass


def draw():
    global font
    clear_canvas()
    game_framework.stack[-2].Scene_draw()
    font.draw()
    update_canvas()
    delay(0.01)
    pass