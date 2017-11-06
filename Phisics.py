from pico2d import *
import GameTime
import Object

GRAVITY = -9.8 * 2
FRICTION = 0.98

Acceleration = 2.0
MaxSpeed = 30.0
JumpSpeed = 100.0

def Apply_GravityField(Object):
    global GRAVITY
    if GameTime.action_Factor() != 0.0:
        Object.RUN_SPEED_KMPH_y += (GRAVITY - Object.RUN_SPEED_KMPH_y) * 0.1 * GameTime.action_Factor()
    Object.Set_moveSpeed(Object.RUN_SPEED_KMPH_x, Object.RUN_SPEED_KMPH_y)


def Apply_Friction_X(Object):
    global FRICTION
    Object.RUN_SPEED_KMPH_x *= FRICTION# * GameTime.action_Factor()
    Object.Set_moveSpeed(Object.RUN_SPEED_KMPH_x, Object.RUN_SPEED_KMPH_y)


def Apply_Jump(Object):
    global JumpSpeed
    Object.RUN_SPEED_KMPH_y += JumpSpeed
    Object.Set_moveSpeed(Object.RUN_SPEED_KMPH_x, Object.RUN_SPEED_KMPH_y)


def Apply_Accelaration_X(Object, Direction):
    global Acceleration, MaxSpeed
    if abs(Object.RUN_SPEED_KMPH_x) < MaxSpeed:
        Object.RUN_SPEED_KMPH_x += Direction * Acceleration * GameTime.action_Factor()
    else:
        Object.RUN_SPEED_KMPH_x = Direction * MaxSpeed * GameTime.action_Factor()
    Object.Set_moveSpeed(Object.RUN_SPEED_KMPH_x, Object.RUN_SPEED_KMPH_y)