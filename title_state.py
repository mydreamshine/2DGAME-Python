from pico2d import *
import game_framework
import main_state
import Object

name = "TitleState"
background = None


def enter():
    global background
    background = Object.CObject(400, 300)
    background.Set_idleimage('Data\\Graphic\\Background\\title.png')
    pass


def exit():
    global background
    del(background)
    clear_canvas()
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
    global image
    clear_canvas()
    background.draw()
    update_canvas()
    pass


def update():
    pass


def pause():
    pass


def resume():
    pass


