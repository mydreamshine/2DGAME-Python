import platform
import os

if platform.architecture()[0] == '32bit':
    os.environ["PYSDL2_DLL_PATH"] = ".\\SDL2\\x86"
else:
    os.environ["PYSDL2_DLL_PATH"] = ".\\SDL2\\x64"


from pico2d import *
import game_framework
import Object
import CollisionCheck
import Stage8
import title_state

open_canvas()
Object.Canvas_SIZE = CollisionCheck.Rect(0.0, get_canvas_height(), get_canvas_width(), 0.0)
Object.Ground_Size = CollisionCheck.Rect(0.0, get_canvas_height(), get_canvas_width(), 45.0)
game_framework.run(Stage8)
Object.DeleteCanvas()
close_canvas()