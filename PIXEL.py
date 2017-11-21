from pico2d import *
import game_framework
import Object
import CollisionCheck
#import Stage1
#import Stage2
#import Stage3
import title_state

open_canvas()
Object.Canvas_SIZE = CollisionCheck.Rect(0.0, get_canvas_height(), get_canvas_width(), 0.0)
Object.Ground_Size = CollisionCheck.Rect(0.0, get_canvas_height(), get_canvas_width(), 45.0)
game_framework.run(title_state)
Object.DeleteCanvas()
close_canvas()