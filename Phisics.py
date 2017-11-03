from pico2d import *
import GameTime
import Object

GRAVITY = -9.8 * 3
FRICTION = 0.95

def Apply_GravityField(Object):
    global GRAVITY
    if GameTime.action_Factor() != 0.0:
        Object.RUN_SPEED_KMPH_y += (GRAVITY - Object.RUN_SPEED_KMPH_y) * 0.1 * GameTime.action_Factor()
    Object.Set_moveSpeed(Object.RUN_SPEED_KMPH_x, Object.RUN_SPEED_KMPH_y)


def Apply_Friction_X(Object):
    global FRICTION
    Object.RUN_SPEED_KMPH_x *= FRICTION# * GameTime.action_Factor()
    Object.Set_moveSpeed(Object.RUN_SPEED_KMPH_x, Object.RUN_SPEED_KMPH_y)


def Apply_Jump(Object, JumpSpeed):
    Object.RUN_SPEED_KMPH_y += JumpSpeed
    Object.Set_moveSpeed(Object.RUN_SPEED_KMPH_x, Object.RUN_SPEED_KMPH_y)


def Apply_Accelaration_X(Object, Accelaration, MaxSpeed):
    if abs(Object.RUN_SPEED_KMPH_x) < MaxSpeed:
        Object.RUN_SPEED_KMPH_x += Accelaration * GameTime.action_Factor()
    else:
        Object.RUN_SPEED_KMPH_x = (Accelaration / abs(Accelaration)) * MaxSpeed * GameTime.action_Factor()
    Object.Set_moveSpeed(Object.RUN_SPEED_KMPH_x, Object.RUN_SPEED_KMPH_y)